# 008. Selection Tools

**You make:** ~/Art/Painting/008-selections.kra
**Builds on:** lesson 006
**Time:** 35 min
**Read:** Krita Manual, Selections; Krita Manual, Rectangular Selection Tool; Krita Manual, Elliptical Selection Tool; Krita Manual, Contiguous Selection Tool

## The idea
A selection is a part of the layer that you pick. Everything you paint stays inside it. The edge is shown as marching ants. Krita has many selection tools: rectangle, ellipse, polygon, freehand, and contiguous (the magic wand). You can add to a selection, subtract from it, or replace it. This is how you paint clean shapes with hard edges.

> "Once an area is selected, most tools will stay inside that area." (Krita Manual, Selections).

## Look
Selections: find the table with Replace, Intersect, Add, Subtract. Elliptical Selection Tool: find the note about holding Shift for a circle.

## Steps
1. Open Krita. Make a new 2400 by 1600 canvas. Add a layer named shapes.
2. Pick the Rectangular Selection Tool. Drag a box.
   You should see: Marching ants show the edge.
3. Pick a Basic preset. Scribble over the box, past its edge.
   You should see: The paint stays inside.
4. Press Ctrl+Shift+A to deselect.
5. Pick the Elliptical Selection Tool. Hold Shift and drag.
   You should see: You get a perfect circle.
6. Fill the circle with a few strokes in a new color.
7. Press Shift, then drag a second circle that overlaps the first.
   You should see: The selection grows.
8. Press Alt, then drag a small circle inside.
   You should see: A hole opens in the selection.
9. Paint inside the selection. Deselect with Ctrl+Shift+A.
10. Pick the Polygonal Selection Tool. Click four points. Double-click to close the shape. Paint it.
11. Pick the Contiguous Selection Tool. Click one painted shape. Paint a stripe in it.
12. Save the file with File ‣ Save As. Use the path ~/Art/Painting/008-selections.kra.

## Check your work
- Does paint stay inside a selection? (Yes.)
- Does the Alt key subtract from a selection? (Yes.)
- Do you press Shift to make a perfect circle? (Yes.)

## Make it yours
- Make a face from selections only: a circle, two ovals, a polygon hat.
- Find which tool selects a color field with one click.

## New words
- **selection** — the part of a layer that you pick to change
- **marching ants** — the moving dashed line along a selection edge
- **deselect** — remove the selection (Ctrl+Shift+A)

---
Source: Krita Manual by the Krita Foundation and contributors, https://docs.krita.org, CC BY-SA 4.0 / GNU FDL 1.3.
