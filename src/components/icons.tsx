type IconProps = { className?: string };

export function CheckIcon({ className = "h-4 w-4" }: IconProps) {
  return (
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true" className={className}>
      <path d="M4.5 10.5l3.5 3.5 7.5-8" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function CrossIcon({ className = "h-4 w-4" }: IconProps) {
  return (
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true" className={className}>
      <path d="M5.5 5.5l9 9m0-9l-9 9" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" />
    </svg>
  );
}

export function ChevronIcon({ className = "h-4 w-4", direction = "right" }: IconProps & { direction?: "left" | "right" }) {
  return (
    <svg
      viewBox="0 0 20 20"
      fill="none"
      aria-hidden="true"
      className={className}
      style={direction === "left" ? { transform: "scaleX(-1)" } : undefined}
    >
      <path d="M7.5 4.5L13 10l-5.5 5.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

/** Pastille d'état d'une leçon : terminée (vert), en cours (bleu), à faire (contour). */
export function StatusDot({ state }: { state: "done" | "current" | "todo" }) {
  if (state === "done") {
    return (
      <span className="grid h-6 w-6 shrink-0 place-items-center rounded-full bg-green text-white" aria-label="Terminée">
        <CheckIcon className="h-3.5 w-3.5" />
      </span>
    );
  }
  if (state === "current") {
    return (
      <span className="grid h-6 w-6 shrink-0 place-items-center rounded-full border-2 border-blue" aria-label="En cours">
        <span className="h-2 w-2 rounded-full bg-blue" />
      </span>
    );
  }
  return <span className="h-6 w-6 shrink-0 rounded-full border-2 border-line" aria-label="À faire" />;
}
