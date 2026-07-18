# BZG-33 source inventory

## Scope

English supporting guide for `https://sizhuatelier.shop/learn/wu-xing/tcm-organs/`.

## Source classification

| ID | Source | Class | Confidence | Intended use | Limitation |
|---|---|---|---:|---|---|
| S001 | Jira BZG-33 and BZG-7 | primary project record | 5 | user outcome, canonical route, safety boundary, acceptance criteria | not a historical or medical authority |
| S002 | User-supplied draft `die_systemische_dynamik_des_wu_xing_eine_wissensc.md` | user_provided | 2 | leads, vocabulary, unsafe-claim audit | citations are incomplete; contains diagnosis, treatment and efficacy claims excluded from publication |
| S003 | *Huangdi Neijing Suwen*, “Great Discourse on the Five Movements,” Chinese Text Project | primary text access layer | 4 | phase, direction, zang, taste and emotion correspondences | website translation is not treated as the sole critical edition |
| S004 | *Huangdi Neijing Suwen*, “Discourse on the Five Zang Organs,” Chinese Text Project | primary text access layer | 4 | distinction between zang storage language and fu transmission/transformation language | historical medical concepts are not modern anatomy |
| S005 | Paul U. Unschuld and Hermann Tessenow, *Huang Di Nei Jing Su Wen: An Annotated Translation*, UC Press, 2011 | scholarly primary-text translation | 5 | translation control and historical context | copyrighted book; referenced, not reproduced |
| S006 | Internet Encyclopedia of Philosophy, “Wuxing (Wu-hsing)” | secondary scholarly reference | 4 | terminology and translation variants: phases, processes, elements | philosophical overview, not a clinical authority |
| S007 | WHO, *International Standard Terminologies on Traditional Chinese Medicine*, 2022 | primary institutional terminology standard | 5 | terminology governance and consistent English naming | standardization does not establish efficacy or biomedical equivalence |
| S008 | NCCIH, “Traditional Chinese Medicine: What You Need To Know” | primary public-health information | 5 | public-facing safety boundary and evidence caution | not a source for classical correspondences |
| S009 | Marshall et al., “Traditional Chinese Medicine and Clinical Pharmacology,” 2020, Table 2 | secondary scholarly overview | 4 | convergent five-phase organ-pair and season table | clinical review contains therapeutic material not used on this page |
| S010 | Existing `DYAI2025/WX-learning` repository | primary project source | 5 | design, build, validation, analytics and deployment conventions | current repository architecture may change |

## SOURCE_NEEDED / unresolved

- A project-designated named medical reviewer is not recorded in Jira. The page can undergo claims exclusion and source review, but `HUMAN_REVIEWED` must remain false until a qualified reviewer is recorded.
- The canonical-domain routing from `sizhuatelier.shop` to the Railway service is not available through current deployment tools.
- Analytics collector receipt location is not defined. Static event hooks can be checked; collection cannot be claimed.
- BZG-29 and BZG-30 remain open in Jira. Their intended rules are implemented as local artifacts, not claimed complete.

## Rejected source use

The user-supplied draft is not used as authority for disease correlations, constitutional diagnosis, herbal formulas, acupuncture outcomes, microbiome mappings, psychiatric claims, treatment comparisons, dosage, prevention or efficacy. Those claims are omitted rather than weakened into implied advice.
