import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { completeLesson } from "@/app/actions/learning";
import { ChevronIcon, StatusDot } from "@/components/icons";
import { Markdown } from "@/components/markdown";
import { getCourseOutline, getUserCourseState, lessonHref, quizHref } from "@/lib/queries";
import { createClient } from "@/lib/supabase/server";

type Props = { params: Promise<{ slug: string; module: string; lesson: string }> };

async function resolve(params: Props["params"]) {
  const { slug, module, lesson } = await params;
  const outline = await getCourseOutline(slug);
  if (!outline) return null;
  const mod = outline.modules.find((m) => String(m.position) === module && m.status === "published");
  const current = mod && outline.lessons.find((l) => l.module_id === mod.id && l.slug === lesson);
  if (!mod || !current) return null;
  return { slug, outline, mod, current };
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const r = await resolve(params);
  return r ? { title: `${r.current.title} — ${r.outline.course.title}`, robots: { index: false } } : {};
}

export default async function LessonPage({ params }: Props) {
  const r = await resolve(params);
  if (!r) notFound();
  const { slug, outline, mod, current } = r;

  const supabase = await createClient();
  const [{ data: lesson }, state] = await Promise.all([
    supabase.from("lessons").select("content_md").eq("id", current.id).single(),
    getUserCourseState(
      outline.course.id,
      outline.lessons.map((l) => l.id),
      outline.quizzes.map((q) => q.id),
    ),
  ]);
  if (!lesson) notFound();

  // Mémorise la position pour le bouton « Reprendre ma formation ».
  await supabase.rpc("touch_lesson", { p_lesson_id: current.id });

  const modPos = new Map(outline.modules.map((m) => [m.id, m.position]));
  const index = outline.lessons.findIndex((l) => l.id === current.id);
  const prev = outline.lessons[index - 1];
  const next = outline.lessons[index + 1];
  const moduleLessons = outline.lessons.filter((l) => l.module_id === mod.id);
  const isLastOfModule = moduleLessons.at(-1)?.id === current.id;
  const quiz = outline.quizzes.find((q) => q.module_id === mod.id);

  const nextHref =
    isLastOfModule && quiz
      ? quizHref(slug, mod.position)
      : next
        ? lessonHref(slug, modPos.get(next.module_id)!, next.slug)
        : `/formations/${slug}`;
  const nextLabel = isLastOfModule && quiz ? "Terminer et passer au quiz" : next ? "Terminer et continuer" : "Terminer la leçon";
  const alreadyDone = state.completedLessonIds.has(current.id);

  return (
    <div className="mx-auto grid max-w-6xl gap-10 px-5 pt-8 lg:grid-cols-[1fr_280px]">
      <article className="min-w-0">
        <nav aria-label="Fil d'Ariane" className="text-sm text-ink-2">
          <Link href={`/formations/${slug}`} className="hover:text-ink">
            {outline.course.title}
          </Link>
          <span className="mx-2 text-ink-3">/</span>
          <span>Module {mod.position}</span>
        </nav>

        <header className="mt-4 border-b border-line pb-7">
          <p className="text-sm font-semibold text-blue">
            Leçon {current.position} sur {moduleLessons.length}, {current.duration_minutes} min de lecture
          </p>
          <h1 className="t-1 mt-2">{current.title}</h1>
          <p className="mt-3 text-lg text-ink-2">{current.summary}</p>
        </header>

        <div className="mt-8">
          <Markdown source={lesson.content_md} />
        </div>

        <footer className="mt-14 flex flex-col-reverse gap-4 border-t border-line pt-8 sm:flex-row sm:items-center sm:justify-between">
          {prev ? (
            <Link href={lessonHref(slug, modPos.get(prev.module_id)!, prev.slug)} className="btn btn-plain justify-start px-0">
              <ChevronIcon direction="left" />
              <span className="truncate">{prev.title}</span>
            </Link>
          ) : (
            <span />
          )}
          <form action={completeLesson} className="sm:ml-auto">
            <input type="hidden" name="lessonId" value={current.id} />
            <input type="hidden" name="next" value={nextHref} />
            <button type="submit" className="btn btn-primary w-full sm:w-auto">
              {alreadyDone ? (isLastOfModule && quiz ? "Aller au quiz" : "Leçon suivante") : nextLabel}
              <ChevronIcon />
            </button>
          </form>
        </footer>
      </article>

      <aside aria-label="Sommaire du module" className="hidden lg:block">
        <div className="sticky top-24 surface p-5">
          <p className="text-sm font-semibold text-blue">Module {mod.position}</p>
          <p className="t-3 mt-1">{mod.title}</p>
          <ul className="mt-4 space-y-1">
            {moduleLessons.map((l) => (
              <li key={l.id}>
                <Link
                  href={lessonHref(slug, mod.position, l.slug)}
                  aria-current={l.id === current.id ? "page" : undefined}
                  className="flex items-center gap-3 rounded-[var(--radius-sm)] px-2 py-2 text-[0.95rem] hover:bg-surface-2 aria-[current=page]:bg-blue-soft aria-[current=page]:font-semibold"
                >
                  <StatusDot state={state.completedLessonIds.has(l.id) ? "done" : l.id === current.id ? "current" : "todo"} />
                  <span className="leading-snug">{l.title}</span>
                </Link>
              </li>
            ))}
            {quiz && (
              <li>
                <Link
                  href={quizHref(slug, mod.position)}
                  className="flex items-center gap-3 rounded-[var(--radius-sm)] px-2 py-2 text-[0.95rem] hover:bg-surface-2"
                >
                  <StatusDot
                    state={(state.bestScoreByQuiz.get(quiz.id) ?? -1) >= quiz.pass_mark ? "done" : "todo"}
                  />
                  <span className="leading-snug">Quiz du module</span>
                </Link>
              </li>
            )}
          </ul>
        </div>
      </aside>
    </div>
  );
}
