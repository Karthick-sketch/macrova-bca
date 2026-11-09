"""Figures: component diagram, deployment diagram, DFD level 0 and level 1."""

import matplotlib.patches as mpatches

from diagram_lib import (BLUE, BLUE_LIGHT, GREY, GREY_LIGHT, INK, ORANGE, ORANGE_LIGHT,
                         TEAL, TEAL_DARK, TEAL_LIGHT, arrow, box, canvas, ellipse, note,
                         poly_arrow, save)

OUT = "/home/user/macrova-bca/docs/output/assets"
BORDER_C = "#c9d6dd"

# ---------------------------------------------------------------- component tree
fig, ax = canvas(13.0, 9.6)
ax.text(50, 90.5, "Angular 19 standalone component tree (frontend project macrova-ui)",
        ha="center", fontsize=13, fontweight="bold", color=INK)

box(ax, 32, 82.0, 36, 6.4, "AppComponent (app-root)", ["hosts header + router outlet"],
    accent=TEAL_DARK, title_size=11.2, body_size=9.4)

box(ax, 5, 73.5, 26, 6.4, "HeaderComponent", ["navigation, profile, sign-out"],
    accent=TEAL, title_size=10.4, body_size=9.0)
box(ax, 37, 73.5, 26, 6.4, "RouterOutlet", ["route rendering of pages"],
    accent=BLUE, title_size=10.4, body_size=9.0)
box(ax, 69, 73.5, 26, 6.4, "ToastComponent", ["error / validation messages"],
    accent=ORANGE, title_size=10.4, body_size=9.0)

for x in (18, 50, 82):
    arrow(ax, (50, 82.0), (x, 79.9), color=GREY, lw=1.0)

# row 1
box(ax, 5, 63.0, 26, 7.4, "LoginComponent", ["/login", "credential form"], accent=TEAL,
    title_size=10.0, body_size=8.8)
box(ax, 37, 63.0, 26, 7.4, "SignupComponent", ["/signup", "username, email, password"],
    accent=TEAL, title_size=10.0, body_size=8.8)
box(ax, 69, 63.0, 26, 7.4, "DashboardComponent", ["/dashboard", "progress + 6 metric cards"],
    accent=BLUE, title_size=10.0, body_size=8.8)
# row 2
box(ax, 5, 52.5, 26, 7.4, "DietPlanFormComponent", ["/diet-plan-form", "wizard host component"],
    accent=ORANGE, title_size=10.0, body_size=8.8)
box(ax, 37, 52.5, 26, 7.4, "DietPlanComponent", ["/progress", "daily macro log editor"],
    accent=BLUE, title_size=10.0, body_size=8.8)
box(ax, 69, 52.5, 26, 7.4, "AIFoodSuggestComponent", ["/meals", "filter chips + results"],
    accent=ORANGE, title_size=10.0, body_size=8.8)
# row 3
box(ax, 5, 42.0, 26, 7.4, "DietPlansListComponent", ["/history", "plan history rows"],
    accent=TEAL, title_size=10.0, body_size=8.8)
box(ax, 37, 42.0, 26, 7.4, "DietPlanOverviewComponent", ["/history/:id", "day-by-day entries"],
    accent=TEAL, title_size=10.0, body_size=8.8)
box(ax, 69, 42.0, 26, 7.4, "DietPlanTrackOverviewComponent", ["/history/track/:id", "stored track reader"],
    accent=TEAL, title_size=9.4, body_size=8.8)
# row 4
box(ax, 5, 31.5, 26, 7.4, "NoActiveDietPlanComponent", ["/no-active-plan", "past-plan fallback"],
    accent=GREY, title_size=9.6, body_size=8.8)
box(ax, 37, 31.5, 26, 7.4, "PageNotFoundComponent", ["/not-found", "wildcard '**' route"],
    accent=GREY, title_size=10.0, body_size=8.8)
box(ax, 69, 31.5, 26, 7.4, "WeightTrackComponent", ["child of dashboard", "Chart.js line chart"],
    accent=BLUE, title_size=10.0, body_size=8.8)

# wizard children
box(ax, 5, 21.0, 26, 7.4, "BodyMetricsFormComponent", ["step 1  (input/output API)"],
    accent=TEAL_LIGHT, fill=TEAL_LIGHT, title_size=9.6, body_size=8.8)
box(ax, 37, 21.0, 26, 7.4, "GoalSelectionFormComponent", ["step 2  (input/output API)"],
    accent=TEAL_LIGHT, fill=TEAL_LIGHT, title_size=9.6, body_size=8.8)
box(ax, 69, 21.0, 26, 7.4, "MealPreferenceFormComponent", ["step 3  (input/output API)"],
    accent=TEAL_LIGHT, fill=TEAL_LIGHT, title_size=9.4, body_size=8.8)
box(ax, 37, 12.0, 26, 6.6, "DietPlanPreviewFormComponent", ["step 4  (input/output API)"],
    accent=TEAL_LIGHT, fill=TEAL_LIGHT, title_size=9.4, body_size=8.8)

arrow(ax, (18, 52.5), (18, 49.5), color=GREY, lw=1.0)
arrow(ax, (18, 42.0), (18, 28.6), color=GREY, lw=1.0)
arrow(ax, (50, 52.5), (50, 49.5), color=GREY, lw=1.0)
arrow(ax, (50, 42.0), (50, 28.6), color=GREY, lw=1.0)

# service layer band
ax.add_patch(mpatches.FancyBboxPatch((4.0, 2.0), 92.0, 8.2, boxstyle="round,pad=0,rounding_size=1.0",
             facecolor="#ffffff", edgecolor=BORDER_C, lw=1.3, zorder=2))
ax.plot([5.0, 95.0], [9.1, 9.1], color=TEAL_DARK, lw=2.6, solid_capstyle="round", zorder=3)
ax.text(50, 7.0, "Singleton service layer (providedIn: 'root')", ha="center", fontsize=10.2,
        fontweight="bold", color=INK, zorder=4)
ax.text(50, 4.2, "AuthService  ·  TokenService  ·  DietPlanService  ·  AIFoodSuggestService  ·  AuthGuard  ·  "
                 "BaseUrlPrefixInterceptor  ·  TokenInterceptor\nHTTP traffic: /api/** → proxy → Spring Boot REST API",
        ha="center", va="center", fontsize=8.8, color=GREY, linespacing=1.6, zorder=4)
save(fig, f"{OUT}/component-diagram.png")

# ---------------------------------------------------------------- deployment
fig, ax = canvas(13.0, 7.4)
ax.text(50, 64.0, "Macrova deployment topology (development profile described by the repository)",
        ha="center", fontsize=12.8, fontweight="bold", color=INK)


def node(ax, x, y, w, h, label, title, lines, accent):
    ax.add_patch(mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                 facecolor="#ffffff", edgecolor=BORDER_C, lw=1.4, zorder=2))
    ax.add_patch(mpatches.FancyBboxPatch((x + 1.0, y + h - 3.6), w - 2.0, 4.6,
                 boxstyle="round,pad=0,rounding_size=0.8", facecolor="#f2f7f8",
                 edgecolor="none", zorder=2.4))
    ax.plot([x + 2.0, x + 6.0], [y + h + 0.9, y + h + 0.9], color=accent, lw=3.0,
            solid_capstyle="round", zorder=3)
    ax.text(x + w / 2, y + h - 1.3, f"«device/node»  {label}", ha="center", va="center",
            fontsize=8.4, color=GREY, zorder=4, style="italic")
    ax.text(x + w / 2, y + h - 5.6, title, ha="center", va="center", fontsize=10.4,
            fontweight="bold", color=INK, zorder=4)
    ax.text(x + w / 2, y + h - 8.6, "\n".join(lines), ha="center", va="top",
            fontsize=9.0, color=GREY, linespacing=1.55, zorder=4)


node(ax, 2.0, 28.0, 29.0, 24.0, "user workstation", "Web browser",
     ["Chrome / Edge / Firefox", "loads the Angular 19 bundle", "from http://localhost:4200",
      "access JWT kept in memory", "refresh token in HttpOnly", "cookie (SameSite=Lax)"], TEAL)
node(ax, 35.5, 28.0, 29.0, 24.0, "presentation", "Angular dev server",
     ["ng serve (Angular CLI 19)", "proxy.conf.json rewrites", "/api/** → :8080 and strips",
      "the /api prefix", "TypeScript compiled", "on demand"], BLUE)
node(ax, 69.0, 28.0, 29.0, 24.0, "application", "Spring Boot 3.4.4",
     ["embedded Tomcat :8080", "stateless filter chain", "BCrypt · JJWT HMAC-512",
      "controllers → services", "→ Spring Data MongoDB"], ORANGE)

node(ax, 35.5, 12.0, 29.0, 12.5, "database server", "MongoDB 27017",
     ["database macrova", "3 collections"], TEAL_DARK)
node(ax, 69.0, 12.0, 29.0, 12.5, "external SaaS", "OpenRouter API",
     ["HTTPS chat completions", "optional dependency"], TEAL_DARK)

arrow(ax, (31.0, 40.0), (35.5, 40.0), label="HTTP /api", lw=1.7, label_dy=1.6)
arrow(ax, (64.5, 40.0), (69.0, 40.0), label="HTTP / JSON", lw=1.7, label_dy=1.6)
arrow(ax, (50.0, 28.0), (50.0, 24.5), label="mongo driver", lw=1.7, label_dx=7.5, label_dy=0.2,
      color=TEAL_DARK)
arrow(ax, (83.5, 28.0), (83.5, 24.5), label="RestTemplate", lw=1.7, label_dx=8.5, label_dy=0.2,
      color=TEAL_DARK)
arrow(ax, (69.0, 33.0), (64.5, 33.0), color=GREY, ls="--", lw=1.2)
ax.text(66.7, 34.2, "LLM call", fontsize=8.4, color=GREY, ha="center")

note(ax, 2.0, 3.0, 60.5,
     "Deployment-profile observations taken from the repository\n"
     "• CORS allow-list contains only http://localhost:4200; the refresh cookie is issued with secure=false.\n"
     "• JWT_SECRET, OPENROUTER_API_KEY and OPENROUTER_MODEL are supplied as environment properties.\n"
     "• MongoDB connectivity relies on the Spring Boot default localhost:27017 URI (the explicit URI line in\n"
     "   application.properties is commented out).\n"
     "• No Dockerfile, container manifest or CI pipeline is present, so the topology above is the documented\n"
     "   development profile rather than a production deployment descriptor.",
     accent=ORANGE, size=8.4)
save(fig, f"{OUT}/deployment-diagram.png")

# ---------------------------------------------------------------- DFD level 0
fig, ax = canvas(12.8, 6.6)
ax.text(50, 55.0, "Data Flow Diagram — Level 0 (context diagram)", ha="center",
        fontsize=13, fontweight="bold", color=INK)

ellipse(ax, 13.0, 31.0, 21.0, 19.0, "USER", ["registered account", "holder using the", "SPA in a browser"])
ellipse(ax, 87.0, 31.0, 21.0, 19.0, "OPENROUTER", ["third-party LLM", "inference", "provider"])
ellipse(ax, 50.0, 47.0, 32.0, 10.5, "0", ["MACROVA PLATFORM"], accent=TEAL_DARK)

box(ax, 4.0, 12.0, 25.0, 12.0, "D1  users", ["_id · username", "email · BCrypt hash"],
    accent=TEAL, title_size=10.4, body_size=8.8)
box(ax, 33.0, 12.0, 30.0, 12.0, "D2  diet_plans", ["plan header, metrics, targets,", "macros, status"],
    accent=BLUE, title_size=10.4, body_size=8.8)
box(ax, 67.0, 12.0, 29.0, 12.0, "D3  diet_plan_tracks", ["daily weight, intake, per-meal", "macro log"],
    accent=BLUE, title_size=10.4, body_size=8.8)

arrow(ax, (23.0, 34.5), (39.0, 41.0), label="credentials, profile,\nmeal and weight logs",
      label_dy=3.4, label_dx=-1.0)
poly_arrow(ax, [(39.0, 36.0), (34.0, 36.0), (25.0, 30.0)],
           label="JWT, dashboard, plan\nand track views", label_at=(26.0, 33.8))
arrow(ax, (61.5, 46.0), (76.5, 35.0), label="prompt\n(JSON mode)", label_dy=2.6, label_dx=4.0)
poly_arrow(ax, [(77.0, 30.0), (77.0, 40.0), (62.5, 43.6)],
           label="JSON array", label_at=(74.0, 39.6))
arrow(ax, (44.0, 41.6), (17.0, 24.2), color=GREY, ls="--", lw=1.3,
      label="user document", label_dy=-2.4, label_dx=3.0)
arrow(ax, (56.0, 41.6), (48.0, 24.2), color=GREY, ls="--", lw=1.3,
      label="plan document", label_dy=-1.0, label_dx=6.6)
poly_arrow(ax, [(57.0, 41.0), (66.0, 41.0), (78.0, 24.2)], color=GREY, ls="--", lw=1.3)
ax.text(80.6, 30.0, "track document", fontsize=8.6, color=GREY, ha="left")

note(ax, 2.0, 2.0, 44.0,
     "External entities\n"
     "The browser user is the only human entity. OpenRouter is contacted only by the AI food\n"
     "suggestion endpoint; the core authentication, plan-building and tracking flows do not\n"
     "depend on it, so the platform remains functional when the key is absent.",
     accent=ORANGE, size=8.6)
save(fig, f"{OUT}/dfd-level-0.png")

# ---------------------------------------------------------------- DFD level 1
fig, ax = canvas(13.0, 8.6)
ax.text(50, 81.0, "Data Flow Diagram — Level 1 (functional decomposition)", ha="center",
        fontsize=13, fontweight="bold", color=INK)

ellipse(ax, 8.5, 41.0, 15.0, 18.0, "USER", ["browser", "client"])
ellipse(ax, 91.5, 41.0, 15.0, 18.0, "OPENROUTER", ["LLM", "provider"])

box(ax, 20.0, 66.0, 26.0, 10.0, "1.0  Identity & Session",
    ["register · authenticate", "BCrypt verify · JWT issue", "refresh · logout"],
    accent=TEAL, title_size=9.8, body_size=8.4)
box(ax, 49.0, 66.0, 26.0, 10.0, "2.0  Plan Construction Wizard",
    ["body metrics · TDEE", "goal & duration · macros", "preview & activation"],
    accent=BLUE, title_size=9.8, body_size=8.4)
box(ax, 77.0, 66.0, 18.0, 10.0, "3.0  Dashboard", ["metrics aggregation", "weight chart feed"],
    accent=ORANGE, title_size=9.8, body_size=8.4)
box(ax, 20.0, 50.0, 26.0, 10.0, "4.0  Daily Macro Tracking",
    ["per-meal taken values", "weight update · totals", "intake recalculation"],
    accent=BLUE, title_size=9.8, body_size=8.4)
box(ax, 49.0, 50.0, 26.0, 10.0, "5.0  History & Review",
    ["plan history list", "per-plan day entries", "stored track reader"],
    accent=TEAL, title_size=9.8, body_size=8.4)
box(ax, 77.0, 50.0, 18.0, 10.0, "6.0  AI Suggestion", ["prompt assembly", "JSON parsing"],
    accent=ORANGE, title_size=9.8, body_size=8.4)

box(ax, 20.0, 39.0, 26.0, 6.4, "D1  users", [], accent=TEAL, title_size=9.6, body_size=8.4)
box(ax, 49.0, 39.0, 26.0, 6.4, "D2  diet_plans", [], accent=BLUE, title_size=9.6, body_size=8.4)
box(ax, 77.0, 39.0, 18.0, 6.4, "D3  diet_plan_tracks", [], accent=BLUE, title_size=8.8, body_size=8.4)
box(ax, 49.0, 28.0, 26.0, 6.4, "D4  ai_food_suggests", [], accent=ORANGE, title_size=9.4, body_size=8.4)

poly_arrow(ax, [(15.0, 47.0), (15.0, 71.0), (20.0, 71.0)], label="credentials", label_at=(15.0, 60.0))
arrow(ax, (20.0, 68.0), (12.5, 44.0), label="JWT", label_dx=-3.0, label_dy=-4.0)
arrow(ax, (33.0, 66.0), (33.0, 60.0), color=GREY, lw=1.3, label="plan state", label_dx=6.5, label_dy=0.1)
arrow(ax, (62.0, 66.0), (62.0, 60.0), color=GREY, lw=1.3, label="track", label_dx=4.2, label_dy=0.1)
poly_arrow(ax, [(46.0, 71.0), (49.0, 71.0)], color=TEAL)
arrow(ax, (33.0, 66.0), (33.0, 45.4), label="user + plan header", label_dx=-9.0, label_dy=0.2,
      color=TEAL, lw=1.4)
arrow(ax, (75.0, 66.0), (75.0, 56.4), label="metrics", label_dx=4.0, label_dy=0.2, lw=1.4)
arrow(ax, (86.0, 66.0), (86.0, 60.0), color=GREY, lw=1.1)
arrow(ax, (77.0, 55.0), (15.0, 55.0), color=GREY, ls="--", lw=1.2)
ax.text(20.0, 56.0, "filter / search request", fontsize=8.4, color=GREY)
arrow(ax, (18.0, 45.4), (86.0, 45.4), color=GREY, ls="--", lw=1.2)
arrow(ax, (86.0, 50.0), (91.5, 44.5), label="prompt", lw=1.4, label_dy=1.6, label_dx=2.0)
arrow(ax, (91.0, 39.0), (86.0, 47.5), color=GREY, lw=1.3)
arrow(ax, (86.0, 39.0), (62.0, 34.4), color=ORANGE, lw=1.4, ls="--")
ax.text(70.0, 34.0, "cached suggestion documents (service method present, not wired)", fontsize=8.0, color=GREY)

note(ax, 2.0, 6.0, 62.0,
     "Reading the diagram against the code\n"
     "Process 1.0 is implemented by UserController, AuthenticationFilter, CustomAuthenticationManager and\n"
     "JWTTokenService. Process 2.0 by DietPlanFormController/DietPlanFormService. Processes 3.0 and 4.0 by\n"
     "DietPlanController/DietPlanService. Process 5.0 reads the same entities through projection queries.\n"
     "Process 6.0 by AIFoodSuggestController/AIFoodSuggestService with the OpenRouter adapter. Data store D4 is\n"
     "written only by AIFoodSuggestService.addSuggestions, which no controller currently calls.",
     accent=ORANGE, size=8.4)
save(fig, f"{OUT}/dfd-level-1.png")
