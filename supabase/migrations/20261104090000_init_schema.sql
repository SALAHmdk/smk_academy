-- SMK Academy — schéma initial (jalon 1)
-- Profils, catalogue, leçons, quiz (réponses privées), inscriptions, progression, tentatives.

create schema if not exists private;
revoke all on schema private from public, anon, authenticated;

-- ---------------------------------------------------------------------------
-- Profils
-- ---------------------------------------------------------------------------
create table public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  full_name text not null default '' check (char_length(full_name) <= 120),
  role text not null default 'student' check (role in ('student', 'admin')),
  plan text not null default 'free' check (plan in ('free', 'premium')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
alter table public.profiles enable row level security;

create policy "profiles: lecture du propriétaire"
  on public.profiles for select to authenticated
  using ((select auth.uid()) = id);

create policy "profiles: mise à jour du propriétaire"
  on public.profiles for update to authenticated
  using ((select auth.uid()) = id)
  with check ((select auth.uid()) = id);

-- L'étudiant ne peut modifier que son nom : rôle et offre restent hors de portée.
revoke insert, update, delete on public.profiles from anon, authenticated;
grant select on public.profiles to authenticated;
grant update (full_name) on public.profiles to authenticated;

create or replace function private.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into public.profiles (id, full_name)
  values (new.id, left(coalesce(new.raw_user_meta_data ->> 'full_name', ''), 120));
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function private.handle_new_user();

create or replace function private.touch_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at := now();
  return new;
end;
$$;

create trigger profiles_touch_updated_at
  before update on public.profiles
  for each row execute function private.touch_updated_at();

-- ---------------------------------------------------------------------------
-- Catalogue
-- ---------------------------------------------------------------------------
create table public.courses (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique check (slug ~ '^[a-z0-9-]+$'),
  title text not null,
  subtitle text not null default '',
  description text not null default '',
  category text not null,
  level text not null check (level in ('debutant', 'intermediaire', 'avance')),
  duration_minutes integer not null default 0 check (duration_minutes >= 0),
  objectives text[] not null default '{}',
  prerequisites text[] not null default '{}',
  status text not null default 'draft' check (status in ('draft', 'published', 'coming_soon')),
  is_premium boolean not null default false,
  position integer not null default 0,
  created_at timestamptz not null default now()
);

create table public.modules (
  id uuid primary key default gen_random_uuid(),
  course_id uuid not null references public.courses (id) on delete cascade,
  title text not null,
  description text not null default '',
  position integer not null,
  status text not null default 'draft' check (status in ('draft', 'published', 'coming_soon')),
  unique (course_id, position)
);
create index modules_course_id_idx on public.modules (course_id);

create table public.lessons (
  id uuid primary key default gen_random_uuid(),
  module_id uuid not null references public.modules (id) on delete cascade,
  slug text not null check (slug ~ '^[a-z0-9-]+$'),
  title text not null,
  summary text not null default '',
  content_md text not null,
  duration_minutes integer not null default 10 check (duration_minutes > 0),
  position integer not null,
  unique (module_id, position),
  unique (module_id, slug)
);
create index lessons_module_id_idx on public.lessons (module_id);

create table public.quizzes (
  id uuid primary key default gen_random_uuid(),
  module_id uuid not null unique references public.modules (id) on delete cascade,
  title text not null,
  pass_mark numeric(4, 2) not null default 10 check (pass_mark between 0 and 20)
);

create table public.quiz_questions (
  id uuid primary key default gen_random_uuid(),
  quiz_id uuid not null references public.quizzes (id) on delete cascade,
  position integer not null,
  kind text not null check (kind in ('single', 'multiple', 'true_false')),
  prompt text not null,
  code text,
  points numeric(5, 2) not null default 1 check (points > 0),
  unique (quiz_id, position)
);
create index quiz_questions_quiz_id_idx on public.quiz_questions (quiz_id);

create table public.quiz_options (
  id uuid primary key default gen_random_uuid(),
  question_id uuid not null references public.quiz_questions (id) on delete cascade,
  position integer not null,
  label text not null,
  unique (question_id, position)
);
create index quiz_options_question_id_idx on public.quiz_options (question_id);

-- Les bonnes réponses vivent dans le schéma privé : jamais exposées à l'API.
create table private.quiz_answer_keys (
  question_id uuid primary key references public.quiz_questions (id) on delete cascade,
  correct_option_ids uuid[] not null check (cardinality(correct_option_ids) > 0),
  explanation text not null default ''
);

-- Fonction d'aide : un module est-il visible (cours publié + module publié) ?
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
  );
$$;

alter table public.courses enable row level security;
alter table public.modules enable row level security;
alter table public.lessons enable row level security;
alter table public.quizzes enable row level security;
alter table public.quiz_questions enable row level security;
alter table public.quiz_options enable row level security;

create policy "courses: catalogue public"
  on public.courses for select to anon, authenticated
  using (status in ('published', 'coming_soon'));

create policy "modules: plan de cours public"
  on public.modules for select to anon, authenticated
  using (exists (
    select 1 from public.courses c
    where c.id = course_id and c.status = 'published'
  ) and status in ('published', 'coming_soon'));

-- Les leçons (titres + contenu) sont visibles par tous pour le SEO du plan de cours,
-- mais le contenu n'est servi par l'application qu'aux personnes connectées.
create policy "lessons: lecture des modules publiés"
  on public.lessons for select to authenticated
  using ((select private.module_is_public(module_id)));

create policy "quizzes: lecture des modules publiés"
  on public.quizzes for select to authenticated
  using ((select private.module_is_public(module_id)));

create policy "quiz_questions: lecture des quiz publiés"
  on public.quiz_questions for select to authenticated
  using (exists (
    select 1 from public.quizzes q
    where q.id = quiz_id and private.module_is_public(q.module_id)
  ));

create policy "quiz_options: lecture des quiz publiés"
  on public.quiz_options for select to authenticated
  using (exists (
    select 1
    from public.quiz_questions qq
    join public.quizzes q on q.id = qq.quiz_id
    where qq.id = question_id and private.module_is_public(q.module_id)
  ));

revoke insert, update, delete on public.courses, public.modules, public.lessons,
  public.quizzes, public.quiz_questions, public.quiz_options from anon, authenticated;
grant select on public.courses, public.modules to anon, authenticated;
grant select on public.lessons, public.quizzes, public.quiz_questions, public.quiz_options to authenticated;

-- ---------------------------------------------------------------------------
-- Données étudiant
-- ---------------------------------------------------------------------------
create table public.enrollments (
  user_id uuid not null references auth.users (id) on delete cascade,
  course_id uuid not null references public.courses (id) on delete cascade,
  created_at timestamptz not null default now(),
  last_lesson_id uuid references public.lessons (id) on delete set null,
  last_activity_at timestamptz not null default now(),
  primary key (user_id, course_id)
);
create index enrollments_course_id_idx on public.enrollments (course_id);
create index enrollments_last_lesson_id_idx on public.enrollments (last_lesson_id);

create table public.lesson_progress (
  user_id uuid not null references auth.users (id) on delete cascade,
  lesson_id uuid not null references public.lessons (id) on delete cascade,
  completed_at timestamptz not null default now(),
  primary key (user_id, lesson_id)
);
create index lesson_progress_lesson_id_idx on public.lesson_progress (lesson_id);

create table public.quiz_attempts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  quiz_id uuid not null references public.quizzes (id) on delete cascade,
  points numeric(6, 2) not null,
  max_points numeric(6, 2) not null,
  score_20 numeric(4, 2) not null check (score_20 between 0 and 20),
  passed boolean not null,
  corrections jsonb not null,
  created_at timestamptz not null default now()
);
create index quiz_attempts_user_quiz_idx on public.quiz_attempts (user_id, quiz_id, created_at desc);
create index quiz_attempts_quiz_id_idx on public.quiz_attempts (quiz_id);

alter table public.enrollments enable row level security;
alter table public.lesson_progress enable row level security;
alter table public.quiz_attempts enable row level security;

create policy "enrollments: lecture du propriétaire"
  on public.enrollments for select to authenticated
  using ((select auth.uid()) = user_id);

create policy "lesson_progress: lecture du propriétaire"
  on public.lesson_progress for select to authenticated
  using ((select auth.uid()) = user_id);

create policy "quiz_attempts: lecture du propriétaire"
  on public.quiz_attempts for select to authenticated
  using ((select auth.uid()) = user_id);

-- Toutes les écritures passent par des fonctions contrôlées (pas d'insert direct).
revoke insert, update, delete on public.enrollments, public.lesson_progress, public.quiz_attempts
  from anon, authenticated;
grant select on public.enrollments, public.lesson_progress, public.quiz_attempts to authenticated;

-- ---------------------------------------------------------------------------
-- RPC : inscription à une formation
-- ---------------------------------------------------------------------------
create or replace function public.enroll_in_course(p_course_id uuid)
returns void
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_uid uuid := auth.uid();
begin
  if v_uid is null then
    raise exception 'Authentification requise' using errcode = '28000';
  end if;
  if not exists (select 1 from public.courses where id = p_course_id and status = 'published') then
    raise exception 'Formation indisponible' using errcode = 'P0002';
  end if;
  insert into public.enrollments (user_id, course_id)
  values (v_uid, p_course_id)
  on conflict (user_id, course_id) do nothing;
end;
$$;

-- ---------------------------------------------------------------------------
-- RPC : leçon terminée (+ reprise)
-- ---------------------------------------------------------------------------
create or replace function public.complete_lesson(p_lesson_id uuid)
returns void
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_uid uuid := auth.uid();
  v_course_id uuid;
begin
  if v_uid is null then
    raise exception 'Authentification requise' using errcode = '28000';
  end if;

  select m.course_id into v_course_id
  from public.lessons l
  join public.modules m on m.id = l.module_id
  where l.id = p_lesson_id and private.module_is_public(m.id);

  if v_course_id is null then
    raise exception 'Leçon indisponible' using errcode = 'P0002';
  end if;

  insert into public.enrollments (user_id, course_id, last_lesson_id, last_activity_at)
  values (v_uid, v_course_id, p_lesson_id, now())
  on conflict (user_id, course_id)
  do update set last_lesson_id = excluded.last_lesson_id, last_activity_at = now();

  insert into public.lesson_progress (user_id, lesson_id)
  values (v_uid, p_lesson_id)
  on conflict (user_id, lesson_id) do nothing;
end;
$$;

-- Mémorise la dernière leçon ouverte (bouton « Reprendre »), sans la marquer terminée.
create or replace function public.touch_lesson(p_lesson_id uuid)
returns void
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_uid uuid := auth.uid();
  v_course_id uuid;
begin
  if v_uid is null then
    raise exception 'Authentification requise' using errcode = '28000';
  end if;

  select m.course_id into v_course_id
  from public.lessons l
  join public.modules m on m.id = l.module_id
  where l.id = p_lesson_id and private.module_is_public(m.id);

  if v_course_id is null then
    raise exception 'Leçon indisponible' using errcode = 'P0002';
  end if;

  insert into public.enrollments (user_id, course_id, last_lesson_id, last_activity_at)
  values (v_uid, v_course_id, p_lesson_id, now())
  on conflict (user_id, course_id)
  do update set last_lesson_id = excluded.last_lesson_id, last_activity_at = now();
end;
$$;

-- ---------------------------------------------------------------------------
-- RPC : correction d'un quiz — calcul exclusivement côté serveur
-- p_answers : {"<question_id>": ["<option_id>", ...], ...}
-- Règle : une question rapporte tous ses points si l'ensemble des options cochées
-- est exactement l'ensemble des bonnes réponses, 0 sinon.
-- ---------------------------------------------------------------------------
create or replace function public.submit_quiz(p_quiz_id uuid, p_answers jsonb)
returns public.quiz_attempts
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_uid uuid := auth.uid();
  v_module_id uuid;
  v_course_id uuid;
  v_pass_mark numeric;
  v_points numeric := 0;
  v_max numeric := 0;
  v_score numeric;
  v_corrections jsonb := '[]'::jsonb;
  v_recent integer;
  v_attempt public.quiz_attempts;
  r record;
  v_selected uuid[];
  v_ok boolean;
begin
  if v_uid is null then
    raise exception 'Authentification requise' using errcode = '28000';
  end if;

  if p_answers is null or jsonb_typeof(p_answers) <> 'object' then
    raise exception 'Format de réponses invalide' using errcode = '22023';
  end if;

  select q.module_id, q.pass_mark, m.course_id
    into v_module_id, v_pass_mark, v_course_id
  from public.quizzes q
  join public.modules m on m.id = q.module_id
  where q.id = p_quiz_id and private.module_is_public(q.module_id);

  if v_module_id is null then
    raise exception 'Quiz indisponible' using errcode = 'P0002';
  end if;

  -- Anti-abus : 10 tentatives max par minute et par quiz.
  select count(*) into v_recent
  from public.quiz_attempts
  where user_id = v_uid and quiz_id = p_quiz_id and created_at > now() - interval '1 minute';
  if v_recent >= 10 then
    raise exception 'Trop de tentatives, réessayez dans une minute' using errcode = '54000';
  end if;

  for r in
    select qq.id, qq.points, qq.position, k.correct_option_ids, k.explanation
    from public.quiz_questions qq
    join private.quiz_answer_keys k on k.question_id = qq.id
    where qq.quiz_id = p_quiz_id
    order by qq.position
  loop
    v_selected := array(
      select distinct o.id
      from jsonb_array_elements_text(
             case when jsonb_typeof(p_answers -> r.id::text) = 'array'
                  then p_answers -> r.id::text else '[]'::jsonb end
           ) as a(val)
      join public.quiz_options o
        on o.question_id = r.id
       and o.id::text = a.val
    );

    v_ok := cardinality(v_selected) > 0
            and v_selected <@ r.correct_option_ids
            and r.correct_option_ids <@ v_selected;

    v_max := v_max + r.points;
    if v_ok then
      v_points := v_points + r.points;
    end if;

    v_corrections := v_corrections || jsonb_build_object(
      'question_id', r.id,
      'selected', to_jsonb(v_selected),
      'correct', to_jsonb(r.correct_option_ids),
      'is_correct', v_ok,
      'points', case when v_ok then r.points else 0 end,
      'max_points', r.points,
      'explanation', r.explanation
    );
  end loop;

  if v_max = 0 then
    raise exception 'Quiz sans question' using errcode = 'P0002';
  end if;

  v_score := round(v_points / v_max * 20, 2);

  insert into public.enrollments (user_id, course_id)
  values (v_uid, v_course_id)
  on conflict (user_id, course_id) do update set last_activity_at = now();

  insert into public.quiz_attempts (user_id, quiz_id, points, max_points, score_20, passed, corrections)
  values (v_uid, p_quiz_id, v_points, v_max, v_score, v_score >= v_pass_mark, v_corrections)
  returning * into v_attempt;

  return v_attempt;
end;
$$;

revoke execute on function public.enroll_in_course(uuid) from public, anon;
revoke execute on function public.complete_lesson(uuid) from public, anon;
revoke execute on function public.touch_lesson(uuid) from public, anon;
revoke execute on function public.submit_quiz(uuid, jsonb) from public, anon;
grant execute on function public.enroll_in_course(uuid) to authenticated;
grant execute on function public.complete_lesson(uuid) to authenticated;
grant execute on function public.touch_lesson(uuid) to authenticated;
grant execute on function public.submit_quiz(uuid, jsonb) to authenticated;

revoke execute on function private.handle_new_user() from public, anon, authenticated;
revoke execute on function private.touch_updated_at() from public, anon, authenticated;
-- module_is_public est appelée dans les politiques RLS : les rôles API doivent pouvoir l'exécuter
-- (elle ne renvoie qu'un booléen sur des données de catalogue déjà publiques).
grant usage on schema private to anon, authenticated;
revoke execute on function private.module_is_public(uuid) from public;
grant execute on function private.module_is_public(uuid) to anon, authenticated;
revoke all on private.quiz_answer_keys from public, anon, authenticated;
