import { STATUS_LABEL } from "@/lib/admin";

export function StatusBadge({ status }: { status: string }) {
  const tone =
    status === "published" ? "bg-green-soft text-green" : status === "coming_soon" ? "bg-blue-soft text-blue" : "bg-surface-2 text-ink-2";
  return <span className={`inline-flex shrink-0 rounded-full px-2.5 py-0.5 text-[13px] font-semibold ${tone}`}>{STATUS_LABEL[status] ?? status}</span>;
}
