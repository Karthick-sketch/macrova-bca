"""Chapter 1 - Introduction."""

from __future__ import annotations

from reportlab.platypus import Paragraph, Spacer

import diagrams_arch as A
import theme as T
from theme import S, bullets, chapter, code_block, figure, h2, h3, note_box, numbered, table


def build():
    st = []
    st += chapter(1, "INTRODUCTION")
    st += [T.body(
        "<b>Macrova</b> is a web-based diet planning and macronutrient tracking system. "
        "It converts a small set of body measurements \u2014 age, gender, height, current "
        "weight, activity level, a goal and a target weight \u2014 into a complete, "
        "numerically consistent nutrition plan, and it then tracks that plan day by day. "
        "The application is delivered as a single-page Angular 19 client served on port "
        "4200 and a stateless Spring Boot 3.4.4 service listening on port 8080, with "
        "MongoDB as the document store. The back end is packaged as the Maven artifact "
        "<font name='Mono' size='8'>org.karthick:macrova:0.0.1-SNAPSHOT</font> and the "
        "front end as the npm project <font name='Mono' size='8'>macrova-ui</font>.")]

    st += [T.body(
        "Functionally the system covers five user-facing areas: account registration and "
        "authentication, creation and revision of a diet plan, a daily macronutrient log "
        "with automatic recomputation of totals, a dashboard that summarises progress and "
        "renders a seven-day weight trend, and an archive of past plans together with "
        "read-only historical day entries. A sixth area, AI-assisted meal suggestion, "
        "combines the calorie budget of a selected meal with three user-chosen filters "
        "(meal type, dietary preference and cuisine) and obtains a list of candidate foods "
        "from a large language model through the OpenRouter inference API.")]

    st += [T.body(
        "The distinguishing property of the implementation is that all nutritional "
        "arithmetic is performed on the server, inside a single utility class "
        "(<font name='Mono' size='8'>NutrientsCalculator</font>), and that the client never "
        "receives a number it did not receive from the server. Consequently the dashboard, "
        "the progress screen and the archived day view cannot disagree, and the numerical "
        "behaviour of the system can be verified by unit-testing one class.")]

    st += figure(A.journey(),
                 "End-to-end user journey through the implemented Macrova application")
    st += [T.body(
        "Figure 1.1 summarises the journey that the remainder of this report documents. "
        "Each stage corresponds to one or more concrete endpoints, services and documents "
        "that are described in Chapters 4 and 6.")]

    # ------------------------------------------------------------------
    st += [h2("1.1 Overview of the Project")]
    st += [T.body(
        "Macrova began as an attempt to answer a narrow question honestly: what exactly "
        "should a person eat tomorrow, in grams, given today's weight and a target date? "
        "Answering it requires a chain of computations whose order is fixed by physiology. "
        "The basal metabolic rate is estimated from body mass, stature, age and gender; it "
        "is multiplied by an activity factor to obtain total daily energy expenditure; a "
        "goal-dependent deficit or surplus converts that expenditure into an energy target; "
        "the target is divided into protein, fat and carbohydrate budgets; and the budgets "
        "are apportioned across meals so that each meal has an actionable target.")]
    st += [T.body(
        "The project therefore consists of three cooperating concerns. The <b>identity "
        "concern</b> registers a user, stores a BCrypt digest of the password and issues a "
        "short-lived access token together with a longer-lived refresh token. The "
        "<b>planning concern</b> validates the requested plan, computes the energy and "
        "macronutrient targets, persists the plan header and immediately seeds the first "
        "daily tracking document. The <b>tracking concern</b> lets the user record a new "
        "weight and the macronutrients consumed at each meal, recomputes the daily totals "
        "and the calorie deficit, and exposes aggregate metrics for the dashboard.")]
    st += [T.body(
        "Two design choices shape the implementation more than any other. First, the "
        "system stores <i>derived</i> values as well as <i>input</i> values: a tracking "
        "document contains both the targets that applied on that day and the values "
        "recorded against them, so a later change to the plan does not silently rewrite "
        "history. Second, the system keeps the plan header and the daily track in separate "
        "collections and links them with a plain identifier, which allows an arbitrary "
        "number of tracking days per plan without growing a single document beyond the "
        "16 MB BSON limit and without requiring joins on the read path.")]

    st += table(
        ["Attribute", "Specification in the current code base"],
        [["Application name", "Macrova \u2014 diet, macronutrient tracking and AI food "
                              "recommendation platform"],
         ["Back-end artifact", "org.karthick:macrova:0.0.1-SNAPSHOT (folder <font name='Mono' size='7'>backend/</font>, "
                               "Maven wrapper included)"],
         ["Front-end project", "macrova-ui (folder <font name='Mono' size='7'>frontend/</font>, Angular CLI "
                               "application builder)"],
         ["Architectural style", "Two-tier client\u2013server architecture: a stateless REST "
                                 "service with a layered internal structure (controller \u2192 "
                                 "service \u2192 repository \u2192 document)"],
         ["Runtime and framework", "Java 21, Spring Boot 3.4.4, Spring Web MVC, Spring "
                                   "Security 6, Spring Data MongoDB 4"],
         ["Data store", "MongoDB, database <font name='Mono' size='7'>macrova</font>; collections "
                        "<font name='Mono' size='7'>users</font>, <font name='Mono' size='7'>diet_plans</font>, "
                        "<font name='Mono' size='7'>diet_plan_tracks</font>, "
                        "<font name='Mono' size='7'>ai_food_suggests</font>"],
         ["Client technology", "Angular 19 standalone components, TypeScript 5.7, RxJS 7.8, "
                               "Chart.js 4.4, CSS custom properties"],
         ["Authentication", "JWT signed with HMAC512; 60-minute access token in memory; "
                            "24-hour refresh token in an HttpOnly cookie; BCrypt password "
                            "digests"],
         ["External integration", "OpenRouter chat-completions API (configurable model, "
                                  "temperature 0.3, JSON-only response contract)"],
         ["Documentation artefacts", "12 interface renderings, 19 architecture, DFD, UML and "
                                    "database figures, 30 data and test tables"]],
        widths=[2.0, 5.2],
        caption="High-level identity and architectural profile of Macrova")

    # ------------------------------------------------------------------
    st += [h2("1.2 Background of the Study")]
    st += [T.body(
        "Energy balance remains the most reliable predictor of short-term weight change. "
        "When energy intake is held below total daily energy expenditure, body mass falls; "
        "when it exceeds expenditure, body mass rises. The practical difficulty is that "
        "neither side of the equation is directly observable. Expenditure must be estimated "
        "from body metrics and habitual activity, and intake must be estimated from meals. "
        "Both estimates carry error, which is why tracking tools emphasise consistency "
        "rather than precision: a plan that is approximately right and is followed is more "
        "useful than a plan that is precisely computed and abandoned.")]
    st += [T.body(
        "The predictive-equation literature offers a well-established route from body "
        "metrics to energy expenditure. The Mifflin\u2013St Jeor equation, published in "
        "1990 [1], remains among the most accurate simple predictors of resting energy "
        "expenditure for non-obese and obese adults, and later systematic reviews "
        "recommended it as the default choice when indirect calorimetry is unavailable. "
        "Multiplying the resting value by a physical-activity-level factor converts resting "
        "expenditure into total daily expenditure; the FAO/WHO/UNU expert consultation "
        "formalised the multiplier approach [3], and the Compendium of Physical Activities "
        "provides the underlying intensity values [5]. Macrova adopts this chain without "
        "modification, and its activity enumeration stores the multipliers recommended in "
        "that literature.")]
    st += [T.body(
        "The composition of intake matters as much as its total. Protein, fat and "
        "carbohydrate differ in energy density \u2014 approximately 4, 9 and 4 kcal per "
        "gram respectively \u2014 and in their effect on satiety and lean-mass retention. A "
        "tracking system that reports only calories denies the user the ability to check "
        "whether protein intake is adequate during a deficit. Hence Macrova reports and "
        "stores a three-way macronutrient split and apportions it across meals.")]
    st += [T.body(
        "The software-engineering background of the project lies in the shift from "
        "server-rendered page applications to stateless APIs consumed by single-page "
        "clients. REST, as characterised by Fielding [10], treats the server as a resource "
        "hierarchy manipulated by uniform methods; the client holds session state. That "
        "model suits a tracking application well, because almost every screen is a view of "
        "the same small set of resources (the plan, today's track, the archive) and because "
        "it allows the same API to serve a future mobile client. Token-based "
        "authentication, standardised as JSON Web Token in RFC 7519 [7], complements the "
        "model: the server need not keep a session table, and the token can carry the "
        "subject and an expiry that the client can inspect before use.")]
    st += [T.body(
        "Finally, the domain background is cultural as much as technical. Indian diets are "
        "predominantly home-cooked, regionally varied and served in composite meals rather "
        "than in labelled portions. A recommendation engine that suggests Western "
        "single-item foods is therefore of limited practical value. The AI suggestion "
        "feature of Macrova deliberately exposes cuisine and dietary-preference filters so "
        "that suggestions can be constrained to Indian, Chinese, Japanese or Thai "
        "traditions, and vegetarian, non-vegetarian or low-carbohydrate preferences.")]

    # ------------------------------------------------------------------
    st += [h2("1.3 Problem Statement")]
    st += [T.body(
        "The problems that motivated the project are summarised below. Each is stated in "
        "terms of the behaviour of the implemented system that addresses it.")]
    st += numbered([
        "<b>Fragmented arithmetic.</b> Energy and macronutrient targets are computed in "
        "spreadsheets or on general-purpose websites, then lost; the tracking application "
        "used afterwards has no knowledge of the plan, so the two disagree. Macrova stores "
        "the computed targets inside the plan and copies them into every tracking day.",
        "<b>Opaque formulae.</b> Commercial applications present a calorie number without "
        "the equation, the activity factor or the macro split that produced it, which "
        "prevents any audit of the recommendation. Macrova evaluates a single documented "
        "class whose methods correspond one-to-one with published equations.",
        "<b>Static targets despite changing weight.</b> A plan computed once for a weight "
        "of 76.5 kg becomes wrong as the user loses mass. Each weight update in Macrova "
        "recomputes expenditure, intake and macro targets from the new weight and stores "
        "the result in that day's track.",
        "<b>No per-meal granularity.</b> Calories consumed are commonly recorded as a "
        "single daily number, which gives no guidance for the next meal. Macrova splits "
        "each macro across breakfast, lunch, snack and dinner and tracks them separately.",
        "<b>Coarse validation of user goals.</b> A user may request a target weight or a "
        "duration that is physiologically unsafe. Macrova rejects targets whose body-mass "
        "index lies outside the healthy band for the chosen direction and durations outside "
        "a derived window of seven to twenty-eight days per kilogram.",
        "<b>Volatile history.</b> Plans and past days are often overwritten when a new plan "
        "starts. Macrova keeps each plan as a separate document, marks the active one with "
        "a boolean flag, and exposes the archive through dedicated read-only endpoints.",
        "<b>Weak session handling in simple implementations.</b> Storing long-lived tokens "
        "in browser storage exposes them to script injection. Macrova keeps the access "
        "token in memory only and the refresh token in an HttpOnly cookie, with a "
        "server-side verification filter on every protected request.",
    ])

    # ------------------------------------------------------------------
    st += [h2("1.4 Objectives of the Project")]
    st += [T.body(
        "The objectives below were fixed at the start of the project and each one is "
        "traceable to a module described in Chapter 6.")]
    st += bullets([
        "<b>O1 \u2014 Deterministic nutritional engine:</b> implement the Mifflin\u2013St "
        "Jeor basal metabolic rate, the activity-multiplier total daily energy expenditure, "
        "the goal-dependent energy target, the 30/30/40 macronutrient split and the "
        "30/30/15/25 meal split in a stateless, unit-testable Java utility.",
        "<b>O2 \u2014 Safe plan validation:</b> reject plan requests whose target weight "
        "implies an unhealthy body-mass index or whose duration falls outside the derived "
        "minimum and maximum window, and communicate the permitted range to the client.",
        "<b>O3 \u2014 Daily tracking model:</b> represent every tracking day as one "
        "self-contained document, create it on demand, and recompute daily totals, the "
        "calorie deficit and the per-meal breakdown whenever a weight or a meal entry "
        "changes.",
        "<b>O4 \u2014 Aggregate progress reporting:</b> expose a single metrics resource "
        "that carries the plan title, elapsed days, planned duration, current weight, "
        "calorie and macro targets and the seven-day weight series used by the dashboard "
        "chart.",
        "<b>O5 \u2014 Plan lifecycle:</b> maintain exactly one active plan per user, retire "
        "a plan automatically when its duration has elapsed, and allow a past plan to be "
        "cloned into a new plan.",
        "<b>O6 \u2014 Token-based security:</b> authenticate with a JSON Web Token signed "
        "using HMAC512, issue a 60-minute access token and a 24-hour refresh token, store "
        "passwords as BCrypt digests, and translate every failure into a JSON error body.",
        "<b>O7 \u2014 AI-assisted suggestions:</b> generate a filtered prompt from the "
        "active plan's meal budget and a three-part filter, call a large language model "
        "through a provider-agnostic service interface, and parse the JSON reply into "
        "typed objects.",
        "<b>O8 \u2014 Responsive interface:</b> deliver a single-page client with guarded "
        "routes, an interceptor-based token handshake, a consistent teal design system and "
        "a charted progress view.",
    ])

    # ------------------------------------------------------------------
    st += [h2("1.5 Scope of the Project")]
    st += [T.body(
        "The functional scope of the release documented here is defined by the eleven "
        "Angular routes and the twenty-three request handlers that exist in the repository — "
        "four on the user controller, seventeen on the plan controller, one on the suggestion "
        "controller and the authentication endpoint implemented as a filter. "
        "Table 1.2 maps the scope onto the modules of the implementation.")]
    st += table(
        ["Area", "Routes / endpoints", "Capabilities implemented"],
        [["Identity", "<font name='Mono' size='7'>/login</font>, <font name='Mono' size='7'>/signup</font>; "
                      "<font name='Mono' size='7'>POST /user/register</font>, "
                      "<font name='Mono' size='7'>POST /authenticate</font>, "
                      "<font name='Mono' size='7'>POST /user/refresh</font>, "
                      "<font name='Mono' size='7'>POST /user/logout</font>, "
                      "<font name='Mono' size='7'>GET /user/username</font>",
          "Registration with duplicate-username and duplicate-e-mail checks, BCrypt "
          "hashing, access and refresh token issue, cookie-based refresh, logout, "
          "authenticated username lookup."],
         ["Plan authoring", "<font name='Mono' size='7'>/diet-plan-form</font>, "
                            "<font name='Mono' size='7'>/no-active-plan</font>; "
                            "<font name='Mono' size='7'>POST /diet-plan</font>, "
                            "<font name='Mono' size='7'>PUT /diet-plan/update</font>, "
                            "<font name='Mono' size='7'>POST /diet-plan/tdee</font>",
          "Client-side field validation, server-side BMI and duration validation, plan "
          "creation with day-1 track seeding, plan update, TDEE preview."],
         ["Daily tracking", "<font name='Mono' size='7'>/progress</font>; "
                            "<font name='Mono' size='7'>GET /diet-plan/track/plan/{id}</font>, "
                            "<font name='Mono' size='7'>POST /diet-plan/add-weight/{id}</font>, "
                            "<font name='Mono' size='7'>POST /diet-plan/{category}/{id}</font>, "
                            "<font name='Mono' size='7'>GET /diet-plan/meal-kcal/{id}</font>",
          "On-demand creation of the current day's track, weight update with full "
          "recomputation, per-meal macro entry for breakfast, lunch, snack and dinner, "
          "meal calorie breakdown."],
         ["Progress reporting", "<font name='Mono' size='7'>/dashboard</font>; "
                                "<font name='Mono' size='7'>GET /diet-plan/metrics</font>, "
                                "<font name='Mono' size='7'>GET /diet-plan/status</font>, "
                                "<font name='Mono' size='7'>GET /diet-plan/active-plans</font>",
          "Streak, current weight, calorie intake and macro targets, seven-day weight "
          "series, automatic retirement of expired plans, active-plan detection."],
         ["Archive", "<font name='Mono' size='7'>/history</font>, "
                     "<font name='Mono' size='7'>/history/:id</font>, "
                     "<font name='Mono' size='7'>/history/track/:id</font>; "
                     "<font name='Mono' size='7'>GET /diet-plan/history</font>, "
                     "<font name='Mono' size='7'>GET /diet-plan/past-plan</font>, "
                     "<font name='Mono' size='7'>GET /diet-plan/overview/{id}</font>",
          "Plan list with status badges, projected day entries, read-only historical day "
          "log, resume-past-plan handshake."],
         ["AI suggestions", "<font name='Mono' size='7'>/meals</font>; "
                            "<font name='Mono' size='7'>POST /ai-food-suggest</font>",
          "Filter selection, prompt construction with the meal calorie budget, OpenRouter "
          "invocation, JSON parsing into food objects, error state on HTTP 410."]],
        widths=[1.25, 2.35, 3.6],
        caption="Functional scope matrix of the implemented release")
    st += [T.body(
        "The following capabilities are deliberately <b>outside</b> the current release: "
        "integration with wearable devices or fitness trackers, photographic food "
        "recognition, barcode scanning of packaged food, recipe generation with ingredient "
        "quantities, social or coaching features, payment and subscription handling, "
        "multi-language localisation, and any clinical recommendation beyond arithmetic. "
        "The exclusion of the last item is a design decision rather than an omission: the "
        "system produces arithmetic targets from a documented equation and does not "
        "present medical advice.")]

    # ------------------------------------------------------------------
    st += [h2("1.6 Project Motivation")]
    st += [T.body(
        "Three observations motivated the work. The first was that the arithmetic of diet "
        "planning is simple but error-prone when performed by hand: converting a weight "
        "difference into a duration, converting a calorie target into grams of three "
        "macronutrients, and apportioning those grams across four meals requires eleven "
        "dependent calculations. Doing this on paper for sixty consecutive days is "
        "impractical, yet doing it once and freezing the result defeats the purpose of "
        "tracking.")]
    st += [T.body(
        "The second observation concerned software structure. A diet tracker is small "
        "enough to be implemented as a single class, and many tutorials do exactly that. "
        "The project was an opportunity to demonstrate that even a small domain benefits "
        "from explicit architectural layers, a documented data model, defensive validation "
        "at both boundaries, and a security model that does not depend on the client's "
        "good behaviour. Every endpoint in the delivered system derives the owner of the "
        "data from the authenticated principal rather than from a request parameter.")]
    st += [T.body(
        "The third observation concerned the responsible use of generative models. A large "
        "language model can propose meals that respect a calorie budget, but its output is "
        "free text. The project therefore treats the model as an unreliable external "
        "service: the prompt fixes the response schema, the temperature is lowered to 0.3, "
        "the reply is parsed into typed objects, and a parse failure is surfaced to the "
        "user as an explicit error rather than a partially rendered list.")]

    # ------------------------------------------------------------------
    st += [h2("1.7 Assumptions and Constraints")]
    st += [h3("1.7.1 Assumptions")]
    st += bullets([
        "The user reports body metrics honestly; no measurement device is integrated.",
        "The Mifflin\u2013St Jeor estimate is an acceptable proxy for measured resting "
        "energy expenditure in a non-clinical application.",
        "The activity multiplier selected by the user describes habitual activity for the "
        "whole plan period and does not change daily.",
        "One active plan per user is sufficient; concurrent plans are not modelled.",
        "The user tracks intake on the same calendar date on which the food is consumed; "
        "the tracking document is keyed by the server's local date.",
        "The language model returns a JSON array in the schema requested by the system "
        "prompt; any deviation is reported as an error.",
        "The deployment target is a single application instance with a single MongoDB "
        "instance; horizontal scaling is out of scope.",
    ])
    st += [h3("1.7.2 Constraints")]
    st += bullets([
        "<b>Time:</b> the project was developed within one academic Semester.",
        "<b>Team size:</b> a single developer, which limited the breadth of the automated "
        "test suite to a Spring context-load test and a manually executed acceptance "
        "catalogue.",
        "<b>Environment:</b> the reference deployment uses a local MongoDB instance on "
        "port 27017 and the Angular development server on port 4200 with a proxy that "
        "rewrites <font name='Mono' size='8'>/api</font> to port 8080.",
        "<b>Secrets:</b> the JWT signing secret and the OpenRouter key are supplied as "
        "environment variables (<font name='Mono' size='8'>JWT_SECRET</font>, "
        "<font name='Mono' size='8'>OPENROUTER_API_KEY</font>, "
        "<font name='Mono' size='8'>OPENROUTER_MODEL</font>) and are never committed.",
        "<b>Currency of literature:</b> the nutritional formulae are deliberately taken "
        "from long-established publications rather than recent web content.",
        "<b>Browser support:</b> evergreen Chromium and Firefox releases; no legacy "
        "browser support is claimed.",
    ])

    # ------------------------------------------------------------------
    st += [h2("1.8 Organisation of the Report")]
    st += [T.body("The report is organised as follows.")]
    st += bullets([
        "<b>Chapter 1 \u2014 Introduction</b> states the problem, objectives, scope and "
        "constraints, and profiles the delivered system.",
        "<b>Chapter 2 \u2014 Literature Review</b> surveys the twelve sources that inform "
        "the nutritional and software design, compares five classes of existing systems and "
        "identifies the gaps addressed here.",
        "<b>Chapter 3 \u2014 System Analysis</b> analyses the existing manual practice, "
        "derives the proposed system, and records functional and non-functional "
        "requirements with a feasibility study.",
        "<b>Chapter 4 \u2014 System Design</b> presents the architecture, data-flow "
        "diagrams, use cases, UML class, sequence, activity and state models, the document "
        "database design with data dictionaries, and the input/output design.",
        "<b>Chapter 5 \u2014 Technologies and Tools</b> lists software, hardware, languages, "
        "frameworks and the development environment.",
        "<b>Chapter 6 \u2014 Implementation</b> describes every module, the core algorithms "
        "with pseudocode and source excerpts, and walks through twelve interface renderings.",
        "<b>Chapter 7 \u2014 Testing and Results</b> records the test strategy, a "
        "twenty-eight case acceptance catalogue, endpoint verification and a performance "
        "and security analysis.",
        "<b>Chapter 8 \u2014 Conclusion and Future Scope</b> summarises the work, states "
        "its limitations candidly and lists enhancements.",
        "<b>Appendices</b> provide the API reference, configuration keys, sample documents, "
        "the installation and user manual, and the glossary.",
    ])
    return st
