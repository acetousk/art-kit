# 037. Set Up the Em Square Grid

**You make:** ~/Art/Lettering/font-sheet.kra
**Builds on:** lesson 036
**Time:** 40 min
**Read:** Design With FontForge, PDF pages 37, 38 and 39; Krita Manual, Grids and Guides Docker; Krita Manual, Snapping

## The idea
Every glyph sits in an em square. FontForge says the baseline, the cap height and the x-height are lines inside it. In this course the em square is 500 px by 500 px. Each cell on the grid is 25 px. The baseline is 16 cells down. The sheet has 30 cells, 6 across and 5 down, one for each letter.

> "So if your uppercase 'H' is 700 units high, it will be 7 pt high on a 10 pt type." (Design With FontForge, PDF p. 38)

## Look
FontForge page 37: see the em square and its baseline. Page 38: read the lines of the em. Page 39: read the x-height section.

## Steps
1. Open Krita. Press Ctrl+N. Make a 3000 by 2500 px image. Save it as font-sheet.kra.
2. Open the Grids and Guides docker. Set X spacing and Y spacing to 25 px. Set Subdivision to 20.
   You should see: solid lines every 500 px. These are the cell borders.
3. Turn on Snap to Grid with Shift+S. Add a paint layer named Guides1.
4. Pick Ink-2 Fineliner at 2 px. Press V for the line tool.
5. Draw five lines across row 1 at y = 25, 50, 150, 400 and 475.
   You should see: five lines across the top 500 px.
6. These are the ascender, cap height, x-height, baseline and descender lines.
7. Choose Layer > Duplicate Layer or Mask. Name the copy Guides2.
8. Use the Move Tool to move Guides2 down by 500 px.
9. Duplicate the layer three times. Move each copy down by another 500 px.
10. Check that each of the five rows has five lines.
11. Add a layer named Labels. Pick the Text tool.
12. Write a to f in row 1 and g to l in row 2.
13. Write m to r in row 3, s to x in row 4, then y and z in row 5.
14. Press Ctrl+S to save to ~/Art/Lettering/font-sheet.kra.

## Check your work
- Are the cell borders 500 px apart?
- Does each row have five guide lines?
- Is the baseline 400 px below the top of each cell?

## Make it yours
- Add a vertical guide in each cell at x = 100 for a left spacing mark.
- Try a larger em square in a second file.

## New words
- **em square** — the square box that every glyph sits inside
- **cap height** — the height of a capital letter
- **baseline** — the line that letters sit on

---
Source: The FontForge Project Contributors, Design With FontForge (free documentation, credited); Krita Manual, by the Krita team (CC BY-SA / GNU FDL). Tool names from the Krita Manual (CC BY-SA / GNU FDL).
