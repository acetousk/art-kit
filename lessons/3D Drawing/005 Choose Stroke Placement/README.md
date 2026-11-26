# 005. Choose Stroke Placement

**You make:** ~/Art/3D Drawing/005-placement.blend
**Builds on:** lesson 004
**Time:** 30 min
**Read:** Blender Manual, Stroke Placement; 3D Cursor

## The idea
Stroke Placement sets where new strokes go in 3D. Quote: "The Stroke Placement selection only affects new strokes and does not affect the existing ones." Origin puts strokes at the object center. 3D Cursor puts them at the cursor. Surface puts them on a mesh. Stroke makes them stick to other strokes.

## Look
Look at the Stroke Placement pop-over in the Draw Mode header. It shows four options: Origin, 3D Cursor, Surface, Stroke.

## Steps
1. Open the file from lesson 004.
2. In Object Mode, choose the Cursor tool in the Toolbar.
3. Click one empty spot in the viewport. The 3D cursor moves there.
4. Open the Mode menu. Choose Draw Mode.
5. Open the Stroke Placement pop-over in the header.
6. Choose 3D Cursor.
7. Draw a short line. It starts at the 3D cursor.
8. Open Stroke Placement again. Choose Origin.
9. Draw a second short line near the first.
10. You should see: the first line starts at the cursor. The second line starts at the object origin.
11. Save the file as ~/Art/3D Drawing/005-placement.blend.

## Check your work
- Did the first stroke start at the 3D cursor?
- Did changing Stroke Placement change only new strokes?
- Did you save the file with the new name?

## Make it yours
Choose Stroke. Draw a line that starts at the end of an old stroke.

## New words
- **3D Cursor** — a point in 3D space. Blender uses it as a reference.
- **Origin** — the center point of an object.
- **Pop-over** — a small panel that opens over the header.

---
Source: Blender Manual, Stroke Placement; 3D Cursor. Blender Team. CC BY-SA 4.0.
Watch (adult, online): Blender Studio, Grease Pencil Fundamentals, "Drawing and Layout in the 3D space". Menus are from Blender 2.8.
