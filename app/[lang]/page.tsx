import { DocPage, docMetadata } from '@/components/DocPage';
import { LANGS, type Lang } from '@/lib/content';

export function generateStaticParams() {
  return LANGS.map((lang) => ({ lang }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  return docMetadata(lang as Lang, 'index');
}

export default async function LangIndex({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  return <DocPage lang={lang as Lang} slug="index" />;
}
