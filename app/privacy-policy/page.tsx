import { LangRedirect } from '@/components/LangRedirect';

export const metadata = {
  title: 'Hinata',
  alternates: { canonical: '/en/privacy-policy/' },
};

/** /privacy-policy is a language-neutral entry point.
 *
 * It is the canonical URL the apps and the store listings point at, so it
 * cannot be an /en/ or /de/ URL. It forwards to the reader's language, and
 * offers both as plain links for anything that does not run scripts. */
export default function Page() {
  return <LangRedirect slug="privacy-policy" />;
}
