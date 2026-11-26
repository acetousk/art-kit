# Lesson review

## Scope

Reviewed 305 lessons across 7 topics. The two topic README files are indexes, not lessons.

## Checks

| Check | Result |
|---|---|
| Control names | Checked 305 lesson step sections against Krita Manual, Sweet Home 3D User's Guide, and Blender Manual 5.3. No unverified control-name patterns remain. |
| Blender camera | Lessons 022, 024, and 030 use the Add menu or a Grease Pencil template. Camera View and the View > Cameras commands are documented in Blender Manual 5.3. No `Add > Camera` path remains. |
| Chains | All 305 Builds on references point to earlier lessons. Checked 133 lessons with explicit file-opening steps against the lesson file paths. No mismatches found. |
| Quotes | Ran `python3 -I tools/check-quotes.py /tmp/art-kit/lessons /tmp/books`. The full scan is running. Separately checked all 19 Revoy quotes against `/tmp/books/revoy/*.txt`; 0 failed. The checker includes Revoy text sources and limits OCR to the cited book. |
| Bridgman safety | Rendered and visually checked all 42 cited PDF pages. No page shows a nude torso, pelvis, or buttocks. |
| Revoy paths | All cited art uses ep06, ep10, or ep20. All three episodes exist in `library/revoy.txt`. Brush path uses `~/Library/Painting/Brushes/`. |

## Unverified control names

| Name pattern | Files | Result |
|---|---:|---|
| None | 0 | No unverified names found in the requested manuals. |

## Patterns fixed

| Pattern | Files | Fix |
|---|---:|---|
| Revoy quote coverage and cross-book OCR | 1 checker | Added Revoy text matching and restricted page OCR to the cited source book. |

## Remaining

The full quote scan is running. No other fixable issue was found.
