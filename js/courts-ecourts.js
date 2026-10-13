/* ============================================
   ECOURTS WORKFLOW — MODAL & FORM LOGIC
   Service workflow navigation and validation
   ============================================ */

let currentService = null;
let currentStep = 1;
let formState = {
  state: '',
  district: '',
  courts: [],
  filters: {}
};

// SERVICE CARD INITIALIZATION
function initiateService(serviceType) {
  currentService = serviceType;
  currentStep = 1;
  formState = { state: '', district: '', courts: [], filters: {} };
  
  // Show modal
  const modal = document.getElementById('service-modal');
  if (modal) {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    
    // Reset forms
    document.getElementById('state-select').value = '';
    document.getElementById('district-select').innerHTML = '<option value="">-- Select District --</option>';
    document.getElementById('court-checkboxes').innerHTML = '';
    document.getElementById('service-filters').innerHTML = '';
    
    // Show step 1
    showStep(1);
    
    // Log for debugging
    console.log('Service initiated:', serviceType);
  }
}

// CLOSE MODAL
function closeServiceModal() {
  const modal = document.getElementById('service-modal');
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
    currentService = null;
    currentStep = 1;
  }
}

// CLOSE MODAL ON BACKDROP CLICK - Already handled in HTML onclick
document.addEventListener('DOMContentLoaded', function() {
  const backdrop = document.querySelector('.modal-backdrop');
  if (backdrop) {
    backdrop.addEventListener('click', closeServiceModal);
  }
});

// SHOW SPECIFIC STEP
function showStep(step) {
  // Hide all steps
  document.querySelectorAll('.workflow-step').forEach(el => {
    el.classList.remove('active');
  });
  
  // Show current step
  const stepElement = document.getElementById(`step-${step}-${['state', 'district', 'court', 'filters'][step-1]}`);
  if (stepElement) {
    stepElement.classList.add('active');
    currentStep = step;
    
    // Scroll to top of modal
    const modalContent = document.querySelector('.modal-content');
    if (modalContent) {
      modalContent.scrollTop = 0;
    }
  }
}

// NAVIGATE TO STEP (single canonical definition)
function goToStep(step, event) {
  if (event) {
    event.preventDefault();
  }

  // Validation for step transitions
  if (step === 2 && !document.getElementById('state-select').value) {
    showFieldError('state-select', 'Please select a state');
    return;
  }

  if (step === 3 && !document.getElementById('district-select').value) {
    showFieldError('district-select', 'Please select a district');
    return;
  }

  // When moving to step 4, render service-specific filters
  if (step === 4) {
    renderServiceFilters();
  }

  showStep(step);
}

// SHOW FIELD ERROR
function showFieldError(fieldId, message) {
  const field = document.getElementById(fieldId);
  if (!field) return;
  field.style.borderColor = '#ef4444';
  field.style.boxShadow = '0 0 0 3px rgba(239,68,68,0.2)';
  const existing = field.parentNode.querySelector('.field-error');
  if (!existing) {
    const err = document.createElement('small');
    err.className = 'field-error';
    err.style.cssText = 'color:#ef4444;font-size:var(--text-xs);margin-top:4px;display:block;';
    err.textContent = message;
    field.parentNode.appendChild(err);
  }
  setTimeout(() => {
    field.style.borderColor = '';
    field.style.boxShadow = '';
    const errEl = field.parentNode.querySelector('.field-error');
    if (errEl) errEl.remove();
  }, 3000);
}

// LOAD DISTRICTS WHEN STATE SELECTED
function loadDistricts() {
  const stateSelect = document.getElementById('state-select');
  const districtSelect = document.getElementById('district-select');
  const selectedState = stateSelect.value;
  
  if (!selectedState || !courtData.districts[selectedState]) {
    districtSelect.innerHTML = '<option value="">-- Select District --</option>';
    return;
  }
  
  formState.state = selectedState;
  
  const districts = courtData.districts[selectedState];
  let html = '<option value="">-- Select District --</option>';
  
  districts.forEach(district => {
    html += `<option value="${district.code}">${district.name}</option>`;
  });
  
  districtSelect.innerHTML = html;
  console.log('Districts loaded for:', selectedState);
}

// LOAD COURTS WHEN DISTRICT SELECTED
function loadCourts() {
  const districtSelect = document.getElementById('district-select');
  const courtCheckboxes = document.getElementById('court-checkboxes');
  const selectedDistrict = districtSelect.value;
  
  if (!selectedDistrict || !courtData.courts[selectedDistrict]) {
    courtCheckboxes.innerHTML = '<p style="color: var(--text-muted);">No courts available</p>';
    return;
  }
  
  formState.district = selectedDistrict;
  
  const courts = courtData.courts[selectedDistrict];
  let html = '';
  
  courts.forEach((court, index) => {
    html += `
      <label>
        <input type="checkbox" value="${court.code}" onchange="toggleCourt('${court.code}')">
        <span>${court.name}</span>
      </label>
    `;
  });
  
  courtCheckboxes.innerHTML = html;
  console.log('Courts loaded for:', selectedDistrict);
}

// TOGGLE COURT SELECTION
function toggleCourt(courtCode) {
  const checkboxes = document.querySelectorAll('#court-checkboxes input[type="checkbox"]:checked');
  formState.courts = Array.from(checkboxes).map(cb => cb.value);
  console.log('Selected courts:', formState.courts);
}

// RENDER SERVICE-SPECIFIC FILTERS (STEP 4)
function renderServiceFilters() {
  const filterContainer = document.getElementById('service-filters');
  const filterTitle = document.getElementById('filter-title');
  const filterDescription = document.getElementById('filter-description');
  
  let filterHTML = '';
  
  switch (currentService) {
    case 'case-status':
      filterTitle.textContent = 'Search Case Status';
      filterDescription.textContent = 'Enter case details to find status';
      filterHTML = `
        <div class="form-group">
          <label for="case-number">Case Number <span class="required">*</span></label>
          <input type="text" id="case-number" placeholder="e.g., CS-2024-001" class="filter-input">
          <small class="form-hint">OR use Filing Number or Party Name below</small>
        </div>
        <div class="form-group">
          <label for="filing-number">Filing Number</label>
          <input type="text" id="filing-number" placeholder="e.g., 2024/1234" class="filter-input">
        </div>
        <div class="form-group">
          <label for="party-name">Party Name</label>
          <input type="text" id="party-name" placeholder="e.g., Rajesh Kumar" class="filter-input">
        </div>
        <div class="form-group">
          <label for="advocate-name">Advocate Name</label>
          <input type="text" id="advocate-name" placeholder="e.g., Rishabh Raj" class="filter-input">
        </div>
      `;
      break;
      
    case 'cause-list':
      filterTitle.textContent = 'Cause List';
      filterDescription.textContent = 'View court schedule';
      filterHTML = `
        <div class="form-group">
          <label for="cause-date">Date <span class="required">*</span></label>
          <input type="date" id="cause-date" class="filter-input" value="${new Date().toISOString().split('T')[0]}">
        </div>
        <div class="form-group">
          <label for="judge-select">Judge (Optional)</label>
          <select id="judge-select" class="filter-input">
            <option value="">-- All Judges --</option>
            <option value="Justice M. Sharma">Justice M. Sharma</option>
            <option value="Justice A. Pandey">Justice A. Pandey</option>
            <option value="Justice P. Verma">Justice P. Verma</option>
            <option value="Justice R. Shukla">Justice R. Shukla</option>
          </select>
        </div>
        <div class="form-group">
          <label for="court-hall">Court Hall (Optional)</label>
          <input type="text" id="court-hall" placeholder="e.g., 5" class="filter-input">
        </div>
      `;
      break;
      
    case 'case-search':
      filterTitle.textContent = 'Search Cases';
      filterDescription.textContent = 'Find cases by various criteria';
      filterHTML = `
        <div class="form-group">
          <label for="search-party">Party Name <span class="required">*</span></label>
          <input type="text" id="search-party" placeholder="Plaintiff or Defendant name" class="filter-input">
        </div>
        <div class="form-group">
          <label for="search-advocate">Advocate Name</label>
          <input type="text" id="search-advocate" placeholder="e.g., Rishabh Raj" class="filter-input">
        </div>
        <div class="form-group">
          <label for="search-case-type">Case Type</label>
          <select id="search-case-type" class="filter-input">
            <option value="">-- All Case Types --</option>
            <option value="Civil Suit">Civil Suit</option>
            <option value="Criminal">Criminal</option>
            <option value="Writ Petition">Writ Petition</option>
            <option value="Original Suit">Original Suit</option>
            <option value="First Appeal">First Appeal</option>
          </select>
        </div>
      `;
      break;
      
    case 'judgments':
      filterTitle.textContent = 'Search Judgments & Orders';
      filterDescription.textContent = 'Find published court decisions';
      filterHTML = `
        <div class="form-group">
          <label for="judge-date-from">From Date</label>
          <input type="date" id="judge-date-from" class="filter-input">
        </div>
        <div class="form-group">
          <label for="judge-date-to">To Date</label>
          <input type="date" id="judge-date-to" class="filter-input" value="${new Date().toISOString().split('T')[0]}">
        </div>
        <div class="form-group">
          <label for="judge-filter">Judge Name</label>
          <select id="judge-filter" class="filter-input">
            <option value="">-- All Judges --</option>
            <option value="Justice M. Sharma">Justice M. Sharma</option>
            <option value="Justice A. Pandey">Justice A. Pandey</option>
            <option value="Justice P. Verma">Justice P. Verma</option>
          </select>
        </div>
        <div class="form-group">
          <label for="verdict-filter">Verdict</label>
          <select id="verdict-filter" class="filter-input">
            <option value="">-- All Verdicts --</option>
            <option value="Allowed">Allowed</option>
            <option value="Dismissed">Dismissed</option>
            <option value="Acquittal">Acquittal</option>
            <option value="Conviction">Conviction</option>
          </select>
        </div>
      `;
      break;
      
    case 'notices':
      filterTitle.textContent = 'Search Notices';
      filterDescription.textContent = 'Find court notices and summons';
      filterHTML = `
        <div class="form-group">
          <label for="notice-date">From Date</label>
          <input type="date" id="notice-date" class="filter-input">
        </div>
        <div class="form-group">
          <label for="notice-type">Notice Type</label>
          <select id="notice-type" class="filter-input">
            <option value="">-- All Types --</option>
            <option value="Summons">Summons</option>
            <option value="Notice to Respondent">Notice to Respondent</option>
            <option value="Notice to Jury">Notice to Jury</option>
            <option value="Decree">Decree</option>
          </select>
        </div>
      `;
      break;
      
    case 'court-info':
      filterTitle.textContent = 'Court Information';
      filterDescription.textContent = 'Court details and contact info';
      filterHTML = `
        <div class="info-box" style="background: var(--bg-tertiary); padding: var(--space-6); border-radius: var(--radius-md); margin-bottom: var(--space-6);">
          <p style="font-size: var(--text-sm); color: var(--text-secondary); margin: 0;">
            Selected courts information will be displayed on next screen.
          </p>
        </div>
      `;
      break;
      
    default:
      filterHTML = '<p>Select a service to continue</p>';
  }
  
  filterContainer.innerHTML = filterHTML;
}

// PERFORM SEARCH
function performSearch(event) {
  event.preventDefault();
  
  // Collect filter data
  const filterInputs = document.querySelectorAll('.filter-input');
  const filters = {};
  filterInputs.forEach(input => {
    if (input.value) {
      filters[input.id] = input.value;
    }
  });
  
  formState.filters = filters;
  
  console.log('Search performed:', {
    service: currentService,
    state: formState.state,
    district: formState.district,
    courts: formState.courts,
    filters: formState.filters
  });
  
  // Mock search results
  displaySearchResults(currentService, formState);
}

// DISPLAY SEARCH RESULTS
function displaySearchResults(serviceType, state) {
  // Hide modal and services
  document.getElementById('service-modal').style.display = 'none';
  document.getElementById('services-section').style.display = 'none';
  document.getElementById('ecourts-search-hero').style.display = 'none';
  
  // Show results page
  const resultsPage = document.getElementById('results-page');
  resultsPage.style.display = 'block';
  
  // Get mock results based on service
  let results = [];
  switch (serviceType) {
    case 'case-status':
    case 'case-search':
      results = courtData.mockCases;
      break;
    case 'cause-list':
      results = courtData.mockCauseList;
      break;
    case 'judgments':
      results = courtData.mockJudgments;
      break;
    case 'notices':
      results = courtData.mockNotices;
      break;
    case 'court-info':
      results = courtData.courts[state.district] || [];
      break;
  }
  
  // Render results
  renderResults(results, serviceType);
  
  // Scroll to results
  setTimeout(() => {
    resultsPage.scrollIntoView({ behavior: 'smooth' });
  }, 100);
}

// RENDER RESULTS TABLE
function renderResults(results, serviceType) {
  const resultsContainer = document.getElementById('results-container');
  
  if (!results || results.length === 0) {
    resultsContainer.innerHTML = `
      <div class="empty-state">
        <div class="empty-state__icon">🔗</div>
        <div class="empty-state__title">Live court data integration in progress</div>
        <div class="empty-state__text">
          Real-time public court data will appear here once the eCourts API connection is active.<br/>
          For immediate case status, visit <a href="https://ecourts.gov.in" target="_blank" rel="noopener" style="color:var(--accent-sapphire-bright);">ecourts.gov.in</a> directly.
        </div>
      </div>
    `;
    document.getElementById('pagination-info').textContent = 'No records';
    return;
  }
  
  let html = '';
  
  results.forEach((item, index) => {
    html += renderResultItem(item, serviceType, index);
  });
  
  resultsContainer.innerHTML = html;
  
  // Update pagination
  document.getElementById('pagination-info').textContent = `Page 1 of 1 (${results.length} results)`;
  
  // Add expand/collapse functionality
  document.querySelectorAll('.result-item__header').forEach(header => {
    header.addEventListener('click', function() {
      const item = this.closest('.result-item');
      item.classList.toggle('expanded');
    });
  });
}

function renderResultItem(item, serviceType, index) {
  let content = '';
  
  if (serviceType === 'case-status' || serviceType === 'case-search') {
    content = `
      <div class="result-item">
        <div class="result-item__header">
          <div>
            <div class="result-item__title">${item.id}</div>
            <div class="result-item__meta">${item.parties.plaintiff} vs ${item.parties.defendant}</div>
          </div>
          <div class="result-item__toggle">▼</div>
        </div>
        <div class="result-item__body">
          <div class="result-details">
            <div class="detail-row">
              <div class="detail-label">Case Type</div>
              <div class="detail-value">${item.caseType}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Status</div>
              <div class="detail-value">${item.status}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Judge</div>
              <div class="detail-value">${item.judge}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Next Hearing</div>
              <div class="detail-value">${item.nextHearing} (${item.nextHearingNotes})</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Court Complex</div>
              <div class="detail-value">${item.courtComplex}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Filing Number</div>
              <div class="detail-value">${item.filingNumber}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">CNR Number</div>
              <div class="detail-value">${item.cnr}</div>
            </div>
          </div>
          <div class="result-actions">
            <button onclick="downloadCaseDetails('${item.id}')">📥 Download</button>
            <button onclick="printCaseDetails('${item.id}')">🖨️ Print</button>
            <button onclick="shareCaseLink('${item.id}')">🔗 Share</button>
          </div>
        </div>
      </div>
    `;
  } else if (serviceType === 'cause-list') {
    content = `
      <div class="result-item">
        <div class="result-item__header">
          <div>
            <div class="result-item__title">${item.caseNumber}</div>
            <div class="result-item__meta">${item.parties}</div>
          </div>
          <div class="result-item__toggle">▼</div>
        </div>
        <div class="result-item__body">
          <div class="result-details">
            <div class="detail-row">
              <div class="detail-label">Judge</div>
              <div class="detail-value">${item.judge}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Court Hall</div>
              <div class="detail-value">${item.courtHall}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Status</div>
              <div class="detail-value">${item.status}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Time</div>
              <div class="detail-value">${item.time}</div>
            </div>
          </div>
        </div>
      </div>
    `;
  } else if (serviceType === 'judgments') {
    content = `
      <div class="result-item">
        <div class="result-item__header">
          <div>
            <div class="result-item__title">${item.title}</div>
            <div class="result-item__meta">${item.caseNumber} • ${item.date}</div>
          </div>
          <div class="result-item__toggle">▼</div>
        </div>
        <div class="result-item__body">
          <div class="result-details">
            <div class="detail-row">
              <div class="detail-label">Judge</div>
              <div class="detail-value">${item.judge}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Verdict</div>
              <div class="detail-value">${item.verdict}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Summary</div>
              <div class="detail-value">${item.summary}</div>
            </div>
          </div>
          <div class="result-actions">
            <button onclick="downloadJudgment('${item.id}')">📥 Download PDF</button>
            <button onclick="shareJudgment('${item.id}')">🔗 Share</button>
          </div>
        </div>
      </div>
    `;
  } else if (serviceType === 'notices') {
    content = `
      <div class="result-item">
        <div class="result-item__header">
          <div>
            <div class="result-item__title">${item.type}</div>
            <div class="result-item__meta">${item.caseNumber} • ${item.issuedDate}</div>
          </div>
          <div class="result-item__toggle">▼</div>
        </div>
        <div class="result-item__body">
          <div class="result-details">
            <div class="detail-row">
              <div class="detail-label">Description</div>
              <div class="detail-value">${item.description}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Target Date</div>
              <div class="detail-value">${item.targetDate}</div>
            </div>
          </div>
        </div>
      </div>
    `;
  } else if (serviceType === 'court-info') {
    content = `
      <div class="result-item">
        <div class="result-item__header">
          <div>
            <div class="result-item__title">${item.name}</div>
            <div class="result-item__meta">${item.address}</div>
          </div>
          <div class="result-item__toggle">▼</div>
        </div>
        <div class="result-item__body">
          <div class="result-details">
            <div class="detail-row">
              <div class="detail-label">Phone</div>
              <div class="detail-value"><a href="tel:${item.phone}">${item.phone}</a></div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Email</div>
              <div class="detail-value"><a href="mailto:${item.email}">${item.email}</a></div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Judges</div>
              <div class="detail-value">${item.judges}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">Court Halls</div>
              <div class="detail-value">${item.halls}</div>
            </div>
          </div>
        </div>
      </div>
    `;
  }
  
  return content;
}

// UTILITY FUNCTIONS
function downloadCaseDetails(caseId) {
  alert(`Download initiated for ${caseId}\n(Mock - would generate PDF in production)`);
}

function printCaseDetails(caseId) {
  window.print();
}

function shareCaseLink(caseId) {
  const link = `${window.location.origin}${window.location.pathname}?case=${caseId}`;
  navigator.clipboard.writeText(link).then(() => {
    alert('Link copied to clipboard: ' + link);
  }).catch(err => {
    alert('Failed to copy link');
  });
}

function downloadJudgment(judgmentId) {
  alert(`Download initiated for judgment ${judgmentId}\n(Mock - would generate PDF in production)`);
}

function shareJudgment(judgmentId) {
  const link = `${window.location.origin}${window.location.pathname}?judgment=${judgmentId}`;
  navigator.clipboard.writeText(link).then(() => {
    alert('Link copied to clipboard');
  }).catch(err => {
    alert('Failed to copy link');
  });
}

// BACK TO SERVICES
function backToServices() {
  // Hide results
  document.getElementById('results-page').style.display = 'none';
  
  // Show services
  document.getElementById('ecourts-search-hero').style.display = 'block';
  document.getElementById('services-section').style.display = 'block';
  
  // Reset
  currentService = null;
  currentStep = 1;
  formState = { state: '', district: '', courts: [], filters: {} };
  
  // Scroll to top
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// PAGINATION
function changeResultsPerPage() {
  // Mock pagination - in production would reload results
  console.log('Results per page changed');
}

function prevPage() {
  alert('Previous page (mock)');
}

function nextPage() {
  alert('Next page (mock)');
}

// QUICK SEARCH FROM HERO
function handleQuickSearch(event) {
  event.preventDefault();
  
  const searchInput = document.getElementById('quick-search-input');
  const query = searchInput.value.trim();
  
  if (!query) {
    alert('Please enter a search term');
    return;
  }
  
  // Simulate quick search
  currentService = 'case-search';
  formState.state = 'UP';
  formState.district = 'LUCKNOW';
  formState.filters = { query: query };
  
  // Display results — will be empty (no mock data) until live API is connected
  document.getElementById('ecourts-search-hero').style.display = 'none';
  document.getElementById('services-section').style.display = 'none';
  document.getElementById('results-page').style.display = 'block';

  renderResults([], 'case-search');

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
  console.log('Courts eCourts JS loaded successfully');
});

/* ============================================
   STEP 8: API INTEGRATION LAYER
   Hooks for real eCourts API (production)
   All functions return Promises
   ============================================ */

const API_CONFIG = {
  BASE_URL: 'https://api.ecourts.gov.in/v1',  // Replace with real endpoint
  TIMEOUT_MS: 8000,
  CACHE_TTL: {
    STATES: 7 * 24 * 60 * 60 * 1000,    // 7 days
    DISTRICTS: 7 * 24 * 60 * 60 * 1000, // 7 days
    COURTS: 7 * 24 * 60 * 60 * 1000,    // 7 days
    CASE_STATUS: 15 * 60 * 1000,          // 15 minutes
    CAUSE_LIST: 2 * 60 * 60 * 1000,       // 2 hours
    JUDGMENTS: 24 * 60 * 60 * 1000,       // 24 hours
    NOTICES: 60 * 60 * 1000               // 1 hour
  },
  USE_MOCK: true   // Set false when real API available
};

// SIMPLE CACHE LAYER (localStorage)
const Cache = {
  set(key, value, ttlMs) {
    try {
      const entry = { value, expires: Date.now() + ttlMs };
      localStorage.setItem('ec_' + key, JSON.stringify(entry));
    } catch(e) { /* localStorage unavailable, skip cache */ }
  },
  get(key) {
    try {
      const raw = localStorage.getItem('ec_' + key);
      if (!raw) return null;
      const entry = JSON.parse(raw);
      if (Date.now() > entry.expires) { localStorage.removeItem('ec_' + key); return null; }
      return entry.value;
    } catch(e) { return null; }
  },
  clear() {
    try {
      Object.keys(localStorage).filter(k => k.startsWith('ec_')).forEach(k => localStorage.removeItem(k));
    } catch(e) {}
  }
};

// FETCH WITH TIMEOUT + RETRY
async function fetchWithTimeout(url, options = {}, retries = 2) {
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const controller = new AbortController();
      const id = setTimeout(() => controller.abort(), API_CONFIG.TIMEOUT_MS);
      const res = await fetch(url, { ...options, signal: controller.signal });
      clearTimeout(id);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch(e) {
      if (attempt === retries) throw e;
      await new Promise(r => setTimeout(r, 1000 * (attempt + 1))); // backoff
    }
  }
}

// API FUNCTION: Get states
async function apiGetStates() {
  const cacheKey = 'states';
  const cached = Cache.get(cacheKey);
  if (cached) return cached;

  if (API_CONFIG.USE_MOCK) {
    const data = { states: courtData.states };
    Cache.set(cacheKey, data, API_CONFIG.CACHE_TTL.STATES);
    return data;
  }

  try {
    const data = await fetchWithTimeout(`${API_CONFIG.BASE_URL}/states`);
    Cache.set(cacheKey, data, API_CONFIG.CACHE_TTL.STATES);
    return data;
  } catch(e) {
    console.warn('apiGetStates failed, using mock:', e.message);
    return { states: courtData.states };
  }
}

// API FUNCTION: Get districts by state
async function apiGetDistricts(stateCode) {
  const cacheKey = `districts_${stateCode}`;
  const cached = Cache.get(cacheKey);
  if (cached) return cached;

  if (API_CONFIG.USE_MOCK) {
    const data = { districts: courtData.districts[stateCode] || [] };
    Cache.set(cacheKey, data, API_CONFIG.CACHE_TTL.DISTRICTS);
    return data;
  }

  try {
    const data = await fetchWithTimeout(`${API_CONFIG.BASE_URL}/districts/${stateCode}`);
    Cache.set(cacheKey, data, API_CONFIG.CACHE_TTL.DISTRICTS);
    return data;
  } catch(e) {
    console.warn('apiGetDistricts failed, using mock:', e.message);
    return { districts: courtData.districts[stateCode] || [] };
  }
}

// API FUNCTION: Get courts by district
async function apiGetCourts(districtCode) {
  const cacheKey = `courts_${districtCode}`;
  const cached = Cache.get(cacheKey);
  if (cached) return cached;

  if (API_CONFIG.USE_MOCK) {
    const data = { courts: courtData.courts[districtCode] || [] };
    Cache.set(cacheKey, data, API_CONFIG.CACHE_TTL.COURTS);
    return data;
  }

  try {
    const data = await fetchWithTimeout(`${API_CONFIG.BASE_URL}/courts/${districtCode}`);
    Cache.set(cacheKey, data, API_CONFIG.CACHE_TTL.COURTS);
    return data;
  } catch(e) {
    console.warn('apiGetCourts failed, using mock:', e.message);
    return { courts: courtData.courts[districtCode] || [] };
  }
}

// API FUNCTION: Search cases
async function apiSearchCases(params) {
  if (API_CONFIG.USE_MOCK) {
    await new Promise(r => setTimeout(r, 600)); // simulate network delay
    return { success: true, data: courtData.mockCases, total: courtData.mockCases.length };
  }

  try {
    return await fetchWithTimeout(`${API_CONFIG.BASE_URL}/case-status`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    });
  } catch(e) {
    console.warn('apiSearchCases failed, using mock:', e.message);
    return { success: true, data: courtData.mockCases, total: courtData.mockCases.length };
  }
}

// API FUNCTION: Get cause list
async function apiGetCauseList(params) {
  if (API_CONFIG.USE_MOCK) {
    await new Promise(r => setTimeout(r, 400));
    return { success: true, data: courtData.mockCauseList, total: courtData.mockCauseList.length };
  }

  try {
    return await fetchWithTimeout(`${API_CONFIG.BASE_URL}/cause-list?` + new URLSearchParams(params));
  } catch(e) {
    return { success: true, data: courtData.mockCauseList, total: courtData.mockCauseList.length };
  }
}

// API FUNCTION: Get judgments
async function apiGetJudgments(params) {
  if (API_CONFIG.USE_MOCK) {
    await new Promise(r => setTimeout(r, 500));
    return { success: true, data: courtData.mockJudgments, total: courtData.mockJudgments.length };
  }

  try {
    return await fetchWithTimeout(`${API_CONFIG.BASE_URL}/judgments?` + new URLSearchParams(params));
  } catch(e) {
    return { success: true, data: courtData.mockJudgments, total: courtData.mockJudgments.length };
  }
}

// API FUNCTION: Get notices
async function apiGetNotices(params) {
  if (API_CONFIG.USE_MOCK) {
    await new Promise(r => setTimeout(r, 400));
    return { success: true, data: courtData.mockNotices, total: courtData.mockNotices.length };
  }

  try {
    return await fetchWithTimeout(`${API_CONFIG.BASE_URL}/notices?` + new URLSearchParams(params));
  } catch(e) {
    return { success: true, data: courtData.mockNotices, total: courtData.mockNotices.length };
  }
}

// LOADING STATE MANAGER
function setLoading(containerId, isLoading, message = 'Loading...') {
  const el = document.getElementById(containerId);
  if (!el) return;
  if (isLoading) {
    el.innerHTML = `
      <div class="loading-state">
        <div class="skeleton" style="height:80px;border-radius:8px;margin-bottom:12px;"></div>
        <div class="skeleton" style="height:80px;border-radius:8px;margin-bottom:12px;width:90%;"></div>
        <div class="skeleton" style="height:80px;border-radius:8px;width:95%;"></div>
        <p style="text-align:center;color:var(--text-muted);font-size:var(--text-sm);margin-top:16px;">${message}</p>
      </div>`;
  }
}

// ERROR STATE MANAGER
function showError(containerId, message, retryFn) {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = `
    <div class="empty-state">
      <div class="empty-state__icon">⚠️</div>
      <div class="empty-state__title">Something went wrong</div>
      <div class="empty-state__text">${message}</div>
      ${retryFn ? '<button class="btn-secondary" onclick="' + retryFn + '()" style="margin-top:16px;padding:8px 20px;">Try Again</button>' : ''}
    </div>`;
}

// ASYNC performSearch (replaces sync version)
async function performSearchAsync(event) {
  if (event) event.preventDefault();

  const filterInputs = document.querySelectorAll('.filter-input');
  const filters = {};
  filterInputs.forEach(input => { if (input.value) filters[input.id] = input.value; });
  formState.filters = filters;

  // Show results page with loading state
  document.getElementById('service-modal').style.display = 'none';
  document.getElementById('services-section').style.display = 'none';
  document.getElementById('ecourts-search-hero').style.display = 'none';
  document.getElementById('results-page').style.display = 'block';

  // Show skeleton loader
  setLoading('results-container', true, 'Searching court records...');
  document.getElementById('pagination-info').textContent = 'Loading...';

  try {
    let response;
    const params = { state: formState.state, district: formState.district, ...filters };

    switch (currentService) {
      case 'case-status':
      case 'case-search':
        response = await apiSearchCases(params); break;
      case 'cause-list':
        response = await apiGetCauseList(params); break;
      case 'judgments':
        response = await apiGetJudgments(params); break;
      case 'notices':
        response = await apiGetNotices(params); break;
      case 'court-info':
        response = { success: true, data: courtData.courts[formState.district] || [] }; break;
      default:
        response = { success: true, data: courtData.mockCases };
    }

    if (response && response.success) {
      renderResults(response.data, currentService);
    } else {
      showError('results-container', 'Could not retrieve results. Please try again.', 'backToServices');
    }
  } catch(e) {
    console.error('Search error:', e);
    showError('results-container', 'A network error occurred. Please check your connection and try again.', 'backToServices');
  }
}

// Override performSearch to use async version
function performSearch(event) { performSearchAsync(event); }

/* ============================================
   STEP 9: PROGRESS INDICATOR + FINAL QA FIXES
   ============================================ */

// Update workflow progress bar
function updateProgressBar(step) {
  for (let i = 1; i <= 4; i++) {
    const el = document.getElementById('wp-' + i);
    if (!el) continue;
    el.classList.remove('active', 'done');
    if (i < step) el.classList.add('done');
    else if (i === step) el.classList.add('active');
  }
}

// Override showStep to also update progress bar
const _origShowStep = showStep;
function showStep(step) {
  _origShowStep(step);
  updateProgressBar(step);
}

// Add status badge helper
function getStatusBadge(status) {
  if (!status) return '';
  const s = status.toLowerCase();
  let cls = 'active';
  if (s.includes('today') || s.includes('hearing'))  cls = 'hearing';
  else if (s.includes('reserved'))                   cls = 'reserved';
  else if (s.includes('disposed') || s.includes('acquittal') || s.includes('allowed')) cls = 'disposed';
  else if (s.includes('pending') || s.includes('evidence') || s.includes('arguments')) cls = 'pending';
  return `<span class="status-badge status-badge--${cls}">${status}</span>`;
}

// Add results count line
function addResultsCount(total) {
  const container = document.getElementById('results-container');
  if (!container) return;
  const countDiv = document.createElement('div');
  countDiv.className = 'results-count';
  countDiv.innerHTML = `<strong>${total}</strong> result${total !== 1 ? 's' : ''} found`;
  container.prepend(countDiv);
}

// Keyboard: close modal on Escape
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    const modal = document.getElementById('service-modal');
    if (modal && modal.style.display !== 'none') closeServiceModal();
  }
});

// Trap focus inside modal when open
document.addEventListener('keydown', function(e) {
  if (e.key !== 'Tab') return;
  const modal = document.getElementById('service-modal');
  if (!modal || modal.style.display === 'none') return;
  const focusable = modal.querySelectorAll('button, input, select, [tabindex]:not([tabindex="-1"])');
  const first = focusable[0], last = focusable[focusable.length - 1];
  if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
  else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
});

// Focus first element in modal when opened
const _origInitiateService = initiateService;
function initiateService(serviceType) {
  _origInitiateService(serviceType);
  setTimeout(() => {
    const modal = document.getElementById('service-modal');
    if (modal) {
      const first = modal.querySelector('button, input, select');
      if (first) first.focus();
    }
  }, 100);
}

// Scroll to results section after showing
const _origBackToServices = backToServices;
function backToServices() {
  _origBackToServices();
  document.getElementById('services-section')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

console.log('eCourts Portal v1.0 ready — ' + new Date().toLocaleDateString());
