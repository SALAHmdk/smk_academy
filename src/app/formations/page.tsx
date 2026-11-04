import type { Metadata } from "next";
import Link from "next/link";
import { CourseCover } from "@/components/course-cover";
import { filterCatalog, formatDuration, LEVEL_LABEL, LEVELS, type Course, type Level } from "@/lib/learning";
import { getCatalog, getCategories } from "@/lib/queries";

export const metadata: Metadata = {
  title: "Formations",
  description:
    "Le catalogue SMK Academy : programmation, développement web, données, IA, cloud, cybersécurité, BI, mobile et langues.",
};

type Props = { searchParams: Promise<Record<string, string | undefined>> };

function CourseCard({ course }: { course: Course }) {
  const available = course.status === "published";
  const card = (
    <>
      <div className="aspect-[16/9] overflow-hidden rounded-[var(--radius-lg)]">
        <CourseCover label={course.cover_label} category={course.categories?.slug} muted={!available} />
      </div>
      <div className="px-1 pb-1 pt-4">
        <div className="flex items-center justify-between gap-3 text-[13px]">
          <span className="truncate text-ink-2">{course.categories?.name}</span>
          {available ? (
            <span className="shrink-0 rounded-full bg-green-soft px-2.5 py-0.5 font-semibold text-green">Disponible</span>
          ) : (
            <span className="shrink-0 rounded-full bg-surface-2 px-2.5 py-0.5 font-medium text-ink-2">Bientôt disponible</span>
          )}
        </div>
        <h3 className="t-3 mt-2">{course.title}</h3>
        <p className="mt-1 line-clamp-2 text-[15px] text-ink-2">{course.subtitle}</p>
        <p className="mt-3 text-[13px] text-ink-3">
          {LEVEL_LABEL[course.level]}, environ {formatDuration(course.duration_minutes)}
        </p>
      </div>
    </>
  );
  return (
    <li>
      <Link
        href={`/formations/${course.slug}`}
        className={`group block rounded-[var(--radius-xl)] bg-surface p-3 transition-transform duration-300 hover:-translate-y-0.5 ${
          available ? "" : "opacity-[0.92]"
        }`}
        aria-label={`${course.title}${available ? "" : " (bientôt disponible)"}`}
      >
        {card}
      </Link>
    </li>
  );
}

export default async function CatalogPage({ searchParams }: Props) {
  const params = await searchParams;
  const [catalog, categories] = await Promise.all([getCatalog(), getCategories()]);

  const filters = {
    q: params.q?.slice(0, 80),
    categorie: categories.some((c) => c.slug === params.categorie) ? params.categorie : undefined,
    langage: params.langage?.slice(0, 40),
    niveau: LEVELS.includes(params.niveau as Level) ? params.niveau : undefined,
    dispo: params.dispo === "1" ? "1" : undefined,
  };
  const results = filterCatalog(catalog, filters);
  const available = results.filter((c) => c.status === "published");
  const upcoming = results.filter((c) => c.status === "coming_soon");
  const topics = [...new Set(catalog.filter((c) => !filters.categorie || c.categories?.slug === filters.categorie).map((c) => c.topic))]
    .filter(Boolean)
    .sort((a, b) => a.localeCompare(b, "fr"));
  const activeFilters = Object.values(filters).some(Boolean);
  const totalAvailable = catalog.filter((c) => c.status === "published").length;

  const chipHref = (slug?: string) => {
    const sp = new URLSearchParams();
    if (filters.q) sp.set("q", filters.q);
    if (slug) sp.set("categorie", slug);
    if (filters.niveau) sp.set("niveau", filters.niveau);
    if (filters.dispo) sp.set("dispo", "1");
    const s = sp.toString();
    return `/formations${s ? `?${s}` : ""}`;
  };

  return (
    <div className="mx-auto max-w-6xl px-5 pt-12">
      <header className="max-w-3xl">
        <h1 className="t-1">Formations</h1>
        <p className="mt-3 text-lg text-ink-2">
          {catalog.length} formations dans {categories.length} domaines. {totalAvailable} disponible
          {totalAvailable > 1 ? "s" : ""} dès aujourd&apos;hui, les autres sont en cours de rédaction et s&apos;ouvriront
          au fur et à mesure.
        </p>
      </header>

      <form role="search" action="/formations" className="mt-8 grid gap-3">
        <div className="relative">
          <label htmlFor="q" className="sr-only">
            Rechercher une formation
          </label>
          <svg
            aria-hidden="true"
            viewBox="0 0 24 24"
            className="pointer-events-none absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-ink-3"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          >
            <circle cx="11" cy="11" r="7" />
            <path d="m20 20-3.5-3.5" />
          </svg>
          <input
            id="q"
            name="q"
            type="search"
            defaultValue={filters.q}
            placeholder="Python, React, Machine Learning, anglais…"
            className="input !min-h-[52px] !rounded-full pl-12 text-[17px]"
            maxLength={80}
          />
        </div>
        <div className="flex flex-wrap items-end gap-3">
          {filters.categorie && <input type="hidden" name="categorie" value={filters.categorie} />}
          <div className="field min-w-[150px] flex-1 sm:flex-none">
            <label htmlFor="langage">Langage ou outil</label>
            <select id="langage" name="langage" defaultValue={filters.langage ?? ""} className="input">
              <option value="">Tous</option>
              {topics.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
          </div>
          <div className="field min-w-[150px] flex-1 sm:flex-none">
            <label htmlFor="niveau">Niveau</label>
            <select id="niveau" name="niveau" defaultValue={filters.niveau ?? ""} className="input">
              <option value="">Tous</option>
              {LEVELS.map((l) => (
                <option key={l} value={l}>
                  {LEVEL_LABEL[l]}
                </option>
              ))}
            </select>
          </div>
          <label className="flex min-h-[48px] items-center gap-2.5 px-1 text-[15px]">
            <input type="checkbox" name="dispo" value="1" defaultChecked={filters.dispo === "1"} className="h-5 w-5 accent-[var(--smk-blue)]" />
            Disponibles uniquement
          </label>
          <div className="ml-auto flex gap-2">
            {activeFilters && (
              <Link href="/formations" className="btn btn-plain">
                Réinitialiser
              </Link>
            )}
            <button type="submit" className="btn btn-primary">
              Rechercher
            </button>
          </div>
        </div>
      </form>

      <nav aria-label="Catégories" className="-mx-5 mt-6 overflow-x-auto px-5 pb-1">
        <ul className="flex w-max gap-2">
          <li>
            <Link
              href={chipHref()}
              aria-current={!filters.categorie ? "page" : undefined}
              className="inline-flex min-h-[40px] items-center rounded-full bg-surface px-4 text-[14px] font-medium text-ink-2 aria-[current=page]:bg-ink aria-[current=page]:text-canvas"
            >
              Tout
            </Link>
          </li>
          {categories.map((c) => (
            <li key={c.id}>
              <Link
                href={chipHref(c.slug)}
                aria-current={filters.categorie === c.slug ? "page" : undefined}
                className="inline-flex min-h-[40px] items-center whitespace-nowrap rounded-full bg-surface px-4 text-[14px] font-medium text-ink-2 aria-[current=page]:bg-ink aria-[current=page]:text-canvas"
              >
                {c.name}
              </Link>
            </li>
          ))}
        </ul>
      </nav>

      {filters.categorie && (
        <p className="mt-4 max-w-2xl text-ink-2">{categories.find((c) => c.slug === filters.categorie)?.description}</p>
      )}

      <p className="mt-8 text-sm text-ink-2" aria-live="polite">
        {results.length === 0
          ? "Aucune formation ne correspond à votre recherche."
          : `${results.length} formation${results.length > 1 ? "s" : ""}`}
      </p>

      {results.length === 0 && (
        <div className="surface mt-4 p-8">
          <p className="t-3">Essayez un autre mot-clé ou retirez un filtre.</p>
          <Link href="/formations" className="btn btn-secondary mt-5">
            Voir tout le catalogue
          </Link>
        </div>
      )}

      {available.length > 0 && (
        <section aria-labelledby="dispo" className="mt-4">
          <h2 id="dispo" className="t-2">
            Disponibles
          </h2>
          <ul className="mt-5 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {available.map((c) => (
              <CourseCard key={c.id} course={c} />
            ))}
          </ul>
        </section>
      )}

      {upcoming.length > 0 && (
        <section aria-labelledby="bientot" className="mt-14">
          <h2 id="bientot" className="t-2">
            Bientôt disponibles
          </h2>
          <p className="mt-2 text-ink-2">
            Ces formations sont annoncées : leur programme est défini, leur contenu est en cours de rédaction.
          </p>
          <ul className="mt-5 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {upcoming.map((c) => (
              <CourseCard key={c.id} course={c} />
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
