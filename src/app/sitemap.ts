import type { MetadataRoute } from "next";

const COURSES = ["python-debutant"];

export default function sitemap(): MetadataRoute.Sitemap {
  const site = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";
  return [
    { url: `${site}/`, changeFrequency: "weekly", priority: 1 },
    { url: `${site}/formations`, changeFrequency: "weekly", priority: 0.9 },
    ...COURSES.map((slug) => ({ url: `${site}/formations/${slug}`, changeFrequency: "weekly" as const, priority: 0.8 })),
  ];
}
