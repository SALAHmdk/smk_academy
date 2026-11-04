import Link from "next/link";

export function SiteFooter() {
  return (
    <footer className="mt-24 border-t border-line">
      <div className="mx-auto flex max-w-6xl flex-col gap-6 px-5 py-10 text-sm text-ink-2 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="font-semibold text-ink">SMK Academy by SMKTECH</p>
          <p>Learn. Practice. Succeed.</p>
        </div>
        <nav aria-label="Liens du pied de page" className="flex flex-wrap gap-x-6 gap-y-2">
          <Link href="/formations" className="hover:text-ink">
            Formations
          </Link>
          <Link href="/inscription" className="hover:text-ink">
            Créer un compte
          </Link>
          <Link href="/connexion" className="hover:text-ink">
            Connexion
          </Link>
        </nav>
        <p>© {new Date().getFullYear()} SMKTECH</p>
      </div>
    </footer>
  );
}
