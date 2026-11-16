"""Build the stable 1.4.1 punctuation update from stable 1.4."""
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "fonts/JPCS_Engineering_Font_1_4.ttf"
OUTPUT = ROOT / "build/JPCS_Engineering_Font_1_4_1.ttf"


def main():
    OUTPUT.parent.mkdir(exist_ok=True)
    with TTFont(SOURCE, recalcTimestamp=False) as font:
        cmap = font.getBestCmap()
        glyf = font["glyf"]
        comma, semicolon = (cmap[ord(char)] for char in ",;")

        # Freeze the existing semicolon outline before changing its comma component.
        glyphs = font.getGlyphSet()
        recording = DecomposingRecordingPen(glyphs)
        glyphs[semicolon].draw(recording)
        pen = TTGlyphPen(None)
        recording.replay(pen)
        glyf[semicolon] = pen.glyph()

        # Scale the original period's contours into a comma head.
        # Replace its lower-right arc with a diagonal, down-left stroke.
        with TTFont(ROOT / "source/jpcs_engring_font.ttf") as original:
            cmap_original = original.getBestCmap()
            dot = original["glyf"][cmap_original[ord(".")]]
            stroke = original["glyf"][cmap_original[ord(",")]]
            xy = [(round(31 + (x - 164) * .74), round(y * .80)) for x, y in dot.coordinates]
            # Retain the original comma's terminal direction; narrow its end.
            x0, y0 = stroke.coordinates[5]
            x1, y1 = stroke.coordinates[6]
            tip_x = -44 + round(31 + ((x0 + x1) / 2 - 164) * .74)
            tip_y = -68 + round((y0 + y1) / 2)
        pen = TTGlyphPen(None)
        pen.moveTo(xy[1])
        pen.lineTo(xy[2])
        pen.qCurveTo(xy[3], xy[4])
        pen.qCurveTo(xy[5], xy[6])
        pen.qCurveTo((82, -115), (tip_x - 9, tip_y + 12))
        pen.qCurveTo((tip_x - 5, tip_y - 2), (tip_x + 4, tip_y))
        pen.qCurveTo((175, -147), xy[8])
        pen.lineTo(xy[9])
        pen.lineTo(xy[10])
        pen.qCurveTo(xy[11], xy[12])
        pen.lineTo(xy[13])
        pen.qCurveTo(xy[0], xy[1])
        pen.closePath()
        glyf[comma] = pen.glyph()
        glyf[comma].recalcBounds(glyf)
        font["hmtx"][comma] = (font["hmtx"][comma][0], glyf[comma].xMin)
        family = "JPCS Engineering Font 1.4.1"
        names = {1: family, 3: family, 4: family, 5: "Version 1.4.1",
                 6: "JPCSEngineeringFont141", 16: family}
        for record in font["name"].names:
            if record.nameID in names:
                record.string = names[record.nameID].encode(record.getEncoding())
        font["head"].fontRevision = 1.401
        font.save(OUTPUT)
    print(datetime.now(ZoneInfo("Asia/Manila")).isoformat(), "saved", OUTPUT)


if __name__ == "__main__":
    main()
