# 022. Multiply and Screen

**You make:** ~/Art/Painting/022-multiply-screen.kra
**Builds on:** lesson 021
**Time:** 40 min
**Read:** Krita Manual, Blending Modes; Krita Manual, Arithmetic (Multiply); Krita Manual, Lighten (Screen)

## The idea
A blending mode sets how a layer mixes with the layers below it. Multiply makes colors darker and keeps the color below, so it is best for shadows. Screen is its opposite and is best for glow. Dark colors in a Screen layer vanish. Light colors in a Multiply layer vanish.

> "This results in light tones being more opaque and dark tones transparent." (Krita Manual, Lighten, on Screen).

## Look
Blending Modes: look at the list of favorites. Arithmetic: read Multiply. Lighten: read Screen.

## Steps
1. Open Krita. Open ~/Art/Painting/021-colored-still-life.kra. Save it as 022-multiply-screen.kra.
2. Add a layer named shade above the apple layer. Set its blending mode to Multiply.
3. Pick a blue-purple and a soft airbrush preset. Paint a shadow on the lower right of the apple and cup.
   You should see: The shadow keeps the color of the object.
4. Switch shade to Normal. Look at the same strokes.
   You should see: They look flat and gray. Switch back to Multiply.
5. Add a layer named glow above shade. Set its blending mode to Screen.
6. Pick a warm orange. Paint a soft glow on the upper left edges of each object.
   You should see: The edges look lit.
7. Paint dark orange on the glow layer.
   You should see: Almost nothing shows. Dark colors vanish in Screen.
8. Lower the opacity of glow to 70%. Lower shade to 80%.
9. Hold Alt and Shift. Press M.
   You should see: The brush now paints in Multiply, without a layer mode.
10. Paint one stroke on a Normal layer. Look at the result. Press Alt+Shift+N to go back to Normal.
11. Group shade and glow. Name the group light and shade.
12. Save the file with File ‣ Save As. Use the path ~/Art/Painting/022-multiply-screen.kra.

## Check your work
- Does Multiply make colors darker? (Yes.)
- Do dark colors disappear in a Screen layer? (Yes.)
- Can a blending mode work on one brush stroke, not only a layer? (Yes.)

## Make it yours
- Add a candle to the table. Use Screen for its glow.
- Paint a shadow under a tree with Multiply.

## New words
- **blending mode** — a rule for how a layer mixes with those below
- **multiply** — a mode that makes colors darker
- **screen** — a mode that makes colors lighter

---
Source: Krita Manual by the Krita Foundation and contributors, https://docs.krita.org, CC BY-SA 4.0 / GNU FDL 1.3.
