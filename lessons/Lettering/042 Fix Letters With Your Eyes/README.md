# 042. Fix Letters With Your Eyes

**You make:** ~/Art/Lettering/font-lower.kra  and  font-caps.kra  (edit)
**Builds on:** lesson 041
**Time:** 45 min
**Read:** Design With FontForge, PDF pages 24, 25, 26, 29, 30 and 31; Brown, PDF page 32

## The idea
FontForge says measuring is not enough. The eye sees optical illusions, so you should change shapes until they look right. A horizontal bar with the same thickness as a vertical stem looks too heavy, so thin it a little. A diagonal looks heavier than a vertical but lighter than a horizontal. Round letters must overshoot flat ones, and pointy letters must overshoot more.

> "making changes until it "looks right" is the correct thing to do." (Design With FontForge, PDF p. 24)

## Look
FontForge page 24: see the two H letters. Page 25: see the diagonals. Page 30: see the crossing diagonals in X. Page 31: see the round and pointed shapes before and after.

## Steps
1. Open Krita. Open font-caps.kra. Save As font-caps-fixed.kra.
2. Open the Grids and Guides docker. Set X spacing and Y spacing to 5 px. Set Subdivision to 5.
3. H: select the bar with the Rectangular Select tool and press Delete. Draw it again at 44 px.
   You should see: a bar that looks as heavy as the stems.
4. Do the same for the horizontal strokes of E, F, T and Z. Use 44 px.
5. Redraw the diagonals of A, V, W, X, Y, K, M and N at 47 px.
6. O: delete it. Draw it again from (3, 3) to (15, 15), but 5 px bigger on every side.
   You should see: O looks the same height as H.
7. Do the same for C, G, Q and S: 5 px overshoot.
8. Let the points of A, V and W pass the guide by 8 px.
9. X: the two diagonals look misaligned where they cross. Move the top half 3 px sideways and judge by eye.
10. Write HOHOH and AVAV. Do they look even in height?
11. Repeat the fixes in font-lower.kra for o, e, s and the points of v and w.
12. Press Ctrl+S in both files.

## Check your work
- Do the thinner bars look as heavy as the stems?
- Do the round letters look as tall as the flat letters?
- Do the points of A and V look level with H?

## Make it yours
- Test an overshoot of 10 px. Is it too much?
- Try thinning a diagonal by 6 px.

## New words
- **overshoot** — a curve or point that goes a little past the guide
- **optical correction** — a change that makes a shape look right
- **illusion** — something that looks different from its measure

---
Source: The FontForge Project Contributors, Design With FontForge (free documentation, credited); Frank Chouteau Brown, Letters and Lettering: A Treatise with 200 Examples, 1902 (public domain); Krita Manual, by the Krita team (CC BY-SA / GNU FDL). Tool names from the Krita Manual (CC BY-SA / GNU FDL).
