"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV = [
  ["/admin", "Formations"],
  ["/admin/offres", "Offres et prix"],
  ["/admin/codes-promo", "Codes promo"],
  ["/admin/acces", "Accès offerts"],
  ["/admin/paiements", "Paiements"],
] as const;

const PREMIUM = ["/admin/offres", "/admin/codes-promo", "/admin/acces", "/admin/paiements"];

export function AdminNav() {
  const pathname = usePathname();
  const isCurrent = (href: string) =>
    href === "/admin" ? !PREMIUM.some((p) => pathname.startsWith(p)) : pathname.startsWith(href);
  return (
    <nav aria-label="Sections de l'administration" className="-mx-5 mb-8 overflow-x-auto px-5">
      <ul className="flex w-max gap-1 rounded-full bg-surface p-1 shadow-[0_0_0_1px_var(--line)]">
        {NAV.map(([href, label]) => {
          const current = isCurrent(href);
          return (
            <li key={href}>
              <Link
                href={href}
                aria-current={current ? "page" : undefined}
                className={`block rounded-full px-4 py-2 text-[14px] font-medium transition-colors ${
                  current ? "bg-blue text-white" : "text-ink-2 hover:bg-surface-2 hover:text-ink"
                }`}
              >
                {label}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
