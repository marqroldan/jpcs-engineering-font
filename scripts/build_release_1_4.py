"""Package the archived 1.4 candidate with stable release naming."""
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from fontTools.ttLib import TTFont

root = Path(__file__).resolve().parents[1]
source = root / "fonts/JPCS_Engineering_Font_1_4_Candidate.ttf"
output = root / "build/JPCS_Engineering_Font_1_4.ttf"
output.parent.mkdir(exist_ok=True)
family = "JPCS Engineering Font 1.4"
names = {
    1: family,
    3: family,
    4: family,
    5: "Version 1.4",
    6: "JPCSEngineeringFont14",
    16: family,
}
with TTFont(source, recalcTimestamp=False) as font:
    for record in font["name"].names:
        if record.nameID in names:
            record.string = names[record.nameID].encode(record.getEncoding())
    font.save(output)
print(datetime.now(ZoneInfo("Asia/Manila")).isoformat(), "saved", output)
