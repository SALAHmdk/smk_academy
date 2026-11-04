"use client";

export default function ErrorPage({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <div className="mx-auto max-w-xl px-5 pt-24 text-center">
      <h1 className="t-1">Le chargement a échoué</h1>
      <p className="mt-4 text-lg text-ink-2">
        Vérifiez votre connexion internet, puis réessayez. Si le problème persiste, revenez dans quelques minutes.
      </p>
      <button type="button" onClick={reset} className="btn btn-primary mt-8">
        Réessayer
      </button>
    </div>
  );
}
