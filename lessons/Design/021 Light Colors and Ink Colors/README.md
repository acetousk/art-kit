# 021. Light Colors and Ink Colors

**You make:** ~/Art/Design/021-rgb-cmy.kra (new file)
**Builds on:** lesson 020
**Time:** 35 min
**Read:** Design Fundamentals (Hass 2015), PDF pages 58–59; Krita Manual, Layers; Krita Manual, Advanced Color Selector; Krita Manual, Blending Modes

## The idea
Screens make color with light. Red, green, and blue light add up to white. This is the additive system, or RGB. Printed ink works the other way. Cyan, magenta, and yellow ink take light away, which is the subtractive system. Hass says to pick colors that work in both.

> "Always choose colours that will work in both systems." (Design Fundamentals, PDF page 59)

## Look
Page 58: find the heading RBG and CMYK Colour Spaces. Page 59: see Figure 3.5, the two sets of overlapping circles, and read the last paragraph.

## Steps
1. Open Krita. Make a new document 1500 x 2000 px at 150 ppi.
2. Fill the whole page with black. Use Edit ‣ Fill with Foreground Color (Shift + Backspace).
3. Add a new Paint Layer. Pick a pure red in the Advanced Color Selector docker.
4. Draw a big circle with the Ellipse Tool.
5. Add two more layers. Make a green circle and a blue circle that overlap the red one.
6. In the Layers docker, set the Blending Mode of each color layer to Addition.
   You should see yellow, cyan, magenta, and white where the circles overlap.
7. Add a new Paint Layer above all the others. Fill it with white.
8. Make three new layers with cyan, magenta, and yellow circles that overlap.
9. Set each of these layers to the Multiply Blending Mode.
   You should see red, green, blue, and a dark center where they overlap.
10. Use the Text Tool. Label the top "light (RGB)" and the bottom "ink (CMYK)".
11. Toggle the layer eyes to compare. Write which pair you prefer in small text.
12. Press Ctrl + S. Save as ~/Art/Design/021-rgb-cmy.kra.

## Check your work
- Did the light circles make white at the center?
- Did the ink circles get darker at the center?
- Can you say which system a screen uses?

## Make it yours
- Make a poster for a light show using the additive circles.
- Pick one color you love. Is it easy to print?

## New words
- **additive** — making color by adding light
- **subtractive** — making color by taking light away with ink
- **RGB** — red, green, and blue light

---
Source: Graphic Design and Print Production Fundamentals, Graphic Communications Open Textbook Collective (Alex Hass, Ken Jeffery and others), BCcampus, 2015. CC BY 4.0. Tool names: Krita Manual (Krita team), CC BY-SA / GNU FDL.
