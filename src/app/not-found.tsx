import Link from "next/link";

export default function NotFound() {
  return (
    <div className="mx-auto max-w-xl px-5 pt-24 text-center">
      <p className="font-semibold text-blue">Erreur 404</p>
      <h1 className="t-1 mt-2">Cette page n&apos;existe pas</h1>
      <p className="mt-4 text-lg text-ink-2">Le lien est peut-être incorrect, ou la page a été déplacée.</p>
      <div className="mt-8 flex justify-center gap-3">
        <Link href="/formations" className="btn btn-primary">
          Voir les formations
        </Link>
        <Link href="/" className="btn btn-secondary">
          Accueil
        </Link>
      </div>
    </div>
  );
}
