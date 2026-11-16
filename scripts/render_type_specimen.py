"""Render the README typography specimen from the stable 1.4.1 TTF."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from render_glyphs import RELEASE, coverage


def main():
    samples = [
        ("01 / PHRASE", [(84, "Engineering in motion")]),
        ("02 / SENTENCE", [(52, "The quick brown fox jumps over the lazy dog.")]),
        ("03 / LETTERS AND NUMBERS", [(49, "A1  B2  C4  E6  X9  R2D4"), (44, "Part AX-204B  /  Rev. C4  /  ⌀12.50 mm")]),
        ("04 / ALPHABET AND DIGITS", [
            (46, "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            (46, "abcdefghijklmnopqrstuvwxyz  0123456789"),
        ]),
        ("05 / ENGINEERING NOTATION", [(51, "V = I × R     x² + y² = r²     θ = 45° ± 0.5°")]),
        ("06 / COMMA AND PERIOD", [
            (52, "Length, width, height."),
            (50, "Rev. B.    1,250.75 mm    0.5, 1.0, 2.5"),
        ]),
    ]
    _, visible = coverage(RELEASE)
    assert {ord(ch) for _, lines in samples for _, line in lines for ch in line if ch != " "} <= visible
    width, height, inset = 1360, 1070, 52
    image = Image.new("RGB", (width, height), "#fffefa")
    draw = ImageDraw.Draw(image)
    ink, teal, rule = "#16282b", "#17665b", "#c8d7d1"
    label = ImageFont.load_default(size=24)
    draw.rectangle((0, 0, width - 1, 8), fill=teal)
    draw.text((inset, 36), "JPCS ENGINEERING FONT  /  VERSION 1.4.1", font=label, fill=teal)

    for (title, lines), top, bottom in zip(
        samples, (89, 251, 382, 551, 720, 850), (251, 382, 551, 720, 850, 1030), strict=True
    ):
        draw.line((inset, top, width - inset, top), fill=rule, width=2)
        draw.text((inset, top + 14), title, font=label, fill=teal)
        for i, (size, line) in enumerate(lines):
            font = ImageFont.truetype(str(RELEASE), size, layout_engine=ImageFont.Layout.RAQM)
            baseline = top + (131 if size > 60 else 94) + i * 52
            position = (inset + 5, baseline)
            left, upper, right, lower = draw.textbbox(position, line, font=font, anchor="ls")
            assert inset <= left < right <= width - inset and top + 42 <= upper < lower < bottom, title
            draw.text(position, line, font=font, anchor="ls", fill=ink)

    output = Path(__file__).resolve().parents[1] / "docs/type-specimen.png"
    image.save(output)


if __name__ == "__main__":
    main()
