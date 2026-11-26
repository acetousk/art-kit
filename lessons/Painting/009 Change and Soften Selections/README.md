# 009. Change and Soften Selections

**You make:** ~/Art/Painting/009-soft-selections.kra
**Builds on:** lesson 008
**Time:** 35 min
**Read:** Krita Manual, Select Menu; Krita Manual, Selections; Krita Manual, Freehand Selection Tool

## The idea
You can change a selection after you make it. Invert it to pick everything else. Grow it by a few pixels. Feather it to soften the edge. Select Opaque turns a layer's paint into a selection. A soft edge looks like light and fog.

> "Feathering in design means to soften sharp borders." (Krita Manual, Select Menu).

## Look
Select Menu: read Invert Selection, Feather Selection, Grow Selection, Select Opaque. Selections: read the part about display modes.

## Steps
1. Open Krita. Make a new 2400 by 1600 canvas. Fill the background layer with dark blue.
2. Add a layer named moon. Pick the Elliptical Selection Tool. Hold Shift and drag a circle.
3. Pick a soft airbrush preset. Paint pale yellow inside the circle. Deselect.
4. Right-click the moon layer. Pick Select Opaque.
   You should see: The moon shape is now a selection.
5. Open Select ‣ Feather Selection. Set it to 40 pixels. Click OK.
6. Add a layer named glow. Paint white inside the selection with a big soft brush.
   You should see: You get a soft glow.
7. Move the glow layer below the moon layer.
   You should see: Now the moon sits on the glow.
8. Deselect. Use the Freehand Selection Tool to draw a hill shape at the bottom.
9. Press Ctrl+Shift+I to invert.
   You should see: Now the sky is selected.
10. Click the selection display button in the status bar.
   You should see: The view changes between ants and mask.
11. Invert again. Add a layer named hill. Fill the hill with black.
12. Save the file with File ‣ Save As. Use the path ~/Art/Painting/009-soft-selections.kra.

## Check your work
- Does feathering make an edge softer? (Yes.)
- Does Invert pick everything that was not selected? (Yes.)
- Does Select Opaque make a selection from the paint on a layer? (Yes.)

## Make it yours
- Paint a sun with a bigger glow.
- Make a window of light on a wall with a feathered rectangle.

## New words
- **feather** — soften the edge of a selection
- **invert** — switch what is selected and what is not
- **mask display** — a view that shows the selection as a red cover

---
Source: Krita Manual by the Krita Foundation and contributors, https://docs.krita.org, CC BY-SA 4.0 / GNU FDL 1.3.
