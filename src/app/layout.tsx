import type { Metadata, Viewport } from "next";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";
import { getTheme } from "@/lib/theme";
import "./globals.css";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "SMK Academy — Learn. Practice. Succeed.",
    template: "%s · SMK Academy",
  },
  description:
    "SMK Academy, la plateforme de formation de SMKTECH : cours de programmation progressifs, exercices corrigés et quiz notés sur 20.",
  applicationName: "SMK Academy",
  openGraph: {
    type: "website",
    locale: "fr_FR",
    siteName: "SMK Academy",
    images: [{ url: "/icons/icon-512.png", width: 512, height: 512, alt: "Logo SMKTECH" }],
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#f5f5f7" },
    { media: "(prefers-color-scheme: dark)", color: "#000000" },
  ],
};

export default async function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  const theme = await getTheme();
  return (
    <html lang="fr" data-theme={theme === "auto" ? undefined : theme}>
      <body className="flex min-h-dvh flex-col">
        <a
          href="#contenu"
          className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-full focus:bg-surface focus:px-4 focus:py-2"
        >
          Aller au contenu
        </a>
        <SiteHeader />
        <main id="contenu" className="flex-1 pb-28 sm:pb-0">
          {children}
        </main>
        <SiteFooter />
      </body>
    </html>
  );
}
