"use client";

import { useActionState, type ReactNode } from "react";
import type { AdminState } from "@/app/admin/actions";

/** Formulaire d'administration : action serveur + message de résultat accessible. */
export function ActionForm({
  action,
  children,
  submitLabel,
  pendingLabel = "Enregistrement…",
  className = "grid gap-5",
  danger = false,
  subtle = false,
}: {
  action: (prev: AdminState, form: FormData) => Promise<AdminState>;
  children: ReactNode;
  submitLabel: string;
  pendingLabel?: string;
  className?: string;
  danger?: boolean;
  subtle?: boolean;
}) {
  const [state, formAction, pending] = useActionState(action, {});
  return (
    <form action={formAction} className={className}>
      {children}
      <div className="flex flex-wrap items-center gap-3">
        <button
          type="submit"
          disabled={pending}
          className={`btn ${danger ? "bg-red text-white hover:opacity-90" : subtle ? "btn-secondary min-h-[36px] px-4 py-1 text-[14px]" : "btn-primary"}`}
        >
          {pending ? pendingLabel : submitLabel}
        </button>
        <p aria-live="polite" className={`text-sm ${state.error ? "text-red" : "text-green"}`}>
          {state.error ?? state.message}
        </p>
      </div>
    </form>
  );
}

export function Field({
  label,
  name,
  defaultValue,
  hint,
  required,
  maxLength,
  type = "text",
  inputMode,
}: {
  label: string;
  name: string;
  defaultValue?: string | number;
  hint?: string;
  required?: boolean;
  maxLength?: number;
  type?: string;
  inputMode?: "numeric" | "text";
}) {
  return (
    <div className="field">
      <label htmlFor={name}>{label}</label>
      <input
        id={name}
        name={name}
        type={type}
        className="input"
        defaultValue={defaultValue}
        required={required}
        maxLength={maxLength}
        inputMode={inputMode}
        aria-describedby={hint ? `${name}-hint` : undefined}
      />
      {hint && (
        <p id={`${name}-hint`} className="text-sm text-ink-3">
          {hint}
        </p>
      )}
    </div>
  );
}

export function TextArea({
  label,
  name,
  defaultValue,
  hint,
  rows = 4,
  mono = false,
  maxLength,
}: {
  label: string;
  name: string;
  defaultValue?: string;
  hint?: string;
  rows?: number;
  mono?: boolean;
  maxLength?: number;
}) {
  return (
    <div className="field">
      <label htmlFor={name}>{label}</label>
      <textarea
        id={name}
        name={name}
        rows={rows}
        className={`input !min-h-0 leading-relaxed ${mono ? "font-mono text-[14px]" : ""}`}
        defaultValue={defaultValue}
        maxLength={maxLength}
        aria-describedby={hint ? `${name}-hint` : undefined}
      />
      {hint && (
        <p id={`${name}-hint`} className="text-sm text-ink-3">
          {hint}
        </p>
      )}
    </div>
  );
}
