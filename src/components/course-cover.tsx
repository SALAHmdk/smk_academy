/**
 * Couverture typographique d'une formation : monogramme de la technologie sur un dégradé
 * tiré de la palette SMKTECH (bleu, vert, marine), décliné par catégorie.
 * Aucune image externe ni logo de marque tierce.
 */
const PALETTES: Record<string, [string, string, string]> = {
  programmation: ["#0b4bd6", "#1f7ae0", "135deg"],
  "developpement-web": ["#1f7ae0", "#00b386", "120deg"],
  "bases-de-donnees": ["#0e1a33", "#0b4bd6", "150deg"],
  "data-science": ["#007a63", "#1f7ae0", "135deg"],
  "intelligence-artificielle": ["#2a2f8f", "#0b4bd6", "135deg"],
  "cloud-devops": ["#0b4bd6", "#47a9ff", "160deg"],
  cybersecurite: ["#0e1a33", "#00a37a", "135deg"],
  "business-intelligence": ["#00a37a", "#7ddc9f", "135deg"],
  "developpement-mobile": ["#0b4bd6", "#00b386", "200deg"],
  langues: ["#00b386", "#0b4bd6", "135deg"],
};

export function CourseCover({
  label,
  category,
  size = "md",
  muted = false,
}: {
  label: string;
  category?: string | null;
  size?: "sm" | "md" | "lg";
  muted?: boolean;
}) {
  const [from, to, angle] = PALETTES[category ?? ""] ?? PALETTES.programmation;
  const text = label || "SMK";
  const fontSize = size === "lg" ? 76 : size === "sm" ? 26 : 46;
  return (
    <div
      aria-hidden="true"
      className="relative grid h-full w-full place-items-center overflow-hidden"
      style={{ background: `linear-gradient(${angle}, ${from}, ${to})`, filter: muted ? "saturate(0.55)" : undefined }}
    >
      {/* reflet doux pour donner de la profondeur sans image */}
      <div
        className="absolute -right-1/4 -top-1/3 h-[120%] w-[80%] rounded-full opacity-25"
        style={{ background: "radial-gradient(circle, rgba(255,255,255,0.7), transparent 65%)" }}
      />
      <span
        className="relative font-bold tracking-[-0.04em] text-white"
        style={{ fontSize, lineHeight: 1, textShadow: "0 2px 18px rgba(0,0,0,0.18)" }}
      >
        {text}
      </span>
    </div>
  );
}
