# Revision notes

- **1.2 Improved:** 465 mapped characters, including Greek, common accented Latin, 13 combining marks, engineering notation and selected drafting symbols. OpenType GPOS carries kerning and mark placement; the legacy kern table provides pair adjustments for compatible layout engines. Dotless forms prevent duplicate dots when top accents are applied to i or j. Original handwriting and the similarities between 0/O and 1/I are preserved.
- **1.3 candidate:** Redrew or respaced punctuation, opened selected uppercase and numeric pairs, and adjusted decimals. Retained the character map and the outlines and widths of 1, I, l, slash, 0 and O. The AVATAR raster matched 1.2 at the sampled size.
- **1.4 candidate:** Changes six kerning pairs. C4 moved from −606 to −200 font units, a 406-unit increase at 2048 units per em. This is positioning displacement, not minimum outline clearance. The glyf, loca, cmap, hmtx and GSUB tables are byte-identical to 1.3. The candidate has not been designated the stable build.

Application-specific shaping and optical judgment can vary. The project does not claim CAD or engineering lettering standards compliance.
