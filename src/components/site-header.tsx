import Image from "next/image";
import Link from "next/link";
import { signOut } from "@/app/actions/auth";
import { getCurrentUser } from "@/lib/supabase/server";

export async function SiteHeader() {
  const user = await getCurrentUser();

  return (
    <header className="sticky top-0 z-40 px-3 pt-3 sm:px-5">
      <nav
        aria-label="Navigation principale"
        className="glass mx-auto flex h-14 max-w-6xl items-center gap-2 rounded-full pl-3 pr-2"
      >
        <Link href="/" className="flex items-center gap-2.5 rounded-full pr-2" aria-label="SMK Academy, accueil">
          <Image src="/smktech-logo.png" alt="" width={34} height={34} priority className="h-[34px] w-auto" />
          <span className="whitespace-nowrap text-[1.02rem] font-bold tracking-tight">
            SMK<span className="hidden font-medium text-ink-2 min-[430px]:inline"> Academy</span>
          </span>
        </Link>

        <div className="ml-auto flex items-center gap-1">
          <Link href="/formations" className="btn btn-plain hidden text-ink sm:inline-flex">
            Formations
          </Link>
          {user ? (
            <>
              <Link href="/tableau-de-bord" className="btn btn-plain text-ink">
                <span className="hidden sm:inline">Tableau de bord</span>
                <span className="sm:hidden">Mon espace</span>
              </Link>
              <form action={signOut}>
                <button type="submit" className="btn btn-secondary px-4">
                  Déconnexion
                </button>
              </form>
            </>
          ) : (
            <>
              <Link href="/connexion" className="btn btn-plain text-ink">
                Connexion
              </Link>
              <Link href="/inscription" className="btn btn-primary px-4">
                <span className="hidden sm:inline">Créer un compte</span>
                <span className="sm:hidden">S&apos;inscrire</span>
              </Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}
