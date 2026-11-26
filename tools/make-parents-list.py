# Writes the per-lesson list into PARENTS.md between the two marker lines.
# Run from the repo root after lessons change: python3 tools/make-parents-list.py
import glob, os, re
TOPICS = ["Drawing", "Painting", "Revoy", "Design", "Lettering", "Interior Design", "3D Drawing"]
APPS = [("Sweet Home 3D", "Sweet Home 3D"), ("Blender", "Blender"), ("Krita", "Krita")]
out = ["## Every lesson", "", "Each topic opens to a list: lesson number, title, the app, what your kid makes, and where the lesson comes from.", ""]
for t in TOPICS:
    rows = []
    for f in sorted(glob.glob(f"lessons/{t}/[0-9]*/README.md")):
        s = open(f).read()
        title = re.sub(r"^#\s*\d+\.\s*", "", s.splitlines()[0]).strip()
        num = os.path.basename(os.path.dirname(f))[:3]
        read = (re.search(r"^\*\*Read:\*\*\s*(.+)$", s, re.M) or [None, ""])[1].strip()
        make = (re.search(r"^\*\*You make:\*\*\s*(.+?)\s*$", s, re.M) or [None, ""])[1]
        make = os.path.basename(make.split(" (")[0].split(",")[0].replace("~/Art/", ""))
        apps = [n for k, n in APPS if k in s.split("## Steps", 1)[-1]] or ["Krita"]
        rows.append(f"| {num} | {title} | {' + '.join(apps)} | {make} | {read.replace('|', '/')} |")
    if not rows: continue
    out += [f"<details><summary><b>{t}</b> — {len(rows)} lessons</summary>", "",
            "| # | Lesson | App | Makes | Source |", "|---|---|---|---|---|"] + rows + ["", "</details>", ""]
p = "PARENTS.md"; s = open(p).read()
A, B = "<!-- lessons:start -->", "<!-- lessons:end -->"
block = A + "\n" + "\n".join(out) + B
s = re.sub(re.escape(A) + ".*?" + re.escape(B), lambda m: block, s, flags=re.S) if A in s else s.replace("## Is it safe?", block + "\n\n## Is it safe?", 1)
open(p, "w").write(s)
print(sum(1 for l in out if l.startswith("| 0") or l.startswith("| 1")), "lessons listed")
