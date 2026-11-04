-- Les offres ont un identifiant texte : journal d'audit dédié (le déclencheur générique attend un UUID).
create or replace function private.audit_plan_change()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into private.audit_log (actor_id, action, entity, entity_id, summary)
  values ((select auth.uid()), tg_op, 'plans', null, jsonb_build_object(
    'plan', new.id, 'name', new.name, 'price_cents', new.price_cents, 'old_price_cents', old.price_cents,
    'is_active', new.is_active));
  return null;
end;
$$;
revoke execute on function private.audit_plan_change() from public, anon, authenticated;

create or replace trigger audit_plans after update on public.plans
  for each row execute function private.audit_plan_change();
