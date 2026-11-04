-- SMK Academy — catalogue généraliste + espace administrateur sécurisé.
-- Catégories, métadonnées de catalogue, droits d'administration (rôle admin ET session MFA aal2),
-- journal d'audit, garde-fous de publication, RPC d'administration des corrigés.

-- ---------------------------------------------------------------------------
-- Catégories
-- ---------------------------------------------------------------------------
create table public.categories (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique check (slug ~ '^[a-z0-9-]+$'),
  name text not null check (char_length(name) between 2 and 80),
  description text not null default '' check (char_length(description) <= 400),
  position integer not null default 0,
  created_at timestamptz not null default now()
);
alter table public.categories enable row level security;
revoke all on public.categories from anon, authenticated;
grant select on public.categories to anon, authenticated;
create policy "categories: lecture publique" on public.categories for select to anon, authenticated using (true);

insert into public.categories (slug, name, description, position) values
  ('programmation', 'Programmation', 'Apprendre un langage de programmation, des bases aux projets complets.', 1),
  ('developpement-web', 'Développement web', 'Créer des sites et des applications web, du HTML aux frameworks modernes.', 2),
  ('bases-de-donnees', 'Bases de données', 'Interroger, modéliser et administrer des données.', 3),
  ('data-science', 'Data Science', 'Analyser des données, faire des statistiques et entraîner des modèles.', 4),
  ('intelligence-artificielle', 'Intelligence artificielle', 'Traitement du langage, grands modèles de langage et agents.', 5),
  ('cloud-devops', 'Cloud et DevOps', 'Déployer, conteneuriser et automatiser.', 6),
  ('cybersecurite', 'Cybersécurité', 'Comprendre et protéger les systèmes, les réseaux et les applications web.', 7),
  ('business-intelligence', 'Business Intelligence', 'Tableurs, tableaux de bord et visualisation pour la décision.', 8),
  ('developpement-mobile', 'Développement mobile', 'Créer des applications pour Android et iOS.', 9),
  ('langues', 'Langues', 'Anglais du A1 au C1, anglais professionnel, espagnol et allemand.', 10);

-- ---------------------------------------------------------------------------
-- Formations : catégorie, technologie, couverture
-- ---------------------------------------------------------------------------
alter table public.courses
  add column category_id uuid references public.categories (id) on delete restrict,
  add column topic text not null default '' check (char_length(topic) <= 40),
  add column cover_label text not null default '' check (char_length(cover_label) <= 6),
  add column updated_at timestamptz not null default now();

update public.courses c set category_id = cat.id
from public.categories cat
where cat.slug = case c.category
  when 'Programmation' then 'programmation'
  when 'Bases de données' then 'bases-de-donnees'
  when 'Langues' then 'langues'
end;

update public.courses set topic = 'Python', cover_label = 'Py' where slug = 'python-debutant';
update public.courses set topic = 'SQL', cover_label = 'SQL' where slug = 'sql-debutant';
update public.courses set topic = 'Anglais', cover_label = 'EN' where slug = 'anglais-professionnel-debutant';

alter table public.courses alter column category_id set not null;
alter table public.courses drop column category;

create index courses_category_id_idx on public.courses (category_id);
create index courses_status_position_idx on public.courses (status, position);

create trigger courses_touch_updated_at
  before update on public.courses
  for each row execute function private.touch_updated_at();

-- ---------------------------------------------------------------------------
-- Administration : rôle admin ET authentification à deux facteurs vérifiée
-- ---------------------------------------------------------------------------
create or replace function private.is_admin()
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select coalesce((select auth.jwt() ->> 'aal') = 'aal2', false)
     and exists (
       select 1 from public.profiles p
       where p.id = (select auth.uid()) and p.role = 'admin'
     );
$$;
revoke execute on function private.is_admin() from public;
grant execute on function private.is_admin() to anon, authenticated;

-- Indique à l'interface si le compte a le rôle admin (sans exiger aal2), pour proposer la MFA.
create or replace function public.my_role()
returns text
language sql
stable
security definer
set search_path = ''
as $$
  select role from public.profiles where id = (select auth.uid());
$$;
revoke execute on function public.my_role() from public, anon;
grant execute on function public.my_role() to authenticated;

-- Promotion de rôle : réservée au propriétaire via l'éditeur SQL (aucun accès API).
create or replace function private.set_role(p_email text, p_role text)
returns void
language plpgsql
security definer
set search_path = ''
as $$
declare v_id uuid;
begin
  if p_role not in ('student', 'admin') then
    raise exception 'Rôle inconnu : %', p_role;
  end if;
  select id into v_id from auth.users where lower(email) = lower(p_email);
  if v_id is null then
    raise exception 'Aucun compte pour %', p_email;
  end if;
  update public.profiles set role = p_role where id = v_id;
end;
$$;
revoke execute on function private.set_role(text, text) from public, anon, authenticated;

-- Écriture du contenu par les administrateurs (RLS) ; lecture des brouillons comprise.
grant insert, update, delete on public.categories, public.courses, public.modules, public.lessons,
  public.quizzes, public.quiz_questions, public.quiz_options to authenticated;

create policy "categories: administration" on public.categories for all to authenticated
  using ((select private.is_admin())) with check ((select private.is_admin()));
create policy "courses: administration" on public.courses for all to authenticated
  using ((select private.is_admin())) with check ((select private.is_admin()));
create policy "modules: administration" on public.modules for all to authenticated
  using ((select private.is_admin())) with check ((select private.is_admin()));
create policy "lessons: administration" on public.lessons for all to authenticated
  using ((select private.is_admin())) with check ((select private.is_admin()));
create policy "quizzes: administration" on public.quizzes for all to authenticated
  using ((select private.is_admin())) with check ((select private.is_admin()));
create policy "quiz_questions: administration" on public.quiz_questions for all to authenticated
  using ((select private.is_admin())) with check ((select private.is_admin()));
create policy "quiz_options: administration" on public.quiz_options for all to authenticated
  using ((select private.is_admin())) with check ((select private.is_admin()));

-- ---------------------------------------------------------------------------
-- Garde-fous de publication : jamais de formation ou de module vide présenté comme disponible
-- ---------------------------------------------------------------------------
create or replace function private.module_is_complete(p_module_id uuid)
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (select 1 from public.lessons where module_id = p_module_id)
     and exists (
       select 1
       from public.quizzes q
       join public.quiz_questions qq on qq.quiz_id = q.id
       where q.module_id = p_module_id
     )
     and not exists (
       select 1
       from public.quizzes q
       join public.quiz_questions qq on qq.quiz_id = q.id
       left join private.quiz_answer_keys k on k.question_id = qq.id
       where q.module_id = p_module_id and k.question_id is null
     );
$$;
revoke execute on function private.module_is_complete(uuid) from public, anon, authenticated;

create or replace function private.guard_module_publication()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  if new.status = 'published' and (tg_op = 'INSERT' or old.status is distinct from 'published') then
    if not private.module_is_complete(new.id) then
      raise exception 'Module incomplet : il faut au moins une leçon et un quiz dont chaque question a un corrigé.'
        using errcode = 'P0001';
    end if;
  end if;
  return new;
end;
$$;

create trigger modules_guard_publication
  before insert or update of status on public.modules
  for each row execute function private.guard_module_publication();

create or replace function private.guard_course_publication()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  if new.status = 'published' and (tg_op = 'INSERT' or old.status is distinct from 'published') then
    if not exists (select 1 from public.modules where course_id = new.id and status = 'published') then
      raise exception 'Formation vide : publiez d''abord au moins un module complet.' using errcode = 'P0001';
    end if;
  end if;
  return new;
end;
$$;

create trigger courses_guard_publication
  before insert or update of status on public.courses
  for each row execute function private.guard_course_publication();

-- ---------------------------------------------------------------------------
-- Corrigés : lecture et écriture réservées aux administrateurs, via RPC
-- ---------------------------------------------------------------------------
create or replace function public.admin_get_answer_keys(p_quiz_id uuid)
returns table (question_id uuid, correct_option_ids uuid[], explanation text)
language plpgsql
stable
security definer
set search_path = ''
as $$
begin
  if not private.is_admin() then
    raise exception 'Accès réservé aux administrateurs (MFA requise)' using errcode = '42501';
  end if;
  return query
    select k.question_id, k.correct_option_ids, k.explanation
    from private.quiz_answer_keys k
    join public.quiz_questions qq on qq.id = k.question_id
    where qq.quiz_id = p_quiz_id;
end;
$$;

create or replace function public.admin_set_answer_key(p_question_id uuid, p_correct uuid[], p_explanation text)
returns void
language plpgsql
security definer
set search_path = ''
as $$
declare v_kind text; v_valid integer;
begin
  if not private.is_admin() then
    raise exception 'Accès réservé aux administrateurs (MFA requise)' using errcode = '42501';
  end if;
  select kind into v_kind from public.quiz_questions where id = p_question_id;
  if v_kind is null then
    raise exception 'Question introuvable' using errcode = 'P0002';
  end if;
  if p_correct is null or cardinality(p_correct) = 0 then
    raise exception 'Indiquez au moins une bonne réponse' using errcode = '22023';
  end if;
  if v_kind <> 'multiple' and cardinality(p_correct) <> 1 then
    raise exception 'Une seule bonne réponse pour ce type de question' using errcode = '22023';
  end if;
  select count(*) into v_valid from public.quiz_options where question_id = p_question_id and id = any (p_correct);
  if v_valid <> cardinality(p_correct) then
    raise exception 'Les bonnes réponses doivent appartenir à la question' using errcode = '22023';
  end if;
  insert into private.quiz_answer_keys (question_id, correct_option_ids, explanation)
  values (p_question_id, p_correct, left(coalesce(p_explanation, ''), 2000))
  on conflict (question_id) do update
    set correct_option_ids = excluded.correct_option_ids, explanation = excluded.explanation;
  insert into private.audit_log (actor_id, action, entity, entity_id, summary)
  values ((select auth.uid()), 'UPDATE', 'quiz_answer_keys', p_question_id, '{}'::jsonb);
end;
$$;

-- ---------------------------------------------------------------------------
-- Journal d'audit des modifications de contenu et de rôles
-- ---------------------------------------------------------------------------
create table private.audit_log (
  id bigint generated always as identity primary key,
  at timestamptz not null default now(),
  actor_id uuid,
  action text not null,
  entity text not null,
  entity_id uuid,
  summary jsonb not null default '{}'::jsonb
);
create index audit_log_at_idx on private.audit_log (at desc);
revoke all on private.audit_log from public, anon, authenticated;

-- Les fonctions ci-dessus référencent audit_log : recompilées implicitement à l'exécution.

create or replace function private.audit_change()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_row jsonb := case when tg_op = 'DELETE' then to_jsonb(old) else to_jsonb(new) end;
  v_summary jsonb;
begin
  -- Jamais de contenu volumineux ni de secret : seulement des champs d'identification.
  v_summary := jsonb_strip_nulls(jsonb_build_object(
    'title', v_row ->> 'title',
    'slug', v_row ->> 'slug',
    'status', v_row ->> 'status',
    'old_status', case when tg_op = 'UPDATE' then to_jsonb(old) ->> 'status' end,
    'role', v_row ->> 'role',
    'old_role', case when tg_op = 'UPDATE' then to_jsonb(old) ->> 'role' end,
    'plan', v_row ->> 'plan'
  ));
  insert into private.audit_log (actor_id, action, entity, entity_id, summary)
  values ((select auth.uid()), tg_op, tg_table_name, (v_row ->> 'id')::uuid, v_summary);
  return null;
end;
$$;

create trigger audit_categories after insert or update or delete on public.categories
  for each row execute function private.audit_change();
create trigger audit_courses after insert or update or delete on public.courses
  for each row execute function private.audit_change();
create trigger audit_modules after insert or update or delete on public.modules
  for each row execute function private.audit_change();
create trigger audit_lessons after insert or update or delete on public.lessons
  for each row execute function private.audit_change();
create trigger audit_quizzes after insert or update or delete on public.quizzes
  for each row execute function private.audit_change();
create trigger audit_quiz_questions after insert or update or delete on public.quiz_questions
  for each row execute function private.audit_change();
create trigger audit_profiles_role after update of role, plan on public.profiles
  for each row execute function private.audit_change();

create or replace function public.admin_audit_log(p_limit integer default 50)
returns table (at timestamptz, actor_email text, action text, entity text, entity_id uuid, summary jsonb)
language plpgsql
stable
security definer
set search_path = ''
as $$
begin
  if not private.is_admin() then
    raise exception 'Accès réservé aux administrateurs (MFA requise)' using errcode = '42501';
  end if;
  return query
    select a.at, u.email::text, a.action, a.entity, a.entity_id, a.summary
    from private.audit_log a
    left join auth.users u on u.id = a.actor_id
    order by a.at desc
    limit least(greatest(p_limit, 1), 200);
end;
$$;

-- Statistiques réelles (aucune donnée fictive)
create or replace function public.admin_stats()
returns jsonb
language plpgsql
stable
security definer
set search_path = ''
as $$
begin
  if not private.is_admin() then
    raise exception 'Accès réservé aux administrateurs (MFA requise)' using errcode = '42501';
  end if;
  return jsonb_build_object(
    'students', (select count(*) from public.profiles where role = 'student'),
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

revoke execute on function public.admin_get_answer_keys(uuid) from public, anon;
revoke execute on function public.admin_set_answer_key(uuid, uuid[], text) from public, anon;
revoke execute on function public.admin_audit_log(integer) from public, anon;
revoke execute on function public.admin_stats() from public, anon;
grant execute on function public.admin_get_answer_keys(uuid) to authenticated;
grant execute on function public.admin_set_answer_key(uuid, uuid[], text) to authenticated;
grant execute on function public.admin_audit_log(integer) to authenticated;
grant execute on function public.admin_stats() to authenticated;

revoke execute on function private.audit_change() from public, anon, authenticated;
revoke execute on function private.guard_module_publication() from public, anon, authenticated;
revoke execute on function private.guard_course_publication() from public, anon, authenticated;
