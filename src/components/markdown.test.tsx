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

  it("colore le SQL, y compris dans les corrections ```solution-sql", () => {
    const html = renderToStaticMarkup(
      <Markdown source={"```sql\nSELECT nom FROM etudiants;\n```\n\n```solution-sql\nSELECT * FROM formations WHERE prix > 0;\n```"} />,
    );
    expect(html).toContain('data-lang="sql"');
    expect(html).toContain("hljs-keyword");
    expect((html.match(/<details class="solution">/g) ?? []).length).toBe(1);
    expect(html).toMatch(/<details class="solution">[\s\S]*data-lang="sql"[\s\S]*hljs-keyword/);
  });

  it("colore les corrections JavaScript, HTML et CSS", () => {
    const html = renderToStaticMarkup(
      <Markdown source={"```solution-js\nconst a = 1;\n```\n\n```solution-html\n<p>Bonjour</p>\n```\n\n```solution-css\np { color: red; }\n```"} />,
    );
    expect((html.match(/<details class="solution">/g) ?? []).length).toBe(3);
    expect(html).toContain('data-lang="js"');
    expect(html).toContain('data-lang="html"');
    expect(html).toContain('data-lang="css"');
    expect(html).toContain("hljs-keyword");
    expect(html).toContain("hljs-tag");
    expect(html).not.toContain("<p>Bonjour</p>");
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
