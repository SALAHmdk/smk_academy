import { setTheme } from "@/app/actions/preferences";
import type { Theme } from "@/lib/theme";

const OPTIONS: { value: Theme; label: string }[] = [
  { value: "auto", label: "Automatique" },
  { value: "light", label: "Clair" },
  { value: "dark", label: "Sombre" },
];

/** Commande segmentée (3 segments égaux), fonctionne sans JavaScript. */
export function ThemeSwitch({ current }: { current: Theme }) {
  return (
    <form action={setTheme} role="radiogroup" aria-label="Apparence" className="inline-grid grid-cols-3 rounded-[11px] bg-surface-2 p-[3px]">
      {OPTIONS.map((o) => (
        <button
          key={o.value}
          type="submit"
          name="theme"
          value={o.value}
          role="radio"
          aria-checked={current === o.value}
          className="min-h-[36px] rounded-[9px] px-3.5 text-[14px] font-medium text-ink-2 transition-colors aria-checked:bg-elevated aria-checked:text-ink aria-checked:shadow-[0_1px_4px_rgba(0,0,0,0.12)]"
        >
          {o.label}
        </button>
      ))}
    </form>
  );
}
