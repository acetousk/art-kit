# 031. Character Light and Finish

**You make:** ~/Art/Painting/031-character-finish.kra
**Builds on:** lesson 030
**Time:** 45 min
**Read:** Krita Manual, Clipping Masks and Alpha Inheritance; Krita Manual, Layers; Krita Manual, File Menu

## The idea
Shade each part of your character on a clipping layer. Pick one light direction, like on the ball in lesson 015. Use Multiply for shade and Screen for rim light. Recolor the lines with Alpha Lock, so the lines are warm in the light and dark in the shadow. Finish with a soft texture on top. Then export a PNG file you can share.

> "Combined with group layers this can be quite powerful." (Krita Manual, Clipping Masks and Alpha Inheritance).

## Look
Clipping Masks and Alpha Inheritance: read the quick clipping group paragraph. File Menu: find Export.

## Steps
1. Open Krita. Open ~/Art/Painting/030-character-flats.kra. Save it as 031-character-finish.kra.
2. Click the hair layer. Press Ctrl+Shift+G.
   You should see: A clipping group forms with a new layer on top.
3. Set the new layer to Multiply. Paint a darker hair color on the right side.
4. Do the same for the hat and the clothes. Use the same light side.
5. Select the skin layer. Make a clipping group. Paint a soft warm shade on the right of the face.
6. Add a layer named rim above the color group. Set it to Screen. Paint thin light on the left edges.
7. Click the lines layer. Turn on Alpha Lock.
8. Paint dark brown over the hair lines and red-brown over the skin lines.
9. Add a layer below everything named background. Fill with a Linear gradient from a deep teal to a pale teal.
10. Add a layer named texture on top. Fill it with your pattern from lesson 029.
11. Set the texture layer to Soft Light at 40%.
12. Check the values with a gray filter layer. Hide it again.
13. Open File ‣ Export. Pick PNG. Save as ~/Art/Painting/031-character-finish.png.
14. Save the file with File ‣ Save As. Use the path ~/Art/Painting/031-character-finish.kra.

## Check your work
- Is all shade on the same side of the character? (It should be.)
- Does the Screen rim light sit on the lit side? (Yes.)
- Do Alpha Lock recolored lines look softer than black ones? (Often yes.)

## Make it yours
- Add a cat on the shoulder with the same light.
- Recolor your character in a night scene with a cool light.

## New words
- **rim light** — a thin light along an edge from behind
- **export** — save a copy as another file type, like PNG
- **finish** — the last pass that makes a piece feel done

---
Source: Krita Manual by the Krita Foundation and contributors, https://docs.krita.org, CC BY-SA 4.0 / GNU FDL 1.3.
