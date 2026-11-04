import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { AuthShell } from "@/components/auth-shell";
import { TotpLoginForm } from "@/components/mfa-forms";
import { safeNextPath } from "@/lib/learning";
import { createClient, getCurrentUser } from "@/lib/supabase/server";

export const metadata: Metadata = { title: "Vérification en deux étapes", robots: { index: false } };

type Props = { searchParams: Promise<{ suite?: string }> };

export default async function TotpVerificationPage({ searchParams }: Props) {
  const next = safeNextPath((await searchParams).suite);
  if (!(await getCurrentUser())) redirect(`/connexion?suite=${encodeURIComponent(next)}`);
  const supabase = await createClient();
  const { data: aal } = await supabase.auth.mfa.getAuthenticatorAssuranceLevel();
  if (aal?.currentLevel === "aal2" || aal?.nextLevel !== "aal2") redirect(next);

  return (
    <AuthShell
      title="Vérification en deux étapes"
      subtitle="Saisissez le code affiché par votre application d'authentification."
    >
      <TotpLoginForm next={next} />
    </AuthShell>
  );
}
