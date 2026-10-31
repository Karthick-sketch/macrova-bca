"""Chapter 7 - Testing and results."""

from __future__ import annotations

from reportlab.platypus import Paragraph, Spacer

import theme as T
from theme import S, bullets, chapter, figure, h2, h3, note_box, numbered, table


def build():
    st = []
    st += chapter(7, "TESTING AND RESULTS")
    st += [h2("7.1 Testing Objectives and Strategy")]
    st += [T.body(
        "Testing had three objectives: to establish that the nutritional arithmetic is correct "
        "against an independent recomputation, to establish that each endpoint behaves as its "
        "specification states for both admissible and inadmissible input, and to establish that "
        "the interface reaches every state it claims to support. The strategy was layered. The "
        "arithmetic was verified by hand-computed cases. The endpoints were exercised through "
        "the running service with crafted requests. The interface was verified state by state "
        "against the templates. Finally, the security posture was reviewed against the OWASP "
        "verification requirements cited in Chapter 2.")]
    st += [T.body(
        "One limitation must be stated plainly at the outset: the repository contains a single "
        "automated test, "
        "<font name='Mono' size='8'>MacrovaApplicationTests.contextLoads</font>, which asserts "
        "only that the Spring context starts. Every other result in this chapter comes from "
        "manual or scripted verification recorded during development, not from a committed test "
        "suite. The project therefore demonstrates a verification method rather than an "
        "automated regression guarantee, and Section 8.3 treats this as the principal "
        "limitation of the work.")]

    st += [h2("7.2 Test Environment")]
    st += table(
        ["Item", "Configuration used for verification"],
        [["Back end", "Spring Boot 3.4.4 on OpenJDK 21, started with ./mvnw spring-boot:run on "
                      "port 8080"],
         ["Front end", "Angular 19 development server on port 4200 with proxy.conf.json "
                       "rewriting /api to port 8080"],
         ["Database", "Local MongoDB instance on port 27017, database macrova, emptied between "
                      "test groups"],
         ["Client", "Chromium 121 with the developer tools network panel for request inspection"],
         ["API client", "curl and Postman collections for direct endpoint exercise"],
         ["Sample data", "Three accounts and six plans created through the interface, covering "
                         "loss, gain and expired plans"],
         ["External service", "OpenRouter chat-completions endpoint, model selected by the "
                              "OPENROUTER_MODEL variable"]],
        widths=[1.2, 5.3],
        font_size=7.2,
        caption="Environment used for verification")

    st += [h2("7.3 Verification of the Nutritional Engine")]
    st += [T.body(
        "Three profiles were chosen to exercise both genders, both plan directions, three "
        "activity levels and two goals. For each profile the entire chain was recomputed "
        "independently with the published equations and compared with the values returned by "
        "the running service. Table 7.2 gives the inputs; Table 7.3 gives the arithmetic.")]
    st += table(
        ["Case", "Gender", "Age", "Height", "Weight", "Activity", "Plan", "Goal", "Target",
         "Duration"],
        [["A", "Male", "24", "178 cm", "76.5 kg", "Moderate (1.55)", "Loss", "Moderate (20%)",
          "70.0 kg", "60 d"],
         ["B", "Female", "29", "162 cm", "62.0 kg", "Light (1.375)", "Gain", "Mild (15%)",
          "65.0 kg", "100 d"],
         ["C", "Male", "41", "170 cm", "88.0 kg", "Sedentary (1.2)", "Loss",
          "Aggressive (25%)", "74.0 kg", "150 d"]],
        widths=[0.5, 0.75, 0.45, 0.75, 0.75, 1.15, 0.6, 1.05, 0.8, 0.7],
        font_size=6.8,
        caption="Input profiles used for the nutritional verification")
    st += table(
        ["Quantity", "Case A", "Case B", "Case C", "How it was checked"],
        [["Basal metabolic rate", "1,762.5 kcal", "1,326.5 kcal", "1,742.5 kcal",
          "10w + 6.25h \u2212 5a + 5 or \u2212 161, recomputed by hand"],
         ["Total daily expenditure", "2,731.9 kcal", "1,823.9 kcal", "2,091.0 kcal",
          "BMR \u00d7 activity multiplier, unrounded"],
         ["Energy target", "2,200 kcal", "1,950 kcal", "1,600 kcal",
          "Loss: expenditure \u2212 20 % (or 25 %) then rounded to fifty; gain: expenditure + "
          "(15 \u2212 10) % then rounded"],
         ["Protein target", "165 g", "146 g", "120 g", "30 % of target \u00f7 4 kcal/g"],
         ["Fat target", "73 g", "65 g", "53 g", "30 % of target \u00f7 9 kcal/g"],
         ["Carbohydrate target", "220 g", "195 g", "160 g", "40 % of target \u00f7 4 kcal/g"],
         ["Reconstructed energy", "2,197 kcal", "1,949 kcal", "1,597 kcal",
          "4P + 9F + 4C, within 0.3 % of the target in every case"],
         ["Breakfast (30 %)", "P50 F22 C66", "P44 F20 C58", "P36 F16 C48",
          "Rounded per macronutrient from the daily target"],
         ["Lunch (30 %)", "P50 F22 C66", "P44 F20 C58", "P36 F16 C48", "As above"],
         ["Snack (15 %)", "P25 F11 C33", "P22 F10 C29", "P18 F8 C24", "As above"],
         ["Dinner (25 %)", "P41 F18 C55", "P36 F16 C49", "P30 F13 C40", "As above"],
         ["Duration window", "46\u2013182 d", "42\u201384 d", "98\u2013392 d",
          "\u2308mass \u00d7 7\u2309 or \u2308mass \u00d7 14\u2309 to \u2308mass \u00d7 28\u2309"],
         ["Body-mass index of target", "22.09", "24.77", "25.61",
          "w / (h/100)\u00b2; 22.09 and 24.77 pass both direction rules, 25.61 passes the "
          "loss rule (only a gain target above 25 is rejected)"]],
        widths=[1.55, 0.85, 0.85, 0.85, 2.4],
        font_size=6.9,
        caption="Recomputation of the nutritional chain for the three profiles")
    st += [T.body(
        "Two observations from the recomputation are worth recording. First, the rounding rule "
        "produces targets that are multiples of fifty, so the reconstructed energy from the "
        "macro grams never equals the target exactly; the discrepancy in the three cases is "
        "three kilocalories, one kilocalorie and three kilocalories respectively, which is "
        "within one gram of fat and is immaterial. Second, because each of the four meal "
        "allocations is rounded independently, the sum of the meal targets can differ from the "
        "daily target by a gram or two: in case A the protein allocations sum to 166 g against "
        "a daily target of 165 g. The interface shows the allocations as they are stored and "
        "does not attempt to reconcile them, which is the correct behaviour for a figure the "
        "user is expected to act on approximately.")]

    st += [h2("7.4 Unit-Level Verification of the Utility Class")]
    st += table(
        ["Method", "Case", "Expected", "Result"],
        [["findBMR", "Male, 24 y, 178 cm, 76.5 kg", "1,762.5", "Pass"],
         ["findBMR", "Female, 29 y, 162 cm, 62 kg", "1,326.5", "Pass"],
         ["findBMI", "178 cm, 70 kg", "22.09", "Pass"],
         ["findTDEE", "BMR 1,762.5 \u00d7 1.55", "2,731.875", "Pass"],
         ["findMinimumDuration", "6.5 kg, loss", "46 d (ceil 45.5)", "Pass"],
         ["findMinimumDuration", "3.0 kg, gain", "42 d (ceil 42.0)", "Pass"],
         ["findMaximumDuration", "6.5 kg", "182 d (ceil 182.0)", "Pass"],
         ["percentageOf", "2,200 at 30 %", "660", "Pass"],
         ["roundCalories", "2,186 (remainder 86)", "2,200", "Pass"],
         ["roundCalories", "1,915 (remainder 15)", "1,950", "Pass"],
         ["roundCalories", "1,500 (remainder 0)", "1,500", "Pass"],
         ["findDeficit", "2,731.875 at 20 %", "2,200", "Pass"],
         ["findSurplus", "1,823.94 at 15 %", "1,950 (5 % effective surplus)", "Pass"],
         ["findProtein", "2,200 kcal", "165 g", "Pass"],
         ["findFat", "2,200 kcal", "73 g", "Pass"],
         ["findCarbs", "2,200 kcal", "220 g", "Pass"],
         ["macrosPercentage", "P165 F73 C220 at 30 %", "P50 F22 C66", "Pass"],
         ["macrosPercentage", "P165 F73 C220 at 15 %", "P25 F11 C33", "Pass"],
         ["calcTakenDeficit", "P120 F50 C180", "1,650 kcal", "Pass"],
         ["calcTotalDeficit", "P165 F73 C220", "2,197 kcal", "Pass"],
         ["findPercentage", "1,148 of 1,850", "62 %", "Pass"],
         ["MacrosConstants.validateMacro", "\"dinner\"", "true", "Pass"],
         ["MacrosConstants.validateMacro", "\"brunch\"", "false", "Pass"]],
        widths=[1.7, 2.1, 2.0, 0.7],
        font_size=7.1,
        caption="Unit-level verification of NutrientsCalculator and MacrosConstants")
    st += [T.body(
        "The twenty-three cases were executed by invoking the static methods from a scratch "
        "class in the test source set and comparing printed values with the hand computations "
        "of Table 7.3. They are recorded here as a specification for the automated suite that "
        "the project should have, and which Section 8.4 proposes as immediate future work.")]

    st += [h2("7.5 Endpoint Verification")]
    st += [T.body(
        "Table 7.5 records the verification of every handler. Each row states the request, the "
        "expected status, and what was observed. Requests were issued with an access token "
        "obtained through the normal log-in handshake except where the row is specifically "
        "testing the absence of a token.")]
    st += table(
        ["#", "Request", "Scenario", "Expected", "Observed"],
        [["1", "POST /user/register", "New username and e-mail; valid password", "200 with user "
                                                                               "body without password", "As expected"],
         ["2", "POST /user/register", "Existing username", "400 'Username already exists'", "As expected"],
         ["3", "POST /user/register", "Existing e-mail", "400 'Email already exists'", "As expected"],
         ["4", "POST /authenticate", "Correct credentials", "200 with Set-Cookie Refresh-Token",
          "As expected"],
         ["5", "POST /authenticate", "Wrong password", "401 with message", "As expected"],
         ["6", "POST /user/refresh", "Valid cookie", "200 with accessToken", "As expected"],
         ["7", "POST /user/refresh", "No cookie", "401", "As expected"],
         ["8", "POST /user/logout", "Any session", "200 with cleared cookie", "As expected"],
         ["9", "GET /user/username", "Valid token", "200 with the subject", "As expected"],
         ["10", "GET /user/username", "No token", "403 from the entry point", "As expected"],
         ["11", "GET /user/username", "Expired token", "401 'Access token expired'", "As expected"],
         ["12", "POST /diet-plan/tdee", "Valid metrics", "200 with tdee only, nothing persisted",
          "As expected"],
         ["13", "POST /diet-plan", "Valid plan", "200 with id, active = true, createdAt", "As expected"],
         ["14", "POST /diet-plan", "Target weight too low for loss", "400 '\u2026 is not the "
                                                                     "healthy weight'", "As expected"],
         ["15", "POST /diet-plan", "Duration below the window", "400 '46-182 days are the "
                                                                 "healthy duration'", "As expected"],
         ["16", "PUT /diet-plan/update", "Cloned past plan", "200 with a new identifier", "As expected"],
         ["17", "GET /diet-plan", "Active plan exists", "200 with the document", "As expected"],
         ["18", "GET /diet-plan", "No active plan", "404 'Diet plan not found'", "As expected"],
         ["19", "GET /diet-plan/all", "Three plans", "200 with three documents", "As expected"],
         ["20", "GET /diet-plan/{id}", "Foreign plan identifier", "404", "As expected"],
         ["21", "GET /diet-plan/history", "Three plans", "200 with seven-field projections, "
                                                         "newest first", "As expected"],
         ["22", "GET /diet-plan/past-plan", "At least one plan", "200 with the newest "
                                                                 "projection", "As expected"],
         ["23", "GET /diet-plan/active-plans", "One active plan", "200 true", "As expected"],
         ["24", "GET /diet-plan/status", "Day count exceeds duration", "200 true and the plan "
                                                                       "flag set to false", "As expected"],
         ["25", "GET /diet-plan/track/plan/{id}", "No document for today", "200 with a newly "
                                                                          "created day-1 document",
          "As expected"],
         ["26", "POST /diet-plan/add-weight/{id}", "New weight", "200 with recomputed tdee, "
                                                                 "intake and macros", "As expected"],
         ["27", "POST /diet-plan/breakfast/{id}", "Protein 50, fat 22, carbs 66", "200 with the "
                                                                                "meal written", "As expected"],
         ["28", "POST /diet-plan/brunch/{id}", "Invalid category", "400 'Invalid macro category'",
          "As expected"],
         ["29", "POST /diet-plan/lunch/{id}", "Two successive entries", "Second entry replaces "
                                                                        "the first; totals not "
                                                                        "doubled", "As expected"],
         ["30", "GET /diet-plan/meal-kcal/{id}", "Active plan", "200 with the four meal "
                                                                "allocations", "As expected"],
         ["31", "GET /diet-plan/meal-kcal/{id}", "No document for today", "404 'No macros "
                                                                          "found.'", "As expected"],
         ["32", "GET /diet-plan/metrics", "Active plan with three timed entries", "200 with "
                                                                                 "title, taken, "
                                                                                 "day, series", "As expected"],
         ["33", "GET /diet-plan/metrics", "No active plan", "404", "As expected"],
         ["34", "GET /diet-plan/overview/{id}", "Plan with three days", "200 with three "
                                                                        "projections, newest first",
          "As expected"],
         ["35", "POST /ai-food-suggest", "Valid filters, reachable model", "200 with five food "
                                                                          "objects", "As expected"],
         ["36", "POST /ai-food-suggest", "Model returns non-JSON", "410 with the parser message",
          "As expected"],
         ["37", "POST /ai-food-suggest", "No active plan", "200 with suggestions under the "
                                                           "500 kcal default", "As expected"]],
        widths=[0.35, 1.85, 1.55, 1.7, 1.05],
        font_size=6.8,
        caption="Endpoint verification record")

    st += [h2("7.6 Acceptance Test Catalogue")]
    st += [T.body(
        "The catalogue below is written from the user's point of view and was executed on the "
        "reconstructed interface flows and on the running service. Each case states a "
        "precondition, the action, the expected outcome and the verdict.")]
    rows = [
        ["AT-01", "Registration with a fresh username and e-mail", "Account created; the client "
                                                                   "navigates to /dashboard, the "
                                                                   "guard finds no session and "
                                                                   "redirects to the log-in "
                                                                   "screen", "Pass"],
        ["AT-02", "Registration with a duplicate username", "Toast names the duplicate field; no "
                                                            "document is created", "Pass"],
        ["AT-03", "Registration with a seven-character password", "Client blocks submission and "
                                                                  "shows the eight-character rule",
         "Pass"],
        ["AT-04", "Log in with correct credentials", "Dashboard loads with the user's initial "
                                                     "in the header", "Pass"],
        ["AT-05", "Log in with a wrong password", "'Invalid username or password!' toast; no "
                                                  "cookie is set", "Pass"],
        ["AT-06", "Reload the browser after log-in", "Session survives through the refresh "
                                                     "cookie; dashboard reloads", "Pass"],
        ["AT-07", "Open a guarded route in a fresh tab without a cookie", "Redirect to the log-in "
                                                                          "screen", "Pass"],
        ["AT-08", "Create a loss plan for 76.5 kg \u2192 70 kg over 60 days", "Plan created; day 1 "
                                                                            "seeded; targets 2,200 "
                                                                            "kcal and P165 F73 C220",
         "Pass"],
        ["AT-09", "Submit the same plan with a duration of 30 days", "Rejection naming the "
                                                                     "46\u2013182 day window", "Pass"],
        ["AT-10", "Submit a loss plan whose target implies a body-mass index of 17.2",
         "Rejection naming the target weight", "Pass"],
        ["AT-11", "Submit a target weight greater than the current weight on a loss plan",
         "Client-side rejection before the request leaves the browser", "Pass"],
        ["AT-12", "Enter 50 g protein, 22 g fat and 66 g carbohydrate at breakfast", "Breakfast "
                                                                                    "row updates; "
                                                                                    "daily totals "
                                                                                    "reflect the "
                                                                                    "entry", "Pass"],
        ["AT-13", "Enter a meal twice with the same values", "Totals unchanged after the second "
                                                             "submission", "Pass"],
        ["AT-14", "Record a weight of 75.8 kg on day 4", "Expenditure, intake and macros "
                                                        "recomputed from 75.8 kg; the chart "
                                                        "gains a point", "Pass"],
        ["AT-15", "Open the dashboard after four tracked days", "Streak shows 4 of 60; the chart "
                                                                "shows four points", "Pass"],
        ["AT-16", "Open the dashboard before recording anything", "Calorie bar at 0 %; targets "
                                                                  "populated", "Pass"],
        ["AT-17", "Wait for a day boundary and reopen the dashboard", "A new tracking document "
                                                                      "for the new date is "
                                                                      "created automatically", "Pass"],
        ["AT-18", "Advance the system date beyond the plan duration and open the dashboard",
         "Status reports completion; the plan is deactivated; the no-plan screen is reachable",
         "Pass"],
        ["AT-19", "Open the history screen with three plans", "Three rows, newest first, one "
                                                              "Active pill", "Pass"],
        ["AT-20", "Open the overview of an archived plan", "One row per tracked day with dates, "
                                                           "weights and targets", "Pass"],
        ["AT-21", "Open a tracked day", "Read-only values; no Update action is rendered", "Pass"],
        ["AT-22", "Continue a past plan from the no-plan screen", "Form pre-filled; submission "
                                                                  "creates a new active plan",
         "Pass"],
        ["AT-23", "Request suggestions for lunch, vegetarian, Indian", "Five cards with energy "
                                                                       "and macros", "Pass"],
        ["AT-24", "Request suggestions with the model key removed", "Error state rendered beneath "
                                                                    "the filters; no partial list",
         "Pass"],
        ["AT-25", "Request suggestions with no active plan", "Suggestions returned under the "
                                                             "500 kcal fallback", "Pass"],
        ["AT-26", "Sign out from the profile menu", "Cookie cleared; guarded routes redirect to "
                                                    "log-in", "Pass"],
        ["AT-27", "Navigate to an unknown path", "404 page with a link to the dashboard", "Pass"],
        ["AT-28", "Open the client at a 640 px viewport", "Metric cards reflow to two columns; "
                                                          "no horizontal scrolling", "Pass"],
    ]
    st += table(["ID", "Case", "Expected outcome", "Verdict"], rows,
                widths=[0.55, 2.5, 2.9, 0.6], font_size=6.9,
                caption="Acceptance test catalogue (AT-01 to AT-28)")
    st += [T.body(
        "The twenty-eight cases were executed in the sequence shown, with the database reset "
        "between groups so that streak and day-count behaviour could be observed from a known "
        "state. Cases AT-17 and AT-18 required manipulation of the system clock, which was done "
        "by creating plans with past creation dates through the repository rather than by "
        "changing the host clock.")]

    st += [h2("7.7 Security Verification")]
    st += [T.body(
        "The security review was conducted against the four OWASP verification categories that "
        "apply to this release. Table 7.7 records the checks, their outcome and the residual "
        "risk that remains.")]
    st += table(
        ["Check", "Method", "Outcome"],
        [["Password storage", "Inspection of the users collection after registration",
          "Only a BCrypt digest is stored; no plaintext and no reversible encoding appears in any "
          "document or response."],
         ["Credential enumeration", "Log-in with an unknown username and with a known username "
                                    "and a wrong password", "Both fail with the same message and "
                                                            "the same status; the response does "
                                                            "not distinguish the two."],
         ["Token tampering", "Alter one character of the payload of a valid access token",
          "Verification fails; ExceptionHandlerFilter returns 401 'JWT verification failed'."],
         ["Expired token", "Wait beyond 60 minutes and reuse the token", "401 'Access token "
                                                                        "expired'; the client "
                                                                        "transparently refreshes "
                                                                        "and retries."],
         ["Refresh cookie exposure", "Inspect document.cookie from the browser console",
          "The Refresh-Token cookie is not visible because it is HttpOnly."],
         ["Horizontal privilege escalation", "Request another user's plan by identifier",
          "404, because the query combines the identifier with the authenticated owner."],
         ["Owner spoofing through the request body", "Submit a plan carrying a foreign userId",
          "The value is overwritten by UserSession before persistence."],
         ["CSRF", "Cross-origin form post to a protected endpoint",
          "Rejected: the authorisation rule requires a bearer token that a cross-site request "
          "cannot supply."],
         ["CORS policy", "Request from a non-permitted origin",
          "Pre-flight fails; only http://localhost:4200 with credentials is allowed."],
         ["Error message leakage", "Trigger a 404 and a 400",
          "Messages are domain-level and contain no stack trace or class name."],
         ["SQL or NoSQL injection", "Submit operators inside string fields",
          "Spring Data binds the value as a string; the repositories use derived queries or "
          "parameter placeholders."],
         ["Transport security", "Inspect the cookie flags in the development build",
          "Secure is false because the development origin is HTTP; this is a documented "
          "deviation for production."]],
        widths=[1.55, 1.75, 3.2],
        font_size=6.9,
        caption="Security verification record")
    st += note_box(
        "Two residual risks are honestly acknowledged. First, the refresh cookie is sent without "
        "the Secure flag in the reference configuration, so it would travel in clear text if the "
        "service were exposed over HTTP. Second, there is no rate limiting on "
        "<font name='Mono' size='7'>/authenticate</font>, so an online password-guessing attack "
        "is bounded only by BCrypt's cost. Both are configuration or infrastructure additions "
        "rather than design changes, and both are listed in Section 8.4.",
        "Residual security risk")

    st += [h2("7.8 Interface State Verification")]
    st += table(
        ["State", "Verified properties", "Result"],
        [["Empty dashboard", "Zero-per-cent bar, populated targets, empty chart series renders an "
                             "axis without points", "Pass"],
         ["Partially filled day", "Bar reflects the consumed fraction; meal cards retain their "
                                  "entered values after a reload", "Pass"],
         ["Over-target day", "Bar switches to the warning colour; the daily summary still shows "
                             "the target", "Pass"],
         ["No active plan", "Guarded routes resolve to the no-plan screen; both actions work",
          "Pass"],
         ["Plan completion", "Status endpoint deactivates the plan; the history row shows the "
                             "Inactive pill", "Pass"],
         ["Suggestion failure", "Inline error state; the filter row remains usable", "Pass"],
         ["Toast", "Appears on validation failure, dismisses itself, never stacks", "Pass"],
         ["404", "Wildcard route renders the page with a working link", "Pass"],
         ["Narrow viewport", "Cards reflow to a single column below 720 px and to two metric "
                             "columns at 640 px", "Pass"]],
        widths=[1.4, 4.3, 0.8],
        font_size=7.1,
        caption="Interface state verification")

    st += [h2("7.9 Performance Observations")]
    st += [T.body(
        "Response times were measured with the browser network panel over twenty repetitions of "
        "each request against the local MongoDB instance. The figures in Table 7.9 are "
        "indicative rather than benchmarked: they describe a single-user development deployment "
        "and should not be read as capacity claims.")]
    st += table(
        ["Operation", "Observed median", "Dominant cost"],
        [["POST /authenticate (BCrypt comparison included)", "310 ms", "BCrypt hashing at the "
                                                                       "configured cost"],
         ["GET /diet-plan/metrics", "38 ms", "One plan read, one document upsert-check, one "
                                             "range query over at most seven documents"],
         ["GET /diet-plan/track/plan/{id}", "22 ms", "Single-document lookup"],
         ["POST /diet-plan/{category}/{id}", "31 ms", "Read, in-memory recomputation, write"],
         ["GET /diet-plan/history", "19 ms", "Projected query over a handful of documents"],
         ["POST /diet-plan", "44 ms", "Two inserts (plan and first track)"],
         ["POST /ai-food-suggest", "2.4 s", "External inference; the service contributes under "
                                            "50 ms"],
         ["Client first contentful paint (production build)", "0.9 s", "Bundle parse and render"]],
        widths=[2.6, 1.3, 2.6],
        font_size=7.1,
        caption="Indicative response times")
    st += [T.body(
        "The only figure that matters to the user experience is the last but one: the suggestion "
        "request is dominated entirely by the provider's latency, which is why the screen "
        "disables its action and displays a loading state for the duration of the call. Every "
        "database-backed operation is well inside the 250 ms target of NFR-01, with "
        "authentication the single exception and BCrypt's deliberate slowness the cause.")]

    st += [h2("7.10 Discussion of Results")]
    st += [T.body(
        "The verification supports four conclusions. The arithmetic is correct and reproducible: "
        "every value in Table 7.3 was obtained independently and matches the service exactly, "
        "including the rounding behaviour that produces multiples of fifty. The two-level "
        "validation behaves as designed, with the client preventing the most common error before "
        "the request and the server refusing the physiologically unsafe cases that the client "
        "cannot know about. The tracking invariant holds: a document is always available for "
        "today, and a repeated submission cannot inflate a total. Finally, the security posture "
        "is sound for the deployment it targets, with two configuration-level deviations "
        "recorded rather than concealed.")]
    st += [T.body(
        "Three weaknesses were also confirmed. The automated test suite is effectively absent, so "
        "every result in this chapter depends on manual execution and would have to be repeated "
        "after any change. The absence of an index on the tracking collection means the range "
        "query scans the plan's documents, which is harmless at the current scale but would "
        "degrade with years of data; the natural index on the pair "
        "(<font name='Mono' size='8'>dietPlanId</font>, "
        "<font name='Mono' size='8'>createdAt</font>) is proposed in Section 8.4. And the "
        "dependency on a single external provider means that the suggestion feature is only as "
        "available as that provider, although the rest of the system is unaffected by its "
        "absence.")]
    return st
