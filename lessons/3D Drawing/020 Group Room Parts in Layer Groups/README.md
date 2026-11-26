# 020. Group Room Parts in Layer Groups

**You make:** add to 019-room.blend (save as 020-room-groups.blend)
**Builds on:** lessons 007–008, 019
**Time:** 30 min
**Read:** Blender Manual, Layers (Layer Tree, Add New Layer Group)

## The idea
A layer group holds several layers together. Quote: "Layers can be grouped using Layer Groups." Put the floor and walls in one group called Room. Put the character in another group. Hide or lock a whole group at once.

## Look
Look at the Layer Tree in the Object Data tab. Groups show a folder-like row above their layers.

## Steps
1. Open the file from lesson 019.
2. Open the Object Data tab in the Properties editor.
3. Click Add New Layer Group. A new group appears.
4. Rename the group Room.
5. Drag the Floor layer into the Room group.
6. Drag the Walls layer into the Room group.
7. Add a new layer called Furniture. Keep it outside the group.
8. Click the eye icon on the Room group. The room disappears.
9. Click the eye icon again. The room returns.
10. You should see: the Room group holds two layers, and Furniture stays outside.
11. Save the file as ~/Art/3D Drawing/020-room-groups.blend.

## Check your work
- Does the Room group hide every layer inside it?
- Is Furniture outside the group?
- Did you save the file?

## Make it yours
Make a group called Props. Put a table layer in it. Hide the group to check the room alone.

## New words
- **Group** — a set of layers that move together.
- **Layer Tree** — the list of layers and groups.
- **Nested** — placed inside another item.

---
Source: Blender Manual, Layers. Blender Team. CC BY-SA 4.0.
