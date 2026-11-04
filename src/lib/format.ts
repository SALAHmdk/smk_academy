/** Formats d'affichage partagés (heure de Paris, euros). */
export function formatDate(value: string | null | undefined, withTime = false): string {
  if (!value) return "—";
  return new Date(value).toLocaleString("fr-FR", {
    dateStyle: withTime ? "short" : "long",
    ...(withTime ? { timeStyle: "short" as const } : {}),
    timeZone: "Europe/Paris",
  });
}

export function formatPrice(cents: number): string {
  const euros = cents / 100;
  return `${euros.toLocaleString("fr-FR", { minimumFractionDigits: Number.isInteger(euros) ? 0 : 2, maximumFractionDigits: 2 })} €`;
}

/** « 1 € / mois », « 10 € / an », « 0 € » */
export function formatPlanPrice(cents: number, interval: string | null): string {
  const price = formatPrice(cents);
  if (interval === "month") return `${price} / mois`;
  if (interval === "year") return `${price} / an`;
  return price;
}

export function formatMonths(months: number | null): string {
  if (months === null) return "Illimité";
  if (months % 12 === 0) return months === 12 ? "1 an" : `${months / 12} ans`;
  return `${months} mois`;
}

export type Access = {
  premium: boolean;
  unlimited?: boolean;
  until?: string | null;
  subscription?: {
    plan_id: string | null;
    status: string;
    current_period_end: string | null;
    cancel_at_period_end: boolean;
    provider: string;
  } | null;
};
