/* ════════════════════════════════════════════════════════
   Leo District 306 D3 — Main JavaScript
   Intersection Observer, Counters, Quiz Timer
   ════════════════════════════════════════════════════════ */

'use strict';

// ─── Navbar scroll effect ──────────────────────────────
const navbar = document.querySelector('.navbar-district');
if (navbar) {
  const handleScroll = () => {
    navbar.classList.toggle('scrolled', window.scrollY > 40);
  };
  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();
}

// ─── Intersection Observer — Scroll Reveal ────────────
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        // Reveal children with stagger if parent has .stagger-children
        const parent = entry.target.closest('.stagger-children');
        if (parent) {
          parent.querySelectorAll('.section-reveal, .section-reveal-left').forEach(el => {
            el.classList.add('revealed');
          });
        }
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.05, rootMargin: '0px 0px -10px 0px' }
);

document.querySelectorAll('.section-reveal, .section-reveal-left').forEach(el => {
  revealObserver.observe(el);
});

// ─── Animated Counter ────────────────────────────────
function animateCounter(el) {
  const target = parseInt(el.dataset.target || el.textContent, 10);
  const suffix = el.dataset.suffix || '';
  const duration = 2000;
  const start = performance.now();

  const tick = (now) => {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    // Ease-out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(eased * target);
    el.textContent = current.toLocaleString() + suffix;
    if (progress < 1) requestAnimationFrame(tick);
  };

  requestAnimationFrame(tick);
}

const counterObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.5 }
);

document.querySelectorAll('.stat-number[data-target]').forEach(el => {
  counterObserver.observe(el);
});

// ─── Club Search & Filter ─────────────────────────────
const clubSearch = document.getElementById('club-search');
const regionFilter = document.getElementById('region-filter');
const zoneFilter = document.getElementById('zone-filter');
const typeFilter = document.getElementById('type-filter');
const clubCards = document.querySelectorAll('.club-card-wrapper');
const noResults = document.getElementById('no-results');

function filterClubs() {
  if (!clubCards.length) return;
  const q = (clubSearch ? clubSearch.value : '').toLowerCase();
  const region = regionFilter ? regionFilter.value : '';
  const zone = zoneFilter ? zoneFilter.value : '';
  const type = typeFilter ? typeFilter.value : '';
  let visible = 0;

  clubCards.forEach(card => {
    const name = (card.dataset.name || '').toLowerCase();
    const pres = (card.dataset.president || '').toLowerCase();
    const cardRegion = card.dataset.region || '';
    const cardZone = card.dataset.zone || '';
    const cardType = card.dataset.type || '';

    const matchSearch = !q || name.includes(q) || pres.includes(q);
    const matchRegion = !region || cardRegion === region;
    const matchZone = !zone || cardZone === zone;
    const matchType = !type || cardType === type;

    const show = matchSearch && matchRegion && matchZone && matchType;
    card.style.display = show ? '' : 'none';
    if (show) visible++;
  });

  if (noResults) noResults.style.display = visible === 0 ? '' : 'none';
}

if (clubSearch)  clubSearch.addEventListener('input', filterClubs);
if (regionFilter) regionFilter.addEventListener('change', filterClubs);
if (zoneFilter)  zoneFilter.addEventListener('change', filterClubs);
if (typeFilter)  typeFilter.addEventListener('change', filterClubs);

// ─── Quiz Timer ───────────────────────────────────────
const timerEl = document.getElementById('quiz-timer-display');
const quizForm = document.getElementById('quiz-form');

if (timerEl && quizForm) {
  const minutes = parseInt(timerEl.dataset.minutes || '30', 10);
  let seconds = minutes * 60;

  const pad = n => String(n).padStart(2, '0');

  const tick = () => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    timerEl.textContent = `${pad(m)}:${pad(s)}`;

    // Visual warnings
    timerEl.classList.remove('warning', 'critical');
    if (seconds <= 60)   timerEl.classList.add('critical');
    else if (seconds <= 300) timerEl.classList.add('warning');

    if (seconds <= 0) {
      clearInterval(timerInterval);
      timerEl.textContent = '00:00';
      // Auto-submit the form
      const hiddenInput = document.createElement('input');
      hiddenInput.type = 'hidden';
      hiddenInput.name = 'auto_submitted';
      hiddenInput.value = 'true';
      quizForm.appendChild(hiddenInput);
      quizForm.submit();
      return;
    }

    seconds--;
  };

  tick(); // immediate first render
  const timerInterval = setInterval(tick, 1000);
}

// ─── Calendar event tooltips ──────────────────────────
document.querySelectorAll('.cell-event').forEach(el => {
  el.title = el.dataset.title || el.textContent;
});

// ─── Smooth anchor scroll for internal links ──────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const href = a.getAttribute('href');
    // Skip bare '#' links (placeholder hrefs) — don't scroll to top
    if (href === '#') {
      e.preventDefault();
      return;
    }
    const target = document.querySelector(href);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ─── Mobile Navbar Auto-Close ─────────────────────────
const mainNav = document.getElementById('mainNav');
if (mainNav) {
  mainNav.querySelectorAll('.nav-link, #academy-nav-btn').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth < 992 && mainNav.classList.contains('show') && typeof bootstrap !== 'undefined') {
        const bsCollapse = bootstrap.Collapse.getInstance(mainNav) || new bootstrap.Collapse(mainNav, { toggle: false });
        bsCollapse.hide();
      }
    });
  });
}
