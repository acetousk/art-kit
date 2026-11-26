# 001. Set Up a Lettering Sheet in Krita

**You make:** ~/Art/Lettering/lettering-sheet.kra  (new file)
**Builds on:** nothing
**Time:** 25 min
**Read:** Krita Manual, Grids and Guides Docker; Krita Manual, Snapping; Speedball, PDF page 9 (right half)

## The idea
Letterers rule lines before they draw one letter. On a tablet, the grid and snapping do this job. In this course one grid cell is 40 pixels. Every capital, small letter and guide line sits on this grid. Set it up once and reuse the file.

> "This arrangement is identical with the system of alignment used in ruling guide lines for lettering." (Speedball, PDF p. 9, right half)

## Look
Page 9, right half, top: see the five lines and four spaces, like a music staff. Lettering sits on lines just like notes do.

## Steps
1. Open Krita. Press Ctrl+N to make a new image.
2. Set Width to 3200 px and Height to 1600 px. Click Create.
3. Open the docker Settings > Dockers > Grids and Guides.
4. On the Grids tab, tick Show Grid. Set Type to Rectangle.
5. Set X spacing and Y spacing to 40 px. Set Subdivision to 2.
   You should see: solid lines every 80 px and dotted lines between them.
6. Tick Snap to Grid. Press Shift+S and check that Grids is ticked in the snap menu.
7. Choose View > Show Rulers. Choose View > Show Guides.
8. Drag from the top ruler down onto the canvas. A horizontal guide appears.
9. Drag it back off the canvas to delete it.
10. Add a paint layer in the Layers docker. Double-click its name and rename it Guides.
11. Press B for the Freehand Brush tool. Pick the Ink-2 Fineliner preset. Set size to 4 px.
12. Press V, then drag along one solid grid line from the left edge to the right edge.
   You should see: the line snaps and ends exactly on the grid.
13. Press Ctrl+Z to undo the line. Press Ctrl+Shift+S and save as ~/Art/Lettering/lettering-sheet.kra.

## Check your work
- Are your grid lines 40 px apart?
- Does Snap to Grid make a line end on a grid line?
- Can you delete a guide by dragging it off the canvas?

## Make it yours
- Change the grid to 20 px and draw a line. Does it still snap?
- Drag two guides to mark side margins.

## New words
- **grid** — a net of evenly spaced lines that Krita can snap to
- **snap** — when Krita pulls your line onto a grid line
- **guide line** — a line that letters sit on or touch

---
Source: Poster Lettering (The Speedball Text Book), 1927 edition, Hunt Pen Co. (public domain); Krita Manual, by the Krita team (CC BY-SA / GNU FDL). Tool names from the Krita Manual (CC BY-SA / GNU FDL).
