# Validation of the Wu Xing expert review

Date: 2026-07-18  
Repository: `DYAI2025/WX-learning`  
Public route: `/learn/wu-xing/`  
Verdict: **PASS after accepted corrections**

## Executive assessment

The expert review is materially sound. Its strongest findings are supported by the project lexicon, the visible page, early textual witnesses, and a published scholarly translation. The review correctly distinguishes verified Hanzi and cycle order from a second layer of modern English process shorthand. It also correctly identifies that the page's main weakness was not a wrong cycle or a wrong Chinese character, but insufficient labelling of interpretive modern language.

The review was not accepted wholesale. Claims were divided into `VERIFIED`, `SUPPORTED WITH NUANCE`, `PROJECT INTERPRETATION`, and `SOURCE_NEEDED`. The implemented patch uses the smallest robust correction: classical textual anchors are made explicit; modern analogies are labelled; source references are made passage-specific; the supplied artwork remains unchanged.

## Decision matrix

| Review item | Validation status | Decision |
|---|---|---|
| Visible Hanzi and Pinyin are correct | VERIFIED | Preserve all tokens and tone-marked Pinyin. |
| Generating order is correct | VERIFIED | Preserve `木 → 火 → 土 → 金 → 水 → 木`. |
| Controlling/overcoming order is correct | VERIFIED | Preserve `木 → 土 → 水 → 火 → 金 → 木`. |
| `相` is missing from the old validator whitelist | VERIFIED project-validator defect | Do not treat it as a page error; validation uses complete cycle terms. |
| “Phases rather than substances” was too absolute | SUPPORTED WITH NUANCE | Replace with “not only inert substances” and foreground operations. |
| Phase qualities were presented as if fixed classical definitions | SUPPORTED WITH NUANCE | Put classical operational anchors before modern shorthand. |
| `相克` should include restraining/checking/overcoming | VERIFIED translation nuance | Keep “Controlling Cycle” but explain the wider semantic field. |
| Regulation automatically implies balance | NOT SUPPORTED AS A UNIVERSAL CLASSICAL CLAIM | Remove automatic-balance wording and qualify later functional interpretations. |
| Balance/excess/lack section is modern systems language | VERIFIED editorial diagnosis | Retitle and explicitly label it a modern reflective analogy. |
| Metal → Water condensation explanation is a universal mechanism | SOURCE_NEEDED / not universal | Retain only as later mnemonic imagery, not mechanism or unique derivation. |
| Earth must be central in these diagrams | REJECTED FOR THIS DIAGRAM TYPE | The diagrams encode relational order, not directional cosmography; add a note. |
| Source list was too general | VERIFIED | Add exact text sections, published Huainanzi translation, and institutional summary. |

## Source boundary

### Classical anchors

- *Shangshu*, “Hong Fan” 洪范: the five categories are described through characteristic operations, including moistening/descending, blazing/rising, bending/straightening, yielding/changing, and sowing/harvesting.
- *Bai Hu Tong*, “Wu Xing”: evidence for the generating sequence.
- *Huainanzi*, “Dixing Xun”: evidence for the overcoming sequence.

These sources support the relational order and operational vocabulary. They do **not** establish that every later school used one identical interpretation or that modern organizational language is itself classical doctrine.

### Translation and secondary sources

- Major, Queen, Meyer, and Roth, eds. and trans., *The Huainanzi* (Columbia University Press, 2010), is included as a published scholarly translation reference.
- The Internet Encyclopedia of Philosophy is used for terminology and intellectual context.
- The Palace Museum entry is used as a modern institutional summary, not as a primary historical witness.

## Glyph and terminology status

Region policy: `CN_SIMPLIFIED` by declared HTML language/font policy. The visible core terms are shared forms and produce no Simplified/Traditional conflict.

| Term | Pinyin | Status |
|---|---|---|
| 五行 | wǔxíng | VERIFIED |
| 木 | mù | VERIFIED |
| 火 | huǒ | VERIFIED |
| 土 | tǔ | VERIFIED |
| 金 | jīn | VERIFIED |
| 水 | shuǐ | VERIFIED |
| 相生 | xiāngshēng | VERIFIED |
| 相克 | xiāngkè | VERIFIED |

## Implemented corrections

1. Historical framing no longer claims that Wu Xing categorically excludes material readings.
2. Each phase now begins with a classical operational anchor.
3. Modern reflective questions are visibly separated from classical descriptions.
4. `相克` is described through controlling, restraining, checking, and overcoming language.
5. The balance section is explicitly marked as a modern analogy and not a BaZi/medical assessment.
6. Metal → Water imagery is labelled mnemonic and non-mechanical.
7. Both diagrams receive a non-compass explanation; the controlling artwork receives an extra terminology caveat without altering the supplied image.
8. Sources now identify passages and include a published scholarly translation.
9. JSON-LD descriptions and source URLs are kept consistent with the visible page.
10. A deterministic build validator blocks publication of partial or stale corrections.

## Claims safety

The patch adds no medical, therapeutic, divinatory, wealth, love, career, or efficacy claim. It does not calculate BaZi data. It does not infer individual imbalance. It distinguishes educational metaphor from diagnosis.

## Final status

- Hanzi/Pinyin: `VERIFIED`
- Cycle relations: `VERIFIED`
- Glyph policy: `CN_SIMPLIFIED`
- Historical framing: `VERIFIED WITH NUANCE`
- Modern analogies: `CLEARLY LABELLED`
- Source apparatus: `PASS`
- Overall: `PASS`
