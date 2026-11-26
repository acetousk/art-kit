# 035. Project A Small Animation

**You make:** ~/Art/Painting/035-small-animation.kra
**Builds on:** lessons 015, 024, 034
**Time:** 60 min
**Read:** Krita Manual, Animation with Krita; Krita Manual, Animation Timeline Docker; Krita Manual, Render Animation

## The idea
Make a short animation of a painted ball that bounces. Use the light and shadow from lesson 015 and the frame skills from lesson 034. The background sits on its own layer with no frames, so it stays still. The ball and its shadow share the frames. Draw the key poses first, then the in-betweens, then render.

> "Krita will first render to a PNG sequence and then use a video encoder to render that sequence to an animated file format." (Krita Manual, Render Animation).

## Look
Render Animation: read General and Export as Image Sequence. Animation Timeline Docker: read about keyframe, duplicate keyframe, and hold.

## Steps
1. Open Krita. Make a new 800 by 450 canvas. Switch to the Animation workspace. Set the frame rate to 12.
2. Add a layer named background. Paint a simple room with a floor, using a Linear gradient. Do not animate it.
3. Add a layer named shadow. Create a blank frame at the first square.
4. Draw an oval shadow on the floor. Set the layer to Multiply.
5. Add a layer named ball. Create a blank frame at the first square.
6. Paint a shaded ball high in the air, with a highlight.
7. Click the lightbulb icon on the ball layer.
   You should see: Onion skin turns on.
8. Make the key poses on both layers: high, floor (squashed), high again. Place them at frames 0, 6, 12.
9. Draw the in-between frames. Put the ball lower and the shadow bigger on the way down. Use onion skin.
10. Scrub through the frames, then click Play.
   You should see: The ball and the shadow move together.
11. Fix any jump. Check that the background shows on every frame.
12. Open File ‣ Render Animation. Pick Export as Image Sequence.
13. Set the Image Location to ~/Art/Painting. Set the Base Name to bounce.
14. Click OK.
   You should see: PNG frames appear in the folder.
15. Save the file with File ‣ Save As. Use the path ~/Art/Painting/035-small-animation.kra.

## Check your work
- Does the shadow move with the ball? (It should.)
- Is the background still on every frame? (It should be.)
- Does the ball squash at the floor? (It should.)

## Make it yours
- Animate a candle flame.
- Make a 24-frame loop of a walking cat.

## New words
- **in-between** — a frame drawn between two key poses
- **render** — turn your work into frames or a video file
- **loop** — an animation that repeats with no jump

---
Source: Krita Manual by the Krita Foundation and contributors, https://docs.krita.org, CC BY-SA 4.0 / GNU FDL 1.3.
