import type { Metadata } from "next";
import { AuthShell } from "@/components/auth-shell";
import { NewPasswordForm } from "@/components/auth-forms";

export const metadata: Metadata = { title: "Nouveau mot de passe", robots: { index: false } };

export default function NewPasswordPage() {
  return (
    <AuthShell title="Choisissez un nouveau mot de passe">
      <NewPasswordForm />
    </AuthShell>
  );
}
