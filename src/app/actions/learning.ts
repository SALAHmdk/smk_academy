"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { z } from "zod";
import { answersFromFormData, quizSubmissionSchema } from "@/lib/learning";
import { createClient, getCurrentUser } from "@/lib/supabase/server";

const uuid = z.uuid();
const internalPath = z.string().regex(/^\/[a-z0-9\-/]*$/);

async function requireUser() {
  const user = await getCurrentUser();
  if (!user) redirect("/connexion");
  return user;
}

export async function enrollInCourse(form: FormData): Promise<void> {
  await requireUser();
  const courseId = uuid.parse(form.get("courseId"));
  const next = internalPath.parse(form.get("next"));

  const supabase = await createClient();
  const { error } = await supabase.rpc("enroll_in_course", { p_course_id: courseId });
  if (error) throw new Error("Inscription impossible pour le moment.");
  revalidatePath("/tableau-de-bord");
  redirect(next);
}

export async function completeLesson(form: FormData): Promise<void> {
  await requireUser();
  const lessonId = uuid.parse(form.get("lessonId"));
  const next = internalPath.parse(form.get("next"));

  const supabase = await createClient();
  const { error } = await supabase.rpc("complete_lesson", { p_lesson_id: lessonId });
  if (error) throw new Error("Impossible d'enregistrer la progression.");
  revalidatePath("/tableau-de-bord");
  redirect(next);
}

export type QuizState = { error?: string };

export async function submitQuiz(_prev: QuizState, form: FormData): Promise<QuizState> {
  await requireUser();
  const parsed = quizSubmissionSchema.safeParse({
    quizId: form.get("quizId"),
    answers: answersFromFormData(form),
  });
  if (!parsed.success) return { error: "Réponses invalides. Rechargez la page et réessayez." };

  const supabase = await createClient();
  // La note est calculée exclusivement en base (public.submit_quiz).
  const { data, error } = await supabase.rpc("submit_quiz", {
    p_quiz_id: parsed.data.quizId,
    p_answers: parsed.data.answers,
  });
  if (error || !data) {
    if (error?.code === "54000") return { error: "Trop de tentatives d'affilée. Réessayez dans une minute." };
    return { error: "La correction n'a pas pu être enregistrée. Réessayez." };
  }

  revalidatePath("/tableau-de-bord");
  redirect(`/resultats/${(data as { id: string }).id}`);
}
