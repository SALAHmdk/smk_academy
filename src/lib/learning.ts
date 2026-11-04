import { z } from "zod";

/** Types métier (miroir du schéma Supabase). */
export type CourseStatus = "draft" | "published" | "coming_soon";
export type Level = "debutant" | "intermediaire" | "avance";
export type QuestionKind = "single" | "multiple" | "true_false";

export type Category = { id: string; slug: string; name: string; description: string; position: number };

export type Course = {
  id: string;
  slug: string;
  title: string;
  subtitle: string;
  description: string;
  category_id: string;
  topic: string;
  cover_label: string;
  categories: { slug: string; name: string } | null;
  level: Level;
  duration_minutes: number;
  objectives: string[];
  prerequisites: string[];
  status: CourseStatus;
  is_premium: boolean;
  position: number;
};

export type Module = {
  id: string;
  course_id: string;
  title: string;
  description: string;
  position: number;
  status: CourseStatus;
};

export type LessonSummary = {
  id: string;
  module_id: string;
  slug: string;
  title: string;
  summary: string;
  duration_minutes: number;
  position: number;
};

export type Correction = {
  question_id: string;
  selected: string[];
  correct: string[];
  is_correct: boolean;
  points: number;
  max_points: number;
  explanation: string;
};

export const LEVELS: Level[] = ["debutant", "intermediaire", "avance"];

export const LEVEL_LABEL: Record<Level, string> = {
  debutant: "Débutant",
  intermediaire: "Intermédiaire",
  avance: "Avancé",
};

export function formatDuration(minutes: number): string {
  if (minutes < 60) return `${minutes} min`;
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return m === 0 ? `${h} h` : `${h} h ${m.toString().padStart(2, "0")}`;
}

/** Note sur 20 au format français : 17,5 / 20 ; 20 / 20. */
export function formatScore(score: number): string {
  const rounded = Math.round(score * 100) / 100;
  return rounded.toLocaleString("fr-FR", { maximumFractionDigits: 2 });
}

export function percent(done: number, total: number): number {
  if (total <= 0) return 0;
  return Math.min(100, Math.round((done / total) * 100));
}

/** Meilleure note par quiz puis moyenne de ces meilleures notes. */
export function averageOfBest(attempts: { quiz_id: string; score_20: number }[]): number | null {
  const best = new Map<string, number>();
  for (const a of attempts) {
    const s = Number(a.score_20);
    best.set(a.quiz_id, Math.max(best.get(a.quiz_id) ?? 0, s));
  }
  if (best.size === 0) return null;
  const sum = [...best.values()].reduce((acc, s) => acc + s, 0);
  return Math.round((sum / best.size) * 100) / 100;
}

/** Ordre de lecture d'une formation : modules puis leçons, par position. */
export function orderLessons<M extends { id: string; position: number }, L extends { module_id: string; position: number }>(
  modules: M[],
  lessons: L[],
): L[] {
  const modPos = new Map(modules.map((m) => [m.id, m.position]));
  return [...lessons]
    .filter((l) => modPos.has(l.module_id))
    .sort((a, b) => modPos.get(a.module_id)! - modPos.get(b.module_id)! || a.position - b.position);
}

const uuid = z.uuid();

/** Validation des réponses envoyées par le navigateur avant l'appel à submit_quiz. */
export const quizSubmissionSchema = z.object({
  quizId: uuid,
  answers: z
    .record(uuid, z.array(uuid).max(10))
    .refine((r) => Object.keys(r).length <= 100, "Trop de questions"),
});

/** Convertit le FormData d'un quiz (champs q_<questionId>) en dictionnaire de réponses. */
export function answersFromFormData(form: FormData): Record<string, string[]> {
  const answers: Record<string, string[]> = {};
  for (const [key, value] of form.entries()) {
    if (!key.startsWith("q_") || typeof value !== "string") continue;
    const questionId = key.slice(2);
    (answers[questionId] ??= []).push(value);
  }
  return answers;
}

/** N'autorise que des redirections internes (évite les redirections ouvertes). */
export function safeNextPath(raw: unknown, fallback = "/tableau-de-bord"): string {
  if (typeof raw !== "string") return fallback;
  if (!raw.startsWith("/") || raw.startsWith("//") || raw.startsWith("/\\")) return fallback;
  if (/[\r\n]/.test(raw)) return fallback;
  return raw;
}

/** Normalise un texte pour la recherche (minuscules, sans accents). */
export function normalize(text: string): string {
  return text
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

export type CatalogFilters = { q?: string; categorie?: string; langage?: string; niveau?: string; dispo?: string };

/** Filtre le catalogue côté serveur (recherche plein texte simple + filtres). */
export function filterCatalog(courses: Course[], f: CatalogFilters): Course[] {
  const words = normalize(f.q ?? "").split(/\s+/).filter(Boolean);
  return courses.filter((c) => {
    if (f.categorie && c.categories?.slug !== f.categorie) return false;
    if (f.langage && c.topic !== f.langage) return false;
    if (f.niveau && c.level !== f.niveau) return false;
    if (f.dispo === "1" && c.status !== "published") return false;
    if (words.length) {
      const haystack = normalize([c.title, c.subtitle, c.description, c.topic, c.categories?.name ?? "", ...c.objectives].join(" "));
      if (!words.every((w) => haystack.includes(w))) return false;
    }
    return true;
  });
}
