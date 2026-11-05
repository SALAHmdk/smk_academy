import type { ReactElement, ReactNode } from "react";
import ReactMarkdown, { type Components } from "react-markdown";
import rehypeHighlight from "rehype-highlight";
import remarkGfm from "remark-gfm";

type CodeElement = ReactElement<{ className?: string; children?: ReactNode }>;

const components: Components = {
  // Les blocs ```solution (Python), ```solution-sql, ```solution-text deviennent une correction repliable.
  pre({ children }) {
    const code = children as CodeElement;
    const className = code?.props?.className ?? "";
    const lang = /language-([\w-]+)/.exec(className)?.[1] ?? "text";

    if (lang === "solution" || lang.startsWith("solution-")) {
      return (
        <details className="solution">
          <summary>Voir la correction</summary>
          <div className="code-block" data-lang={lang === "solution" ? "python" : lang.slice("solution-".length)}>
            <pre>{children}</pre>
          </div>
        </details>
      );
    }

    return (
      <div className="code-block" data-lang={lang}>
        <pre>{children}</pre>
      </div>
    );
  },
  // Pas d'images ni de HTML brut dans le contenu pour l'instant.
  img: () => null,
};

export function Markdown({ source }: { source: string }) {
  return (
    <div className="lesson">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[[rehypeHighlight, { aliases: { python: ["solution"], sql: ["solution-sql"], plaintext: ["solution-text"], javascript: ["solution-js"], xml: ["solution-html"], css: ["solution-css"] }, detect: false }]]}
        components={components}
        skipHtml
      >
        {source}
      </ReactMarkdown>
    </div>
  );
}
