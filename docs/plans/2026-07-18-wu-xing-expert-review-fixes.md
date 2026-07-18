# Wu Xing Expert Review Fixes – Implementation Plan

Plan path: `docs/plans/2026-07-18-wu-xing-expert-review-fixes.md`  
Status: ready-for-execution  
Execution status: completed

<!-- GOAL_START -->
Goal: Make the Wu Xing cornerstone historically precise and source-auditable

Ziel. Validate the external expert review, correct the public Wu Xing learning page where the review is well supported, and preserve the existing Sizhu Learn design, embedded diagrams, CTA routing, accessibility, and Railway deployment. Readers must be able to distinguish classical textual anchors from modern reflective language without losing the page’s clarity.

Scope. Default branch `master`; build-time transformation in `scripts/apply_public_branding.py`; deterministic validation in `scripts/validate_public_content.py`; Railway build gate in `Dockerfile`; documentation under `docs/`.

Bedingungen (hart).
- Hanzi, tone-marked Pinyin, generating order, and controlling order remain unchanged unless evidence requires correction.
- Classical source claims must be passage-specific and separated from modern systems, coaching, organizational, medical, or diagnostic analogies.
- The existing visual system, embedded cycle images, responsive layout, Sizhu Shop CTA, and Bazodiac calculation CTA must remain functional.
- The build must fail when expected source passages cannot be transformed or required review outcomes are absent.

Akzeptanzkriterien.
- The categorical “phases instead of substances” sentence is replaced by a historically nuanced formulation.
- Each phase displays a classical operational anchor before modern interpretive shorthand.
- 相克 is described as checking, restraining, or overcoming; regulation is framed as a later functional interpretation.
- Balance, excess, and lack are explicitly labelled as a modern reflective analogy, not BaZi or medical assessment.
- The Metal-generates-Water explanation is identified as mnemonic teaching imagery, not a physical mechanism or universal derivation.
- Both diagrams state that layout positions show relational order rather than compass directions.
- Sources name the relevant texts/passages and include a published scholarly Huainanzi translation.
- Automated validation passes for required copy, forbidden legacy copy, Hanzi/Pinyin, JSON-LD, alt text, and build markers.

Explizit out-of-scope.
- Recalculating a personal BaZi chart or adding individualized interpretation.
- Redesigning the page, replacing the supplied cycle artwork, or changing the overall information architecture.
- Adding TCM, Feng Shui, dietary, medical, fate, wealth, love, or efficacy claims.
- Migrating the page to a framework, CMS, or shared multi-page repository.

Done-Definition. The expert-review transformation and validator run successfully during the Railway Docker build; the committed review record maps every accepted or rejected recommendation to evidence and implementation.

Reference-Doc: `docs/reviews/2026-07-18-wu-xing-expert-review-validation.md`
<!-- GOAL_END -->

## Evidence and source boundary

- User-provided expert review: `Eingefügter Text(11).txt`.
- Repository evidence: the public page is a large static HTML document with embedded cycle images; the current deployment already applies build-time corrections through `scripts/apply_public_branding.py`.
- Primary-text evidence: *Shangshu*, “Hong Fan”; *Bai Hu Tong*, “Wu Xing”; *Huainanzi*, “Dixing Xun”.
- Published translation evidence: Major, Queen, Meyer, and Roth, eds. and trans., *The Huainanzi*, Columbia University Press, 2010.
- Institutional secondary summary: Palace Museum entry on 相生相克.

## Assumptions, missing information, open questions, blockers

- ASSUMPTION: Railway remains connected to `master` and deploys after each GitHub commit.
- MISSING: authenticated Railway deployment logs and direct browser automation from this environment.
- OPEN QUESTION: the final custom-domain canonical remains a hosting decision; this patch preserves the current route architecture.
- BLOCKER: none for repository implementation. Live verification depends on Railway completing the deployment.

## Requirements

| ID | Requirement | Verification |
|---|---|---|
| REQ-F-001 | Nuance the historical substances/processes contrast. | New sentence present; old categorical sentence absent. |
| REQ-F-002 | Anchor phase descriptions in classical operations. | Five classical anchors appear before reflective questions. |
| REQ-F-003 | Clarify 相克 terminology. | Checking/restraining/overcoming present; automatic-balance claim absent. |
| REQ-F-004 | Label balance/excess/lack as modern analogy. | Heading and disclaimer present; pseudo-diagnostic wording absent. |
| REQ-F-005 | Qualify Metal → Water mnemonic. | No physical-mechanism claim; mnemonic status explicit. |
| REQ-F-006 | Add non-compass diagram note. | One note after each cycle figure. |
| REQ-F-007 | Make sources passage-specific. | Primary texts, scholarly translation, and institutional summary linked. |
| REQ-NF-001 | Preserve design, images, CTA links, responsiveness, and accessibility. | Embedded images, CTA targets, one H1, and alt text validate. |
| REQ-A-001 | Keep the change reversible and local to the static deployment pipeline. | Build-time transform plus validation; no framework migration. |
| REQ-O-001 | Expose a version marker for live deployment review. | `/version.txt` contains v6 review marker. |

## Architecture and file boundaries

Extend the existing deterministic build-time transformer and add a build-failing validator. This avoids rewriting a roughly 1.2 MB HTML file containing embedded images while keeping changes reviewable and reversible.

### Options considered

| Option | Benefit | Cost/Risk | Decision |
|---|---|---|---|
| Directly rewrite generated HTML | Final source contains all fixes | Large binary-like diff; image corruption and merge risk | Rejected |
| Build-time transformation + validator | Small diff, reversible, protects embedded assets | String matching can become brittle | Selected; fail-fast checks mitigate brittleness |
| Template/component migration | Best long-term maintainability | Large scope and deployment risk | Out of scope |

## Implementation phases

1. Validate the expert review against primary and scholarly sources.
2. Implement accepted corrections in the build transformer.
3. Add deterministic content, Hanzi/Pinyin, JSON-LD, and accessibility validation.
4. Run validation during the Docker build.
5. Commit the plan, review record, implementation, and tests.
6. Confirm GitHub and inspect the live version marker after Railway deploys.

## Tasks

### TASK-001: Document the evidence decision

Objective: Record which expert claims are accepted, qualified, or rejected.

Files/modules:
- Create: `docs/reviews/2026-07-18-wu-xing-expert-review-validation.md`

Steps:
1. Map each review item to primary, academic, institutional, or project evidence.
2. Mark unsupported statements as qualified rather than silently adopting them.
3. Record glyph policy and modern-analogy boundaries.

Acceptance criteria:
- Every requested content change has an evidence status and implementation decision.

Validation:
- Manual review for source traceability and no deterministic medical/fate claims.

Rollback note: Documentation can be reverted independently.

### TASK-002: Write content assertions first

Objective: Encode the expected post-review page state before relying on visual inspection.

Files/modules:
- Create: `scripts/validate_public_content.py`

Steps:
1. Assert required revised phrases and source references.
2. Assert removal of categorical and pseudo-diagnostic legacy wording.
3. Validate Hanzi and tone-marked Pinyin tokens.
4. Parse JSON-LD and verify one H1 and image alt text.
5. Assert one explanatory note per diagram and the expected build marker.

Acceptance criteria:
- Validator fails against the unmodified page and passes after transformation.

Validation:
- Command: `python scripts/validate_public_content.py`
- Expected result: `PASS`.

Rollback note: Remove the validator and Docker invocation without changing source HTML.

### TASK-003: Implement the expert-review transformation

Objective: Apply the smallest deterministic copy changes without touching embedded image payloads.

Files/modules:
- Modify: `scripts/apply_public_branding.py`

Steps:
1. Replace the historical framing paragraph.
2. Replace the phase section with classical anchors plus labelled modern questions.
3. Qualify the Metal → Water mnemonic.
4. Rewrite the 相克 introduction and heading.
5. Insert diagram interpretation notes without altering the supplied artwork.
6. Replace the balance section with explicitly modern reflective language.
7. Replace the source section with passage-specific references.
8. Update matching JSON-LD descriptions and citation URLs.
9. Fail the transformation if required source sections or phrases are missing.

Acceptance criteria:
- All functional requirements pass and embedded image payloads remain untouched.

Validation:
- Command: `python scripts/apply_public_branding.py && python scripts/validate_public_content.py`
- Expected result: transformation message followed by `PASS`.

Rollback note: Revert the transformer commit; original static HTML remains intact.

### TASK-004: Gate the Railway build

Objective: Prevent publishing a partial or stale transformation.

Files/modules:
- Modify: `Dockerfile`

Steps:
1. Run the transformer in the Python prepare stage.
2. Run the validator immediately afterward.
3. Copy validated output into the Caddy stage only after both commands pass.

Acceptance criteria:
- Docker build exits non-zero on missing correction, invalid JSON-LD, missing alt text, or wrong version marker.

Validation:
- Focused command: `python scripts/apply_public_branding.py && python scripts/validate_public_content.py`
- Deployment command: `docker build .` where Docker is available.

Rollback note: Restore the previous single transformer command.

### TASK-005: Review deployment and ticket state

Objective: Confirm published behavior and avoid closing unrelated work.

Files/modules:
- No code file.

Steps:
1. Confirm commits on `master`.
2. Check `/version.txt` for `wu-xing-2026-07-18-v6-expert-review` after Railway deploys.
3. Review the public copy, diagram notes, CTA links, and unchanged visual layout.
4. Inspect Jira BZG-31; add final review evidence if useful, but do not alter BZG-32 or future-page tickets.

Acceptance criteria:
- BZG-31 remains `Fertig`; no unrelated ticket is closed.

Validation:
- Live URL and Jira status check.

Rollback note: Railway can redeploy the previous commit.

## Validation strategy

- Focused transformation test against the original HTML fixture.
- Standard-library HTML and JSON-LD parsing.
- Required/forbidden copy assertions.
- Hanzi and Pinyin presence checks.
- Diagram-note cardinality checks.
- CTA target checks.
- Build/version marker checks.
- Manual source audit against primary and published references.

## Rollback and safety

- No database, API contract, user data, or calculation logic changes.
- Original embedded images remain untouched.
- The transformer is fail-fast; unexpected source changes block deployment instead of silently publishing mixed copy.
- Failure chain: source wording changes → transformer cannot find expected passage → build exits non-zero → Railway retains the previous healthy deployment.

## Execution handoff

Run from repository root:

```bash
python scripts/apply_public_branding.py
python scripts/validate_public_content.py
```

Then build/deploy through the existing Railway Docker pipeline. Verify `/version.txt`, the public copy, both CTAs, and the two diagram notes.

## Plausibility and truth self-check

- The plan does not claim that Wu Xing has one single ahistorical definition.
- Classical passages, modern shorthand, and reflective analogy are separated.
- The Palace Museum entry is not treated as a primary historical source.
- The Huainanzi community/AI English rendering is not used as the sole translation authority.
- The solution avoids a large generated-HTML rewrite.
- Acceptance criteria are binary and testable.
- Missing live-deployment access is explicit.
- Confirmation-bias check: the expert review was not accepted wholesale; central corrections were accepted because they align with primary text and source-quality concerns.
