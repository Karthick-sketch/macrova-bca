"""Interface renderings of the Macrova single-page application.

Every screen is reconstructed from the corresponding Angular component
template and its scoped stylesheet so that the figures shown in the report
reflect the implemented layout, design tokens and wording.  Dimensions are
expressed in points on a 475-point wide canvas, which is the exact width of
the printed text block.
"""

from __future__ import annotations

import os

from reportlab.graphics.shapes import Circle, Image as GImage, Line, Polygon, Rect
from reportlab.lib import colors

from figlib import D, sw, wrap
from theme import SANS, SANS_B, MONO

BG = colors.HexColor("#f8fafb")
SURFACE = colors.white
BORDER = colors.HexColor("#e2e8e6")
PRIMARY = colors.HexColor("#1a9c8a")
PRIMARY_D = colors.HexColor("#13786b")
PRIMARY_L = colors.HexColor("#e6f7f5")
PRIMARY_M = colors.HexColor("#b2e4de")
TEXT = colors.HexColor("#1f2937")
MUTED = colors.HexColor("#6b7280")
LIGHT = colors.HexColor("#9ca3af")
INPUT = colors.HexColor("#f0f6f5")
DANGER = colors.HexColor("#dc2626")
DANGER_BG = colors.HexColor("#fee2e2")
WARN = colors.HexColor("#d97706")
WARN_BG = colors.HexColor("#fef3c7")
CHART = colors.HexColor("#4591df")

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(HERE, "..", "..", "frontend", "public")


# ---------------------------------------------------------------------------
# chrome
# ---------------------------------------------------------------------------
def window(h, url):
    d = D(475, h)
    d.rect(0, 0, 475, h, fill=BG, stroke=None)
    d.rect(0, 0, 475, 14, fill=colors.HexColor("#eceff0"), stroke=BORDER, lw=0.6)
    for i, col in enumerate(["#e0675c", "#e3b04b", "#63b56a"]):
        d.d.add(Circle(9 + i * 8, d.y(7), 2.4, fillColor=colors.HexColor(col),
                       strokeColor=colors.HexColor(col)))
    d.rrect(46, 3.4, 300, 7.4, r=3.7, fill=colors.white, stroke=BORDER, lw=0.5)
    d.text(52, 8.8, url, 4.5, SANS, MUTED)
    return d


def app_header(d, top, active=None, initial="K", auth=None):
    h = 19
    d.rect(0, top, 475, h, fill=SURFACE, stroke=BORDER, lw=0.6)
    d.d.add(Circle(12, d.y(top + 9.5), 3.4, fillColor=PRIMARY, strokeColor=PRIMARY))
    d.text(19, top + 12, "Macrova", 7.4, SANS_B, PRIMARY_D)
    if auth:
        bw = 34
        d.rrect(475 - bw - 10, top + 4.5, bw, 10, r=3, fill=PRIMARY_L, stroke=PRIMARY_M, lw=0.6)
        d.text(475 - bw / 2 - 10, top + 11.6, auth, 5.4, SANS_B, PRIMARY_D, "middle")
        return top + h
    items = ["dashboard", "progress", "meals", "history"]
    x = 175
    for it in items:
        w = sw(it, SANS_B if it == active else SANS, 5.4) + 10
        if it == active:
            d.rrect(x, top + 5, w, 9.5, r=3, fill=PRIMARY_L, stroke=None, lw=0)
            d.text(x + w / 2, top + 11.6, it, 5.4, SANS_B, PRIMARY_D, "middle")
        else:
            d.text(x + w / 2, top + 11.6, it, 5.4, SANS, MUTED, "middle")
        x += w + 4
    d.d.add(Circle(462, d.y(top + 9.5), 6.2, fillColor=PRIMARY, strokeColor=PRIMARY))
    d.text(462, top + 11.6, initial, 5.6, SANS_B, colors.white, "middle")
    return top + h


def page_title(d, x, top, title, sub=None):
    d.text(x, top + 8, title, 10.2, SANS_B, TEXT)
    if sub:
        d.text(x, top + 15.5, sub, 5.4, SANS, MUTED)
        return top + 20
    return top + 12


def card(d, x, top, w, h, label=None):
    d.rrect(x, top, w, h, r=5, fill=SURFACE, stroke=BORDER, lw=0.6)
    if label:
        d.text(x + 7, top + 8, label, 5.6, SANS_B, TEXT)


def inp(d, x, top, w, h=10.5, placeholder="", value=None, focus=False, label=None):
    if label:
        d.text(x, top + 4.4, label, 5.0, SANS, MUTED)
        top += 6
    d.rrect(x, top, w, h, r=3, fill=INPUT, stroke=BORDER, lw=0.5)
    txt = value if value is not None else placeholder
    d.text(x + 4, top + h / 2 + 1.9, txt, 5.2, SANS, TEXT if value else LIGHT)
    return top + h


def btn(d, x, top, w, h=11, label="", kind="primary"):
    if kind == "primary":
        fill, stroke, col = PRIMARY, PRIMARY, colors.white
    elif kind == "special":
        fill, stroke, col = PRIMARY_L, PRIMARY_M, PRIMARY_D
    else:
        fill, stroke, col = SURFACE, BORDER, MUTED
    d.rrect(x, top, w, h, r=3.4, fill=fill, stroke=stroke, lw=0.6)
    d.text(x + w / 2, top + h / 2 + 1.9, label, 5.3, SANS_B, col, "middle")
    return top + h


def chip(d, x, top, label, selected=False, h=10):
    w = sw(label, SANS_B, 5.2) + 12
    d.rrect(x, top, w, h, r=3, fill=PRIMARY if selected else SURFACE,
            stroke=PRIMARY if selected else BORDER, lw=0.6)
    d.text(x + w / 2, top + h / 2 + 1.8, label, 5.2,
           SANS_B if selected else SANS, colors.white if selected else MUTED, "middle")
    return w


def metric(d, x, top, w, h, label, value, unit="", accent=False):
    d.rrect(x, top, w, h, r=5, fill=SURFACE, stroke=BORDER, lw=0.6)
    if accent:
        d.rect(x, top, 2.4, h, fill=PRIMARY, stroke=None)
    d.text(x + 7, top + 8, label.upper(), 4.4, SANS_B, MUTED)
    d.text(x + 7, top + 18.4, value, 10.4, SANS_B, TEXT)
    if unit:
        d.text(x + 9 + sw(value, SANS_B, 10.4), top + 18.4, unit, 4.8, SANS, MUTED)


def bar(d, x, top, w, pct, h=4, fill=PRIMARY):
    d.rrect(x, top, w, h, r=h / 2, fill=INPUT, stroke=None, lw=0)
    d.rrect(x, top, max(3, w * min(pct, 100) / 100), h, r=h / 2, fill=fill, stroke=None, lw=0)


def toast(d, x, top, w, msg):
    h = 13
    d.rrect(x, top, w, h, r=4, fill=colors.white, stroke=DANGER, lw=0.7)
    d.d.add(Circle(x + 8, d.y(top + h / 2), 3.2, fillColor=DANGER_BG, strokeColor=DANGER,
                   strokeWidth=0.5))
    d.text(x + 8, top + h / 2 + 1.7, "\u00d7", 5.4, SANS_B, DANGER, "middle")
    d.text(x + 15, top + h / 2 + 1.8, msg, 5.2, SANS, TEXT)
    return top + h


def _chevron(d, x, top, size=5, color=MUTED):
    d.line(x, top, x + size * 0.6, top + size * 0.6, color, 0.8)
    d.line(x + size * 0.6, top + size * 0.6, x, top + size * 1.2, color, 0.8)


# ---------------------------------------------------------------------------
# 1. Login
# ---------------------------------------------------------------------------
def login():
    d = window(214, "localhost:4200/login")
    t = app_header(d, 14, auth="Sign Up")
    cw, ch = 196, 138
    cx = (475 - cw) / 2
    cy = 58
    d.rrect(cx, cy, cw, ch, r=6, fill=SURFACE, stroke=BORDER, lw=0.6)
    d.text(475 / 2, cy + 20, "Welcome back", 9.2, SANS_B, TEXT, "middle")
    d.text(475 / 2, cy + 29, "Log in to your Macrova account", 5.2, SANS, MUTED, "middle")
    inp(d, cx + 16, cy + 40, cw - 32, 12, "Username")
    inp(d, cx + 16, cy + 58, cw - 32, 12, "Password")
    btn(d, cx + 16, cy + 78, cw - 32, 13, "Log In")
    lead = "New to Macrova? "
    link = "Sign up here"
    total = sw(lead, SANS, 5.0) + sw(link, SANS_B, 5.0)
    lx = 475 / 2 - total / 2
    d.text(lx, cy + 110, lead, 5.0, SANS, MUTED)
    d.text(lx + sw(lead, SANS, 5.0), cy + 110, link, 5.0, SANS_B, PRIMARY)
    d.text(12, 200, "login.component.html  \u00b7  POST /authenticate \u2192 HttpOnly refresh cookie", 4.6, MONO, LIGHT)
    return d.outcome()


# ---------------------------------------------------------------------------
# 2. Sign up
# ---------------------------------------------------------------------------
def signup():
    d = window(224, "localhost:4200/signup")
    app_header(d, 14, auth="Log In")
    cw, ch = 196, 142
    cx = (475 - cw) / 2
    cy = 56
    d.rrect(cx, cy, cw, ch, r=6, fill=SURFACE, stroke=BORDER, lw=0.6)
    d.text(475 / 2, cy + 18, "Create account", 9.0, SANS_B, TEXT, "middle")
    d.text(475 / 2, cy + 27, "Start tracking your nutrition today", 5.2, SANS, MUTED, "middle")
    inp(d, cx + 16, cy + 38, cw - 32, 12, "Username")
    inp(d, cx + 16, cy + 55, cw - 32, 12, "Email")
    inp(d, cx + 16, cy + 72, cw - 32, 12, "Password")
    btn(d, cx + 16, cy + 92, cw - 32, 13, "Sign Up")
    d.text(475 / 2 - 8, cy + 122, "Already have an account?", 5.0, SANS, MUTED, "middle")
    d.text(475 / 2 + 44, cy + 122, "Log in here", 5.0, SANS_B, PRIMARY, "middle")
    toast(d, 120, 204, 236, "Password must be at least 8 characters long")
    return d.outcome()


# ---------------------------------------------------------------------------
# 3. Dashboard
# ---------------------------------------------------------------------------
def dashboard():
    d = window(272, "localhost:4200/dashboard")
    t = app_header(d, 14, active="dashboard", initial="K")
    page_title(d, 12, t + 6, "Lean Cut \u2014 Phase 2", None)

    # progress section
    d.rrect(12, 52, 451, 26, r=5, fill=SURFACE, stroke=BORDER, lw=0.6)
    d.text(18, 61, "Daily Goal", 5.2, SANS, MUTED)
    d.text(451, 61, "62%", 5.2, SANS_B, PRIMARY, "end")
    bar(d, 18, 66, 439, 62, 4)

    # metric rows
    labels = [("Streak", "12", " / 60 days", True), ("Current Weight", "74.2", " kg", False),
              ("Daily Calorie Intake", "1,850", " kcal", False)]
    x = 12
    for lab, val, unit, acc in labels:
        metric(d, x, 84, 145, 26, lab, val, unit, acc)
        x += 153
    labels2 = [("Protein", "138", " g"), ("Carbohydrates", "185", " g"), ("Fat", "62", " g")]
    x = 12
    for lab, val, unit in labels2:
        metric(d, x, 115, 145, 26, lab, val, unit)
        x += 153

    # weight chart card
    cy = 148
    d.rrect(12, cy, 451, 100, r=5, fill=SURFACE, stroke=BORDER, lw=0.6)
    d.text(19, cy + 11, "Weight Trend", 5.8, SANS_B, TEXT)
    plot_x, plot_y, plot_w, plot_h = 34, cy + 20, 420, 58
    for i in range(5):
        yy = plot_y + plot_h * i / 4
        d.line(plot_x, yy, plot_x + plot_w, yy, colors.HexColor("#eef2f2"), 0.5)
        val = 76.0 - i * 0.5
        d.text(plot_x - 3, yy + 1.6, f"{val:.1f}", 4.2, SANS, LIGHT, "end")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    pts = [75.6, 75.3, 75.0, 74.8, 74.6, 74.4, 74.2]
    lo, hi = 74.0, 76.0
    coords = []
    for i, (day, wt) in enumerate(zip(days, pts)):
        px = plot_x + 14 + i * ((plot_w - 24) / 6)
        py = plot_y + plot_h * (1 - (wt - lo) / (hi - lo))
        coords.append((px, py))
        d.text(px, plot_y + plot_h + 7, day, 4.2, SANS, MUTED, "middle")
    for i in range(len(coords) - 1):
        d.line(coords[i][0], coords[i][1], coords[i + 1][0], coords[i + 1][1], CHART, 1.1)
    for px, py in coords:
        d.d.add(Circle(px, d.y(py), 1.5, fillColor=colors.white, strokeColor=CHART,
                       strokeWidth=0.8))
    d.text(19, cy + 94, "Weight (\u00b10.5 kg drift accepted)  \u00b7  Chart.js line chart, seven-day window (Asia/Kolkata)",
           4.4, SANS, LIGHT)
    return d.outcome()


# ---------------------------------------------------------------------------
# 4. Daily macronutrient log
# ---------------------------------------------------------------------------
def progress():
    d = window(320, "localhost:4200/progress")
    t = app_header(d, 14, active="progress", initial="K")
    page_title(d, 12, t + 4, "Today's Macronutrients Log",
               "Track your macronutrient intake by meal for a balanced diet.")

    # daily summary
    sy = 48
    d.rrect(12, sy, 451, 58, r=5, fill=SURFACE, stroke=BORDER, lw=0.6)
    d.text(19, sy + 10, "Daily Summary", 5.8, SANS_B, TEXT)
    d.text(20, sy + 20, "Day", 4.4, SANS, MUTED)
    d.rrect(20, sy + 22, 34, 10, r=3, fill=INPUT, stroke=BORDER, lw=0.5)
    d.text(24, sy + 29, "12", 5.0, SANS, LIGHT)
    d.text(64, sy + 20, "Current Weight (kg)", 4.4, SANS, MUTED)
    d.rrect(64, sy + 22, 48, 10, r=3, fill=INPUT, stroke=BORDER, lw=0.5)
    d.text(68, sy + 29, "74.2", 5.0, SANS, TEXT)
    btn(d, 120, sy + 22, 52, 10, "Update Weight")
    d.text(19, sy + 42, "Calories", 4.6, SANS, MUTED)
    d.text(40, sy + 42, "1,148", 5.4, SANS_B, TEXT)
    d.text(60, sy + 42, "/ 1,850 kcal", 4.6, SANS, MUTED)
    bar(d, 19, sy + 47, 436, 62, 4)

    # intake card
    iy = 112
    d.rrect(12, iy, 451, 196, r=5, fill=SURFACE, stroke=BORDER, lw=0.6)
    d.text(19, iy + 10, "Intake", 5.8, SANS_B, TEXT)
    meals = [
        ("Breakfast", (32, 42, 18), (14, 26, 8)),
        ("Lunch", (48, 62, 22), (36, 58, 18)),
        ("Snack", (12, 10, 4), (10, 12, 3)),
        ("Dinner", (46, 71, 18), (38, 60, 16)),
    ]
    my = iy + 18
    for name, req, taken in meals:
        d.rrect(19, my, 437, 40, r=4, fill=colors.HexColor("#fbfdfd"), stroke=BORDER, lw=0.5)
        d.text(24, my + 10, name, 5.4, SANS_B, TEXT)
        cols = ["Proteins", "Carbohydrates", "Fat"]
        x = 24
        for i, (cname, unit) in enumerate(zip(cols, ["g", "g", "g"])):
            d.text(x, my + 19, cname, 4.5, SANS, MUTED)
            d.text(x + sw(cname, SANS, 4.5) + 3, my + 19, f"(Required {req[i]}g)", 4.2, SANS, LIGHT)
            d.rrect(x, my + 22, 118, 10, r=3, fill=INPUT, stroke=BORDER, lw=0.5)
            d.text(x + 4, my + 29, str(taken[i]), 4.9, SANS, TEXT)
            x += 128
        d.rrect(410, my + 23, 40, 9.5, r=3, fill=PRIMARY, stroke=PRIMARY, lw=0.5)
        d.text(430, my + 30, "Update", 4.6, SANS_B, colors.white, "middle")
        my += 44
    return d.outcome()


# ---------------------------------------------------------------------------
# 5. Diet plan form
# ---------------------------------------------------------------------------
def plan_form():
    d = window(292, "localhost:4200/diet-plan-form")
    t = app_header(d, 14, active="dashboard", initial="K")
    page_title(d, 12, t + 4, "Create Diet Plan")
    d.rrect(12, 52, 451, 224, r=5, fill=SURFACE, stroke=BORDER, lw=0.6)

    def field(x, y, w, label, value=None, ph=""):
        d.text(x, y + 4.4, label, 4.9, SANS, MUTED)
        d.text(x + sw(label, SANS, 4.9) + 2, y + 4.4, "*", 4.9, SANS_B, DANGER)
        inp(d, x, y + 6.5, w, 11, ph, value)

    field(20, 60, 200, "Title", "Lean Cut \u2014 Phase 2")
    # plan toggle
    d.text(238, 64.4, "Plan", 4.9, SANS, MUTED)
    d.text(238 + sw("Plan", SANS, 4.9) + 2, 64.4, "*", 4.9, SANS_B, DANGER)
    chip(d, 238, 66.5, "Weight Loss", True)
    chip(d, 238 + 52, 66.5, "Weight Gain", False)

    field(20, 88, 200, "Age (18\u201365 years)", "24")
    d.text(238, 92.4, "Gender", 4.9, SANS, MUTED)
    chip(d, 238, 94.5, "Male", True)
    chip(d, 238 + 30, 94.5, "Female", False)

    field(20, 116, 200, "Height (140\u2013210 cm)", "174")
    field(238, 116, 200, "Weight (40\u2013180 kg)", "76.5")

    d.text(20, 152.4, "Goal", 4.9, SANS, MUTED)
    chip(d, 20, 154.5, "Mild", True)
    chip(d, 20 + 28, 154.5, "Moderate", False)
    chip(d, 20 + 76, 154.5, "Aggressive", False)

    d.text(158, 152.4, "Activity Level", 4.9, SANS, MUTED)
    labels = ["Sedentary", "Light", "Moderate", "Hard", "Athlete"]
    x = 194
    for i, lab in enumerate(labels):
        x += chip(d, x, 154.5, lab, i == 2) + 3

    field(20, 176, 200, "Target Weight", "70")
    field(238, 176, 200, "Duration (days)", "60")

    d.line(20, 204, 455, 204, BORDER, 0.5)
    d.text(20, 214, "Required fields are validated twice: validateFields() in the component and validateDietPlan() in DietPlanService before persistence.",
           4.3, SANS, LIGHT)
    btn(d, 20, 220, 92, 12, "Create Diet Plan")
    d.text(120, 228, "TDEE preview is computed server-side (POST /diet-plan/tdee)", 4.3, SANS, LIGHT)
    toast(d, 120, 244, 340, "Target weight must be less than current weight")
    return d.outcome()


# ---------------------------------------------------------------------------
# 6. AI food suggestions
# ---------------------------------------------------------------------------
def meals():
    d = window(352, "localhost:4200/meals")
    t = app_header(d, 14, active="meals", initial="K")
    page_title(d, 12, t + 4, "AI Food Suggestions",
               "AI-powered food suggestions tailored by meal type, dietary preference, and global cuisine.")
    d.rrect(12, 56, 451, 62, r=5, fill=SURFACE, stroke=BORDER, lw=0.6)
    rows = [("Meal", ["Breakfast", "Lunch", "Snack", "Dinner"], 0),
            ("Diet", ["Vegetarian", "Non-vegetarian", "Low-carb"], 1),
            ("Cuisine", ["Indian", "Chinese", "Japanese", "Thai"], 2)]
    y = 64
    for lab, chips, sel in rows:
        d.text(20, y + 7, lab, 4.9, SANS, MUTED)
        x = 52
        for i, c in enumerate(chips):
            x += chip(d, x, y, c, i == sel) + 4
        y += 18
    btn(d, 20, 124, 74, 12, "Get Suggestions")

    foods = [
        ("1. Masala oats with vegetables",
         "Rolled oats tempered with mustard seeds, curry leaves and mixed vegetables; a fibre-rich start.",
         "~280", "9", "44", "7"),
        ("2. Moong dal chilla with mint chutney",
         "Protein-dense lentil pancakes served with a low-fat mint chutney.",
         "~310", "16", "38", "9"),
        ("3. Sprouted ragi porridge",
         "Finger-millet porridge with sprouted grains and skimmed milk.",
         "~265", "11", "46", "5"),
        ("4. Paneer and spinach poha",
         "Flattened rice with crumbled paneer, spinach and peanuts.",
         "~330", "15", "42", "10"),
    ]
    y = 144
    for name, desc, cal, p, c, f in foods:
        d.rrect(12, y, 451, 40, r=5, fill=SURFACE, stroke=BORDER, lw=0.6)
        d.text(20, y + 11, name, 5.6, SANS_B, TEXT)
        d.text(20, y + 20, desc[:92], 4.5, SANS, MUTED)
        x = 20
        for lab, val, unit in [("Calories", cal, ""), ("Protein", p, "g"), ("Carbs", c, "g"),
                               ("Fat", f, "g")]:
            d.text(x, y + 33, lab, 4.4, SANS, LIGHT)
            d.text(x + sw(lab, SANS, 4.4) + 3, y + 33, f"{val}{unit}", 4.7, SANS_B, PRIMARY_D)
            x += 108
        y += 45
    d.text(12, 344, "Each card is one element of the JSON array returned by the language model; the calorie budget comes from the meal split.",
           4.3, SANS, LIGHT)
    return d.outcome()


# ---------------------------------------------------------------------------
# 7. Plan history
# ---------------------------------------------------------------------------
def history():
    d = window(280, "localhost:4200/history")
    t = app_header(d, 14, active="history", initial="K")
    page_title(d, 12, t + 6, "Diet Plans History",
               "View your past diet plans and track your progress.")
    items = [
        ("Lean Cut \u2014 Phase 2", True, "Weight Loss \u00b7 76.5kg \u2192 70.0kg \u00b7 60 days"),
        ("Recomposition \u2014 Q2", False, "Weight Gain \u00b7 68.0kg \u2192 73.0kg \u00b7 90 days"),
        ("Monsoon Reset", False, "Weight Loss \u00b7 79.4kg \u2192 74.0kg \u00b7 120 days"),
    ]
    y = 66
    for title, active, meta in items:
        d.rrect(12, y, 451, 42, r=5, fill=SURFACE, stroke=BORDER, lw=0.6)
        d.text(20, y + 13, title, 6.2, SANS_B, TEXT)
        bw = sw("Active", SANS_B, 4.5) + 12
        d.rrect(20 + sw(title, SANS_B, 6.2) + 8, y + 6, bw, 9, r=4.5,
                fill=PRIMARY_L if active else colors.HexColor("#f1f3f3"),
                stroke=PRIMARY_M if active else BORDER, lw=0.5)
        d.text(20 + sw(title, SANS_B, 6.2) + 8 + bw / 2, y + 12.4, "Active" if active else "Inactive",
               4.5, SANS_B, PRIMARY_D if active else MUTED, "middle")
        d.text(20, y + 24, meta, 4.8, SANS, MUTED)
        d.d.add(Circle(443, d.y(y + 21), 9, fillColor=PRIMARY_L, stroke=PRIMARY_M,
                       strokeWidth=0.5))
        _chevron(d, 441, y + 18.5, 4.4, PRIMARY_D)
        y += 48
    d.rrect(12, 210, 451, 46, r=5, fill=colors.HexColor("#fbfdfd"), stroke=BORDER, lw=0.5,
            dash=(2, 2))
    d.text(237, 228, "Selecting a plan opens its archived day-by-day tracking entries", 4.8, SANS, MUTED,
           "middle")
    d.text(237, 238, "(/history/:id \u2192 /history/track/:id)", 4.8, MONO, LIGHT, "middle")
    d.text(20, 268, "Only plans that belong to the authenticated principal are returned by findDietPlansHistoryByUserId().",
           4.4, SANS, LIGHT)
    return d.outcome()


# ---------------------------------------------------------------------------
# 8. Archived tracking entries
# ---------------------------------------------------------------------------
def overview():
    d = window(260, "localhost:4200/history/64f1c9")
    t = app_header(d, 14, active="history", initial="K")
    page_title(d, 12, t + 6, "Past Tracking Entries",
               "View day-by-day progress from your completed diet plans.")
    entries = [
        ("12 March 2026", "Weight: 75.0kg \u00b7 Calories: 2 310kcal \u00b7 Deficit: 1 890kcal",
         "Protein: 142g \u00b7 Carbs: 189g \u00b7 Fat: 63g"),
        ("11 March 2026", "Weight: 75.2kg \u00b7 Calories: 2 304kcal \u00b7 Deficit: 1 812kcal",
         "Protein: 136g \u00b7 Carbs: 181g \u00b7 Fat: 60g"),
        ("10 March 2026", "Weight: 75.4kg \u00b7 Calories: 2 298kcal \u00b7 Deficit: 1 940kcal",
         "Protein: 145g \u00b7 Carbs: 176g \u00b7 Fat: 66g"),
    ]
    y = 66
    for date, meta1, meta2 in entries:
        d.rrect(12, y, 451, 44, r=5, fill=SURFACE, stroke=BORDER, lw=0.6)
        d.text(20, y + 13, date, 5.8, SANS_B, TEXT)
        d.text(20, y + 24, meta1, 4.7, SANS, MUTED)
        d.text(20, y + 33, meta2, 4.7, SANS, MUTED)
        d.d.add(Circle(443, d.y(y + 22), 9, fillColor=PRIMARY_L, stroke=PRIMARY_M, strokeWidth=0.5))
        _chevron(d, 441, y + 19.5, 4.4, PRIMARY_D)
        y += 50
    d.text(12, 238, "One row per DietPlanTrack document. The archive view is read-only; the same DTO also feeds the dashboard chart.",
           4.4, SANS, LIGHT)
    return d.outcome()


# ---------------------------------------------------------------------------
# 9. Read-only archived log
# ---------------------------------------------------------------------------
def track_detail():
    d = window(290, "localhost:4200/history/track/64f1cf")
    t = app_header(d, 14, active="history", initial="K")
    page_title(d, 12, t + 4, "12 March 2026's Log", "Macronutrient intake by meal for this day.")
    sy = 54
    d.rrect(12, sy, 451, 50, r=5, fill=SURFACE, stroke=BORDER, lw=0.6)
    d.text(19, sy + 10, "Daily Summary", 5.8, SANS_B, TEXT)
    d.text(20, sy + 20, "Current Weight (kg)", 4.4, SANS, MUTED)
    d.rrect(20, sy + 22, 48, 10, r=3, fill=INPUT, stroke=BORDER, lw=0.5)
    d.text(24, sy + 29, "75.0", 5.0, SANS, TEXT)
    d.text(76, sy + 30, "Calories", 4.6, SANS, MUTED)
    d.text(96, sy + 30, "1 890", 5.2, SANS_B, TEXT)
    d.text(115, sy + 30, "/ 2 310 kcal", 4.6, SANS, MUTED)
    bar(d, 20, sy + 38, 435, 82, 4)
    iy = 112
    d.rrect(12, iy, 451, 160, r=5, fill=SURFACE, stroke=BORDER, lw=0.6)
    d.text(19, iy + 10, "Intake", 5.8, SANS_B, TEXT)
    meals = [("Breakfast", (48, 64, 21)), ("Lunch", (52, 66, 22)), ("Snack", (18, 22, 8)),
             ("Dinner", (24, 37, 12))]
    my = iy + 18
    for name, vals in meals:
        d.rrect(19, my, 437, 30, r=4, fill=colors.HexColor("#fbfdfd"), stroke=BORDER, lw=0.5)
        d.text(24, my + 10, name, 5.2, SANS_B, TEXT)
        x = 24
        for i, cname in enumerate(["Proteins", "Carbohydrates", "Fat"]):
            d.text(x, my + 20, cname, 4.4, SANS, MUTED)
            d.text(x + sw(cname, SANS, 4.4) + 3, my + 20, f"(Required {vals[i]}g)", 4.1, SANS, LIGHT)
            d.rrect(x, my + 22, 118, 6, r=2, fill=INPUT, stroke=BORDER, lw=0.4)
            d.text(x + 3, my + 26.8, str(vals[i]), 4.4, SANS, LIGHT)
            x += 128
        my += 34
    d.text(20, 280, "Archived entries are immutable: no update or delete endpoint is exposed for historical track documents.",
           4.4, SANS, LIGHT)
    return d.outcome()


# ---------------------------------------------------------------------------
# 10. No active plan
# ---------------------------------------------------------------------------
def no_plan():
    d = window(268, "localhost:4200/no-active-plan")
    app_header(d, 14, active="dashboard", initial="K")
    img_path = os.path.join(PUBLIC, "no-diet-plan.png")
    if os.path.exists(img_path):
        d.d.add(GImage(207, d.y(96), 60, 34, img_path))
    d.text(237, 116, "No Active Diet Plan", 8.6, SANS_B, TEXT, "middle")
    d.text(237, 126, "You don't have an active diet plan.", 5.0, SANS, MUTED, "middle")
    d.text(237, 134,
           "Continue with a past plan or create one to start tracking your meals and progress.",
           5.0, SANS, MUTED, "middle")
    cy = 146
    d.rrect(137, cy, 200, 62, r=5, fill=SURFACE, stroke=BORDER, lw=0.6)
    d.text(237, cy + 12, "Recomposition \u2014 Q2", 6.2, SANS_B, TEXT, "middle")
    d.text(237, cy + 22, "Weight Gain \u00b7 68.0kg \u2192 73.0kg \u00b7 90 days", 4.8, SANS, MUTED, "middle")
    d.text(237, cy + 34, "Would you like to continue with this plan?", 4.8, SANS, MUTED, "middle")
    btn(d, 148, cy + 42, 84, 12, "Continue this plan")
    btn(d, 240, cy + 42, 84, 12, "Create new plan", "special")
    d.text(12, 254, "Shown when /diet-plan/status reports an expired plan or /diet-plan returns 404.",
           4.4, SANS, LIGHT)
    return d.outcome()


# ---------------------------------------------------------------------------
# 11. 404
# ---------------------------------------------------------------------------
def not_found():
    d = window(216, "localhost:4200/not-found")
    app_header(d, 14, active="dashboard", initial="K")
    d.text(237, 90, "404", 30, SANS_B, PRIMARY_L, "middle")
    d.text(237, 108, "Page not found", 9.4, SANS_B, TEXT, "middle")
    d.text(237, 118, "The page you're looking for doesn't exist or has been moved.", 5.2, SANS,
           MUTED, "middle")
    btn(d, 200, 128, 74, 13, "Back to Dashboard")
    d.text(12, 202, "Wildcard route  /**  \u2192  PageNotFoundComponent", 4.4, MONO, LIGHT)
    return d.outcome()


# ---------------------------------------------------------------------------
# 12. Header dropdown + error toast
# ---------------------------------------------------------------------------
def dropdown():
    d = window(250, "localhost:4200/dashboard")
    t = app_header(d, 14, active="dashboard", initial="K")
    d.rrect(390, 34, 74, 34, r=4, fill=SURFACE, stroke=BORDER, lw=0.6)
    d.text(398, 44, "Edit profile", 4.8, SANS, TEXT)
    d.line(390, 49, 464, 49, BORDER, 0.5)
    d.text(398, 60, "Sign Out", 4.8, SANS_B, DANGER)
    toast(d, 108, 76, 260, "Invalid username or password!")
    d.text(12, 100, "HeaderComponent renders the nav items (dashboard, progress, meals, history) from a single", 4.5, SANS, LIGHT)
    d.text(12, 107, "string array and toggles a click-outside-aware profile menu; the toast lives for five seconds.", 4.5, SANS, LIGHT)
    d.rrect(12, 120, 451, 118, r=5, fill=SURFACE, stroke=BORDER, lw=0.6)
    d.text(20, 132, "Session state", 5.8, SANS_B, TEXT)
    lines = [
        ("AuthService.username", "angular signal \u2014 drives the avatar initial"),
        ("Access token", "in-memory only, never written to localStorage"),
        ("Refresh cookie", "Refresh-Token, HttpOnly, SameSite=Lax, 24 h"),
        ("Guard", "AuthGuard \u2192 isAuthenticated() \u2192 /user/refresh"),
    ]
    y = 144
    for a, b in lines:
        d.text(20, y, a, 4.8, SANS_B, PRIMARY_D)
        d.text(20 + sw(a, SANS_B, 4.8) + 8, y, b, 4.8, SANS, MUTED)
        y += 11
    d.text(12, 246, "signOut() calls POST /user/logout (cookie max-age 0) and clears the signal before navigating to /login.",
           4.4, SANS, LIGHT)
    return d.outcome()
