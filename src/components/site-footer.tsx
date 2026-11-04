import Link from "next/link";

export function SiteFooter() {
  return (
    <footer className="mt-24 bg-canvas">
      <div className="mx-auto max-w-5xl px-5 pb-32 pt-8 text-[12px] leading-relaxed text-ink-2 sm:pb-10">
        <p className="border-b border-line pb-4">
          Les attestations SMK Academy sont des attestations internes de réussite. Elles ne constituent pas des diplômes
          reconnus par l&apos;État.
        </p>
        <div className="flex flex-col gap-3 pt-4 sm:flex-row sm:items-center sm:justify-between">
          <p>Copyright © {new Date().getFullYear()} SMKTECH. Tous droits réservés.</p>
          <nav aria-label="Liens du pied de page" className="flex flex-wrap gap-x-5 gap-y-1">
            <Link href="/formations" className="hover:text-ink hover:underline">
              Formations
            </Link>
            <Link href="/tarifs" className="hover:text-ink hover:underline">
              Tarifs
            </Link>
            <Link href="/inscription" className="hover:text-ink hover:underline">
              Créer un compte
            </Link>
            <Link href="/connexion" className="hover:text-ink hover:underline">
              Connexion
            </Link>
          </nav>
        </div>
      </div>
    </footer>
  );
}
