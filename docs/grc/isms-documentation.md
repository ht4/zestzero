# ZestZero | GRC operations and ISMS documentation

| Document control | Value |
|---|---|
| Document ID | ZZ-GRC-001 |
| Version | 0.1 |
| Status | Draft for portfolio review |
| Proposed owner | Project maintainer |
| Review cycle | After material changes; proposed quarterly review |
| Classification | Public — synthetic laboratory |
| Related register | [security-register.xlsx](security-register.xlsx) |

## 1. Purpose and scope

ZestZero is an independent LegalTech security assurance laboratory. This
document defines a proposed, lightweight Information Security Management
System (ISMS) operating model for its source repository, deterministic
retrieval and authorization fixture, synthetic documents, CI workflow,
published evidence and research metrics. It is a training exercise,
not an operational or certified ISMS.

The public demonstration is static; local execution uses FastAPI. There
is no production authentication, real client information, generative LLM,
customer SLA or third-party security testing. Intentionally defective
configurations must remain isolated from real information. ContractNLI
evidence-ranking metrics are separate from confidentiality checks.

## 2. Proposed information security policy

- Protect confidentiality, integrity and availability according to asset
  classification and risk.
- Use fictional identities and documents only in the assurance fixture.
- Require least privilege and current authorization; revoke access when
  no longer justified.
- Preserve traceable evidence without exporting private information.
- Treat automated pass results as input to human review, never as formal
  release approval or certification.
- Escalate uncertain legal, privacy and security decisions to a qualified
  reviewer in a real organization.

## 3. Document and version control

Indicative ISO/IEC 27001:2022 references: clauses 5.2 and 7.5.

The proposed owner maintains document IDs, versions, status, scope, change
summaries and evidence references. Changes are reviewed through Git diffs
before commit. In a real team, a designated independent approver records
approval and date before controlled publication. Superseded versions
remain identifiable through repository history. Never commit credentials,
personal information or private evidence.

| Version | Change | Review |
|---|---|---|
| 0.1 | Initial GRC register and operating procedures | Pending maintainer review |

## 4. Asset management and risk assessment

Indicative references: clause 6.1.2 and Annex A 5.9.

1. Record each information asset, type, classification, criticality,
   proposed owner and source in the Asset Inventory worksheet.
2. Link each risk to the affected asset and relevant check identifier.
3. Estimate likelihood and impact independently on a 1–5 scale: 1 very
   low, 2 low, 3 moderate, 4 high, 5 very high.
4. Multiply likelihood by impact. Proposed priority bands: 1–4 low,
   5–9 moderate, 10–16 high, 17–25 very high. Escalate significant
   confidentiality exposures regardless of the calculated band.
5. Record planned controls and provisional residual scores. A passing
   check does not establish real-world likelihood or risk acceptance.
6. Review after changes in data, permission logic, dependencies or
   deployment conditions.

The register includes the six intentional baseline failures ZZ-02
through ZZ-07, not a complete enterprise risk assessment. Scores and
criticality are exercise assumptions, not observed probabilities.

## 5. Risk treatment and release review

Indicative references: clause 6.1.3 and Annex A 5.15–5.18, 5.33.

The proposed owner records a treatment action, due date, responsible
role, linked evidence and review status. Test the corrected configuration,
retain the result and escalate unresolved high-impact findings. The
recorded baseline failed six of nine checks; the corrected snapshot
passed nine of nine and is eligible for human review. No risk has been
formally accepted or closed by this exercise. In a real ISMS, designated
risk owners approve residual risk and maintain an applicable controls
statement; neither is asserted here.

## 6. Access and confidentiality procedure

Indicative references: Annex A 5.15–5.18.

For the laboratory, use the existing synthetic identities and matter
permissions. Verify that each retrieval and derived-content operation
honors current access, including after revocation. Reject unknown
identities and unsupported requests. Review active document versions and
retain source identifiers. For repository administration, proposed
controls are MFA, least privilege and periodic access review; actual
account settings are not verified in this pack.

## 7. Third-party due diligence and customer questionnaires

Indicative references: Annex A 5.19–5.23.

The Vendor Due Diligence worksheet exercises screening of a fictional
document-sharing supplier. The scenario assumes synthetic-only data;
confirm actual scope and risk tier before any real supplier approval.
Collect evidence on access, encryption, incident reporting, privacy,
subprocessors, retention, continuity and assurance scope. Record evidence
received, gaps, reviewer and next steps. Never treat unanswered items as
compliant. The sample decision is HOLD until evidence gaps are resolved.

For customer security questionnaires, use approved scope-specific
responses and link supporting records. Mark unknown or inapplicable
controls explicitly; escalate contractual and regulatory questions. The
sample Security Questionnaire describes ZestZero only; it is not an
answer on behalf of any real company.

## 8. Audit evidence management

Indicative reference: clause 7.5 and Annex A 5.33.

Record evidence ID, check ID, source, execution date, observed result
and review status. Link baseline and corrected runs separately. Preserve
original JSON records and use Git history to locate the relevant version.
SHA-256 fingerprints support comparison and integrity checks but do not
establish signer authenticity or tamper-proof storage. The Audit Evidence
worksheet indexes a recorded snapshot and does not constitute an audit
opinion.

## 9. Incident response and vulnerability management

Indicative references: Annex A 5.24–5.28 and 8.8.

For a simulated incident, register the finding, severity, affected assets,
time, proposed owner and evidence. Triage, contain, investigate, remediate,
retest and obtain human closure. The Incident Register contains tabletop
examples of intentional test defects, not actual breaches.

For vulnerability scanning, use an authorized, isolated test environment.
Record tool and version, scope, time, findings, false-positive review,
severity and remediation evidence. Do not scan GitHub Pages, third-party
systems or real customer assets without explicit permission. This pack
does not include or claim a Nessus scan of ZestZero.

## 10. Privacy and secure AI usage

Indicative reference: Annex A 5.34.

Keep personal data and client-confidential content out of the public
laboratory. If applying the methodology in a real LATAM organization,
identify the applicable jurisdictions, controller/processor roles,
lawful basis, notices, data-subject rights, retention, transfers and
incident obligations; escalate to legal/privacy staff before processing.

Study references (jurisdictional applicability must be assessed):
- Chile: Laws 19.628 and 21.719; consult the [Biblioteca del Congreso Nacional](https://www.bcn.cl/leychile/).
- Peru: Law 29733 and D.S. 016-2024-JUS; consult the [ANPD](https://www.gob.pe/anpd).
- Mexico: LFPDPPP; consult the [Diario Oficial de la Federación](https://www.dof.gob.mx/).
- Colombia: Law 1581; consult the [Superintendencia de Industria y Comercio](https://www.sic.gov.co/).

These references are study signposts, not a legal applicability or
compliance assessment. No statutory deadlines are asserted.

When using external AI tools to summarize or draft, use only approved
tools and permitted data; remove confidential identifiers and secrets,
check outputs against original evidence, and obtain human review before
publication. ZestZero itself does not run a generative LLM.

## 11. Metrics, tickets, SLAs and continuous improvement

Indicative references: clauses 9.1 and 10.

Monitor pass rates by configuration, outstanding treatment reviews, and
time to respond to evidence requests. Define each metric's numerator,
denominator and population. For simulated tickets, record priority,
request, owner, target, elapsed time, status and evidence; escalate
missed targets. The workbook provides two explicitly fictional SLA
examples, not customer commitments or historical service performance.
The workbook does not demonstrate a live Jira integration.

Review findings and evidence quality after each material change. In a
real team, maintain a training and awareness record and review lessons
learned with the security manager.

## 12. Maintainer validation before publication

- [ ] Confirm the inventory and classifications against the local checkout.
- [ ] Review the proposed risk scores and justify one residual estimate.
- [ ] Trace each of the six treatment records to its baseline and corrected
      JSON check; retain the relevant commit identifier.
- [ ] Review the fictional vendor's missing evidence and explain the HOLD decision.
- [ ] Verify the customer questionnaire answers against the project scope.
- [ ] Test the KPI formulas in Excel or LibreOffice Calc; change one practice
      SLA example and confirm that the summary updates.
- [ ] Confirm no personal data, credentials or real customer claims are included.
- [ ] Record maintainer review in a new Git commit; leave independent approval
      and formal risk acceptance unclaimed.

## 13. References and limitations

- [Project README](https://github.com/ht4/zestzero/blob/main/README.md)
- [Assurance implementation](https://github.com/ht4/zestzero/blob/main/app/assurance.py)
- [Recorded assurance results](https://github.com/ht4/zestzero/blob/main/site/results.json)
- [Benchmark record](https://github.com/ht4/zestzero/blob/main/site/benchmark.json)
- [Pages workflow](https://github.com/ht4/zestzero/blob/main/.github/workflows/pages.yml)
- [ISO/IEC 27001 overview](https://www.iso.org/standard/27001)

References to clauses and Annex A are indicative study mappings, not
reproductions of the standard or claims of conformity. This draft must
be reviewed by the maintainer before being described as completed work.
