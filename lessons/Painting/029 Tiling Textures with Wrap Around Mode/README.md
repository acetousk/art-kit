# 029. Tiling Textures with Wrap Around Mode

**You make:** ~/Art/Painting/029-tile-texture.kra
**Builds on:** lesson 027
**Time:** 45 min
**Read:** Krita Manual, View Menu; Krita Manual, Patterns; Krita Manual, Fill Tool; Krita Manual, Common Workflows

## The idea
A tile is a small picture that repeats with no seam. In Wrap Around Mode the canvas repeats on every side as you paint. Paint off the right edge and the stroke comes in on the left. You check the seams as you work. You can turn the tile into a pattern, and fill a whole page with it. Revoy's texture layers do the same job: a tiled grain on top of the colors.

> "This will show the image as if tiled orthographically." (Krita Manual, View Menu, on Wrap Around Mode).

## Look
View Menu: find Wrap Around Mode in the list. Patterns: read Temporary patterns and generating patterns from the canvas.

## Steps
1. Open Krita. Make a new 512 by 512 canvas. Fill the background with a mid green.
2. Open View ‣ Wrap Around Mode.
   You should see: You see the canvas repeat in all directions.
3. Pick a Basic preset. Paint a grass blade that crosses the right edge.
   You should see: The rest of it comes in from the left.
4. Paint more blades. Let some cross the top and the bottom edges.
5. Add a layer. Paint small dots with a brush from the Textures family. Use a darker green.
6. Look at the repeat. Fill any hole that looks empty. Remove any shape that looks like a stamp.
7. In the toolbar, open the pattern drop-down. Open the Custom tab. Press Update.
8. Click Use as Pattern.
   You should see: Your tile is now the current pattern.
9. Turn off Wrap Around Mode. Make a new 2400 by 1600 canvas.
10. Open Edit ‣ Fill with Pattern.
   You should see: The page fills with your tile.
11. Pick the Fill Tool. Set Fill Source to Pattern. Set Scale to 50%. Fill a new layer. Compare.
12. Set that layer to Soft Light at 40%.
   You should see: You get a grain over the page. Close the test canvas.
13. Go back to the tile. Save the file with File ‣ Save As. Use the path ~/Art/Painting/029-tile-texture.kra.

## Check your work
- Does a stroke that leaves the right edge come back on the left? (Yes, in Wrap Around Mode.)
- Should a tile show no seams when it repeats? (Yes.)
- Can you set a tile as a pattern for the Fill Tool? (Yes.)

## Make it yours
- Make a tile for brick, water, or stone.
- Use a tile as a texture layer over a flat painting.

## New words
- **tile** — a small picture that repeats with no seam
- **seam** — a line where two tiles meet and do not match
- **pattern** — a tile Krita can use to fill an area

---
Source: Krita Manual by the Krita Foundation and contributors, https://docs.krita.org, CC BY-SA 4.0 / GNU FDL 1.3. Pepper&Carrot by David Revoy, www.peppercarrot.com, CC BY 4.0 (Krita source files: www.peppercarrot.com/0_sources/).
