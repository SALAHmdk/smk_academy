"use client";

import { useActionState } from "react";
import { updateProfile } from "@/app/actions/preferences";

export function ProfileForm({ fullName }: { fullName: string }) {
  const [state, action, pending] = useActionState(updateProfile, {});
  return (
    <form action={action} className="relative flex flex-col gap-3 sm:flex-row sm:items-end sm:pb-5">
      <div className="field flex-1">
        <label htmlFor="fullName">Nom affiché</label>
        <input id="fullName" name="fullName" className="input" defaultValue={fullName} autoComplete="name" maxLength={120} required />
      </div>
      <button type="submit" className="btn btn-secondary" disabled={pending}>
        {pending ? "Enregistrement…" : "Enregistrer"}
      </button>
      <p aria-live="polite" className={`min-h-5 text-sm sm:absolute sm:mt-[5.5rem] ${state.error ? "text-red" : "text-green"}`}>
        {state.error ?? state.message}
      </p>
    </form>
  );
}
