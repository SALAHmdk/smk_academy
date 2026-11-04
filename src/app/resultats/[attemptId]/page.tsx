import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { z } from "zod";
import { CheckIcon, CrossIcon } from "@/components/icons";
import { formatScore, type Correction } from "@/lib/learning";
import { createClient } from "@/lib/supabase/server";

type Props = { params: Promise<{ attemptId: string }> };

export const metadata: Metadata = { title: "Résultat du quiz", robots: { index: false } };

export default async function ResultPage({ params }: Props) {
  const { attemptId } = await params;
  if (!z.uuid().safeParse(attemptId).success) notFound();

  const supabase = await createClient();
  // RLS : seul l'auteur de la tentative peut la lire.
  const { data: attempt } = await supabase
    .from("quiz_attempts")
    .select("id, quiz_id, points, max_points, score_20, passed, corrections, created_at")
    .eq("id", attemptId)
    .maybeSingle();
  if (!attempt) notFound();

  const { data: quiz } = await supabase
    .from("quizzes")
    .select("id, title, pass_mark, modules(position, courses(slug, title))")
    .eq("id", attempt.quiz_id)
    .single();
  const { data: questions } = await supabase
    .from("quiz_questions")
    .select("id, position, prompt, code, quiz_options(id, label, position)")
    .eq("quiz_id", attempt.quiz_id)
    .order("position");
  if (!quiz || !questions) notFound();

  const mod = quiz.modules as unknown as { position: number; courses: { slug: string; title: string } };
  const corrections = new Map((attempt.corrections as Correction[]).map((c) => [c.question_id, c]));
  const score = Number(attempt.score_20);
  const correctCount = [...corrections.values()].filter((c) => c.is_correct).length;
  const courseHref = `/formations/${mod.courses.slug}`;

  return (
    <div className="mx-auto max-w-3xl px-5 pt-8">
      <nav aria-label="Fil d'Ariane" className="text-sm text-ink-2">
        <Link href={courseHref} className="hover:text-ink">
          {mod.courses.title}
        </Link>
        <span className="mx-2 text-ink-3">/</span>
        <span>{quiz.title}</span>
      </nav>

      <section
        aria-labelledby="note"
        className={`mt-5 rounded-[var(--radius-lg)] p-8 sm:p-10 ${attempt.passed ? "bg-green-soft" : "bg-surface"}`}
      >
        <p className={`font-semibold ${attempt.passed ? "text-green" : "text-ink-2"}`}>
          {attempt.passed ? "Module validé" : `Pas encore validé : il faut ${formatScore(Number(quiz.pass_mark))}/20`}
        </p>
        <h1 id="note" className="mt-2 flex items-baseline gap-2">
          <span className="text-[clamp(4rem,14vw,7rem)] font-bold leading-none tracking-[-0.04em]">{formatScore(score)}</span>
          <span className="text-3xl font-semibold text-ink-2">/20</span>
        </h1>
        <p className="mt-4 text-ink-2">
          {correctCount} bonne{correctCount > 1 ? "s" : ""} réponse{correctCount > 1 ? "s" : ""} sur {questions.length}, soit{" "}
          {formatScore(Number(attempt.points))} points sur {formatScore(Number(attempt.max_points))}.
        </p>
        <div className="mt-7 flex flex-wrap gap-3">
          <Link href={`${courseHref}/${mod.position}/quiz`} className={`btn ${attempt.passed ? "btn-secondary" : "btn-primary"}`}>
            Repasser le quiz
          </Link>
          <Link href={courseHref} className={`btn ${attempt.passed ? "btn-primary" : "btn-secondary"}`}>
            Retour à la formation
          </Link>
        </div>
      </section>

      <section aria-labelledby="correction" className="mt-12">
        <h2 id="correction" className="t-2">
          Correction détaillée
        </h2>
        <ol className="mt-5 space-y-4">
          {questions.map((q) => {
            const c = corrections.get(q.id);
            const selected = new Set(c?.selected ?? []);
            const correct = new Set(c?.correct ?? []);
            const options = [...(q.quiz_options ?? [])].sort((a, b) => a.position - b.position);
            return (
              <li key={q.id} className="surface p-6">
                <div className="flex items-start justify-between gap-4">
                  <p className="text-sm font-semibold text-ink-2">Question {q.position}</p>
                  <span
                    className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-sm font-semibold ${
                      c?.is_correct ? "bg-green-soft text-green" : "bg-red-soft text-red"
                    }`}
                  >
                    {c?.is_correct ? <CheckIcon /> : <CrossIcon />}
                    {formatScore(Number(c?.points ?? 0))}/{formatScore(Number(c?.max_points ?? 0))}
                  </span>
                </div>
                <p className="t-3 mt-2">{q.prompt}</p>
                {q.code && (
                  <div className="code-block mt-3" data-lang="python">
                    <pre>
                      <code>{q.code}</code>
                    </pre>
                  </div>
                )}
                <ul className="mt-4 grid gap-2">
                  {options.map((o) => {
                    const isCorrect = correct.has(o.id);
                    const isSelected = selected.has(o.id);
                    return (
                      <li
                        key={o.id}
                        className={`flex items-center gap-3 rounded-[var(--radius-sm)] border px-4 py-2.5 ${
                          isCorrect ? "border-green bg-green-soft" : isSelected ? "border-red bg-red-soft" : "border-line"
                        }`}
                      >
                        <span className={`shrink-0 ${isCorrect ? "text-green" : isSelected ? "text-red" : "text-transparent"}`}>
                          {isCorrect ? <CheckIcon /> : <CrossIcon />}
                        </span>
                        <span className="flex-1">{o.label}</span>
                        {isSelected && <span className="text-sm text-ink-2">Votre réponse</span>}
                        {!isSelected && isCorrect && <span className="text-sm text-ink-2">Bonne réponse</span>}
                      </li>
                    );
                  })}
                </ul>
                {selected.size === 0 && <p className="mt-3 text-sm text-ink-2">Vous n&apos;avez pas répondu à cette question.</p>}
                {c?.explanation && (
                  <p className="mt-4 border-l-[3px] border-blue pl-4 text-ink-2">
                    <span className="font-semibold text-ink">Explication. </span>
                    {c.explanation}
                  </p>
                )}
              </li>
            );
          })}
        </ol>
      </section>
    </div>
  );
}
