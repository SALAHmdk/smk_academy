import "server-only";
import { cookies } from "next/headers";

export type Theme = "auto" | "light" | "dark";

export async function getTheme(): Promise<Theme> {
  const value = (await cookies()).get("smk-theme")?.value;
  return value === "light" || value === "dark" ? value : "auto";
}
