import Link from "next/link";
import { notFound } from "next/navigation";
import { deleteLesson, updateLesson } from "@/app/admin/actions";
import { ActionForm, Field, TextArea } from "@/components/admin/action-form";
import { Markdown } from "@/components/markdown";
import { requireAdmin } from "@/lib/admin";

type Props = { params: Promise<{ id: string }> };

const GUIDE = "Markdown : ## Titre, **gras**, `code`, blocs ```python ... ```, sortie ```text, correction repliable ```solution ... ```.";

export default async function AdminLessonPage({ params }: Props) {
  const { id } = await params;
  const { supabase } = await requireAdmin(`/admin/lecons/${id}`);
  const { data: lesson } = await supabase
    .from("lessons")
    .select("*, modules(id, title, position, courses(title))")
    .eq("id", id)
    .maybeSingle();
  if (!lesson) notFound();
  const mod = lesson.modules as unknown as { id: string; title: string; position: number; courses: { title: string } };

  return (
    <>
      <nav aria-label="Fil d'Ariane" className="text-sm text-ink-2">
        <Link href="/admin" className="hover:text-ink">
          Administration
        </Link>
        <span className="mx-2 text-ink-3">/</span>
        <span>{mod.courses.title}</span>
        <span className="mx-2 text-ink-3">/</span>
        <Link href={`/admin/modules/${mod.id}`} className="hover:text-ink">
          Module {mod.position}
        </Link>
      </nav>
      <h1 className="t-1 mt-3">{lesson.title}</h1>

      <div className="mt-8 grid gap-8 xl:grid-cols-2">
        <div className="surface p-6">
          <ActionForm action={updateLesson} submitLabel="Enregistrer la leçon">
            <input type="hidden" name="id" value={lesson.id} />
            <Field label="Titre" name="title" defaultValue={lesson.title} required maxLength={160} />
            <div className="grid gap-5 sm:grid-cols-3">
              <Field label="Slug" name="slug" defaultValue={lesson.slug} required maxLength={60} />
              <Field label="Durée (min)" name="duration_minutes" type="number" defaultValue={lesson.duration_minutes} />
              <Field label="Position" name="position" type="number" defaultValue={lesson.position} />
            </div>
            <Field label="Résumé" name="summary" defaultValue={lesson.summary} maxLength={300} />
            <TextArea label="Contenu" name="content_md" defaultValue={lesson.content_md} rows={24} mono hint={GUIDE} maxLength={100000} />
          </ActionForm>
          <form action={deleteLesson} className="mt-6 border-t border-line pt-5">
            <input type="hidden" name="id" value={lesson.id} />
            <button className="btn btn-plain px-0 text-red">Supprimer cette leçon</button>
          </form>
        </div>
        <div>
          <p className="mb-3 text-sm font-semibold text-ink-2">Aperçu (dernière version enregistrée)</p>
          <div className="surface p-6">
            <Markdown source={lesson.content_md} />
          </div>
        </div>
      </div>
    </>
  );
}
