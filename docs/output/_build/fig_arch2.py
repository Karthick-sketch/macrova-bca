"""Figures: deployment diagram and DFD level 1 (final layouts)."""

import matplotlib.patches as mpatches

from diagram_lib import (BLUE, GREY, INK, ORANGE, TEAL, TEAL_DARK, arrow, box, canvas,
                         ellipse, note, poly_arrow, save)

OUT = "/home/user/macrova-bca/docs/output/assets"
BORDER_C = "#c9d6dd"

# ---------------------------------------------------------------- deployment
fig, ax = canvas(13.0, 9.6)
ax.text(50, 71.0, "Macrova deployment topology (development profile described by the repository)",
        ha="center", fontsize=12.6, fontweight="bold", color=INK)


def node(x, y, w, h, label, title, lines, accent):
    ax.add_patch(mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                 facecolor="#ffffff", edgecolor=BORDER_C, lw=1.4, zorder=2))
    ax.add_patch(mpatches.FancyBboxPatch((x + 1.0, y + h - 3.6), w - 2.0, 4.6,
                 boxstyle="round,pad=0,rounding_size=0.8", facecolor="#f2f7f8",
                 edgecolor="none", zorder=2.4))
    ax.plot([x + 2.0, x + 6.0], [y + h + 0.85, y + h + 0.85], color=accent, lw=3.0,
            solid_capstyle="round", zorder=3)
    ax.text(x + w / 2, y + h - 1.3, f"«device/node»   {label}", ha="center", va="center",
            fontsize=8.2, color=GREY, zorder=4, style="italic")
    ax.text(x + w / 2, y + h - 5.6, title, ha="center", va="center", fontsize=10.2,
            fontweight="bold", color=INK, zorder=4)
    ax.text(x + w / 2, y + h - 8.4, "\n".join(lines), ha="center", va="top",
            fontsize=8.8, color=GREY, linespacing=1.55, zorder=4)


node(2.0, 45.0, 29.0, 21.0, "user workstation", "Web browser",
     ["Chrome / Edge / Firefox", "loads the Angular 19 bundle", "from http://localhost:4200",
      "access JWT kept in memory", "refresh token in HttpOnly", "cookie (SameSite=Lax)"], TEAL)
node(35.5, 45.0, 29.0, 21.0, "presentation", "Angular dev server",
     ["ng serve (Angular CLI 19)", "proxy.conf.json rewrites", "/api/** → :8080 and strips",
      "the /api prefix", "TypeScript compiled on demand"], BLUE)
node(69.0, 45.0, 29.0, 21.0, "application", "Spring Boot 3.4.4",
     ["embedded Tomcat :8080", "stateless filter chain", "BCrypt · JJWT HMAC-512",
      "controllers → services", "→ Spring Data MongoDB"], ORANGE)

node(35.5, 30.5, 29.0, 10.5, "database server", "MongoDB 27017",
     ["database macrova · 3 collections"], TEAL_DARK)
node(69.0, 30.5, 29.0, 10.5, "external SaaS", "OpenRouter API",
     ["HTTPS chat completions · optional"], TEAL_DARK)

arrow(ax, (31.0, 56.0), (35.5, 56.0), label="HTTP /api", lw=1.7, label_dy=1.7)
arrow(ax, (64.5, 56.0), (69.0, 56.0), label="HTTP / JSON", lw=1.7, label_dy=1.7)
arrow(ax, (50.0, 45.0), (50.0, 41.2), label="mongo driver", lw=1.7, label_dx=7.0, label_dy=0.2,
      color=TEAL_DARK)
arrow(ax, (83.5, 45.0), (83.5, 41.2), label="RestTemplate", lw=1.7, label_dx=8.0, label_dy=0.2,
      color=TEAL_DARK)

note(ax, 2.0, 3.0, 96.0,
     "Deployment-profile observations taken from the repository sources\n"
     "• The CORS allow-list contains only http://localhost:4200 and the refresh cookie is issued with secure = false,\n"
     "   which pins the current configuration to a local development profile.\n"
     "• JWT_SECRET, OPENROUTER_API_KEY and OPENROUTER_MODEL are supplied as environment properties and have no\n"
     "   defaults in application.properties, so the backend will not start without them.\n"
     "• MongoDB connectivity relies on the Spring Boot default localhost:27017 URI, because the explicit spring.data.mongodb.uri\n"
     "   line in application.properties is commented out; the database name is fixed to 'macrova' in MongoConfig.\n"
     "• No Dockerfile, container manifest or CI pipeline is present in the repository; the topology above therefore documents the\n"
     "   development profile rather than a production deployment descriptor.",
     accent=ORANGE, size=8.6)
save(fig, f"{OUT}/deployment-diagram.png")

# ---------------------------------------------------------------- DFD level 1
fig, ax = canvas(14.0, 9.2)
ax.text(50, 62.0, "Data Flow Diagram — Level 1 (functional decomposition)", ha="center",
        fontsize=12.8, fontweight="bold", color=INK)

C1, C2, C3 = 28.0, 52.0, 75.0


def proc(xc, y, h, num, name, lines, accent, w=21.0):
    x = xc - w / 2
    ax.add_patch(mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.1",
                 facecolor="#ffffff", edgecolor=BORDER_C, lw=1.2, zorder=2))
    ax.add_patch(mpatches.Rectangle((x, y + h - 3.4), w, 3.4, facecolor=accent, alpha=0.13,
                 edgecolor="none", zorder=2.2))
    ax.plot([x + 0.8, x + w - 0.8], [y + h, y + h], color=accent, lw=2.4, zorder=3)
    ax.text(xc, y + h - 1.7, f"{num}   {name}", ha="center", va="center",
            fontsize=9.2, fontweight="bold", color=INK, zorder=4)
    ax.text(xc, y + h - 4.6, "\n".join(lines), ha="center", va="top",
            fontsize=8.0, color=GREY, linespacing=1.45, zorder=4)


def store(xc, y, label, lines, accent, w=21.0, h=4.4):
    x = xc - w / 2
    ax.add_patch(mpatches.Rectangle((x, y), w, h, facecolor="#ffffff", edgecolor=BORDER_C,
                 lw=1.1, zorder=2))
    ax.plot([x + w - 2.0, x + w - 2.0], [y, y + h], color=BORDER_C, lw=1.0, zorder=2.4)
    ax.add_patch(mpatches.Rectangle((x, y), w, 2.9, facecolor=accent, alpha=0.14,
                 edgecolor="none", zorder=2.3))
    ax.text(x + 1.2, y + 1.45, label, ha="left", va="center", fontsize=8.6,
            fontweight="bold", color=INK, zorder=4)
    ax.text(xc, y - 1.9, lines, ha="center", va="top", fontsize=7.8, color=GREY, zorder=4)


# entities
ellipse(ax, 8.0, 46.0, 13.0, 11.0, "USER", ["account holder", "in a browser"])
ellipse(ax, 93.0, 46.0, 12.0, 11.0, "OPENROUTER", ["LLM inference", "provider"])

proc(C1, 50.0, 8.5, "1.0", "Identity & Session",
     ["register · BCrypt check", "JWT + refresh cookie"], TEAL)
proc(C2, 50.0, 8.5, "2.0", "Plan Construction",
     ["body metrics · TDEE", "goal · macros · activate"], BLUE)
proc(C3, 50.0, 8.5, "6.0", "AI Food Suggestion",
     ["prompt assembly", "JSON completion parse"], ORANGE)

store(C1, 41.0, "D1  users", "username · email · BCrypt hash", TEAL)
store(C2, 41.0, "D2  diet_plans", "metrics · targets · macros · status", BLUE)
store(C3, 41.0, "D4  ai_food_suggests", "name · calories · macros", ORANGE)

proc(C1, 25.0, 8.5, "3.0", "Dashboard", ["weekly aggregation", "goal % · weight chart"], BLUE)
proc(C2, 25.0, 8.5, "4.0", "Daily Macro Tracking", ["per-meal taken values", "weight · intake totals"], BLUE)
proc(C3, 25.0, 8.5, "5.0", "History & Review", ["plan history rows", "per-day stored entries"], TEAL)

store(C2, 18.4, "D3  diet_plan_tracks", "weight · intake · meal split", BLUE)

arrow(ax, (14.5, 49.0), (17.5, 51.5), label="credentials", lw=1.4, label_dx=-2.8, label_dy=2.4,
      label_size=7.8)
arrow(ax, (17.5, 54.5), (14.5, 52.0), color=GREY, lw=1.2,
      label="JWT", label_dx=3.0, label_dy=-2.8, label_size=7.8)
arrow(ax, (C1, 50.0), (C1, 45.0), label="user document", lw=1.4, label_dx=8.4, label_dy=0.1,
      color=TEAL, label_size=7.8)
arrow(ax, (C1 + 6, 45.0), (C1 + 6, 50.0), color=GREY, lw=1.1, ls="--",
      label="lookup by username", label_dx=10.2, label_dy=0.1, label_size=7.6)

arrow(ax, (C2, 50.0), (C2, 45.0), label="plan writes", lw=1.4, label_dx=6.4, label_dy=0.1,
      color=BLUE, label_size=7.8)
arrow(ax, (C2 + 6, 45.0), (C2 + 6, 50.0), color=GREY, lw=1.1, ls="--",
      label="pending plan", label_dx=8.2, label_dy=0.1, label_size=7.6)

arrow(ax, (C2, 41.0), (C2, 35.0), label="active plan header", lw=1.4, label_dx=10.4, label_dy=0.1,
      color=BLUE, label_size=7.8)
arrow(ax, (C3, 50.0), (C3, 45.0), color=GREY, lw=1.2, ls="--",
      label="addSuggestions()", label_dx=-10.4, label_dy=-1.6, label_size=7.6)
arrow(ax, (C3, 45.0), (C3, 50.0), color=ORANGE, lw=0.0)
arrow(ax, (86.0, 46.0), (C3 + 10.5, 53.0), label="chat completion", lw=1.4, label_dx=1.0,
      label_dy=2.6, label_size=7.8)
arrow(ax, (C3 + 10.5, 56.0), (86.0, 50.0), color=GREY, lw=1.2,
      label="JSON array", label_dx=2.0, label_dy=-2.4, label_size=7.8)

arrow(ax, (C1, 41.0), (C1, 35.0), color=GREY, lw=1.2, ls="--")
arrow(ax, (C2, 25.0), (C2, 22.9), lw=1.4, color=BLUE)
poly_arrow(ax, [(C2 - 10.5, 20.6), (C1 + 12.6, 20.6), (C1 + 12.6, 25.0)], color=GREY, lw=1.2,
           ls="--")
ax.text(C1 + 15.9, 21.9, "weekly tracks", fontsize=7.6, color=GREY)
poly_arrow(ax, [(C2 + 10.5, 28.0), (C3 - 10.5, 28.0)], color=TEAL, lw=1.3)
ax.text(C2 + 11.8, 29.4, "plan + day projections", fontsize=7.6, color=GREY)

note(ax, 2.0, 1.0, 96.0,
     "Solid arrows carry data written by a process; dashed arrows are read paths.\n"
     "1.0 UserController · AuthenticationFilter · CustomAuthenticationManager · JWTTokenService · UserService.\n"
     "2.0 DietPlanFormController / DietPlanFormService.    3.0 and 4.0 DietPlanController / DietPlanService.\n"
     "5.0 history endpoints of DietPlanController backed by projection queries in the two repositories.\n"
     "6.0 AIFoodSuggestController / AIFoodSuggestService through the OpenRouterLLMService adapter. Data store D4 is\n"
     "      written only by addSuggestions(), which no controller calls, so suggestions reach the browser unpersisted.",
     accent=ORANGE, size=8.0)
save(fig, f"{OUT}/dfd-level-1.png")
