# Lesson rules v2 (all topic writers)

## Audience and device
- A kid, age 13. Smart, likes art. Reads at grade 7–8.
- Surface tablet + pen + Type Cover. Apps: **Krita 5.2** and **Sweet Home 3D 7**. No internet. No paper, paint, or ink.
- Her files: `~/Art` (read/write). Books and files: `~/Library` (read-only).

## Sources (all in /tmp/books/)
- Book PDFs + text (`<name>.pdf`, `<name>.txt`). The text has form-feed characters (`\f`) between pages: page N of the PDF = the text after the (N-1)th `\f`.
- **Cite PDF page numbers** (not printed page numbers). Check each one: `pdftotext -f N -l N -layout /tmp/books/<name>.pdf -`. Look at picture pages: `pdftoppm -f N -l N -r 50 -png <pdf> /tmp/<you>/p` then view the PNG.
- Krita Manual (CC BY-SA / GNU FDL, by the Krita team): `/tmp/books/krita-manual/` (xhtml). Use it for exact tool names, menus, and shortcuts. Cite as `Krita Manual, <page title>`.
- Sweet Home 3D User's Guide: `/tmp/books/SweetHome3D-Guide.txt`. Cite the section name.
- Never invent a page, a menu, a button, or a shortcut. If you cannot verify it, leave it out.

## One lesson = one folder
Write to `<OUT>/<NNN Title>/README.md` (NNN = 001, 002 …). Title: max 8 words, no `/ : "`.

```markdown
# NNN. Title

**You make:** ~/Art/<Topic>/<file>  (new file, or "add to" an earlier file)
**Builds on:** lesson NNN (or "nothing")
**Time:** 20–45 min
**Read:** <Source>, PDF pages N–M  (2–6 pages)

## The idea
3–6 short sentences. Explain the idea in plain words, as the author teaches it.
One short quote from the source (max 25 words), in quotes, with the page.

## Look
What to look at on the pages: "Page 14, the top drawing: see how the far lines get closer."

## Steps
8–15 numbered steps. One action per step. Max 20 words per step.
Name the app on step 1. Use the exact menu, tool, and docker names from the Krita Manual / SH3D Guide.
After hard steps, add a line: "You should see: …"
The last step saves the file to the "You make" path.

## Check your work
3 yes/no questions, about the idea (not only "did you save").

## Make it yours
1–2 ideas to try again with her own subject.

## New words
- **word** — meaning in under 12 words. (max 3 per lesson; use them again in later lessons)

---
Source: <full credit and license>
```

## Course rules
- Easy → hard. Each lesson uses skills from earlier lessons. Every ~8 lessons, add a **project lesson** that combines what came before (bigger file, 45–60 min, "Project" in the title).
- Translate physical exercises into Krita (name the brush preset, e.g. "Pencil-2", "Ink-2 Fineliner"; check names in the Krita Manual or use "a pencil brush preset").
- Skip dated social opinions and anything not right for a 13-year-old. Bridgman: hands, arms, head, face, legs from the front/side, feet, skeleton only. No nude torso, pelvis, or buttocks pages.
- Steps must be things she can do on the tablet now. No downloads, no internet, no add-ons.
- Write simple English: short sentences, active voice, common words.

## When done
Write `<OUT>/INDEX.md`: a table `| # | Title | Read | You make | Min |`. Then reply with: count, the list of PDF pages you could not verify (should be none), and any gaps.
