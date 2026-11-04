import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "SMK Academy by SMKTECH",
    short_name: "SMK Academy",
    description: "Cours, exercices et quiz notés sur 20.",
    start_url: "/tableau-de-bord",
    display: "standalone",
    background_color: "#f2f5fa",
    theme_color: "#0b4bd6",
    lang: "fr",
    icons: [
      { src: "/icons/icon-192.png", sizes: "192x192", type: "image/png" },
      { src: "/icons/icon-512.png", sizes: "512x512", type: "image/png" },
      { src: "/icons/maskable-512.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
    ],
  };
}
