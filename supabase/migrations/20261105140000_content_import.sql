-- Import automatique des formations depuis le dépôt (étape de build Netlify).
-- Appelé sans session, protégé par un jeton dont seule l'empreinte SHA-256 est stockée
-- (private.app_secrets, name = 'content_import'). Idempotent ; ne supprime jamais rien.
-- Les garde-fous de publication s'appliquent : un module ou une formation incomplète ne peut pas être publié.

create or replace function public.content_import_course(p_token text, p_payload jsonb)
returns text
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_hash text;
  c jsonb := p_payload -> 'course';
  m jsonb;
  q jsonb;
  v_cid uuid := (c ->> 'id')::uuid;
  v_lessons int := 0;
  v_questions int := 0;
begin
  select sha256_hex into v_hash from private.app_secrets where name = 'content_import';
  if v_hash is null or p_token is null or encode(extensions.digest(p_token, 'sha256'), 'hex') <> v_hash then
    raise exception 'Jeton d''import invalide' using errcode = '42501';
  end if;
  if c is null or v_cid is null then
    raise exception 'Formation absente du contenu' using errcode = '22023';
  end if;

  insert into public.courses (id, slug, title, subtitle, description, category_id, topic, cover_label, level,
    duration_minutes, objectives, prerequisites, status, is_premium, position)
  values (v_cid, c ->> 'slug', c ->> 'title', c ->> 'subtitle', c ->> 'description',
    (select id from public.categories where slug = c ->> 'category_slug'), coalesce(c ->> 'topic', ''),
    coalesce(c ->> 'cover_label', ''), c ->> 'level', (c ->> 'duration_minutes')::int,
    array(select jsonb_array_elements_text(c -> 'objectives')), array(select jsonb_array_elements_text(c -> 'prerequisites')),
    'coming_soon', (c ->> 'is_premium')::boolean, (c ->> 'position')::int)
  on conflict (slug) do update set title = excluded.title, subtitle = excluded.subtitle, description = excluded.description,
    category_id = excluded.category_id, topic = excluded.topic, cover_label = excluded.cover_label, level = excluded.level,
    duration_minutes = excluded.duration_minutes, objectives = excluded.objectives, prerequisites = excluded.prerequisites,
    is_premium = excluded.is_premium, position = excluded.position;

  for m in select * from jsonb_array_elements(p_payload -> 'modules') loop
    insert into public.modules (id, course_id, title, description, position, status)
    values ((m ->> 'id')::uuid, v_cid, m ->> 'title', m ->> 'description', (m ->> 'position')::int, 'draft')
    on conflict (id) do update set title = excluded.title, description = excluded.description, position = excluded.position;

    insert into public.lessons (id, module_id, slug, title, summary, content_md, duration_minutes, position)
    select l.id, (m ->> 'id')::uuid, l.slug, l.title, l.summary, l.content_md, l.duration_minutes, l.position
    from jsonb_to_recordset(m -> 'lessons') as l(id uuid, slug text, title text, summary text, content_md text,
                                                 duration_minutes int, position int)
    on conflict (id) do update set slug = excluded.slug, title = excluded.title, summary = excluded.summary,
      content_md = excluded.content_md, duration_minutes = excluded.duration_minutes, position = excluded.position;
    v_lessons := v_lessons + jsonb_array_length(m -> 'lessons');

    if m ? 'quiz' and jsonb_typeof(m -> 'quiz') = 'object' then
      insert into public.quizzes (id, module_id, title, pass_mark)
      values ((m -> 'quiz' ->> 'id')::uuid, (m ->> 'id')::uuid, m -> 'quiz' ->> 'title', (m -> 'quiz' ->> 'pass_mark')::numeric)
      on conflict (id) do update set title = excluded.title, pass_mark = excluded.pass_mark;

      for q in select * from jsonb_array_elements(m -> 'quiz' -> 'questions') loop
        insert into public.quiz_questions (id, quiz_id, position, kind, prompt, code, points)
        values ((q ->> 'id')::uuid, (m -> 'quiz' ->> 'id')::uuid, (q ->> 'position')::int, q ->> 'kind',
                q ->> 'prompt', q ->> 'code', (q ->> 'points')::numeric)
        on conflict (id) do update set position = excluded.position, kind = excluded.kind, prompt = excluded.prompt,
          code = excluded.code, points = excluded.points;

        insert into public.quiz_options (id, question_id, position, label)
        select o.id, (q ->> 'id')::uuid, o.position, o.label
        from jsonb_to_recordset(q -> 'options') as o(id uuid, position int, label text)
        on conflict (id) do update set position = excluded.position, label = excluded.label;

        insert into private.quiz_answer_keys (question_id, correct_option_ids, explanation)
        values ((q ->> 'id')::uuid, array(select jsonb_array_elements_text(q -> 'correct'))::uuid[], q ->> 'explanation')
        on conflict (question_id) do update set correct_option_ids = excluded.correct_option_ids,
          explanation = excluded.explanation;
        v_questions := v_questions + 1;
      end loop;
    end if;
  end loop;

  -- Statuts en dernier (garde-fous de complétude)
  update public.modules mo set status = x.status
  from jsonb_to_recordset(p_payload -> 'modules') as x(id uuid, status text)
  where mo.id = x.id and mo.status is distinct from x.status;
  update public.courses set status = c ->> 'status' where id = v_cid and status is distinct from c ->> 'status';

  return format('%s : %s modules, %s leçons, %s questions, statut %s', c ->> 'slug',
    jsonb_array_length(p_payload -> 'modules'), v_lessons, v_questions, c ->> 'status');
end;
$$;

revoke execute on function public.content_import_course(text, jsonb) from public;
grant execute on function public.content_import_course(text, jsonb) to anon, authenticated;
