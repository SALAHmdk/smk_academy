import Image from "next/image";

export function AuthShell({
  title,
  subtitle,
  children,
  footer,
}: {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}) {
  return (
    <div className="mx-auto max-w-md px-5 pt-12 sm:pt-16">
      <div className="surface p-7 sm:p-9">
        <Image src="/smktech-logo.png" alt="SMKTECH" width={52} height={52} className="h-[52px] w-auto" />
        <h1 className="t-2 mt-5">{title}</h1>
        {subtitle && <p className="mt-2 text-ink-2">{subtitle}</p>}
        <div className="mt-7">{children}</div>
      </div>
      {footer && <p className="mt-6 text-center text-ink-2">{footer}</p>}
    </div>
  );
}
