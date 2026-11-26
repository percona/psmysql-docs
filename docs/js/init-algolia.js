/**
 * Algolia search for the Percona Server for MySQL documentation.
 *
 * Same search as on the docs home page (docs-home repository), set up for
 * this doc set. Looks and works like the search on www.percona.com:
 * - a search icon in the header that expands into a search field,
 * - a results popup with a "See all N results" button,
 * - a full results page (search-results.md).
 *
 * Only Percona Server for MySQL pages are shown (ALGOLIA_CONFIG.urlPrefix).
 * When a page exists in several versions, results link to this doc set's
 * version (ALGOLIA_CONFIG.preferredVersion) and list the other versions.
 */
(() => {
  'use strict';

  /* ---------- Configuration ---------- */

  const ALGOLIA_CONFIG = {
    appId: 'QPF6EL892Z',
    apiKey: '72ae01e59f74373372979e09001708fb',
    indexName: 'percona_docs_pages',
    urlPrefix: 'https://docs.percona.com/percona-server/',
    scopeLabel: 'Percona Server for MySQL',
    placeholder: 'Search documentation...',
    // Relative to this doc set's root, e.g. /percona-server/8.0/
    resultsPage: 'search-results.html',
    // Version of this doc set: results link to it when the page exists there
    preferredVersion: '9.7',
    popupResults: 10,
    resultsPerPage: 20,
  };

  // Abbreviations people search for, mapped to the product name used at the
  // end of page titles ("Page title - Product name").
  const PRODUCT_ABBREVIATIONS = {
    pxb: 'Percona XtraBackup',
    pxc: 'Percona XtraDB Cluster',
    psmdb: 'Percona Server for MongoDB',
    pbm: 'Percona Backup for MongoDB',
    pmm: 'Percona Monitoring and Management',
    pt: 'Percona Toolkit',
  };

  const SEARCH_ENDPOINT =
    `https://${ALGOLIA_CONFIG.appId}-dsn.algolia.net/1/indexes/` +
    `${encodeURIComponent(ALGOLIA_CONFIG.indexName)}/query`;

  // Up to 1,000 records per search (about 30 KB compressed): enough to group
  // versions of the same page and count unique pages.
  const MAX_HITS = 1000;
  const DEBOUNCE_MS = 200;
  const SEARCH_LABEL = ALGOLIA_CONFIG.placeholder.replace(/\.+$/, '');

  const SEARCH_ICON =
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<circle cx="11" cy="11" r="7"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>';

  /* ---------- Helpers ---------- */

  function createElement(tag, className, text) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  }

  // Results and "See all N results" open in a new tab, so the search stays
  // open in the current one.
  function openInNewTab(link) {
    link.target = '_blank';
    link.rel = 'noopener';
  }

  function plural(count) {
    return `${count} result${count === 1 ? '' : 's'}`;
  }

  // Root of this doc set, e.g. https://docs.percona.com/percona-server/8.0/.
  // Material for MkDocs publishes it, relative to the page, as config.base.
  function siteRoot() {
    try {
      const config = JSON.parse(document.getElementById('__config').textContent);
      return new URL(`${config.base}/`, window.location.href);
    } catch {
      return new URL('./', window.location.href);
    }
  }

  const RESULTS_PAGE = new URL(ALGOLIA_CONFIG.resultsPage, siteRoot()).pathname;

  function resultsPageUrl(query, page) {
    const params = new URLSearchParams({ q: query });
    if (page > 0) params.set('p', String(page + 1));
    return `${RESULTS_PAGE}?${params}`;
  }

  // Replaces known abbreviations (pxb, pmm, ...) with the product name and
  // returns that product, so its pages can be ranked first.
  function expandQuery(query) {
    let product = null;
    const expanded = (query || '')
      .split(/\s+/)
      .map((word) => {
        const fullName = PRODUCT_ABBREVIATIONS[word.toLowerCase()];
        if (!fullName) return word;
        product = fullName;
        return fullName;
      })
      .join(' ');
    return { expanded, product };
  }

  // "Page title - Product name" -> "Product name"
  function productOf(title) {
    const i = (title || '').lastIndexOf(' - ');
    return i > 0 ? title.slice(i + 3) : '';
  }

  function isInScope(hit) {
    return Boolean(hit.url) && hit.url.startsWith(ALGOLIA_CONFIG.urlPrefix);
  }

  // Version segment of a docs URL: .../percona-server/8.4/... -> "8.4"
  function versionOf(url) {
    const path = url.replace(ALGOLIA_CONFIG.urlPrefix, '');
    return path.split('/').find((part) => /^\d+(\.\d+)*(\.x)?$/.test(part)) || '';
  }

  function compareVersionsDesc(a, b) {
    const pa = a.split('.').map((n) => parseInt(n, 10) || 0);
    const pb = b.split('.').map((n) => parseInt(n, 10) || 0);
    for (let i = 0; i < Math.max(pa.length, pb.length); i += 1) {
      const diff = (pb[i] || 0) - (pa[i] || 0);
      if (diff) return diff;
    }
    return 0;
  }

  /* ---------- Search ---------- */

  // The index has one record per page per product version, so the same page
  // appears several times (9.7, 8.4, 8.0, ...). Group them into one result
  // that links to this doc set's version (or the newest one if the page
  // doesn't exist here) and lists all versions, newest first.
  function groupVersions(hits) {
    const groups = new Map();
    hits.forEach((hit) => {
      const key = (hit.title || hit.url).trim().toLowerCase();
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(hit);
    });

    return [...groups.values()].map((group) => {
      const sorted = [...group].sort((a, b) =>
        compareVersionsDesc(versionOf(a.url), versionOf(b.url))
      );
      const main =
        sorted.find((hit) => versionOf(hit.url) === ALGOLIA_CONFIG.preferredVersion) || sorted[0];
      const versions = sorted
        .map((hit) => ({ version: versionOf(hit.url), url: hit.url, isMain: hit === main }))
        .filter((item) => item.version);
      return { ...main, versions: versions.length > 1 ? versions : [] };
    });
  }

  async function searchDocs(query) {
    const { expanded, product } = expandQuery(query);

    const response = await fetch(SEARCH_ENDPOINT, {
      method: 'POST',
      headers: {
        'X-Algolia-Application-Id': ALGOLIA_CONFIG.appId,
        'X-Algolia-API-Key': ALGOLIA_CONFIG.apiKey,
      },
      body: JSON.stringify({
        query: expanded,
        hitsPerPage: MAX_HITS,
        attributesToRetrieve: ['title', 'url', 'image'],
        attributesToHighlight: ['title'],
        attributesToSnippet: ['description:30'],
        highlightPreTag: '<mark>',
        highlightPostTag: '</mark>',
      }),
    });
    if (!response.ok) throw new Error(`Algolia returned ${response.status}`);

    const data = await response.json();
    let results = groupVersions(data.hits.filter(isInScope));
    if (product) {
      results = [
        ...results.filter((hit) => productOf(hit.title) === product),
        ...results.filter((hit) => productOf(hit.title) !== product),
      ];
    }
    return { results, total: results.length };
  }

  /* ---------- Result cards (same markup as www.percona.com) ---------- */

  function renderVersions(versions) {
    const row = createElement('div', 'hit-versions');
    row.append('Versions: ');
    versions.forEach(({ version, url, isMain }) => {
      // Highlighted: the version the result itself links to
      const link = createElement('a', isMain ? 'latest' : '', version);
      link.href = url;
      openInNewTab(link);
      row.append(link);
    });
    return row;
  }

  function renderHit(hit) {
    const item = createElement('li', 'ais-Hits-item');
    const link = createElement('a', 'hit-link');
    link.href = hit.url;
    openInNewTab(link);

    if (hit.image) {
      const imageWrap = createElement('div', 'c_img');
      const image = createElement('img');
      image.src = hit.image;
      image.alt = '';
      image.loading = 'lazy';
      image.addEventListener('error', () => imageWrap.remove());
      imageWrap.append(image);
      link.append(imageWrap);
    }

    // Algolia escapes the record text; only its <mark> highlight tags are HTML.
    const title = createElement('div', 'row1');
    title.innerHTML = hit._highlightResult?.title?.value || hit.title || hit.url;

    const description = createElement('div', 'c_desc');
    description.innerHTML = hit._snippetResult?.description?.value || '';

    const body = createElement('div', 'c_body');
    body.append(title, description);
    link.append(body);
    item.append(link);

    if (hit.versions.length) item.append(renderVersions(hit.versions));
    return item;
  }

  function renderHitList(hits) {
    const list = createElement('ol', 'ais-Hits-list');
    hits.forEach((hit) => list.append(renderHit(hit)));
    const wrap = createElement('div', 'ais-Hits');
    wrap.append(list);
    return wrap;
  }

  /* ---------- Header search: icon, search field and popup ---------- */

  function initHeaderSearch() {
    const container = document.getElementById('docsearch');
    if (!container) return;

    const root = createElement('div', 'topbar-search');
    root.innerHTML = `
      <button type="button" class="search-icon-btn" aria-label="Open search">${SEARCH_ICON}</button>
      <div class="search-input-wrap">
        <form class="ais-SearchBox-form" role="search" novalidate>
          <input class="ais-SearchBox-input" type="search" name="q"
            autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" maxlength="512"
            role="combobox" aria-expanded="false" aria-controls="search-popup" aria-autocomplete="list">
        </form>
        <button type="button" class="search-collapse-btn" aria-label="Close search">×</button>
      </div>
      <div class="sr-only" aria-live="polite"></div>
      <div id="search-popup" class="search-popup" role="region" aria-label="Search suggestions">
        <div class="results active" role="tabpanel"><div class="hits"></div></div>
        <div class="popup-footer">
          <span class="popup-summary"></span>
          <a class="see-all-link" href="#"></a>
        </div>
      </div>`;
    container.prepend(root);

    const iconButton = root.querySelector('.search-icon-btn');
    const inputWrap = root.querySelector('.search-input-wrap');
    const form = root.querySelector('form');
    const input = root.querySelector('.ais-SearchBox-input');
    const closeButton = root.querySelector('.search-collapse-btn');
    const liveRegion = root.querySelector('[aria-live]');
    const popup = root.querySelector('.search-popup');
    const resultsPanel = root.querySelector('.results');
    const hitsContainer = root.querySelector('.hits');
    const summary = root.querySelector('.popup-summary');
    const seeAll = root.querySelector('.see-all-link');

    input.placeholder = ALGOLIA_CONFIG.placeholder;
    input.setAttribute('aria-label', SEARCH_LABEL);
    openInNewTab(seeAll);

    let lastQuery = '';
    let requestId = 0;
    let debounceTimer = null;
    let activeIndex = -1;

    const isExpanded = () => root.classList.contains('expanded');
    const isPopupOpen = () => popup.classList.contains('open');
    const resultLinks = () => [...hitsContainer.querySelectorAll('.hit-link')];

    // Below 1560px the field and popup open as floating panels under the
    // header; CSS positions them with these variables.
    function updatePositions() {
      const header = document.querySelector('.md-header') || container;
      const headerBottom = header.getBoundingClientRect().bottom;
      root.style.setProperty('--search-drop-top', `${headerBottom + 8}px`);
      const wrapBottom = inputWrap.getBoundingClientRect().bottom;
      root.style.setProperty('--search-popup-top', `${wrapBottom + 8}px`);

      // Bottom of the part of the screen the reader can see. On phones the
      // on-screen keyboard covers the lower part of the page, so the popup
      // ends above it and its "See all" footer stays visible.
      const viewport = window.visualViewport;
      const visibleBottom = viewport ? viewport.offsetTop + viewport.height : window.innerHeight;
      root.style.setProperty('--search-visible-bottom', `${visibleBottom}px`);
    }

    function setActive(index) {
      const links = resultLinks();
      links.forEach((link) => link.classList.remove('is-active'));
      activeIndex = index;
      if (index >= 0 && links[index]) {
        links[index].classList.add('is-active');
        links[index].scrollIntoView({ block: 'nearest' });
      }
    }

    function openPopup() {
      updatePositions();
      popup.classList.add('open');
      input.setAttribute('aria-expanded', 'true');
    }

    function closePopup() {
      popup.classList.remove('open');
      input.setAttribute('aria-expanded', 'false');
      setActive(-1);
    }

    function expand() {
      if (isExpanded()) {
        input.focus();
        return;
      }
      root.classList.add('expanded');
      updatePositions();
      input.focus();
      if (input.value.trim()) openPopup();
    }

    function collapse() {
      closePopup();
      root.classList.remove('expanded');
      iconButton.focus();
    }

    function showResults(query, { results, total }) {
      const hits = results.slice(0, ALGOLIA_CONFIG.popupResults);

      hitsContainer.replaceChildren();
      resultsPanel.classList.toggle('no-results', hits.length === 0);
      if (hits.length) hitsContainer.append(renderHitList(hits));
      resultsPanel.scrollTop = 0;
      activeIndex = -1;

      summary.textContent = `${plural(total)} in ${ALGOLIA_CONFIG.scopeLabel}`;
      seeAll.textContent = `See all ${plural(total)} →`;
      seeAll.href = resultsPageUrl(query, 0);
      seeAll.hidden = total === 0;
      liveRegion.textContent = `${plural(total)} in ${ALGOLIA_CONFIG.scopeLabel}.`;
    }

    function showError() {
      hitsContainer.replaceChildren();
      resultsPanel.classList.add('no-results');
      summary.textContent = 'Search is not available right now.';
      seeAll.hidden = true;
    }

    async function runSearch(query) {
      const id = ++requestId;
      try {
        const data = await searchDocs(query);
        if (id !== requestId) return; // a newer search has started
        showResults(query, data);
      } catch (error) {
        if (id !== requestId) return;
        showError();
        console.error(error);
      }
      openPopup();
    }

    input.addEventListener('input', () => {
      const query = input.value.trim();
      clearTimeout(debounceTimer);
      if (!query) {
        lastQuery = '';
        requestId++;
        closePopup();
        return;
      }
      debounceTimer = setTimeout(() => {
        if (query === lastQuery && isPopupOpen()) return;
        lastQuery = query;
        runSearch(query);
      }, DEBOUNCE_MS);
    });

    input.addEventListener('focus', () => {
      if (input.value.trim() && hitsContainer.childElementCount) openPopup();
    });

    input.addEventListener('keydown', (event) => {
      const links = resultLinks();
      if (event.key === 'ArrowDown' && links.length) {
        event.preventDefault();
        if (!isPopupOpen()) openPopup();
        setActive(Math.min(activeIndex + 1, links.length - 1));
      } else if (event.key === 'ArrowUp' && links.length) {
        event.preventDefault();
        setActive(Math.max(activeIndex - 1, -1));
      } else if (event.key === 'Escape') {
        event.preventDefault();
        if (isPopupOpen()) closePopup();
        else collapse();
      }
    });

    // Enter opens the highlighted result in a new tab, or the full results
    // page in this tab.
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const links = resultLinks();
      if (activeIndex >= 0 && links[activeIndex]) {
        window.open(links[activeIndex].href, '_blank', 'noopener');
        return;
      }
      const query = input.value.trim();
      if (query) window.location.href = resultsPageUrl(query, 0);
    });

    iconButton.addEventListener('click', (event) => {
      event.stopPropagation();
      if (isExpanded()) input.focus();
      else expand();
    });

    closeButton.addEventListener('click', (event) => {
      event.stopPropagation();
      input.value = '';
      lastQuery = '';
      requestId++;
      hitsContainer.replaceChildren();
      collapse();
    });

    document.addEventListener('click', (event) => {
      if (!root.contains(event.target)) closePopup();
    });

    // Cmd+K / Ctrl+K opens the search.
    document.addEventListener('keydown', (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault();
        expand();
      }
    });

    const repositionIfExpanded = () => {
      if (isExpanded()) updatePositions();
    };
    window.addEventListener('resize', repositionIfExpanded);
    window.addEventListener('scroll', repositionIfExpanded, { passive: true });
    // Fires when the on-screen keyboard opens or closes
    window.visualViewport?.addEventListener('resize', repositionIfExpanded);
    window.visualViewport?.addEventListener('scroll', repositionIfExpanded);
  }

  /* ---------- Full results page ---------- */

  function renderPagination(query, page, pageCount) {
    const nav = createElement('nav', 'search-page-pagination');
    nav.setAttribute('aria-label', 'Search results pages');
    if (pageCount <= 1) return nav;

    const addPage = (label, target, isCurrent) => {
      if (isCurrent) {
        const current = createElement('span', 'page current', label);
        current.setAttribute('aria-current', 'page');
        nav.append(current);
        return;
      }
      const link = createElement('a', 'page', label);
      link.href = resultsPageUrl(query, target);
      nav.append(link);
    };

    if (page > 0) addPage('← Previous', page - 1, false);

    // Up to five numbered pages around the current one
    const first = Math.max(0, Math.min(page - 2, pageCount - 5));
    const last = Math.min(pageCount - 1, first + 4);
    for (let p = first; p <= last; p += 1) addPage(String(p + 1), p, p === page);

    if (page < pageCount - 1) addPage('Next →', page + 1, false);
    return nav;
  }

  async function initResultsPage() {
    const container = document.getElementById('algolia-results');
    if (!container) return;

    const params = new URLSearchParams(window.location.search);
    const query = (params.get('q') || '').trim();
    const page = Math.max(0, (parseInt(params.get('p'), 10) || 1) - 1);

    container.classList.add('search-page');

    // Page heading and browser tab title include the search term.
    if (query) {
      const heading = document.querySelector('.md-content h1');
      if (heading) heading.textContent = `Search results for “${query}”`;
      document.title = document.title.replace('Search results', `Search results for “${query}”`);
    }

    container.innerHTML = `
      <form class="search-page-form" role="search" action="${RESULTS_PAGE}" method="get">
        <input class="ais-SearchBox-input" type="search" name="q"
          autocomplete="off" spellcheck="false" maxlength="512">
        <button type="submit" class="search-page-submit">Search</button>
      </form>
      <p class="search-page-summary" aria-live="polite"></p>
      <div class="search-page-results"></div>`;

    const input = container.querySelector('input');
    const status = container.querySelector('.search-page-summary');
    const resultsContainer = container.querySelector('.search-page-results');

    input.value = query;
    input.placeholder = ALGOLIA_CONFIG.placeholder;
    input.setAttribute('aria-label', SEARCH_LABEL);

    if (!query) {
      status.textContent = 'Type a search term to see results.';
      input.focus();
      return;
    }

    status.textContent = 'Searching…';

    try {
      const { results, total } = await searchDocs(query);
      const perPage = ALGOLIA_CONFIG.resultsPerPage;
      const pageCount = Math.ceil(total / perPage);

      // A page number past the end (for example, an old link) shows the last
      // page, and the address bar is corrected to match.
      const currentPage = Math.min(page, Math.max(pageCount - 1, 0));
      if (currentPage !== page) {
        window.history.replaceState(null, '', resultsPageUrl(query, currentPage));
      }
      const pageResults = results.slice(currentPage * perPage, (currentPage + 1) * perPage);

      status.textContent = `${plural(total)} for “${query}” in ${ALGOLIA_CONFIG.scopeLabel}`;

      if (!pageResults.length) {
        resultsContainer.classList.add('no-results');
        return;
      }
      resultsContainer.append(renderHitList(pageResults), renderPagination(query, currentPage, pageCount));
    } catch (error) {
      status.textContent = 'Search is not available right now. Please try again later.';
      console.error(error);
    }
  }

  initHeaderSearch();
  initResultsPage();
})();
