import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { QuizForm, type QuizQuestion } from "@/components/quiz-form";
import { formatScore } from "@/lib/learning";
import { getCourseOutline } from "@/lib/queries";
import { createClient } from "@/lib/supabase/server";

type Props = { params: Promise<{ slug: string; module: string }> };

export const metadata: Metadata = { title: "Quiz", robots: { index: false } };

export default async function QuizPage({ params }: Props) {
  const { slug, module } = await params;
  const outline = await getCourseOutline(slug);
  const mod = outline?.modules.find((m) => String(m.position) === module && m.status === "published");
  const quiz = mod && outline?.quizzes.find((q) => q.module_id === mod.id);
  if (!outline || !mod || !quiz) notFound();

  const supabase = await createClient();
  // Seuls l'énoncé et les options sont lus : les corrigés restent dans le schéma privé.
  const [{ data: rows }, { data: attempts }] = await Promise.all([
    supabase
      .from("quiz_questions")
      .select("id, position, kind, prompt, code, points, quiz_options(id, label, position)")
      .eq("quiz_id", quiz.id)
      .order("position"),
    supabase
      .from("quiz_attempts")
      .select("id, score_20, created_at")
      .eq("quiz_id", quiz.id)
      .order("created_at", { ascending: false })
      .limit(5),
  ]);

  const questions: QuizQuestion[] = (rows ?? []).map((q) => ({
    id: q.id,
    position: q.position,
    kind: q.kind as QuizQuestion["kind"],
    prompt: q.prompt,
    code: q.code,
    points: Number(q.points),
    options: [...(q.quiz_options ?? [])].sort((a, b) => a.position - b.position).map(({ id, label }) => ({ id, label })),
  }));
  const total = questions.reduce((s, q) => s + q.points, 0);
  const best = attempts?.length ? Math.max(...attempts.map((a) => Number(a.score_20))) : null;

  return (
    <div className="mx-auto max-w-3xl px-5 pt-8">
      <nav aria-label="Fil d'Ariane" className="text-sm text-ink-2">
        <Link href={`/formations/${slug}`} className="hover:text-ink">
          {outline.course.title}
        </Link>
        <span className="mx-2 text-ink-3">/</span>
        <span>Module {mod.position}</span>
      </nav>

      <header className="mt-4 mb-8">
        <h1 className="t-1">{quiz.title}</h1>
        <p className="mt-3 text-lg text-ink-2">
          {questions.length} questions, {total} points ramenés sur 20. Module validé à partir de{" "}
          {formatScore(quiz.pass_mark)}/20. Vous pouvez repasser le quiz autant de fois que nécessaire.
        </p>
        {best !== null && (
          <p className="mt-3 text-sm text-ink-2">
            Votre meilleure note : <strong className="text-ink">{formatScore(best)}/20</strong> ({attempts!.length}{" "}
            tentative{attempts!.length > 1 ? "s" : ""} récente{attempts!.length > 1 ? "s" : ""}).
          </p>
        )}
      </header>

      <QuizForm quizId={quiz.id} questions={questions} />
    </div>
  );
}
