/** Choix d'une durée d'accès Premium (mois) ou illimitée. */
export function DurationSelect({ max, defaultValue = "1" }: { max: number; defaultValue?: string }) {
  const options = [1, 2, 3, 6, 9, 12, 18, 24, 36, 48, 60, 120].filter((m) => m <= max);
  return (
    <div className="field">
      <label htmlFor="duration">Durée de l&apos;accès Premium</label>
      <select id="duration" name="duration" className="input" defaultValue={defaultValue}>
        {options.map((m) => (
          <option key={m} value={m}>
            {m % 12 === 0 ? (m === 12 ? "1 an (12 mois)" : `${m / 12} ans (${m} mois)`) : `${m} mois`}
          </option>
        ))}
        <option value="illimite">Illimitée (accès total permanent)</option>
      </select>
    </div>
  );
}
