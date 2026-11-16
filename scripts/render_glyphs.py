"""Render the public README specimen and list every newly visible codepoint."""
from pathlib import Path
import unicodedata

from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "source/jpcs_engring_font.ttf"
RELEASE = ROOT / "fonts/JPCS_Engineering_Font_1_4_1.ttf"


def coverage(path):
    with TTFont(path) as font:
        glyphs = font.getGlyphSet()
        mapped = font.getBestCmap()
        visible = set()
        for cp, name in mapped.items():
            pen = BoundsPen(glyphs)
            glyphs[name].draw(pen)
            if pen.bounds and pen.bounds[0] < pen.bounds[2] and pen.bounds[1] < pen.bounds[3]:
                visible.add(cp)
        return set(mapped), visible


def main():
    old_mapped, old_visible = coverage(ORIGINAL)
    new_mapped, new_visible = coverage(RELEASE)
    added = new_visible - old_visible
    placeholder = added & old_mapped
    rows = [
        ("Greek", "ΑΓΔΘΛΞΠΣΦΨΩαβγδελμπσω"),
        ("Math and electrical", "±×÷√∞≈≠≤≥∑∫∂∇∝∠Ω⏚"),
        ("Drafting and arrows", "⌀⌖⌔⌒⌴⌵←↑→↓↔"),
        ("Raised and lowered forms", "⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉"),
        ("Accents and punctuation", "ÀÉÑÖÜàéñöü–—‘’“”…"),
    ]
    image = Image.new("RGB", (1360, 1000), "#fffefa")
    d = ImageDraw.Draw(image)
    ink, teal, muted = "#16282b", "#17665b", "#405859"
    label = ImageFont.load_default(size=25)
    small = ImageFont.load_default(size=22)
    heading = ImageFont.load_default(size=54)
    glyph = ImageFont.truetype(str(RELEASE), 49, layout_engine=ImageFont.Layout.RAQM)
    sample = ImageFont.truetype(str(RELEASE), 40, layout_engine=ImageFont.Layout.RAQM)
    d.rectangle((0, 0, 1359, 8), fill=teal)
    d.text((48, 39), "JPCS ENGINEERING FONT", font=label, fill=teal)
    d.text((45, 73), "Added glyphs", font=heading, fill=ink)
    d.text((48, 151), f"{len(added)} newly visible characters vs. the original  |  Selected examples from 1.4.1", font=small, fill=muted)
    for i, (title, chars) in enumerate(rows):
        top = 210 + i * 121
        d.line((48, top, 1311, top), fill="#c8d7d1", width=2)
        d.text((48, top + 11), title, font=label, fill=teal)
        selected = [ch for ch in chars if ord(ch) in added]
        for j, ch in enumerate(selected):
            d.text((66 + 58 * j, top + 94), ch, font=glyph, anchor="ls", fill=ink)
    d.rectangle((48, 836, 1311, 953), fill="#e8f0eb")
    d.text((70, 851), "IN USE", font=small, fill=teal)
    examples = "Lorem ipsum    |    V = I × R    |    x² + y² = r²"
    assert set(map(ord, examples)) <= new_mapped
    d.text((70, 927), examples, font=sample, anchor="ls", fill=ink)
    image.save(ROOT / "docs/added-glyphs.png")
    lines = [
        "# Added glyphs", "",
        f"{len(added)} codepoints have drawable outlines in 1.4.1 that did not in the original.",
        f"Of these, {len(placeholder)} were already mapped to blank glyphs; {len(added - placeholder)} had no original mapping.",
        f"The release maps {len(new_mapped)} codepoints overall. The comparison counts encoded characters, not unique glyph IDs.",
        "Whitespace and format controls without drawable outlines are excluded. Redrawn existing symbols are tracked separately.", "",
        "| Codepoint | Unicode name | Original |", "| --- | --- | --- |",
    ]
    for cp in sorted(added):
        state = "Blank mapping" if cp in placeholder else "Unmapped"
        lines.append(f"| U+{cp:04X} | {unicodedata.name(chr(cp), 'Unnamed')} | {state} |")
    (ROOT / "docs/added-glyphs.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
