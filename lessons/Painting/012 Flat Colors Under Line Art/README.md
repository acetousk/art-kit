# 012. Flat Colors Under Line Art

**You make:** ~/Art/Painting/012-flat-colors.kra
**Builds on:** lesson 010
**Time:** 40 min
**Read:** Krita Manual, Flat Coloring; Krita Manual, Layers

## The idea
Flat colors are solid colors with no shading. Put the line art on top of the colors. Set the line layer to Multiply so the white of the lines vanishes. Then each color goes on its own layer under the lines. This is how comic artists color. When every color has its own layer, you can change one color without redoing the rest.

> "The layer docker is a way for you to control the drawing order of multiple images" (Krita Manual, Flat Coloring).

## Look
Flat Coloring: read Understanding Layers, then The Multiply Blending Mode. Look at the pink and blue example.

## Steps
1. Open Krita. Make a new 2400 by 1600 canvas.
2. Add a layer named lines. Pick the preset Ink Fineliner.
3. Draw a mushroom: a cap, a stem, three spots, and the ground. Close every shape.
4. Select the lines layer. In the blending mode box, change Normal to Multiply.
   You should see: The white around the lines is see-through.
5. Add a layer. Drag it under the lines layer. Name it cap.
6. Pick the Fill Tool. Click the cap with red.
   You should see: The cap fills. Check the edge for gaps.
7. Add a layer named stem. Put it under the lines. Fill the stem with cream.
8. Add a layer named spots. Fill the spots with white.
9. Add a layer named ground. Fill the ground with a green.
10. Hide the lines layer with its eye.
   You should see: You see flat shapes with no outlines. Show it again.
11. Pick the cap layer. Paint over the edge of the lines with red to close small gaps.
12. Save the file with File ‣ Save As. Use the path ~/Art/Painting/012-flat-colors.kra.

## Check your work
- Is the line layer above the color layers? (Yes.)
- Does Multiply hide the white of the line layer? (Yes.)
- Does each color have its own layer? (Yes, it should.)

## Make it yours
- Color a cartoon cat with six flat colors, each on its own layer.
- Change the color of one layer. See how little work it is.

## New words
- **line art** — a drawing made only of lines
- **multiply** — a mode that makes white vanish and darks stay
- **flats** — a first pass of solid colors without shading

---
Source: Krita Manual by the Krita Foundation and contributors, https://docs.krita.org, CC BY-SA 4.0 / GNU FDL 1.3.
