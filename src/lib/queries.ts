import "server-only";
import { cache } from "react";
import type { Course, LessonSummary, Module } from "@/lib/learning";
import { orderLessons } from "@/lib/learning";
import { createClient } from "@/lib/supabase/server";

const COURSE_COLUMNS =
  "id, slug, title, subtitle, description, category, level, duration_minutes, objectives, prerequisites, status, is_premium, position";

export async function getCatalog(): Promise<Course[]> {
  const supabase = await createClient();
  const { data, error } = await supabase.from("courses").select(COURSE_COLUMNS).order("position");
  if (error) throw new Error("Catalogue indisponible");
  return (data ?? []) as Course[];
}

export type QuizSummary = { id: string; module_id: string; title: string; pass_mark: number };

export type CourseOutline = {
  course: Course;
  modules: Module[];
  /** Vide pour un visiteur non connecté (RLS). */
  lessons: LessonSummary[];
  quizzes: QuizSummary[];
};

/** Formation + plan (modules, leçons, quiz). Mis en cache pour la durée de la requête. */
export const getCourseOutline = cache(async (slug: string): Promise<CourseOutline | null> => {
  const supabase = await createClient();
  const { data: course } = await supabase.from("courses").select(COURSE_COLUMNS).eq("slug", slug).maybeSingle();
  if (!course) return null;

  const { data: modules } = await supabase
    .from("modules")
    .select("id, course_id, title, description, position, status")
    .eq("course_id", course.id)
    .order("position");
  const moduleIds = (modules ?? []).map((m) => m.id);

  const [lessonsRes, quizzesRes] = moduleIds.length
    ? await Promise.all([
        supabase
          .from("lessons")
          .select("id, module_id, slug, title, summary, duration_minutes, position")
          .in("module_id", moduleIds),
        supabase.from("quizzes").select("id, module_id, title, pass_mark").in("module_id", moduleIds),
      ])
    : [{ data: [] }, { data: [] }];

  const mods = (modules ?? []) as Module[];
  return {
    course: course as Course,
    modules: mods,
    lessons: orderLessons(mods, (lessonsRes.data ?? []) as LessonSummary[]),
    quizzes: ((quizzesRes.data ?? []) as QuizSummary[]).map((q) => ({ ...q, pass_mark: Number(q.pass_mark) })),
  };
});

export type UserCourseState = {
  enrolled: boolean;
  lastLessonId: string | null;
  completedLessonIds: Set<string>;
  bestScoreByQuiz: Map<string, number>;
};

export async function getUserCourseState(courseId: string, lessonIds: string[], quizIds: string[]): Promise<UserCourseState> {
  const supabase = await createClient();
  const [enrollment, progress, attempts] = await Promise.all([
    supabase.from("enrollments").select("last_lesson_id").eq("course_id", courseId).maybeSingle(),
    lessonIds.length
      ? supabase.from("lesson_progress").select("lesson_id").in("lesson_id", lessonIds)
      : Promise.resolve({ data: [] as { lesson_id: string }[] }),
    quizIds.length
      ? supabase.from("quiz_attempts").select("quiz_id, score_20").in("quiz_id", quizIds)
      : Promise.resolve({ data: [] as { quiz_id: string; score_20: number }[] }),
  ]);

  const best = new Map<string, number>();
  for (const a of attempts.data ?? []) {
    best.set(a.quiz_id, Math.max(best.get(a.quiz_id) ?? 0, Number(a.score_20)));
  }
  return {
    enrolled: Boolean(enrollment.data),
    lastLessonId: enrollment.data?.last_lesson_id ?? null,
    completedLessonIds: new Set((progress.data ?? []).map((p) => p.lesson_id)),
    bestScoreByQuiz: best,
  };
}

export function lessonHref(slug: string, modulePosition: number, lessonSlug: string) {
  return `/formations/${slug}/${modulePosition}/${lessonSlug}`;
}

export function quizHref(slug: string, modulePosition: number) {
  return `/formations/${slug}/${modulePosition}/quiz`;
}
