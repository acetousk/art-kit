# 013. Alpha Lock and Inherit Alpha

**You make:** ~/Art/Painting/013-alpha-lock.kra
**Builds on:** lesson 012
**Time:** 40 min
**Read:** Krita Manual, Layers; Krita Manual, Clipping Masks and Alpha Inheritance; Krita Manual, Flat Coloring

## The idea
Alpha means how see-through a pixel is. Alpha Lock keeps a layer's see-through parts as they are. Then you can only paint where paint already exists. Inherit Alpha is a second tool. It limits a layer to the shape of the layers below it. Both let you shade a shape without going over its edge.

> "When we turn on alpha inheritance, the alpha-inherited layer keeps the same transparency as the layers below." (Krita Manual, Clipping Masks and Alpha Inheritance).

## Look
Layers: find the Alpha Lock and Alpha Inheritance icons. Clipping Masks and Alpha Inheritance: look at the white scribble before and after.

## Steps
1. Open Krita. Open your file ~/Art/Painting/012-flat-colors.kra. Save it as 013-alpha-lock.kra.
2. Click the cap layer. Click the Alpha Lock icon in the layer stack.
3. Pick a darker red. Use a big soft brush. Paint across the edge of the cap.
   You should see: Paint stays in the shape.
4. Paint a shadow on the right side of the cap. Make the left side lighter.
5. Turn off Alpha Lock. Paint over the edge on purpose.
   You should see: Paint spills out. Undo with Ctrl+Z.
6. Click the lines layer. Turn on Alpha Lock. Paint a dark brown across the lines.
   You should see: Only the lines change color.
7. Click the cap layer. Press Ins to add a layer above it. Name it cap shine.
8. Click the Alpha Inheritance icon on cap shine.
9. Paint white strokes across the cap and past its edge.
   You should see: Only the part over the cap shows.
10. Select the stem layer. Press Ctrl+Shift+G.
   You should see: Krita makes a clipping group with a new layer on top.
11. Paint shade on the new layer. It stays inside the stem.
12. Save the file with File ‣ Save As. Use the path ~/Art/Painting/013-alpha-lock.kra.

## Check your work
- Does Alpha Lock keep paint inside the shape? (Yes.)
- Does Inherit Alpha use the shape of the layers below? (Yes.)
- Can you recolor line art with Alpha Lock on? (Yes.)

## Make it yours
- Shade the whole mushroom with one clipping group per part.
- Color the lines of a drawing with a darker color of each shape.

## New words
- **alpha** — how see-through a pixel is
- **alpha lock** — a switch that keeps see-through areas unchanged
- **clipping** — limit a layer to the shape of the layers below

---
Source: Krita Manual by the Krita Foundation and contributors, https://docs.krita.org, CC BY-SA 4.0 / GNU FDL 1.3.
