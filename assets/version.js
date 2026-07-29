// Keeps the platform version shown on the site in sync with the newest vX.Y.Z
// tag on hinata-app — without waiting for the next docs deploy.
//
// build.py bakes the version it saw at build time into every page (the hero
// pill, `{{version}}` in prose and in code snippets). That value goes stale the
// moment the app ships a release, so here we ask the GitHub API for the current
// tag and patch the page:
//   * elements carrying data-app-version get their text replaced,
//   * every remaining occurrence of the baked version in the page text is
//     rewritten, which covers the snippets (HINATA_APP_TAG=…) we cannot mark up
//     because they are inside highlighted <pre> blocks.
// The answer is cached in localStorage so a reader costs one API call per TTL,
// and any failure simply leaves the built-in value in place.
(function () {
  var meta = document.querySelector('meta[name="hinata:app-version"]');
  if (!meta) return;

  var built = meta.getAttribute('content');
  var repo = meta.getAttribute('data-repo') || 'hinata-platform/hinata-app';
  var CACHE_KEY = 'hinata-app-version';
  var TTL = 6 * 60 * 60 * 1000; // 6 h

  function parse(name) {
    var m = /^v(\d+)\.(\d+)\.(\d+)$/.exec(name || '');
    return m ? [+m[1], +m[2], +m[3]] : null;
  }

  function highest(tags) {
    var best = null;
    for (var i = 0; i < tags.length; i++) {
      var v = parse(tags[i] && tags[i].name);
      if (!v) continue;
      if (!best || v[0] > best[0] ||
          (v[0] === best[0] && (v[1] > best[1] ||
          (v[1] === best[1] && v[2] > best[2])))) best = v;
    }
    return best ? best.join('.') : null;
  }

  function replaceInText(from, to) {
    var escaped = '\\b' + from.replace(/\./g, '\\.') + '\\b';
    var pattern = new RegExp(escaped, 'g');
    var probe = new RegExp(escaped); // separate, non-global: .test() is stateful with /g
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        var tag = node.parentNode && node.parentNode.nodeName;
        if (tag === 'SCRIPT' || tag === 'STYLE') return NodeFilter.FILTER_REJECT;
        return probe.test(node.nodeValue)
          ? NodeFilter.FILTER_ACCEPT
          : NodeFilter.FILTER_REJECT;
      },
    });
    var hits = [];
    while (walker.nextNode()) hits.push(walker.currentNode);
    for (var i = 0; i < hits.length; i++) {
      hits[i].nodeValue = hits[i].nodeValue.replace(pattern, to);
    }
  }

  function apply(version) {
    if (!version || version === built) return;
    var pills = document.querySelectorAll('[data-app-version]');
    for (var i = 0; i < pills.length; i++) {
      var prefix = pills[i].textContent.charAt(0) === 'v' ? 'v' : '';
      pills[i].textContent = prefix + version;
    }
    if (built) replaceInText(built, version);
    meta.setAttribute('content', version);
    built = version;
  }

  function cached() {
    try {
      var raw = localStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      var entry = JSON.parse(raw);
      if (!entry || !parse('v' + entry.v)) return null;
      return { version: entry.v, fresh: Date.now() - entry.t < TTL };
    } catch (e) {
      return null;
    }
  }

  function store(version) {
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify({ v: version, t: Date.now() }));
    } catch (e) { /* private mode — just skip the cache */ }
  }

  var hit = cached();
  if (hit) apply(hit.version);
  if (hit && hit.fresh) return;

  fetch('https://api.github.com/repos/' + repo + '/tags?per_page=100', {
    headers: { Accept: 'application/vnd.github+json' },
  })
    .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
    .then(function (tags) {
      var version = highest(tags || []);
      if (!version) return;
      store(version);
      apply(version);
    })
    .catch(function () { /* offline or rate-limited — the built value stands */ });
})();
