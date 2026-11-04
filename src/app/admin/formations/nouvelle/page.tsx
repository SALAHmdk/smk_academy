import Link from "next/link";
import { createCourse } from "@/app/admin/actions";
import { ActionForm } from "@/components/admin/action-form";
import { CourseFields } from "@/components/admin/course-fields";
import { requireAdmin } from "@/lib/admin";

export default async function NewCoursePage() {
  const { supabase } = await requireAdmin("/admin/formations/nouvelle");
  const { data: categories } = await supabase.from("categories").select("id, slug, name, description, position").order("position");

  return (
    <>
      <nav aria-label="Fil d'Ariane" className="text-sm text-ink-2">
        <Link href="/admin" className="hover:text-ink">
          Administration
        </Link>
        <span className="mx-2 text-ink-3">/</span>
        <span>Nouvelle formation</span>
      </nav>
      <h1 className="t-1 mt-3">Nouvelle formation</h1>
      <p className="mt-2 max-w-2xl text-ink-2">
        La formation est créée en brouillon, invisible des étudiants. Vous ajouterez ensuite modules, leçons et quiz, puis
        la publierez.
      </p>
      <div className="surface mt-8 p-6 sm:p-8">
        <ActionForm action={createCourse} submitLabel="Créer le brouillon" pendingLabel="Création…">
          <CourseFields categories={categories ?? []} slugHint="Laissez vide pour le générer depuis le titre." />
        </ActionForm>
      </div>
    </>
  );
}
