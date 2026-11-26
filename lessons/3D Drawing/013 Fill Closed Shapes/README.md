# 013. Fill Closed Shapes

**You make:** add to 012-project-shapes.blend (save as 013-fill.blend)
**Builds on:** lessons 009 and 012
**Time:** 30 min
**Read:** Blender Manual, Fill Tool

## The idea
The Fill tool colors the area inside closed lines. Quote: "The Fill tool creates filled Grease Pencil strokes by detecting enclosed regions formed by existing strokes." The Delaunay solver uses the stroke shape. The Pixel solver checks the drawing like an image. Use Delaunay for clean lines. Use Pixel for sketches.

## Look
Look at the Fill tool settings. Look at the Direction option. Look at the Fill Solver option under Advanced.

## Steps
1. Open the file from lesson 012. Stay in Draw Mode.
2. Choose the Fill tool in the Toolbar.
3. Pick a fill material in the Tool Settings.
4. Click inside the floor shape. The floor fills.
5. Hold Ctrl and click inside the room. The fill goes outside the shape.
6. Press Ctrl-Z to undo the fill.
7. Open Advanced. Check that Fill Solver is Delaunay.
8. Click inside the back wall. The wall fills.
9. You should see: each closed shape has a fill color.
10. Save the file as ~/Art/3D Drawing/013-fill.blend.

## Check your work
- Did the floor fill when you clicked inside it?
- Did Ctrl change which side fills?
- Did you save the file?

## Make it yours
Draw an open shape with a gap. Use Fill on it. Close the gap with the Line tool. Fill again.

## New words
- **Solver** — the method that finds the closed area.
- **Delaunay** — a fill method that uses the stroke shape.
- **Boundary** — the lines that stop the fill.

---
Source: Blender Manual, Fill Tool. Blender Team. CC BY-SA 4.0.
