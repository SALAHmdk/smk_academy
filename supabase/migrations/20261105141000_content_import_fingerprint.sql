-- Empreinte du dernier import : une formation inchangée dans le dépôt n'est pas réimportée
-- (les retouches faites depuis l'administration ne sont écrasées que si la source change).
create table if not exists private.content_imports (
  slug text primary key,
  fingerprint text not null,
  imported_at timestamptz not null default now()
);
revoke all on private.content_imports from public, anon, authenticated;

create or replace function public.content_import_if_changed(p_token text, p_payload jsonb)
returns text
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_slug text := p_payload -> 'course' ->> 'slug';
  v_fp text := md5(p_payload::text);
  v_hash text;
  v_result text;
begin
  select sha256_hex into v_hash from private.app_secrets where name = 'content_import';
  if v_hash is null or p_token is null or encode(extensions.digest(p_token, 'sha256'), 'hex') <> v_hash then
    raise exception 'Jeton d''import invalide' using errcode = '42501';
  end if;
  if exists (select 1 from private.content_imports where slug = v_slug and fingerprint = v_fp) then
    return v_slug || ' : inchangée';
  end if;
  v_result := public.content_import_course(p_token, p_payload);
  insert into private.content_imports (slug, fingerprint) values (v_slug, v_fp)
  on conflict (slug) do update set fingerprint = excluded.fingerprint, imported_at = now();
  return v_result;
end;
$$;
revoke execute on function public.content_import_if_changed(text, jsonb) from public;
grant execute on function public.content_import_if_changed(text, jsonb) to anon, authenticated;
