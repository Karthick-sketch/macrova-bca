"""Figures: use case, class, document (ER), activity, state machine, sequence."""

import textwrap

import matplotlib.patches as mpatches

from diagram_lib import (BLUE, BLUE_LIGHT, GREY, GREY_LIGHT, INK, ORANGE, ORANGE_LIGHT,
                         TEAL, TEAL_DARK, TEAL_LIGHT, arrow, box, canvas, ellipse, note,
                         poly_arrow, save)

OUT = "/home/user/macrova-bca/docs/output/assets"
BORDER_C = "#c9d6dd"


def wrap_note(ax, x, y, w, text, size=7.6, accent=ORANGE, chars=None):
    chars = chars or int(w * 100 / (size * 0.52))
    lines = []
    for para in text.split("\n"):
        lines.extend(textwrap.wrap(para, chars) or [""])
    h = 2.6 + len(lines) * (size * 0.30)
    ax.add_patch(mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.9",
                 linewidth=1.0, edgecolor="#f0c48a", facecolor="#fdf6ea", zorder=2))
    ax.text(x + 1.2, y + h / 2, "\n".join(lines), ha="left", va="center", fontsize=size,
            color="#7a4b12", linespacing=1.5, zorder=3)
    return h


# ================================================================ USE CASE
fig, ax = canvas(13.6, 9.6)
ax.text(50, 66.0, "UML use case diagram — Macrova platform", ha="center", fontsize=13.2,
        fontweight="bold", color=INK)
ax.text(50, 63.4, "Angular 19 single-page client together with the Spring Boot REST API",
        ha="center", fontsize=9.6, color=GREY)

ax.add_patch(mpatches.FancyBboxPatch((21.0, 15.0), 76.0, 46.0, boxstyle="round,pad=0,rounding_size=1.2",
             facecolor="#ffffff", edgecolor=BORDER_C, lw=1.3, zorder=1))
ax.text(59.0, 58.6, "Macrova system boundary", ha="center", fontsize=9.0, style="italic",
        color=GREY, zorder=3)

ellipse(ax, 9.5, 37.0, 14.0, 12.0, "USER", ["registered", "account holder"])
ax.plot([14.0, 14.0], [31.8, 42.2], color=GREY, lw=1.1, zorder=1)
ax.plot([14.0, 21.0], [37.0, 37.0], color=GREY, lw=1.1, zorder=1)

rows = [
    [("UC-01", "Register an account"), ("UC-02", "Log in and obtain JWT"), ("UC-03", "Refresh or end session")],
    [("UC-04", "Enter body metrics"), ("UC-05", "Detect TDEE & target kcal"), ("UC-06", "Select goal & duration")],
    [("UC-07", "Configure macro split"), ("UC-08", "Preview and activate plan"), ("UC-09", "View dashboard metrics")],
    [("UC-10", "Log per-meal intake"), ("UC-11", "Update body weight"), ("UC-12", "Browse plan history")],
    [("UC-13", "Review stored day entries"), ("UC-14", "Request AI food suggestions"), ("UC-15", "Recover from unknown route")],
]
cols = [33.0, 59.0, 85.0]
for r, row in enumerate(rows):
    cy = 52.0 - r * 8.0
    for c, (uid, name) in enumerate(row):
        cx = cols[c]
        ax.add_patch(mpatches.Ellipse((cx, cy), 22.5, 6.4, facecolor="#f7fbfb",
                     edgecolor=BORDER_C, lw=1.0, zorder=2))
        ax.text(cx, cy + 1.0, uid, ha="center", fontsize=6.6, color=TEAL, zorder=4)
        ax.text(cx, cy - 1.4, name, ha="center", fontsize=7.4, color=INK, zorder=4)
        ax.plot([21.0, cx - 11.2], [37.0, cy], color=GREY, lw=0.6, alpha=0.5, zorder=1)

# include / extend notation between neighbouring use cases
arrow(ax, (44.2, 45.6), (46.6, 42.6), color=TEAL, lw=0.9, style="-|>")
ax.text(43.6, 47.2, "«include»", fontsize=6.2, color=TEAL, ha="center")
arrow(ax, (66.0, 45.6), (66.0, 42.6), color=TEAL, lw=0.9, style="-|>")
ax.text(67.6, 47.2, "«include»", fontsize=6.2, color=TEAL, ha="center")
arrow(ax, (70.2, 37.0), (73.0, 37.0), color=TEAL, lw=0.9, style="-|>")
ax.text(71.6, 38.6, "«include»", fontsize=6.2, color=TEAL, ha="center")
arrow(ax, (44.2, 28.2), (46.6, 30.0), color=ORANGE, lw=0.9, style="-|>")
ax.text(44.0, 26.6, "«extend»", fontsize=6.2, color=ORANGE, ha="center")

wrap_note(ax, 21.0, 0.6, 76.0,
          "Mapping of use cases onto implementation artefacts — every ellipse corresponds to a route, an HTTP endpoint or a service operation present in the codebase.\n"
          "UC-01 POST /user/register and SignupComponent  ·  UC-02 POST /authenticate handled by AuthenticationFilter and CustomAuthenticationManager  ·  "
          "UC-03 POST /user/refresh and POST /user/logout  ·  UC-04 to UC-08 the four wizard steps of DietPlanFormController backed by DietPlanFormService.\n"
          "UC-09 GET /diet-plan/metrics  ·  UC-10 POST /diet-plan/{category}/{dietPlanId}  ·  UC-11 POST /diet-plan/add-weight/{dietPlanId}  ·  "
          "UC-12 GET /diet-plan/history  ·  UC-13 GET /diet-plan/overview/{id} and /diet-plan/track/{id}  ·  UC-14 POST /ai-food-suggest  ·  "
          "UC-15 the '**' wildcard route rendering PageNotFoundComponent.",
          size=7.2, chars=150)
save(fig, f"{OUT}/usecase-diagram.png")

# ================================================================ CLASS DIAGRAM
fig, ax = canvas(14.0, 11.4)
ax.text(50, 82.6, "UML class diagram — domain entities and value objects", ha="center",
        fontsize=13.0, fontweight="bold", color=INK)
ax.text(50, 80.2, "package org.karthick.macrova  ·  fields as declared in the Java sources",
        ha="center", fontsize=9.4, color=GREY)


def class_box(x, ytop, w, title, attrs, accent=TEAL, stereotype=None):
    hh = 3.4
    ah = 2.15 * len(attrs) + 1.4
    h = hh + ah
    ax.add_patch(mpatches.FancyBboxPatch((x, ytop - h), w, h, boxstyle="round,pad=0,rounding_size=0.7",
                 facecolor="#ffffff", edgecolor=BORDER_C, lw=1.1, zorder=2))
    ax.add_patch(mpatches.Rectangle((x, ytop - hh), w, hh, facecolor=accent, alpha=0.16,
                 edgecolor="none", zorder=2.2))
    ax.plot([x, x + w], [ytop - hh, ytop - hh], color=BORDER_C, lw=1.0, zorder=2.4)
    ax.text(x + w / 2, ytop - 1.15, stereotype, ha="center", va="center", fontsize=7.0,
            style="italic", color=GREY, zorder=4)
    ax.text(x + w / 2, ytop - 2.75, title, ha="center", va="center", fontsize=9.0,
            fontweight="bold", color=INK, zorder=4)
    for i, a in enumerate(attrs):
        ax.text(x + 1.1, ytop - hh - 1.7 - i * 2.15, a, ha="left", va="center", fontsize=7.3,
                color=GREY, zorder=4)
    return ytop - h


COLX = (2.0, 36.5, 71.0)
BOXW = 27.0


def place(col, top, gap, title, attrs, accent=TEAL, stereotype=None):
    x = COLX[col]
    return class_box(x, top, BOXW, title, attrs, accent=accent, stereotype=stereotype)


# ---- column 1: user identity and macro presets
c_user = place(0, 78.0, 0, "User", ["- String id", "- String username",
             "- String email", "- String password"], accent=TEAL, stereotype="«document: users»")
c_pref = place(0, 61.5, 0, "MacrosPreference", ["- Macros balanced", "- Macros highProtein",
             "- Macros lowCarb", "- Macros lowFat"], accent=TEAL, stereotype="«transient DTO»")
c_macros = place(0, 45.0, 0, "Macros", ["- double protein", "- double carbs", "- double fat"],
                 accent=TEAL, stereotype="«embedded value object»")
c_qty = place(0, 30.5, 0, "MacrosQuantity", ["- double min  ·  double max"], accent=TEAL,
              stereotype="«value object»")
c_meals = place(0, 23.0, 0, "Meals", ["- List<String> breakfast · lunch",
              "- List<String> snack · dinner"], accent=GREY, stereotype="«declared, not referenced»")

# ---- column 2: plan header and calorie values
c_plan = place(1, 78.0, 0, "DietPlan", ["- String id · title · userId",
             "- Plan plan · Goal goal", "- int age · duration · mealCount",
             "- Gender · Activity · DietType · MealType", "- double height · weight · todayWeight",
             "- double targetWeight · tdee", "- double targetCalories · currentCalories",
             "- Macros macros · boolean eveningSnack", "- LocalDate createdAt",
             "- PlanStatus · FormStatus"], accent=BLUE, stereotype="«document: diet_plans»")
c_cal = place(1, 47.0, 0, "Calories", ["- double taken", "- double total"], accent=TEAL,
              stereotype="«embedded value object»")
c_mt = place(1, 34.5, 0, "MacrosTrack", ["- Calories protein", "- Calories fat", "- Calories carbs"],
             accent=ORANGE, stereotype="«embedded value object»")
c_enum = place(1, 25.0, 0, "Enumerations", ["Plan · Gender · Goal · Activity", "DietType · MealType",
              "FormStatus · PlanStatus"], accent=GREY, stereotype="«enumeration»")

# ---- column 3: tracking and AI suggestions
c_track = place(2, 78.0, 0, "DietPlanTrack", ["- String id · dietPlanId",
               "- double weight · tdee", "- Calories intake · protein", "- Calories carbs · fat",
               "- MealKcal mealKcal", "- int dayCount", "- LocalDate createdAt"],
               accent=BLUE, stereotype="«document: diet_plan_tracks»")
c_meal = place(2, 56.0, 0, "MealKcal", ["- MacrosTrack breakfast", "- MacrosTrack lunch",
              "- MacrosTrack snack", "- MacrosTrack dinner"], accent=ORANGE,
              stereotype="«embedded value object»")
c_ai = place(2, 42.0, 0, "AIFoodSuggest", ["- String id · name", "- Calories calories",
             "- Macros macronutrients", "- String description"], accent=ORANGE,
             stereotype="«document: ai_food_suggests»")
c_calc = place(2, 27.0, 0, "NutrientsCalculator", ["+ findBMR(…) · findBMI(…)",
              "+ findTDEE(…) · findDeficit(…)", "+ findSurplus(…) · findProtein/Carbs/Fat(…)",
              "+ macrosPercentage(…) · roundCalories(…)"], accent=TEAL_DARK,
              stereotype="«utility, static»")


def link(p1, p2, label=None, lx=None, ly=None, ls="-", color=GREY, lw=1.1, rot=0):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=lw, ls=ls, zorder=1.4)
    if label:
        ax.text(lx, ly, label, fontsize=6.9, color=GREY, ha="center", va="center", rotation=rot,
                bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="none"), zorder=3)


link((29.0, 71.0), (36.5, 71.0), "owns  1 .. *", 32.7, 72.2)
link((63.5, 71.0), (71.0, 71.0), "tracks  1 .. *", 67.2, 72.2)
link((36.5, 55.2), (29.0, 50.6), "macros  1", 32.4, 53.2, ls="--", color=TEAL)
link((36.5, 45.0), (29.0, 40.0), "taken / total", 31.6, 43.6, ls="--", color=TEAL)
link((29.0, 54.6), (29.0, 58.2), color=TEAL)
link((27.0, 35.8), (36.5, 30.6), "min / max band", 33.0, 32.4, ls="--", color=TEAL)
link((84.5, 56.0), (84.5, 63.3), "4 x MacrosTrack", 89.0, 59.6, ls="--", color=ORANGE)
link((63.5, 50.0), (71.0, 50.0), "mealKcal  1", 67.2, 51.2, ls="--", color=ORANGE)
link((36.5, 35.4), (43.5, 41.0), "4 x Calories", 48.0, 38.6, ls="--", color=TEAL)
link((50.0, 25.0), (50.0, 21.4), "", ls="--", color=GREY)
ax.text(54.0, 23.2, "target band", fontsize=6.9, color=GREY, ha="center")
wrap_note(ax, 2.0, 1.0, 96.0,
          "Notation — solid lines are reference relationships resolved in application code: DietPlan stores userId as a plain string and DietPlanTrack stores "
          "dietPlanId, both resolved by repository query methods rather than by database foreign keys. Dashed lines mark embedded value objects persisted inside "
          "the parent document. Accessors, builders and constructors generated by Lombok are omitted; only the fields declared in each class are listed, together "
          "with the enumerations that the entities reference. The Meals class exists in the source tree but is not referenced by any entity or service.",
          size=7.6, chars=158)
save(fig, f"{OUT}/class-diagram.png")
