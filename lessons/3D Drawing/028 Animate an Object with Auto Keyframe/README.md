# 028. Animate an Object with Auto Keyframe

**You make:** add to 027-interpolate.blend (save as 028-object-move.blend)
**Builds on:** lessons 021, 027
**Time:** 30 min
**Read:** Blender Manual, Grease Pencil, Animation (Introduction); Keyframe Editing (Auto Keyframe)

## The idea
You can move a whole object over time. Quote: "Auto Keyframe adds keyframes automatically to the set frame if the value for transform type properties changes." Turn on Auto Keyframe first. Then move the object on one frame. Blender stores the new place. Move the object again on a later frame.

## Look
Look at the record button in the Timeline header. It is Auto Keyframe. Look at the Move gizmo.

## Steps
1. Open the file from lesson 027.
2. In Object Mode, select the character Grease Pencil object.
3. In the Timeline header, turn on Auto Keyframe.
4. Go to frame 1.
5. Drag the Move gizmo to the left side of the room.
6. Go to frame 20.
7. Drag the Move gizmo to the right side of the room.
8. Play the Timeline from frame 1 to frame 20.
9. You should see: the character slides from left to right.
10. Save the file as ~/Art/3D Drawing/028-object-move.blend.

## Check your work
- Did Auto Keyframe create keys when you moved the object?
- Does the character move between the two places?
- Did you save the file?

## Make it yours
Add a turn. Go to frame 10. Use the Rotate gizmo to turn the character a little.

## New words
- **Auto Keyframe** — record a key when you change an object.
- **Transform** — move, turn, or size.
- **Timeline** — the bar that shows frames and keys.

---
Source: Blender Manual, Grease Pencil, Animation, Introduction; Keyframe Editing. Blender Team. CC BY-SA 4.0.
