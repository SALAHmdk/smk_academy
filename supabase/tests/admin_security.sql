-- Tests de l'espace administrateur (rôle + MFA aal2, garde-fous, journal). Tout est annulé à la fin.
do $$
declare
  v_student uuid := gen_random_uuid();
  v_admin uuid := gen_random_uuid();
  v_cat uuid := (select id from public.categories where slug = 'programmation');
  v_course uuid;
  v_module uuid;
  v_lesson uuid;
  v_quiz uuid;
  v_q uuid;
  v_o1 uuid;
  v_o2 uuid;
  v_count integer;
  report text := '';
begin
  insert into auth.users (id, instance_id, aud, role, email, created_at, updated_at) values
    (v_student, '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated', 'stu@smk.test', now(), now()),
    (v_admin, '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated', 'adm@smk.test', now(), now());
  update public.profiles set role = 'admin' where id = v_admin;

  -- Étudiant (même avec une session aal2) -------------------------------------
  perform set_config('request.jwt.claims', json_build_object('sub', v_student, 'role', 'authenticated', 'aal', 'aal2')::text, true);
  perform set_config('role', 'authenticated', true);
  begin
    insert into public.courses (slug, title, category_id, level) values ('pirate', 'Pirate', v_cat, 'debutant');
    report := report || 'FAIL étudiant : création de formation' || chr(10);
  exception when insufficient_privilege then report := report || 'PASS étudiant : création de formation refusée' || chr(10);
  end;
  update public.courses set title = 'Piraté' where slug = 'python-debutant';
  get diagnostics v_count = row_count;
  report := report || case when v_count = 0 then 'PASS' else 'FAIL' end || ' étudiant : modification d''une formation sans effet (RLS)' || chr(10);
  begin
    perform public.admin_stats();
    report := report || 'FAIL étudiant : statistiques admin' || chr(10);
  exception when insufficient_privilege then report := report || 'PASS étudiant : statistiques admin refusées' || chr(10);
  end;
  begin
    perform public.admin_get_answer_keys('5e138572-4d1c-5200-b7bc-b707fe41a1a3');
    report := report || 'FAIL étudiant : lecture des corrigés via RPC' || chr(10);
  exception when insufficient_privilege then report := report || 'PASS étudiant : corrigés via RPC refusés' || chr(10);
  end;
  begin
    perform public.admin_set_answer_key('4d482a46-cdc9-5a2d-af30-f6697f046f49', array['69a6177c-7d2b-5855-aa10-c7f9b128d95c']::uuid[], 'x');
    report := report || 'FAIL étudiant : modification d''un corrigé' || chr(10);
  exception when insufficient_privilege then report := report || 'PASS étudiant : modification d''un corrigé refusée' || chr(10);
  end;
  begin
    perform private.set_role('stu@smk.test', 'admin');
    report := report || 'FAIL étudiant : auto-promotion admin' || chr(10);
  exception when insufficient_privilege then report := report || 'PASS étudiant : auto-promotion admin refusée' || chr(10);
  end;

  -- Administrateur SANS double authentification (aal1) -----------------------
  perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated', 'aal', 'aal1')::text, true);
  begin
    insert into public.courses (slug, title, category_id, level) values ('test-aal1', 'Test', v_cat, 'debutant');
    report := report || 'FAIL admin aal1 : création possible sans MFA' || chr(10);
  exception when insufficient_privilege then report := report || 'PASS admin aal1 : création refusée sans MFA' || chr(10);
  end;
  begin
    perform public.admin_stats();
    report := report || 'FAIL admin aal1 : statistiques sans MFA' || chr(10);
  exception when insufficient_privilege then report := report || 'PASS admin aal1 : statistiques refusées sans MFA' || chr(10);
  end;

  -- Administrateur AVEC double authentification (aal2) -----------------------
  perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated', 'aal', 'aal2')::text, true);
  insert into public.courses (slug, title, category_id, level) values ('test-admin', 'Test admin', v_cat, 'debutant') returning id into v_course;
  report := report || 'PASS admin aal2 : brouillon créé' || chr(10);

  begin
    update public.courses set status = 'published' where id = v_course;
    report := report || 'FAIL garde-fou : formation vide publiée' || chr(10);
  exception when raise_exception then report := report || 'PASS garde-fou : formation vide non publiable' || chr(10);
  end;

  insert into public.modules (course_id, title, position) values (v_course, 'M1', 1) returning id into v_module;
  begin
    update public.modules set status = 'published' where id = v_module;
    report := report || 'FAIL garde-fou : module vide publié' || chr(10);
  exception when raise_exception then report := report || 'PASS garde-fou : module sans leçon non publiable' || chr(10);
  end;

  insert into public.lessons (module_id, slug, title, content_md, position) values (v_module, 'l1', 'L1', 'Contenu', 1) returning id into v_lesson;
  insert into public.quizzes (module_id, title) values (v_module, 'Q') returning id into v_quiz;
  insert into public.quiz_questions (quiz_id, position, kind, prompt) values (v_quiz, 1, 'single', 'Question ?') returning id into v_q;
  insert into public.quiz_options (question_id, position, label) values (v_q, 1, 'A') returning id into v_o1;
  insert into public.quiz_options (question_id, position, label) values (v_q, 2, 'B') returning id into v_o2;
  begin
    update public.modules set status = 'published' where id = v_module;
    report := report || 'FAIL garde-fou : question sans corrigé publiée' || chr(10);
  exception when raise_exception then report := report || 'PASS garde-fou : question sans corrigé non publiable' || chr(10);
  end;

  begin
    perform public.admin_set_answer_key(v_q, array[v_o1, v_o2], 'deux réponses pour une question simple');
    report := report || 'FAIL corrigé : 2 réponses acceptées pour une question simple' || chr(10);
  exception when invalid_parameter_value then report := report || 'PASS corrigé : une seule réponse pour une question simple' || chr(10);
  end;
  begin
    perform public.admin_set_answer_key(v_q, array['4d482a46-cdc9-5a2d-af30-f6697f046f49']::uuid[], 'option étrangère');
    report := report || 'FAIL corrigé : option d''une autre question acceptée' || chr(10);
  exception when invalid_parameter_value then report := report || 'PASS corrigé : option étrangère refusée' || chr(10);
  end;
  perform public.admin_set_answer_key(v_q, array[v_o2], 'B est juste.');
  update public.modules set status = 'published' where id = v_module;
  update public.courses set status = 'published' where id = v_course;
  select count(*) into v_count from public.courses where id = v_course and status = 'published';
  report := report || case when v_count = 1 then 'PASS' else 'FAIL' end || ' admin aal2 : module complet puis formation publiés' || chr(10);

  select count(*) into v_count from public.admin_audit_log(50) where actor_email = 'adm@smk.test';
  report := report || case when v_count >= 8 then 'PASS' else 'FAIL' end || ' journal d''audit : ' || v_count || ' actions de l''admin tracées' || chr(10);

  -- L'étudiant voit la nouvelle formation publiée mais pas un brouillon ------
  perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated', 'aal', 'aal2')::text, true);
  insert into public.courses (slug, title, category_id, level) values ('brouillon-secret', 'Secret', v_cat, 'debutant');
  perform set_config('request.jwt.claims', json_build_object('sub', v_student, 'role', 'authenticated', 'aal', 'aal1')::text, true);
  select count(*) into v_count from public.courses where slug in ('test-admin', 'brouillon-secret');
  report := report || case when v_count = 1 then 'PASS' else 'FAIL' end || ' étudiant : voit la formation publiée, pas le brouillon' || chr(10);
  perform set_config('request.jwt.claims', '{"role":"anon"}', true);
  perform set_config('role', 'anon', true);
  select count(*) into v_count from public.courses where status = 'draft';
  report := report || case when v_count = 0 then 'PASS' else 'FAIL' end || ' visiteur : aucun brouillon visible' || chr(10);

  raise exception 'RAPPORT (rollback)%', chr(10) || report;
end;
$$;
