import type { Metadata } from "next";
import Link from "next/link";
import { AdminNav } from "@/components/admin/admin-nav";

export const metadata: Metadata = { title: "Administration", robots: { index: false, follow: false } };

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="mx-auto max-w-6xl px-5 pt-8">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <Link href="/admin" className="text-sm font-semibold text-blue">
          Administration SMK Academy
        </Link>
        <span className="rounded-full bg-green-soft px-3 py-1 text-[13px] font-medium text-green">
          Session vérifiée par double authentification
        </span>
      </div>
      <AdminNav />
      {children}
    </div>
  );
}
