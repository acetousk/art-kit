# 006. Group and Move Layers

**You make:** ~/Art/Painting/006-groups.kra
**Builds on:** lesson 005
**Time:** 35 min
**Read:** Krita Manual, Group Layers; Krita Manual, Move Tool; Krita Manual, Transform Tool; Krita Manual, Layers Menu

## The idea
A group layer holds other layers, like a folder. Krita first mixes all layers inside the group. Then it puts the result in the stack. You can hide or move a whole group at once. The Move Tool slides a layer. The Transform Tool changes its size, turn, or shape.

> "All layers inside are combined first, and then this intermediate result is used on the outside" (Krita Manual, Group Layers).

## Look
Group Layers: read the second paragraph. Transform Tool: read the first paragraph and Free transform.

## Steps
1. Open Krita. Make a new 2400 by 1600 canvas.
2. Add three layers. Name them sun, hill, and tree. Paint one simple shape on each.
3. Click the sun layer. Hold Ctrl and click the hill and tree layers.
4. Press Ctrl+G.
   You should see: The three layers go into a new group.
5. Rename the group scene. Click its eye.
   You should see: All three shapes hide at once. Show them again.
6. Pick the Move Tool. Click the sun layer. Drag the sun to a new place.
7. Pick the Transform Tool. Drag a corner of the tree. Hold Shift to keep the shape.
   You should see: The tree gets bigger.
8. In the Transform Tool Options, click the flip horizontally button.
   You should see: The tree turns around.
9. Press Enter to confirm the transform.
10. Right-click the tree layer. Pick Duplicate Layer or Mask. Move the copy to the left.
11. Shrink the copy with the Transform Tool.
   You should see: You now have a near tree and a far tree.
12. Save the file with File ‣ Save As. Use the path ~/Art/Painting/006-groups.kra.

## Check your work
- Does hiding a group hide all layers inside it? (Yes.)
- Does Shift keep the shape the same while you resize? (Yes.)
- Does a duplicate layer give you a copy to change on its own? (Yes.)

## Make it yours
- Build a forest. Duplicate one tree five times. Scale each one.
- Group a face by parts: hair, skin, eyes.

## New words
- **group layer** — a folder that holds other layers
- **transform** — change a layer's size, turn, or shape
- **merge** — join two layers into one

---
Source: Krita Manual by the Krita Foundation and contributors, https://docs.krita.org, CC BY-SA 4.0 / GNU FDL 1.3.
