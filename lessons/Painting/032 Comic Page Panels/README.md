# 032. Comic Page Panels

**You make:** ~/Art/Painting/032-page-panels.kra
**Builds on:** lesson 028
**Time:** 45 min
**Read:** Krita Manual, Comic Panel Editing Tool; Krita Manual, Vector Layers; Pepper&Carrot ep06_The-Potion-Contest/E06P03.kra

## The idea
A comic page is a set of panels with gutters between them. The gutter is the white gap. Revoy keeps his panels on a vector layer at the top of the stack, named panel-frame. Vector shapes stay sharp at any size. Krita has a tool that cuts a big rectangle into panels with even gutters. Plan a clear order of panels before you paint them.

> "create comic panels by either slicing through shapes and adding a gutter in between the resulting halves" (Krita Manual, Comic Panel Editing Tool).

## Look
E06P03.kra: click the panel-frame layer, then look at the shapes. Comic Panel Editing Tool: read Cutting mode.

## Steps
1. Open Krita. Open ~/Library/Painting/Pepper-and-Carrot/ep06_The-Potion-Contest/E06P03.kra. Do not save over it.
2. Click the layer panel-frame.
   You should see: The panel shapes show handles. Look at the gaps between them.
3. Close the file. Click No when Krita asks to save.
4. Make a new 2481 by 3503 canvas. This is the size of Revoy's page.
5. Press Shift+Ins to add a vector layer. Name it panel-frame.
6. Pick the Rectangle Tool. Drag one big rectangle that fills the page except for a margin.
7. Pick the Comic Panel Editing Tool. In Tool Options, set Cutting mode.
8. Drag a line across the rectangle from the left to the right, one third from the top.
   You should see: The shape splits with a gap.
9. Drag a line across the lower part, from top to bottom.
   You should see: You now have three panels.
10. Pick Merging mode. Drag across the gap between two panels.
   You should see: The panels join. Undo with Ctrl+Z.
11. Draw a stick figure thumbnail in each panel with a Pencil preset on a new layer. Number the panels.
12. Save the file with File ‣ Save As. Use the path ~/Art/Painting/032-page-panels.kra.

## Check your work
- Is the gutter the white gap between two panels? (Yes.)
- Are panel shapes on a vector layer? (Yes, in Revoy's page.)
- Does your page plan have a clear reading order? (It should.)

## Make it yours
- Lay out a page with six panels.
- Make a page with one wide panel and two small ones.

## New words
- **panel** — one framed picture in a comic
- **gutter** — the gap between panels
- **vector layer** — a layer that keeps shapes as math, not pixels

---
Source: Krita Manual by the Krita Foundation and contributors, https://docs.krita.org, CC BY-SA 4.0 / GNU FDL 1.3. Pepper&Carrot by David Revoy, www.peppercarrot.com, CC BY 4.0 (Krita source files: www.peppercarrot.com/0_sources/).
