"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { z } from "zod";
import { adminError, requireAdmin, slugify } from "@/lib/admin";

export type AdminState = { error?: string; message?: string };

const uuid = z.uuid();
const slug = z
  .string()
  .trim()
  .min(2, "Identifiant d'URL trop court")
  .max(60)
  .regex(/^[a-z0-9-]+$/, "L'identifiant d'URL ne contient que des minuscules, chiffres et tirets");
const status = z.enum(["draft", "coming_soon", "published"]);
const lines = (max: number) =>
  z
    .string()
    .max(4000)
    .transform((v) => v.split("\n").map((l) => l.trim()).filter(Boolean).slice(0, max));

const courseSchema = z.object({
  title: z.string().trim().min(3, "Titre trop court").max(120),
  slug: z.string().trim().max(60).optional(),
  subtitle: z.string().trim().max(160),
  description: z.string().trim().max(2000),
  category_id: uuid,
  topic: z.string().trim().max(40),
  cover_label: z.string().trim().max(6, "Couverture : 6 caractères maximum"),
  level: z.enum(["debutant", "intermediaire", "avance"]),
  duration_minutes: z.coerce.number().int().min(0).max(100000),
  objectives: lines(12),
  prerequisites: lines(8),
  is_premium: z.literal("on").optional(),
});

function courseInput(form: FormData) {
  return courseSchema.safeParse({
    title: form.get("title"),
    slug: form.get("slug") || undefined,
    subtitle: form.get("subtitle") ?? "",
    description: form.get("description") ?? "",
    category_id: form.get("category_id"),
    topic: form.get("topic") ?? "",
    cover_label: form.get("cover_label") ?? "",
    level: form.get("level"),
    duration_minutes: form.get("duration_minutes"),
    objectives: form.get("objectives") ?? "",
    prerequisites: form.get("prerequisites") ?? "",
    is_premium: form.get("is_premium") ?? undefined,
  });
}

export async function createCourse(_prev: AdminState, form: FormData): Promise<AdminState> {
  const { supabase } = await requireAdmin();
  const parsed = courseInput(form);
  if (!parsed.success) return { error: parsed.error.issues[0].message };
  const { is_premium, slug: rawSlug, ...data } = parsed.data;
  const finalSlug = slug.safeParse(rawSlug || slugify(data.title));
  if (!finalSlug.success) return { error: finalSlug.error.issues[0].message };

  const { data: row, error } = await supabase
    .from("courses")
    .insert({ ...data, slug: finalSlug.data, is_premium: Boolean(is_premium), status: "draft", position: 500 })
    .select("id")
    .single();
  if (error || !row) return { error: adminError(error) };
  redirect(`/admin/formations/${row.id}?cree=1`);
}

export async function updateCourse(_prev: AdminState, form: FormData): Promise<AdminState> {
  const { supabase } = await requireAdmin();
  const id = uuid.safeParse(form.get("id"));
  const parsed = courseInput(form);
  const st = status.safeParse(form.get("status"));
  if (!id.success || !st.success) return { error: "Formulaire invalide." };
  if (!parsed.success) return { error: parsed.error.issues[0].message };
  const { is_premium, slug: rawSlug, ...data } = parsed.data;
  const finalSlug = slug.safeParse(rawSlug);
  if (!finalSlug.success) return { error: finalSlug.error.issues[0].message };

  const { error } = await supabase
    .from("courses")
    .update({ ...data, slug: finalSlug.data, is_premium: Boolean(is_premium), status: st.data })
    .eq("id", id.data);
  if (error) return { error: adminError(error) };
  revalidatePath("/", "layout");
  return { message: st.data === "published" ? "Enregistré et publié." : "Modifications enregistrées." };
}

export async function deleteDraftCourse(_prev: AdminState, form: FormData): Promise<AdminState> {
  const { supabase } = await requireAdmin();
  const id = uuid.safeParse(form.get("id"));
  if (!id.success) return { error: "Formulaire invalide." };
  if (form.get("confirm") !== "SUPPRIMER") return { error: "Tapez SUPPRIMER pour confirmer." };
  const { data: course } = await supabase.from("courses").select("status").eq("id", id.data).single();
  if (course?.status !== "draft") return { error: "Seul un brouillon peut être supprimé. Repassez d'abord la formation en brouillon." };
  const { error } = await supabase.from("courses").delete().eq("id", id.data);
  if (error) return { error: adminError(error) };
  redirect("/admin?supprime=1");
}

// ---------------------------------------------------------------------------
// Modules
// ---------------------------------------------------------------------------
export async function createModule(form: FormData): Promise<void> {
  const { supabase } = await requireAdmin();
  const courseId = uuid.parse(form.get("course_id"));
  const title = z.string().trim().min(2).max(120).parse(form.get("title"));
  const { data: last } = await supabase
    .from("modules")
    .select("position")
    .eq("course_id", courseId)
    .order("position", { ascending: false })
    .limit(1)
    .maybeSingle();
  const { data: row, error } = await supabase
    .from("modules")
    .insert({ course_id: courseId, title, position: (last?.position ?? 0) + 1, status: "draft" })
    .select("id")
    .single();
  if (error || !row) throw new Error(adminError(error));
  redirect(`/admin/modules/${row.id}`);
}

export async function updateModule(_prev: AdminState, form: FormData): Promise<AdminState> {
  const { supabase } = await requireAdmin();
  const parsed = z
    .object({
      id: uuid,
      title: z.string().trim().min(2).max(120),
      description: z.string().trim().max(400),
      position: z.coerce.number().int().min(1).max(100),
      status,
    })
    .safeParse(Object.fromEntries(form));
  if (!parsed.success) return { error: parsed.error.issues[0].message };
  const { id, ...data } = parsed.data;
  const { error } = await supabase.from("modules").update(data).eq("id", id);
  if (error) return { error: adminError(error) };
  revalidatePath("/", "layout");
  return { message: data.status === "published" ? "Module enregistré et publié." : "Module enregistré." };
}

// ---------------------------------------------------------------------------
// Leçons
// ---------------------------------------------------------------------------
export async function createLesson(form: FormData): Promise<void> {
  const { supabase } = await requireAdmin();
  const moduleId = uuid.parse(form.get("module_id"));
  const title = z.string().trim().min(2).max(160).parse(form.get("title"));
  const { data: last } = await supabase
    .from("lessons")
    .select("position")
    .eq("module_id", moduleId)
    .order("position", { ascending: false })
    .limit(1)
    .maybeSingle();
  const position = (last?.position ?? 0) + 1;
  const { data: row, error } = await supabase
    .from("lessons")
    .insert({
      module_id: moduleId,
      title,
      slug: slugify(title) || `lecon-${position}`,
      position,
      content_md: "## Introduction\n\nRédigez ici le contenu de la leçon.",
    })
    .select("id")
    .single();
  if (error || !row) throw new Error(adminError(error));
  redirect(`/admin/lecons/${row.id}`);
}

export async function updateLesson(_prev: AdminState, form: FormData): Promise<AdminState> {
  const { supabase } = await requireAdmin();
  const parsed = z
    .object({
      id: uuid,
      title: z.string().trim().min(2).max(160),
      slug,
      summary: z.string().trim().max(300),
      duration_minutes: z.coerce.number().int().min(1).max(600),
      position: z.coerce.number().int().min(1).max(100),
      content_md: z.string().min(1, "Le contenu ne peut pas être vide").max(100000),
    })
    .safeParse(Object.fromEntries(form));
  if (!parsed.success) return { error: parsed.error.issues[0].message };
  const { id, ...data } = parsed.data;
  const { error } = await supabase.from("lessons").update(data).eq("id", id);
  if (error) return { error: adminError(error) };
  revalidatePath("/", "layout");
  return { message: "Leçon enregistrée." };
}

export async function deleteLesson(form: FormData): Promise<void> {
  const { supabase } = await requireAdmin();
  const id = uuid.parse(form.get("id"));
  const { data: lesson } = await supabase.from("lessons").select("module_id, modules(status)").eq("id", id).single();
  if (!lesson) redirect("/admin");
  const moduleStatus = (lesson.modules as unknown as { status: string } | null)?.status;
  const { count } = await supabase.from("lessons").select("id", { count: "exact", head: true }).eq("module_id", lesson.module_id);
  if (moduleStatus === "published" && (count ?? 0) <= 1) {
    redirect(`/admin/modules/${lesson.module_id}?erreur=derniere-lecon`);
  }
  await supabase.from("lessons").delete().eq("id", id);
  redirect(`/admin/modules/${lesson.module_id}`);
}

// ---------------------------------------------------------------------------
// Quiz et questions
// ---------------------------------------------------------------------------
export async function createQuiz(form: FormData): Promise<void> {
  const { supabase } = await requireAdmin();
  const moduleId = uuid.parse(form.get("module_id"));
  const { data: mod } = await supabase.from("modules").select("title").eq("id", moduleId).single();
  const { data: row, error } = await supabase
    .from("quizzes")
    .insert({ module_id: moduleId, title: `Quiz — ${mod?.title ?? "module"}`, pass_mark: 10 })
    .select("id")
    .single();
  if (error || !row) throw new Error(adminError(error));
  redirect(`/admin/quiz/${row.id}`);
}

export async function updateQuiz(_prev: AdminState, form: FormData): Promise<AdminState> {
  const { supabase } = await requireAdmin();
  const parsed = z
    .object({ id: uuid, title: z.string().trim().min(2).max(160), pass_mark: z.coerce.number().min(0).max(20) })
    .safeParse(Object.fromEntries(form));
  if (!parsed.success) return { error: parsed.error.issues[0].message };
  const { id, ...data } = parsed.data;
  const { error } = await supabase.from("quizzes").update(data).eq("id", id);
  if (error) return { error: adminError(error) };
  return { message: "Quiz enregistré." };
}

const questionSchema = z
  .object({
    quiz_id: uuid,
    id: uuid.optional(),
    kind: z.enum(["single", "multiple", "true_false"]),
    prompt: z.string().trim().min(3, "Énoncé trop court").max(500),
    code: z.string().max(2000).optional(),
    points: z.coerce.number().min(0.5).max(20),
    options: lines(8),
    correct: z
      .string()
      .trim()
      .regex(/^\d+(\s*,\s*\d+)*$/, "Bonnes réponses : numéros d'options séparés par des virgules (ex. 1,3)")
      .transform((v) => [...new Set(v.split(",").map((n) => Number(n.trim())))]),
    explanation: z.string().trim().min(5, "Ajoutez une explication pour la correction").max(2000),
  })
  .superRefine((q, ctx) => {
    const options = q.kind === "true_false" ? ["Vrai", "Faux"] : q.options;
    if (options.length < 2) ctx.addIssue({ code: "custom", message: "Au moins deux options." });
    if (q.correct.some((n) => n < 1 || n > options.length))
      ctx.addIssue({ code: "custom", message: "Une bonne réponse ne correspond à aucune option." });
    if (q.kind !== "multiple" && q.correct.length !== 1)
      ctx.addIssue({ code: "custom", message: "Une seule bonne réponse pour ce type de question." });
  });

export async function saveQuestion(_prev: AdminState, form: FormData): Promise<AdminState> {
  const { supabase } = await requireAdmin();
  const raw = Object.fromEntries(form);
  const parsed = questionSchema.safeParse({ ...raw, id: raw.id || undefined, code: raw.code || undefined });
  if (!parsed.success) return { error: parsed.error.issues[0].message };
  const q = parsed.data;
  const options = q.kind === "true_false" ? ["Vrai", "Faux"] : q.options;

  let questionId = q.id;
  const fields = { kind: q.kind, prompt: q.prompt, code: q.code?.trim() ? q.code : null, points: q.points };
  if (questionId) {
    const { error } = await supabase.from("quiz_questions").update(fields).eq("id", questionId).eq("quiz_id", q.quiz_id);
    if (error) return { error: adminError(error) };
  } else {
    const { data: last } = await supabase
      .from("quiz_questions")
      .select("position")
      .eq("quiz_id", q.quiz_id)
      .order("position", { ascending: false })
      .limit(1)
      .maybeSingle();
    const { data: row, error } = await supabase
      .from("quiz_questions")
      .insert({ ...fields, quiz_id: q.quiz_id, position: (last?.position ?? 0) + 1 })
      .select("id")
      .single();
    if (error || !row) return { error: adminError(error) };
    questionId = row.id;
  }

  // Options mises à jour en place (identifiants conservés pour l'historique des corrections).
  const { data: existing } = await supabase.from("quiz_options").select("id, position").eq("question_id", questionId).order("position");
  const ids: string[] = [];
  for (let i = 0; i < options.length; i++) {
    const current = existing?.find((o) => o.position === i + 1);
    if (current) {
      const { error } = await supabase.from("quiz_options").update({ label: options[i] }).eq("id", current.id);
      if (error) return { error: adminError(error) };
      ids.push(current.id);
    } else {
      const { data: row, error } = await supabase
        .from("quiz_options")
        .insert({ question_id: questionId, position: i + 1, label: options[i] })
        .select("id")
        .single();
      if (error || !row) return { error: adminError(error) };
      ids.push(row.id);
    }
  }
  const extra = (existing ?? []).filter((o) => o.position > options.length).map((o) => o.id);
  if (extra.length) await supabase.from("quiz_options").delete().in("id", extra);

  const { error: keyError } = await supabase.rpc("admin_set_answer_key", {
    p_question_id: questionId,
    p_correct: q.correct.map((n) => ids[n - 1]),
    p_explanation: q.explanation,
  });
  if (keyError) return { error: adminError(keyError) };
  revalidatePath(`/admin/quiz/${q.quiz_id}`);
  return { message: q.id ? "Question mise à jour." : "Question ajoutée." };
}

export async function deleteQuestion(form: FormData): Promise<void> {
  const { supabase } = await requireAdmin();
  const id = uuid.parse(form.get("id"));
  const quizId = uuid.parse(form.get("quiz_id"));
  const { data: quiz } = await supabase.from("quizzes").select("modules(status)").eq("id", quizId).single();
  const { count } = await supabase.from("quiz_questions").select("id", { count: "exact", head: true }).eq("quiz_id", quizId);
  if ((quiz?.modules as unknown as { status: string } | null)?.status === "published" && (count ?? 0) <= 1) {
    redirect(`/admin/quiz/${quizId}?erreur=derniere-question`);
  }
  await supabase.from("quiz_questions").delete().eq("id", id).eq("quiz_id", quizId);
  redirect(`/admin/quiz/${quizId}`);
}
