"use client";

import Link from "next/link";
import { useActionState } from "react";
import {
  requestPasswordReset,
  signIn,
  signUp,
  updatePassword,
  type FormState,
} from "@/app/actions/auth";

function Feedback({ state }: { state: FormState }) {
  if (state.error)
    return (
      <p role="alert" className="rounded-[var(--radius-md)] bg-red-soft px-4 py-3 text-[0.95rem] text-red">
        {state.error}
      </p>
    );
  if (state.message)
    return (
      <p role="status" className="rounded-[var(--radius-md)] bg-green-soft px-4 py-3 text-[0.95rem] text-green">
        {state.message}
      </p>
    );
  return null;
}

export function SignUpForm({ next }: { next?: string }) {
  const [state, action, pending] = useActionState(signUp, {});
  if (state.message) return <Feedback state={state} />;

  return (
    <form action={action} className="grid gap-5" noValidate>
      <div className="field">
        <label htmlFor="fullName">Nom complet</label>
        <input id="fullName" name="fullName" className="input" autoComplete="name" required maxLength={120} defaultValue={state.fields?.fullName} />
      </div>
      <div className="field">
        <label htmlFor="email">Adresse email</label>
        <input id="email" name="email" type="email" className="input" autoComplete="email" inputMode="email" required defaultValue={state.fields?.email} />
      </div>
      <div className="field">
        <label htmlFor="password">Mot de passe</label>
        <input id="password" name="password" type="password" className="input" autoComplete="new-password" required minLength={8} maxLength={72} aria-describedby="password-hint" />
        <p id="password-hint" className="text-sm text-ink-3">
          8 caractères minimum.
        </p>
      </div>
      <label className="flex items-start gap-3 text-[0.95rem] text-ink-2">
        <input type="checkbox" name="terms" className="mt-1 h-5 w-5 shrink-0 accent-[var(--smk-blue)]" required />
        <span>J&apos;accepte que SMK Academy conserve mes données de compte et de progression pour me fournir le service.</span>
      </label>
      {next && <input type="hidden" name="suite" value={next} />}
      <Feedback state={state} />
      <button type="submit" className="btn btn-primary w-full" disabled={pending}>
        {pending ? "Création du compte…" : "Créer mon compte"}
      </button>
    </form>
  );
}

export function SignInForm({ next, notice }: { next?: string; notice?: string }) {
  const [state, action, pending] = useActionState(signIn, {});
  return (
    <form action={action} className="grid gap-5" noValidate>
      {notice && !state.error && (
        <p role="status" className="rounded-[var(--radius-md)] bg-surface-2 px-4 py-3 text-[0.95rem] text-ink-2">
          {notice}
        </p>
      )}
      <div className="field">
        <label htmlFor="email">Adresse email</label>
        <input id="email" name="email" type="email" className="input" autoComplete="email" inputMode="email" required defaultValue={state.fields?.email} />
      </div>
      <div className="field">
        <div className="flex items-baseline justify-between">
          <label htmlFor="password">Mot de passe</label>
          <Link href="/mot-de-passe-oublie" className="text-sm font-medium text-blue">
            Mot de passe oublié ?
          </Link>
        </div>
        <input id="password" name="password" type="password" className="input" autoComplete="current-password" required />
      </div>
      <input type="hidden" name="suite" value={next ?? "/tableau-de-bord"} />
      <Feedback state={state} />
      <button type="submit" className="btn btn-primary w-full" disabled={pending}>
        {pending ? "Connexion…" : "Se connecter"}
      </button>
    </form>
  );
}

export function ForgotPasswordForm() {
  const [state, action, pending] = useActionState(requestPasswordReset, {});
  if (state.message) return <Feedback state={state} />;
  return (
    <form action={action} className="grid gap-5" noValidate>
      <div className="field">
        <label htmlFor="email">Adresse email du compte</label>
        <input id="email" name="email" type="email" className="input" autoComplete="email" inputMode="email" required />
      </div>
      <Feedback state={state} />
      <button type="submit" className="btn btn-primary w-full" disabled={pending}>
        {pending ? "Envoi…" : "Recevoir un lien de réinitialisation"}
      </button>
    </form>
  );
}

export function NewPasswordForm() {
  const [state, action, pending] = useActionState(updatePassword, {});
  return (
    <form action={action} className="grid gap-5" noValidate>
      <div className="field">
        <label htmlFor="password">Nouveau mot de passe</label>
        <input id="password" name="password" type="password" className="input" autoComplete="new-password" required minLength={8} maxLength={72} />
      </div>
      <div className="field">
        <label htmlFor="confirm">Confirmez le mot de passe</label>
        <input id="confirm" name="confirm" type="password" className="input" autoComplete="new-password" required />
      </div>
      <Feedback state={state} />
      <button type="submit" className="btn btn-primary w-full" disabled={pending}>
        {pending ? "Enregistrement…" : "Enregistrer le mot de passe"}
      </button>
    </form>
  );
}
