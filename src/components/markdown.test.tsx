import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { Markdown } from "./markdown";

describe("Markdown des leçons", () => {
  it("colore le Python et replie les corrections", () => {
    const html = renderToStaticMarkup(
      <Markdown source={'```python\nprint("Bonjour")\n```\n\n```solution\nx = 1\n```'} />,
    );
    expect(html).toContain('data-lang="python"');
    expect(html).toContain("hljs-built_in");
    expect(html).toContain('<details class="solution">');
    expect(html).toContain("Voir la correction");
  });

  it("ignore le HTML brut (pas d'injection de script)", () => {
    const html = renderToStaticMarkup(<Markdown source={"<script>alert(1)</script>\n\nTexte"} />);
    expect(html).not.toContain("<script>");
    expect(html).toContain("Texte");
  });

  it("rend les tableaux GFM", () => {
    const html = renderToStaticMarkup(<Markdown source={"| a | b |\n|---|---|\n| 1 | 2 |"} />);
    expect(html).toContain("<table>");
  });
});
