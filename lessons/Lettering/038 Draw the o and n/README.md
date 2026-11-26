# 038. Draw the o and n

**You make:** ~/Art/Lettering/font-lower.kra
**Builds on:** lesson 037
**Time:** 45 min
**Read:** Design With FontForge, PDF pages 79, 80 and 81

## The idea
FontForge says to begin with o. It sets the round shape and the white inside. The white inside the o is called the counter. The n is a stem and an arch. You can reuse both for other letters. Use the same stroke weight everywhere. Your font uses a 50 px round stroke. All coordinates here count grid cells from the top left of the glyph cell.

> "the white — or counter — provides the size and shape used by the rest of the font." (Design With FontForge, PDF p. 79)

## Look
FontForge page 79: read why o is first. Page 80: see the n split into a stem and a curve. Page 81: see how the parts repeat in other letters.

## Steps
1. Open Krita. Open font-sheet.kra. Save As font-lower.kra.
2. Add a paint layer named Glyphs. Pick Ink-2 Fineliner. Set size to 50 px.
3. o lives in row 3, third cell (cell origin x = 1000, y = 1000).
   Count cells from that corner: x goes right, y goes down.
4. Pick the Ellipse tool. Drag from (4, 7) to (12, 15) to draw o.
   You should see: a circle between the x-height and baseline guides.
5. n lives in row 3, second cell. Draw an ellipse from (4, 7) to (12, 15).
6. Use the Rectangular Select tool (Ctrl+R). Select everything below y = 11 in that cell. Press Delete.
   You should see: only the top half of the circle is left.
7. Press Ctrl+Shift+A to deselect. Pick the Line tool (V).
8. Draw the left stem from (4, 7) to (4, 15). Draw the right stem from (12, 11) to (12, 15).
9. Compare o and n. Are the heights the same? Is the stroke the same weight?
10. Write o n o n o n by copy and paste to test. Do the stems look even?
11. Press Ctrl+S to save to ~/Art/Lettering/font-lower.kra.

## Check your work
- Does o touch the x-height line and the baseline?
- Does n have the same stroke weight as o?
- Is the counter of n similar to the counter of o?

## Make it yours
- Make the o 10 cells wide. Does the n need to change?
- Try a stroke width of 40 px.

## New words
- **counter** — the white space inside a letter
- **stem** — the main upright stroke
- **arch** — the curve that springs from a stem

---
Source: The FontForge Project Contributors, Design With FontForge (free documentation, credited); Krita Manual, by the Krita team (CC BY-SA / GNU FDL). Tool names from the Krita Manual (CC BY-SA / GNU FDL).
