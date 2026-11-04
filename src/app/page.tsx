import Link from "next/link";
import { formatDuration, LEVEL_LABEL } from "@/lib/learning";
import { getCatalog } from "@/lib/queries";
import { getCurrentUser } from "@/lib/supabase/server";

const steps = [
  {
    title: "Learn",
    text: "Des leçons courtes et progressives, écrites pour être lues aussi bien sur ordinateur que sur téléphone.",
  },
  {
    title: "Practice",
    text: "Chaque leçon se termine par des exercices concrets. La correction reste cachée jusqu'à ce que vous la demandiez.",
  },
  {
    title: "Succeed",
    text: "Un quiz noté sur 20 valide chaque module. Votre progression et vos notes vous suivent sur tous vos appareils.",
  },
];

export default async function HomePage() {
  const [user, catalog] = await Promise.all([getCurrentUser(), getCatalog()]);
  const featured = catalog.find((c) => c.status === "published");

  return (
    <>
      <section className="mx-auto grid max-w-6xl items-center gap-12 px-5 pb-16 pt-14 sm:pt-20 lg:grid-cols-[1.1fr_1fr] lg:gap-16">
        <div>
          <p className="mb-5 text-lg font-medium text-ink-2">SMK Academy, par SMKTECH</p>
          <h1 className="t-hero">
            Learn.
            <br />
            Practice.
            <br />
            Succeed.
          </h1>
          <p className="mt-6 max-w-[34ch] text-xl leading-relaxed text-ink-2">
            Apprenez à programmer avec des cours clairs, des exercices corrigés et des quiz notés sur 20.
          </p>
          <div className="mt-9 flex flex-wrap items-center gap-3">
            {user ? (
              <Link href="/tableau-de-bord" className="btn btn-primary">
                Reprendre mes cours
              </Link>
            ) : (
              <Link href="/inscription" className="btn btn-primary">
                Créer mon compte gratuit
              </Link>
            )}
            <Link href="/formations" className="btn btn-plain">
              Voir les formations
            </Link>
          </div>
        </div>

        {/* Élément signature : un vrai programme Python, et la note qu'il affiche. */}
        <figure aria-label="Exemple de code Python tiré de la formation" className="relative min-w-0">
          <div className="code-block shadow-[0_30px_80px_-30px_rgba(11,75,214,0.55)]" data-lang="python">
            <div className="flex items-center gap-2 border-b border-white/10 px-5 py-3 text-xs text-white/50">
              <span className="h-2.5 w-2.5 rounded-full bg-white/20" />
              <span className="h-2.5 w-2.5 rounded-full bg-white/20" />
              <span className="h-2.5 w-2.5 rounded-full bg-white/20" />
              <span className="ml-2">module_1.py</span>
            </div>
            <pre className="text-[0.95rem] sm:text-base">
              <code>
                <span className="hljs-comment"># Votre premier quiz, corrigé</span>
                {"\n"}
                {"bonnes_reponses = "}
                <span className="hljs-number">9</span>
                {"\n"}
                {"questions = "}
                <span className="hljs-number">10</span>
                {"\n\n"}
                {"note = bonnes_reponses / questions * "}
                <span className="hljs-number">20</span>
                {"\n"}
                <span className="hljs-built_in">print</span>
                {"("}
                <span className="hljs-string">{'f"Note : {note:.0f}/20"'}</span>
                {")"}
              </code>
            </pre>
            <div className="border-t border-white/10 px-5 py-4 font-mono">
              <span className="text-white/45">&gt;&gt;&gt; </span>
              <span className="text-[1.35rem] font-semibold text-[#4fe0b5]">Note : 18/20</span>
            </div>
          </div>
        </figure>
      </section>

      <section aria-labelledby="methode" className="mx-auto max-w-6xl px-5 py-10">
        <h2 id="methode" className="sr-only">
          La méthode SMK Academy
        </h2>
        <ol className="grid gap-px overflow-hidden rounded-[var(--radius-lg)] bg-line sm:grid-cols-3">
          {steps.map((s, i) => (
            <li key={s.title} className="bg-surface p-7">
              <span className="text-sm font-semibold text-blue">Étape {i + 1}</span>
              <h3 className="t-2 mt-2">{s.title}</h3>
              <p className="mt-3 text-ink-2">{s.text}</p>
            </li>
          ))}
        </ol>
      </section>

      {featured && (
        <section aria-labelledby="formation-phare" className="mx-auto max-w-6xl px-5 py-14">
          <div className="surface grid gap-8 p-7 sm:p-10 md:grid-cols-[1.4fr_1fr] md:items-end">
            <div>
              <p className="text-ink-2">Disponible gratuitement</p>
              <h2 id="formation-phare" className="t-1 mt-2">
                {featured.title}
              </h2>
              <p className="mt-4 max-w-[52ch] text-lg text-ink-2">{featured.description}</p>
            </div>
            <div className="flex flex-col gap-5 md:items-end">
              <dl className="flex gap-8 text-sm">
                <div>
                  <dt className="text-ink-3">Niveau</dt>
                  <dd className="mt-1 font-semibold">{LEVEL_LABEL[featured.level]}</dd>
                </div>
                <div>
                  <dt className="text-ink-3">Durée estimée</dt>
                  <dd className="mt-1 font-semibold">{formatDuration(featured.duration_minutes)}</dd>
                </div>
              </dl>
              <Link href={`/formations/${featured.slug}`} className="btn btn-primary">
                Découvrir la formation
              </Link>
            </div>
          </div>
        </section>
      )}
    </>
  );
}
