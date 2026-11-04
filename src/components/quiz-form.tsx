"use client";

import { useActionState, useState } from "react";
import { submitQuiz, type QuizState } from "@/app/actions/learning";
import type { QuestionKind } from "@/lib/learning";

export type QuizQuestion = {
  id: string;
  position: number;
  kind: QuestionKind;
  prompt: string;
  code: string | null;
  points: number;
  options: { id: string; label: string }[];
};

const KIND_HINT: Record<QuestionKind, string> = {
  single: "Une seule réponse",
  multiple: "Plusieurs réponses possibles",
  true_false: "Vrai ou faux",
};

export function QuizForm({ quizId, questions }: { quizId: string; questions: QuizQuestion[] }) {
  const [state, action, pending] = useActionState<QuizState, FormData>(submitQuiz, {});
  const [answered, setAnswered] = useState<Record<string, number>>({});
  const answeredCount = Object.values(answered).filter((n) => n > 0).length;
  const remaining = questions.length - answeredCount;

  function track(questionId: string, form: HTMLFormElement | null) {
    if (!form) return;
    const count = form.querySelectorAll(`input[name="q_${questionId}"]:checked`).length;
    setAnswered((a) => ({ ...a, [questionId]: count }));
  }

  return (
    <form
      action={action}
      className="space-y-5"
      onChange={(e) => {
        const input = e.target;
        if (input instanceof HTMLInputElement && input.name.startsWith("q_")) {
          track(input.name.slice(2), e.currentTarget);
        }
      }}
    >
      <input type="hidden" name="quizId" value={quizId} />

      {questions.map((q) => (
        <fieldset key={q.id} className="surface p-6 sm:p-7">
          <legend className="sr-only">Question {q.position}</legend>
          <div className="flex items-baseline justify-between gap-4 text-sm">
            <span className="font-semibold text-blue">Question {q.position}</span>
            <span className="text-ink-3">
              {KIND_HINT[q.kind]}, {q.points} pts
            </span>
          </div>
          <p className="t-3 mt-2">{q.prompt}</p>
          {q.code && (
            <div className="code-block mt-4" data-lang="python">
              <pre>
                <code>{q.code}</code>
              </pre>
            </div>
          )}
          <div className="mt-4 grid gap-2">
            {q.options.map((o) => (
              <label
                key={o.id}
                className="flex min-h-[52px] cursor-pointer items-center gap-3 rounded-[var(--radius-md)] border border-line px-4 py-3 transition-colors hover:bg-surface-2 has-[:checked]:border-blue has-[:checked]:bg-blue-soft"
              >
                <input
                  type={q.kind === "multiple" ? "checkbox" : "radio"}
                  name={`q_${q.id}`}
                  value={o.id}
                  className="h-5 w-5 shrink-0 accent-[var(--smk-blue)]"
                />
                <span className={/[=()"+%/]|^\d/.test(o.label) ? "font-mono text-[0.95rem]" : ""}>{o.label}</span>
              </label>
            ))}
          </div>
        </fieldset>
      ))}

      <div className="glass sticky bottom-[calc(max(14px,env(safe-area-inset-bottom))_+_72px)] z-10 sm:bottom-3 flex flex-col gap-3 rounded-[var(--radius-lg)] p-4 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-sm text-ink-2" aria-live="polite">
          {remaining === 0
            ? "Toutes les questions ont une réponse."
            : `${remaining} question${remaining > 1 ? "s" : ""} sans réponse : elles compteront 0.`}
        </p>
        <button type="submit" className="btn btn-primary" disabled={pending}>
          {pending ? "Correction en cours…" : "Valider mes réponses"}
        </button>
      </div>

      {state.error && (
        <p role="alert" className="rounded-[var(--radius-md)] bg-red-soft px-4 py-3 text-red">
          {state.error}
        </p>
      )}
    </form>
  );
}
