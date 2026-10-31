"""Appendices A to D."""

from __future__ import annotations

from reportlab.platypus import Paragraph, Spacer

import theme as T
from theme import S, bullets, chapter, code_block, h2, h3, note_box, numbered, prelim, table, table_caption


def _tab(label, caption, headers, rows, widths, font_size=7.0):
    return [table_caption(caption, label=label)] + table(
        headers, rows, widths=widths, caption=None, font_size=font_size)


def build():
    st = []

    # ------------------------------------------------------------------
    st += prelim("APPENDIX A \u2014 REST API REFERENCE", toc=True, level=0)
    st += [T.body(
        "Every endpoint is served from the application root on port 8080 in development. The "
        "client addresses them through a <font name='Mono' size='8'>/api</font> prefix that the "
        "development proxy strips. Requests and responses are "
        "<font name='Mono' size='8'>application/json</font> except where stated. With the two "
        "stated exceptions, every endpoint requires "
        "<font name='Mono' size='8'>Authorization: Bearer &lt;access token&gt;</font>.")]
    st += _tab("Table A.1", "User and session endpoints",
               ["Method and path", "Auth", "Request", "Response"],
               [["POST /authenticate", "No", "{username, password}",
                 "200 with Set-Cookie Refresh-Token; 401 on failure"],
                ["POST /user/register", "No", "{username, email, password}",
                 "200 with the user document minus the password; 400 on duplicate"],
                ["POST /user/refresh", "Cookie", "None (cookie is read)",
                 "200 {accessToken}; 401 if the cookie is absent or invalid"],
                ["POST /user/logout", "Yes", "None",
                 "200 with an empty Refresh-Token cookie and max-age 0"],
                ["GET /user/username", "Yes", "None", "200 {username}"],
                ["POST /user/refresh (expired token)", "Cookie",
                 "None", "401 'Access token expired' or 'JWT verification failed' from the "
                         "exception filter"]],
               [1.7, 0.55, 1.6, 2.55])
    st += _tab("Table A.2", "Diet-plan and tracking endpoints",
               ["Method and path", "Request", "Response"],
               [["GET /diet-plan", "None", "200 with the active plan; 404 if none"],
                ["GET /diet-plan/{id}", "Path: plan id", "200 with the plan; 404 if absent or "
                                                          "foreign"],
                ["GET /diet-plan/all", "None", "200 with every plan of the user"],
                ["GET /diet-plan/history", "None",
                 "200 with projections {id, title, plan, weight, targetWeight, duration, "
                 "active}, newest first"],
                ["GET /diet-plan/past-plan", "None", "200 with the newest projection; 404 if "
                                                     "none"],
                ["GET /diet-plan/active-plans", "None", "200 boolean"],
                ["GET /diet-plan/status", "None", "200 boolean; deactivates the plan when the "
                                                  "duration is exceeded"],
                ["POST /diet-plan", "Plan body", "200 with the stored plan"],
                ["PUT /diet-plan/update", "Plan body", "200 with a new plan document"],
                ["POST /diet-plan/tdee", "Body-metrics body", "200 with the expenditure "
                                                              "preview; nothing persisted"],
                ["GET /diet-plan/track/{trackId}", "Path: track id", "200 with the document; "
                                                                     "404 if absent"],
                ["GET /diet-plan/track/plan/{planId}", "Path: plan id",
                 "200 with today's document, created if missing; 404 if the plan is absent or "
                 "foreign"],
                ["POST /diet-plan/add-weight/{planId}", "{weight}", "200 with the recomputed "
                                                                    "document"],
                ["POST /diet-plan/{category}/{planId}", "Macros body {protein, fat, carbs}",
                 "200 with the updated document; 400 'Invalid macro category'"],
                ["GET /diet-plan/meal-kcal/{planId}", "Path: plan id",
                 "200 with the four meal allocations; 404 'No macros found.'"],
                ["GET /diet-plan/metrics", "None", "200 with MetricsDTO; 404 if no active plan"],
                ["GET /diet-plan/overview/{planId}", "Path: plan id",
                 "200 with the day projections, newest first"]],
               [2.0, 1.65, 2.75], font_size=6.9)
    st += _tab("Table A.3", "Suggestion endpoint and error mapping",
               ["Method and path / code", "Request or cause", "Response"],
               [["POST /ai-food-suggest", "{mealFilter, foodFilter, cuisineFilter}",
                 "200 with a list of five food objects"],
                ["400 Bad Request", "Unsafe target weight, duration outside the window, invalid "
                                    "macro category, duplicate registration, unparsable body",
                 "{\"error\":[\"message\"]}"],
                ["401 Unauthorized", "Expired or unverifiable token; failed credential check",
                 "{\"error\":[\"message\"]} for handlers; plain text from the filters"],
                ["403 Forbidden", "No bearer token supplied for a protected path",
                 "Empty body from the default entry point"],
                ["404 Not Found", "Absent document, or a document owned by another user",
                 "{\"error\":[\"message\"]}"],
                ["410 Gone", "Model response could not be parsed into the expected schema",
                 "{\"error\":[\"message\"]}"]],
               [1.55, 2.75, 2.1], font_size=6.9)

    # ------------------------------------------------------------------
    st += prelim("APPENDIX B \u2014 INSTALLATION AND USER MANUAL", toc=True, level=0)
    st += [h2("B.1 Prerequisites")]
    st += bullets([
        "JDK 21 and the bundled Maven wrapper (no separate Maven installation is needed).",
        "Node.js 18.19+ or 20.11+ or 22.x with npm 10, as required by Angular 19.",
        "MongoDB reachable on port 27017 with permission to create the database "
        "<font name='Mono' size='8'>macrova</font>.",
        "A signing secret for the JWT (any long random string) and, optionally, an OpenRouter "
        "API key and model identifier.",
    ])
    st += [h2("B.2 Back-End Setup")]
    st += code_block(
        """# 1. environment (Linux/macOS syntax)
export JWT_SECRET="<a long random string>"
export OPENROUTER_API_KEY="<provider key>"      # optional
export OPENROUTER_MODEL="<model slug>"          # optional

# 2. build and test
cd backend
./mvnw clean verify          # runs the context-load test

# 3. run
./mvnw spring-boot:run       # serves http://localhost:8080

# 4. smoke check (expect 403 without a token)
curl -i http://localhost:8080/diet-plan/metrics""",
        label="Listing B.1", caption="Back-end build and start sequence")
    st += [T.body(
        "The database is created implicitly on the first registration. If the MongoDB instance "
        "is not on the default port, uncomment and edit "
        "<font name='Mono' size='8'>spring.data.mongodb.uri</font> in "
        "<font name='Mono' size='8'>backend/src/main/resources/application.properties</font>; the "
        "database name itself is set in "
        "<font name='Mono' size='8'>MongoConfig</font> and does not come from the URI.")]
    st += [h2("B.3 Front-End Setup")]
    st += code_block(
        """cd frontend
npm install
npm start          # ng serve --proxy-config proxy.conf.json, http://localhost:4200
npm run build      # production bundle in dist/macrova-ui""",
        label="Listing B.2", caption="Client installation and development server")
    st += [T.body(
        "The development server must be started through the proxy configuration, otherwise the "
        "browser sends requests to port 4200 and the refresh cookie is not treated as "
        "first-party. The proxy rewrites <font name='Mono' size='8'>/api</font> to the service "
        "root on port 8080.")]
    st += [h2("B.4 First-Run Checklist")]
    st += numbered([
        "Start MongoDB, then the back end, then the client.",
        "Open <font name='Mono' size='8'>http://localhost:4200</font>; the log-in screen is "
        "shown and the header is hidden.",
        "Register an account; the client navigates to the log-in screen on success.",
        "Log in; the router redirects to the dashboard, which detects that no plan is active "
        "and offers the plan form.",
        "Create a plan within the duration window shown beneath the field.",
        "Confirm that the dashboard shows a day-1 streak, the calorie target and an empty "
        "seven-day series.",
        "Open the progress screen, enter one meal and confirm that the daily totals change.",
        "Record a new weight and confirm that the target and macro figures change with it.",
        "Request suggestions from the meals screen; if no key is configured, confirm that the "
        "error state is shown rather than a partial list.",
        "Sign out and confirm that a guarded route redirects to the log-in screen.",
    ])
    st += [h2("B.5 Operating Notes")]
    st += bullets([
        "The service is stateless; it may be restarted at any time without losing data, but "
        "restarting invalidates nothing because tokens are self-contained and signed with the "
        "same secret.",
        "Changing <font name='Mono' size='8'>JWT_SECRET</font> invalidates every issued token, "
        "which is the supported way to force a global sign-out.",
        "A day&#39;s tracking document is created the first time the dashboard or progress "
        "screen is opened on that date; a user who does not open the application on a day will "
        "have no document for it, and the chart will therefore contain a gap.",
        "The suggestion feature degrades gracefully: without a key, the endpoint returns the "
        "provider error and the screen displays it; no other feature is affected.",
    ])

    # ------------------------------------------------------------------
    st += prelim("APPENDIX C \u2014 SAMPLE DOCUMENTS", toc=True, level=0)
    st += [T.body(
        "The three documents below were exported from a verification database after the "
        "scenario of Table 7.3, case A, had been recorded for one day. They illustrate the four "
        "nested levels of the tracking document and the way in which targets and recorded "
        "values coexist.")]
    st += [h3("C.1 users")]
    st += code_block(
        """{
  "_id": { "$oid": "66f0a1c4e13b4a2f9c7d5101" },
  "username": "karthick",
  "email": "karthick@example.edu",
  "password": "$2a$10$Qm5t1s0hZ8kYv2rWc0lJ3e9Xb1nS7pPd4Tg6uHy2Vf5Rk8Lm3Nq0S",
  "_class": "org.karthick.macrova.user.entity.User"
}""",
        label="Listing C.1", caption="Sample users document (digest truncated for the reader)")
    st += [h3("C.2 diet_plans")]
    st += code_block(
        """{
  "_id": { "$oid": "66f0a2d7e13b4a2f9c7d5102" },
  "title": "Semester cut",
  "plan": "WEIGHT_LOSS",
  "age": 24,
  "gender": "MALE",
  "height": 178.0,
  "weight": 76.5,
  "todayWeight": 75.8,
  "goal": "MODERATE",
  "targetWeight": 70.0,
  "duration": 60,
  "activity": "MODERATE",
  "userId": "66f0a1c4e13b4a2f9c7d5101",
  "active": true,
  "createdAt": "2025-09-20",
  "_class": "org.karthick.macrova.dietplan.entity.DietPlan"
}""",
        label="Listing C.2", caption="Sample diet_plans document after a weight update")
    st += [h3("C.3 diet_plan_tracks")]
    st += code_block(
        """{
  "_id": { "$oid": "66f0a2e1e13b4a2f9c7d5103" },
  "weight": 75.8,
  "tdee": 2721.03,
  "intake":   { "taken": 1292.0, "total": 2200.0 },
  "protein":  { "taken": 96.0,  "total": 165.0 },
  "carbs":    { "taken": 128.0, "total": 220.0 },
  "fat":      { "taken": 44.0,  "total": 73.0 },
  "mealKcal": {
    "breakfast": { "protein": { "taken": 32.0, "total": 50.0 },
                   "fat":     { "taken": 14.0, "total": 22.0 },
                   "carbs":   { "taken": 48.0, "total": 66.0 } },
    "lunch":     { "protein": { "taken": 40.0, "total": 50.0 },
                   "fat":     { "taken": 18.0, "total": 22.0 },
                   "carbs":   { "taken": 50.0, "total": 66.0 } },
    "snack":     { "protein": { "taken": 24.0, "total": 25.0 },
                   "fat":     { "taken": 12.0, "total": 11.0 },
                   "carbs":   { "taken": 30.0, "total": 33.0 } },
    "dinner":    { "protein": { "taken": 0.0,  "total": 41.0 },
                   "fat":     { "taken": 0.0,  "total": 18.0 },
                   "carbs":   { "taken": 0.0,  "total": 55.0 } }
  },
  "dayCount": 4,
  "createdAt": "2025-09-23",
  "dietPlanId": "66f0a2d7e13b4a2f9c7d5102",
  "_class": "org.karthick.macrova.dietplan.entity.DietPlanTrack"
}""",
        label="Listing C.3", caption="Sample diet_plan_tracks document for the fourth day")
    st += [T.body(
        "Three properties of the sample deserve attention. The recorded calories are exactly "
        "4 \u00d7 96 + 9 \u00d7 44 + 4 \u00d7 128 = 1,292 kcal, a value the service computed "
        "from the meal entries rather than one supplied by the client. The targets were "
        "recomputed when the weight fell from 76.5 kg to 75.8 kg, which is why expenditure is "
        "2,721.03 kcal against 2,731.88 kcal on the previous day. And the ratio of recorded to "
        "target energy is 59 per cent, which is the figure the dashboard bar displays for that "
        "day.")]

    # ------------------------------------------------------------------
    st += prelim("APPENDIX D \u2014 GLOSSARY", toc=True, level=0)
    st += [table_caption("Glossary of terms used throughout the report", label="Table D.1")]
    st += table(
        ["Term", "Definition as used in this report"],
        [["Access token", "A signed JSON Web Token with a sixty-minute lifetime, held in memory "
                          "by the client and sent in the Authorization header."],
         ["Activity multiplier", "The factor by which basal metabolic rate is multiplied to "
                                 "obtain total daily energy expenditure; one of 1.2, 1.375, "
                                 "1.55, 1.725 or 1.9 in this implementation."],
         ["Basal metabolic rate (BMR)", "Energy expended at complete rest, estimated here with "
                                        "the Mifflin\u2013St Jeor equation."],
         ["Body-mass index (BMI)", "Mass in kilograms divided by the square of stature in "
                                   "metres; used to validate a target weight."],
         ["BCrypt", "An adaptive password-hashing function with a per-password salt and a "
                    "configurable cost; the only form in which a password is stored."],
         ["Daily deficit / surplus target", "The calorie figure derived from expenditure and the "
                                            "goal; stored as the <i>total</i> of the "
                                            "<i>intake</i> value object."],
         ["Day count", "The number of days between a plan's creation date and the tracked date, "
                       "inclusive; the streak denominator."],
         ["Document (MongoDB)", "A BSON object stored in a collection; the unit of persistence "
                                "for every entity here."],
         ["Embedded value object", "A class persisted inside its parent document rather than in "
                                   "its own collection; Calories, Macros and MealKcal here."],
         ["Goal", "The aggressiveness of the plan, one of mild (15), moderate (20) or aggressive "
                  "(25) per cent."],
         ["HMAC512", "The keyed hash used to sign tokens; the signature covers header and "
                     "payload."],
         ["Interceptor (Angular)", "A function that transforms outgoing HTTP requests; two are "
                                   "used here, for URL prefixing and for token attachment."],
         ["JWT", "JSON Web Token, RFC 7519."],
         ["Macronutrient", "Protein, fat or carbohydrate; stored as grams and converted to "
                           "kilocalories with 4, 9 and 4 kcal per gram."],
         ["Meal split", "The apportionment of each daily macro target across four meals as 30, "
                        "30, 15 and 25 per cent."],
         ["Metrics resource", "The flat projection consumed by the dashboard, containing the "
                              "title, percentage taken, day, duration, weight, targets and the "
                              "seven-day series."],
         ["Owner identifier", "The string form of the authenticated user's ObjectId, stamped on "
                              "every plan and used in every ownership predicate."],
         ["Projection (MongoDB)", "A query that returns a subset of fields; used by the history "
                                  "and overview queries."],
         ["Refresh token", "A signed token with a twenty-four-hour lifetime, delivered in an "
                           "HttpOnly cookie and used only to mint access tokens."],
         ["Signal (Angular)", "A reactive value container used by the client to hold loaded "
                              "resources."],
         ["TDEE", "Total daily energy expenditure; BMR multiplied by the activity multiplier."],
         ["Track (document)", "One day of one plan: its weight, targets, recorded values and "
                              "meal breakdown."],
         ["Two-tier architecture", "A client tier and a server tier, where the server also hosts "
                                   "the data access layer; used here because no separate "
                                   "middleware exists."]],
        widths=[1.6, 4.9],
        font_size=7.0)
    return st
