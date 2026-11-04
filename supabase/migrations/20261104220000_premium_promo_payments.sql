-- SMK Academy — offres Free / Premium, accès offerts, codes promotionnels, paiements (mode test).
-- Principe : le navigateur ne décide jamais d'un prix ni d'un accès Premium.
--   * prix lus en base (modifiables uniquement par un admin aal2) ;
--   * accès Premium = abonnement actif synchronisé par webhook signé OU accès offert (admin / code promo) ;
--   * toutes les écritures passent par des RPC SECURITY DEFINER ; aucune écriture directe autorisée.

-- ---------------------------------------------------------------------------
-- Offres
-- ---------------------------------------------------------------------------
create table public.plans (
  id text primary key check (id in ('free', 'premium_monthly', 'premium_yearly')),
  name text not null check (char_length(name) between 2 and 60),
  tagline text not null default '' check (char_length(tagline) <= 160),
  price_cents integer not null check (price_cents between 0 and 100000),
  currency text not null default 'eur' check (currency = 'eur'),
  billing_interval text check (billing_interval in ('month', 'year')),
  features text[] not null default '{}' check (cardinality(features) <= 20),
  is_active boolean not null default true,
  position integer not null default 0,
  updated_at timestamptz not null default now(),
  check ((id = 'free') = (billing_interval is null)),
  check (id <> 'free' or price_cents = 0)
);
alter table public.plans enable row level security;
revoke all on public.plans from public, anon, authenticated;
grant select on public.plans to anon, authenticated;
grant update (name, tagline, price_cents, features, is_active) on public.plans to authenticated;

create policy "plans: lecture publique des offres actives" on public.plans for select to anon, authenticated
  using (is_active or (select private.is_admin()));
create policy "plans: modification admin" on public.plans for update to authenticated
  using ((select private.is_admin())) with check ((select private.is_admin()));

create trigger plans_touch_updated_at before update on public.plans
  for each row execute function private.touch_updated_at();

insert into public.plans (id, name, tagline, price_cents, billing_interval, features, position) values
  ('free', 'SMK Free', 'Pour apprendre les bases, sans carte bancaire.', 0, null,
   array['Compte gratuit', 'Cours fondamentaux', 'Exercices et quiz notés sur 20', 'Corrections détaillées', 'Progression et tableau de bord'], 1),
  ('premium_monthly', 'SMK Premium', 'Toutes les formations, sans engagement.', 100, 'month',
   array['Tous les avantages Free', 'Formations et parcours avancés', 'Examens blancs supplémentaires', 'Projets pratiques avancés', 'Statistiques détaillées', 'Attestations internes'], 2),
  ('premium_yearly', 'SMK Premium annuel', 'Premium pour un an, renouvellement annuel indiqué clairement.', 1000, 'year',
   array['Tous les avantages Premium', 'Paiement une fois par an', 'Renouvellement annuel, résiliable à tout moment'], 3)
on conflict (id) do nothing;

-- ---------------------------------------------------------------------------
-- Abonnements et paiements (alimentés uniquement par les webhooks vérifiés)
-- ---------------------------------------------------------------------------
create table public.subscriptions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  provider text not null check (provider in ('stripe', 'paypal')),
  provider_subscription_id text not null,
  provider_customer_id text,
  plan_id text references public.plans (id),
  status text not null,
  current_period_end timestamptz,
  cancel_at_period_end boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (provider, provider_subscription_id)
);
create index subscriptions_user_idx on public.subscriptions (user_id);

create table public.payments (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users (id) on delete set null,
  provider text not null check (provider in ('stripe', 'paypal')),
  provider_ref text not null,
  provider_subscription_id text,
  plan_id text references public.plans (id),
  amount_cents integer not null check (amount_cents >= 0),
  currency text not null default 'eur',
  status text not null check (status in ('paid', 'failed', 'refunded')),
  livemode boolean not null default false,
  created_at timestamptz not null default now(),
  unique (provider, provider_ref)
);
create index payments_user_idx on public.payments (user_id);
create index payments_created_idx on public.payments (created_at desc);

alter table public.subscriptions enable row level security;
alter table public.payments enable row level security;
revoke all on public.subscriptions, public.payments from public, anon, authenticated;
grant select on public.subscriptions, public.payments to authenticated;

create policy "subscriptions: lecture du titulaire ou admin" on public.subscriptions for select to authenticated
  using (user_id = (select auth.uid()) or (select private.is_admin()));
create policy "payments: lecture du titulaire ou admin" on public.payments for select to authenticated
  using (user_id = (select auth.uid()) or (select private.is_admin()));

-- Idempotence des webhooks
create table private.webhook_events (
  provider text not null,
  event_id text not null,
  event_type text not null,
  received_at timestamptz not null default now(),
  primary key (provider, event_id)
);
revoke all on private.webhook_events from public, anon, authenticated;

-- Secrets partagés (seule l'empreinte SHA-256 est stockée)
create table private.app_secrets (
  name text primary key,
  sha256_hex text not null check (sha256_hex ~ '^[0-9a-f]{64}$'),
  updated_at timestamptz not null default now()
);
revoke all on private.app_secrets from public, anon, authenticated;

-- ---------------------------------------------------------------------------
-- Accès Premium offerts (clients fidèles, codes promo)
-- ---------------------------------------------------------------------------
create table public.premium_grants (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  source text not null check (source in ('admin', 'promo')),
  starts_at timestamptz not null default now(),
  ends_at timestamptz,                      -- null = accès illimité
  note text not null default '' check (char_length(note) <= 200),
  promo_code_id uuid,
  granted_by uuid references auth.users (id) on delete set null,
  revoked_at timestamptz,
  created_at timestamptz not null default now(),
  check (ends_at is null or ends_at > starts_at)
);
create index premium_grants_user_idx on public.premium_grants (user_id);
alter table public.premium_grants enable row level security;
revoke all on public.premium_grants from public, anon, authenticated;
grant select on public.premium_grants to authenticated;
create policy "premium_grants: lecture du titulaire ou admin" on public.premium_grants for select to authenticated
  using (user_id = (select auth.uid()) or (select private.is_admin()));

create table public.promo_codes (
  id uuid primary key default gen_random_uuid(),
  code text not null unique check (code ~ '^[A-Z0-9-]{6,32}$'),
  months integer check (months between 1 and 60),   -- null = accès illimité
  restricted_email text check (restricted_email is null or restricted_email = lower(restricted_email)),
  max_redemptions integer not null default 1 check (max_redemptions between 1 and 10000),
  redemptions_count integer not null default 0 check (redemptions_count >= 0),
  expires_at timestamptz,
  note text not null default '' check (char_length(note) <= 200),
  created_by uuid references auth.users (id) on delete set null,
  disabled_at timestamptz,
  created_at timestamptz not null default now()
);
alter table public.promo_codes enable row level security;
revoke all on public.promo_codes from public, anon, authenticated;
grant select on public.promo_codes to authenticated;
create policy "promo_codes: lecture admin" on public.promo_codes for select to authenticated
  using ((select private.is_admin()));

alter table public.premium_grants
  add constraint premium_grants_promo_fk foreign key (promo_code_id) references public.promo_codes (id) on delete set null;
create index premium_grants_promo_idx on public.premium_grants (promo_code_id);

create table public.promo_redemptions (
  id uuid primary key default gen_random_uuid(),
  promo_code_id uuid not null references public.promo_codes (id) on delete cascade,
  user_id uuid not null references auth.users (id) on delete cascade,
  grant_id uuid references public.premium_grants (id) on delete set null,
  redeemed_at timestamptz not null default now(),
  unique (promo_code_id, user_id)
);
create index promo_redemptions_user_idx on public.promo_redemptions (user_id);
create index promo_redemptions_grant_idx on public.promo_redemptions (grant_id);
alter table public.promo_redemptions enable row level security;
revoke all on public.promo_redemptions from public, anon, authenticated;
grant select on public.promo_redemptions to authenticated;
create policy "promo_redemptions: lecture du titulaire ou admin" on public.promo_redemptions for select to authenticated
  using (user_id = (select auth.uid()) or (select private.is_admin()));

-- Limitation des essais de codes (anti force brute)
create table private.promo_attempts (
  user_id uuid not null,
  at timestamptz not null default now(),
  success boolean not null
);
create index promo_attempts_user_at_idx on private.promo_attempts (user_id, at desc);
revoke all on private.promo_attempts from public, anon, authenticated;

-- ---------------------------------------------------------------------------
-- Calcul de l'accès Premium (unique source de vérité)
-- ---------------------------------------------------------------------------
create or replace function private.premium_until(p_user uuid)
returns timestamptz   -- 'infinity' si illimité, null si aucun accès
language sql
stable
security definer
set search_path = ''
as $$
  select max(e) from (
    select coalesce(g.ends_at, 'infinity'::timestamptz) as e
    from public.premium_grants g
    where g.user_id = p_user and g.revoked_at is null and g.starts_at <= now()
      and (g.ends_at is null or g.ends_at > now())
    union all
    select s.current_period_end
    from public.subscriptions s
    where s.user_id = p_user and s.status in ('active', 'trialing', 'past_due')
      and s.current_period_end > now()
  ) t;
$$;

create or replace function private.has_premium(p_user uuid)
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select p_user is not null and private.premium_until(p_user) is not null;
$$;

revoke execute on function private.premium_until(uuid) from public, anon, authenticated;
revoke execute on function private.has_premium(uuid) from public;
grant execute on function private.has_premium(uuid) to anon, authenticated;  -- utilisée par les politiques RLS

create or replace function public.my_access()
returns jsonb
language plpgsql
stable
security definer
set search_path = ''
as $$
declare
  v_uid uuid := auth.uid();
  v_until timestamptz;
begin
  if v_uid is null then
    return jsonb_build_object('premium', false);
  end if;
  v_until := private.premium_until(v_uid);
  return jsonb_build_object(
    'premium', v_until is not null,
    'unlimited', v_until = 'infinity'::timestamptz,
    'until', case when v_until is null or v_until = 'infinity'::timestamptz then null else v_until end,
    'subscription', (
      select jsonb_build_object('plan_id', s.plan_id, 'status', s.status,
        'current_period_end', s.current_period_end, 'cancel_at_period_end', s.cancel_at_period_end,
        'provider', s.provider)
      from public.subscriptions s where s.user_id = v_uid
      order by s.current_period_end desc nulls last limit 1)
  );
end;
$$;
revoke execute on function public.my_access() from public;
grant execute on function public.my_access() to anon, authenticated;

-- Contenu Premium : un module d'une formation Premium n'est servi qu'aux comptes Premium.
create or replace function private.module_is_public(p_module_id uuid)
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1
    from public.modules m
    join public.courses c on c.id = m.course_id
    where m.id = p_module_id and m.status = 'published' and c.status = 'published'
      and (not c.is_premium or private.has_premium((select auth.uid())))
  );
$$;

create or replace function public.enroll_in_course(p_course_id uuid)
returns void
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_uid uuid := auth.uid();
  v_premium boolean;
begin
  if v_uid is null then
    raise exception 'Authentification requise' using errcode = '28000';
  end if;
  select is_premium into v_premium from public.courses where id = p_course_id and status = 'published';
  if not found then
    raise exception 'Formation indisponible' using errcode = 'P0002';
  end if;
  if v_premium and not private.has_premium(v_uid) then
    raise exception 'Formation réservée à SMK Premium' using errcode = '42501';
  end if;
  insert into public.enrollments (user_id, course_id)
  values (v_uid, p_course_id)
  on conflict (user_id, course_id) do nothing;
end;
$$;

-- ---------------------------------------------------------------------------
-- Utilisation d'un code promo par un étudiant
-- ---------------------------------------------------------------------------
create or replace function public.redeem_promo_code(p_code text)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_uid uuid := auth.uid();
  v_email text;
  v_code text := upper(regexp_replace(coalesce(p_code, ''), '\s', '', 'g'));
  v_promo public.promo_codes%rowtype;
  v_until timestamptz;
  v_start timestamptz;
  v_grant uuid;
begin
  if v_uid is null then
    raise exception 'Authentification requise' using errcode = '28000';
  end if;
  if (select count(*) from private.promo_attempts
      where user_id = v_uid and not success and at > now() - interval '1 hour') >= 10 then
    return jsonb_build_object('ok', false, 'reason', 'rate_limited');
  end if;

  select * into v_promo from public.promo_codes where code = v_code for update;
  select lower(email) into v_email from auth.users where id = v_uid;

  if v_promo.id is null
     or v_promo.disabled_at is not null
     or (v_promo.expires_at is not null and v_promo.expires_at <= now())
     or v_promo.redemptions_count >= v_promo.max_redemptions
     or (v_promo.restricted_email is not null and v_promo.restricted_email <> v_email) then
    insert into private.promo_attempts (user_id, success) values (v_uid, false);
    return jsonb_build_object('ok', false, 'reason', 'invalid');
  end if;

  if exists (select 1 from public.promo_redemptions where promo_code_id = v_promo.id and user_id = v_uid) then
    return jsonb_build_object('ok', false, 'reason', 'already_used');
  end if;

  v_until := private.premium_until(v_uid);
  if v_until = 'infinity'::timestamptz then
    return jsonb_build_object('ok', false, 'reason', 'already_unlimited');
  end if;
  -- Les mois offerts s'ajoutent à l'accès en cours.
  v_start := greatest(now(), coalesce(v_until, now()));

  insert into public.premium_grants (user_id, source, starts_at, ends_at, note, promo_code_id)
  values (v_uid, 'promo', v_start,
          case when v_promo.months is null then null else v_start + make_interval(months => v_promo.months) end,
          'Code ' || v_promo.code, v_promo.id)
  returning id into v_grant;

  insert into public.promo_redemptions (promo_code_id, user_id, grant_id) values (v_promo.id, v_uid, v_grant);
  update public.promo_codes set redemptions_count = redemptions_count + 1 where id = v_promo.id;
  insert into private.promo_attempts (user_id, success) values (v_uid, true);

  return jsonb_build_object('ok', true, 'months', v_promo.months,
    'until', (select ends_at from public.premium_grants where id = v_grant));
end;
$$;
revoke execute on function public.redeem_promo_code(text) from public, anon;
grant execute on function public.redeem_promo_code(text) to authenticated;

-- ---------------------------------------------------------------------------
-- Administration Premium (admin + MFA aal2, vérifié en base)
-- ---------------------------------------------------------------------------
create or replace function private.require_admin()
returns void
language plpgsql
stable
security definer
set search_path = ''
as $$
begin
  if not private.is_admin() then
    raise exception 'Accès réservé aux administrateurs (MFA requise)' using errcode = '42501';
  end if;
end;
$$;
revoke execute on function private.require_admin() from public, anon, authenticated;

create or replace function private.log_admin(p_action text, p_entity text, p_entity_id uuid, p_summary jsonb)
returns void
language sql
security definer
set search_path = ''
as $$
  insert into private.audit_log (actor_id, action, entity, entity_id, summary)
  values ((select auth.uid()), p_action, p_entity, p_entity_id, coalesce(p_summary, '{}'::jsonb));
$$;
revoke execute on function private.log_admin(text, text, uuid, jsonb) from public, anon, authenticated;

-- Accès offert à un client (fidélité) : p_months null = illimité
create or replace function public.admin_grant_premium(p_email text, p_months integer, p_note text)
returns uuid
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_user uuid;
  v_grant uuid;
begin
  perform private.require_admin();
  if p_months is not null and (p_months < 1 or p_months > 120) then
    raise exception 'Durée invalide (1 à 120 mois, ou illimitée)' using errcode = '22023';
  end if;
  select id into v_user from auth.users where lower(email) = lower(trim(p_email));
  if v_user is null then
    raise exception 'Aucun compte pour cette adresse email' using errcode = 'P0002';
  end if;
  insert into public.premium_grants (user_id, source, ends_at, note, granted_by)
  values (v_user, 'admin',
          case when p_months is null then null else now() + make_interval(months => p_months) end,
          left(coalesce(p_note, ''), 200), (select auth.uid()))
  returning id into v_grant;
  perform private.log_admin('GRANT', 'premium_grants', v_grant,
    jsonb_build_object('email', lower(trim(p_email)), 'months', p_months));
  return v_grant;
end;
$$;

create or replace function public.admin_revoke_premium(p_grant_id uuid)
returns void
language plpgsql
security definer
set search_path = ''
as $$
begin
  perform private.require_admin();
  update public.premium_grants set revoked_at = now() where id = p_grant_id and revoked_at is null;
  if not found then
    raise exception 'Accès introuvable ou déjà révoqué' using errcode = 'P0002';
  end if;
  perform private.log_admin('REVOKE', 'premium_grants', p_grant_id, '{}'::jsonb);
end;
$$;

create or replace function public.admin_create_promo_code(
  p_months integer, p_max_redemptions integer, p_restricted_email text,
  p_expires_at timestamptz, p_note text, p_code text default null)
returns text
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_alphabet constant text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';  -- sans 0/O ni 1/I
  v_bytes bytea;
  v_code text;
  v_id uuid;
  i integer;
begin
  perform private.require_admin();
  if p_code is not null and trim(p_code) <> '' then
    v_code := upper(trim(p_code));
  else
    v_bytes := extensions.gen_random_bytes(12);
    v_code := 'SMK-';
    for i in 0..11 loop
      v_code := v_code || substr(v_alphabet, (get_byte(v_bytes, i) % 32) + 1, 1);
      if i in (3, 7) then v_code := v_code || '-'; end if;
    end loop;
  end if;
  insert into public.promo_codes (code, months, restricted_email, max_redemptions, expires_at, note, created_by)
  values (v_code, p_months, nullif(lower(trim(coalesce(p_restricted_email, ''))), ''),
          coalesce(p_max_redemptions, 1), p_expires_at, left(coalesce(p_note, ''), 200), (select auth.uid()))
  returning id into v_id;
  perform private.log_admin('INSERT', 'promo_codes', v_id,
    jsonb_build_object('months', p_months, 'max', coalesce(p_max_redemptions, 1),
                       'personal', p_restricted_email is not null and trim(p_restricted_email) <> ''));
  return v_code;
end;
$$;

create or replace function public.admin_disable_promo_code(p_id uuid)
returns void
language plpgsql
security definer
set search_path = ''
as $$
begin
  perform private.require_admin();
  update public.promo_codes set disabled_at = now() where id = p_id and disabled_at is null;
  if not found then
    raise exception 'Code introuvable ou déjà désactivé' using errcode = 'P0002';
  end if;
  perform private.log_admin('DISABLE', 'promo_codes', p_id, '{}'::jsonb);
end;
$$;

-- Vue d'ensemble des accès (avec emails, réservée aux admins)
create or replace function public.admin_premium_members()
returns table (grant_id uuid, email text, source text, starts_at timestamptz, ends_at timestamptz,
               note text, revoked_at timestamptz, created_at timestamptz)
language plpgsql
stable
security definer
set search_path = ''
as $$
begin
  perform private.require_admin();
  return query
    select g.id, u.email::text, g.source, g.starts_at, g.ends_at, g.note, g.revoked_at, g.created_at
    from public.premium_grants g join auth.users u on u.id = g.user_id
    order by g.created_at desc limit 500;
end;
$$;

create or replace function public.admin_payments_overview()
returns jsonb
language plpgsql
stable
security definer
set search_path = ''
as $$
begin
  perform private.require_admin();
  return jsonb_build_object(
    'payments', coalesce((
      select jsonb_agg(row_to_json(t) order by t.created_at desc) from (
        select p.id, u.email, p.provider, p.provider_ref, p.plan_id, p.amount_cents, p.currency,
               p.status, p.livemode, p.created_at
        from public.payments p left join auth.users u on u.id = p.user_id
        order by p.created_at desc limit 200) t), '[]'::jsonb),
    'subscriptions', coalesce((
      select jsonb_agg(row_to_json(t) order by t.updated_at desc) from (
        select s.id, u.email, s.provider, s.plan_id, s.status, s.current_period_end,
               s.cancel_at_period_end, s.updated_at
        from public.subscriptions s join auth.users u on u.id = s.user_id
        order by s.updated_at desc limit 200) t), '[]'::jsonb),
    'totals', jsonb_build_object(
      'paid_cents', (select coalesce(sum(amount_cents), 0) from public.payments where status = 'paid'),
      'failed', (select count(*) from public.payments where status = 'failed'),
      'active_subscriptions', (select count(*) from public.subscriptions
                               where status in ('active', 'trialing') and current_period_end > now()),
      'premium_members', (select count(distinct id) from public.profiles where private.has_premium(id)),
      'free_members', (select count(*) from public.profiles where role = 'student' and not private.has_premium(id))
    )
  );
end;
$$;

revoke execute on function public.admin_grant_premium(text, integer, text) from public, anon;
revoke execute on function public.admin_revoke_premium(uuid) from public, anon;
revoke execute on function public.admin_create_promo_code(integer, integer, text, timestamptz, text, text) from public, anon;
revoke execute on function public.admin_disable_promo_code(uuid) from public, anon;
revoke execute on function public.admin_premium_members() from public, anon;
revoke execute on function public.admin_payments_overview() from public, anon;
grant execute on function public.admin_grant_premium(text, integer, text) to authenticated;
grant execute on function public.admin_revoke_premium(uuid) to authenticated;
grant execute on function public.admin_create_promo_code(integer, integer, text, timestamptz, text, text) to authenticated;
grant execute on function public.admin_disable_promo_code(uuid) to authenticated;
grant execute on function public.admin_premium_members() to authenticated;
grant execute on function public.admin_payments_overview() to authenticated;

create trigger audit_plans after update on public.plans
  for each row execute function private.audit_change();

-- ---------------------------------------------------------------------------
-- Webhooks de paiement : appelés par le serveur Next.js APRÈS vérification de la signature
-- Stripe, avec un jeton partagé (empreinte en base, jeton dans les variables Netlify).
-- ---------------------------------------------------------------------------
create or replace function public.payments_apply_event(
  p_token text, p_provider text, p_event_id text, p_type text, p_data jsonb)
returns text
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_hash text;
  v_user uuid := nullif(p_data ->> 'user_id', '')::uuid;
  v_plan text := nullif(p_data ->> 'plan_id', '');
begin
  select sha256_hex into v_hash from private.app_secrets where name = 'payments_webhook';
  if v_hash is null or p_token is null
     or encode(extensions.digest(p_token, 'sha256'), 'hex') <> v_hash then
    raise exception 'Jeton de webhook invalide' using errcode = '42501';
  end if;
  if p_provider not in ('stripe', 'paypal') then
    raise exception 'Fournisseur inconnu' using errcode = '22023';
  end if;
  if coalesce((p_data ->> 'livemode')::boolean, false) then
    raise exception 'Paiements réels refusés : la plateforme est en mode test' using errcode = '42501';
  end if;
  if v_plan is not null and not exists (select 1 from public.plans where id = v_plan) then
    v_plan := null;
  end if;

  insert into private.webhook_events (provider, event_id, event_type) values (p_provider, p_event_id, p_type)
  on conflict do nothing;
  if not found then
    return 'duplicate';
  end if;

  if p_type = 'subscription' then
    if v_user is null then
      return 'ignored';
    end if;
    insert into public.subscriptions as s (user_id, provider, provider_subscription_id, provider_customer_id,
      plan_id, status, current_period_end, cancel_at_period_end)
    values (v_user, p_provider, p_data ->> 'subscription_id', p_data ->> 'customer_id', v_plan,
      p_data ->> 'status', to_timestamp((p_data ->> 'current_period_end')::bigint),
      coalesce((p_data ->> 'cancel_at_period_end')::boolean, false))
    on conflict (provider, provider_subscription_id) do update set
      status = excluded.status,
      plan_id = coalesce(excluded.plan_id, s.plan_id),
      provider_customer_id = coalesce(excluded.provider_customer_id, s.provider_customer_id),
      current_period_end = coalesce(excluded.current_period_end, s.current_period_end),
      cancel_at_period_end = excluded.cancel_at_period_end,
      updated_at = now();
    return 'subscription_synced';
  elsif p_type = 'payment' then
    insert into public.payments (user_id, provider, provider_ref, provider_subscription_id, plan_id,
      amount_cents, currency, status, livemode)
    values (v_user, p_provider, p_data ->> 'ref', p_data ->> 'subscription_id', v_plan,
      (p_data ->> 'amount_cents')::integer, coalesce(p_data ->> 'currency', 'eur'), p_data ->> 'status', false)
    on conflict (provider, provider_ref) do update set status = excluded.status;
    return 'payment_recorded';
  end if;
  return 'ignored';
end;
$$;
revoke execute on function public.payments_apply_event(text, text, text, text, jsonb) from public;
-- Appelée par le serveur sans session : protégée par le jeton partagé.
grant execute on function public.payments_apply_event(text, text, text, text, jsonb) to anon, authenticated;

-- Statistiques admin enrichies (conversion Free → Premium, sans chiffres fictifs)
create or replace function public.admin_stats()
returns jsonb
language plpgsql
stable
security definer
set search_path = ''
as $$
begin
  perform private.require_admin();
  return jsonb_build_object(
    'students', (select count(*) from public.profiles where role = 'student'),
    'premium_students', (select count(*) from public.profiles where role = 'student' and private.has_premium(id)),
    'courses_published', (select count(*) from public.courses where status = 'published'),
    'courses_coming_soon', (select count(*) from public.courses where status = 'coming_soon'),
    'courses_draft', (select count(*) from public.courses where status = 'draft'),
    'enrollments', (select count(*) from public.enrollments),
    'lessons_completed', (select count(*) from public.lesson_progress),
    'quiz_attempts', (select count(*) from public.quiz_attempts),
    'average_score', (select round(avg(score_20), 2) from public.quiz_attempts)
  );
end;
$$;
