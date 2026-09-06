'use client';

import { useEffect } from 'react';

import { ICONS } from '@/lib/icons';

/** Puts a copy button on every code block of the rendered article.
 *
 * The article is HTML from the markdown pipeline, not React children, so the
 * buttons are attached to the DOM after it lands rather than rendered into it.
 * It re-runs per page because a client navigation swaps the article without
 * remounting the layout.
 */
export function CodeCopy({ deps, copy, copied }: { deps: string; copy: string; copied: string }) {
  useEffect(() => {
    const blocks = document.querySelectorAll<HTMLElement>('.prose pre');
    const added: HTMLElement[] = [];
    blocks.forEach((block) => {
      if (block.querySelector('.copy-btn')) return;
      const code = block.querySelector('code');
      if (!code) return;
      const btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.type = 'button';
      btn.append(icon('copy'), label(copy));
      btn.addEventListener('click', () => {
        navigator.clipboard.writeText(code.innerText).then(() => {
          btn.classList.add('copied');
          btn.replaceChildren(icon('check'), label(copied));
          setTimeout(() => {
            btn.classList.remove('copied');
            btn.replaceChildren(icon('copy'), label(copy));
          }, 1600);
        });
      });
      block.appendChild(btn);
      added.push(btn);
    });
    return () => added.forEach((b) => b.remove());
  }, [deps, copy, copied]);

  return null;
}

/** The same glyphs the rest of the chrome uses, as a detached SVG node.
 *
 * Reusing ICONS keeps the button's copy mark identical to the one in the icon
 * set; the bodies are a build-time constant from this repository. */
function icon(name: string): SVGSVGElement {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('width', '14');
  svg.setAttribute('height', '14');
  svg.setAttribute('viewBox', '0 0 24 24');
  svg.setAttribute('fill', 'none');
  svg.setAttribute('stroke', 'currentColor');
  svg.setAttribute('stroke-width', '2');
  svg.setAttribute('stroke-linecap', 'round');
  svg.setAttribute('stroke-linejoin', 'round');
  svg.innerHTML = ICONS[name] ?? '';
  return svg;
}

function label(text: string): HTMLSpanElement {
  const span = document.createElement('span');
  span.textContent = text;
  return span;
}
