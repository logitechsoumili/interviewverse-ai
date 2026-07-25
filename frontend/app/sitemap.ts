import type { MetadataRoute } from "next";

export const dynamic = "force-static";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl =
    process.env.NEXT_PUBLIC_APP_URL?.trim() || "https://interviewverse-ai.example.com";
  const cleanBaseUrl = baseUrl.replace(/\/$/, "");

  // Only index public routes (Auth-gated /dashboard pages are excluded)
  const routes = ["", "/login", "/register"];

  return routes.map((route) => ({
    url: `${cleanBaseUrl}${route}`,
    lastModified: new Date(),
    changeFrequency: "daily" as const,
    priority: route === "" ? 1.0 : 0.8,
  }));
}
