import Link from 'next/link';

export const metadata = { title: 'Not found · Hinata Docs' };

export default function NotFound() {
  return (
    <main className="notfound">
      <div>
        <h1>404</h1>
        <p>This page does not exist.</p>
        <p>
          <Link href="/en/">← Documentation (EN)</Link> ·{' '}
          <Link href="/de/">Dokumentation (DE) →</Link>
        </p>
      </div>
    </main>
  );
}
