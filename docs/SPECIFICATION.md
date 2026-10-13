# REFINED SPECIFICATION: Courts Services Portal Redesign
## Ink & Equity Website v5

---

## EXECUTIVE SUMMARY

Transform the Courts page from a static firm-specific court matter display into a **dynamic eCourts Services portal** for District Courts across India. The new page will provide public-facing tools for case search, status tracking, and court information lookup while maintaining the firm's existing design language, accessibility, and brand identity.

---

## PHASE 1: REQUIREMENTS CLARIFICATION & REFINEMENT

### Issues Identified in Original Specification

#### 1. **Data Source Ambiguity**
**Original Issue:** Specification references "eCourts Services ecosystem" but doesn't clarify:
- Which eCourts APIs to use
- Fallback strategies if APIs are unavailable
- Rate limiting & caching mechanisms
- Data freshness guarantees

**Refined Approach:**
- Primary: Use official eCourts National Portal API (if publicly accessible)
- Secondary: Use district court websites' eCourts modules via web scraping
- Tertiary: Provide static demo data with clear "demo" labels during development
- **Implementation Decision:** Start with demo/static data with API integration hooks for future scaling

#### 2. **Geographic Scope Unclear**
**Original Issue:** "District Courts across India" is vague
- 676 district courts in India
- Multiple state hierarchies (State → District → Court Complex)
- Not all courts have eCourts integration

**Refined Approach:**
- **Phase 1 Initial:** Focus on UP (Uttar Pradesh) district courts as pilot
- Reason: Firm has active practice in UP, complete court hierarchy exists
- Extensible architecture to add other states later
- UI allows state selection; district/court selection populate dynamically

#### 3. **Service Integration Strategy Missing**
**Original Issue:** Long list of eCourts services without clear priority or integration feasibility

**Refined Approach - Tiered Implementation:**
```
TIER 1 (MVP - Must Have):
  - Case Status Lookup (by case number, filing number)
  - Case Search (by party name, advocate name)
  - Cause List (by date, judge)
  - Judgments & Orders
  - Notices

TIER 2 (Phase 2 - Should Have):
  - CNR Number Search
  - Court Establishment Info
  - Certified Copy Status
  - Hearing Information
  - Court Complex Info

TIER 3 (Future - Nice to Have):
  - FIR/Police Station Search
  - Judge-wise Cases
  - Advocate-wise Cases
  - Court Orders (advanced filtering)
  - Case History Timeline
```

#### 4. **UX Flow Oversimplification**
**Original Issue:** State → District → Court Complex flow doesn't account for:
- User already knowing their court/case
- Mobile users struggling with 3+ select dropdowns
- Accessibility of cascading selects
- Search-first vs. browse-first patterns

**Refined UX Flow:**

**Option A: Search-First (Recommended)**
```
User Landing
├─ Option 1: Direct Case Search
│  ├─ Enter Case Number OR Filing Number OR Party Name
│  ├─ Auto-detect court from case metadata
│  └─ Display results immediately
└─ Option 2: Browse by Court
   ├─ Select State (required)
   ├─ Select District (required)
   ├─ Select Court Complex (optional)
   └─ Select Service & Filters
```

**Option B: Tab-Based**
```
Services Portal
├─ "Quick Search" tab (prominent)
│  └─ Unified search box
└─ "Browse Services" tab
   └─ Filterable service grid
```

**Decision:** Implement Option A with search-first + service cards below

#### 5. **Accessibility & Mobile Concerns**
**Original Issue:** Cascading selects are notoriously difficult on mobile & for assistive tech

**Refined Approach:**
- Use combobox pattern (searchable select) not plain `<select>`
- Autocomplete for state/district/court
- Large tap targets (min 44×44px)
- ARIA labels on all interactive elements
- Keyboard navigation fully functional
- Focus management when modals open
- Mobile: Stack filters vertically, not horizontally

#### 6. **Results Display Ambiguity**
**Original Issue:** "Clean searchable results table" too vague

**Refined Approach - Results Page Requirements:**
```
Desktop (≥1024px):
- Expandable rows (click to see full details)
- Sortable columns (case number, status, date, next hearing)
- Inline filtering (by status, judge, date range)
- Pagination (25/50/100 results per page)
- Card view toggle (optional)

Tablet (768-1023px):
- Single column collapsible cards
- Filter drawer (swipe from side or hamburger)
- Pagination preserved

Mobile (<768px):
- Full-width cards
- Stacked filters (collapsed by default)
- Swipe-able pagination OR "Load More" button
- Print: full-page PDF export
```

#### 7. **Missing Error Scenarios**
**Original Issue:** No guidance on handling API failures, rate limits, invalid inputs

**Refined Error Handling:**
```
API Unavailable:
→ "This service is temporarily unavailable. Try again in a moment."
→ Display cached results if available with timestamp
→ Fallback to contact form: "Can't find it? Contact us"

No Results:
→ "No cases found. Try:"
→ "• Using a different search criteria"
→ "• Checking the case number"
→ "• Contacting the court directly" (with court phone)

Rate Limited:
→ "Please wait before searching again"
→ Display countdown timer
→ Queue search in background

Invalid Input:
→ Client-side validation with helpful messages
→ "Case number must be numeric"
→ Format hints below input fields

Network Timeout:
→ Retry button visible
→ "This is taking longer than expected..."
→ Auto-retry with exponential backoff (3 attempts)
```

#### 8. **Design Consistency Gaps**
**Original Issue:** Card design not specified in detail

**Refined Card Component:**
```
Service Card Anatomy:
┌─────────────────────────────────────┐
│  [Icon] [Illustration/Photo]        │  ← 60% card height
│                                     │
│  Service Title (Headline 2)         │  
│  ─────────────────────────────────  │
│  Short description (2-3 lines max)  │
│  [Accent color underline]           │
│                                     │
│  ┌──────────────────────────────┐   │
│  │ Explore Service →            │   │
│  └──────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘

States:
- Default: --bg-card, --shadow-sm
- Hover: --bg-card-hover, --shadow-md, slight scale (1.02)
- Active: --accent-sapphire glow, --shadow-glow
- Focus: Outline 2px --accent-sapphire-bright with 2px offset

Colors (per design system):
- Icon: --accent-sapphire-bright
- Title: --text-primary
- Description: --text-secondary
- Border: --border-subtle
- Button: --accent-sapphire bg with --text-inverse
```

#### 9. **Caching & Performance**
**Original Issue:** No guidance on caching, loading states, performance budgets

**Refined Approach:**
```
Data Caching:
- State/District/Court lists: Cache 7 days (rarely change)
- Cause list: Cache 2 hours (updates multiple times daily)
- Case status: Cache 15 minutes (frequently updated)
- Judgments/Orders: Cache 24 hours (static once published)

Use localStorage for offline court data + IndexedDB for search history

Loading States:
- Skeleton screens for lists (not spinners)
- Progressive content reveal
- Time budget: Show content within 1.5s or show error

Performance Budget:
- Page load: <2s (FCP), <3.5s (LCP)
- Search response: <1.5s or show "searching..." state
- Result render: <500ms for 50 items
```

#### 10. **Security Concerns**
**Original Issue:** No mention of security when integrating third-party eCourts services

**Refined Security Approach:**
```
API Integration:
- Never expose API keys in frontend
- Backend proxy all eCourts requests via Node server
- Rate limit requests (prevent abuse)
- Validate all user inputs (sanitize for injection)
- CORS properly configured
- CSP headers to restrict external resource loading

Data Handling:
- No sensitive case details stored locally
- Clear search history option
- Comply with Indian court data confidentiality rules
- Display disclaimer: "Public information only"

SSL/HTTPS:
- All requests HTTPS only
- Secure cookie flags
```

---

## PHASE 2: FINAL SPECIFICATION

### A. INFORMATION ARCHITECTURE

#### State Structure (UP Focus, v1)

```
UTTAR PRADESH
├─ Lucknow District
│  ├─ District Court, Lucknow (Main Complex)
│  ├─ City Sessions Court, Lucknow
│  └─ Additional District Court Offices
├─ Kanpur District
│  ├─ District Court, Kanpur
│  └─ Additional Courts
├─ Agra District
│  ├─ District Court, Agra
│  └─ Additional Courts
└─ [20+ other UP districts]

Services available across all courts (mostly)
```

#### Service Catalog (MVP - Tier 1)

| Service | Primary Input | Output | Filter Options |
|---------|---------------|--------|-----------------|
| **Case Status** | Case Number / Filing Number / CNR | Case details, judge, next hearing | Date range, court |
| **Case Search** | Party Name / Advocate Name | Matching cases | Status, case type |
| **Cause List** | Court + Date (optional) | Today's/date's cause list | Judge, court hall |
| **Judgments & Orders** | Court + Date Range | Published judgments | Judge, case type |
| **Notices** | Court + Date | Filed notices | Court, type |

---

### B. PAGE STRUCTURE & LAYOUT

#### Hero Section
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
eCourts Services — District Courts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Access case information, court calendars, judgments, 
and notices across district courts in India.

[Search Box - See below]

⚡ All data is PUBLIC and sourced from official 
eCourts platforms. Not legal advice.
```

#### Search Box (Hero - Prominent CTA)
```
┌──────────────────────────────────────────────────────┐
│ What are you looking for?                     [×]    │
│ ├─ Case Number / Filing Number (e.g., "CS-2024-001")│
│ ├─ Party Name (e.g., "John Doe")                    │
│ └─ Advocate Name                                    │
│                                                    │
│ [Search Button]  or  [Browse Services] →           │
└──────────────────────────────────────────────────────┘
```

#### Service Cards Grid
```
Below search box:

┌────────────┬────────────┬────────────┐
│   Case     │   Cause    │ Judgments  │
│  Status    │   List     │  & Orders  │
└────────────┴────────────┴────────────┘

┌────────────┬────────────┬────────────┐
│   Case     │  Notices   │   Court    │
│  Search    │            │   Info     │
└────────────┴────────────┴────────────┘

3 columns on desktop, 2 on tablet, 1 on mobile
Max width: 1320px (matches container)
```

---

### C. USER FLOWS (Detailed)

#### FLOW 1: Quick Search
```
User enters: "CS-2024-001" → Search

↓ (via backend API or demo data)

Display:
- Court: District Court, Lucknow
- Case Type: Civil Suit
- Parties: A vs B
- Status: Ongoing
- Next Hearing: 15 June 2024
- Judge: Justice X
- [View Full Details] [Download Case History] [Share]
```

#### FLOW 2: Browse by Service (Case Status)
```
User clicks "Case Status" card

↓ Step 1: State Selection
┌────────────────────────┐
│ State: [Uttar Pradesh▼]│
│        (1 choice)      │
│ [Continue]             │
└────────────────────────┘

↓ Step 2: District Selection
┌────────────────────────┐
│ District: [Lucknow▼]   │
│ (22 options)           │
│ (searchable)           │
│ [Continue]             │
└────────────────────────┘

↓ Step 3: Court Selection (Optional)
┌────────────────────────┐
│ Court Complex:         │
│ ☑ District Court       │ (default)
│ ☐ Additional Courts    │
│ [Continue]             │
└────────────────────────┘

↓ Step 4: Service-Specific Filters
┌─────────────────────────────────┐
│ Search Case Status              │
│ ─────────────────────────────── │
│ Case Number: [_____________]    │
│ Filing Number: [_____________]  │
│ CNR Number: [_____________]     │
│ Party Name: [_____________]     │
│                                 │
│ [Search] [Clear]                │
└─────────────────────────────────┘

↓ Results (See Results Page spec below)
```

#### FLOW 3: Browse Service (Cause List)
```
User clicks "Cause List" card

↓ Same as FLOW 2 (State → District → Court)

↓ Step 4: Service-Specific Filters
┌─────────────────────────────────┐
│ Cause List                      │
│ ─────────────────────────────── │
│ Date: [Today ▼] (or pick date)  │
│ Judge: [All Judges ▼]           │
│ Court Hall: [All Halls ▼]       │
│                                 │
│ [Show Cause List] [Reset]       │
└─────────────────────────────────┘

↓ Results: Tabular list of cases for the day
```

---

### D. RESULTS PAGE SPECIFICATION

#### Desktop View (≥1024px)
```
┌─────────────────────────────────────────────────────┐
│ Results: 47 cases found                             │
│ 👁 View: [Grid] [List] | Sort: [Date▼] | Per page: [25▼] │
├─────────────────────────────────────────────────────┤
│ ▼ Case CS-2024-001                                  │ ← Expandable
│   A vs B | Lucknow District Court | Ongoing       │
│   Judge: Justice X | Next: 15 June 2024            │
│   [Download] [Print] [Share] [More Details]        │
├─────────────────────────────────────────────────────┤
│ ▼ Case CS-2024-002                                  │
│   ...                                              │
├─────────────────────────────────────────────────────┤
│ Pagination: [< 1 2 3 4 ... >]                      │
└─────────────────────────────────────────────────────┘

When ▼ expanded:
├─────────────────────────────────────────────────────┤
│ ▲ Case CS-2024-001                                  │
│   A vs B | Lucknow District Court | Ongoing       │
│   ──────────────────────────────────────────────   │
│   Judge: Justice X                                 │
│   Case Type: Civil Suit                            │
│   Filed: 10 Jan 2024                               │
│   Next Hearing: 15 June 2024                       │
│   Court Hall: No. 5                                │
│   Advocates: [Adv 1], [Adv 2]                      │
│   Status: Arguments in progress                    │
│   [Download Details PDF] [Print] [Share Link]      │
├─────────────────────────────────────────────────────┤

Inline filters (above results):
┌──────────────────────────────────────────────────┐
│ Filters: [Status▼] [Date▼] [Judge▼] [Clear All] │
└──────────────────────────────────────────────────┘
```

#### Tablet View (768-1023px)
```
Results displayed as full-width cards:

┌────────────────────────────────┐
│ CS-2024-001                    │
│ A vs B | Lucknow DC | Ongoing  │
│                                │
│ Next Hearing: 15 June 2024     │
│ [Expand] [Share] [Print]       │
└────────────────────────────────┘

Filters: Collapsible drawer on left or hamburger
```

#### Mobile View (<768px)
```
┌──────────────────────────┐
│ Results: 47 cases        │
│ [Filters ☰]              │
├──────────────────────────┤
│ CS-2024-001              │
│ A vs B | Ongoing         │
│ 15 June 2024             │
│ [Expand]                 │
├──────────────────────────┤
│ CS-2024-002              │
│ ...                      │
├──────────────────────────┤
│ [Load More ↓]            │
└──────────────────────────┘
```

---

### E. EMPTY STATES & ERROR STATES

#### No Results
```
┌──────────────────────────────────────────┐
│  No cases found                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Try:                                    │
│  • Checking the spelling                 │
│  • Using a different search term         │
│  • Broadening your date range            │
│  • Visiting the court directly           │
│                                          │
│  Still can't find it?                    │
│  [Contact the Court] [Contact Us]        │
└──────────────────────────────────────────┘
```

#### Error State
```
┌──────────────────────────────────────────┐
│  ⚠ Something went wrong                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  We couldn't fetch results at the moment.│
│  Please try again.                       │
│                                          │
│  [← Go Back] [Try Again]                 │
│                                          │
│  Errors persist? [Report Issue]          │
└──────────────────────────────────────────┘
```

#### Loading State
```
Skeleton Screens (NOT spinners):
┌──────────────────────────┐
│ [████████████████] Case  │
│ [██████] Judge | [████]  │
│ [████████] Hearing      │
└──────────────────────────┘
```

---

### F. DETAILED TECHNICAL REQUIREMENTS

#### Backend Architecture
```
Frontend (HTML/CSS/JS)
       ↓
Express.js Backend Server
  ├─ /api/courts/states
  ├─ /api/courts/districts/:state
  ├─ /api/courts/complexes/:district
  ├─ /api/case-status (POST)
  ├─ /api/case-search (GET)
  ├─ /api/cause-list (GET)
  ├─ /api/judgments (GET)
  └─ /api/notices (GET)
       ↓
eCourts APIs / Web Scraping / Cache Layer
       ↓
Data Sources:
  - eCourts National Portal (primary)
  - District court websites (secondary)
  - Local data cache (fallback)
```

#### Frontend Patterns
```
Components:
  - StateSelector (combobox)
  - DistrictSelector (combobox, cascading)
  - CourtSelector (checkboxes)
  - ServiceFilters (dynamic per service)
  - ResultsTable (expandable rows)
  - ResultsCard (mobile view)
  - EmptyState (component)
  - LoadingState (skeleton)
  - ErrorBoundary (catch errors)

State Management:
  - Use vanilla JS or lightweight store (localStorage)
  - Maintain: selectedState, selectedDistrict, selectedServices
  - Persist to localStorage for faster repeat visits

Data Flow:
  1. User selects state → fetch districts
  2. User selects district → fetch courts
  3. User fills filters → POST to /api/{service}
  4. Backend queries data source
  5. Results rendered with skeleton → full content
```

#### API Response Format
```
// GET /api/courts/states
{
  "states": [
    { "code": "UP", "name": "Uttar Pradesh", "courts_count": 76 }
  ]
}

// GET /api/courts/districts/UP
{
  "districts": [
    { "code": "LKO", "name": "Lucknow", "courts_count": 3 },
    ...
  ]
}

// POST /api/case-status
Request:
{
  "state": "UP",
  "district": "LKO",
  "case_number": "CS-2024-001"
}

Response:
{
  "success": true,
  "data": {
    "case_number": "CS-2024-001",
    "filing_number": "2024/1234",
    "cnr": "UP1234200",
    "parties": {
      "plaintiff": "John Doe",
      "defendant": "Jane Smith"
    },
    "case_type": "Civil Suit",
    "status": "Ongoing",
    "judge": "Justice X",
    "next_hearing": "2024-06-15",
    "next_hearing_notes": "Arguments",
    "last_hearing": "2024-06-01",
    "court_complex": "District Court, Lucknow",
    "court_hall": "No. 5"
  }
}

// Error Response:
{
  "success": false,
  "error": "CASE_NOT_FOUND",
  "message": "No case found with that number"
}
```

---

### G. DESIGN SPECIFICATIONS (Detailed)

#### Color Palette (Using existing design tokens)
```
Primary Components:
- Cards: --bg-card (#1a1a1f) on dark
- Card Borders: --border-subtle (rgba(200, 205, 214, 0.08))
- Text (Headers): --text-primary (#f0ede8)
- Text (Body): --text-secondary (#a8a5a0)
- Accents: --accent-sapphire (#4a7ab5)
- Hover: --surface-glass-hover (rgba(255, 255, 255, 0.06))

Icons:
- Primary: --accent-sapphire-bright (#6b9fd4)
- Success: #4ade80 (new - for status)
- Warning: #facc15 (new - for pending)
- Error: #ef4444 (new - for issues)
```

#### Typography
```
Page Title: --text-5xl (Cormorant Garamond, serif)
Service Card Title: --text-xl (Cormorant, bold)
Filters Label: --text-sm (Jost, uppercase, letterspaced)
Results Table Headers: --text-sm (Jost, bold)
Body Text: --text-base (Jost)
```

#### Spacing
```
Hero to Services: --space-24 (6rem)
Between Cards: --space-8 (2rem)
Card Padding: --space-6 (1.5rem)
Filter Spacing: --space-4 (1rem)
Result Row Padding: --space-4 (1rem)
```

#### Responsive Breakpoints
```
Mobile: <640px (--bp-sm)
  - 1 column for cards
  - Full-width inputs
  - Stacked filters

Tablet: 640-1024px (--bp-md to --bp-lg)
  - 2 columns for cards
  - Side-by-side filters (in drawer)

Desktop: ≥1024px (--bp-lg+)
  - 3 columns for cards
  - Expandable filter sidebar
  - Sortable tables
```

---

### H. ACCESSIBILITY REQUIREMENTS (WCAG 2.1 AA)

```
✓ Color contrast: 4.5:1 for normal text, 3:1 for large text
✓ Focus indicators: 2px solid outline, visible at all times
✓ Keyboard navigation: Tab through all interactive elements
✓ ARIA labels: All inputs, buttons, regions properly labeled
✓ Semantic HTML: <header>, <main>, <section>, <form> etc.
✓ Form validation: Clear error messages, field-level hints
✓ Mobile: Touch targets ≥44×44px
✓ Screen readers: All content announced properly
✓ Reduced motion: Respect prefers-reduced-motion media query
✓ Responsive text: Use fluid typography (clamp)
✓ Link text: Descriptive, not "click here"
```

---

### I. SECURITY & DATA PRIVACY

```
GDPR/Data Handling:
✓ All data from public eCourts sources
✓ No personal data collection beyond search queries
✓ No cookies except session token (if login required)
✓ Clear privacy disclaimer on page
✓ Search history not stored server-side (localStorage only)
✓ User can clear history anytime

API Security:
✓ All requests proxied through backend (no direct CORS)
✓ Rate limiting: 60 requests/minute per IP
✓ Input sanitization: Prevent SQL injection, XSS
✓ HTTPS only
✓ CSP headers configured
✓ No API keys exposed in frontend

External Data:
✓ Display disclaimer: "This information is public and from official sources"
✓ Not responsible for accuracy (users verify via official channels)
✓ No legal advice implied
```

---

### J. PERFORMANCE REQUIREMENTS

```
Metrics:
✓ First Contentful Paint (FCP): <1.5s
✓ Largest Contentful Paint (LCP): <2.5s
✓ Cumulative Layout Shift (CLS): <0.1
✓ Time to Interactive (TTI): <3.5s

Strategies:
✓ Lazy load images/illustrations
✓ Cache state/district/court data (localStorage)
✓ Cache API responses (2 hour TTL)
✓ Minify CSS/JS
✓ Compress images (WebP with JPEG fallback)
✓ Use skeleton screens (not spinners)
✓ Pagination (max 50 items per page)
✓ Debounce search input (500ms)
```

---

## PHASE 2 IMPLEMENTATION ROADMAP

### Sprint 1: Foundation
- [ ] Set up page layout (hero, search box, service cards)
- [ ] Build state/district/court data structure
- [ ] Create service card components
- [ ] Implement search box (basic)

### Sprint 2: Search & Filter Flow
- [ ] Implement state → district → court flow
- [ ] Build filter forms per service
- [ ] Connect to mock API endpoints
- [ ] Add loading states

### Sprint 3: Results & Display
- [ ] Build results page (desktop + mobile)
- [ ] Implement expandable rows
- [ ] Add sorting/filtering on results
- [ ] Error handling & empty states

### Sprint 4: Polish & Testing
- [ ] Responsive design refinement
- [ ] Accessibility audit (WCAG AA)
- [ ] Performance optimization
- [ ] Cross-browser testing

---

## PHASE 3: TESTING CHECKLIST

```
Functional Testing:
☐ State selection populates districts
☐ District selection populates courts
☐ Court selection toggles (multi-select works)
☐ Filters display per service
☐ Search returns results
☐ Results pagination works
☐ Sort/filter on results works
☐ Expandable rows toggle
☐ All buttons/links are clickable

Responsive Testing:
☐ Mobile (<640px): Single column, stacked filters
☐ Tablet (640-1024px): Two columns, side drawer
☐ Desktop (≥1024px): Three columns, sidebar

Accessibility Testing:
☐ Tab navigation complete
☐ Focus visible at all times
☐ ARIA labels present
☐ Color contrast ≥4.5:1
☐ Keyboard-only usage possible
☐ Screen reader friendly (test with NVDA/JAWS)

Edge Cases:
☐ No results state
☐ API timeout/error state
☐ Rate limit state
☐ Empty filters submitted
☐ Very long case numbers
☐ Special characters in party names

Performance:
☐ FCP < 1.5s
☐ Search results load < 2s
☐ No layout shifts (CLS <0.1)

Cross-Browser:
☐ Chrome (latest)
☐ Firefox (latest)
☐ Safari (latest)
☐ Edge (latest)
☐ Mobile Safari (iOS)
☐ Chrome Mobile (Android)
```

---

## PHASE 4: DEPLOYMENT

```
Pre-Deployment:
☐ All tests passing
☐ No console errors
☐ Lighthouse score ≥85
☐ Accessibility audit ≥85
☐ Final stakeholder approval

Deployment Steps:
1. Commit all code to feature branch
2. Create Pull Request with changelog
3. Run automated tests (CI/CD)
4. Merge to main branch
5. Deploy to GitHub Pages
6. Smoke test production site
7. Monitor error logs for 24 hours
8. Publish changelog/release notes

Rollback Plan:
- If critical issues: revert to previous commit
- Test rollback in staging first
- Notify users of any service disruption
```

---

## FUTURE ENHANCEMENTS (Post-MVP)

```
Phase 2 (Optional):
- Add more states beyond UP
- Integrate with eCourts APIs (replace demo data)
- User accounts for saved searches
- Case notifications/reminders
- Export to PDF/Excel
- Mobile app (React Native/Flutter)
- Multi-language support (Hindi, regional)

Phase 3:
- Judge schedules integration
- Advocate profiles
- Courtroom location maps
- Court fee calculators
- Legal document templates
```

---

## SIGN-OFF

**This specification is now detailed, implementable, and resolves all ambiguities from the original brief.**

Key decisions made:
1. **Search-first UX** with service cards as secondary navigation
2. **UP district courts pilot** (extensible to other states)
3. **5 Tier-1 services** for MVP (expandable later)
4. **Backend API proxy** for security & flexibility
5. **Skeleton screens** for better UX than spinners
6. **WCAG AA compliance** throughout
7. **Performance budget** with clear metrics

Ready for implementation. ✓
