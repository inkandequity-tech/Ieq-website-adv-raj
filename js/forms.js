/**
 * INK & EQUITY — forms.js v2
 * Stateful multi-step forms: Booking (contact.html) + Application (careers.html)
 * Includes: HTML5 validation · Error display · State management · Success screens
 */

(function () {
  'use strict';

  /* ================================================
     SHARED UTILITIES
     ================================================ */

  /**
   * Validate a single field and show/hide error
   * Returns true if valid
   */
  function validateField(field) {
    const group = field.closest('.form-group');
    if (!group) return true;

    const errorEl = group.querySelector('.form-error');
    const isValid = field.checkValidity();

    group.classList.toggle('has-error', !isValid);
    field.classList.toggle('is-invalid', !isValid);
    field.classList.toggle('is-valid', isValid);

    if (errorEl) {
      errorEl.textContent = field.validationMessage || 'This field is required.';
    }
    return isValid;
  }

  /**
   * Validate all required fields in a given container
   * Returns true if all valid
   */
  function validateContainer(container) {
    const fields = container.querySelectorAll('input[required], select[required], textarea[required]');
    let allValid = true;
    fields.forEach(field => {
      if (!validateField(field)) allValid = false;
    });
    if (!allValid) {
      // Focus first invalid field
      const first = container.querySelector('.has-error input, .has-error select, .has-error textarea');
      if (first) first.focus();
    }
    return allValid;
  }

  /**
   * Bind live validation to all fields in a container
   */
  function bindLiveValidation(container) {
    const fields = container.querySelectorAll('input, select, textarea');
    fields.forEach(field => {
      field.addEventListener('blur', () => validateField(field));
      field.addEventListener('input', () => {
        if (field.classList.contains('is-invalid')) validateField(field);
      });
    });
  }

  /* ================================================
     BOOKING FORM (contact.html)
     ================================================ */

  function initBookingForm() {
    const form = document.querySelector('.booking-form');
    if (!form) return;

    let currentStep = 1;
    const totalSteps = 3;

    const steps = {
      panels: () => Array.from({ length: totalSteps }, (_, i) => document.getElementById(`bs${i + 1}`)),
      progress: () => Array.from({ length: totalSteps }, (_, i) => document.getElementById(`ps${i + 1}`)),
    };

    // Bind live validation to step panels
    steps.panels().forEach(panel => {
      if (panel) bindLiveValidation(panel);
    });

    function showStep(step) {
      const panels = steps.panels();
      const progressSteps = steps.progress();

      panels.forEach((panel, i) => {
        if (!panel) return;
        panel.style.display = i + 1 === step ? 'block' : 'none';
      });

      progressSteps.forEach((ps, i) => {
        if (!ps) return;
        ps.classList.remove('active', 'done');
        if (i + 1 === step) ps.classList.add('active');
        if (i + 1 < step)  ps.classList.add('done');
      });

      // Update step number label
      const stepNum = document.getElementById('step-number');
      if (stepNum) stepNum.textContent = step;

      currentStep = step;
      form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function goNext() {
      const currentPanel = document.getElementById(`bs${currentStep}`);
      if (!currentPanel) return;

      // Step 1: require matter selection
      if (currentStep === 1) {
        const selected = currentPanel.querySelector('.matter-option.selected');
        if (!selected) {
          // Show inline error
          let errEl = currentPanel.querySelector('.matter-required-error');
          if (!errEl) {
            errEl = document.createElement('p');
            errEl.className = 'matter-required-error';
            errEl.style.cssText = 'color:var(--color-error,#ef4444);font-size:var(--text-sm);margin-top:var(--space-3);';
            errEl.textContent = 'Please select a matter type to continue.';
            const grid = currentPanel.querySelector('.matter-grid');
            if (grid) grid.after(errEl);
          }
          errEl.style.display = 'block';
          return;
        }
        // Clear error if present
        const errEl = currentPanel.querySelector('.matter-required-error');
        if (errEl) errEl.style.display = 'none';
      }

      // Step 3: validate contact fields
      if (currentStep === 3) {
        if (!validateContainer(currentPanel)) return;
      }

      if (currentStep < totalSteps) showStep(currentStep + 1);
    }

    function goBack() {
      if (currentStep > 1) showStep(currentStep - 1);
    }

    function submitBooking() {
      const currentPanel = document.getElementById(`bs${currentStep}`);
      if (!validateContainer(currentPanel)) return;

      // Hide all panels + mark all done
      steps.panels().forEach(p => { if (p) p.style.display = 'none'; });
      steps.progress().forEach(ps => {
        if (!ps) return;
        ps.classList.remove('active');
        ps.classList.add('done');
      });

      const success = document.getElementById('booking-success');
      if (success) success.style.display = 'block';
      form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Wire up matter selection cards
    form.querySelectorAll('.matter-option').forEach(card => {
      card.addEventListener('click', () => {
        form.querySelectorAll('.matter-option').forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
      });
      // Keyboard support
      card.setAttribute('role', 'radio');
      card.setAttribute('tabindex', '0');
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          card.click();
        }
      });
    });

    // Wire up court selection
    form.querySelectorAll('.court-option').forEach(option => {
      option.addEventListener('click', () => {
        form.querySelectorAll('.court-option').forEach(o => o.classList.remove('selected'));
        option.classList.add('selected');
      });
      option.setAttribute('role', 'radio');
      option.setAttribute('tabindex', '0');
      option.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          option.click();
        }
      });
    });

    // Wire up navigation buttons
    const nextBtns = form.querySelectorAll('[data-booking-next]');
    const backBtns = form.querySelectorAll('[data-booking-back]');
    const submitBtn = form.querySelector('[data-booking-submit]');

    nextBtns.forEach(btn => btn.addEventListener('click', goNext));
    backBtns.forEach(btn => btn.addEventListener('click', goBack));
    if (submitBtn) submitBtn.addEventListener('click', submitBooking);

    // Initialise
    showStep(1);
  }

  /* ================================================
     CAREERS APPLICATION FORM (careers.html)
     ================================================ */

  function initCareersForm() {
    const form = document.querySelector('.apply-form');
    if (!form) return;

    let currentStep = 1;
    const totalSteps = 3;

    function getPanel(step) { return document.getElementById(`form-step-${step}`); }
    function getDot(step)   { return document.getElementById(`step${step}`); }

    // Bind live validation
    for (let i = 1; i <= totalSteps; i++) {
      const panel = getPanel(i);
      if (panel) bindLiveValidation(panel);
    }

    function showStep(step) {
      for (let i = 1; i <= totalSteps; i++) {
        const panel = getPanel(i);
        const dot   = getDot(i);
        if (panel) panel.style.display = i === step ? 'block' : 'none';
        if (dot) {
          dot.classList.remove('active', 'done');
          if (i === step) dot.classList.add('active');
          if (i < step)   dot.classList.add('done');
        }
      }

      const stepNum = form.querySelector('#step-number');
      if (stepNum) stepNum.textContent = step;

      currentStep = step;
    }

    function goNext() {
      const currentPanel = getPanel(currentStep);
      if (!currentPanel) return;
      if (!validateContainer(currentPanel)) return;
      if (currentStep < totalSteps) showStep(currentStep + 1);
    }

    function goBack() {
      if (currentStep > 1) showStep(currentStep - 1);
    }

    function submitApp() {
      const currentPanel = getPanel(currentStep);
      if (!validateContainer(currentPanel)) return;

      for (let i = 1; i <= totalSteps; i++) {
        const panel = getPanel(i);
        const dot   = getDot(i);
        if (panel) panel.style.display = 'none';
        if (dot) { dot.classList.remove('active'); dot.classList.add('done'); }
      }

      const success = document.getElementById('form-success');
      if (success) success.style.display = 'block';
    }

    // Wire navigation buttons
    const nextBtns = form.querySelectorAll('[data-form-next]');
    const backBtns = form.querySelectorAll('[data-form-back]');
    const submitBtn = form.querySelector('[data-form-submit]');

    nextBtns.forEach(btn => btn.addEventListener('click', goNext));
    backBtns.forEach(btn => btn.addEventListener('click', goBack));
    if (submitBtn) submitBtn.addEventListener('click', submitApp);

    // Initialise
    showStep(1);
  }

  /* ================================================
     PRACTICE AREAS MODAL (practice-areas.html)
     ================================================ */

  function initPracticeModal() {
    const modal = document.getElementById('pa-modal');
    if (!modal) return;

    window.openPaModal = function (id) {
      if (!window.practiceAreas) return;
      const pa = window.practiceAreas.find(p => p.id === id);
      if (!pa) return;

      document.getElementById('modal-title').textContent = pa.title;
      document.getElementById('modal-subtitle').textContent = pa.subtitle;
      document.getElementById('modal-body').innerHTML = pa.details;

      modal.classList.add('open');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';

      // Focus close button
      const closeBtn = modal.querySelector('.modal__close');
      if (closeBtn) setTimeout(() => closeBtn.focus(), 50);
    };

    window.closePaModal = function () {
      modal.classList.remove('open');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    };

    modal.addEventListener('click', (e) => {
      if (e.target === modal) closePaModal();
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('open')) closePaModal();
    });
  }

  /* ================================================
     INIT
     ================================================ */
  document.addEventListener('DOMContentLoaded', () => {
    initBookingForm();
    initCareersForm();
    initPracticeModal();
  });

})();
