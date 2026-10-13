/**
 * INK & EQUITY — global.js v2
 * Unified: Theme · Nav · Scroll · Reveal · Court Tabs · Counters
 * Replaces all inline <script> blocks across every page
 */

(function () {
  'use strict';

  /* ================================================
     1. THEME — dark/light persistence
     ================================================ */
  const html = document.documentElement;

  function initTheme() {
    const saved = localStorage.getItem('ie-theme') || 'dark';
    html.setAttribute('data-theme', saved);
  }

  function bindThemeToggle() {
    const btn = document.getElementById('theme-toggle');
    if (!btn) return;
    btn.addEventListener('click', () => {
      const current = html.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('ie-theme', next);
      btn.setAttribute('aria-label', `Switch to ${current} mode`);
    });
  }

  /* ================================================
     2. NAVBAR — scroll state
     ================================================ */
  function initNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;
    const onScroll = () => {
      navbar.classList.toggle('scrolled', window.scrollY > 50);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // run once on load
  }

  /* ================================================
     3. MOBILE NAV — ARIA-friendly (no display toggle)
     Uses aria-hidden + visibility/opacity/transform
     ================================================ */
  function initMobileNav() {
    const hamburger = document.getElementById('hamburger');
    const mobileNav = document.getElementById('mobile-nav');
    if (!hamburger || !mobileNav) return;

    // Ensure initial ARIA state
    hamburger.setAttribute('aria-expanded', 'false');
    hamburger.setAttribute('aria-controls', 'mobile-nav');
    mobileNav.setAttribute('aria-hidden', 'true');
    mobileNav.setAttribute('role', 'navigation');
    mobileNav.setAttribute('aria-label', 'Mobile navigation');

    function toggle() {
      const isOpen = hamburger.getAttribute('aria-expanded') === 'true';
      const next = !isOpen;
      hamburger.setAttribute('aria-expanded', String(next));
      mobileNav.setAttribute('aria-hidden', String(!next));
    }

    hamburger.addEventListener('click', toggle);

    // Close on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && hamburger.getAttribute('aria-expanded') === 'true') {
        hamburger.setAttribute('aria-expanded', 'false');
        mobileNav.setAttribute('aria-hidden', 'true');
        hamburger.focus();
      }
    });

    // Close when a nav link is clicked
    mobileNav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.setAttribute('aria-expanded', 'false');
        mobileNav.setAttribute('aria-hidden', 'true');
      });
    });
  }

  /* ================================================
     4. SCROLL REVEAL — single IntersectionObserver
     ================================================ */
  function initReveal() {
    const elements = document.querySelectorAll('.reveal');
    if (!elements.length) return;

    // Respect reduced motion preference
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      elements.forEach(el => el.classList.add('revealed'));
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    );

    elements.forEach(el => observer.observe(el));
  }

  /* ================================================
     5. COUNTER ANIMATIONS
     ================================================ */
  function animateCounter(el) {
    const target = parseInt(el.dataset.count, 10);
    if (isNaN(target)) return;

    // Skip animation if reduced motion
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      el.textContent = target + '+';
      return;
    }

    const duration = 1800;
    const start = performance.now();

    const update = (now) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.floor(eased * target) + (progress < 1 ? '' : '+');
      if (progress < 1) requestAnimationFrame(update);
    };
    requestAnimationFrame(update);
  }

  function initCounters() {
    const counters = document.querySelectorAll('[data-count]');
    if (!counters.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach(el => observer.observe(el));
  }

  /* ================================================
     6. COURT TABS — WAI-ARIA tablist
     ================================================ */
  function initCourtTabs() {
    const tablist = document.querySelector('[role="tablist"]');
    if (!tablist) return;

    const tabs = tablist.querySelectorAll('[role="tab"]');
    const panels = document.querySelectorAll('[role="tabpanel"]');

    function activateTab(tab) {
      // Deactivate all
      tabs.forEach(t => {
        t.setAttribute('aria-selected', 'false');
        t.setAttribute('tabindex', '-1');
        t.classList.remove('active');
      });
      panels.forEach(p => {
        p.setAttribute('aria-hidden', 'true');
        p.classList.remove('active');
      });

      // Activate selected
      tab.setAttribute('aria-selected', 'true');
      tab.setAttribute('tabindex', '0');
      tab.classList.add('active');

      const panelId = tab.getAttribute('aria-controls');
      const panel = document.getElementById(panelId);
      if (panel) {
        panel.setAttribute('aria-hidden', 'false');
        panel.classList.add('active');
      }
    }

    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => activateTab(tab));

      // Keyboard: Arrow keys, Home, End
      tab.addEventListener('keydown', (e) => {
        let newIndex = index;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
          newIndex = (index + 1) % tabs.length;
          e.preventDefault();
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
          newIndex = (index - 1 + tabs.length) % tabs.length;
          e.preventDefault();
        } else if (e.key === 'Home') {
          newIndex = 0;
          e.preventDefault();
        } else if (e.key === 'End') {
          newIndex = tabs.length - 1;
          e.preventDefault();
        }
        if (newIndex !== index) {
          activateTab(tabs[newIndex]);
          tabs[newIndex].focus();
        }
      });
    });

    // Activate first tab on load
    if (tabs.length) activateTab(tabs[0]);
  }

  /* ================================================
     7. DISCLAIMER MODAL — first visit (localStorage persistence)
     ================================================ */
  function initDisclaimer() {
    const modal = document.getElementById('disclaimer-modal');
    if (!modal) return;

    // localStorage with graceful fallback
    function hasAccepted() {
      try { return !!localStorage.getItem('ie-disclaimer-accepted'); } catch (e) { return false; }
    }
    function markAccepted() {
      try { localStorage.setItem('ie-disclaimer-accepted', '1'); } catch (e) { /* unavailable */ }
    }

    window.closeDisclaimer = function () {
      markAccepted();
      modal.classList.remove('open');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    };

    window.openDisclaimer = function () {
      modal.classList.add('open');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      // Focus the agree button for accessibility
      const agreeBtn = modal.querySelector('#disclaimer-agree');
      if (agreeBtn) setTimeout(() => agreeBtn.focus(), 100);
    };

    // Wire agree button — closes modal + marks accepted
    const agreeBtn = document.getElementById('disclaimer-agree');
    if (agreeBtn) {
      agreeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        closeDisclaimer();
      });
    }

    // Wire X / close button — redirects to the Law Empire game
    const closeBtn = document.getElementById('disclaimer-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        window.location.href = 'law-empire-game.html';
      });
    }

    // Block overlay click — do NOT close on background click
    modal.addEventListener('click', (e) => {
      e.stopPropagation();
      // intentionally no close
    });

    // Block ESC key — modal is mandatory acceptance
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('open')) {
        e.preventDefault();
        e.stopPropagation();
      }
    });

    // Show only on first visit (localStorage persists across sessions)
    const loading = document.getElementById('loading-screen');
    const showDisclaimer = () => {
      if (!hasAccepted()) {
        setTimeout(() => openDisclaimer(), 600);
      }
    };

    if (loading) {
      loading.addEventListener('transitionend', showDisclaimer, { once: true });
    } else {
      showDisclaimer();
    }
  }

  /* ================================================
     8. LOADING SCREEN
     ================================================ */
  function initLoadingScreen() {
    const screen = document.getElementById('loading-screen');
    if (!screen) return;
    window.addEventListener('load', () => {
      setTimeout(() => screen.classList.add('hidden'), 2200);
    });
  }

  /* ================================================
     9. NEWSLETTER
     ================================================ */
  function initNewsletter() {
    const form = document.querySelector('.newsletter-form');
    if (!form) return;
    const btn = form.querySelector('button');
    const input = form.querySelector('input[type="email"]');
    if (!btn || !input) return;

    btn.addEventListener('click', () => {
      if (input.value && input.checkValidity()) {
        input.value = '';
        input.placeholder = "Thank you — you're subscribed.";
        input.style.color = 'var(--accent-sapphire-bright)';
        btn.textContent = '✓';
        btn.style.background = '#4ade80';
        btn.disabled = true;
      } else {
        input.focus();
      }
    });
  }

  /* ================================================
     10. COURTS QUICKNAV (courts.html)
     ================================================ */
  function initCourtsQuicknav() {
    const qnavBtns = document.querySelectorAll('.qnav-btn');
    if (!qnavBtns.length) return;

    // Click
    qnavBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetId = btn.dataset.target;
        if (!targetId) return;
        const target = document.getElementById(targetId);
        if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        qnavBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
      });
    });

    // Scroll spy
    const sections = Array.from(qnavBtns)
      .map(btn => document.getElementById(btn.dataset.target))
      .filter(Boolean);

    window.addEventListener('scroll', () => {
      let current = sections[0]?.id;
      sections.forEach(sec => {
        if (sec.getBoundingClientRect().top < window.innerHeight * 0.5) {
          current = sec.id;
        }
      });
      qnavBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.target === current);
      });
    }, { passive: true });
  }

  /* ================================================
     11. FILTER BUTTONS (insights.html)
     ================================================ */
  function initFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    if (!filterBtns.length) return;

    // Filterable items: featured article + article cards
    const filterableItems = document.querySelectorAll('[data-tag]');

    filterBtns.forEach(btn => {
      // Accessibility
      btn.setAttribute('role', 'button');
      const isAll = btn.classList.contains('active');
      btn.setAttribute('aria-pressed', isAll ? 'true' : 'false');

      // Keyboard support
      btn.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); btn.click(); }
      });

      btn.addEventListener('click', () => {
        // Update active + aria states
        filterBtns.forEach(b => {
          b.classList.remove('active');
          b.setAttribute('aria-pressed', 'false');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');

        const selected = (btn.dataset.filterTag || 'all').toLowerCase();

        // Show/hide filterable items
        filterableItems.forEach(item => {
          if (selected === 'all') {
            item.style.display = '';
            item.removeAttribute('aria-hidden');
          } else {
            const tags = (item.dataset.tag || '').toLowerCase().split(' ');
            const visible = tags.includes(selected);
            item.style.display = visible ? '' : 'none';
            item.setAttribute('aria-hidden', visible ? 'false' : 'true');
          }
        });
      });
    });
  }

  /* ================================================
     INIT — run all on DOMContentLoaded
     ================================================ */
  document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    bindThemeToggle();
    initNavbar();
    initMobileNav();
    initReveal();
    initCounters();
    initCourtTabs();
    initDisclaimer();
    initLoadingScreen();
    initNewsletter();
    initCourtsQuicknav();
    initFilters();
  });

  // Theme must apply before paint — re-run synchronously
  initTheme();

})();
