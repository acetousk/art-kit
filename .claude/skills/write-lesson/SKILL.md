---
name: write-lesson
description: Write a new Art Kit lesson with the user. Use when the user says "write a lesson", "new lesson", "add a lesson", or "make a tutorial" in the Art Kit repo.
---

# Write a lesson

Use this skill to add one lesson folder to `lessons/`. Follow `lessons/RULES.md` for the format.

## Hard rules

- Do not invent a PDF page, menu, tool, button, or shortcut.
- If you cannot check an item, leave it out.
- Make every step work offline on the kiosk.
- Do not use a browser, a PDF viewer, or a timer app in steps.
- Book pages show in the Library app.
- Use only open sources: public domain, CC0, CC BY, CC BY-SA, GNU FDL, or the author's own teaching.
- Keep the content safe for children. Skip nude pages and unsuitable opinions.
- Do not put personal names, towns, or accounts in the repo.

## Steps

1. Ask for the topic. Use a folder in `lessons/`, or a new folder name.
2. Ask for the learner's age and level.
3. Ask what the learner will make. Get the file name and path.
4. Ask for the source. Check that its license is open. If it is not, ask for another source.
5. Find the next free number. List `lessons/<Topic>/` and add 1 to the highest `NNN`.
6. Check each cited PDF page. Run `pdftotext -f N -l N -layout <file.pdf> -`.
7. Check that the page text supports the claim. If not, find the right page.
8. Check each menu, tool, and shortcut. Use the Krita Manual or the Sweet Home 3D User's Guide.
9. Write the exact names from those sources. Do not shorten or guess them.
10. Create `lessons/<Topic>/<NNN Title>/README.md`. Use the template in `lessons/RULES.md`.
11. Keep the title under 9 words. Do not use `/`, `:`, or `"` in the title.
12. If the source is new, add one line to `library/books.txt`: `folder|name|url|pages|remove|credit`.
13. Add the lesson to its unit in `lessons/COURSE.md`.
14. Read the lesson as a 13-year-old would. Mark each step that is unclear.
15. Fix each marked step. Check the PDF pages and menu names again.
16. Report the lesson path. List any page you could not check.

## Check the lesson

| Check | Pass when |
|---|---|
| Pages | Every page in `Read:` shows the cited idea |
| Menus | Every menu and tool name matches the manual |
| Steps | Each step has one action and at most 20 words |
| Offline | No step needs a browser, a PDF viewer, or a timer |
| Privacy | No personal names or accounts appear |
| Length | 8 to 15 steps, 3 check questions, 3 new words at most |
