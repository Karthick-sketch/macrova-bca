"""Chapters 2 (literature review) and 3 (system analysis)."""

from __future__ import annotations

from reportlab.platypus import Paragraph, Spacer

import diagrams_arch as A
import theme as T
from theme import S, bullets, chapter, figure, h2, h3, numbered, table


# ---------------------------------------------------------------------------
# Chapter 2
# ---------------------------------------------------------------------------
SURVEYS = [
    ("Predictive Equations for Resting Energy Expenditure in Healthy Adults",
     "1990", "1",
     "M. D. Mifflin, S. T. St Jeor, L. A. Hill, B. J. Scott, S. A. Daugherty and "
     "Y. O. Koh",
     "The paper introduces the equation that is now cited as Mifflin\u2013St Jeor: a "
     "resting energy expenditure of 10w + 6.25h \u2212 5a + 5 kcal/day for men and "
     "10w + 6.25h \u2212 5a \u2212 161 kcal/day for women, where w is mass in kilograms, "
     "h is stature in centimetres and a is age in years. It was derived from indirect "
     "calorimetry on 498 adults and reported closer agreement with measured values than "
     "the older Harris\u2013Benedict equation. Macrova implements both branches verbatim "
     "in <font name='Mono' size='7.6'>NutrientsCalculator.findBMR</font>.",
     ),
    ("Comparison of Predictive Equations for Resting Metabolic Rate in Healthy "
     "Non-obese and Obese Adults",
     "2005", "2",
     "J. Frankenfield, L. Roth-Yousey and C. Compher",
     "A systematic review that compares predictive equations against measured resting "
     "metabolic rate and concludes that the Mifflin\u2013St Jeor equation is the most "
     "reliable general-purpose predictor when calorimetry is unavailable, while noting "
     "that individual error of 10 per cent is expected. The review justified the "
     "decision to use one documented equation rather than a proprietary formula, and to "
     "display targets as guidance rather than prescription.",
     ),
    ("Human Energy Requirements: Report of a Joint FAO/WHO/UNU Expert Consultation",
     "2004", "3",
     "Food and Agriculture Organization, World Health Organization and United Nations "
     "University",
     "The consultation formalises the factorial method in which total energy expenditure "
     "is expressed as a multiple of resting expenditure according to a physical activity "
     "level. It classifies habitual activity into sedentary, light, moderate, vigorous "
     "and extremely vigorous bands. Macrova's <font name='Mono' size='7.6'>Activity</font> "
     "enumeration stores the five multipliers 1.2, 1.375, 1.55, 1.725 and 1.9 and its "
     "labels mirror these bands.",
     ),
    ("Indices of Relative Weight and Obesity",
     "1972", "4",
     "A. Keys, F. Fidanza, M. J. Karvonen, N. Kimura and H. L. Taylor",
     "The classical paper that established the body-mass index as a stature-independent "
     "index of relative weight. Macrova uses the index twice: to validate that a "
     "requested target weight is inside a healthy band, and to reject unsafe plans. The "
     "implementation rejects a weight-loss target whose index falls below 18 and a "
     "weight-gain target whose index exceeds 25.",
     ),
    ("Compendium of Physical Activities: A Second Update of Codes and MET Values",
     "2011", "5",
     "B. E. Ainsworth, W. L. Haskell, S. D. Herrmann, N. Meckes, D. R. Bassett and "
     "others",
     "The compendium tabulates metabolic equivalents for dozens of activities and "
     "provides the empirical basis for the activity multipliers used in factorial "
     "estimation. It supports the design decision to expose activity as five discrete "
     "levels rather than a free numeric field, which reduces both input error and "
     "unrealistic multiplier values.",
     ),
    ("JSON Web Token (JWT), RFC 7519",
     "2015", "7",
     "M. Jones, J. Bradley and N. Sakimura",
     "The specification defines a compact, self-describing token consisting of a header, "
     "a claim set and a signature. Macrova uses the <font name='Mono' size='7.6'>java-jwt</font> "
     "implementation to sign tokens with HMAC-SHA512 over a secret supplied through the "
     "<font name='Mono' size='7.6'>JWT_SECRET</font> environment variable, to place the "
     "username in the subject claim and to bound validity with the expiry claim.",
     ),
    ("The OAuth 2.0 Authorization Framework, RFC 6749",
     "2012", "8",
     "D. Hardt (editor)",
     "Although Macrova implements its own password grant rather than delegating to an "
     "authorisation server, RFC 6749 supplies the vocabulary the implementation uses: a "
     "short-lived bearer credential for resource access and a longer-lived refresh "
     "credential used solely to mint new access credentials. The lifetime ratio adopted "
     "here \u2014 one hour against twenty-four hours \u2014 follows the guidance that the "
     "refresh credential should outlive the access credential by at least an order of "
     "magnitude.",
     ),
    ("OWASP Application Security Verification Standard, Version 4.0.3",
     "2021", "9",
     "OWASP Foundation",
     "The standard enumerates verifiable security requirements for authentication, "
     "session management, access control and data protection. The project adopts its "
     "guidance on adaptive password hashing (BCrypt with per-password salt), on generic "
     "authentication failure messages that do not disclose whether a username exists, and "
     "on server-side authorisation decisions. Section 7.7 records the conformance "
     "position honestly, including the requirements that remain unmet in this release.",
     ),
    ("Architectural Styles and the Design of Network-based Software Architectures",
     "2000", "10",
     "R. T. Fielding",
     "Fielding's dissertation defines representational state transfer and the constraints "
     "that distinguish it: client\u2013server separation, statelessness, cacheability, a "
     "uniform interface and layered components. Macrova's API follows the style by "
     "exposing resource-oriented paths under <font name='Mono' size='7.6'>/user</font>, "
     "<font name='Mono' size='7.6'>/diet-plan</font> and "
     "<font name='Mono' size='7.6'>/ai-food-suggest</font>, by keeping no server session "
     "and by returning JSON representations.",
     ),
    ("Patterns of Enterprise Application Architecture",
     "2002", "11",
     "M. Fowler",
     "The catalogue supplies three patterns that structure the back end: the layering of "
     "presentation, domain and data source responsibilities; the data transfer object "
     "used to decouple the wire representation from persistence objects; and the "
     "repository that encapsulates query construction. Macrova implements them as "
     "controllers, DTO records, services and Spring Data repository interfaces.",
     ),
    ("Designing Data-Intensive Applications",
     "2017", "12",
     "M. Kleppmann",
     "The book compares relational and document models and observes that the document "
     "model suits data that is read and written as a self-contained unit, while "
     "normalisation suits many-to-many relationships. Macrova stores each tracking day as "
     "one document with embedded macronutrient objects precisely because the dashboard "
     "reads that unit whole, and it keeps the plan header separate because the archive "
     "pages the plan list without its tracks.",
     ),
    ("Usability Engineering and the Heuristic Evaluation of Interactive Systems",
     "1994", "13",
     "J. Nielsen",
     "Nielsen's heuristics \u2014 visibility of system status, match between system and "
     "the real world, user control, consistency and prevention of errors \u2014 inform "
     "the interface design described in Section 4.8. The loading state on the suggestion "
     "screen, the confirmation of active versus inactive plans, the persistent navigation "
     "bar and the inline validation messages are direct applications of these heuristics.",
     ),
]


def chapter2():
    st = []
    st += chapter(2, "LITERATURE REVIEW")
    st += [h2("2.1 Introduction")]
    st += [T.body(
        "Macrova sits at the intersection of two bodies of knowledge. The first is "
        "nutritional physiology: how energy expenditure is estimated from body metrics, "
        "how energy balance determines weight change, and why macronutrient composition "
        "matters. The second is software engineering: how a small information system should "
        "be layered, how its data should be modelled, how its endpoints should be secured "
        "and how its interface should communicate state. This chapter reviews twelve "
        "sources drawn from both bodies, records the specific decision each source "
        "influenced, compares the delivered system with five classes of existing software, "
        "and states the gaps that the project addresses.")]
    st += [T.body(
        "The sources were selected by a simple rule: a source was included only if a "
        "concrete artefact in the repository could be traced back to it. Consequently the "
        "review is deliberately narrow. It does not attempt a survey of machine learning for "
        "dietary recommendation, of wearable sensing or of clinical nutrition therapy, "
        "because the implemented system makes no claim in those areas.")]

    st += [h2("2.2 Review of Existing Systems and Related Literature")]
    for i, (title, year, refno, author, abstract) in enumerate(SURVEYS, start=1):
        st += [h3(f"2.2.{i} Literature Survey {i}")]
        st.append(Paragraph(f"<b>TITLE:</b> {title}", S["Body"]))
        st.append(Paragraph(f"<b>YEAR OF PUBLICATION:</b> {year}", S["Body"]))
        st.append(Paragraph(f"<b>AUTHOR(S):</b> {author}", S["Body"]))
        st.append(Paragraph(
            f"<b>ABSTRACT AND RELEVANCE:</b> {abstract} <b>[{refno}]</b>", S["Body"]))

    st += [h2("2.3 Comparative Study of Related Work")]
    st += [T.body(
        "Table 2.1 positions the delivered system against five classes of software that a "
        "student or fitness enthusiast might use for the same purpose. The comparison is "
        "qualitative and is based on the features each class typically exposes rather than "
        "on a measured benchmark.")]
    st += table(
        ["Criterion", "Paper or spreadsheet", "Generic calorie web calculator",
         "Consumer tracking app", "Clinical dietitian software", "Macrova (this work)"],
        [["Energy target derived from body metrics", "Manual", "Yes, formula hidden",
          "Yes, formula hidden", "Yes, supervised", "Yes, documented equation"],
         ["Macronutrient split stored", "Occasionally", "Rarely", "Yes", "Yes", "Yes (30/30/40)"],
         ["Per-meal targets",   "Manual", "No", "Sometimes", "Yes", "Yes (30/30/15/25)"],
         ["Server-side recomputation on weight change", "No", "No", "Partial", "By clinician",
          "Yes, on every update"],
         ["Plan validation (BMI, duration window)", "No", "No", "No", "Clinician judgement",
          "Yes, automated"],
         ["Immutable daily history", "No", "No", "Partial", "Yes", "Yes, one document per day"],
         ["Resume a previous plan", "Manual", "No", "Sometimes", "Yes", "Yes, cloned by id"],
         ["AI meal suggestion with cuisine filters", "No", "No", "Rarely", "No",
          "Yes, via OpenRouter"],
         ["Auditable open arithmetic", "Yes, by hand", "No", "No", "Partially", "Yes, one utility class"],
         ["Token-based stateless session", "Not applicable", "No", "Vendor-specific", "No",
          "Yes, JWT + refresh cookie"]],
        widths=[1.7, 1.0, 1.0, 1.0, 1.1, 1.2],
        font_size=7.0,
        caption="Comparative analysis of existing diet-planning approaches against Macrova")

    st += [h2("2.4 Research Gaps Identified")]
    st += numbered([
        "<b>Traceability of computed targets.</b> None of the surveyed consumer tools "
        "exposes the equation, the activity table and the macro ratios that produced a "
        "target. An auditable chain from inputs to grams per meal is absent, which prevents "
        "academic verification of the recommendation.",
        "<b>Recomputation on weight change.</b> Tools that store a plan usually freeze its "
        "targets. The literature on energy balance implies that targets must be recomputed "
        "as mass changes; the implemented system re-derives expenditure, intake and macros "
        "on every weight update.",
        "<b>Per-meal granularity of all three macronutrients.</b> Applications tend to track "
        "calories per meal and macronutrients per day. Splitting protein, fat and "
        "carbohydrate across four meals, as Macrova does, closes this gap.",
        "<b>Server-side validation of goal safety.</b> Consumer applications accept any "
        "target weight and duration. A derived duration window and a body-mass index guard "
        "are simple, deterministic checks that are rarely implemented.",
        "<b>Controlled use of generative models.</b> Where meal suggestions are "
        "AI-assisted, the model output is typically inserted into the page without schema "
        "validation. Treating the model as an unreliable service with a fixed JSON "
        "contract and an explicit failure state is not common practice in student "
        "projects, and is demonstrated here.",
    ])

    st += [h2("2.5 Summary of Literature Review")]
    st += [T.body(
        "The review establishes four conclusions that shaped the implementation. "
        "First, an energy model constructed from a published predictive equation and a "
        "documented activity table is defensible for a non-clinical application, provided "
        "the estimate is presented as guidance. Second, a document store is an appropriate "
        "substrate for a tracking workload that reads and writes one self-contained day at "
        "a time. Third, stateless token authentication with a short access lifetime and a "
        "longer refresh lifetime is a sound default for a JSON API. Fourth, interface "
        "consistency and explicit system status measurably reduce user error, which "
        "justifies the investment in a design system rather than ad-hoc styling. The next "
        "chapter converts these conclusions into requirements.")]
    return st


# ---------------------------------------------------------------------------
# Chapter 3
# ---------------------------------------------------------------------------
def chapter3():
    st = []
    st += chapter(3, "SYSTEM ANALYSIS")
    st += [h2("3.1 Existing System Analysis")]
    st += [T.body(
        "Before the application existed, the same task was performed with a spreadsheet and "
        "a printed calculator. The workflow had six steps: measure weight; choose a target "
        "weight and date; compute a basal metabolic rate and multiply by an activity factor; "
        "subtract or add a percentage to obtain a calorie target; split the target into "
        "protein, fat and carbohydrate; and write the grams into a notebook at each meal. "
        "Recording intake required a second pass in which the macronutrients of each meal "
        "were summed by hand and compared with the targets.")]
    st += [T.body(
        "The workflow is arithmetically correct and requires no software. Its weaknesses are "
        "operational: the eleven dependent calculations are repeated for every plan "
        "revision; the spreadsheet is not available at the dining table; the notebook "
        "carries no derived totals; and nothing links a plan to the days it governed. "
        "Because the target is frozen at the start of the plan, a user who loses three "
        "kilograms in the first month continues to eat against a budget computed for the "
        "original weight.")]
    st += figure(A.existing_vs_proposed(),
                 "Comparison of the existing manual workflow with the proposed system workflow")

    st += [h2("3.2 Limitations of the Existing System")]
    st += bullets([
        "Repeated manual computation invites arithmetic and unit errors, particularly when "
        "converting a calorie allocation into grams of protein, fat and carbohydrate.",
        "The plan and the record are physically separate artefacts, so the record cannot be "
        "validated against the plan.",
        "No authoritative history exists: a revised spreadsheet overwrites the previous "
        "plan, and paper pages are easily lost.",
        "There is no validation of the requested target weight or duration, so "
        "physiologically implausible goals are accepted.",
        "Targets do not adapt to the measured weight, so the deficit or surplus drifts "
        "away from the intended value.",
        "The per-meal split, if performed at all, is performed once and not updated.",
        "No access control exists; the notebook is either private or shared, with no "
        "middle ground.",
        "No reporting: producing a weekly weight trend requires manual plotting.",
        "No suggestion capability: the user must invent meals that fit the remaining "
        "budget.",
        "No portability: records cannot be consulted from another device.",
    ])

    st += [h2("3.3 Proposed System")]
    st += [T.body(
        "The proposed system automates the arithmetic, persists every artefact and exposes "
        "the plan and its history through a guarded web interface. It is implemented as a "
        "two-tier application. The presentation tier is an Angular single-page application "
        "that renders eleven routes; the application tier is a Spring Boot service that "
        "exposes twenty-three request handlers (four user, seventeen plan, one suggestion and the "
        "authentication filter) and persists to MongoDB.")]
    st += [T.body(
        "A plan is accepted only if two safety conditions hold. The body-mass index "
        "computed from the requested target weight and the stated height must be consistent "
        "with the direction of the plan: at least 18 kg/m\u00b2 for weight loss and at most "
        "25 kg/m\u00b2 for weight gain. The requested duration must lie between the "
        "minimum number of days derived at the fastest safe rate (seven days per kilogram "
        "for loss, fourteen days per kilogram for gain) and the maximum derived at the "
        "slowest useful rate (twenty-eight days per kilogram). Both conditions are evaluated "
        "server-side and reported to the client as a human-readable range.")]
    st += [T.body(
        "Once a plan is stored, the service immediately creates the first tracking document "
        "for the current date. That document embeds the computed calorie target, the three "
        "macronutrient targets, and the four meal allocations. When the user records a meal, "
        "the service writes the recorded values into the appropriate meal object, re-sums "
        "the three macronutrient totals across all four meals, and recomputes the calorie "
        "value actually consumed from the standard energy densities. When the user records a "
        "new weight, the service updates the plan's current weight and re-runs the entire "
        "energy chain for that day.")]

    st += [h2("3.4 Advantages of the Proposed System")]
    st += bullets([
        "Every displayed number is computed once, on the server, from a documented formula; "
        "the client performs no nutritional arithmetic.",
        "Targets adapt to the measured weight, so the intended deficit or surplus is "
        "preserved across the plan.",
        "Plans are validated against two independent safety rules before persistence.",
        "The daily record is immutable in structure and complete in itself, which makes the "
        "archive auditable and the dashboard a single-document read.",
        "The archive preserves every plan and every tracking day, and allows a past plan to "
        "be cloned into a new one.",
        "Session handling separates a short-lived access token from a long-lived refresh "
        "credential and keeps the refresh credential out of reach of page scripts.",
        "A single design system gives consistent typography, spacing and colour semantics "
        "across all screens.",
        "AI suggestions are constrained by the remaining calorie budget of the selected "
        "meal and by cuisine and dietary filters, rather than being unconstrained text.",
    ])

    st += [h2("3.5 Software Requirements Specification")]
    st += [h3("3.5.1 Functional Requirements")]
    st += table(
        ["ID", "Requirement", "Acceptance criterion"],
        [["FR-01", "The system shall register a user with a unique username, a unique e-mail "
                   "address and a password.",
          "Duplicate username or e-mail returns HTTP 400 with a descriptive message; the "
          "stored document contains a BCrypt digest, never the raw password."],
         ["FR-02", "The system shall authenticate a user and issue an access token and a "
                   "refresh token.",
          "POST /authenticate with valid credentials returns 200 and a Set-Cookie header "
          "containing an HttpOnly Refresh-Token cookie."],
         ["FR-03", "The system shall renew an access token from a valid refresh cookie.",
          "POST /user/refresh returns {accessToken}; a missing or expired cookie returns "
          "HTTP 401."],
         ["FR-04", "The system shall terminate a session on request.",
          "POST /user/logout returns a cookie with an empty value and max-age 0."],
         ["FR-05", "The system shall report the authenticated username.",
          "GET /user/username returns the subject of the validated access token."],
         ["FR-06", "The system shall validate a plan request on the client before submission.",
          "Empty title, age outside 18\u201365, height outside 140\u2013210 cm, weight outside "
          "40\u2013170 kg, target weight on the wrong side of the current weight, or duration "
          "outside 14\u2013730 days raises an inline toast."],
         ["FR-07", "The system shall validate a plan request on the server.",
          "A plan whose target-weight body-mass index violates the direction rule, or whose "
          "duration is outside the derived window, returns HTTP 400 with the permitted "
          "range."],
         ["FR-08", "The system shall compute basal metabolic rate, total daily energy "
                   "expenditure, calorie target and macronutrient targets.",
          "The computed values match the published equations to the nearest whole kcal and "
          "gram."],
         ["FR-09", "The system shall split each macronutrient target across four meals.",
          "Breakfast and lunch receive 30 per cent each, snack 15 per cent and dinner 25 per "
          "cent of each target."],
         ["FR-10", "The system shall persist a plan with its owner and creation date and mark "
                   "it active.",
          "The stored document contains the authenticated user identifier, active = true and "
          "an ISO date."],
         ["FR-11", "The system shall create the first tracking document when a plan is "
                   "created.",
          "A document exists for the current date with day count 1 and populated targets."],
         ["FR-12", "The system shall return the tracking document for a given plan and date, "
                   "creating it on demand.",
          "A request on a date without a document creates and returns one; a request for "
          "another user's plan returns HTTP 404."],
         ["FR-13", "The system shall record a new weight and recompute the day's targets.",
          "The stored track contains the new weight, the recomputed expenditure, target and "
          "macronutrients."],
         ["FR-14", "The system shall record per-meal macronutrient intake and recompute the "
                   "daily totals.",
          "The response contains updated per-meal and aggregate values; the consumed "
          "calories equal 4P + 9F + 4C."],
         ["FR-15", "The system shall expose a metrics resource for the dashboard.",
          "The response contains the plan title, elapsed day, duration, current weight, "
          "targets and a seven-entry day and weight series."],
         ["FR-16", "The system shall retire a plan whose duration has elapsed.",
          "GET /diet-plan/status returns true and sets active = false once the elapsed day "
          "count exceeds the duration."],
         ["FR-17", "The system shall list the plans of the authenticated user with status "
                   "summaries.",
          "GET /diet-plan/history returns one entry per plan ordered by creation date, with "
          "id, title, plan type, weights, duration and active flag."],
         ["FR-18", "The system shall return every tracking day of a plan for archival "
                   "display.",
          "GET /diet-plan/overview/{id} returns weight, expenditure, intake and macro values "
          "with dates in descending order."],
         ["FR-19", "The system shall allow a past plan to be resumed.",
          "The client passes the past plan identifier through navigation state; the form is "
          "pre-filled and the update endpoint replaces the active plan."],
         ["FR-20", "The system shall suggest foods using a language model constrained by the "
                   "meal budget and three filters.",
          "POST /ai-food-suggest returns a JSON array of five objects; a parse failure "
          "returns HTTP 410 and the client displays an error state."],
         ["FR-21", "The system shall protect every resource except registration and refresh.",
          "A request carrying no bearer token is rejected by the authorisation rule and returns "
          "HTTP 403 from the default entry point; an expired or unverifiable token returns "
          "HTTP 401 with the plain-text reason 'Access token expired' or 'JWT verification "
          "failed'."],
         ["FR-22", "The system shall return a uniform JSON error body.",
          "Errors are returned as {\"error\": [\"message\"]} with the appropriate status "
          "code."]],
        widths=[0.55, 2.9, 3.7],
        font_size=7.0,
        caption="Functional requirements specification (FR-01 to FR-22)")

    st += [h3("3.5.2 Non-Functional Requirements")]
    st += table(
        ["ID", "Category", "Requirement and target"],
        [["NFR-01", "Performance", "Every REST handler completes in under 250 ms against a "
                                   "local MongoDB instance, excluding the external language-model call."],
         ["NFR-02", "Scalability", "The service is stateless; additional instances may be "
                                   "placed behind a load balancer without session affinity."],
         ["NFR-03", "Security", "Passwords are stored only as BCrypt digests; tokens are "
                                "signed with HMAC512; the refresh token is HttpOnly and SameSite=Lax."],
         ["NFR-04", "Reliability", "A missing tracking document is created on demand rather "
                                   "than raising an error, so a day boundary cannot break the dashboard."],
         ["NFR-05", "Usability", "All screens use one design system; every form error is "
                                 "explained in words rather than codes."],
         ["NFR-06", "Portability", "The back end runs on any JDK 21 platform; the client "
                                   "runs on evergreen browsers."],
         ["NFR-07", "Maintainability", "Layering is enforced by package structure; "
                                       "nutritional arithmetic is isolated in one class."],
         ["NFR-08", "Auditability", "Each plan and each tracking day records the values that "
                                    "were in force on that date."],
         ["NFR-09", "Observability", "Exceptions are mapped to explicit status codes and "
                                     "messages; unhandled runtime exceptions return a generic body."],
         ["NFR-10", "Data integrity", "Queries are scoped by the authenticated principal; the "
                                      "client cannot supply an owner identifier."]],
        widths=[0.6, 1.15, 5.4],
        font_size=7.2,
        caption="Non-functional requirements specification (NFR-01 to NFR-10)")

    st += [h3("3.5.3 External Interface Requirements")]
    st += bullets([
        "<b>User interfaces:</b> HTML5 rendered by Angular 19; eleven routes; responsive "
        "down to 640 px where metric cards reflow to two columns.",
        "<b>Software interfaces:</b> JSON over HTTP/1.1; MongoDB wire protocol on port "
        "27017; the OpenRouter chat-completions REST API over HTTPS.",
        "<b>Communication interfaces:</b> bearer-token authorisation header, HttpOnly "
        "refresh cookie, and a development proxy that rewrites the "
        "<font name='Mono' size='7.6'>/api</font> prefix to the service root.",
    ])

    st += [h2("3.6 Feasibility Study")]
    st += [h3("3.6.1 Technical Feasibility")]
    st += [T.body(
        "Every component of the system is available in a mature, freely licensed form. Java "
        "21 and Spring Boot 3.4.4 provide the web, security and persistence infrastructure; "
        "MongoDB provides a schema-flexible document store that suits a tracking workload "
        "whose document shape is stable but whose embedded objects vary in count; Angular 19 "
        "provides a component model with guarded routing and typed HTTP clients. The "
        "nutritional equations require no numerical library beyond the Java standard "
        "library. The only external dependency with a variable cost is the language-model "
        "call, which is abstracted behind the "
        "<font name='Mono' size='7.6'>LLMService</font> interface so that the provider can "
        "be replaced without touching the food-suggestion module.")]
    st += [T.body(
        "The developer's existing competence in Java, TypeScript and REST design was "
        "sufficient; the learning effort concentrated on the newer Angular control-flow "
        "syntax, on Spring Security's filter chain and on the Jackson mapping of nested "
        "generic types returned by the model.")]

    st += [h3("3.6.2 Economic Feasibility")]
    st += [T.body(
        "The direct cost of the delivered system is zero: all frameworks, the database and "
        "the development tools are open source. The only recurring cost is the inference "
        "charge of the language-model provider, which is incurred per suggestion request. "
        "Table 3.3 summarises the cost position for a single-developer academic deployment "
        "and for a hypothetical hundred-user institute deployment.")]
    st += table(
        ["Cost head", "Academic deployment (current)", "Institute deployment (100 users)"],
        [["Runtime licences", "Nil (open-source stack)", "Nil (open-source stack)"],
         ["Application hosting", "Student laptop, port 8080", "One small virtual instance"],
         ["Database hosting", "Local MongoDB instance", "Managed MongoDB tier"],
         ["Language-model inference", "Pay per suggestion request", "Budget cap per month"],
         ["Development effort", "One semester, one developer", "Not applicable"],
         ["Subscription fees for users", "Nil", "Nil"]],
        widths=[1.6, 2.6, 2.6],
        caption="Economic feasibility summary")
    st += [T.body(
        "Because the application replaces a manual spreadsheet rather than a licensed "
        "product, the relevant comparison is the value of eliminated arithmetic and of the "
        "preserved plan history, not a licence saving. The language-model feature is "
        "optional: the remainder of the system functions when no API key is configured, and "
        "the suggestion screen is the only component that degrades.")]

    st += [h3("3.6.3 Operational Feasibility")]
    st += [T.body(
        "The interface follows conventions that users of consumer applications already know: "
        "a persistent top navigation bar with four destinations, a single primary action per "
        "screen, inline validation with plain-language messages, and a consistent teal "
        "palette in which the primary colour always denotes the forward action. No training "
        "is required beyond the user manual in Appendix B. The administrator's operational "
        "burden is limited to starting two processes and providing three environment "
        "variables.")]
    st += [T.body(
        "Social and organisational feasibility were assessed during internal reviews: the "
        "system does not collect health data beyond what the user volunteers, does not "
        "provide medical advice, and stores no payment information. Its outputs are "
        "presented as arithmetic guidance derived from published equations, which is "
        "consistent with the academic framing of the project.")]

    st += [h2("3.7 Summary of System Analysis")]
    st += [T.body(
        "The analysis converts a manual, error-prone workflow into twenty-two functional "
        "requirements and ten non-functional requirements, all of which are traceable to "
        "concrete handlers or components. The feasibility study finds the solution "
        "technically achievable with a free tool-chain, economically neutral apart from "
        "optional inference charges, and operationally simple. Chapter 4 now designs the "
        "system that satisfies these requirements.")]
    return st
