import Image from "next/image";
import Link from "next/link";
import { createClient, getCurrentUser } from "@/lib/supabase/server";
import { TabBar } from "@/components/tab-bar";

export async function SiteHeader() {
  const user = await getCurrentUser();
  const isAdmin = user ? (await (await createClient()).rpc("my_role")).data === "admin" : false;

  return (
    <>
      <div className="scroll-edge" aria-hidden="true" />
      <header className="sticky top-0 z-40 px-3 pt-3 sm:px-5">
        <nav
          aria-label="Navigation principale"
          className="glass mx-auto flex h-[52px] max-w-5xl items-center gap-1 rounded-full pl-2.5 pr-1.5"
        >
          <Link href="/" className="flex items-center gap-2 rounded-full pr-2" aria-label="SMK Academy, accueil">
            <Image src="/smktech-logo.png" alt="" width={32} height={32} priority className="h-8 w-auto" />
            <span className="whitespace-nowrap text-[15px] font-semibold tracking-tight">
              SMK <span className="font-normal text-ink-2">Academy</span>
            </span>
          </Link>

          <div className="ml-auto hidden items-center gap-1 text-[14px] sm:flex">
            <Link href="/formations" className="rounded-full px-3.5 py-2 text-ink/80 transition-colors hover:text-ink">
              Formations
            </Link>
            {user ? (
              <>
                <Link href="/tableau-de-bord" className="rounded-full px-3.5 py-2 text-ink/80 transition-colors hover:text-ink">
                  Ma progression
                </Link>
                <Link href="/compte" className="rounded-full px-3.5 py-2 text-ink/80 transition-colors hover:text-ink">
                  Compte
                </Link>
                {isAdmin && (
                  <Link href="/admin" className="rounded-full px-3.5 py-2 font-medium text-blue">
                    Administration
                  </Link>
                )}
              </>
            ) : (
              <>
                <Link href="/connexion" className="rounded-full px-3.5 py-2 text-ink/80 transition-colors hover:text-ink">
                  Connexion
                </Link>
                <Link href="/inscription" className="btn btn-primary min-h-[38px] px-4 py-1.5 text-[14px]">
                  Créer un compte
                </Link>
              </>
            )}
          </div>

          <div className="ml-auto sm:hidden">
            {user ? (
              <Link href="/tableau-de-bord" className="btn btn-secondary min-h-[38px] px-4 py-1.5 text-[14px]">
                Reprendre
              </Link>
            ) : (
              <Link href="/inscription" className="btn btn-primary min-h-[38px] px-4 py-1.5 text-[14px]">
                S&apos;inscrire
              </Link>
            )}
          </div>
        </nav>
      </header>
      <TabBar loggedIn={Boolean(user)} />
    </>
  );
}
