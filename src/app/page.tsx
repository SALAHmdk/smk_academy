import Image from "next/image";
import Link from "next/link";
import { CheckIcon, ChevronIcon, CrossIcon } from "@/components/icons";
import { formatDuration, LEVEL_LABEL } from "@/lib/learning";
import { getCatalog } from "@/lib/queries";
import { getCurrentUser } from "@/lib/supabase/server";

/** Écran de leçon miniature, présenté dans un cadre de téléphone (visuel du héros). */
function LessonScreen() {
  return (
    <div className="device-screen text-left">
      <div className="device-island" />
      <div className="flex h-full flex-col px-5 pb-5 pt-14 text-[12px]">
        <p className="font-semibold text-blue">Module 1, leçon 2</p>
        <p className="mt-1 text-[19px] font-bold leading-tight tracking-tight">Variables et types de base</p>
        <div className="progress mt-3" aria-hidden="true">
          <span style={{ width: "66%" }} />
        </div>
        <p className="mt-4 leading-relaxed text-ink-2">
          Une <strong className="text-ink">variable</strong> est un nom qui désigne une valeur stockée en mémoire.
        </p>
        <div className="code-block mt-3 text-[11px]" data-lang="python">
          <pre className="!px-3.5 !py-3">
            <code>
              {"age = "}
              <span className="hljs-number">25</span>
              {"\nprenom = "}
              <span className="hljs-string">&quot;Amina&quot;</span>
              {"\n"}
              <span className="hljs-built_in">print</span>
              {"(prenom, age)"}
            </code>
          </pre>
        </div>
        <div className="solution mt-3">
          <p className="flex min-h-[38px] items-center px-3.5 text-[12px] font-semibold text-blue">Voir la correction</p>
        </div>
        <p className="mt-5 text-[14px] font-bold tracking-tight">À retenir</p>
        <ul className="mt-2 space-y-1.5 leading-snug text-ink-2">
          <li className="flex gap-2">
            <span className="mt-[0.45em] h-1 w-1 shrink-0 rounded-full bg-blue" />
            <span>
              <code className="font-mono text-ink">nom = valeur</code> range une valeur.
            </span>
          </li>
          <li className="flex gap-2">
            <span className="mt-[0.45em] h-1 w-1 shrink-0 rounded-full bg-blue" />
            <span>Quatre types : int, float, str, bool.</span>
          </li>
        </ul>
        <div className="mt-auto">
          <span className="btn btn-primary w-full min-h-[40px] text-[13px]">Terminer et continuer</span>
        </div>
      </div>
    </div>
  );
}

/** Résultat de quiz miniature (section sombre). */
function ResultCard() {
  const rows: [string, boolean][] = [
    ['print("2" + "3") affiche 23', true],
    ["17 // 5 vaut 3", true],
    ["8 / 2 renvoie l'entier 4", false],
    ["input() renvoie toujours un str", true],
  ];
  return (
    <div className="mx-auto w-full max-w-[440px] rounded-[var(--radius-xl)] bg-surface p-7 text-left sm:p-9">
      <p className="text-sm font-semibold text-green">Module validé</p>
      <p className="mt-1 flex items-baseline gap-1.5">
        <span className="text-[88px] font-bold leading-none tracking-[-0.045em]">18</span>
        <span className="text-2xl font-semibold text-ink-2">/20</span>
      </p>
      <ul className="mt-6 space-y-2.5 text-[15px]">
        {rows.map(([label, ok]) => (
          <li key={label} className="flex items-center gap-3">
            <span
              className={`grid h-6 w-6 shrink-0 place-items-center rounded-full ${ok ? "bg-green-soft text-green" : "bg-red-soft text-red"}`}
            >
              {ok ? <CheckIcon className="h-3.5 w-3.5" /> : <CrossIcon className="h-3.5 w-3.5" />}
            </span>
            <span className="text-ink-2">{label}</span>
          </li>
        ))}
      </ul>
      <p className="mt-6 border-l-[3px] border-blue pl-4 text-[14px] leading-relaxed text-ink-2">
        <span className="font-semibold text-ink">Explication. </span>L&apos;opérateur / renvoie toujours un float : 8 / 2 vaut
        4.0.
      </p>
    </div>
  );
}

export default async function HomePage() {
  const [user, catalog] = await Promise.all([getCurrentUser(), getCatalog()]);
  const featured = catalog.find((c) => c.status === "published");
  const upcoming = catalog.filter((c) => c.status === "coming_soon");

  return (
    <>
      {/* Héros : une seule idée, un seul visuel */}
      <section className="overflow-hidden px-5 pt-14 text-center sm:pt-20">
        <div className="mx-auto max-w-[860px]">
          <Image src="/smktech-logo.png" alt="" width={64} height={64} priority className="rise mx-auto h-16 w-auto" />
          <p className="eyebrow rise mt-5" style={{ "--i": 1 } as React.CSSProperties}>
            SMK Academy
          </p>
          <h1 className="t-hero rise mt-2" style={{ "--i": 2 } as React.CSSProperties}>
            Learn. Practice. Succeed.
          </h1>
          <p className="subhead rise mx-auto mt-6 max-w-[34em]" style={{ "--i": 3 } as React.CSSProperties}>
            Des cours de programmation clairs, des exercices corrigés et des quiz notés sur 20. Sur ordinateur comme sur
            téléphone.
          </p>
          <div className="rise mt-8 flex flex-wrap items-center justify-center gap-x-6 gap-y-3" style={{ "--i": 4 } as React.CSSProperties}>
            <Link href={user ? "/tableau-de-bord" : "/inscription"} className="btn btn-primary">
              {user ? "Reprendre mes cours" : "Commencer gratuitement"}
            </Link>
            <Link href="/formations" className="link-more">
              Voir les formations
              <ChevronIcon className="h-4 w-4" />
            </Link>
          </div>
        </div>

        <div className="rise relative z-10 mx-auto mt-16 flex justify-center sm:mt-20" style={{ "--i": 5 } as React.CSSProperties}>
          <div className="device" role="img" aria-label="Aperçu d'une leçon SMK Academy sur téléphone">
            <LessonScreen />
          </div>
        </div>
      </section>

      {/* Section sombre : la note sur 20 */}
      <section className="section section-dark mt-[-120px] px-5 pt-[calc(clamp(72px,11vw,140px)+120px)] text-center">
        <div className="mx-auto max-w-[980px]">
          <p className="eyebrow">Quiz notés</p>
          <h2 className="t-display mt-2">
            <span className="text-gradient">Une note sur 20.</span>
            <br />
            Calculée, jamais devinée.
          </h2>
          <p className="subhead mx-auto mt-6 max-w-[36em]">
            Chaque module se valide par un quiz. La correction est faite sur nos serveurs, puis chaque erreur est
            expliquée. Repassez-le autant de fois que nécessaire : votre meilleure note est conservée.
          </p>
          <div className="mt-14">
            <ResultCard />
          </div>
        </div>
      </section>

      {/* Bento : la méthode */}
      <section className="section px-5">
        <div className="mx-auto max-w-[1024px]">
          <div className="mx-auto max-w-[800px] text-center">
            <p className="eyebrow">La méthode</p>
            <h2 className="t-display mt-2">Comprendre, s&apos;exercer, réussir.</h2>
          </div>

          <div className="bento mt-14">
            <div className="md:col-span-4">
              <p className="t-3">Des leçons qui se lisent partout</p>
              <p className="mt-2 max-w-[36ch] text-ink-2">
                Courtes, progressives, avec de vrais exemples de code commentés et un rappel « À retenir » à la fin.
              </p>
              <div className="code-block mt-6 text-[13px]" data-lang="python">
                <pre>
                  <code>
                    <span className="hljs-keyword">for</span>
                    {" lettre "}
                    <span className="hljs-keyword">in</span> <span className="hljs-string">&quot;SMK&quot;</span>
                    {":\n    "}
                    <span className="hljs-built_in">print</span>
                    {"(lettre)"}
                  </code>
                </pre>
              </div>
            </div>
            <div className="flex flex-col justify-between md:col-span-2">
              <p className="t-3">Gratuit</p>
              <p className="mt-6 text-[64px] font-bold leading-none tracking-[-0.04em]">0 €</p>
              <p className="mt-3 text-ink-2">Compte, cours fondamentaux, quiz et progression.</p>
            </div>
            <div className="md:col-span-2">
              <p className="t-3">Exercices corrigés</p>
              <p className="mt-2 text-ink-2">La correction reste repliée jusqu&apos;à ce que vous la demandiez.</p>
              <div className="solution mt-6">
                <p className="flex min-h-[44px] items-center px-4 font-semibold text-blue">Voir la correction</p>
              </div>
            </div>
            <div className="md:col-span-2">
              <p className="t-3">Progression synchronisée</p>
              <p className="mt-2 text-ink-2">Reprenez exactement où vous en étiez, sur n&apos;importe quel appareil.</p>
              <div className="mt-6">
                <div className="mb-1.5 flex justify-between text-sm">
                  <span className="text-ink-2">Python pour débutants</span>
                  <span className="font-semibold">4/6</span>
                </div>
                <div className="progress" aria-hidden="true">
                  <span style={{ width: "66%" }} />
                </div>
              </div>
            </div>
            <div className="md:col-span-2">
              <p className="t-3">Clair ou sombre</p>
              <p className="mt-2 text-ink-2">L&apos;interface suit votre système, ou le thème de votre choix.</p>
              <div className="mt-6 flex gap-3" aria-hidden="true">
                <span className="h-14 flex-1 rounded-[var(--radius-md)] border border-line bg-[#f5f5f7]" />
                <span className="h-14 flex-1 rounded-[var(--radius-md)] bg-black" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Formation phare */}
      {featured && (
        <section className="px-5 pb-6">
          <div className="mx-auto max-w-[1024px] rounded-[var(--radius-xl)] bg-surface px-6 py-14 text-center sm:px-12 sm:py-20">
            <p className="eyebrow">Disponible gratuitement</p>
            <h2 className="t-display mt-2">{featured.title}</h2>
            <p className="subhead mx-auto mt-5 max-w-[34em]">{featured.subtitle}</p>
            <p className="mt-4 text-[15px] text-ink-2">
              Niveau {LEVEL_LABEL[featured.level].toLowerCase()}, environ {formatDuration(featured.duration_minutes)} de
              formation.
            </p>
            <div className="mt-8 flex flex-wrap items-center justify-center gap-x-6 gap-y-3">
              <Link href={`/formations/${featured.slug}`} className="btn btn-primary">
                Découvrir la formation
              </Link>
              {upcoming.length > 0 && (
                <Link href="/formations" className="link-more">
                  Bientôt : {upcoming.map((c) => c.title.split(" —")[0]).join(", ")}
                  <ChevronIcon className="h-4 w-4" />
                </Link>
              )}
            </div>
          </div>
        </section>
      )}
    </>
  );
}
