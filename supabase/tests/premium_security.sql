-- Tests Premium : offres, accès offerts, codes promo, webhooks de paiement. Tout est annulé à la fin.
do $$
declare
  v_stu uuid := gen_random_uuid();
  v_stu2 uuid := gen_random_uuid();
  v_admin uuid := gen_random_uuid();
  v_course uuid := (select id from public.courses where slug = 'python-debutant');
  v_code_personal text;
  v_code_shared text;
  v_grant uuid;
  v_res jsonb;
  v_txt text;
  v_count integer;
  i integer;
  report text := '';
begin
  insert into auth.users (id, instance_id, aud, role, email, created_at, updated_at) values
    (v_stu, '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated', 'stu@smk.test', now(), now()),
    (v_stu2, '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated', 'stu2@smk.test', now(), now()),
    (v_admin, '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated', 'adm@smk.test', now(), now());
  update public.profiles set role = 'admin' where id = v_admin;
  -- Simulation : la formation Python devient Premium le temps du test.
  update public.courses set is_premium = true where id = v_course;
  insert into private.app_secrets (name, sha256_hex)
  values ('payments_webhook', encode(extensions.digest('jeton-de-test', 'sha256'), 'hex'))
  on conflict (name) do update set sha256_hex = excluded.sha256_hex;

  -- Visiteur -----------------------------------------------------------------
  perform set_config('request.jwt.claims', '{"role":"anon"}', true);
  perform set_config('role', 'anon', true);
  select count(*) into v_count from public.plans;
  report := report || case when v_count = 3 then 'PASS' else 'FAIL' end || ' visiteur : 3 offres lisibles (' || v_count || ')' || chr(10);
  select price_cents into v_count from public.plans where id = 'premium_monthly';
  report := report || case when v_count = 100 then 'PASS' else 'FAIL' end || ' visiteur : Premium mensuel à 1 € lu en base' || chr(10);
  begin
    update public.plans set price_cents = 0 where id = 'premium_monthly';
    report := report || 'FAIL visiteur : prix modifiable' || chr(10);
  exception when insufficient_privilege then report := report || 'PASS visiteur : prix non modifiable' || chr(10);
  end;
  begin
    perform public.payments_apply_event('mauvais-jeton', 'stripe', 'evt_x', 'subscription',
      jsonb_build_object('user_id', v_stu, 'subscription_id', 'sub_x', 'status', 'active',
                         'current_period_end', extract(epoch from now() + interval '1 year')::bigint));
    report := report || 'FAIL webhook : faux jeton accepté' || chr(10);
  exception when insufficient_privilege then report := report || 'PASS webhook : faux jeton refusé' || chr(10);
  end;

  -- Étudiant sans Premium ------------------------------------------------------
  perform set_config('request.jwt.claims', json_build_object('sub', v_stu, 'role', 'authenticated', 'aal', 'aal1')::text, true);
  perform set_config('role', 'authenticated', true);
  update public.plans set price_cents = 0 where id = 'premium_monthly';
  get diagnostics v_count = row_count;
  report := report || case when v_count = 0 then 'PASS' else 'FAIL' end || ' étudiant : modification du prix sans effet (RLS)' || chr(10);
  begin
    insert into public.premium_grants (user_id, source) values (v_stu, 'admin');
    report := report || 'FAIL étudiant : auto-attribution Premium' || chr(10);
  exception when insufficient_privilege then report := report || 'PASS étudiant : auto-attribution Premium refusée' || chr(10);
  end;
  begin
    insert into public.subscriptions (user_id, provider, provider_subscription_id, status, current_period_end)
    values (v_stu, 'stripe', 'sub_fake', 'active', now() + interval '1 year');
    report := report || 'FAIL étudiant : faux abonnement' || chr(10);
  exception when insufficient_privilege then report := report || 'PASS étudiant : faux abonnement refusé' || chr(10);
  end;
  begin
    perform public.admin_create_promo_code(12, 1, null, null, 'pirate');
    report := report || 'FAIL étudiant : création de code promo' || chr(10);
  exception when insufficient_privilege then report := report || 'PASS étudiant : création de code promo refusée' || chr(10);
  end;
  begin
    perform public.admin_grant_premium('stu@smk.test', null, 'pirate');
    report := report || 'FAIL étudiant : accès offert à soi-même' || chr(10);
  exception when insufficient_privilege then report := report || 'PASS étudiant : accès offert à soi-même refusé' || chr(10);
  end;
  select count(*) into v_count from public.lessons l join public.modules m on m.id = l.module_id where m.course_id = v_course;
  report := report || case when v_count = 0 then 'PASS' else 'FAIL' end || ' étudiant Free : leçons Premium non lisibles (' || v_count || ')' || chr(10);
  begin
    perform public.enroll_in_course(v_course);
    report := report || 'FAIL étudiant Free : inscription à une formation Premium' || chr(10);
  exception when insufficient_privilege then report := report || 'PASS étudiant Free : inscription Premium refusée' || chr(10);
  end;

  -- Administrateur sans MFA -----------------------------------------------------
  perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated', 'aal', 'aal1')::text, true);
  begin
    perform public.admin_grant_premium('stu@smk.test', 3, 'test');
    report := report || 'FAIL admin aal1 : accès offert sans MFA' || chr(10);
  exception when insufficient_privilege then report := report || 'PASS admin aal1 : accès offert refusé sans MFA' || chr(10);
  end;

  -- Administrateur avec MFA ---------------------------------------------------
  perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated', 'aal', 'aal2')::text, true);
  v_code_personal := public.admin_create_promo_code(3, 1, 'STU@smk.test', null, 'Client fidèle');
  v_code_shared := public.admin_create_promo_code(1, 2, null, now() + interval '30 days', 'Salon');
  report := report || case when v_code_personal ~ '^SMK-[A-Z2-9]{4}-[A-Z2-9]{4}-[A-Z2-9]{4}$' then 'PASS' else 'FAIL' end
    || ' admin aal2 : code généré (' || v_code_personal || ')' || chr(10);
  update public.plans set price_cents = 150 where id = 'premium_monthly';
  get diagnostics v_count = row_count;
  report := report || case when v_count = 1 then 'PASS' else 'FAIL' end || ' admin aal2 : prix modifiable' || chr(10);
  update public.plans set price_cents = 100 where id = 'premium_monthly';

  -- Utilisation des codes -------------------------------------------------------
  perform set_config('request.jwt.claims', json_build_object('sub', v_stu2, 'role', 'authenticated', 'aal', 'aal1')::text, true);
  v_res := public.redeem_promo_code(v_code_personal);
  report := report || case when v_res ->> 'reason' = 'invalid' then 'PASS' else 'FAIL' end || ' code personnel refusé à un autre compte' || chr(10);

  perform set_config('request.jwt.claims', json_build_object('sub', v_stu, 'role', 'authenticated', 'aal', 'aal1')::text, true);
  v_res := public.redeem_promo_code(lower(v_code_personal));
  report := report || case when (v_res ->> 'ok')::boolean
      and (v_res ->> 'until')::timestamptz between now() + interval '89 days' and now() + interval '93 days'
    then 'PASS' else 'FAIL' end || ' code personnel utilisé : 3 mois offerts' || chr(10);
  v_res := public.redeem_promo_code(v_code_personal);
  report := report || case when v_res ->> 'reason' in ('already_used', 'invalid') then 'PASS' else 'FAIL' end || ' code à usage unique non réutilisable' || chr(10);
  v_res := public.redeem_promo_code(v_code_shared);
  report := report || case when (v_res ->> 'until')::timestamptz between now() + interval '119 days' and now() + interval '124 days'
    then 'PASS' else 'FAIL' end || ' mois offerts cumulés (3 + 1)' || chr(10);
  v_res := public.my_access();
  report := report || case when (v_res ->> 'premium')::boolean then 'PASS' else 'FAIL' end || ' my_access : Premium actif' || chr(10);
  select count(*) into v_count from public.lessons l join public.modules m on m.id = l.module_id where m.course_id = v_course;
  report := report || case when v_count = 15 then 'PASS' else 'FAIL' end || ' étudiant Premium : leçons lisibles (' || v_count || ')' || chr(10);
  perform public.enroll_in_course(v_course);
  report := report || 'PASS étudiant Premium : inscription acceptée' || chr(10);
  select count(*) into v_count from public.premium_grants;
  report := report || case when v_count = 2 then 'PASS' else 'FAIL' end || ' étudiant : ne voit que ses propres accès' || chr(10);
  select count(*) into v_count from public.promo_codes;
  report := report || case when v_count = 0 then 'PASS' else 'FAIL' end || ' étudiant : liste des codes invisible' || chr(10);

  -- Force brute -----------------------------------------------------------------
  perform set_config('request.jwt.claims', json_build_object('sub', v_stu2, 'role', 'authenticated', 'aal', 'aal1')::text, true);
  for i in 1..10 loop
    v_res := public.redeem_promo_code('SMK-FAUX-CODE-' || i);
  end loop;
  v_res := public.redeem_promo_code(v_code_shared);
  report := report || case when v_res ->> 'reason' = 'rate_limited' then 'PASS' else 'FAIL' end || ' force brute : blocage après 10 échecs en 1 h' || chr(10);

  -- Client fidèle : accès illimité puis révocation ----------------------------
  perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated', 'aal', 'aal2')::text, true);
  v_grant := public.admin_grant_premium('STU2@smk.test', null, 'Client fidèle');
  perform set_config('request.jwt.claims', json_build_object('sub', v_stu2, 'role', 'authenticated', 'aal', 'aal1')::text, true);
  v_res := public.my_access();
  report := report || case when (v_res ->> 'unlimited')::boolean then 'PASS' else 'FAIL' end || ' accès illimité offert par l''admin' || chr(10);
  perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated', 'aal', 'aal2')::text, true);
  perform public.admin_revoke_premium(v_grant);
  select count(*) into v_count from public.admin_premium_members() where email = 'stu2@smk.test' and revoked_at is not null;
  report := report || case when v_count = 1 then 'PASS' else 'FAIL' end || ' révocation tracée' || chr(10);
  perform set_config('request.jwt.claims', json_build_object('sub', v_stu2, 'role', 'authenticated', 'aal', 'aal1')::text, true);
  v_res := public.my_access();
  report := report || case when not (v_res ->> 'premium')::boolean then 'PASS' else 'FAIL' end || ' accès révoqué : retour à Free' || chr(10);

  -- Webhooks (appel serveur, rôle anon + jeton) -------------------------------
  perform set_config('request.jwt.claims', '{"role":"anon"}', true);
  perform set_config('role', 'anon', true);
  v_txt := public.payments_apply_event('jeton-de-test', 'stripe', 'evt_1', 'subscription',
    jsonb_build_object('user_id', v_stu2, 'subscription_id', 'sub_1', 'customer_id', 'cus_1', 'plan_id', 'premium_monthly',
      'status', 'active', 'current_period_end', extract(epoch from now() + interval '1 month')::bigint));
  report := report || case when v_txt = 'subscription_synced' then 'PASS' else 'FAIL' end || ' webhook : abonnement synchronisé' || chr(10);
  v_txt := public.payments_apply_event('jeton-de-test', 'stripe', 'evt_1', 'subscription', '{}'::jsonb);
  report := report || case when v_txt = 'duplicate' then 'PASS' else 'FAIL' end || ' webhook : événement rejoué ignoré (idempotence)' || chr(10);
  v_txt := public.payments_apply_event('jeton-de-test', 'stripe', 'evt_2', 'payment',
    jsonb_build_object('user_id', v_stu2, 'ref', 'in_1', 'subscription_id', 'sub_1', 'plan_id', 'premium_monthly',
      'amount_cents', 100, 'currency', 'eur', 'status', 'paid'));
  report := report || case when v_txt = 'payment_recorded' then 'PASS' else 'FAIL' end || ' webhook : paiement de 1 € enregistré' || chr(10);
  begin
    perform public.payments_apply_event('jeton-de-test', 'stripe', 'evt_3', 'payment',
      jsonb_build_object('user_id', v_stu2, 'ref', 'in_live', 'amount_cents', 100, 'status', 'paid', 'livemode', true));
    report := report || 'FAIL webhook : paiement réel accepté' || chr(10);
  exception when insufficient_privilege then report := report || 'PASS webhook : paiement réel refusé (mode test)' || chr(10);
  end;

  perform set_config('request.jwt.claims', json_build_object('sub', v_stu2, 'role', 'authenticated', 'aal', 'aal1')::text, true);
  perform set_config('role', 'authenticated', true);
  v_res := public.my_access();
  report := report || case when (v_res ->> 'premium')::boolean and v_res -> 'subscription' ->> 'status' = 'active'
    then 'PASS' else 'FAIL' end || ' abonné Stripe : Premium actif' || chr(10);
  perform set_config('request.jwt.claims', json_build_object('sub', v_stu, 'role', 'authenticated', 'aal', 'aal1')::text, true);
  select count(*) into v_count from public.payments;
  report := report || case when v_count = 0 then 'PASS' else 'FAIL' end || ' paiements d''autrui invisibles' || chr(10);

  perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated', 'aal', 'aal2')::text, true);
  v_res := public.admin_payments_overview();
  report := report || case when (v_res -> 'totals' ->> 'paid_cents')::int >= 100 then 'PASS' else 'FAIL' end
    || ' admin : paiements visibles (' || (v_res -> 'totals' ->> 'paid_cents') || ' centimes)' || chr(10);

  raise exception 'RAPPORT (rollback)%', chr(10) || report;
end;
$$;
