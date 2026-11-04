"use client";

import { useActionState } from "react";
import { openBillingPortal, redeemCode, startCheckout, type BillingState } from "@/app/actions/billing";

export function CheckoutButton({ plan, label, primary }: { plan: string; label: string; primary?: boolean }) {
  const [state, action, pending] = useActionState(startCheckout, {} as BillingState);
  return (
    <form action={action} className="grid gap-2">
      <input type="hidden" name="plan" value={plan} />
      <button type="submit" disabled={pending} className={`btn w-full ${primary ? "btn-primary" : "btn-secondary"}`}>
        {pending ? "Redirection vers le paiement…" : label}
      </button>
      <p aria-live="polite" className="text-center text-[13px] text-red">
        {state.error}
      </p>
    </form>
  );
}

export function PortalButton() {
  const [state, action, pending] = useActionState(async () => openBillingPortal(), {} as BillingState);
  return (
    <form action={action} className="grid gap-2">
      <button type="submit" disabled={pending} className="btn btn-secondary">
        {pending ? "Ouverture…" : "Gérer le paiement, les factures ou résilier"}
      </button>
      <p aria-live="polite" className="text-[13px] text-red">
        {state.error}
      </p>
    </form>
  );
}

export function RedeemForm() {
  const [state, action, pending] = useActionState(redeemCode, {} as BillingState);
  return (
    <form action={action} className="grid gap-3">
      <div className="field">
        <label htmlFor="code">Code promo</label>
        <div className="flex flex-col gap-2 sm:flex-row">
          <input
            id="code"
            name="code"
            className="input font-mono uppercase tracking-wide sm:flex-1"
            placeholder="SMK-XXXX-XXXX-XXXX"
            autoComplete="off"
            autoCapitalize="characters"
            spellCheck={false}
            maxLength={40}
            required
          />
          <button type="submit" disabled={pending} className="btn btn-primary">
            {pending ? "Vérification…" : "Utiliser le code"}
          </button>
        </div>
      </div>
      <p aria-live="polite" className={`text-sm ${state.error ? "text-red" : "text-green"}`}>
        {state.error ?? state.message}
      </p>
    </form>
  );
}
