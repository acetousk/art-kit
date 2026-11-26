# 017. Blending Soft Edges

**You make:** ~/Art/Painting/017-soft-edges.kra
**Builds on:** lesson 016
**Time:** 35 min
**Read:** Krita Manual, Color Smudge Brush Engine; Krita Manual, Krita 4 Preset Bundle Overview; Krita Manual, Blur (Filters)

## The idea
A hard edge ends fast. A soft edge fades. Round forms need soft edges where light turns into shadow. Flat forms keep hard edges. Krita can soften with a Blender preset, a soft airbrush, or the Gaussian Blur filter. A shadow is sharp near its object and soft far away.

> "The Color Smudge Brush is a brush engine that allows you to mix colors by smearing or dulling." (Krita Manual, Color Smudge Brush Engine).

## Look
Preset Bundle Overview: read Blender. Blur filters: read Gaussian Blur.

## Steps
1. Open Krita. Open ~/Art/Painting/016-forms.kra. Save it as 017-soft-edges.kra.
2. Click the cylinder layer. Pick a Blender preset.
3. Drag across the cylinder gradient in short strokes.
   You should see: The tones melt smoothly.
4. Click the cube right layer. Smear the border between two cube faces with the Blender.
   You should see: The sharp corner melts and the cube looks flat.
5. Undo with Ctrl+Z. Cubes keep hard edges.
6. Click the cast shadows layer. Pick the Rectangular Selection Tool. Select the part of the shadow far from the objects.
7. Open Filter ‣ Blur ‣ Gaussian Blur. Set a radius of 15. Click OK.
   You should see: The far shadow softens.
8. Select the part of the shadow near the objects. Blur it with a radius of 3.
9. Deselect. Look at the shadows.
   You should see: They are sharp at the object and soft far away.
10. Add a layer named contact. Set it to Multiply. Paint a thin dark line where the cube touches the floor.
11. Compare with the old file 016. Which one looks more real?
12. Save the file with File ‣ Save As. Use the path ~/Art/Painting/017-soft-edges.kra.

## Check your work
- Do round forms need soft edges between light and shadow? (Yes.)
- Do cube faces keep their hard edges? (Yes.)
- Is a cast shadow sharper near the object? (Yes.)

## Make it yours
- Soften one side of a ball and keep the other hard. See which looks better.
- Blur a tree line to make fog.

## New words
- **soft edge** — an edge that fades into the next area
- **hard edge** — an edge that ends fast
- **blur** — a filter that softens a layer

---
Source: Krita Manual by the Krita Foundation and contributors, https://docs.krita.org, CC BY-SA 4.0 / GNU FDL 1.3.
