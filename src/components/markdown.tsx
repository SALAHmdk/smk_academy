import type { ReactElement, ReactNode } from "react";
import ReactMarkdown, { type Components } from "react-markdown";
import rehypeHighlight from "rehype-highlight";
import remarkGfm from "remark-gfm";

type CodeElement = ReactElement<{ className?: string; children?: ReactNode }>;

const components: Components = {
  // Les blocs ```solution deviennent une correction repliable ; les autres, un bloc de code.
  pre({ children }) {
    const code = children as CodeElement;
    const className = code?.props?.className ?? "";
    const lang = /language-([\w-]+)/.exec(className)?.[1] ?? "text";

    if (lang === "solution") {
      return (
        <details className="solution">
          <summary>Voir la correction</summary>
          <div className="code-block" data-lang="python">
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
        rehypePlugins={[[rehypeHighlight, { aliases: { python: ["solution"] }, detect: false }]]}
        components={components}
        skipHtml
      >
        {source}
      </ReactMarkdown>
    </div>
  );
}
