# 023. Overlay, Soft Light and Color

**You make:** ~/Art/Painting/023-overlay-color.kra
**Builds on:** lesson 015
**Time:** 40 min
**Read:** Krita Manual, Mix (Overlay); Krita Manual, Lighten (Soft Light); Krita Manual, HSX (Color)

## The idea
Overlay uses Multiply on dark parts and Screen on light parts. It adds contrast and color together. Soft Light is a gentler Overlay. Color is different: it keeps the light and dark of the layer below and swaps in the hue and saturation of your layer. That makes it great for coloring a gray painting. Always check the value in gray first.

> "This is useful for deepening shadows and highlights." (Krita Manual, Mix, on Overlay).

## Look
Mix: read Overlay. Lighten: read Soft Light. HSX: read the first lines of Color.

## Steps
1. Open Krita. Open ~/Art/Painting/015-sphere-light.kra. Save it as 023-overlay-color.kra.
2. Add a layer named tint above the ball. Set its blending mode to Color.
3. Pick a red. Paint over the ball with a big brush.
   You should see: The ball turns red. The light and dark stay the same.
4. Paint the floor with a green.
   You should see: The floor turns green. The values stay.
5. Add a layer named overlay. Set it to Overlay.
6. Paint warm orange on the upper left.
   You should see: The light side glows and the contrast rises.
7. Add a layer named soft. Set it to Soft Light.
8. Paint the same orange in the same spot.
   You should see: The effect is milder.
9. Lower the opacity of overlay to 50%. Compare it to soft.
10. Paint a bright blue on the lower right on the overlay layer.
   You should see: The shadow side turns cool and deep.
11. Hide the tint layer.
   You should see: The picture stays gray with a light glow. Show it again.
12. Save the file with File ‣ Save As. Use the path ~/Art/Painting/023-overlay-color.kra.

## Check your work
- Does Color keep the light and dark of the layer below? (Yes.)
- Is Soft Light milder than Overlay? (Yes.)
- Does Overlay raise contrast? (Yes.)

## Make it yours
- Color a gray drawing of a face with only the Color mode.
- Try a Soft Light layer with white and black strokes to add light and dark.

## New words
- **overlay** — a mode that darkens darks and lightens lights
- **soft light** — a milder overlay
- **color mode** — a mode that swaps hue but keeps light and dark

---
Source: Krita Manual by the Krita Foundation and contributors, https://docs.krita.org, CC BY-SA 4.0 / GNU FDL 1.3.
