# 043. Stair and Ramp Math

**You make:** add to ~/Art/Interior Design/My-Home/My-Home.sh3d
**Builds on:** lesson 042
**Time:** 35–45 min
**Read:** ADA 2010 Standards, PDF pages 131–133 and 157

## The idea
Stairs and ramps follow math. The ADA says every riser is 4 in to 7 in high and every tread at least 11 in deep. All steps in one flight must match. A ramp slope is 1:12 at most: 1 in of rise needs 12 in of run. One ramp run may rise 30 in at most, and needs a 60 in landing at each end. Over 6 in of rise, a ramp needs handrails.
"Risers shall be 4 inches (100 mm) high minimum and 7 inches (180 mm) high maximum." (ADA, section 504.2, PDF page 157)

## Look
- PDF page 157, top: find 504.2 and Figure 504.5 (stair nosings).
- PDF page 131, bottom: find 405.2, the 1:12 slope.
- PDF page 132: find 405.5 (36 in wide) and 405.6 (30 in rise).
- PDF page 133: find 405.7.3, the 60 in landing.

## Steps
1. Open My-Home.sh3d. Open Plan > Levels > Modify level… Read the upper level's elevation.
2. This is the total rise. Example: 104 in.
3. Divide the total rise by 7. Round up. This is the number of risers.
4. Example: 104 ÷ 7 = 14.86. Use 15 risers.
5. Divide the total rise by the risers. This is each riser height: 104 ÷ 15 = 6.93 in.
6. A flight with N risers has N − 1 treads. With 15 risers, there are 14 treads.
7. Multiply the treads by 11 in. This is the run. Example: 14 × 11 = 154 in.
8. Double-click your staircase. Set its height to the total rise. Set its depth to the run or more.
9. Click Create dimensions. Draw one along the stairs. It must show the run.
10. Add a text label near the stairs: rise, risers, riser height, treads, run.
11. Plan a ramp for a step 18 in high. At 1:12, the run is 18 × 12 = 216 in.
12. Outside the front door, add a flat piece 36 in wide and 216 in long. Name it Ramp footprint.
13. Add a 60 in landing at each end of the ramp.
14. Click the Save home button.

You should see: labeled stair math, and a ramp footprint that is 18 ft long.

## Check your work
1. Is each riser 7 in or lower?
2. Is each tread 11 in or more?
3. Does the ramp run equal rise times 12?

## Make it yours
- Compute a ramp for a 6 in step. Does it need handrails?
- Compute stairs for a 120 in ceiling. How many risers?

## New words
- **riser** — the vertical part of a step.
- **tread** — the part of a step you stand on.
- **slope** — how steep a surface is. 1:12 rises 1 in over 12 in.

---
Source: 2010 ADA Standards for Accessible Design, U.S. Department of Justice. U.S. government work, public domain. Sweet Home 3D User's Guide, version 7.5 (sweethome3d.com), by Space Mushrooms. Sweet Home 3D is free software under the GNU GPL.
