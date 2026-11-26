# 025. Revoy Page Study 1 Layers and Modes

**You make:** ~/Art/Painting/025-revoy-layer-map.kra
**Builds on:** lesson 024
**Time:** 45 min
**Read:** Pepper&Carrot ep06_The-Potion-Contest/E06P03.kra; Krita Manual, Layers; Krita Manual, Blending Modes

## The idea
David Revoy paints Pepper&Carrot in Krita and shares his files. Open one to see how a pro stacks layers. On a page from episode 6, the lines sit on a Multiply layer. A Soft Light texture layer, at about 40%, sits above the color group. The flat colors sit below, in a group.

> "Blending modes can not just apply to Layers, but also to individual strokes." (Krita Manual, Blending Modes).

## Look
In E06P03.kra, from top to bottom: txt-tmp (hidden), panel-frame, white, frame-extra, ink, texture-harmony, the group color (char, base), background.

## Steps
1. Open Krita. Open ~/Library/Painting/Pepper-and-Carrot/ep06_The-Potion-Contest/E06P03.kra. Do not save over it.
2. In the Layers docker, count the layers. Find the group color. Click its arrow to open it.
3. Click the eye of the ink layer.
   You should see: The black lines hide. Click it again.
4. Click the ink layer. Read its blending mode in the Layers docker.
   You should see: It is Multiply.
5. Click texture-harmony. Read its blending mode and opacity.
   You should see: It is Soft Light (SVG) at about 40%.
6. Hide texture-harmony.
   You should see: The picture looks flatter. Show it again.
7. Hold Alt and click the char layer.
   You should see: Only that layer shows. Alt-click again to go back.
8. Alt-click the base layer in the same way. See what it holds.
9. Close the file. Click No when Krita asks to save.
10. Make a new canvas 1600 by 2200. Add a layer named background.
11. Add a group named color. Put layers base and char inside it. Add layers ink and texture-harmony above it.
12. Set ink to Multiply. Set texture-harmony to Soft Light (SVG) at 40%. Check the order.
13. Use File ‣ Create Template from Image. Name it revoy stack.
14. Save the file with File ‣ Save As. Use the path ~/Art/Painting/025-revoy-layer-map.kra.

## Check your work
- Is the ink layer set to Multiply? (Yes.)
- Is the texture layer above the color group? (Yes.)
- Are the flat colors below the lines? (Yes.)

## Make it yours
- Open E06P01.kra and E06P05.kra. Write how the stack differs.
- Add one more layer to your map: a Screen layer for glow.

## New words
- **source file** — the real working file of an artist
- **stack** — the order of layers in a file
- **texture layer** — a layer of grain placed over the picture

---
Source: Pepper&Carrot by David Revoy, www.peppercarrot.com, CC BY 4.0 (Krita source files: www.peppercarrot.com/0_sources/). Krita Manual by the Krita Foundation and contributors, https://docs.krita.org, CC BY-SA 4.0 / GNU FDL 1.3.
