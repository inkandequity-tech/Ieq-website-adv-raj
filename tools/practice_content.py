"""Practice-area pages beyond the original four.

Content is general information for readers, not legal advice. Each page is
reviewed by the responsible advocate before publication (see the PR). Statute
names are given as they are commonly cited; section numbers and thresholds
must be checked against the current text before any change is made.
"""

# (slug, index title, index blurb)
NEW_PRACTICE = [
    ("civil-litigation", "Civil litigation",
     "Civil suits, injunctions, recovery of money, appeals and execution of decrees."),
    ("commercial-and-contract-disputes", "Commercial and contract disputes",
     "Breach of contract, supply and distribution disputes, and commercial suits."),
    ("arbitration-and-adr", "Arbitration and dispute resolution",
     "Domestic and international arbitration, setting aside and enforcement of awards, mediation."),
    ("criminal-law", "Criminal law",
     "Bail, complaints, trials, appeals and quashing, under the new criminal codes."),
    ("family-and-matrimonial", "Family and matrimonial matters",
     "Divorce, maintenance, custody, domestic violence and related family proceedings."),
    ("succession-and-wills", "Succession, wills and probate",
     "Wills, probate, letters of administration, family settlements and inheritance disputes."),
    ("corporate-and-commercial", "Corporate and commercial law",
     "Company, LLP and partnership structures, governance and commercial documentation."),
    ("mergers-acquisitions-and-investment", "Mergers, acquisitions and investment",
     "Due diligence, shareholders' agreements, investment documentation and transaction support."),
    ("intellectual-property", "Intellectual property",
     "Trade marks, copyright, designs and patents: ownership, licensing and enforcement."),
    ("data-privacy-and-technology", "Data, privacy and technology law",
     "Privacy notices, data protection, IT Act issues, software and platform terms."),
    ("tax-customs-and-fema", "Tax, customs and FEMA",
     "Tax notices and appeals, GST and customs disputes, and foreign exchange compliance."),
    ("employment-and-labour", "Employment and labour",
     "Employment contracts, terminations, workplace claims, POSH compliance and labour law."),
    ("consumer-protection", "Consumer protection",
     "Consumer complaints against sellers, service providers, builders, banks and insurers."),
    ("banking-recovery-and-insolvency", "Banking, recovery and insolvency",
     "Loan defaults, SARFAESI and debt recovery, and matters under the Insolvency and Bankruptcy Code."),
    ("competition-and-regulatory", "Competition and regulatory matters",
     "Competition Act issues, regulatory show-cause notices and appeals against regulators."),
    ("environment-energy-and-infrastructure", "Environment, energy and infrastructure",
     "Environmental clearances, pollution proceedings, power contracts and infrastructure disputes."),
    ("insurance-and-claims", "Insurance and claims",
     "Repudiation and delay in insurance claims, policy interpretation and insurance disputes."),
    ("healthcare-education-and-professional-regulation", "Healthcare, education and professional bodies",
     "School and university disputes, admissions, fee issues and professional disciplinary proceedings."),
    ("media-entertainment-and-sports", "Media, entertainment and sports",
     "Production and talent contracts, licensing, takedowns, defamation and personality rights."),
    ("non-profit-trusts-and-societies", "Trusts, societies and non-profits",
     "Trust deeds, society governance, Section 8 companies and donation and funding agreements."),
    ("cross-border-and-nri-matters", "Cross-border and NRI matters",
     "International contracts, foreign arbitral awards and property and succession for NRIs."),
    ("government-procurement-and-rti", "Government contracts, RTI and public grievances",
     "Tender disputes, blacklisting, Right to Information appeals and public grievances."),
]

NEW_PAGES = {
"civil-litigation": dict(
    title="Civil Litigation in Lucknow | Ink & Equity",
    desc="A plain guide to civil suits, injunctions, money recovery, appeals and execution in India. Ink & Equity, advocates in Lucknow.",
    h1="Civil litigation",
    lede="Civil suits for money, property, contract and injunctions, and the appeals and execution proceedings that follow.",
    sections=[
        ("What this covers", """<ul>
<li>Civil suits in the trial courts, including plaint drafting, written statements and interim applications.</li>
<li>Temporary and permanent injunctions, and status quo orders.</li>
<li>Recovery of money, damages and summary suits on written contracts or negotiable instruments.</li>
<li>Appeals, revisions and review applications.</li>
<li>Execution of decrees, and enforcement of settlements.</li>
</ul>"""),
        ("Governing law", """<p>Civil procedure in India is governed by the Code of Civil Procedure, 1908. Limitation periods are governed by the Limitation Act, 1963. Specific Relief Act, 1963 governs remedies such as specific performance and injunctions. Commercial disputes above the monetary threshold may be heard under the Commercial Courts Act, 2015. Each state may add its own rules and court fee requirements.</p>"""),
        ("Papers that usually matter", """<ul>
<li>The agreement, deed, cheque or other document on which the claim rests.</li>
<li>Correspondence, notices and replies, in date order.</li>
<li>Records of payment, possession or default.</li>
<li>Any earlier orders or decrees in the same matter.</li>
</ul>"""),
    ],
    faq=[
        ("How long does a civil suit take?", "Timelines depend on the court's caseload, the stage of the matter and whether the parties settle. No fixed time can be given in advance."),
        ("What is an interim injunction?", "A temporary order that preserves the position of the parties until the suit is decided. It is granted only if the legal test for it is met."),
    ]),
"commercial-and-contract-disputes": dict(
    title="Commercial and Contract Disputes | Ink & Equity",
    desc="Guidance on breach of contract, supply and distribution disputes, payment defaults and commercial suits in India. Ink & Equity, Lucknow.",
    h1="Commercial and contract disputes",
    lede="Disputes over contracts, supply, distribution, services and payment, from the demand notice to the court or tribunal.",
    sections=[
        ("What this covers", """<ul>
<li>Breach of contract, damages and restitution.</li>
<li>Non-payment for goods or services, and disputes over invoices.</li>
<li>Distribution, dealership, agency and franchise disputes.</li>
<li>Termination, force majeure and limitation-of-liability issues.</li>
<li>Negotiated settlements and mediation.</li>
</ul>"""),
        ("Where these matters are heard", """<p>Commercial disputes may be heard by civil courts or, where the Commercial Courts Act, 2015 applies, by commercial courts or commercial divisions. Contracts with an arbitration clause are generally referred to arbitration (see the arbitration page).</p>"""),
        ("Early steps that matter", """<ul>
<li>Read the contract's governing law, jurisdiction and dispute-resolution clauses first.</li>
<li>Send a clear demand or notice, and keep proof of delivery.</li>
<li>Gather invoices, purchase orders, delivery records and emails.</li>
<li>Check limitation periods early.</li>
</ul>"""),
    ],
    faq=[
        ("Should a legal notice be sent before filing a suit?", "It is often sensible, and in some cases a notice is required by the contract or the law. Whether it is needed depends on the facts."),
        ("Does a contract's arbitration clause stop a court case?", "Generally a court must refer parties to arbitration where a valid arbitration agreement exists and a party asks for it, subject to the Arbitration and Conciliation Act, 1996."),
    ]),
"arbitration-and-adr": dict(
    title="Arbitration and Dispute Resolution | Ink & Equity",
    desc="Guidance on domestic and international arbitration, setting aside and enforcement of awards, and mediation under Indian law. Ink & Equity, Lucknow.",
    h1="Arbitration and dispute resolution",
    lede="Resolving commercial disputes through arbitration and mediation, and challenging or enforcing arbitral awards.",
    sections=[
        ("What this covers", """<ul>
<li>Drafting arbitration clauses and reviewing existing ones.</li>
<li>Appointment and challenge of arbitrators.</li>
<li>Interim relief from courts before or during arbitration.</li>
<li>Challenges to awards under Section 34 of the Arbitration and Conciliation Act, 1996, and enforcement under Section 36.</li>
<li>Mediation and conciliation, including settlement agreements.</li>
</ul>"""),
        ("Governing law and time limits", """<p>The Arbitration and Conciliation Act, 1996 governs arbitration in India, including Part II for international commercial arbitration and the enforcement of foreign awards. An application to set aside a domestic award under Section 34 is generally made within three months of receiving the award, extendable by a further thirty days for sufficient cause. Limits must be checked against the facts.</p>"""),
        ("Papers that usually matter", """<ul>
<li>The contract containing the arbitration clause.</li>
<li>The notice invoking arbitration and any reply.</li>
<li>The statement of claim, defence and the award, with proof of the date it was received.</li>
</ul>"""),
    ],
    faq=[
        ("Is an arbitral award final?", "It can be challenged only on the limited grounds set out in the Act. Courts do not usually re-examine the merits."),
        ("Can a court grant interim relief during arbitration?", "Yes, in appropriate cases, under the Act. The test is applied to the facts of each case."),
    ]),
"criminal-law": dict(
    title="Criminal Law and Bail in Uttar Pradesh | Ink & Equity",
    desc="A plain guide to criminal complaints, bail, trials, appeals and quashing under the BNS, BNSS and BSA. Ink & Equity, Lucknow.",
    h1="Criminal law",
    lede="Criminal complaints, bail, trials and appeals under the Bharatiya Nyaya Sanhita, the Bharatiya Nagarik Suraksha Sanhita and the Bharatiya Sakshya Adhiniyam.",
    sections=[
        ("What this covers", """<ul>
<li>Complaints and information about cognizable offences, and remedies where a police report is not recorded.</li>
<li>Regular and anticipatory bail, and bail applications in the courts of session and the High Court.</li>
<li>Trials, evidence and procedural applications.</li>
<li>Appeals, revisions and applications to quash proceedings where the law allows.</li>
<li>Compounding and settlement where permitted.</li>
</ul>"""),
        ("Governing law", """<p>Since 1 July 2024, criminal matters are governed by the Bharatiya Nyaya Sanhita, 2023 (offences and punishments), the Bharatiya Nagarik Suraksha Sanhita, 2023 (procedure) and the Bharatiya Sakshya Adhiniyam, 2023 (evidence). The transition and savings provisions must be checked for the date of the offence and the stage of the case before any earlier law is relied on.</p>"""),
        ("Papers that usually matter", """<ul>
<li>The FIR or complaint, and the case diary or charge sheet where available.</li>
<li>Arrest and remand papers, and bail orders.</li>
<li>Medical and other reports, and the list of witnesses.</li>
<li>Proof of residence and surety documents for bail applications.</li>
</ul>"""),
    ],
    faq=[
        ("Can an FIR be registered at any police station?", "A complaint about a cognizable offence is ordinarily made to the police, and the procedure for recording it is set out in the BNSS. Remedies exist if the police do not act."),
        ("What is the difference between regular and anticipatory bail?", "Regular bail is sought after arrest. Anticipatory bail is sought before arrest, where a person apprehends arrest. Each depends on the offence and the facts."),
    ]),
"family-and-matrimonial": dict(
    title="Family and Matrimonial Matters | Ink & Equity",
    desc="Guidance on divorce, maintenance, child custody, domestic violence and family proceedings in India. Ink & Equity, advocates in Lucknow.",
    h1="Family and matrimonial matters",
    lede="Divorce, maintenance, custody, domestic violence and other family proceedings, handled with care for everyone affected, including children.",
    sections=[
        ("What this covers", """<ul>
<li>Divorce by mutual consent and contested divorce.</li>
<li>Judicial separation, nullity and restitution of conjugal rights, where relevant.</li>
<li>Maintenance and interim maintenance.</li>
<li>Child custody, guardianship and visitation.</li>
<li>Protection orders, residence orders and other relief under the Protection of Women from Domestic Violence Act, 2005.</li>
<li>Division of matrimonial property and financial disclosures.</li>
</ul>"""),
        ("Governing law", """<p>Matters are governed by personal laws (such as the Hindu Marriage Act, 1955 and the Muslim Personal Law as applicable) and the Special Marriage Act, 1954. Custody and guardianship are governed by the Guardians and Wards Act, 1890 and the relevant personal law. Maintenance may also be claimed under the provisions of the Bharatiya Nagarik Suraksha Sanhita, 2023.</p>"""),
        ("Sensitivity", """<p>Family matters involve children and private information. Content on this site, and any filing, avoids identifying children and keeps personal details confidential.</p>"""),
    ],
    faq=[
        ("Can a divorce be obtained by mutual consent?", "Under the Hindu Marriage Act, a mutual consent divorce generally involves a waiting period after the first petition. The law must be checked for the parties' personal law."),
        ("Does the Domestic Violence Act apply only to married women?", "The Act provides relief to women in domestic relationships. Whether it applies depends on the relationship and facts."),
    ]),
"succession-and-wills": dict(
    title="Succession, Wills and Probate | Ink & Equity",
    desc="Guidance on wills, probate, letters of administration, family settlements and inheritance disputes in India. Ink & Equity, Lucknow.",
    h1="Succession, wills and probate",
    lede="Planning inheritance through wills and settlements, and resolving disputes over estates after a death.",
    sections=[
        ("What this covers", """<ul>
<li>Drafting and reviewing wills.</li>
<li>Probate and letters of administration.</li>
<li>Succession under personal law and the Indian Succession Act, 1925.</li>
<li>Family settlements, partition and relinquishment deeds.</li>
<li>Disputes over inherited property and estate administration.</li>
</ul>"""),
        ("Governing law", """<p>Succession is governed by personal law where it applies, including the Hindu Succession Act, 1956, and by the Indian Succession Act, 1925 for other matters. Probate and letters of administration are sought from the competent court. The execution formalities for a will, including attestation, are set out in the Indian Succession Act, 1925 and must be checked for each case.</p>"""),
        ("Papers that usually matter", """<ul>
<li>The death certificate and the family tree.</li>
<li>Property documents, including registered deeds and records.</li>
<li>The will, and any earlier drafts or codicils.</li>
<li>Bank, insurance and other asset records.</li>
</ul>"""),
    ],
    faq=[
        ("Does a will need to be registered?", "Registration is not compulsory, but a registered will is easier to prove. The formalities of execution matter more than registration."),
        ("Is probate always required?", "Not always. Whether probate or letters of administration is required depends on the law, the asset and the institutions holding it."),
    ]),
"corporate-and-commercial": dict(
    title="Corporate and Commercial Law | Ink & Equity",
    desc="Guidance on forming and running companies, LLPs and partnerships, governance, and commercial documentation under Indian law. Ink & Equity, Lucknow.",
    h1="Corporate and commercial law",
    lede="Structuring and running businesses in India: company, LLP and partnership matters, governance, and the commercial documents that support them.",
    sections=[
        ("What this covers", """<ul>
<li>Choosing and forming a private company, LLP or partnership.</li>
<li>Shareholders' and partnership agreements.</li>
<li>Board and shareholder resolutions, and governance records.</li>
<li>Commercial documentation: supply, services, licence and confidentiality agreements.</li>
<li>Disputes between shareholders, partners and directors.</li>
</ul>"""),
        ("Governing law", """<p>The main statutes are the Companies Act, 2013, the Limited Liability Partnership Act, 2008 and the Indian Partnership Act, 1932. Foreign investment is regulated under the Foreign Exchange Management Act, 1999 and its rules. Compliance filings are generally made with the Ministry of Corporate Affairs. Filings should be handled with a qualified company secretary or accountant as needed.</p>"""),
        ("Scope note", """<p>This practice gives legal advice and drafts documents. Regulated company secretarial certification and audit work are not included unless separately qualified.</p>"""),
    ],
    faq=[
        ("Should a startup form a company or an LLP?", "It depends on funding plans, the number of owners and tax and regulatory factors. This is a decision to make with advice on the facts."),
        ("Who signs board resolutions?", "The directors or authorised persons, as provided by the Companies Act and the company's articles."),
    ]),
"mergers-acquisitions-and-investment": dict(
    title="Mergers, Acquisitions and Investment | Ink & Equity",
    desc="Guidance on due diligence, investment agreements, shareholders' agreements and transaction documents in India. Ink & Equity, Lucknow.",
    h1="Mergers, acquisitions and investment",
    lede="Supporting share purchases, investments and business transfers, with the legal review and documents each transaction needs.",
    sections=[
        ("What this covers", """<ul>
<li>Legal due diligence on corporate, contract, property, employment and litigation records.</li>
<li>Share purchase, asset purchase and business transfer agreements.</li>
<li>Investment agreements, shareholders' agreements and articles of association.</li>
<li>Conditions precedent, representations, warranties and indemnities.</li>
<li>Closing checklists and post-closing matters.</li>
</ul>"""),
        ("Regulatory points", """<p>Transactions may require approvals or filings under the Companies Act, 2013, the Competition Act, 2002, FEMA and sector-specific regulation. Financial, tax and valuation advice is usually provided by other professionals and is coordinated with the legal team.</p>"""),
        ("Scope note", """<p>The scope of each engagement is agreed in writing. Specialised financial, tax and technical advice is outside the scope of legal review unless separately agreed and qualified.</p>"""),
    ],
    faq=[
        ("What is due diligence?", "A review of a target company's records and obligations, to identify risks before a deal closes."),
        ("Does a shareholders' agreement override the articles?", "Between the parties, it can give rights and obligations. The articles of the company still govern its internal affairs, so both should be consistent."),
    ]),
"intellectual-property": dict(
    title="Intellectual Property Law in India | Ink & Equity",
    desc="Guidance on trade marks, copyright, designs and patents in India: ownership, licensing, infringement and enforcement. Ink & Equity, Lucknow.",
    h1="Intellectual property",
    lede="Protecting and enforcing trade marks, copyright and designs, and advising on ownership and licences of intellectual property.",
    sections=[
        ("What this covers", """<ul>
<li>Trade mark clearance, applications, oppositions and infringement and passing off.</li>
<li>Copyright ownership, assignment, licensing and infringement, including takedowns.</li>
<li>Design registration and enforcement.</li>
<li>Employee and contractor IP ownership and confidentiality agreements.</li>
<li>IP due diligence in transactions.</li>
</ul>"""),
        ("Governing law", """<p>The main statutes are the Trade Marks Act, 1999, the Copyright Act, 1957, the Designs Act, 2000, the Patents Act, 1970 and the Geographical Indications of Goods (Registration and Protection) Act, 1999. Patent prosecution is generally handled through registered patent agents, and this practice coordinates with them where required.</p>"""),
        ("Scope note", """<p>Patent drafting and prosecution are not offered as a patent agent service unless the practice is so registered. Foreign filings are handled through local counsel.</p>"""),
    ],
    faq=[
        ("Is a trade mark registration the same as ownership?", "Registration gives statutory rights and evidence of ownership. Use and reputation also matter in disputes."),
        ("Does copyright need registration?", "Copyright arises on creation for protected works. Registration is useful evidence but is not a precondition in most cases."),
    ]),
"data-privacy-and-technology": dict(
    title="Data Privacy and Technology Law | Ink & Equity",
    desc="Guidance on privacy notices, data protection, IT Act issues, software contracts and online platform terms in India. Ink & Equity, Lucknow.",
    h1="Data, privacy and technology law",
    lede="Privacy notices, data protection compliance, software and platform contracts, and the IT Act issues businesses face online.",
    sections=[
        ("What this covers", """<ul>
<li>Privacy notices, consent and data processing terms.</li>
<li>Vendor, cloud and SaaS agreements, including data-processing clauses.</li>
<li>Website and app terms of use and privacy policies.</li>
<li>Responding to data incidents and related notices.</li>
<li>Online intermediary and content takedown issues.</li>
</ul>"""),
        ("Governing law", """<p>The Digital Personal Data Protection Act, 2023 governs digital personal data. Its rules and commencement timeline must be checked before advice is given. The Information Technology Act, 2000 and its rules govern electronic records, intermediaries and cyber offences. Sector regulators may impose additional requirements.</p>"""),
        ("Scope note", """<p>Technical security certification and forensic work are outside legal scope and are coordinated with qualified technical professionals.</p>"""),
    ],
    faq=[
        ("Does a privacy policy make a website compliant?", "A policy is one part of compliance. Actual data practices, consent and contracts must also match it."),
        ("Who is a data fiduciary?", "Under the DPDP Act, a data fiduciary decides the purpose and means of processing. The role depends on the facts and should be assessed for each arrangement."),
    ]),
"tax-customs-and-fema": dict(
    title="Tax, Customs and FEMA Matters | Ink & Equity",
    desc="Guidance on income tax notices, GST disputes, customs matters and FEMA compliance in India. Ink & Equity, Lucknow.",
    h1="Tax, customs and FEMA",
    lede="Responding to tax notices and appeals, customs and GST disputes, and foreign exchange compliance for businesses and individuals.",
    sections=[
        ("What this covers", """<ul>
<li>Income-tax notices, assessments, penalties and appeals.</li>
<li>GST registration, classification, input tax credit disputes, refunds and appeals.</li>
<li>Customs classification, valuation and duty disputes.</li>
<li>FEMA and Reserve Bank of India compliance for inward and outward remittances, and foreign investment reporting.</li>
</ul>"""),
        ("Scope note", """<p>Tax planning and tax computation are handled with qualified tax professionals. This practice does not promise tax outcomes. Tax and FEMA positions depend on the year, the facts and the current law, which must be checked before advice is given.</p>"""),
        ("Time limits", """<p>Notices carry deadlines for reply and appeal, and missing them can have serious consequences. Dates on any notice should be recorded at once.</p>"""),
    ],
    faq=[
        ("What should I do on receiving a tax notice?", "Record the date, note the deadline for reply, and seek advice before responding. Do not ignore the notice."),
        ("Can GST input tax credit be claimed on every purchase?", "Only where the conditions in the GST law are met. The conditions depend on the facts."),
    ]),
"employment-and-labour": dict(
    title="Employment and Labour Law | Ink & Equity",
    desc="Guidance on employment contracts, terminations, workplace claims, POSH compliance and labour law in India. Ink & Equity, Lucknow.",
    h1="Employment and labour",
    lede="Employment contracts, terminations, workplace claims and compliance with labour and workplace-safety laws.",
    sections=[
        ("What this covers", """<ul>
<li>Employment, consultancy and independent contractor agreements.</li>
<li>HR policies, handbooks and disciplinary procedures.</li>
<li>Termination, notice, severance and employee claims.</li>
<li>Gratuity, provident fund and wage disputes.</li>
<li>Compliance under the Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013.</li>
<li>Restrictive covenants and confidentiality, subject to enforceability.</li>
</ul>"""),
        ("Governing law", """<p>Labour law has been reorganised under the four Labour Codes. Commencement, rules and state-specific provisions must be checked for each matter before advice is given. Industrial disputes are heard before the authorities and tribunals set up under the relevant law.</p>"""),
        ("Papers that usually matter", """<ul>
<li>The employment contract, offer letter and policies.</li>
<li>Attendance, salary and payment records.</li>
<li>The termination or disciplinary letters and replies.</li>
</ul>"""),
    ],
    faq=[
        ("Can an employer stop an employee from joining a competitor?", "Restrictive covenants are enforceable only to the extent the law allows. Enforceability depends on the terms and the facts."),
        ("What is a POSH Internal Committee?", "A committee that every workplace with ten or more employees must set up under the POSH Act, 2013 to receive complaints."),
    ]),
"consumer-protection": dict(
    title="Consumer Protection and Complaints | Ink & Equity",
    desc="Guidance on consumer complaints against sellers, service providers, builders, banks and insurers under the Consumer Protection Act, 2019.",
    h1="Consumer protection",
    lede="Complaints about defective goods, deficient services, unfair trade practices, and disputes with builders, banks and insurers.",
    sections=[
        ("What this covers", """<ul>
<li>Defective goods and deficient services.</li>
<li>Unfair trade practices and misleading advertisements.</li>
<li>Real estate and builder delay complaints.</li>
<li>Banking, insurance and telecom complaints, where the forum allows.</li>
<li>Appeals from consumer commissions.</li>
</ul>"""),
        ("Governing law and forums", """<p>The Consumer Protection Act, 2019 provides for complaints before District, State and National Consumer Commissions. Which commission hears a complaint depends on the value of the claim, and the pecuniary limits set by the rules must be checked. Complaints may also be filed electronically.</p>"""),
        ("Limitation", """<p>A complaint is generally made within two years from the cause of action, subject to the Act's provisions for condonation of delay. The date should be confirmed for each case.</p>"""),
    ],
    faq=[
        ("Is a lawyer needed to file a consumer complaint?", "Not necessarily. A complainant may file in person or through an authorised representative."),
        ("Can a consumer complaint be filed online?", "The Act and the rules allow electronic filing through the official portal. The current procedure should be checked."),
    ]),
"banking-recovery-and-insolvency": dict(
    title="Banking Recovery and Insolvency Matters | Ink & Equity",
    desc="Guidance on loan defaults, SARFAESI, debt recovery and the Insolvency and Bankruptcy Code in India. Ink & Equity, Lucknow.",
    h1="Banking, recovery and insolvency",
    lede="Loan defaults, security enforcement, debt recovery and matters under the Insolvency and Bankruptcy Code, 2016.",
    sections=[
        ("What this covers", """<ul>
<li>Loan and facility agreements, and default notices.</li>
<li>Security enforcement and challenges under the SARFAESI Act, 2002.</li>
<li>Recovery proceedings before the Debt Recovery Tribunals under the Recovery of Debts and Bankruptcy Act, 1993.</li>
<li>Corporate insolvency resolution, creditor claims and personal guarantor matters under the IBC.</li>
<li>Negotiated restructuring and settlement.</li>
</ul>"""),
        ("Scope note", """<p>An advocate does not act as an insolvency professional. Insolvency professional and regulated roles are performed by registered professionals. This practice advises on legal rights and proceedings and coordinates with them.</p>"""),
        ("Time limits", """<p>Time limits under the SARFAESI Act, the IBC and the Limitation Act are strict. They must be checked against the default and the stage of the proceedings.</p>"""),
    ],
    faq=[
        ("Can a bank take possession of a mortgaged property without a court order?", "Under the SARFAESI Act, a secured creditor may take steps after notice, subject to the Act's procedure. The steps must be followed exactly, and challenges are available."),
        ("What is a corporate insolvency resolution process?", "A time-bound process under the IBC in which creditors and a resolution professional manage the company's affairs and look for a resolution plan."),
    ]),
"competition-and-regulatory": dict(
    title="Competition and Regulatory Matters | Ink & Equity",
    desc="Guidance on Competition Act issues, regulatory show-cause notices and appeals against regulators in India. Ink & Equity, Lucknow.",
    h1="Competition and regulatory matters",
    lede="Responding to competition and sector regulators, and appealing regulatory decisions.",
    sections=[
        ("What this covers", """<ul>
<li>Anti-competitive agreements and abuse of dominance under the Competition Act, 2002.</li>
<li>Merger filing assessment.</li>
<li>Show-cause notices and replies to regulators.</li>
<li>Appeals against regulatory orders, where the statute allows.</li>
</ul>"""),
        ("Governing law", """<p>The Competition Act, 2002 is administered by the Competition Commission of India, and sector regulators such as those for telecom, electricity, insurance and securities have their own laws. Appeals lie to the forum set by each statute. Procedures and timelines should be checked for each regulator.</p>"""),
        ("Scope note", """<p>Economic and technical analysis is coordinated with qualified economists and technical experts where required.</p>"""),
    ],
    faq=[
        ("What should be done on receiving a show-cause notice?", "Note the deadline for reply and seek advice before replying. A reply should be accurate and consistent with the record."),
        ("Can a regulatory order be appealed?", "Where the statute provides for an appeal, yes. The forum and the time limit depend on the regulator and the statute."),
    ]),
"environment-energy-and-infrastructure": dict(
    title="Environment, Energy and Infrastructure Law | Ink & Equity",
    desc="Guidance on environmental clearances, pollution proceedings, power contracts and infrastructure disputes in India. Ink & Equity, Lucknow.",
    h1="Environment, energy and infrastructure",
    lede="Environmental clearances and pollution matters, power purchase and project contracts, and infrastructure disputes.",
    sections=[
        ("What this covers", """<ul>
<li>Environmental clearance and compliance under the Environment (Protection) Act, 1986 and the EIA Notification, 2006.</li>
<li>Pollution control consents and proceedings under the Water and Air Acts.</li>
<li>Proceedings before the National Green Tribunal under the NGT Act, 2010.</li>
<li>Power purchase agreements and disputes under the Electricity Act, 2003.</li>
<li>Construction, EPC and concession contract disputes.</li>
</ul>"""),
        ("Scope note", """<p>Environmental impact assessment and technical studies are prepared by qualified consultants. Legal review covers approvals, compliance and disputes.</p>"""),
        ("Time limits", """<p>Appeals to the National Green Tribunal and to other forums are subject to time limits that must be checked against the order.</p>"""),
    ],
    faq=[
        ("Is an environmental clearance always needed for a project?", "It depends on the project category and size under the EIA Notification, 2006, as amended."),
        ("Which forum hears environmental disputes?", "The National Green Tribunal hears many environmental disputes, subject to its jurisdiction and time limits."),
    ]),
"insurance-and-claims": dict(
    title="Insurance Claims and Disputes | Ink & Equity",
    desc="Guidance on rejected or delayed insurance claims, policy interpretation and insurance disputes in India. Ink & Equity, Lucknow.",
    h1="Insurance and claims",
    lede="Rejected, delayed or disputed insurance claims, and the interpretation of policy terms.",
    sections=[
        ("What this covers", """<ul>
<li>Life, health, motor, property and commercial policy claims.</li>
<li>Repudiation, partial settlement and delay in settling claims.</li>
<li>Interpretation of exclusions and conditions.</li>
<li>Complaints to the Insurance Ombudsman and consumer commissions.</li>
<li>Professional indemnity and directors' liability cover.</li>
</ul>"""),
        ("Where these matters are heard", """<p>Complaints may be made to the Insurance Ombudsman, to consumer commissions under the Consumer Protection Act, 2019, or to civil courts, depending on the claim and the forum's limits. The Insurance Act, 1938 and IRDAI regulations govern many aspects.</p>"""),
        ("Papers that usually matter", """<ul>
<li>The policy with its schedule and terms.</li>
<li>The proposal form and any medical or other reports.</li>
<li>The claim form, correspondence and the repudiation letter.</li>
</ul>"""),
    ],
    faq=[
        ("What if an insurer rejects a claim?", "Ask in writing for the reasons. The policy terms and the facts decide whether the rejection can be challenged."),
        ("Is there a limit on claims before the Insurance Ombudsman?", "Yes, the Ombudsman's jurisdiction is limited by the value of the claim as set by the rules."),
    ]),
"healthcare-education-and-professional-regulation": dict(
    title="Healthcare and Education Matters | Ink & Equity",
    desc="Guidance on school and university disputes, admissions, fee issues and disciplinary proceedings for professionals in India.",
    h1="Healthcare, education and professional bodies",
    lede="Disputes involving schools, universities, admissions and fees, and disciplinary proceedings before professional councils.",
    sections=[
        ("What this covers", """<ul>
<li>Admission, examination, result and affiliation disputes.</li>
<li>Student fee and refund disputes.</li>
<li>Employment disputes in educational institutions.</li>
<li>Disciplinary proceedings before professional councils.</li>
<li>Contracts with hospitals and healthcare providers, and related consumer complaints.</li>
</ul>"""),
        ("Governing law", """<p>Education matters are governed by the statutes, regulations and university ordinances that apply to each institution. Professional conduct is governed by the regulatory council for each profession. Healthcare negligence complaints may be made under the Consumer Protection Act, 2019 or in civil or criminal proceedings, depending on the facts.</p>"""),
        ("Scope note", """<p>Clinical and technical assessment is provided by qualified medical and other professionals. Legal review does not replace their opinion.</p>"""),
    ],
    faq=[
        ("Can a student challenge a university decision?", "Usually through the university's own remedies first, then a writ or other forum where the law allows."),
        ("Can a patient complain about medical negligence?", "A complaint may be made to a consumer commission or a civil or criminal court, subject to the forum's rules and time limits."),
    ]),
"media-entertainment-and-sports": dict(
    title="Media, Entertainment and Sports Law | Ink & Equity",
    desc="Guidance on production and talent contracts, licensing, takedowns, defamation and personality rights in India. Ink & Equity, Lucknow.",
    h1="Media, entertainment and sports",
    lede="Contracts for creators, production houses and talent, licensing, takedowns, and reputation and personality rights.",
    sections=[
        ("What this covers", """<ul>
<li>Production, talent, management and endorsement agreements.</li>
<li>Music, publishing and royalty agreements.</li>
<li>Copyright licensing and takedown requests.</li>
<li>Defamation and reputation-related matters.</li>
<li>Personality, publicity and privacy rights.</li>
</ul>"""),
        ("Governing law", """<p>The Copyright Act, 1957, the Trade Marks Act, 1999, the Information Technology Act, 2000 and the law of defamation and privacy apply. Courts in India have recognised personality rights in several cases, and the law continues to develop. Current decisions must be checked before advice is given.</p>"""),
        ("Scope note", """<p>Client work is taken on only after confirming the practice's capability and any conflicts.</p>"""),
    ],
    faq=[
        ("Can a creator take down content that copies their work?", "Where the work is protected and the copying is not permitted, takedown and other remedies may be available under the relevant platform rules and the law."),
        ("Is defamation a civil or criminal matter?", "In India, defamation can be pursued both as a civil wrong and as a criminal offence. Each route has its own procedure and limits."),
    ]),
"non-profit-trusts-and-societies": dict(
    title="Trusts, Societies and Non-Profits | Ink & Equity",
    desc="Guidance on trust deeds, society governance, Section 8 companies, donations and funding agreements in India. Ink & Equity, Lucknow.",
    h1="Trusts, societies and non-profits",
    lede="Setting up and governing trusts, societies and non-profit companies, and the agreements they rely on.",
    sections=[
        ("What this covers", """<ul>
<li>Trust deeds and trustee duties under the Indian Trusts Act, 1882.</li>
<li>Society formation and governance under the Societies Registration Act, 1860 and applicable state law.</li>
<li>Section 8 companies under the Companies Act, 2013.</li>
<li>Donation, grant and funding agreements.</li>
<li>Disputes between trustees, members and governing bodies.</li>
</ul>"""),
        ("Scope note", """<p>Tax exemption and foreign contribution approvals depend on specific rules and are reviewed with qualified tax and regulatory professionals. This practice does not imply that any exemption or approval has been obtained.</p>"""),
        ("Governing law", """<p>Registration, governance, tax and foreign contribution rules apply in addition to the trust, society or company law. The applicable state law and the current rules should be checked for each organisation.</p>"""),
    ],
    faq=[
        ("Is a trust the same as a society?", "No. A trust is created by a deed and is governed by trust law. A society is a registered body of members, governed by its memorandum and rules."),
        ("Does a Section 8 company need to be registered?", "Yes. It is incorporated under the Companies Act, 2013 and must meet the licence and compliance conditions set by the Act."),
    ]),
"cross-border-and-nri-matters": dict(
    title="Cross-Border and NRI Matters | Ink & Equity",
    desc="Guidance on Indian property, succession, documents and disputes for NRIs, and on international contracts and arbitral awards. Ink & Equity, Lucknow.",
    h1="Cross-border and NRI matters",
    lede="Indian property, succession and documents for NRIs, and cross-border contracts and disputes. Foreign law is handled by counsel qualified in that jurisdiction.",
    sections=[
        ("Indian law", """<ul>
<li>Indian property purchase, sale and disputes, with remittance and FEMA compliance.</li>
<li>Inheritance and probate of Indian assets.</li>
<li>Power of attorney and the execution and attestation of documents.</li>
<li>Recognition and enforcement of foreign arbitral awards in India under Part II of the Arbitration and Conciliation Act, 1996.</li>
<li>Recognition of foreign judgments under the Code of Civil Procedure, 1908.</li>
</ul>"""),
        ("Foreign law", """<p>This practice does not advise on the domestic law of any foreign country and is not admitted to practise there. Where foreign law applies, the matter is referred to appropriately qualified counsel in that jurisdiction. Any coordination is described to the client in writing.</p>"""),
        ("Documents and identity", """<p>Documents executed abroad generally need to be attested or apostilled as required for use in India. The requirements depend on the country and the purpose and should be checked before execution.</p>"""),
    ],
    faq=[
        ("Can an NRI sell property in India through a power of attorney?", "A power of attorney can authorise an agent to act, but title is transferred through a registered conveyance. The powers granted and the documents needed must be checked."),
        ("Can a foreign arbitral award be enforced in India?", "Under Part II of the Arbitration and Conciliation Act, 1996, a foreign award may be enforced if the statutory conditions are met."),
    ]),
"government-procurement-and-rti": dict(
    title="Government Contracts, RTI and Grievances | Ink & Equity",
    desc="Guidance on tender disputes, blacklisting, Right to Information appeals and public grievances in Uttar Pradesh and India. Ink & Equity, Lucknow.",
    h1="Government contracts, RTI and public grievances",
    lede="Challenging tender decisions and blacklisting, seeking information under the Right to Information Act, and pursuing public grievances.",
    sections=[
        ("What this covers", """<ul>
<li>Tender eligibility, evaluation and award challenges.</li>
<li>Performance security, termination and blacklisting.</li>
<li>Public-private partnership and concession disputes.</li>
<li>Requests and appeals under the Right to Information Act, 2005.</li>
<li>Public grievances and administrative representations.</li>
</ul>"""),
        ("Where these matters are heard", """<p>Tender and contract disputes are generally pursued through the contract's dispute clause, through the High Court by writ where the State's action is arbitrary, or through arbitration where the contract provides it. RTI appeals lie first to the authority designated under the Act and then to the State Information Commission.</p>"""),
        ("Time limits", """<p>RTI applications and appeals have time limits under the Act. Tender challenges are often time-sensitive, and dates should be recorded as soon as the decision is received.</p>"""),
    ],
    faq=[
        ("Can an RTI application be refused?", "Only on the grounds set out in the Act. A refusal can be appealed."),
        ("Can a blacklisting order be challenged?", "Yes. The order can be challenged in the appropriate forum, subject to the contract and the law."),
    ]),
}
