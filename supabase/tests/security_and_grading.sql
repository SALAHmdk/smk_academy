-- Tests de sécurité et de notation SMK Academy.
-- Exécution : coller dans l'éditeur SQL Supabase (ou via MCP execute_sql).
-- Le bloc se termine TOUJOURS par une exception qui annule tout : aucune donnée n'est conservée.
-- Le message de l'exception contient le rapport : chaque ligne PASS/FAIL.

do $$
declare
  v_a uuid := gen_random_uuid();
  v_b uuid := gen_random_uuid();
  v_quiz uuid := '5e138572-4d1c-5200-b7bc-b707fe41a1a3';
  v_lesson uuid := '32ccfaee-b4c9-537b-ae27-01b54d7c1d0e';
  v_all_correct jsonb := '{}'::jsonb;
  v_half jsonb := '{}'::jsonb;
  v_wrong_option uuid;
  r record;
  i integer := 0;
  v_attempt public.quiz_attempts;
  v_count integer;
  v_text text;
  report text := '';
  procedure_ok boolean;
begin
  -- Préparation (rôle postgres) ---------------------------------------------
  insert into auth.users (id, instance_id, aud, role, email, raw_user_meta_data, created_at, updated_at)
  values
    (v_a, '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated', 'test-a@smk.test', '{"full_name":"Étudiant A"}', now(), now()),
    (v_b, '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated', 'test-b@smk.test', '{}', now(), now());

  select count(*) into v_count from public.profiles where id = v_a and full_name = 'Étudiant A' and role = 'student';
  report := report || case when v_count = 1 then 'PASS' else 'FAIL' end || ' trigger: profil créé avec rôle student' || chr(10);

  -- Construit une copie « toutes bonnes réponses » et une « moitié juste ».
  for r in
    select qq.id, qq.position, k.correct_option_ids
    from public.quiz_questions qq join private.quiz_answer_keys k on k.question_id = qq.id
    where qq.quiz_id = v_quiz order by qq.position
  loop
    i := i + 1;
    v_all_correct := v_all_correct || jsonb_build_object(r.id::text, to_jsonb(r.correct_option_ids));
    if i <= 5 then
      v_half := v_half || jsonb_build_object(r.id::text, to_jsonb(r.correct_option_ids));
    else
      select o.id into v_wrong_option from public.quiz_options o
      where o.question_id = r.id and not (o.id = any (r.correct_option_ids)) limit 1;
      v_half := v_half || jsonb_build_object(r.id::text, jsonb_build_array(v_wrong_option));
    end if;
  end loop;

  -- Étudiant A ---------------------------------------------------------------
  perform set_config('request.jwt.claims', json_build_object('sub', v_a, 'role', 'authenticated')::text, true);
  perform set_config('role', 'authenticated', true);

  begin
    perform 1 from private.quiz_answer_keys limit 1;
    report := report || 'FAIL lecture des corrigés autorisée' || chr(10);
  exception when insufficient_privilege then
    report := report || 'PASS corrigés (private.quiz_answer_keys) inaccessibles' || chr(10);
  end;

  begin
    update public.profiles set role = 'admin' where id = v_a;
    report := report || 'FAIL un étudiant peut devenir admin' || chr(10);
  exception when insufficient_privilege then
    report := report || 'PASS impossible de modifier son rôle' || chr(10);
  end;

  begin
    update public.profiles set plan = 'premium' where id = v_a;
    report := report || 'FAIL un étudiant peut passer Premium seul' || chr(10);
  exception when insufficient_privilege then
    report := report || 'PASS impossible de modifier son offre' || chr(10);
  end;

  update public.profiles set full_name = 'Nouveau nom' where id = v_a;
  select count(*) into v_count from public.profiles where id = v_a and full_name = 'Nouveau nom';
  report := report || case when v_count = 1 then 'PASS' else 'FAIL' end || ' modification de son nom autorisée' || chr(10);

  begin
    insert into public.quiz_attempts (user_id, quiz_id, points, max_points, score_20, passed, corrections)
    values (v_a, v_quiz, 20, 20, 20, true, '[]');
    report := report || 'FAIL insertion directe d''une note 20/20 acceptée' || chr(10);
  exception when insufficient_privilege then
    report := report || 'PASS insertion directe de note refusée' || chr(10);
  end;

  select count(*) into v_count from public.quiz_options o
    join public.quiz_questions qq on qq.id = o.question_id where qq.quiz_id = v_quiz;
  report := report || case when v_count = 36 then 'PASS' else 'FAIL' end || ' options du quiz lisibles (' || v_count || ')' || chr(10);

  v_attempt := public.submit_quiz(v_quiz, v_all_correct);
  report := report || case when v_attempt.score_20 = 20 and v_attempt.passed then 'PASS' else 'FAIL' end
    || ' toutes bonnes réponses → ' || v_attempt.score_20 || '/20' || chr(10);

  v_attempt := public.submit_quiz(v_quiz, v_half);
  report := report || case when v_attempt.score_20 = 10 and v_attempt.passed then 'PASS' else 'FAIL' end
    || ' moitié juste → ' || v_attempt.score_20 || '/20 (seuil 10 atteint)' || chr(10);

  v_attempt := public.submit_quiz(v_quiz, '{}'::jsonb);
  report := report || case when v_attempt.score_20 = 0 and not v_attempt.passed then 'PASS' else 'FAIL' end
    || ' copie vide → ' || v_attempt.score_20 || '/20, non validé' || chr(10);

  -- Tricher en cochant toutes les options d'une question à choix multiples ne rapporte rien.
  select jsonb_object_agg(qq.id::text, (select jsonb_agg(o.id) from public.quiz_options o where o.question_id = qq.id))
    into v_half
  from public.quiz_questions qq where qq.quiz_id = v_quiz;
  v_attempt := public.submit_quiz(v_quiz, v_half);
  report := report || case when v_attempt.score_20 = 0 then 'PASS' else 'FAIL' end
    || ' cocher toutes les options → ' || v_attempt.score_20 || '/20' || chr(10);

  -- Options d'une autre question / identifiants fantaisistes ignorés.
  v_attempt := public.submit_quiz(v_quiz, jsonb_build_object('pas-un-uuid', jsonb_build_array('x'), v_lesson::text, jsonb_build_array(v_lesson)));
  report := report || case when v_attempt.score_20 = 0 then 'PASS' else 'FAIL' end || ' réponses forgées ignorées' || chr(10);

  begin
    perform public.submit_quiz(v_quiz, '[]'::jsonb);
    report := report || 'FAIL format tableau accepté' || chr(10);
  exception when invalid_parameter_value then
    report := report || 'PASS format de réponses invalide rejeté' || chr(10);
  end;

  select jsonb_array_length(corrections), (corrections -> 0 ? 'explanation') into v_count, procedure_ok
  from public.quiz_attempts where user_id = v_a order by created_at desc limit 1;
  report := report || case when v_count = 10 and procedure_ok then 'PASS' else 'FAIL' end || ' correction détaillée (10 questions + explications)' || chr(10);

  perform public.complete_lesson(v_lesson);
  perform public.complete_lesson(v_lesson);  -- idempotent
  select count(*) into v_count from public.lesson_progress where user_id = v_a;
  report := report || case when v_count = 1 then 'PASS' else 'FAIL' end || ' leçon terminée enregistrée (idempotent)' || chr(10);

  select count(*) into v_count from public.enrollments where user_id = v_a and last_lesson_id = v_lesson;
  report := report || case when v_count = 1 then 'PASS' else 'FAIL' end || ' inscription + dernière leçon mémorisées' || chr(10);

  select count(*) into v_count from public.quiz_attempts where user_id = v_a;
  report := report || case when v_count = 5 then 'PASS' else 'FAIL' end || ' historique des tentatives (' || v_count || ')' || chr(10);

  -- Étudiant B ne voit rien de A ----------------------------------------------
  perform set_config('request.jwt.claims', json_build_object('sub', v_b, 'role', 'authenticated')::text, true);
  select count(*) into v_count from public.quiz_attempts;
  report := report || case when v_count = 0 then 'PASS' else 'FAIL' end || ' B ne voit pas les notes de A' || chr(10);
  select count(*) into v_count from public.lesson_progress;
  report := report || case when v_count = 0 then 'PASS' else 'FAIL' end || ' B ne voit pas la progression de A' || chr(10);
  select count(*) into v_count from public.profiles;
  report := report || case when v_count = 1 then 'PASS' else 'FAIL' end || ' B ne voit que son propre profil' || chr(10);

  -- Visiteur anonyme ---------------------------------------------------------
  perform set_config('request.jwt.claims', '{"role":"anon"}', true);
  perform set_config('role', 'anon', true);
  select count(*) into v_count from public.courses;
  report := report || case when v_count = 3 then 'PASS' else 'FAIL' end || ' visiteur : catalogue visible (' || v_count || ' formations)' || chr(10);
  select count(*) into v_count from public.modules;
  report := report || case when v_count = 5 then 'PASS' else 'FAIL' end || ' visiteur : plan de cours visible' || chr(10);
  begin
    perform 1 from public.lessons limit 1;
    report := report || 'FAIL visiteur : leçons lisibles' || chr(10);
  exception when insufficient_privilege then
    report := report || 'PASS visiteur : contenu des leçons réservé aux inscrits' || chr(10);
  end;
  begin
    perform public.submit_quiz(v_quiz, v_all_correct);
    report := report || 'FAIL visiteur : soumission de quiz possible' || chr(10);
  exception when insufficient_privilege then
    report := report || 'PASS visiteur : soumission de quiz refusée' || chr(10);
  end;

  raise exception 'RAPPORT (rollback)%', chr(10) || report;
end;
$$;
