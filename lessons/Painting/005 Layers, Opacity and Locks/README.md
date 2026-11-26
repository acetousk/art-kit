# 005. Layers, Opacity and Locks

**You make:** ~/Art/Painting/005-layers.kra
**Builds on:** lesson 003
**Time:** 35 min
**Read:** Krita Manual, Introduction to Layers and Masks; Krita Manual, Layers; Krita Manual, Paint Layers

## The idea
Layers are like clear sheets stacked on a table. You paint on one sheet and the others stay safe. Krita draws the stack from bottom to top. A layer higher up covers the layers below it. Each layer has a name, an eye, an opacity slider, and a lock. Use layers to fix mistakes without hurting the rest of your picture.

> "In Krita instead of papers we use Layers." (Krita Manual, Introduction to Layers and Masks).

## Look
Layers (docker): find the eye, the lock, the Opacity slider, and the blending mode box. Paint Layers: read the last line about the hotkey.

## Steps
1. Open Krita. Make a new 2000 by 1400 canvas. Open the Layers docker.
2. Press Ins to add a new paint layer.
   You should see: A new layer shows in the stack.
3. Double-click the layer name. Type red. Press Enter.
4. Paint a big red circle on it.
5. Press Ins again. Name the new layer blue. Paint a blue circle that overlaps the red one.
6. Drag the blue layer below the red layer.
   You should see: The red circle now covers the blue one.
7. Click the eye on the red layer.
   You should see: The red circle hides. Click it again.
8. Set the Opacity slider of the red layer to 50%.
   You should see: You see the blue circle through the red.
9. Click the lock icon on the blue layer. Try to paint on it.
   You should see: Nothing changes. Unlock it.
10. Right-click the red layer. Pick a color label. Click the filter button and show only that color.
11. Add a third layer named yellow. Paint a yellow circle at the bottom of the stack.
12. Save the file with File ‣ Save As. Use the path ~/Art/Painting/005-layers.kra.

## Check your work
- Does the top layer in the stack cover the ones below it? (Yes.)
- Does the eye icon delete a layer? (No: it only hides it.)
- Can you paint on a locked layer? (No.)

## Make it yours
- Draw a face. Put eyes, nose, and mouth on three layers. Move them around.
- Name layers in a way that your future self can understand.

## New words
- **layer** — one clear sheet in a stack that you paint on
- **layer stack** — all layers, from bottom to top
- **opacity slider** — a bar that makes a layer more or less see-through

---
Source: Krita Manual by the Krita Foundation and contributors, https://docs.krita.org, CC BY-SA 4.0 / GNU FDL 1.3.
