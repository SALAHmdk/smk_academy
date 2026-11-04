import type { Metadata } from "next";
import Link from "next/link";
import { formatDuration, LEVEL_LABEL, type Course } from "@/lib/learning";
import { getCatalog } from "@/lib/queries";

export const metadata: Metadata = {
  title: "Formations",
  description: "Le catalogue SMK Academy : formations disponibles et à venir en programmation, données et langues.",
};

function CourseRow({ course }: { course: Course }) {
  const available = course.status === "published";
  const body = (
    <>
      <div className="min-w-0 flex-1">
        <p className="text-sm text-ink-3">{course.category}</p>
        <h2 className="t-2 mt-1">{course.title}</h2>
        <p className="mt-2 text-ink-2">{course.subtitle}</p>
      </div>
      <dl className="flex shrink-0 gap-6 text-sm sm:w-64 sm:justify-end">
        <div>
          <dt className="text-ink-3">Niveau</dt>
          <dd className="mt-0.5 font-medium">{LEVEL_LABEL[course.level]}</dd>
        </div>
        <div>
          <dt className="text-ink-3">Durée</dt>
          <dd className="mt-0.5 font-medium">{formatDuration(course.duration_minutes)}</dd>
        </div>
      </dl>
      <div className="shrink-0 sm:w-36 sm:text-right">
        {available ? (
          <span className="btn btn-secondary">Commencer</span>
        ) : (
          <span className="inline-flex min-h-[44px] items-center text-sm font-medium text-ink-3">En préparation</span>
        )}
      </div>
    </>
  );

  const className = "flex flex-col gap-4 p-6 sm:flex-row sm:items-center sm:gap-8 sm:p-7";
  return (
    <li className="bg-surface">
      {available ? (
        <Link href={`/formations/${course.slug}`} className={`${className} transition-colors hover:bg-surface-2`}>
          {body}
        </Link>
      ) : (
        <div className={`${className} opacity-80`} aria-disabled="true">
          {body}
        </div>
      )}
    </li>
  );
}

export default async function CatalogPage() {
  const catalog = await getCatalog();
  const available = catalog.filter((c) => c.status === "published");
  const upcoming = catalog.filter((c) => c.status === "coming_soon");

  return (
    <div className="mx-auto max-w-5xl px-5 pt-12">
      <h1 className="t-1">Formations</h1>
      <p className="mt-3 max-w-[56ch] text-lg text-ink-2">
        Chaque formation indique son niveau, sa durée et ses prérequis. Seules les formations complètes sont ouvertes.
      </p>

      <section aria-labelledby="dispo" className="mt-10">
        <h2 id="dispo" className="t-3 mb-3 text-ink-2">
          Disponibles ({available.length})
        </h2>
        <ul className="grid gap-px overflow-hidden rounded-[var(--radius-lg)] bg-line">
          {available.map((c) => (
            <CourseRow key={c.id} course={c} />
          ))}
        </ul>
      </section>

      {upcoming.length > 0 && (
        <section aria-labelledby="bientot" className="mt-12">
          <h2 id="bientot" className="t-3 mb-3 text-ink-2">
            Bientôt disponibles ({upcoming.length})
          </h2>
          <ul className="grid gap-px overflow-hidden rounded-[var(--radius-lg)] bg-line">
            {upcoming.map((c) => (
              <CourseRow key={c.id} course={c} />
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
