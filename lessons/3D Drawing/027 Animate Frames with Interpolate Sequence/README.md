# 027. Animate Frames with Interpolate Sequence

**You make:** add to 026-onion.blend (save as 027-interpolate.blend)
**Builds on:** lessons 025–026
**Time:** 35 min
**Read:** Blender Manual, Interpolation (Interpolate Sequence)

## The idea
Interpolate Sequence adds in-between frames for you. Quote: "Interpolate strokes between the previous and next keyframe by adding multiple keyframes." Draw two key poses first. Then let Blender fill the frames between them. Check each frame after you run it.

## Look
Look at the Header menu for Interpolate. Look at the Step and Layer options.

## Steps
1. Open the file from lesson 026.
2. Go to frame 1. Draw a ball on the left.
3. Go to frame 10. Draw the same ball on the right.
4. Go to frame 5. This frame sits between the two keys.
5. Open the Header menu. Choose Interpolate.
6. Choose Interpolate Sequence.
7. Set Step to 1. Set Layer to Active.
8. Click OK or the confirm button.
9. Play the Timeline from frame 1 to frame 10.
10. You should see: the ball moves smoothly from left to right.
11. Save the file as ~/Art/3D Drawing/027-interpolate.blend.

## Check your work
- Did Interpolate Sequence add frames between your two keys?
- Does the ball move in even steps?
- Did you save the file?

## Make it yours
Draw a leaf falling from frame 1 to frame 12. Use Interpolate Sequence. Then fix one in-between frame by hand.

## New words
- **Interpolate** — make in-between frames from two keyframes.
- **Key pose** — a main frame you draw first.
- **Step** — how many frames between each new frame.

---
Source: Blender Manual, Interpolation. Blender Team. CC BY-SA 4.0.
