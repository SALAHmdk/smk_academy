import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { AuthShell } from "@/components/auth-shell";
import { SignInForm } from "@/components/auth-forms";
import { safeNextPath } from "@/lib/learning";
import { getCurrentUser } from "@/lib/supabase/server";

export const metadata: Metadata = { title: "Connexion" };

type Props = { searchParams: Promise<{ suite?: string; lien?: string }> };

export default async function SignInPage({ searchParams }: Props) {
  const params = await searchParams;
  const next = safeNextPath(params.suite);
  if (await getCurrentUser()) redirect(next);

  return (
    <AuthShell
      title="Connexion"
      subtitle="Retrouvez vos formations là où vous les avez laissées."
      footer={
        <>
          Pas encore de compte ?{" "}
          <Link href={`/inscription?suite=${encodeURIComponent(next)}`} className="font-medium text-blue">
            Créer un compte gratuit
          </Link>
        </>
      }
    >
      <SignInForm
        next={next}
        notice={params.lien === "invalide" ? "Ce lien a expiré ou a déjà été utilisé. Connectez-vous, ou demandez un nouveau lien." : undefined}
      />
    </AuthShell>
  );
}
