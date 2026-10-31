"""Architecture, data-flow and deployment figures."""

from __future__ import annotations

from reportlab.lib import colors

from figlib import (AMBER, AMBER_PALE, BLUE, BLUE_PALE, D, GREEN, GREEN_PALE,
                    GREY, GREY_PALE, ROSE, ROSE_PALE, WHITE, sw)
from theme import (INK, INK_SOFT, MUTED, SANS, SANS_B, SERIF, SERIF_B, TEAL,
                   TEAL_DARK, TEAL_MID, TEAL_PALE)


# ---------------------------------------------------------------------------
# Figure 4.1  Three-tier architecture
# ---------------------------------------------------------------------------
def architecture():
    d = D(475, 352)
    # client tier
    d.frame(0, 12, 475, 88, "Presentation Tier  \u2014  Angular 19 single-page application")
    labels = ["Auth & Session", "Dashboard", "Diet Planner", "AI Meal Studio", "Plan History"]
    x = 9
    for i, lab in enumerate(labels):
        d.box(x, 26, 87, 34, lab, fill=TEAL_PALE, stroke=TEAL_MID, tsize=7.4,
              sub=["login.component", "dashboard.component", "diet-plan.component",
                   "ai-food-suggest", "diet-plans-list"][i], ssize=5.9)
        x += 93
    d.box(9, 66, 457, 26,
          "Tree-shakable standalone components  \u00b7  AuthGuard  \u00b7  TokenInterceptor  \u00b7  "
          "BaseUrlPrefixInterceptor  \u00b7  Reactive signals  \u00b7  Chart.js",
          fill=WHITE, stroke=TEAL_MID, tsize=6.5, tfont=SANS, tcolor=INK_SOFT)

    # mid arrows
    d.arrow(150, 100, 150, 118, both=True)
    d.arrow(320, 100, 320, 118, both=True)
    d.text(330, 112, "HTTPS / JSON  (dev proxy  /api \u2192 :8080)", 6.4, SANS, MUTED)

    # application tier
    d.frame(0, 118, 475, 130, "Application Tier  \u2014  Spring Boot 3.4.4 on Java 21 (org.karthick.macrova)")
    d.box(8, 132, 110, 42, "Security Layer", "SecurityConfig\nAuthenticationFilter\nJWTAuthenticationFilter\nExceptionHandlerFilter",
          fill=BLUE_PALE, stroke=BLUE, tsize=7.6, ssize=5.9)
    d.box(124, 132, 96, 42, "User Module", "UserController\nUserService\nUserRepository", fill=BLUE_PALE,
          stroke=BLUE, tsize=7.6, ssize=5.9)
    d.box(226, 132, 146, 42, "Diet Plan Module", "DietPlanController  \u00b7  DietPlanService\nDietPlanRepository  \u00b7  DietPlanTrackRepository\nDTOs \u00b7 Enums",
          fill=BLUE_PALE, stroke=BLUE, tsize=7.6, ssize=5.9)
    d.box(378, 132, 89, 42, "AI Suggest", "AIFoodSuggest\nController/Service\nLLMService", fill=BLUE_PALE,
          stroke=BLUE, tsize=7.6, ssize=5.9)
    d.box(8, 180, 150, 42, "NutrientsCalculator (util)", "BMR  \u00b7  TDEE  \u00b7  BMI  \u00b7  deficit/surplus\nmacro grams  \u00b7  meal split",
          fill=GREY_PALE, stroke=GREY, tsize=7.4, ssize=5.9)
    d.box(164, 180, 140, 42, "Cross-cutting", "UserSession  \u00b7  Mapper (ModelMapper)\nMacrosConstants  \u00b7  ErrorResponse", fill=GREY_PALE,
          stroke=GREY, tsize=7.4, ssize=5.9)
    d.box(310, 180, 157, 42, "Exception Handling", "@ControllerAdvice\nApplicationExceptionHandler\n404 \u00b7 400 \u00b7 401 \u00b7 410 mapping",
          fill=GREY_PALE, stroke=GREY, tsize=7.4, ssize=5.9)

    # external LLM
    d.box(330, 258, 137, 30, "OpenRouter LLM API", "chat/completions \u00b7 external service",
          fill=AMBER_PALE, stroke=AMBER, tsize=7.4, ssize=6.0, dash=(3, 2))
    d.poly([(420, 222), (420, 258)], color=AMBER, lw=1.0, dash=(2, 2))
    d.text(424, 244, "HTTPS", 6.2, SANS, AMBER)

    # data tier
    d.frame(0, 288, 330, 62, "Data Tier  \u2014  MongoDB  (database: macrova)")
    for i, (lab, sub) in enumerate([("users", "credentials"), ("diet_plans", "plan headers"),
                                    ("diet_plan_tracks", "daily logs"), ("ai_food_suggests", "AI cache")]):
        d.cylinder(9 + i * 79, 302, 72, 34, lab, sub, tsize=6.6)
    d.arrow(300, 248, 300, 288, both=True)
    d.text(86, 262, "Spring Data MongoDB repositories", 6.3, SANS, MUTED)
    d.text(86, 272, "(MongoTemplate converters)", 6.3, SANS, MUTED)
    return d.outcome()


# ---------------------------------------------------------------------------
# Figure 4.2  Package / component structure
# ---------------------------------------------------------------------------
def packages():
    d = D(475, 330)
    d.rrect(0, 10, 475, 312, r=8, fill=colors.white, stroke=TEAL, lw=1.0)
    d.text(10, 26, "org.karthick.macrova", 8.6, SANS_B, TEAL_DARK)
    d.text(10, 37, "MacrovaApplication  \u00b7  @SpringBootApplication  \u00b7  PasswordEncoder  \u00b7  RestTemplate beans",
           6.5, SANS, MUTED)

    # column 1
    d.box(8, 48, 148, 66, "user", "controller \u2192 UserController\nservice \u2192 UserService\nrepository \u2192 UserRepository\nentity \u2192 User (@Document)\ndto \u2192 UserDTO, UsernameDTO,\n        AccessTokenDTO",
          fill=BLUE_PALE, stroke=BLUE, tsize=8.0, ssize=6.1, align="center")
    d.box(8, 122, 148, 58, "security", "SecurityConfig \u00b7 SecurityConstants\nJWTTokenService \u00b7 UserSession\nfilter \u2192 AuthenticationFilter,\n         JWTAuthenticationFilter,\n         ExceptionHandlerFilter\nmanager \u2192 CustomAuthenticationManager",
          fill=ROSE_PALE, stroke=ROSE, tsize=8.0, ssize=5.9)
    d.box(8, 188, 148, 52, "exception", "ApplicationExceptionHandler\nBadRequestException\nEntityNotFoundException\nUnauthorizedException\nErrorResponse",
          fill=GREY_PALE, stroke=GREY, tsize=8.0, ssize=6.0)

    # column 2
    d.box(164, 48, 152, 122, "dietplan", "controller \u2192 DietPlanController\nservice \u2192 DietPlanService\nrepository \u2192 DietPlanRepository,\n             DietPlanTrackRepository\nentity \u2192 DietPlan, DietPlanTrack\ndto \u2192 BodyMetricsRequest/Response,\n      DietPlanOverviewDTO,\n      DietPlansHistoryDTO, MetricsDTO\nenums \u2192 Plan, Goal, Activity, Gender",
          fill=TEAL_PALE, stroke=TEAL, tsize=8.0, ssize=6.1)
    d.box(164, 178, 152, 62, "aifoodsuggest", "controller \u2192 AIFoodSuggestController\nservice \u2192 AIFoodSuggestService\nrepository \u2192 AIFoodSuggestRepository\nentity \u2192 AIFoodSuggest\ndto \u2192 FilterDTO",
          fill=GREEN_PALE, stroke=GREEN, tsize=8.0, ssize=6.0)

    # column 3
    d.box(324, 48, 143, 62, "aichatservice", "LLMService (interface)\nOpenRouterLLMService\nmodel \u2192 ChatModel, MessageModel",
          fill=AMBER_PALE, stroke=AMBER, tsize=8.0, ssize=6.1)
    d.box(324, 118, 143, 58, "shared", "Mapper\nmodel \u2192 Calories, Macros,\n         MealKcal, Meals",
          fill=GREY_PALE, stroke=GREY, tsize=8.0, ssize=6.1)
    d.box(324, 184, 143, 56, "util", "NutrientsCalculator\nconstants \u2192 MacrosConstants",
          fill=GREY_PALE, stroke=GREY, tsize=8.0, ssize=6.1)
    d.box(324, 248, 143, 34, "config", "MongoConfig (LocalDate conv.)\nModelMapperConfig", fill=GREY_PALE,
          stroke=GREY, tsize=8.0, ssize=6.1)

    d.box(8, 248, 308, 34, "Cross-package dependency rule:  web \u2192 service \u2192 repository \u2192 entity/document  \u00b7  "
          "DTOs never expose entities  \u00b7  util is stateless", fill=WHITE, stroke=TEAL_MID,
          tsize=6.6, tfont=SANS, tcolor=INK_SOFT)
    # dependency arrows
    d.arrow(156, 110, 164, 110)
    d.arrow(316, 110, 324, 80)
    d.arrow(316, 200, 324, 148)
    d.text(240, 226, "aifoodsuggest depends on dietplan (calorie budget)",
           6.2, SANS, MUTED)
    d.text(240, 235, "and on aichatservice through the LLMService port", 6.2, SANS, MUTED)
    return d.outcome()


# ---------------------------------------------------------------------------
# Figure 4.3  Security filter chain
# ---------------------------------------------------------------------------
def filter_chain():
    d = D(475, 420)
    x, w = 70, 300
    steps = [
        ("HTTP request", "Angular TokenInterceptor attaches  Authorization: Bearer <jwt>", WHITE, GREY),
        ("CORS filter", "corsConfigurationSource \u00b7 origin http://localhost:4200 \u00b7 credentials", WHITE, GREY),
        ("ExceptionHandlerFilter", "JWTVerificationException \u2192 401  \u00b7  TokenExpired \u2192 401  \u00b7  RuntimeException \u2192 400", ROSE_PALE, ROSE),
        ("AuthenticationFilter  (/authenticate)", "reads JSON body \u2192 UsernamePasswordAuthenticationToken \u2192 CustomAuthenticationManager", AMBER_PALE, AMBER),
        ("JWTAuthenticationFilter", "validates signature (HMAC512) and places the principal in SecurityContext", BLUE_PALE, BLUE),
        ("Authorization rule", "POST /user/register and /user/refresh permitAll  \u00b7  anyRequest().authenticated()", BLUE_PALE, BLUE),
        ("DispatcherServlet \u2192 @RestController", "UserController  \u00b7  DietPlanController  \u00b7  AIFoodSuggestController", TEAL_PALE, TEAL),
        ("Service layer", "@Service beans \u00b7 @Transactional-free, request-scoped user resolution", TEAL_PALE, TEAL),
        ("Repository layer", "Spring Data MongoDB proxies (MongoRepository + @Query)", TEAL_PALE, TEAL),
        ("MongoDB  \u00b7  database macrova", "collection documents \u00b7 ObjectId keys \u00b7 embedded value objects", WHITE, GREY),
    ]
    top = 14
    for i, (title, sub, fill, stroke) in enumerate(steps):
        d.box(x, top, w, 31, title, sub, fill=fill, stroke=stroke, tsize=7.5, ssize=6.0)
        if i < len(steps) - 1:
            d.arrow(x + w / 2, top + 31, x + w / 2, top + 41, head=5.5)
        top += 41

    # side annotations
    d.text(6, 58, "stateless session", 6.2, SANS, MUTED)
    d.text(6, 140, "fail fast, no", 6.2, SANS, MUTED)
    d.text(6, 150, "stack trace leak", 6.2, SANS, MUTED)
    d.text(378, 168, "\u2192 issues access", 6.2, SANS, MUTED)
    d.text(378, 178, "  token (1 h) and", 6.2, SANS, MUTED)
    d.text(378, 188, "  refresh cookie", 6.2, SANS, MUTED)
    d.text(378, 198, "  (24 h, HttpOnly)", 6.2, SANS, MUTED)
    d.poly([(370, 182), (378, 182)], color=MUTED, head=False)
    d.box(378, 250, 92, 36, "SecurityContext", "principal = username", fill=WHITE,
          stroke=BLUE, tsize=6.8, ssize=5.8, dash=(2, 2))
    d.arrow(370, 268, 378, 268, head=5, color=BLUE, dash=(2, 2))
    d.box(378, 322, 92, 40, "Global error body", '{"error":["message"]}', fill=WHITE,
          stroke=ROSE, tsize=6.8, ssize=5.8, dash=(2, 2))
    return d.outcome()


# ---------------------------------------------------------------------------
# Figure 4.4  DFD level 0
# ---------------------------------------------------------------------------
def dfd0():
    d = D(475, 216)
    d.actor(46, 44, "Macrova user")
    d.text(46, 86, "(visitor or registered user)", 6.2, SANS, MUTED, "middle")
    d.rrect(150, 46, 180, 96, r=48, fill=TEAL_PALE, stroke=TEAL, lw=1.1)
    d.text(240, 76, "0", 11, SANS_B, TEAL_DARK, "middle")
    d.text(240, 90, "Macrova Diet & Nutrition", 7.4, SANS_B, INK, "middle")
    d.text(240, 100, "Management System", 7.4, SANS_B, INK, "middle")
    d.text(240, 118, "Angular SPA  \u00b7  Spring Boot  \u00b7  MongoDB", 6.0, SANS, MUTED, "middle")

    d.text(58, 70, "registration, login,", 5.9, SANS, MUTED)
    d.text(58, 79, "plan, meal & weight data", 5.9, SANS, MUTED)
    d.arrow(58, 96, 146, 96, head=5.5)
    d.text(58, 112, "JWT, metrics, macros,", 5.9, SANS, MUTED)
    d.text(58, 121, "history, meal ideas", 5.9, SANS, MUTED)
    d.arrow(146, 104, 58, 104, head=5.5)

    d.box(352, 32, 118, 46, "OpenRouter", "LLM inference API\n(external entity)", fill=AMBER_PALE,
          stroke=AMBER, tsize=7.2, ssize=5.9, dash=(3, 2))
    d.arrow(330, 70, 352, 58, head=5, color=AMBER)
    d.text(332, 50, "prompt", 5.8, SANS, AMBER)
    d.arrow(352, 74, 330, 88, head=5, color=AMBER)
    d.text(334, 92, "JSON list", 5.8, SANS, AMBER)

    d.line(0, 158, 475, 158, colors.HexColor("#dfe7e6"), 0.6)
    d.text(0, 172, "Inputs: registration, login, body metrics, target weight, duration, daily weight and meal macro entries, filter selections.",
           6.0, SANS, MUTED)
    d.text(0, 184, "Outputs: authenticated session, computed energy targets, daily macro dashboard, weekly weight trend, plan history, meal recommendations.",
           6.0, SANS, MUTED)
    d.text(0, 202, "Level 0 (context) data-flow diagram of the Macrova system.", 6.2, SANS, MUTED)
    return d.outcome()


# ---------------------------------------------------------------------------
# Figure 4.5  DFD level 1
# ---------------------------------------------------------------------------
def dfd1():
    d = D(475, 392)
    d.actor(30, 118, "User")
    d.text(30, 162, "(presentation tier)", 5.8, SANS, MUTED, "middle")
    # interaction trunk
    d.line(64, 56, 64, 320, TEAL_DARK, 0.9)
    d.arrow(48, 146, 64, 146, head=5)
    d.arrow(64, 156, 48, 156, head=5)

    procs = [
        (34, "1.0  Account &\nSession Management", BLUE_PALE, BLUE),
        (100, "2.0  Diet Plan\nConfiguration", TEAL_PALE, TEAL),
        (166, "3.0  Nutrition\nComputation", GREEN_PALE, GREEN),
        (232, "4.0  Daily Tracking\n& Progress", TEAL_PALE, TEAL),
        (298, "5.0  AI Meal\nRecommendation", AMBER_PALE, AMBER),
    ]
    for top, title, fill, stroke in procs:
        d.oval(84, top, 120, 44, title, fill=fill, stroke=stroke, tsize=6.9)
        d.arrow(64, top + 22, 84, top + 22, head=5, both=True)

    stores = [
        (43, "D1  users", ROSE_PALE),
        (109, "D2  diet_plans", BLUE_PALE),
        (241, "D3  diet_plan_tracks", TEAL_PALE),
        (307, "D4  ai_food_suggests", AMBER_PALE),
    ]
    for top, title, fill in stores:
        d.datastore(300, top, 158, 26, title, fill=fill)
    for top in (43, 109, 241, 307):
        d.arrow(204, top + 22, 300, top + 13, head=5)
        d.arrow(300, top + 18, 204, top + 27, head=5, color=MUTED, dash=(2, 2))

    # internal computation links
    d.arrow(144, 144, 144, 166, head=5, both=True, color=GREEN)
    d.arrow(144, 210, 144, 232, head=5, both=True, color=GREEN)
    d.text(148, 158, "energy & macro targets", 5.7, SANS, GREEN)
    d.text(148, 224, "recompute on new weight", 5.7, SANS, GREEN)

    # external entity
    d.box(300, 356, 158, 28, "OpenRouter LLM API", "external inference service", fill=AMBER_PALE,
          stroke=AMBER, tsize=6.9, ssize=5.6, dash=(2, 2))
    d.arrow(270, 320, 300, 366, head=5, color=AMBER)
    d.arrow(300, 372, 268, 330, head=5, color=AMBER)
    d.text(206, 348, "prompt with meal calorie budget", 5.6, SANS, AMBER)
    d.text(206, 358, "JSON food list", 5.6, SANS, AMBER)
    return d.outcome()


# ---------------------------------------------------------------------------
# Figure 4.6  DFD level 2 for process 4.0
# ---------------------------------------------------------------------------
def dfd2():
    d = D(475, 250)
    d.rrect(0, 8, 475, 232, r=6, fill=colors.white, stroke=TEAL_MID, lw=0.8, dash=(3, 2))
    d.text(8, 22, "Process 4.0  \u2014  Daily Tracking & Progress (decomposition)", 7.4, SANS_B, TEAL_DARK)
    labels = ["4.1  Resolve\ntoday's track", "4.2  Apply\nweight", "4.3  Apply meal\nmacros",
              "4.4  Recompute\ntotals", "4.5  Build\nmetrics DTO"]
    xs = [8, 102, 196, 290, 384]
    for i, (x, lab) in enumerate(zip(xs, labels)):
        fill = GREEN_PALE if i >= 3 else TEAL_PALE
        stroke = GREEN if i >= 3 else TEAL
        d.box(x, 30, 84, 36, lab, fill=fill, stroke=stroke, tsize=6.8, ssize=5.7)
        if i < 4:
            d.arrow(x + 84, 48, x + 94, 48, head=5)
    d.datastore(14, 112, 168, 26, "D2  diet_plans", fill=BLUE_PALE)
    d.datastore(250, 112, 176, 26, "D3  diet_plan_tracks", fill=TEAL_PALE)
    d.arrow(50, 66, 50, 112, head=5, both=True)
    d.arrow(143, 66, 143, 112, head=5, both=True)
    d.arrow(270, 66, 270, 112, head=5, both=True)
    d.arrow(350, 66, 350, 112, head=5, both=True)
    d.box(290, 168, 170, 30, "MetricsDTO  \u2192  dashboard.component", "weekly weight series + macro totals",
          fill=WHITE, stroke=BLUE, tsize=6.8, ssize=5.6)
    d.poly([(426, 66), (426, 168)], head=True)
    d.text(24, 152, "record, read & update", 5.7, SANS, MUTED)
    d.text(24, 164, "one document per day", 5.7, SANS, MUTED)
    d.text(8, 208, "Every meal update re-derives protein, fat and carbohydrate intake totals and the calorie deficit; the dashboard is never",
           5.9, SANS, MUTED)
    d.text(8, 218, "computed in the browser. A missing record for the current date triggers on-demand creation of the day's track document.",
           5.9, SANS, MUTED)
    return d.outcome()


# ---------------------------------------------------------------------------
# Figure 5.1  Technology stack
# ---------------------------------------------------------------------------
def tech_stack():
    d = D(475, 250)
    layers = [
        ("User interface", "Angular 19  \u00b7  TypeScript 5.7  \u00b7  HTML5  \u00b7  CSS custom properties  \u00b7  Chart.js 4.4",
         TEAL_PALE, TEAL),
        ("Client services", "HttpClient + functional interceptors  \u00b7  RxJS 7.8  \u00b7  jwt-decode 4  \u00b7  Signals  \u00b7  Route guards",
         BLUE_PALE, BLUE),
        ("Web / API layer", "Spring Boot 3.4.4 Web MVC  \u00b7  Jackson  \u00b7  REST controllers  \u00b7  Bean validation  \u00b7  ModelMapper 3.2",
         GREEN_PALE, GREEN),
        ("Security", "Spring Security 6  \u00b7  BCryptPasswordEncoder  \u00b7  java-jwt 4.5 (HMAC512)  \u00b7  Servlet filters",
         ROSE_PALE, ROSE),
        ("Domain & persistence", "Spring Data MongoDB  \u00b7  Lombok 1.18  \u00b7  MongoTemplate converters  \u00b7  Java 21 time API",
         GREY_PALE, GREY),
        ("Data store", "MongoDB  \u00b7  database macrova  \u00b7  collections, embedded documents, ObjectId", BLUE_PALE, BLUE),
        ("Integration & tooling", "OpenRouter LLM  \u00b7  Maven  \u00b7  npm  \u00b7  Git  \u00b7  Postman  \u00b7  Chrome DevTools",
         AMBER_PALE, AMBER),
    ]
    top = 10
    for title, sub, fill, stroke in layers:
        d.box(76, top, 394, 28, title, sub, fill=fill, stroke=stroke, tsize=7.6, ssize=6.3,
              align="center")
        top += 34
    d.text(0, 128, "presentation", 6.0, SANS, MUTED)
    d.text(0, 196, "service", 6.0, SANS, MUTED)
    d.text(0, 232, "data & tools", 6.0, SANS, MUTED)
    d.text(62, 136, "\u2193", 8, SANS_B, TEAL)
    return d.outcome()


# ---------------------------------------------------------------------------
# Figure 4.x  Nutrition computation pipeline
# ---------------------------------------------------------------------------
def nutrition():
    d = D(475, 205)
    steps = [
        ("Body metrics", "age, gender, height,\nweight, activity"),
        ("BMR", "Mifflin\u2013St Jeor"),
        ("TDEE", "BMR \u00d7 activity\nfactor (1.2\u20131.9)"),
        ("Energy target", "TDEE \u2212 deficit  or\nTDEE + surplus"),
        ("Macro split", "protein 30 %\nfat 30 %  carbs 40 %"),
        ("Meal split", "B 30 / L 30\nS 15 / D 25 %"),
    ]
    x = 4
    for i, (title, sub) in enumerate(steps):
        fill = TEAL_PALE if i % 2 == 0 else GREEN_PALE
        stroke = TEAL if i % 2 == 0 else GREEN
        d.box(x, 22, 70, 44, title, sub, fill=fill, stroke=stroke, tsize=7.0, ssize=5.9)
        if i < len(steps) - 1:
            d.arrow(x + 70, 44, x + 78, 44, head=5)
        x += 78
    # formulas band
    d.rrect(0, 78, 475, 50, r=5, fill=colors.HexColor("#f9fbfb"), stroke=TEAL_MID, lw=0.7)
    d.text(8, 92, "BMR male   = 10 w + 6.25 h \u2212 5 a + 5          BMR female = 10 w + 6.25 h \u2212 5 a \u2212 161",
           6.5, SANS, INK_SOFT)
    d.text(8, 104, "BMI        = w / h\u00b2 \u00d7 10 000          grams    = (kcal share) / (4 or 9)",
           6.5, SANS, INK_SOFT)
    d.text(8, 116, "duration   = min 7 d/kg (loss) / 14 d/kg (gain)  \u2026  max 28 d/kg          rounding \u2192 nearest 50/100 kcal",
           6.5, SANS, INK_SOFT)
    # feedback
    d.poly([(300, 66), (300, 74), (240, 74), (240, 66)], head=False, color=MUTED, dash=(2, 2))
    d.arrow(240, 66, 300, 66, head=5, color=MUTED, dash=(2, 2))
    d.text(8, 146, "Recorded weight changes re-run the chain from TDEE onwards, so calorie and macro targets adapt as the plan progresses.",
           6.3, SANS, MUTED)
    d.text(8, 158, "All arithmetic is executed server-side in NutrientsCalculator; the browser only displays the resulting values.",
           6.3, SANS, MUTED)
    return d.outcome()


# ---------------------------------------------------------------------------
# Figure 7.x  Deployment
# ---------------------------------------------------------------------------
def deployment():
    d = D(475, 240)
    d.box(6, 20, 120, 60, "Client device", "Chrome / Edge / Firefox\nAngular 19 bundle\nserved on :4200", fill=WHITE,
          stroke=GREY, tsize=7.6, ssize=6.0)
    d.box(6, 104, 120, 52, "Development proxy", "proxy.conf.json\n/api \u2192 localhost:8080", fill=GREY_PALE,
          stroke=GREY, tsize=7.4, ssize=6.0, dash=(2, 2))
    d.box(176, 60, 150, 90, "Application server", "Spring Boot 3.4.4 executable JAR\nembedded Tomcat :8080\nJava 21 runtime\nJWT secret + LLM keys\nvia environment variables",
          fill=TEAL_PALE, stroke=TEAL, tsize=7.8, ssize=6.1)
    d.cylinder(360, 66, 100, 46, "MongoDB", "localhost:27017/macrova", tsize=7.2)
    d.box(360, 148, 100, 46, "OpenRouter", "api/v1/chat/completions", fill=AMBER_PALE, stroke=AMBER,
          tsize=7.2, ssize=5.9, dash=(2, 2))
    d.box(176, 180, 150, 40, "Browser assets", "HTML5 \u00b7 CSS \u00b7 SVG icons\npublic/ static files", fill=WHITE,
          stroke=GREY, tsize=7.2, ssize=5.9)

    d.arrow(126, 50, 176, 76, both=True, head=5)
    d.text(128, 44, "HTTP :4200", 6.0, SANS, MUTED)
    d.arrow(126, 122, 176, 118, both=True, head=5)
    d.text(130, 138, "XHR /api", 6.0, SANS, MUTED)
    d.arrow(326, 92, 360, 88, both=True, head=5)
    d.text(322, 76, "27017", 6.0, SANS, MUTED)
    d.arrow(326, 132, 360, 164, both=True, head=5)
    d.text(300, 158, "HTTPS 443", 6.0, SANS, AMBER)
    d.arrow(250, 180, 250, 150, head=5, dash=(2, 2))
    return d.outcome()


# ---------------------------------------------------------------------------
# Figure 4.x  Front-end route / component map
# ---------------------------------------------------------------------------
def routes():
    d = D(475, 300)
    d.box(150, 6, 175, 26, "AppComponent  (app-root)", "", fill=TEAL_PALE, stroke=TEAL, tsize=7.8)
    d.box(150, 42, 175, 22, "HeaderComponent  +  RouterOutlet", "", fill=WHITE, stroke=TEAL_MID, tsize=7.2)
    items = [
        ("/login", "LoginComponent", 4, 96),
        ("/signup", "SignupComponent", 4, 130),
        ("/dashboard", "DashboardComponent \u2020", 4, 164),
        ("/progress", "DietPlanComponent \u2020", 168, 164),
        ("/meals", "AIFoodSuggestComponent \u2020", 330, 164),
        ("/history", "DietPlansListComponent \u2020", 4, 198),
        ("/history/:id", "DietPlanOverviewComponent", 168, 198),
        ("/history/track/:id", "DietPlanTrackOverviewComponent", 330, 198),
        ("/diet-plan-form", "DietPlanFormComponent \u2020", 4, 232),
        ("/no-active-plan", "NoActiveDietPlanComponent \u2020", 168, 232),
        ("/**", "PageNotFoundComponent", 330, 232),
    ]
    for path, comp, x, top in items:
        d.rrect(x, top, 148, 28, r=4, fill=WHITE, stroke=TEAL_MID, lw=0.8)
        d.text(x + 6, top + 10.5, path, 6.9, SANS_B, TEAL_DARK)
        d.text(x + 6, top + 20.5, comp, 6.2, SANS, INK_SOFT)
    d.text(4, 84, "Routes declared in app.routes.ts  \u2014  \u2020 protected by AuthGuard (refresh-token handshake on activation)",
           6.2, SANS, MUTED)
    d.text(4, 272, "Lazy-free eager imports: every route binds a standalone component declared in the bootstrap configuration;",
           6.0, SANS, MUTED)
    d.text(4, 282, "child components (WeightTrackComponent, ToastComponent) are imported directly by their hosts.",
           6.0, SANS, MUTED)
    return d.outcome()


# ---------------------------------------------------------------------------
# Figure 4.x  JWT session lifecycle
# ---------------------------------------------------------------------------
def tokens():
    d = D(475, 185)
    # timeline
    d.line(30, 40, 445, 40, GREY, 1.0)
    marks = [(30, "t0\nlogin"), (150, "t0 + 60 min\naccess token expires"), (300, "t0 + 24 h\nrefresh token expires"), (445, "re-login")]
    for x, lab in marks:
        d.line(x, 34, x, 46, GREY, 1.0)
        for i, ln in enumerate(lab.split("\n")):
            d.text(x, 56 + i * 9, ln, 6.1, SANS, MUTED, "middle")
    d.rrect(30, 18, 120, 14, r=7, fill=TEAL, stroke=TEAL)
    d.text(90, 27.5, "access token valid (1 h)", 6.0, SANS_B, WHITE, "middle")
    d.rrect(150, 92, 150, 14, r=7, fill=BLUE, stroke=BLUE)
    d.text(225, 101.5, "refresh cookie valid (24 h, HttpOnly)", 6.0, SANS_B, WHITE, "middle")
    d.arrow(150, 40, 150, 88, head=5, dash=(2, 2), color=BLUE)
    d.arrow(90, 92, 90, 44, head=5, dash=(2, 2), color=TEAL)
    d.text(4, 120, "1.  POST /authenticate  \u2192  AuthenticationFilter issues the access token in the response body and the refresh token as a",
           6.2, SANS, INK_SOFT)
    d.text(10, 131, "     SameSite=Lax, HttpOnly cookie (path /, max-age 86 400 s).", 6.2, SANS, INK_SOFT)
    d.text(4, 144, "2.  TokenInterceptor verifies expiry locally with jwt-decode; an expired token triggers POST /user/refresh, which",
           6.2, SANS, INK_SOFT)
    d.text(10, 155, "     re-issues a fresh 60-minute access token from the cookie.", 6.2, SANS, INK_SOFT)
    d.text(4, 168, "3.  POST /user/logout clears the cookie (max-age 0) and the SPA drops the in-memory token.", 6.2, SANS, INK_SOFT)
    return d.outcome()


# ---------------------------------------------------------------------------
# Figure 1.1  End-to-end user journey
# ---------------------------------------------------------------------------
def journey():
    d = D(475, 126)
    stages = [
        ("Register", "POST /user/register\nBCrypt digest"),
        ("Create plan", "body metrics, target,\nduration, activity"),
        ("Receive targets", "TDEE, intake, macros\nmeal split"),
        ("Log intake", "per-meal macros\nweight update"),
        ("Review trend", "dashboard chart\nweekly metrics"),
        ("Plan archive", "history, past plan\nresume or renew"),
    ]
    w, gap = 72, 6
    x = 4
    for i, (title, sub) in enumerate(stages):
        fill = TEAL_PALE if i % 2 == 0 else GREEN_PALE
        stroke = TEAL if i % 2 == 0 else GREEN
        d.rrect(x, 26, w, 46, r=5, fill=fill, stroke=stroke)
        d.text(x + w / 2, 40, title, 6.9, SANS_B, INK, "middle")
        for j, line in enumerate(sub.split("\n")):
            d.text(x + w / 2, 51 + j * 7.2, line, 5.5, SANS, INK_SOFT, "middle")
        if i < len(stages) - 1:
            d.arrow(x + w, 49, x + w + gap - 1, 49, head=4.5)
        x += w + gap
    d.box(120, 84, 236, 28, "AI meal suggestion (optional branch)",
          "POST /ai-food-suggest  \u2192  OpenRouter  \u2192  JSON food list",
          fill=AMBER_PALE, stroke=AMBER, tsize=6.6, ssize=5.6, dash=(2, 2))
    d.arrow(238, 84, 238, 74, head=5, color=AMBER)
    d.text(4, 16, "A single account spans the whole journey: the plan, the daily tracks and the archive are all scoped to the authenticated principal.",
           5.8, SANS, MUTED)
    return d.outcome()


# ---------------------------------------------------------------------------
# Figure 3.1  Existing versus proposed workflow
# ---------------------------------------------------------------------------
def existing_vs_proposed():
    d = D(475, 250)
    d.rrect(0, 8, 232, 226, r=6, fill=colors.HexColor("#fbf7f6"), stroke=ROSE, lw=0.9)
    d.text(116, 22, "Existing practice", 7.6, SANS_B, ROSE, "middle")
    left = [
        ("Paper or spreadsheet plan", "target weight, no energy budget"),
        ("Generic online calculator", "single number, formula hidden"),
        ("Manual macro arithmetic", "grams guessed per meal"),
        ("Daily diary / notes app", "no derived totals"),
        ("Rework on every change", "old records overwritten"),
        ("No traceable history", "cannot compare plans"),
    ]
    y = 34
    for title, sub in left:
        d.rrect(10, y, 212, 24, r=4, fill=WHITE, stroke=colors.HexColor("#e8cfcb"), lw=0.6)
        d.text(16, y + 10, title, 6.4, SANS_B, INK)
        d.text(16, y + 18.6, sub, 5.5, SANS, MUTED)
        y += 29
    d.rrect(243, 8, 232, 226, r=6, fill=colors.HexColor("#f6fbfa"), stroke=TEAL, lw=0.9)
    d.text(359, 22, "Proposed system (Macrova)", 7.6, SANS_B, TEAL_DARK, "middle")
    right = [
        ("Validated plan request", "BMI and duration guards"),
        ("Deterministic engine", "BMR \u2192 TDEE \u2192 intake \u2192 macros"),
        ("Per-meal targets", "30 / 30 / 15 / 25 split"),
        ("Server-side recomputation", "totals and deficit derived"),
        ("Immutable daily documents", "one per tracked day"),
        ("Archive and resume", "history, past plan, new plan"),
    ]
    y = 34
    for title, sub in right:
        d.rrect(253, y, 212, 24, r=4, fill=WHITE, stroke=TEAL_MID, lw=0.6)
        d.text(259, y + 10, title, 6.4, SANS_B, INK)
        d.text(259, y + 18.6, sub, 5.5, SANS, INK_SOFT)
        y += 29
    d.arrow(232, 120, 243, 120, head=5, color=TEAL)
    return d.outcome()
