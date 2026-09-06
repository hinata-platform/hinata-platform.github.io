import type { Metadata } from 'next';

import { Landing } from '@/components/Landing';
import { SITE } from '@/lib/content';
import { latestAppVersion } from '@/lib/version';

export const metadata: Metadata = {
  title: 'Hinata · Open-source, self-hosted project management',
  description:
    'Hinata is an independent, self-hosted project & issue tracker — boards, sprints, Gantt, knowledge base and Git integration, on Android, iOS, Web, macOS, Windows and Linux.',
  alternates: { canonical: '/' },
  openGraph: {
    type: 'website',
    title: 'Hinata — project management you actually own',
    description:
      'Open-source, self-hosted project & issue tracking. Boards, sprints, Gantt, Git integration. Android · iOS · Web · macOS · Windows · Linux.',
    url: String(SITE.base_url) + '/',
  },
};

export default async function Home() {
  return <Landing version={await latestAppVersion()} />;
}
