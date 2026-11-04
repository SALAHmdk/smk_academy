"use server";

import { revalidatePath } from "next/cache";
import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { z } from "zod";
import { env } from "@/lib/env";
import { stripeConfig, stripeRequest } from "@/lib/stripe";
import { createClient, getCurrentUser } from "@/lib/supabase/server";

export type BillingState = { error?: string; message?: string };

async function origin(): Promise<string> {
  const h = (await headers()).get("origin");
  if (h && /^https?:\/\/[a-z0-9.-]+(:\d+)?$/i.test(h)) return h;
  return env.siteUrl;
}

/** Démarre un abonnement Stripe Checkout (mode test). Le prix est lu en base, jamais dans le formulaire. */
export async function startCheckout(_prev: BillingState, form: FormData): Promise<BillingState> {
  const user = await getCurrentUser();
  if (!user) redirect("/connexion?suite=/tarifs");

  const planId = z.enum(["premium_monthly", "premium_yearly"]).safeParse(form.get("plan"));
  if (!planId.success) return { error: "Offre inconnue." };

  const cfg = stripeConfig();
  if (!cfg) return { error: "Le paiement en ligne sera ouvert très prochainement. En attendant, vous pouvez utiliser un code promo." };

  const supabase = await createClient();
  const [{ data: plan }, { data: access }, { data: sub }] = await Promise.all([
    supabase.from("plans").select("id, name, price_cents, billing_interval, is_active").eq("id", planId.data).single(),
    supabase.rpc("my_access"),
    supabase.from("subscriptions").select("provider_customer_id, status").order("updated_at", { ascending: false }).limit(1).maybeSingle(),
  ]);
  if (!plan || !plan.is_active || !plan.billing_interval) return { error: "Cette offre n'est pas disponible actuellement." };
  const acc = (access ?? {}) as { subscription?: { status: string } | null; unlimited?: boolean };
  if (acc.unlimited) return { error: "Vous bénéficiez déjà d'un accès Premium illimité." };
  if (acc.subscription && ["active", "trialing", "past_due"].includes(acc.subscription.status))
    return { error: "Vous avez déjà un abonnement en cours : gérez-le depuis Mon compte → Abonnement." };

  const base = await origin();
  let url: string;
  try {
    const session = await stripeRequest<{ url: string }>(
      cfg.secretKey,
      "POST",
      "/checkout/sessions",
      {
        mode: "subscription",
        locale: "fr",
        client_reference_id: user.id,
        ...(sub?.provider_customer_id ? { customer: sub.provider_customer_id } : { customer_email: user.email ?? undefined }),
        line_items: [
          {
            quantity: 1,
            price_data: {
              currency: "eur",
              unit_amount: plan.price_cents,
              recurring: { interval: plan.billing_interval },
              product_data: { name: plan.name },
              tax_behavior: "inclusive",
            },
          },
        ],
        metadata: { user_id: user.id, plan_id: plan.id },
        subscription_data: { metadata: { user_id: user.id, plan_id: plan.id } },
        success_url: `${base}/compte/abonnement?paiement=ok`,
        cancel_url: `${base}/tarifs?paiement=annule`,
      },
      `checkout-${user.id}-${plan.id}-${Math.floor(Date.now() / 60000)}`,
    );
    url = session.url;
  } catch (e) {
    console.error("Stripe checkout", e instanceof Error ? e.message : e);
    return { error: "Le paiement n'a pas pu démarrer. Réessayez dans un instant." };
  }
  redirect(url);
}

/** Portail client Stripe : moyen de paiement, factures, résiliation. */
export async function openBillingPortal(): Promise<BillingState> {
  const user = await getCurrentUser();
  if (!user) redirect("/connexion?suite=/compte/abonnement");
  const cfg = stripeConfig();
  if (!cfg) return { error: "La gestion en ligne de l'abonnement n'est pas encore ouverte." };
  const supabase = await createClient();
  const { data: sub } = await supabase
    .from("subscriptions")
    .select("provider_customer_id")
    .eq("provider", "stripe")
    .not("provider_customer_id", "is", null)
    .order("updated_at", { ascending: false })
    .limit(1)
    .maybeSingle();
  if (!sub?.provider_customer_id) return { error: "Aucun abonnement Stripe associé à ce compte." };
  let url: string;
  try {
    const portal = await stripeRequest<{ url: string }>(cfg.secretKey, "POST", "/billing_portal/sessions", {
      customer: sub.provider_customer_id,
      locale: "fr",
      return_url: `${await origin()}/compte/abonnement`,
    });
    url = portal.url;
  } catch (e) {
    console.error("Stripe portal", e instanceof Error ? e.message : e);
    return { error: "Le portail de gestion n'a pas pu s'ouvrir. Réessayez dans un instant." };
  }
  redirect(url);
}

const reasons: Record<string, string> = {
  invalid: "Ce code n'est pas valide, a expiré ou n'est pas destiné à ce compte.",
  already_used: "Vous avez déjà utilisé ce code.",
  already_unlimited: "Votre accès Premium est déjà illimité.",
  rate_limited: "Trop d'essais. Réessayez dans une heure.",
};

export async function redeemCode(_prev: BillingState, form: FormData): Promise<BillingState> {
  const user = await getCurrentUser();
  if (!user) redirect("/connexion?suite=/compte/abonnement");
  const code = z.string().trim().min(4).max(40).safeParse(form.get("code"));
  if (!code.success) return { error: "Saisissez un code promo." };
  const supabase = await createClient();
  const { data, error } = await supabase.rpc("redeem_promo_code", { p_code: code.data });
  if (error) return { error: "Le code n'a pas pu être vérifié. Réessayez." };
  const r = (data ?? {}) as { ok?: boolean; reason?: string; until?: string | null; months?: number | null };
  if (!r.ok) return { error: reasons[r.reason ?? ""] ?? "Code refusé." };
  revalidatePath("/compte/abonnement");
  revalidatePath("/tableau-de-bord");
  if (!r.until) return { message: "Code accepté : vous bénéficiez d'un accès Premium illimité." };
  const until = new Date(r.until).toLocaleDateString("fr-FR", { dateStyle: "long", timeZone: "Europe/Paris" });
  return { message: `Code accepté : SMK Premium est actif jusqu'au ${until}.` };
}
