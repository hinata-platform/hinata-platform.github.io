import { DocsChrome } from '@/components/DocsChrome';
import { LANGS, type Lang } from '@/lib/content';

export function generateStaticParams() {
  return LANGS.map((lang) => ({ lang }));
}

export const dynamicParams = false;

export default async function DocsLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  // Next types a dynamic segment as string; only these two are ever generated.
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  return <DocsChrome lang={lang as Lang}>{children}</DocsChrome>;
}
