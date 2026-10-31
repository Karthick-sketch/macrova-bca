"""UML and database figures: use case, class, sequence, activity, state, ER."""

from __future__ import annotations

from reportlab.graphics.shapes import Circle, Polygon
from reportlab.lib import colors

from figlib import (AMBER, AMBER_PALE, BLUE, BLUE_PALE, D, GREEN, GREEN_PALE,
                    GREY, GREY_PALE, ROSE, ROSE_PALE, WHITE, sw, wrap)
from theme import (INK, INK_SOFT, MUTED, SANS, SANS_B, TEAL, TEAL_DARK,
                   TEAL_MID, TEAL_PALE)


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
def _diamond_marker(d, x, top, size=4.0, fill=TEAL_DARK):
    y = d.y(top)
    d.d.add(Polygon([x, y + size, x + size * 0.7, y, x, y - size, x - size * 0.7, y],
                    fillColor=fill, strokeColor=fill))


def _uml_class(d, x, top, w, title, attrs, ops=None, stereotype=None,
               fill=colors.HexColor("#fbfdfd"), header=TEAL_DARK, size=6.3):
    head_h = 26 if stereotype else 16
    attr_h = len(attrs) * 8.3 + 9
    ops_h = (len(ops) * 8.3 + 10) if ops else 0
    h = head_h + attr_h + ops_h
    d.rrect(x, top, w, h, r=2, fill=fill, stroke=TEAL_DARK, lw=0.8)
    d.rect(x, top, w, head_h, fill=header, stroke=header, lw=0.8)
    if stereotype:
        d.text(x + w / 2, top + 10, stereotype, 5.5, SANS, colors.white, "middle")
        d.text(x + w / 2, top + 20.5, title, 7.0, SANS_B, colors.white, "middle")
    else:
        d.text(x + w / 2, top + 11, title, 7.0, SANS_B, colors.white, "middle")
    y = top + head_h + 9
    for a in attrs:
        d.text(x + 5, y, a, size, SANS, INK_SOFT)
        y += 8.3
    if ops:
        d.line(x, top + head_h + attr_h - 2, x + w, top + head_h + attr_h - 2, TEAL_DARK, 0.6)
        y = top + head_h + attr_h + 6
        for o in ops:
            d.text(x + 5, y, o, size, SANS, INK_SOFT)
            y += 8.3
    return h


def _entity(d, x, top, w, name, rows, fill=BLUE_PALE, header=BLUE, size=6.4):
    head_h = 15
    h = head_h + len(rows) * 8.6 + 6
    d.rect(x, top, w, h, fill=WHITE, stroke=header, lw=0.8)
    d.rect(x, top, w, head_h, fill=header, stroke=header, lw=0.8)
    d.text(x + w / 2, top + 10.5, name, 7.0, SANS_B, colors.white, "middle")
    y = top + head_h + 9.5
    for r in rows:
        key = r.startswith("PK") or r.startswith("FK")
        d.text(x + 4, y, r, size, SANS_B if key else SANS,
               TEAL_DARK if key else INK_SOFT)
        y += 8.6
    return h


def _diamond(d, cx, top, w, h, label, fill=AMBER_PALE, stroke=AMBER, size=6.1):
    y = d.y(top + h / 2)
    d.d.add(Polygon([cx, y + h / 2, cx + w / 2, y, cx, y - h / 2, cx - w / 2, y],
                    fillColor=fill, strokeColor=stroke, strokeWidth=0.9))
    lines = wrap(label, SANS, size, w * 0.62)
    start = top + h / 2 - (len(lines) - 1) * 3.8 + 1.9
    for i, ln in enumerate(lines):
        d.text(cx, start + i * 7.6, ln, size, SANS, INK, "middle")


# ---------------------------------------------------------------------------
# Figure 4.7  Use case diagram
# ---------------------------------------------------------------------------
def usecase():
    d = D(475, 392)
    d.rrect(124, 12, 232, 352, r=6, fill=colors.HexColor("#fcfefe"), stroke=TEAL, lw=1.0)
    d.text(240, 26, "Macrova \u2014 diet & nutrition platform", 7.0, SANS_B, TEAL_DARK, "middle")

    items = [
        ("Register account", 44), ("Log in", 82), ("Maintain session (refresh / sign out)", 120),
        ("Create or update diet plan", 158), ("Log daily meal macros", 196),
        ("Update body weight", 234), ("Review dashboard, plans & history", 272),
        ("Request AI food suggestions", 310),
    ]
    for label, top in items:
        d.oval(134, top, 212, 26, label, fill=TEAL_PALE, stroke=TEAL, tsize=6.8)

    d.actor(46, 44, "Visitor")
    d.actor(46, 214, "Registered user")
    d.text(46, 76, "\u00abactor\u00bb", 5.6, SANS, MUTED, "middle")
    d.arrow(46, 268, 46, 122, head=4.5, dash=(2, 2), color=MUTED)
    d.text(50, 186, "generalisation", 5.4, SANS, MUTED)

    for top in (57, 95):
        d.line(56, 58, 134, top, TEAL_DARK, 0.7)
    for top in (133, 171, 209, 247, 285):
        d.line(56, 250, 134, top, TEAL_DARK, 0.7)

    d.actor(432, 300, "OpenRouter LLM")
    d.text(432, 340, "secondary actor", 5.6, SANS, MUTED, "middle")
    d.line(420, 312, 346, 323, AMBER, 0.8)

    d.text(6, 376, "The visitor may only register or authenticate; every other use case requires an authenticated principal resolved "
                   "from the access token.", 5.8, SANS, MUTED)
    return d.outcome()


# ---------------------------------------------------------------------------
# Figure 4.8  Domain class diagram
# ---------------------------------------------------------------------------
def class_diagram():
    d = D(610, 432)
    _uml_class(d, 4, 16, 172, "User", [
        "- id : String  \u00abObjectId\u00bb",
        "- username : String",
        "- email : String",
        "- password : String  \u00abBCrypt\u00bb",
    ], ["+ toUserDTO() : UserDTO"], stereotype="\u00abdocument: users\u00bb")

    _uml_class(d, 196, 16, 198, "DietPlan", [
        "- id : String",
        "- title : String",
        "- plan : Plan",
        "- age : int",
        "- gender : Gender",
        "- height : double   \u00abcm\u00bb",
        "- weight : double   \u00abkg\u00bb",
        "- todayWeight : double",
        "- goal : Goal",
        "- targetWeight : double",
        "- duration : int    \u00abdays\u00bb",
        "- activity : Activity",
        "- userId : String   \u00abFK users\u00bb",
        "- active : boolean = true",
        "- createdAt : LocalDate",
    ], ["+ DietPlan()"], stereotype="\u00abdocument: diet_plans\u00bb")

    track_top = 246
    _uml_class(d, 196, track_top, 198, "DietPlanTrack", [
        "- id : String",
        "- weight : double",
        "- tdee : double",
        "- intake : Calories",
        "- protein : Calories",
        "- carbs : Calories",
        "- fat : Calories",
        "- mealKcal : MealKcal",
        "- dayCount : int",
        "- createdAt : LocalDate",
        "- dietPlanId : String \u00abFK\u00bb",
    ], ["+ DietPlanTrack(w, date, day, id)"],
        stereotype="\u00abdocument: diet_plan_tracks\u00bb")

    h_cal = _uml_class(d, 416, 16, 190, "Calories", ["- taken : double", "- total : double"],
                       ["+ Calories(total)"], fill=GREY_PALE, header=GREY)
    mac_top = 16 + h_cal + 14
    h_mac = _uml_class(d, 416, mac_top, 190, "Macros",
                       ["- protein : Calories", "- fat : Calories", "- carbs : Calories"],
                       fill=GREY_PALE, header=GREY)
    meal_top = mac_top + h_mac + 14
    h_meal = _uml_class(d, 416, meal_top, 190, "MealKcal",
                        ["- breakfast : Macros", "- lunch : Macros", "- snack : Macros",
                         "- dinner : Macros"], fill=GREY_PALE, header=GREY)
    _uml_class(d, 416, meal_top + h_meal + 14, 190, "AIFoodSuggest", [
        "- id : String", "- name : String", "- calories : Calories",
        "- macronutrients : Macros", "- description : String",
    ], stereotype="\u00abdocument: ai_food_suggests\u00bb", fill=AMBER_PALE, header=AMBER)

    # enumeration note
    d.rrect(4, 128, 172, 112, r=3, fill=colors.HexColor("#fdf8ec"), stroke=AMBER, lw=0.8)
    d.text(9, 140, "\u00abenumeration\u00bb domain enums", 6.3, SANS_B, AMBER)
    for i, line in enumerate([
        "Plan      WEIGHT_LOSS, WEIGHT_GAIN",
        "Gender    MALE, FEMALE",
        "Goal      MILD(15), MODERATE(20),",
        "          AGGRESSIVE(25)",
        "Activity  SEDENTARY(1.2), LIGHT(1.375),",
        "          MODERATE(1.55), HARD(1.725),",
        "          ATHLETE(1.9)",
    ]):
        d.text(9, 152 + i * 8.6, line, 5.9, SANS, INK_SOFT)

    # associations / compositions
    d.line(176, 42, 196, 42, TEAL_DARK, 0.8)
    d.text(177, 37, "1", 5.6, SANS, TEAL_DARK)
    d.text(185, 37, "0..*", 5.6, SANS, TEAL_DARK)
    d.arrow(295, 196, 295, track_top, head=5)
    d.text(299, 220, "dietPlanId  (1 : N)", 5.8, SANS, TEAL_DARK)

    d.line(511, 16 + h_cal, 511, mac_top, TEAL_DARK, 0.8)
    _diamond_marker(d, 511, 16 + h_cal + 2.5, 3.4, GREY)
    d.line(511, mac_top + h_mac, 511, meal_top, TEAL_DARK, 0.8)
    _diamond_marker(d, 511, mac_top + h_mac + 2.5, 3.4, GREY)
    d.line(394, track_top, 470, meal_top + h_meal + 2, TEAL_DARK, 0.8)
    _diamond_marker(d, 398, track_top - 3, 3.6, TEAL_DARK)

    d.text(4, 404, "Composition: a DietPlanTrack owns one MealKcal, which aggregates four Macros; each Macros embeds three Calories value",
           5.9, SANS, MUTED)
    d.text(4, 415, "objects (taken/total). Association: every track document stores the identifier of the owning plan. AIFoodSuggest",
           5.9, SANS, MUTED)
    d.text(4, 426, "reuses Macros for the macronutrient figures returned by the language model.", 5.9, SANS, MUTED)
    return d.outcome()


# ---------------------------------------------------------------------------
# Sequence diagram helpers
# ---------------------------------------------------------------------------
def _lifelines(d, xs, labels, top=22, bottom=300):
    for x, lab in zip(xs, labels):
        d.rrect(x - 42, top, 84, 22, r=3, fill=TEAL_DARK, stroke=TEAL_DARK)
        lines = wrap(lab, SANS_B, 5.6, 78)
        start = top + 11 - (len(lines) - 1) * 3.4
        for i, ln in enumerate(lines):
            d.text(x, start + i * 6.8, ln, 5.6, SANS_B, colors.white, "middle")
        d.line(x, top + 22, x, bottom, GREY, 0.6, dash=(2, 2))


def _clip(label, font, size, max_w):
    """Shorten a label with an ellipsis so that it cannot leave the canvas."""
    if sw(label, font, size) <= max_w:
        return label
    out = label
    while out and sw(out + "\u2026", font, size) > max_w:
        out = out[:-1]
    return out.rstrip(" ,;:-") + "\u2026"


def _msg(d, x1, x2, top, label, color=TEAL_DARK, num=None, dash=None, size=5.6):
    d.arrow(x1, top, x2, top, head=5, color=color, lw=0.8, dash=dash)
    if label:
        label = _clip(label, SANS, size, 462)
        tw = sw(label, SANS, size) + 4
        left = min(x1, x2) + 3
        if left + tw > 470:
            left = 470 - tw
        d.rect(left - 1, top - 8.2, tw, 8.4, fill=colors.white, stroke=None, lw=0)
        d.text(left, top - 2.4, label, size, SANS, INK)
    if num:
        d.text(min(x1, x2) - 3, top - 2.4, str(num), 5.5, SANS_B, MUTED, "end")


def _self(d, x, top, label, color=TEAL_DARK, size=5.6):
    label = _clip(label, SANS, size, 468 - (x + 27))
    d.poly([(x, top), (x + 22, top), (x + 22, top + 11), (x + 2, top + 11)], color=color, lw=0.8)
    tw = sw(label, SANS, size) + 2
    d.rect(x + 24, top + 0.8, min(tw, 470 - x - 24), 8.4, fill=colors.white, stroke=None, lw=0)
    d.text(x + 27, top + 6.4, label, size, SANS, INK)


def seq_login():
    d = D(475, 404)
    xs = [50, 140, 240, 335, 428]
    _lifelines(d, xs, ["LoginComponent", "AuthService /\nTokenInterceptor",
                       "AuthenticationFilter", "CustomAuthentication\nManager / UserService",
                       "MongoDB +\nJWTTokenService"], bottom=352)
    y = 64
    _msg(d, 50, 140, y, "login(username, password)", num="1")
    y += 24
    _msg(d, 140, 240, y, "POST /authenticate", num="2")
    y += 24
    _msg(d, 240, 335, y, "authenticate(UsernamePasswordAuthenticationToken)", num="3")
    y += 24
    _msg(d, 335, 428, y, "findByUsername(username)", num="4")
    y += 24
    _msg(d, 428, 335, y, "user document (BCrypt hash)", num="5", dash=(2, 2), color=MUTED)
    y += 22
    _self(d, 335, y, "matches(raw, hash)")
    y += 24
    _msg(d, 335, 240, y, "Authentication (authenticated)", num="6", dash=(2, 2), color=MUTED)
    y += 22
    _self(d, 240, y, "generateToken(sub, 86 400 000 ms)")
    y += 24
    _msg(d, 240, 140, y, "200 OK + Set-Cookie Refresh-Token", num="7", dash=(2, 2), color=MUTED)
    y += 26
    d.text(4, y - 2, "lazy token handshake", 5.5, SANS_B, TEAL_DARK)
    _msg(d, 140, 240, y, "GET /user/username (no access token yet)", num="8")
    y += 24
    _msg(d, 140, 428, y, "POST /user/refresh (cookie) \u2192 {accessToken}", num="9")
    y += 24
    _msg(d, 140, 428, y, "GET /user/username + Authorization: Bearer", num="10")
    y += 24
    _msg(d, 428, 140, y, "200 OK {username}", num="11", dash=(2, 2), color=MUTED)
    y += 24
    badge = "router.navigate(['/dashboard'])"
    bw = sw(badge, SANS_B, 5.6) + 16
    d.rrect(6, y - 9, bw, 13, r=6, fill=TEAL_PALE, stroke=TEAL_MID, lw=0.6)
    d.text(6 + bw / 2, y, badge, 5.6, SANS_B, TEAL_DARK, "middle")
    d.text(4, y + 16, "Both tokens are signed with HMAC512. The refresh token exists only inside an HttpOnly cookie; the access token "
                      "exists only in Angular memory.", 5.6, SANS, MUTED)
    return d.outcome()


def seq_plan():
    d = D(475, 424)
    xs = [50, 142, 240, 332, 424]
    _lifelines(d, xs, ["DietPlanForm\nComponent", "DietPlanService\n(HTTP)", "DietPlanController",
                       "DietPlanService\n(server)", "NutrientsCalculator /\nRepositories"], bottom=404)
    y = 64
    _self(d, 50, y, "validateFields()")
    y += 26
    _msg(d, 50, 142, y, "createDietPlan(dto)", num="1")
    y += 24
    _msg(d, 142, 240, y, "POST /diet-plan", num="2")
    y += 24
    _msg(d, 240, 332, y, "createDietPlan(dietPlan)", num="3")
    y += 24
    _msg(d, 332, 424, y, "findBMI(), findMin/MaxDuration()", num="4")
    y += 24
    _msg(d, 424, 332, y, "healthy ranges (else BadRequestException)", num="5", dash=(2, 2), color=MUTED)
    y += 22
    _self(d, 332, y, "userId, todayWeight, active")
    y += 26
    _msg(d, 332, 424, y, "save(DietPlan) \u2192 diet_plans", num="6")
    y += 24
    _msg(d, 332, 424, y, "findTDEE, findDeficit/Surplus, findProtein/Fat/Carbs", num="7")
    y += 24
    _msg(d, 332, 424, y, "save(DietPlanTrack) \u2192 diet_plan_tracks", num="8")
    y += 24
    _msg(d, 240, 142, y, "200 OK  DietPlan", num="9", dash=(2, 2), color=MUTED)
    y += 24
    _msg(d, 142, 50, y, "navigate('/dashboard')", num="10", dash=(2, 2), color=MUTED)
    d.text(4, 418, "The day-1 track document is created inside the same request, so the dashboard is immediately populated.",
           5.6, SANS, MUTED)
    return d.outcome()


def seq_ai():
    d = D(475, 352)
    xs = [50, 142, 240, 332, 424]
    _lifelines(d, xs, ["AIFoodSuggest\nComponent", "AIFoodSuggest\nController", "AIFoodSuggest\nService",
                       "DietPlanService", "OpenRouterLLM\nService"], bottom=310)
    y = 64
    _msg(d, 50, 142, y, "POST /ai-food-suggest {meal, diet, cuisine}", num="1")
    y += 24
    _msg(d, 142, 240, y, "suggestFood(FilterDTO)", num="2")
    y += 24
    _msg(d, 240, 332, y, "getCaloriesByMealCategory(mealFilter)", num="3")
    y += 22
    _self(d, 332, y, "active plan \u2192 today \u2192 meal")
    y += 26
    _msg(d, 332, 240, y, "kcal budget (500 when no plan exists)", num="4", dash=(2, 2), color=MUTED)
    y += 22
    _self(d, 240, y, "buildPrompt()")
    y += 26
    _msg(d, 240, 424, y, "foodSuggestChat(prompt) \u2192 POST /chat/completions", num="5")
    y += 26
    _msg(d, 424, 240, y, "choices[0].message.content (JSON text)", num="6", dash=(2, 2), color=MUTED)
    y += 22
    _self(d, 240, y, "ObjectMapper.readValue(\u2026, List<AIFoodSuggest>)")
    y += 26
    _msg(d, 240, 50, y, "200 OK List<AIFoodSuggest> \u2192 food cards", num="7", dash=(2, 2), color=MUTED)
    y += 24
    d.rrect(6, y - 9, 108, 13, r=6, fill=ROSE_PALE, stroke=ROSE, lw=0.6)
    d.text(60, y, "410 GONE on parse failure", 5.6, SANS_B, ROSE, "middle")
    d.text(4, y + 16, "The model must answer with a JSON array only (temperature 0.3, /no_think); "
                      "a parse failure becomes HTTP 410.", 5.6, SANS, MUTED)
    return d.outcome()


# ---------------------------------------------------------------------------
# Figure 4.x  Activity diagram
# ---------------------------------------------------------------------------
def activity_plan():
    d = D(475, 372)
    d.rrect(196, 6, 84, 18, r=9, fill=TEAL, stroke=TEAL)
    d.text(238, 18, "start", 6.2, SANS_B, colors.white, "middle")
    d.box(150, 34, 176, 26, "Open /diet-plan-form", "AuthGuard obtains a valid access token",
          fill=TEAL_PALE, stroke=TEAL, tsize=6.8, ssize=5.7)
    d.box(150, 72, 176, 26, "Fill plan attributes",
          "title, plan, age, gender, height, weight, goal, activity, target, duration",
          fill=TEAL_PALE, stroke=TEAL, tsize=6.8, ssize=5.7)
    d.box(150, 110, 176, 24, "Client-side validation", "validateFields() \u00b7 validateTargetWeight()",
          fill=BLUE_PALE, stroke=BLUE, tsize=6.8, ssize=5.7)
    _diamond(d, 238, 148, 92, 30, "valid?")
    d.box(150, 196, 176, 26, "POST /diet-plan", "Bearer token attached by TokenInterceptor",
          fill=BLUE_PALE, stroke=BLUE, tsize=6.8, ssize=5.7)
    _diamond(d, 238, 236, 104, 32, "healthy BMI\n& duration?")
    d.box(150, 288, 176, 26, "Persist plan + day-1 track", "diet_plans  \u00b7  diet_plan_tracks",
          fill=GREEN_PALE, stroke=GREEN, tsize=6.8, ssize=5.7)
    d.box(150, 326, 176, 22, "Redirect to /dashboard", "", fill=TEAL_PALE, stroke=TEAL, tsize=6.8)
    d.rrect(196, 354, 84, 16, r=8, fill=WHITE, stroke=TEAL, lw=0.9)
    d.text(238, 365, "end", 6.2, SANS_B, TEAL_DARK, "middle")

    d.box(334, 108, 134, 30, "Toast: requirement message", "shown 5 s \u00b7 form retained", fill=ROSE_PALE,
          stroke=ROSE, tsize=6.4, ssize=5.5)
    d.box(334, 238, 134, 34, "400 Bad Request", '{"error":["min-max days are the healthy duration"]}',
          fill=ROSE_PALE, stroke=ROSE, tsize=6.4, ssize=5.4)

    d.arrow(238, 24, 238, 34, head=5)
    d.arrow(238, 60, 238, 72, head=5)
    d.arrow(238, 98, 238, 110, head=5)
    d.arrow(238, 134, 238, 148, head=5)
    d.arrow(238, 163, 238, 196, head=5)
    d.text(242, 184, "yes", 5.8, SANS_B, GREEN)
    d.poly([(284, 148), (312, 148), (312, 123), (334, 123)], head=True, color=ROSE)
    d.text(288, 142, "no", 5.8, SANS_B, ROSE)
    d.text(336, 148, "correct the field and resubmit", 5.4, SANS, MUTED)
    d.arrow(238, 222, 238, 236, head=5)
    d.arrow(238, 252, 238, 288, head=5)
    d.text(242, 274, "yes", 5.8, SANS_B, GREEN)
    d.poly([(290, 252), (318, 252), (318, 255), (334, 255)], head=True, color=ROSE)
    d.text(296, 246, "no", 5.8, SANS_B, ROSE)
    d.arrow(238, 314, 238, 326, head=5)
    d.arrow(238, 348, 238, 354, head=5)
    return d.outcome()


# ---------------------------------------------------------------------------
# Figure 4.x  State machine
# ---------------------------------------------------------------------------
def state_plan():
    d = D(475, 220)
    d.d.add(Circle(16, d.y(74), 5, fillColor=INK, strokeColor=INK))
    d.arrow(22, 74, 40, 74, head=5)
    d.rrect(40, 50, 118, 48, r=8, fill=GREY_PALE, stroke=GREY)
    d.text(99, 70, "No active plan", 7.2, SANS_B, INK, "middle")
    d.text(99, 84, "active = false", 5.9, SANS, MUTED, "middle")
    d.rrect(190, 50, 126, 48, r=8, fill=TEAL_PALE, stroke=TEAL, lw=1.1)
    d.text(253, 70, "Active plan", 7.2, SANS_B, TEAL_DARK, "middle")
    d.text(253, 84, "active = true, day \u2264 duration", 5.9, SANS, MUTED, "middle")
    d.rrect(348, 50, 108, 48, r=8, fill=AMBER_PALE, stroke=AMBER)
    d.text(402, 70, "Completed", 7.2, SANS_B, AMBER, "middle")
    d.text(402, 84, "active = false", 5.9, SANS, MUTED, "middle")

    d.arrow(158, 74, 190, 74, head=5)
    d.text(162, 68, "createDietPlan()", 5.7, SANS, MUTED)
    d.arrow(316, 74, 348, 74, head=5)
    d.text(318, 68, "day > duration", 5.7, SANS, MUTED)
    d.d.add(Circle(468, d.y(74), 6, fillColor=WHITE, strokeColor=INK))
    d.d.add(Circle(468, d.y(74), 3.4, fillColor=INK, strokeColor=INK))
    d.arrow(456, 74, 462, 74, head=5)

    # resume transition
    d.poly([(402, 50), (402, 24), (253, 24), (253, 50)], head=True, color=TEAL, dash=(2, 2))
    d.text(268, 20, "continue a past plan  \u2192  new active plan", 5.7, SANS, TEAL_DARK)

    # self transition
    d.curved = None
    d.line(253, 98, 253, 112, TEAL, 0.9)
    d.line(253, 112, 300, 112, TEAL, 0.9)
    d.arrow(300, 112, 300, 98, head=5, color=TEAL)
    d.text(306, 118, "addWeight() / updateMacros()  \u21ba  stay active", 5.7, SANS, TEAL_DARK)

    d.text(4, 148, "A plan is created in the active state; once the elapsed day count exceeds the planned duration the server flips the flag to false",
           5.8, SANS, MUTED)
    d.text(4, 160, "on the next status check. Archived plans remain readable through the history screens and can be cloned into a new plan,",
           5.8, SANS, MUTED)
    d.text(4, 172, "which re-seeds a fresh day-1 track document. Terminal state is reached when the user abandons tracking altogether.",
           5.8, SANS, MUTED)
    return d.outcome()


# ---------------------------------------------------------------------------
# Figure 4.x  Document / ER model
# ---------------------------------------------------------------------------
def _crowsfoot(d, x, top, direction="right", size=6, color=INK):
    if direction == "right":
        d.line(x, top, x + size, top - 3, color, 0.8)
        d.line(x, top, x + size, top, color, 0.8)
        d.line(x, top, x + size, top + 3, color, 0.8)
    else:
        d.line(x, top, x - size, top - 3, color, 0.8)
        d.line(x, top, x - size, top, color, 0.8)
        d.line(x, top, x - size, top + 3, color, 0.8)


def er():
    d = D(560, 340)
    h_user = _entity(d, 4, 18, 150, "users", [
        "PK  _id : ObjectId",
        "     username : String",
        "     email : String",
        "     password : String",
        "              (BCrypt)",
    ], fill=ROSE_PALE, header=ROSE)

    h_plan = _entity(d, 174, 18, 176, "diet_plans", [
        "PK  _id : ObjectId",
        "     title : String",
        "     plan : Plan",
        "     age : int, gender : Gender",
        "     height, weight, todayWeight",
        "     goal : Goal",
        "     targetWeight, duration",
        "     activity : Activity",
        "FK  userId \u2192 users._id",
        "     active : boolean",
        "     createdAt : ISODate",
    ], fill=TEAL_PALE, header=TEAL_DARK)

    _entity(d, 174, 176, 176, "diet_plan_tracks", [
        "PK  _id : ObjectId",
        "FK  dietPlanId \u2192 diet_plans._id",
        "     weight, tdee : double",
        "     intake : Calories",
        "     protein, carbs, fat : Calories",
        "     mealKcal : MealKcal",
        "     dayCount : int",
        "     createdAt : ISODate",
    ], fill=TEAL_PALE, header=TEAL_DARK)

    _entity(d, 368, 18, 186, "ai_food_suggests", [
        "PK  _id : ObjectId",
        "     name : String",
        "     calories : Calories",
        "     macronutrients : Macros",
        "     description : String",
    ], fill=AMBER_PALE, header=AMBER)

    d.line(158, 40, 174, 40, INK, 0.9)
    d.text(157, 35, "1", 5.9, SANS, INK, "end")
    d.text(176, 35, "N", 5.9, SANS, INK)
    y_link = 18 + h_plan + 10
    d.line(262, 18 + h_plan, 262, 176, INK, 0.9)
    d.text(266, 18 + h_plan + 12, "1", 5.9, SANS, INK)
    d.text(266, 170, "N", 5.9, SANS, INK)

    d.rrect(368, 108, 186, 76, r=4, fill=colors.HexColor("#f9fbfb"), stroke=TEAL_MID, lw=0.8, dash=(2, 2))
    d.text(374, 120, "embedded value objects", 6.2, SANS_B, TEAL_DARK)
    for i, line in enumerate([
        "MealKcal { breakfast, lunch, snack, dinner }",
        "Macros   { protein, fat, carbs : Calories }",
        "Calories { taken : double, total : double }",
    ]):
        d.text(374, 132 + i * 9, line, 5.8, SANS, INK_SOFT)
    d.text(374, 168, "One self-contained document per day:", 5.8, SANS, INK_SOFT)
    d.text(374, 178, "the dashboard needs no joins.", 5.8, SANS, INK_SOFT)

    d.text(4, 292, "Referential integrity is enforced in the service layer: identifiers are never accepted from the client and every repository",
           5.9, SANS, MUTED)
    d.text(4, 303, "query is scoped by the authenticated principal read from the security context. Collections are created implicitly by",
           5.9, SANS, MUTED)
    d.text(4, 314, "Spring Data MongoDB on first write; the release does not use a schema-migration tool.", 5.9, SANS, MUTED)
    d.text(4, 330, "Cardinalities: users 1 \u2014 0..* diet_plans; diet_plans 1 \u2014 0..* diet_plan_tracks (one per tracked day).",
           5.9, SANS, MUTED)
    return d.outcome()
