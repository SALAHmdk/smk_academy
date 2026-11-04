-- Durcissement : Supabase accorde par défaut tous les privilèges (dont TRUNCATE) aux rôles API
-- sur les nouvelles tables du schéma public. On repart de zéro et on n'accorde que le nécessaire.

revoke all on public.profiles, public.courses, public.modules, public.lessons, public.quizzes,
  public.quiz_questions, public.quiz_options, public.enrollments, public.lesson_progress,
  public.quiz_attempts from anon, authenticated;

-- Catalogue public
grant select on public.courses, public.modules to anon, authenticated;

-- Contenu réservé aux comptes connectés
grant select on public.lessons, public.quizzes, public.quiz_questions, public.quiz_options to authenticated;

-- Données personnelles (filtrées par RLS ; écriture uniquement via fonctions)
grant select on public.profiles, public.enrollments, public.lesson_progress, public.quiz_attempts to authenticated;
grant update (full_name) on public.profiles to authenticated;

-- Les futures tables ne reçoivent plus de droits automatiques.
alter default privileges in schema public revoke all on tables from anon, authenticated;
alter default privileges in schema public revoke all on functions from anon, authenticated, public;
