import Link from "next/link";
import { notFound } from "next/navigation";
import { deleteQuestion, saveQuestion, updateQuiz } from "@/app/admin/actions";
import { ActionForm, Field, TextArea } from "@/components/admin/action-form";
import { requireAdmin } from "@/lib/admin";

type Props = { params: Promise<{ id: string }>; searchParams: Promise<{ erreur?: string }> };
type Question = { id: string; position: number; kind: string; prompt: string; code: string | null; points: number; quiz_options: { id: string; position: number; label: string }[] };

function QuestionFields({ quizId, q, correct, explanation }: { quizId: string; q?: Question; correct?: string; explanation?: string }) {
  const options = [...(q?.quiz_options ?? [])].sort((a, b) => a.position - b.position);
  return (
    <>
      <input type="hidden" name="quiz_id" value={quizId} />
      {q && <input type="hidden" name="id" value={q.id} />}
      <div className="grid gap-5 sm:grid-cols-[1fr_200px_110px]">
        <Field label="Énoncé" name="prompt" defaultValue={q?.prompt} required maxLength={500} />
        <div className="field">
          <label htmlFor={`kind-${q?.id ?? "new"}`}>Type</label>
          <select id={`kind-${q?.id ?? "new"}`} name="kind" className="input" defaultValue={q?.kind ?? "single"}>
            <option value="single">Une seule réponse</option>
            <option value="multiple">Plusieurs réponses</option>
            <option value="true_false">Vrai / faux</option>
          </select>
        </div>
        <Field label="Points" name="points" type="number" defaultValue={q?.points ?? 2} />
      </div>
      <TextArea label="Code affiché (facultatif)" name="code" defaultValue={q?.code ?? ""} rows={3} mono maxLength={2000} />
      <div className="grid gap-5 sm:grid-cols-2">
        <TextArea
          label="Options (une par ligne)"
          name="options"
          defaultValue={options.map((o) => o.label).join("\n")}
          rows={5}
          hint="Ignoré pour vrai / faux (options Vrai puis Faux)."
        />
        <div className="grid content-start gap-5">
          <Field label="Bonne(s) réponse(s) : numéro(s) d'option" name="correct" defaultValue={correct} required hint="Ex. 2 ou 1,3 pour plusieurs réponses." />
          <TextArea label="Explication affichée dans la correction" name="explanation" defaultValue={explanation} rows={3} maxLength={2000} />
        </div>
      </div>
    </>
  );
}

export default async function AdminQuizPage({ params, searchParams }: Props) {
  const { id } = await params;
  const { supabase } = await requireAdmin(`/admin/quiz/${id}`);
  const { erreur } = await searchParams;
  const [{ data: quiz }, { data: questions }, { data: keys }] = await Promise.all([
    supabase.from("quizzes").select("id, title, pass_mark, modules(id, title, position)").eq("id", id).maybeSingle(),
    supabase.from("quiz_questions").select("id, position, kind, prompt, code, points, quiz_options(id, position, label)").eq("quiz_id", id).order("position"),
    supabase.rpc("admin_get_answer_keys", { p_quiz_id: id }),
  ]);
  if (!quiz) notFound();
  const mod = quiz.modules as unknown as { id: string; title: string; position: number };
  const keyBy = new Map((keys ?? []).map((k) => [k.question_id, k]));
  const total = (questions ?? []).reduce((s, q) => s + Number(q.points), 0);

  return (
    <>
      <nav aria-label="Fil d'Ariane" className="text-sm text-ink-2">
        <Link href="/admin" className="hover:text-ink">
          Administration
        </Link>
        <span className="mx-2 text-ink-3">/</span>
        <Link href={`/admin/modules/${mod.id}`} className="hover:text-ink">
          Module {mod.position} — {mod.title}
        </Link>
      </nav>
      <h1 className="t-1 mt-3">{quiz.title}</h1>
      <p className="mt-2 text-ink-2">
        {(questions ?? []).length} question(s), {total} point(s) ramenés sur 20. Les corrigés sont stockés dans un espace
        privé de la base : ils ne sont jamais envoyés aux étudiants avant correction.
      </p>
      {erreur === "derniere-question" && (
        <p role="alert" className="mt-4 rounded-[var(--radius-md)] bg-red-soft px-4 py-3 text-red">
          Impossible de supprimer la dernière question du quiz d&apos;un module publié.
        </p>
      )}

      <div className="surface mt-6 p-6">
        <ActionForm action={updateQuiz} submitLabel="Enregistrer" className="flex flex-wrap items-end gap-4">
          <input type="hidden" name="id" value={quiz.id} />
          <div className="min-w-[240px] flex-1">
            <Field label="Titre du quiz" name="title" defaultValue={quiz.title} required maxLength={160} />
          </div>
          <div className="w-36">
            <Field label="Seuil (/20)" name="pass_mark" type="number" defaultValue={Number(quiz.pass_mark)} />
          </div>
        </ActionForm>
      </div>

      <ol className="mt-8 space-y-5">
        {(questions as Question[] | null ?? []).map((q) => {
          const k = keyBy.get(q.id);
          const opts = [...(q.quiz_options ?? [])].sort((a, b) => a.position - b.position);
          const correct = k ? k.correct_option_ids.map((cid) => opts.findIndex((o) => o.id === cid) + 1).filter((n) => n > 0).join(",") : "";
          return (
            <li key={q.id} className="surface p-6">
              <div className="mb-4 flex items-center justify-between gap-3">
                <p className="font-semibold text-blue">Question {q.position}</p>
                {!k && <span className="rounded-full bg-red-soft px-2.5 py-0.5 text-[13px] font-semibold text-red">Corrigé manquant</span>}
              </div>
              <ActionForm action={saveQuestion} submitLabel="Enregistrer la question">
                <QuestionFields quizId={quiz.id} q={q} correct={correct} explanation={k?.explanation} />
              </ActionForm>
              <form action={deleteQuestion} className="mt-4">
                <input type="hidden" name="id" value={q.id} />
                <input type="hidden" name="quiz_id" value={quiz.id} />
                <button className="btn btn-plain px-0 text-red">Supprimer la question</button>
              </form>
            </li>
          );
        })}
        <li className="surface border-2 border-dashed border-line p-6">
          <p className="mb-4 font-semibold">Nouvelle question</p>
          <ActionForm action={saveQuestion} submitLabel="Ajouter la question">
            <QuestionFields quizId={quiz.id} />
          </ActionForm>
        </li>
      </ol>
    </>
  );
}
