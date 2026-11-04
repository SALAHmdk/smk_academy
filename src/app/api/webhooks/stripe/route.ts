import { createClient } from "@supabase/supabase-js";
import { env } from "@/lib/env";
import { stripeConfig, stripeRequest, verifyStripeSignature } from "@/lib/stripe";

export const dynamic = "force-dynamic";

type Obj = Record<string, unknown>;
type StripeSubscription = {
  id: string;
  customer: string;
  status: string;
  cancel_at_period_end: boolean;
  current_period_end?: number;
  metadata?: Record<string, string>;
  items?: { data?: { current_period_end?: number }[] };
};

function periodEnd(sub: StripeSubscription): number | null {
  return sub.current_period_end ?? sub.items?.data?.[0]?.current_period_end ?? null;
}

function subscriptionData(sub: StripeSubscription) {
  return {
    user_id: sub.metadata?.user_id ?? null,
    plan_id: sub.metadata?.plan_id ?? null,
    subscription_id: sub.id,
    customer_id: typeof sub.customer === "string" ? sub.customer : null,
    status: sub.status,
    current_period_end: periodEnd(sub),
    cancel_at_period_end: sub.cancel_at_period_end,
  };
}

/**
 * Webhook Stripe (mode test).
 * 1. signature Stripe vérifiée (HMAC-SHA256, tolérance 5 min) ;
 * 2. événements « livemode » refusés ;
 * 3. écriture via la RPC payments_apply_event, protégée par un jeton partagé et idempotente (identifiant d'événement).
 */
export async function POST(req: Request) {
  const cfg = stripeConfig();
  if (!cfg) return new Response("Paiements non configurés", { status: 503 });

  const payload = await req.text();
  if (payload.length > 512 * 1024) return new Response("Trop volumineux", { status: 413 });
  const valid = await verifyStripeSignature(payload, req.headers.get("stripe-signature"), cfg.webhookSecret);
  if (!valid) return new Response("Signature invalide", { status: 400 });

  const event = JSON.parse(payload) as { id: string; type: string; livemode: boolean; data: { object: Obj } };
  if (event.livemode) return new Response("Mode réel refusé", { status: 400 });

  const db = createClient(env.supabaseUrl, env.supabaseKey, { auth: { persistSession: false, autoRefreshToken: false } });
  const apply = async (type: "subscription" | "payment", data: Obj) => {
    const { data: result, error } = await db.rpc("payments_apply_event", {
      p_token: cfg.dbToken,
      p_provider: "stripe",
      p_event_id: `${event.id}:${type}`,
      p_type: type,
      p_data: data,
    });
    if (error) throw new Error(`${error.code} ${error.message}`);
    return result as string;
  };

  try {
    const o = event.data.object;
    switch (event.type) {
      case "checkout.session.completed": {
        if (o.mode === "subscription" && typeof o.subscription === "string") {
          const sub = await stripeRequest<StripeSubscription>(cfg.secretKey, "GET", `/subscriptions/${o.subscription}`);
          await apply("subscription", subscriptionData(sub));
        }
        break;
      }
      case "customer.subscription.created":
      case "customer.subscription.updated":
      case "customer.subscription.deleted":
        await apply("subscription", subscriptionData(o as unknown as StripeSubscription));
        break;
      case "invoice.paid":
      case "invoice.payment_failed": {
        const parent = (o.parent ?? {}) as { subscription_details?: { subscription?: string; metadata?: Record<string, string> } };
        const subId = (o.subscription as string | undefined) ?? parent.subscription_details?.subscription ?? null;
        let meta = parent.subscription_details?.metadata ?? (o.subscription_details as { metadata?: Record<string, string> } | undefined)?.metadata;
        if (!meta?.user_id && subId) {
          meta = (await stripeRequest<StripeSubscription>(cfg.secretKey, "GET", `/subscriptions/${subId}`)).metadata;
        }
        const paid = event.type === "invoice.paid";
        await apply("payment", {
          user_id: meta?.user_id ?? null,
          plan_id: meta?.plan_id ?? null,
          ref: o.id,
          subscription_id: subId,
          amount_cents: paid ? o.amount_paid : o.amount_due,
          currency: o.currency,
          status: paid ? "paid" : "failed",
        });
        break;
      }
      default:
        break;
    }
  } catch (e) {
    console.error("Webhook Stripe", event.type, e instanceof Error ? e.message : e);
    return new Response("Erreur de traitement", { status: 500 }); // Stripe réessaiera
  }
  return Response.json({ received: true });
}
