import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { AuthShell } from "@/components/auth-shell";
import { SignUpForm } from "@/components/auth-forms";
import { safeNextPath } from "@/lib/learning";
import { getCurrentUser } from "@/lib/supabase/server";

export const metadata: Metadata = {
  title: "Créer un compte",
  description: "Créez gratuitement votre compte SMK Academy pour suivre les formations et enregistrer votre progression.",
};

type Props = { searchParams: Promise<{ suite?: string }> };

export default async function SignUpPage({ searchParams }: Props) {
  const next = safeNextPath((await searchParams).suite);
  if (await getCurrentUser()) redirect(next);

  return (
    <AuthShell
      title="Créer votre compte"
      subtitle="Gratuit, sans carte bancaire. Votre progression est enregistrée sur tous vos appareils."
      footer={
        <>
          Déjà inscrit ?{" "}
          <Link href={`/connexion?suite=${encodeURIComponent(next)}`} className="font-medium text-blue">
            Se connecter
          </Link>
        </>
      }
    >
      <SignUpForm next={next} />
    </AuthShell>
  );
}
