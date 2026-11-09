"""Figures: activity diagram (plan wizard), state machine, sequence (plan creation),
document/ER model, navigation sitemap."""

import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

from diagram_lib import (BLUE, GREY, GREY_LIGHT, INK, ORANGE, TEAL, TEAL_DARK, TEAL_LIGHT,
                         arrow, box, canvas, note, save, poly_arrow)

OUT = "/home/user/macrova-bca/docs/output/assets"
BORDER_C = "#c9d6dd"


def wrap_note(ax, x, y, w, text, size=7.6, chars=None):
    import textwrap
    chars = chars or int(w * 100 / (size * 0.52))
    lines = []
    for para in text.split("\n"):
        lines.extend(textwrap.wrap(para, chars) or [""])
    h = 2.4 + len(lines) * (size * 0.30)
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.9",
                 linewidth=1.0, edgecolor="#f0c48a", facecolor="#fdf6ea", zorder=2))
    ax.text(x + 1.2, y + h / 2, "\n".join(lines), ha="left", va="center", fontsize=size,
            color="#7a4b12", linespacing=1.5, zorder=3)
    return h


def diamond(ax, cx, cy, w, h, text, size=7.4, accent=BLUE):
    ax.add_patch(Polygon([[cx, cy + h / 2], [cx + w / 2, cy], [cx, cy - h / 2], [cx - w / 2, cy]],
                 closed=True, facecolor="#f7fbfb", edgecolor=accent, lw=1.1, zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=size, color=INK, zorder=3)


def step(ax, x, y, w, h, text, accent=TEAL, size=8.0, fill="#ffffff"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.4",
                 facecolor=fill, edgecolor=BORDER_C, lw=1.1, zorder=2))
    ax.plot([x + 1.0, x + w - 1.0], [y + h, y + h], color=accent, lw=2.2, zorder=3,
            solid_capstyle="round")
    ax.text(x + w / 2, y + h / 2 - 0.3, text, ha="center", va="center", fontsize=size,
            color=INK, zorder=3, linespacing=1.5)


# ================================================================ ACTIVITY (wizard)
fig, ax = canvas(13.0, 11.0)
ax.text(50, 81.0, "UML activity diagram — diet plan creation wizard", ha="center",
        fontsize=13.0, fontweight="bold", color=INK)

ax.add_patch(mpatches.Circle((50, 76.0), 1.5, facecolor=INK, edgecolor=INK, zorder=3))
step(ax, 38.0, 69.5, 24.0, 4.8, "Open /diet-plan-form", accent=TEAL)
step(ax, 38.0, 62.0, 24.0, 5.6, "GET /diet-plan/form/status\nresolve PENDING or ACTIVE plan",
     accent=BLUE, size=7.6)
diamond(ax, 50.0, 53.5, 26.0, 9.0, "an ACTIVE plan\nalready exists?", accent=BLUE)

step(ax, 5.0, 40.0, 25.0, 6.6, "Step 1  Body Metrics\nclient-side range validation", accent=TEAL, size=7.6)
step(ax, 5.0, 30.5, 25.0, 6.6, "POST /form/body-metrics\nfindTDEE → tdee stored", accent=TEAL, size=7.6)
step(ax, 5.0, 21.0, 25.0, 6.6, "Step 2  Goal & Duration\nPOST /form/goal-selection", accent=TEAL, size=7.4)
step(ax, 37.5, 21.0, 25.0, 6.6, "findDeficit / findSurplus\ntarget kcal + macro presets", accent=ORANGE, size=7.4)
step(ax, 37.5, 30.5, 25.0, 6.6, "Step 3  Meal Preferences\nPOST /form/meal-preference", accent=TEAL, size=7.4)
step(ax, 37.5, 40.0, 25.0, 6.6, "client recomputes kcal\nprotein·4 + carbs·4 + fat·9", accent=ORANGE, size=7.4)
step(ax, 70.0, 40.0, 25.0, 6.6, "Step 4  Preview\nplan snapshot for review", accent=TEAL, size=7.4)
step(ax, 70.0, 30.5, 25.0, 6.6, "POST /form/create\nACTIVE · COMPLETED", accent=TEAL, size=7.4)
step(ax, 70.0, 21.0, 25.0, 6.6, "createDietPlanTrack\nday 1 track with meal split", accent=ORANGE, size=7.4)
ax.add_patch(mpatches.Circle((82.5, 15.0), 1.5, facecolor="#ffffff", edgecolor=INK, lw=1.2, zorder=3))
ax.add_patch(mpatches.Circle((82.5, 15.0), 0.85, facecolor=INK, edgecolor=INK, zorder=4))

arrow(ax, (50, 74.5), (50, 74.3))
arrow(ax, (50, 69.5), (50, 67.6))
arrow(ax, (50, 62.0), (50, 58.0))
arrow(ax, (37.0, 53.5), (17.5, 53.5), color=BLUE)
ax.text(26.0, 55.0, "[no]", fontsize=8.0, color=BLUE, ha="center")
arrow(ax, (17.5, 53.5), (17.5, 46.6), color=BLUE)
arrow(ax, (63.0, 53.5), (80.0, 53.5), color=GREY, ls="--")
ax.text(71.5, 55.0, "[yes] redirect /dashboard", fontsize=7.6, color=GREY, ha="center")
poly_arrow(ax, [(30.0, 43.3), (37.5, 43.3)], color=GREY, ls="--")
ax.text(33.7, 46.9, "", fontsize=7)
arrow(ax, (17.5, 40.0), (17.5, 37.1))
arrow(ax, (17.5, 30.5), (17.5, 27.6))
arrow(ax, (30.0, 24.3), (37.5, 24.3))
arrow(ax, (50.0, 27.6), (50.0, 30.5))
arrow(ax, (62.5, 33.8), (70.0, 33.8), color=GREY, ls="--")
ax.text(66.3, 35.2, "snapshot", fontsize=6.8, color=GREY, ha="center")
arrow(ax, (62.5, 43.3), (70.0, 43.3), color=GREY, ls="--")
arrow(ax, (82.5, 40.0), (82.5, 37.1))
arrow(ax, (82.5, 30.5), (82.5, 27.6))
arrow(ax, (82.5, 21.0), (82.5, 16.5))

ax.text(2.0, 37.5, "Back navigation", fontsize=8.2, fontweight="bold", color=INK)
ax.text(2.0, 34.6, "POST /form/status carrying an\nearlier FormStatus re-renders\nthe previous step from the\npersisted plan document",
        fontsize=7.0, color=GREY, va="top", linespacing=1.45)

wrap_note(ax, 2.0, 2.0, 96.0,
          "The wizard is resumable because every step persists formStatus on the pending DietPlan document, so a page reload returns the user to the step recorded "
          "in the database. Uniqueness of the pending plan is enforced by the findByUserIdAndPlanStatus query rather than by a database constraint. Range validation "
          "(age 18–65, height 140–210 cm, weight 40–180 kg, and target weight below or above the current weight depending on the chosen plan) runs in the browser, "
          "while the server recomputes TDEE and target calories so that tampered client values cannot alter the stored targets.",
          size=7.6, chars=150)
save(fig, f"{OUT}/activity-wizard.png")

# ================================================================ STATE MACHINE
fig, ax = canvas(13.0, 9.6)
ax.text(50, 67.0, "UML state machine diagram — lifecycle of a diet plan document",
        ha="center", fontsize=13.0, fontweight="bold", color=INK)


def state(x, y, w, h, name, sub, accent=TEAL, fill="#ffffff"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=2.0",
                 facecolor=fill, edgecolor=accent, lw=1.3, zorder=2))
    ax.text(x + w / 2, y + h - 2.6, name, ha="center", va="center", fontsize=9.0,
            fontweight="bold", color=INK, zorder=3)
    ax.text(x + w / 2, y + h - 6.2, sub, ha="center", va="center", fontsize=7.2, color=GREY,
            zorder=3, linespacing=1.5)


ax.add_patch(mpatches.Circle((3.4, 51.0), 1.5, facecolor=INK, zorder=3))
state(8.0, 44.0, 25.0, 14.5, "PENDING · BODY_METRICS", "plan created on the first submit\nformStatus persisted")
state(38.0, 44.0, 25.0, 14.5, "PENDING · GOAL_SELECTION", "tdee and target calories\nstored on the same document")
state(68.0, 44.0, 25.0, 14.5, "PENDING · MEAL_PREFERENCE", "macros, dietType,\nmealCount, eveningSnack")
state(68.0, 19.0, 25.0, 14.5, "PENDING · PREVIEW", "full snapshot available\nfor the review screen")
state(38.0, 19.0, 25.0, 14.5, "ACTIVE · COMPLETED", "planStatus ACTIVE\ncreatedAt and day-1 track", accent=TEAL_DARK)
state(8.0, 19.0, 25.0, 14.5, "INACTIVE · COMPLETED", "duration exceeded\nchecked on every load", accent=GREY)
ax.add_patch(mpatches.Circle((3.4, 26.2), 1.5, facecolor="#ffffff", edgecolor=INK, lw=1.2, zorder=3))
ax.add_patch(mpatches.Circle((3.4, 26.2), 0.85, facecolor=INK, zorder=4))

arrow(ax, (4.9, 51.0), (8.0, 51.0))
arrow(ax, (33.0, 51.0), (38.0, 51.0), label="POST body-metrics", label_dy=2.0, label_size=6.9)
arrow(ax, (63.0, 51.0), (68.0, 51.0), label="POST goal-selection", label_dy=2.0, label_size=6.9)
arrow(ax, (80.5, 44.0), (80.5, 33.5), label="POST\nmeal-preference", label_dx=9.6, label_dy=0.0,
      label_size=6.9)
arrow(ax, (68.0, 26.2), (63.0, 26.2), label="POST form/create", label_dy=2.0, label_size=6.9)
arrow(ax, (38.0, 26.2), (33.0, 26.2), label="dayCount > duration", label_dy=2.0, label_size=6.9)
arrow(ax, (8.0, 26.2), (4.9, 26.2))
arrow(ax, (20.5, 44.0), (50.5, 33.5), color=GREY, ls="--",
      label="back navigation (POST /form/status)", label_dx=-5.0, label_dy=-4.6, label_size=6.6,
      rad=-0.12)
ax.text(26.0, 39.0, "resume at stored step", fontsize=6.6, color=GREY, ha="center")

wrap_note(ax, 2.0, 1.0, 96.0,
          "The state machine is driven by two enumerations: FormStatus (BODY_METRICS → GOAL_SELECTION → MEAL_PREFERENCE → PREVIEW → COMPLETED) records wizard "
          "progress, while PlanStatus (PENDING → ACTIVE → INACTIVE) records the lifecycle of the plan itself. Transitions are performed by DietPlanFormService; the "
          "PENDING → INACTIVE shortcut is not reachable in practice, because only an ACTIVE plan is evaluated by isDietPlanReachedDuration().",
          size=7.6, chars=152)
save(fig, f"{OUT}/state-diagram.png")

# ================================================================ SEQUENCE
fig, ax = canvas(13.2, 9.6)
ax.text(50, 64.0, "UML sequence diagram — creating a plan and recording the first day",
        ha="center", fontsize=12.8, fontweight="bold", color=INK)

lanes = [("Browser\n(Angular)", 6.5), ("DietPlanForm\nComponent", 24.0), ("DietPlan\nService", 43.0),
         ("DietPlanForm\nController", 61.0), ("DietPlanForm\nService", 79.0), ("MongoDB\nrepositories", 94.0)]
for name, x in lanes:
    ax.add_patch(FancyBboxPatch((x - 6.8, 56.2), 13.6, 5.2, boxstyle="round,pad=0,rounding_size=0.8",
                 facecolor="#eef7f6", edgecolor=BORDER_C, lw=1.0, zorder=2))
    ax.text(x, 58.8, name, ha="center", va="center", fontsize=7.4, fontweight="bold", color=INK,
            zorder=3, linespacing=1.3)
    ax.plot([x, x], [12.5, 56.2], color=BORDER_C, lw=1.0, ls=(0, (4, 4)), zorder=1)


def msg(y, x1, x2, text, dashed=False, color=TEAL, size=6.9, dx=0.0):
    style = "-|>"
    ax.add_patch(FancyArrowPatch((x1, y), (x2, y), arrowstyle=style, mutation_scale=10,
                 color=color, lw=1.1, ls="--" if dashed else "-", zorder=3,
                 shrinkA=0, shrinkB=0))
    ax.text((x1 + x2) / 2 + dx, y + 0.75, text, ha="center", fontsize=size, color=GREY, zorder=4)


def self_msg(y, x, text, size=6.8):
    ax.add_patch(FancyArrowPatch((x, y), (x + 4.0, y - 1.6), arrowstyle="-", color=TEAL, lw=1.0,
                 connectionstyle="arc3,rad=-0.6", zorder=3))
    ax.add_patch(FancyArrowPatch((x + 4.0, y - 1.6), (x, y - 3.2), arrowstyle="-|>", color=TEAL,
                 lw=1.0, mutation_scale=9, connectionstyle="arc3,rad=-0.6", zorder=3))
    ax.text(x + 5.2, y - 1.6, text, fontsize=size, color=GREY, va="center", zorder=4)


msg(53.0, 6.5, 24.0, "submit body metrics")
msg(49.6, 24.0, 24.0, "", dashed=True)
ax.text(25.6, 48.4, "validateFieldRanges()", fontsize=6.8, color=GREY)
msg(46.0, 24.0, 43.0, "createDietPlanBodyMetrics()")
msg(42.4, 43.0, 61.0, "POST /diet-plan/form/body-metrics")
msg(39.0, 61.0, 79.0, "createDietPlanBodyMetrics(request)")
msg(35.4, 79.0, 94.0, "findByUserIdAndPlanStatus() / save()")
msg(31.8, 94.0, 79.0, "persisted DietPlan", dashed=True, color=GREY)
ax.text(43.0, 33.9, "tdee = round(findTDEE(age, weight, height, gender, activity))", fontsize=6.6, color=GREY, ha="center")
msg(28.2, 79.0, 61.0, "BodyMetricsResponse(tdee, weights)", dashed=True, color=GREY)
msg(24.6, 61.0, 24.0, "HTTP 200", dashed=True, color=GREY)
msg(21.0, 24.0, 79.0, "next steps reuse the same pending document (goal → preferences → preview)",
    color=BLUE, size=6.9)
msg(17.6, 24.0, 43.0, "createDietPlan()  →  POST /form/create")
msg(14.6, 43.0, 94.0, "save(ACTIVE plan) + createDietPlanTrack()")

wrap_note(ax, 2.0, 1.0, 96.0,
          "The lifelines correspond to real classes: DietPlanFormComponent and DietPlanService on the client, DietPlanFormController and DietPlanFormService "
          "on the server, and the two Spring Data repositories. Note that the client-side service in DietPlanService mixes the /diet-plan and /diet-plan/form "
          "paths, and that the controller delegates every step to the same stateless service, which resolves the acting user from UserSession instead of "
          "accepting a user identifier from the request body.",
          size=7.4, chars=150)
save(fig, f"{OUT}/sequence-plan.png")

# ================================================================ DOCUMENT / ER MODEL
fig, ax = canvas(13.4, 9.0)
ax.text(50, 61.0, "Document model of the MongoDB database macrova (collection-per-entity design)",
        ha="center", fontsize=12.6, fontweight="bold", color=INK)


def coll(x, y, w, name, fields, accent=TEAL, h=None):
    hh = 3.2
    rows = len(fields)
    h = h or hh + rows * 2.15 + 1.2
    ax.add_patch(FancyBboxPatch((x, y - h), w, h, boxstyle="round,pad=0,rounding_size=0.8",
                 facecolor="#ffffff", edgecolor=BORDER_C, lw=1.1, zorder=2))
    ax.add_patch(mpatches.Rectangle((x, y - hh), w, hh, facecolor=accent, alpha=0.17,
                 edgecolor="none", zorder=2.3))
    ax.text(x + w / 2, y - 1.6, name, ha="center", va="center", fontsize=8.8,
            fontweight="bold", color=INK, zorder=4)
    for i, f in enumerate(fields):
        ax.text(x + 1.0, y - hh - 1.7 - i * 2.15, f, ha="left", va="center", fontsize=7.0,
                color=GREY, zorder=4)
    return (x, y - h, w, h)


coll(2.0, 56.0, 28.0, "users", ["_id : ObjectId (String in Java)",
     "username : String", "email : String", "password : String (BCrypt hash)"], accent=TEAL)
coll(36.0, 56.0, 28.0, "diet_plans", ["_id : String", "userId : String  (→ users._id)",
     "title · plan · goal · age · gender", "height · weight · targetWeight · activity",
     "tdee · targetCalories · currentCalories", "dietType · mealType · mealCount",
     "macros { protein, carbs, fat }", "createdAt : LocalDate", "planStatus · formStatus"],
     accent=BLUE)
coll(70.0, 56.0, 28.0, "diet_plan_tracks", ["_id : String", "dietPlanId : String  (→ diet_plans._id)",
     "weight · tdee · dayCount", "createdAt : LocalDate", "intake { taken, total }",
     "protein / carbs / fat { taken, total }", "mealKcal { breakfast, lunch, snack,", "   dinner → macrosTrack }"],
     accent=BLUE)
coll(36.0, 34.0, 28.0, "ai_food_suggests", ["_id : String", "name : String",
     "calories { taken, total }", "macronutrients { protein, carbs, fat }", "description : String"],
     accent=ORANGE)

ax.annotate("", xy=(36.0, 44.0), xytext=(30.0, 44.0),
            arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.2))
ax.text(33.0, 45.4, "1 : N", fontsize=7.2, color=GREY, ha="center")
ax.plot([30.0, 33.0], [44.0, 44.0], color=GREY, lw=1.2)
ax.annotate("", xy=(30.0, 44.0), xytext=(30.0, 44.0), arrowprops=dict(arrowstyle="-"))
ax.plot([30.0, 30.0], [44.0, 40.0], color=GREY, lw=1.2)
ax.annotate("", xy=(30.0, 36.0), xytext=(30.0, 36.0), arrowprops=dict(arrowstyle="-"))
ax.text(20.0, 40.0, "no database-level foreign key;\nreferential integrity is enforced\nby repository queries",
        fontsize=6.8, color=GREY, ha="center", va="center")
ax.annotate("", xy=(70.0, 46.0), xytext=(64.0, 46.0),
            arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.2))
ax.text(67.0, 47.4, "1 : N", fontsize=7.2, color=GREY, ha="center")

wrap_note(ax, 2.0, 1.0, 96.0,
          "Macrova stores data in three collections plus an optional suggestion cache. Documents embed their value objects (macros, calories, meal split) instead "
          "of normalising them into separate tables, so a DietPlanTrack is one atomic document per day. Identifiers such as userId and dietPlanId are plain "
          "hexadecimal strings; the application, not the database, is responsible for referential integrity, which is why deletion of a user leaves plans orphaned "
          "(no cascade or delete endpoint exists in the current implementation).",
          size=7.6, chars=152)
save(fig, f"{OUT}/er-document-model.png")
