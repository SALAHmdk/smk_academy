"use client";

import { useActionState, useState, useTransition } from "react";
import {
  confirmTotpEnrollment,
  startTotpEnrollment,
  verifyTotpLogin,
  type EnrollState,
} from "@/app/actions/mfa";

function CodeInput({ autoFocus = false }: { autoFocus?: boolean }) {
  return (
    <div className="field">
      <label htmlFor="code">Code à 6 chiffres</label>
      <input
        id="code"
        name="code"
        className="input text-center font-mono text-2xl tracking-[0.4em]"
        inputMode="numeric"
        autoComplete="one-time-code"
        pattern="\d{6}"
        maxLength={6}
        required
        autoFocus={autoFocus}
      />
    </div>
  );
}

export function TotpEnrollment() {
  const [setup, setSetup] = useState<EnrollState | null>(null);
  const [starting, startTransition] = useTransition();
  const [state, action, pending] = useActionState(confirmTotpEnrollment, {});

  if (state.done) {
    return (
      <p role="status" className="rounded-[var(--radius-md)] bg-green-soft px-4 py-3 text-green">
        Double authentification activée. Votre application vous demandera désormais un code à chaque connexion.
      </p>
    );
  }

  if (!setup?.factorId) {
    return (
      <div>
        <button
          type="button"
          className="btn btn-primary"
          disabled={starting}
          onClick={() => startTransition(async () => setSetup(await startTotpEnrollment()))}
        >
          {starting ? "Préparation…" : "Activer la double authentification"}
        </button>
        {setup?.error && (
          <p role="alert" className="mt-3 text-sm text-red">
            {setup.error}
          </p>
        )}
      </div>
    );
  }

  return (
    <div className="grid gap-6 sm:grid-cols-[200px_1fr] sm:items-start">
      <div className="rounded-[var(--radius-md)] bg-white p-3">
        {/* QR code SVG fourni par Supabase (data URL) */}
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={setup.qr} alt="QR code à scanner avec votre application d'authentification" className="h-auto w-full" />
      </div>
      <div>
        <ol className="list-decimal space-y-1.5 pl-5 text-[15px] text-ink-2">
          <li>Ouvrez Google Authenticator, Microsoft Authenticator ou une application compatible TOTP.</li>
          <li>Scannez le QR code, ou saisissez la clé ci-dessous.</li>
          <li>Entrez le code à 6 chiffres affiché.</li>
        </ol>
        <p className="mt-3 break-all rounded-[var(--radius-sm)] bg-surface-2 px-3 py-2 font-mono text-[13px]">{setup.secret}</p>
        <form action={action} className="mt-4 grid gap-3">
          <input type="hidden" name="factorId" value={setup.factorId} />
          <CodeInput autoFocus />
          {state.error && (
            <p role="alert" className="text-sm text-red">
              {state.error}
            </p>
          )}
          <button type="submit" className="btn btn-primary" disabled={pending}>
            {pending ? "Vérification…" : "Vérifier et activer"}
          </button>
        </form>
      </div>
    </div>
  );
}

export function TotpLoginForm({ next }: { next: string }) {
  const [state, action, pending] = useActionState(verifyTotpLogin, {});
  return (
    <form action={action} className="grid gap-5">
      <input type="hidden" name="suite" value={next} />
      <CodeInput autoFocus />
      {state.error && (
        <p role="alert" className="rounded-[var(--radius-md)] bg-red-soft px-4 py-3 text-[0.95rem] text-red">
          {state.error}
        </p>
      )}
      <button type="submit" className="btn btn-primary w-full" disabled={pending}>
        {pending ? "Vérification…" : "Valider"}
      </button>
    </form>
  );
}
