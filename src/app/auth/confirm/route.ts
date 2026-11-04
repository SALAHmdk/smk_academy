import type { EmailOtpType } from "@supabase/supabase-js";
import { NextResponse, type NextRequest } from "next/server";
import { safeNextPath } from "@/lib/learning";
import { createClient } from "@/lib/supabase/server";

/**
 * Point d'arrivée des liens envoyés par email (confirmation d'inscription, réinitialisation).
 * Gère le flux PKCE (?code=) et le flux token_hash (modèles d'email personnalisés).
 */
export async function GET(request: NextRequest) {
  const { searchParams, origin } = request.nextUrl;
  const next = safeNextPath(searchParams.get("suite"));
  const code = searchParams.get("code");
  const tokenHash = searchParams.get("token_hash");
  const type = searchParams.get("type") as EmailOtpType | null;

  const supabase = await createClient();
  let ok = false;

  if (code) {
    ok = !(await supabase.auth.exchangeCodeForSession(code)).error;
  } else if (tokenHash && type) {
    ok = !(await supabase.auth.verifyOtp({ type, token_hash: tokenHash })).error;
  }

  if (ok) return NextResponse.redirect(new URL(next, origin));
  return NextResponse.redirect(new URL("/connexion?lien=invalide", origin));
}
