#!/usr/bin/env python3
from pathlib import Path
import re

PAGE = Path("public/learn/wu-xing/index.html")
ROOT = Path("public/index.html")
VERSION = Path("public/version.txt")
CADDY = Path("Caddyfile")

SHOP_URL = "https://sizhuatelier-shop-production.up.railway.app/"
BAZIODIAC_URL = "https://bazodiac.space/"
BUILD = "wu-xing-2026-07-18-v6-expert-review"
CTA_ALIGNMENT_MARKER = "/* CTA_CARD_ALIGNMENT_V1 */"
CTA_ALIGNMENT_CSS = """
    /* CTA_CARD_ALIGNMENT_V1 */
    .cta-grid { align-items: stretch; }
    .cta { display: flex; flex-direction: column; height: 100%; }
    .cta > h3 { margin-top: 0; }
    .cta > p { margin-bottom: 1.25rem; }
    .cta > .button {
      margin-top: auto;
      align-self: flex-start;
      justify-content: center;
      text-align: center;
    }
"""

PHASES_SECTION = '''<section id="phases"><h2>The five phases</h2>
      <p class="notice"><strong>Interpretive note:</strong> The English terms below are process shorthand anchored in classical descriptions. They are not fixed definitions shared identically by every historical Wu Xing tradition.</p>
      <div class="phase-grid" aria-label="Five phases overview">
        <div class="phase wood"><strong>Wood</strong><span class="hanzi" lang="zh-Hans">木</span><span>mù</span><p>Bending and straightening; growth, extension, and flexible development.</p></div>
        <div class="phase fire"><strong>Fire</strong><span class="hanzi" lang="zh-Hans">火</span><span>huǒ</span><p>Blazing and rising; activity, warmth, visibility, and culmination.</p></div>
        <div class="phase earth"><strong>Earth</strong><span class="hanzi" lang="zh-Hans">土</span><span>tǔ</span><p>Sowing and harvesting; cultivation, transformation, stabilization, and support.</p></div>
        <div class="phase metal"><strong>Metal</strong><span class="hanzi" lang="zh-Hans">金</span><span>jīn</span><p>Yielding and changing; contraction, delimitation, refinement, and structure.</p></div>
        <div class="phase water"><strong>Water</strong><span class="hanzi" lang="zh-Hans">水</span><span>shuǐ</span><p>Moistening and descending; storage, depth, conservation, and adaptability.</p></div>
      </div>
      <div class="table-wrap"><table><thead><tr><th>Phase</th><th>Classical anchor</th><th>Modern reflective question</th></tr></thead><tbody>
        <tr><td>Wood</td><td>Bending and straightening</td><td>What is beginning or trying to grow?</td></tr>
        <tr><td>Fire</td><td>Blazing and rising</td><td>What is becoming active, warm, or visible?</td></tr>
        <tr><td>Earth</td><td>Sowing and harvesting</td><td>What is being cultivated, transformed, or supported?</td></tr>
        <tr><td>Metal</td><td>Yielding and changing</td><td>What must be delimited, refined, or released?</td></tr>
        <tr><td>Water</td><td>Moistening and descending</td><td>What must be conserved, restored, or allowed to deepen?</td></tr>
      </tbody></table></div>
      <p>These descriptions are not personality diagnoses. The second and third columns deliberately separate classical textual anchors from modern reflective language.</p>
    </section>'''

BALANCE_SECTION = '''<section id="balance"><h2>A modern reflective analogy: balance, excess, and lack</h2>
      <p>The following section uses contemporary systems language to make the cycle easier to reflect on. It is <strong>not</strong> a universal classical definition of Wu Xing balance, and it is not a BaZi or medical assessment.</p>
      <p>A common mistake is to imagine that balance means five equal portions. In this modern analogy, the useful pattern depends on the situation: a beginning may call for Wood-like exploration; a public performance for Fire-like expression; a transition for Earth-like coordination; editing for Metal-like discrimination; and recovery for Water-like conservation.</p>
      <ul>
        <li><strong>Excess</strong> means that one function dominates this particular process and suppresses needed alternatives.</li>
        <li><strong>Lack</strong> means that a needed function is unavailable or underdeveloped in this context.</li>
        <li><strong>Balance</strong> means that the process can generate, check, shift, and recover in a way suited to current conditions.</li>
      </ul>
      <p>Endless ideation without selection can be described as <em>Wood-like expansion without sufficient Metal-like selection</em>. Excessive rules that prevent exploration can be described as <em>Metal-like delimitation without sufficient Wood-like development</em>. These are reflective metaphors, not diagnoses of a person, body, or chart.</p>
      <h3>What this page does not claim</h3>
      <ul>
        <li>Wu Xing is not presented as a chemical or physical element system.</li>
        <li>It is not presented as a scientifically validated causal mechanism.</li>
        <li>It is not used here for health diagnosis or treatment.</li>
        <li>It does not prove personality, fate, compatibility, or future events.</li>
        <li>No color, object, food, direction, or poster is claimed to change health, wealth, love, or career outcomes.</li>
      </ul>
    </section>'''

SOURCES_SECTION = '''<section id="sources"><h2>Sources and further reading</h2><ul>
      <li><a href="https://ctext.org/shang-shu/great-plan/zhs"><em>Shangshu</em>, “Hong Fan” 洪范</a>: the five classical operations, from Water “moistening and descending” to Earth “sowing and harvesting.”</li>
      <li><a href="https://ctext.org/bai-hu-tong/juan-san/ens"><em>Bai Hu Tong</em>, “Wu Xing”</a>: the generating sequence Wood → Fire → Earth → Metal → Water → Wood.</li>
      <li><a href="https://ctext.org/huainanzi/di-xing-xun"><em>Huainanzi</em>, “Dixing Xun”</a>: the overcoming sequence Wood → Earth → Water → Fire → Metal → Wood. The linked Chinese source text is used here rather than treating the site’s community/AI English rendering as the sole translation authority.</li>
      <li>John S. Major, Sarah A. Queen, Andrew Seth Meyer, and Harold D. Roth, eds. and trans., <a href="https://cup.columbia.edu/book/the-huainanzi/9780231142045/"><em>The Huainanzi</em></a>, Columbia University Press, 2010.</li>
      <li><a href="https://iep.utm.edu/wuxing/">“Wuxing (Wu-hsing)” — Internet Encyclopedia of Philosophy</a>, for terminology and philosophical context.</li>
      <li><a href="https://www.dpm.org.cn/lemmas/244166.html">Palace Museum: “Mutual generation and mutual overcoming”</a>, for a contemporary institutional summary of both sequences.</li>
    </ul><p><small>Terminology, Hanzi, Pinyin, cycle order, source framing, and claims were reviewed against the Sizhu Learn editorial standards. Classical descriptions and modern analogies are intentionally labelled as different layers.</small></p></section>'''


def replace_anchor_href(html: str, predicate, target: str) -> str:
    pattern = re.compile(r"<a\b(?P<attrs>[^>]*)>(?P<body>.*?)</a>", re.I | re.S)
    def repl(match: re.Match) -> str:
        attrs, body = match.group("attrs"), match.group("body")
        probe = f"{attrs} {re.sub(r'<[^>]+>', ' ', body)}".lower()
        if not predicate(probe):
            return match.group(0)
        if re.search(r'\bhref\s*=\s*([\"\']).*?\1', attrs, re.I | re.S):
            attrs = re.sub(r'\bhref\s*=\s*([\"\']).*?\1', f'href="{target}"', attrs, count=1, flags=re.I | re.S)
        else:
            attrs = f' href="{target}"{attrs}'
        return f"<a{attrs}>{body}</a>"
    return pattern.sub(repl, html)


def replace_once(html: str, old: str, new: str, label: str) -> str:
    count = html.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one {label}; found {count}")
    return html.replace(old, new, 1)


def replace_section(html: str, section_id: str, replacement: str) -> str:
    pattern = re.compile(rf'<section id="{re.escape(section_id)}">.*?</section>', re.S)
    html, count = pattern.subn(replacement, html, count=1)
    if count != 1:
        raise SystemExit(f"Could not replace section #{section_id}; found {count}")
    return html


def append_after_figure(html: str, labelledby: str, note: str) -> str:
    marker = f'data-review-note="{labelledby}"'
    if marker in html:
        return html
    pattern = re.compile(rf'(<figure aria-labelledby="{re.escape(labelledby)}">.*?</figure>)', re.S)
    replacement = rf'\1\n      <p class="diagram-note" {marker}><small>{note}</small></p>'
    html, count = pattern.subn(replacement, html, count=1)
    if count != 1:
        raise SystemExit(f"Could not annotate figure {labelledby}; found {count}")
    return html


def ensure_cta_alignment(html: str) -> str:
    if CTA_ALIGNMENT_MARKER in html:
        return html
    if "</style>" not in html:
        raise SystemExit("Cannot inject CTA alignment CSS: closing style tag missing")
    return html.replace("</style>", f"{CTA_ALIGNMENT_CSS}\n  </style>", 1)


def apply_expert_review(html: str) -> str:
    old_history = ('<p>An influential early formulation appears in the <em>Great Plan</em> chapter of the <em>Classic of Documents</em>. '
                   'Instead of defining five substances, it describes characteristic operations: Water moistens and descends, Fire blazes and rises, '
                   'Wood bends and straightens, Metal yields and changes, and Earth supports sowing and harvest. Later thinkers expanded the model into '
                   'systems of seasonal, political, cosmological, and medical correspondence.</p>')
    new_history = ('<p>An influential early formulation appears in the <em>Great Plan</em> chapter of the <em>Classic of Documents</em>. '
                   'Rather than presenting the five categories only as inert substances, the text characterizes them through typical operations: '
                   'Water moistens and descends, Fire blazes and rises, Wood bends and straightens, Metal yields and changes, and Earth is associated '
                   'with sowing and harvesting. Later thinkers expanded the model into systems of seasonal, political, cosmological, and medical correspondence.</p>')
    html = replace_once(html, old_history, new_history, "historical framing paragraph")
    html = replace_section(html, "phases", PHASES_SECTION)

    html = replace_once(
        html,
        '<li><strong>Metal generates Water:</strong> A traditional relation often taught through condensation or mineral-water imagery; not a physical law.</li>',
        '<li><strong>Metal generates Water:</strong> This traditional relation is sometimes illustrated in later teaching through condensation, mineral, or collection imagery. These are mnemonic explanations, not a physical mechanism and not a single universally accepted classical derivation.</li>',
        "Metal-generates-Water explanation",
    )
    html = append_after_figure(
        html,
        "gen-title gen-caption",
        "Cycle layout: positions show relational order, not compass directions. Earth is shown as a cycle node here, not as the spatial center of a directional correspondence model.",
    )

    html = replace_once(html, '<section id="controlling"><h2>The Controlling Cycle: regulation and constraint</h2>', '<section id="controlling"><h2>The Controlling Cycle: restraining and checking</h2>', "controlling-cycle heading")
    html = replace_once(
        html,
        '<p>The Controlling Cycle is called <strong><span lang="zh-Hans">相克</span> (xiāngkè)</strong>. It describes how each phase limits another so that growth does not continue without restraint.</p>',
        '<p>The cycle is commonly called <strong><span lang="zh-Hans">相克</span> (xiāngkè)</strong>, the Controlling, Restraining, or Overcoming Cycle. It represents relations in which one phase checks, limits, or overcomes another. In later functional interpretations, including Chinese medicine, these relations are often understood as part of regulation rather than simple hostility.</p>',
        "controlling-cycle definition",
    )
    html = append_after_figure(
        html,
        "ctl-title ctl-caption",
        "Terminology note: the artwork’s phrase “balancing / restraining” is simplified teaching language. More precisely, 相克 expresses checking, restraining, or overcoming relations; it does not automatically guarantee balance. Positions show relational order, not compass directions.",
    )
    html = replace_section(html, "balance", BALANCE_SECTION)
    html = replace_section(html, "sources", SOURCES_SECTION)

    structured_replacements = {
        '"description": "The phase language of growth, emergence, extension, and flexibility."': '"description": "Classically associated with bending and straightening; here summarized through growth, extension, and flexible development."',
        '"description": "The phase language of activity, expression, visibility, and culmination."': '"description": "Classically associated with blazing and rising; here summarized through activity, warmth, visibility, and culmination."',
        '"description": "The phase language of stabilization, transition, integration, and support."': '"description": "Classically associated with sowing and harvesting; here summarized through cultivation, transformation, stabilization, and support."',
        '"description": "The phase language of contraction, selection, refinement, and structure."': '"description": "Classically associated with yielding and changing; here summarized through contraction, delimitation, refinement, and structure."',
        '"description": "The phase language of storage, depth, continuity, and adaptability."': '"description": "Classically associated with moistening and descending; here summarized through storage, depth, conservation, and adaptability."',
        '"description": "Wood regulates Earth, Earth regulates Water, Water regulates Fire, Fire regulates Metal, and Metal regulates Wood."': '"description": "Wood checks Earth, Earth checks Water, Water checks Fire, Fire checks Metal, and Metal checks Wood."',
        '"https://ctext.org/bai-hu-tong/wu-xing2"': '"https://ctext.org/bai-hu-tong/juan-san/ens"',
        '"https://ctext.org/huainanzi/di-xing-xun/ens"': '"https://ctext.org/huainanzi/di-xing-xun"',
        '"https://iep.utm.edu/?p=12533"': '"https://iep.utm.edu/wuxing/",\n        "https://cup.columbia.edu/book/the-huainanzi/9780231142045/",\n        "https://www.dpm.org.cn/lemmas/244166.html"',
    }
    for old, new in structured_replacements.items():
        if old in html:
            html = html.replace(old, new)

    return html


def update_page() -> None:
    html = PAGE.read_text(encoding="utf-8")
    html = html.replace("Bazodiac Learn", "Sizhu Learn").replace("BAZODIAC LEARN", "SIZHU LEARN")
    html = ensure_cta_alignment(html)
    html = apply_expert_review(html)

    html = re.sub(r"PUBLIC_BUILD:\s*[A-Za-z0-9._-]+", f"PUBLIC_BUILD: {BUILD}", html)
    html = re.sub(r'(<meta\s+name=["\']x-public-build["\']\s+content=["\'])[^"\']+(["\'])', rf"\g<1>{BUILD}\g<2>", html, flags=re.I)
    html = re.sub(r'(data-content-version=["\'])[^"\']+(["\'])', rf"\g<1>{BUILD}\g<2>", html, flags=re.I)
    html = re.sub(r'("dateModified"\s*:\s*")[^"]+("\s*)', r'\g<1>2026-07-18T05:00:00+02:00\2', html, count=1)

    for old in ["/products/wu-xing-cycle-poster/", "/products/wu-xing-poster/", "https://sizhuatelier.shop/"]:
        html = html.replace(old, SHOP_URL)
    for old in ["/atlas/", "https://bazodiac.space/atlas/", "https://www.bazodiac.space/atlas/"]:
        html = html.replace(old, BAZIODIAC_URL)

    html = replace_anchor_href(html, lambda p: ('data-analytics="product"' in p or "poster" in p or "sizhu atelier shop" in p or "shop the" in p), SHOP_URL)
    html = replace_anchor_href(html, lambda p: ('data-analytics="atlas"' in p or 'data-analytics="bazodiac"' in p or "calculate with bazodiac" in p or "calculate your wu xing" in p or ("bazodiac" in p and "calculate" in p)), BAZIODIAC_URL)
    html = html.replace('data-analytics="atlas"', 'data-analytics="bazodiac"').replace("learn_wuxing_cta_atlas_click", "learn_wuxing_cta_bazodiac_click")

    required = ["Sizhu Learn", SHOP_URL, BAZIODIAC_URL, CTA_ALIGNMENT_MARKER, "Rather than presenting the five categories only as inert substances", "A modern reflective analogy: balance, excess, and lack", "Major, Sarah A. Queen"]
    missing = [item for item in required if item not in html]
    if missing:
        raise SystemExit(f"Required public content missing: {missing}")
    forbidden = ["Instead of defining five substances", "too much Wood and too little Metal", "It describes how each phase limits another so that growth does not continue without restraint"]
    present = [item for item in forbidden if item in html]
    if present:
        raise SystemExit(f"Legacy expert-review wording remains: {present}")

    PAGE.write_text(html, encoding="utf-8")


def update_root() -> None:
    html = ROOT.read_text(encoding="utf-8").replace("Bazodiac Learn", "Sizhu Learn").replace("BAZODIAC LEARN", "SIZHU LEARN")
    ROOT.write_text(html, encoding="utf-8")


def update_runtime_metadata() -> None:
    VERSION.write_text("\n".join([
        f"WU_XING_PUBLIC_BUILD={BUILD}",
        "EXPECTED_ROUTE=/learn/wu-xing/",
        "SITE_BRAND=Sizhu Learn",
        f"BAZIODIAC_CTA={BAZIODIAC_URL}",
        f"SIZHU_SHOP_CTA={SHOP_URL}",
        "CTA_ALIGNMENT=equal-cards-top-copy-bottom-buttons",
        "EXPERT_REVIEW=historical-nuance-classical-anchors-modern-analogy-source-precision",
        "INTERNAL_TICKET_LABELS=removed",
        "",
    ]), encoding="utf-8")
    caddy = CADDY.read_text(encoding="utf-8")
    caddy = re.sub(r"X-Bazodiac-Build\s+\"[^\"]+\"", f'X-Sizhu-Build "{BUILD}"', caddy)
    caddy = re.sub(r"X-Sizhu-Build\s+\"[^\"]+\"", f'X-Sizhu-Build "{BUILD}"', caddy)
    CADDY.write_text(caddy, encoding="utf-8")


if __name__ == "__main__":
    update_page()
    update_root()
    update_runtime_metadata()
    print(f"Applied public Sizhu Learn build: {BUILD}")
