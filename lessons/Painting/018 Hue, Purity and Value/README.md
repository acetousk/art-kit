# 018. Hue, Purity and Value

**You make:** ~/Art/Painting/018-hue-value.kra
**Builds on:** lesson 017
**Time:** 40 min
**Read:** Color Problems (Vanderpoel), PDF pages 48–50; Krita Manual, Advanced Color Selector; Krita Manual, Color Models

## The idea
Vanderpoel says every color has three qualities. Hue is the color family, like red or blue. Purity is how free the color is from white, black, or gray. Luminosity is how light or dark it looks. Value matters most in a painting. A pure yellow is light, and a pure violet is dark.

> "The second quality or constant of colors is purity, that is, its lack of any mixture of white, black, or any other color." (Vanderpoel, PDF page 49).

## Look
Page 49: read the three qualities. Page 50: find the line that a yellow room is the lightest room.

## Steps
1. Open Krita. Make a new 2400 by 1200 canvas. Open the Advanced Color Selector docker (Settings ‣ Dockers).
2. Click the settings icon of the docker. Choose the HSV model.
3. Draw six boxes in a row with a rectangle selection. Fill them red, orange, yellow, green, blue, and violet.
4. Add a layer. Draw six boxes below the first row. Use the same hues but pick them with low saturation.
   You should see: The colors are duller. Each is less pure.
5. Add a layer. Draw six more boxes below. Use the same hues but lower the value.
   You should see: The colors are darker.
6. Click the + in the layer stack. Add a Filter Layer. Pick HSV/HSL Adjustment.
7. Set Saturation to -100. Click OK.
   You should see: The picture turns gray.
8. Look at the top row. Which hue is the lightest gray? Which is the darkest?
9. Hide the filter layer. Look again. Say it aloud: yellow is light, violet is dark.
10. Write the words hue, purity, and value near the rows with the Text Tool.
11. Look at each row. Write which quality changes in that row.
12. Save the file with File ‣ Save As. Use the path ~/Art/Painting/018-hue-value.kra.

## Check your work
- Is the hue the family of the color, like red or blue? (Yes.)
- Is a pure yellow lighter than a pure violet? (Yes.)
- Does a gray view show value? (Yes.)

## Make it yours
- Check your last painting with a gray filter layer. Is the value clear?
- Make a value scale from white to black in nine steps.

## New words
- **hue** — the color family, like red or blue
- **saturation** — how pure a color is, free of gray
- **luminosity** — how light a color looks

---
Source: Color Problems by Emily Noyes Vanderpoel, 1903 (public domain). Krita Manual by the Krita Foundation and contributors, https://docs.krita.org, CC BY-SA 4.0 / GNU FDL 1.3.
