## Outcome

Implements **BZG-33** at `/learn/wu-xing/tcm-organs/` as an English, source-oriented supporting guide to traditional Wu Xing organ correspondences.

## User result

Readers can distinguish historical Five-Phase, zang-fu, season, direction and emotion correspondences from modern biomedical anatomy and health claims.

## Source and claims status

- Primary/classical: *Huangdi Neijing Suwen* passages on Five Movements and the five zang/fu distinction.
- Scholarly control: Unschuld & Tessenow annotated translation; IEP Wuxing overview.
- Institutional terminology/safety: WHO 2022 terminology standard; NCCIH public information.
- User-supplied draft: used as a lead and unsafe-claim audit only, not as medical authority.
- Region policy: `CN_SIMPLIFIED`.
- `CONTEXTUAL_VARIANT`: Earth as center vs late summer/seasonal transitions; emotion translation families.
- Blocked from copy: diagnosis, treatment, prevention, dosage, efficacy, disease correlations and biomedical equivalence.

## Included

- [x] structured content source and full page
- [x] source inventory and claim matrix
- [x] visible disclaimer and system limits
- [x] canonical/OG/Twitter metadata and JSON-LD
- [x] semantic landmarks, skip link, focus, reduced motion and accessible table
- [x] stable analytics events
- [x] reciprocal Wu Xing hub link
- [x] Sizhu Atelier, Etsy and chart-calculation CTAs
- [x] sitemap and robots files
- [x] deterministic BZG-33 validator
- [ ] preview/browser evidence
- [ ] named qualified human review
- [ ] canonical production acceptance

## Validation

- Static: `python scripts/validate_tcm_organs.py`
- Existing hub: `python scripts/validate_public_content.py`
- Build: Dockerfile runs both validators before Caddy image creation.
- Browser/mobile, accessibility tooling and event emission: pending preview deployment.

## Release boundary

This PR does not prove publication. BZG-33 must remain open until the exact merge SHA is deployed and accepted at `https://sizhuatelier.shop/learn/wu-xing/tcm-organs/`.

## Dependencies

- BZG-29: open; this PR follows its intended canonical IA without claiming the dependency complete.
- BZG-30: open; this PR supplies page-specific source and claims artifacts without claiming the project-wide policy complete.
- BZG-31: done; its Wu Xing hub is the foundation page and receives a reciprocal card.
