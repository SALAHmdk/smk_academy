import { Field, TextArea } from "@/components/admin/action-form";
import { LEVEL_LABEL, LEVELS, type Category } from "@/lib/learning";

export type CourseValues = {
  title?: string;
  slug?: string;
  subtitle?: string;
  description?: string;
  category_id?: string;
  topic?: string;
  cover_label?: string;
  level?: string;
  duration_minutes?: number;
  objectives?: string[];
  prerequisites?: string[];
  is_premium?: boolean;
};

export function CourseFields({ categories, values = {}, slugHint }: { categories: Category[]; values?: CourseValues; slugHint: string }) {
  return (
    <>
      <div className="grid gap-5 sm:grid-cols-2">
        <Field label="Titre" name="title" defaultValue={values.title} required maxLength={120} />
        <Field label="Identifiant d'URL (slug)" name="slug" defaultValue={values.slug} maxLength={60} hint={slugHint} />
      </div>
      <Field label="Sous-titre (une phrase)" name="subtitle" defaultValue={values.subtitle} maxLength={160} />
      <TextArea label="Description" name="description" defaultValue={values.description} rows={3} maxLength={2000} />
      <div className="grid gap-5 sm:grid-cols-3">
        <div className="field">
          <label htmlFor="category_id">Catégorie</label>
          <select id="category_id" name="category_id" className="input" defaultValue={values.category_id} required>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>
        <Field label="Langage ou outil" name="topic" defaultValue={values.topic} maxLength={40} hint="Utilisé par le filtre du catalogue." />
        <Field label="Couverture (2 à 6 caractères)" name="cover_label" defaultValue={values.cover_label} maxLength={6} hint="Ex. Py, JS, SQL." />
      </div>
      <div className="grid gap-5 sm:grid-cols-3">
        <div className="field">
          <label htmlFor="level">Niveau</label>
          <select id="level" name="level" className="input" defaultValue={values.level ?? "debutant"}>
            {LEVELS.map((l) => (
              <option key={l} value={l}>
                {LEVEL_LABEL[l]}
              </option>
            ))}
          </select>
        </div>
        <Field label="Durée estimée (minutes)" name="duration_minutes" type="number" inputMode="numeric" defaultValue={values.duration_minutes ?? 300} />
        <label className="flex min-h-[48px] items-center gap-3 self-end">
          <input type="checkbox" name="is_premium" defaultChecked={values.is_premium} className="h-5 w-5 accent-[var(--smk-blue)]" />
          Réservée à l&apos;offre Premium
        </label>
      </div>
      <div className="grid gap-5 sm:grid-cols-2">
        <TextArea label="Objectifs (un par ligne)" name="objectives" defaultValue={values.objectives?.join("\n")} rows={4} />
        <TextArea label="Prérequis (un par ligne)" name="prerequisites" defaultValue={values.prerequisites?.join("\n")} rows={4} />
      </div>
    </>
  );
}
