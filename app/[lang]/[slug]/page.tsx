import { DocPage, docMetadata } from '@/components/DocPage';
import { ALL_SLUGS, LANGS, type Lang } from '@/lib/content';

export function generateStaticParams() {
  // `index` is the /<lang>/ route one level up, not /<lang>/index/.
  return LANGS.flatMap((lang) =>
    ALL_SLUGS.filter((slug) => slug !== 'index').map((slug) => ({ lang, slug })),
  );
}

export const dynamicParams = false;

export async function generateMetadata({
  params,
}: {
  params: Promise<{ lang: string; slug: string }>;
}) {
  const { lang, slug } = await params;
  return docMetadata(lang as Lang, slug);
}

export default async function DocRoute({
  params,
}: {
  params: Promise<{ lang: string; slug: string }>;
}) {
  const { lang, slug } = await params;
  return <DocPage lang={lang as Lang} slug={slug} />;
}
