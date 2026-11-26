# 010. Fill Tool and Fill Shortcuts

**You make:** ~/Art/Painting/010-fills.kra
**Builds on:** lesson 008
**Time:** 35 min
**Read:** Krita Manual, Fill Tool; Krita Manual, Edit Menu; Krita Manual, Color Sampler Tool

## The idea
Filling covers a whole area with color in one click. The Fill Tool fills the area that touches your click. Threshold sets how much a pixel may differ and still fill. Spread sets how far the solid color reaches. Shortcuts fill a whole layer or a selection with the foreground or background color. These are the fastest ways to lay down flat color.

> "Krita has one of the most powerful and capable Fill functions available." (Krita Manual, Fill Tool).

## Look
Fill Tool: find Fill Mode (Current Selection, Contiguous Region) and the words Threshold and Spread. Edit Menu: find the four Fill with lines and their shortcuts.

## Steps
1. Open Krita. Make a new 2400 by 1600 canvas. Add a layer named shapes.
2. Draw five closed shapes with a Basic preset: a circle, a star, a house, a leaf, a box.
3. Pick a color in the color selector. It is now the foreground color.
4. Pick the Fill Tool. Click inside the circle.
   You should see: The circle fills with color.
5. Fill the star with a second color.
6. Click the Fill Tool options. Set Threshold to a low value. Fill the house. Look at the edge.
7. Raise the Threshold. Fill the leaf. Compare the edges.
8. Pick the Rectangular Selection Tool. Select the box.
9. Press Shift+Backspace.
   You should see: The box fills with the foreground color.
10. Press Backspace.
   You should see: The box fills with the background color.
11. Press Ctrl+Shift+Backspace.
   You should see: The box fills again. This time Krita counts the opacity.
12. Save the file with File ‣ Save As. Use the path ~/Art/Painting/010-fills.kra.

## Check your work
- Does the Fill Tool fill the area next to your click? (Yes, in Contiguous Region mode.)
- Does Shift+Backspace use the foreground color? (Yes.)
- Does a higher Threshold fill more nearby colors? (Yes.)

## Make it yours
- Fill a drawing of a flag with four colors.
- Try to fill a shape with a gap in the line. See what happens.

## New words
- **foreground color** — the color your brush paints with now
- **threshold** — how much a color may differ and still be filled
- **flat color** — one solid color with no shading

---
Source: Krita Manual by the Krita Foundation and contributors, https://docs.krita.org, CC BY-SA 4.0 / GNU FDL 1.3.
