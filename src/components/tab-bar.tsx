"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BooksIcon, ChartIcon, HomeIcon, PersonIcon } from "@/components/icons";

/** Barre d'onglets flottante (Liquid Glass), affichée sur téléphone uniquement. */
export function TabBar({ loggedIn }: { loggedIn: boolean }) {
  const pathname = usePathname();
  const tabs = loggedIn
    ? [
        { href: "/", label: "Accueil", Icon: HomeIcon, match: (p: string) => p === "/" },
        { href: "/formations", label: "Formations", Icon: BooksIcon, match: (p: string) => p.startsWith("/formations") },
        { href: "/tableau-de-bord", label: "Progression", Icon: ChartIcon, match: (p: string) => p.startsWith("/tableau-de-bord") || p.startsWith("/resultats") },
        { href: "/compte", label: "Compte", Icon: PersonIcon, match: (p: string) => p.startsWith("/compte") },
      ]
    : [
        { href: "/", label: "Accueil", Icon: HomeIcon, match: (p: string) => p === "/" },
        { href: "/formations", label: "Formations", Icon: BooksIcon, match: (p: string) => p.startsWith("/formations") },
        { href: "/connexion", label: "Connexion", Icon: PersonIcon, match: (p: string) => p === "/connexion" || p === "/inscription" },
      ];

  return (
    <nav aria-label="Navigation principale (mobile)" className="tabbar glass sm:hidden">
      {tabs.map(({ href, label, Icon, match }) => (
        <Link key={href} href={href} aria-current={match(pathname) ? "page" : undefined}>
          <Icon />
          <span>{label}</span>
        </Link>
      ))}
    </nav>
  );
}
