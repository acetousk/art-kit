# 024. Transparency and Filter Masks

**You make:** ~/Art/Painting/024-masks.kra
**Builds on:** lesson 023
**Time:** 45 min
**Read:** Krita Manual, Transparency Masks; Krita Manual, Filter Masks; Krita Manual, Clone Layers

## The idea
A mask changes a layer without damaging it. A transparency mask hides or shows parts. You paint black to hide and white to show. A filter mask applies a filter, like blur, to the part you choose. A clone layer is a live copy of another layer. With these three you can fix and tweak a painting later without painting it again.

> "Black paints transparency (see-through), white paints opacity (visible)." (Krita Manual, Transparency Masks).

## Look
Transparency Masks: read How to add a transparency mask. Filter Masks: read the paragraph on editing a filter mask. Clone Layers: read the glow example.

## Steps
1. Open Krita. Make a new 2400 by 1600 canvas. Fill the background with dark blue.
2. Add a layer named moon. Paint a pale circle with a Basic preset.
3. Click the + drop-down in the Layers docker. Pick Transparency Mask.
   You should see: A mask appears under the moon layer.
4. Click the mask. Paint black over half the moon.
   You should see: That half hides.
5. Paint white over it.
   You should see: The half returns. Nothing was lost.
6. Paint gray with a soft brush on the edge.
   You should see: The moon fades.
7. Add a layer named trees. Paint dark pine trees with a hard brush.
8. Add a Filter Mask on trees. Pick Gaussian Blur. Set a radius of 8.
9. Click the mask. Paint black on the near trees. Paint white on the far trees.
   You should see: Only the far trees blur.
10. Add a layer named star. Paint one bright star.
11. Use the + drop-down to add a Clone Layer of the star. Put it below star.
12. Add a Gaussian Blur filter mask to the clone.
13. Set the clone layer blending mode to Color Dodge.
   You should see: A glow shows around the star.
14. Save the file with File ‣ Save As. Use the path ~/Art/Painting/024-masks.kra.

## Check your work
- Does black on a transparency mask hide paint? (Yes.)
- Does a mask delete the paint under it? (No.)
- Does a clone layer follow the layer it copies? (Yes.)

## Make it yours
- Make a ghost with a clone layer and a lens blur.
- Fade a mountain into fog with a transparency mask.

## New words
- **mask** — a layer part that hides or shows another layer
- **filter mask** — a mask that applies a filter to part of a layer
- **clone layer** — a live copy of another layer

---
Source: Krita Manual by the Krita Foundation and contributors, https://docs.krita.org, CC BY-SA 4.0 / GNU FDL 1.3.
