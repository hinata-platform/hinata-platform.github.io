'use client';

import { useEffect } from 'react';

export function LangRedirect({ slug }: { slug: string }) {
  useEffect(() => {
    let pref: string | null = null;
    try {
      pref = localStorage.getItem('hinata-lang');
    } catch {
      /* private mode */
    }
    if (pref !== 'en' && pref !== 'de') {
      pref = navigator.language?.toLowerCase().startsWith('de') ? 'de' : 'en';
    }
    location.replace(`/${pref}/${slug}/`);
  }, [slug]);

  return (
    <p style={{ padding: 24, textAlign: 'center' }}>
      <a href={`/en/${slug}/`}>English</a> · <a href={`/de/${slug}/`}>Deutsch</a>
    </p>
  );
}
