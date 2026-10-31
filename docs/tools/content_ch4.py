"""Chapter 4 - System design."""

from __future__ import annotations

from reportlab.platypus import Paragraph, Spacer

import diagrams_arch as A
import diagrams_uml as U
import theme as T
from theme import S, bullets, chapter, figure, h2, h3, note_box, numbered, table


def build():
    st = []
    st += chapter(4, "SYSTEM DESIGN")

    # ------------------------------------------------------------------
    st += [h2("4.1 Design Overview and Architectural Principles")]
    st += [T.body(
        "The design follows six principles, each of which is visible in the package "
        "structure. <b>Separation of concerns</b> places web handling, business rules and "
        "persistence in distinct packages so that a controller never constructs a query and "
        "a repository never performs arithmetic, which is the classical layered decomposition "
        "described in [14]. <b>Single source of truth for arithmetic</b> "
        "keeps every equation in <font name='Mono' size='8'>NutrientsCalculator</font>, a "
        "final class of static methods with no dependencies, so that the numerical behaviour "
        "of the system can be reasoned about and tested in isolation. <b>Server-side "
        "authority</b> derives the owner of every resource from the authenticated principal "
        "rather than from the request, and performs every validation that protects the user "
        "on the server as well as in the browser.")]
    st += [T.body(
        "<b>Denormalisation by read unit</b> stores each tracking day as one self-contained "
        "document that embeds its targets, its recorded values and its per-meal breakdown, "
        "because the dashboard, the progress screen and the archive all read that unit "
        "whole, exactly as the document-model argument in [12] predicts. <b>Explicit contracts</b> restricts the wire format to DTOs and to the "
        "document classes that the client already understands, and never leaks internal "
        "fields such as the password digest. <b>Fail visibly</b> maps each exception family "
        "to one HTTP status and one JSON body so that the client can react deterministically "
        "instead of guessing.")]

    # ------------------------------------------------------------------
    st += [h2("4.2 System Architecture")]
    st += [T.body(
        "Macrova is a two-tier client\u2013server system with an external inference "
        "dependency. Figure 4.1 shows the three logical layers of the delivered "
        "implementation and the external service. The presentation tier is the Angular "
        "application; the application tier is the Spring Boot service; the data tier is "
        "MongoDB; and the language model is reached only through the "
        "<font name='Mono' size='8'>LLMService</font> abstraction inside the application "
        "tier, which prevents any controller from depending on a vendor SDK.")]
    st += figure(A.architecture(),
                 "Three-tier architecture of the Macrova application with the external "
                 "inference service")
    st += [T.body(
        "The package view in Figure 4.2 shows how the application tier is decomposed. The "
        "root package <font name='Mono' size='8'>org.karthick.macrova</font> contains nine "
        "sub-packages. The dependency direction is downward and inward: controllers depend "
        "on services, services depend on repositories and on the utility class, and no "
        "repository depends on a controller. The "
        "<font name='Mono' size='8'>security</font> package is consumed by the service layer "
        "through <font name='Mono' size='8'>UserSession</font>, which resolves the current "
        "principal from the security context.")]
    st += figure(A.packages(),
                 "Package and component structure of the Spring Boot application tier")
    st += table(
        ["Layer", "Responsibilities", "Key types"],
        [["Presentation (Angular)", "Routing, guarded navigation, template rendering, "
                                    "client-side validation, HTTP interception, chart rendering",
          "AppComponent, HeaderComponent, LoginComponent, DashboardComponent, "
          "DietPlanComponent, DietPlanFormComponent, AIFoodSuggestComponent, "
          "DietPlansListComponent, DietPlanOverviewComponent, DietPlanTrackOverviewComponent, "
          "NoActiveDietPlanComponent, PageNotFoundComponent, ToastComponent, WeightTrackComponent"],
         ["Web (Spring MVC)", "Request binding, response serialisation, status codes, "
                              "exception translation",
          "UserController, DietPlanController, AIFoodSuggestController, "
          "ApplicationExceptionHandler"],
         ["Security", "Authentication, token issue and verification, principal resolution, "
                      "CORS policy",
          "SecurityConfig, AuthenticationFilter, JWTAuthenticationFilter, "
          "ExceptionHandlerFilter, CustomAuthenticationManager, JWTTokenService, UserSession"],
         ["Service", "Plan validation, energy computation, track lifecycle, metrics "
                     "aggregation, prompt construction",
          "UserService, DietPlanService, AIFoodSuggestService, OpenRouterLLMService"],
         ["Domain", "Document entities, embedded value objects, enumerations",
          "User, DietPlan, DietPlanTrack, AIFoodSuggest, Calories, Macros, MealKcal, Plan, "
          "Goal, Activity, Gender"],
         ["Persistence", "Query derivation, projections, aggregation of weekly series",
          "UserRepository, DietPlanRepository, DietPlanTrackRepository, "
          "AIFoodSuggestRepository"],
         ["Utility and configuration", "Stateless arithmetic, constants, date conversion, "
                                       "bean wiring",
          "NutrientsCalculator, MacrosConstants, MongoConfig, ModelMapperConfig, Mapper"]],
        widths=[1.05, 2.6, 3.5],
        font_size=7.0,
        caption="Layer responsibilities and key types")

    # ------------------------------------------------------------------
    st += [h2("4.3 Data Flow Diagrams")]
    st += [T.body(
        "Three levels of data-flow diagram describe the movement of information. The "
        "context diagram fixes the system boundary; the level-1 diagram decomposes the "
        "system into five processes and four data stores; the level-2 diagram decomposes "
        "the daily-tracking process, which carries the most intricate logic.")]
    st += [h3("4.3.1 Level 0 \u2014 Context Diagram")]
    st += [T.body(
        "At the context level, Macrova exchanges two flows with the user and two flows with "
        "the inference service. The user supplies credentials, plan parameters, meal entries "
        "and filter selections; the system returns an authenticated session, computed "
        "targets, dashboard metrics, history and food suggestions. The inference service "
        "receives a prompt containing the meal calorie budget and returns a JSON array.")]
    st += figure(A.dfd0(), "Data-flow diagram, level 0 \u2014 context of the Macrova system")
    st += [h3("4.3.2 Level 1 \u2014 Functional Decomposition")]
    st += [T.body(
        "The level-1 diagram introduces the four collections as data stores and the five "
        "processes that constitute the system. Process 3.0 is shared: it is invoked by plan "
        "configuration when a plan is created, and by daily tracking whenever a weight "
        "changes.")]
    st += figure(A.dfd1(), "Data-flow diagram, level 1 \u2014 functional decomposition")
    st += table(
        ["Process", "Description", "Realised by"],
        [["1.0 Account and session management",
          "Registers a user, verifies credentials, issues and refreshes tokens, terminates a "
          "session and resolves the authenticated principal.",
          "UserService, CustomAuthenticationManager, JWTTokenService, AuthenticationFilter, "
          "JWTAuthenticationFilter, UserController"],
         ["2.0 Diet plan configuration",
          "Accepts plan parameters, validates them, delegates the arithmetic to process 3.0, "
          "persists the plan header and seeds the first tracking day.",
          "DietPlanController.createDietPlan, DietPlanService.validateDietPlan, "
          "DietPlanService.createDietPlan"],
         ["3.0 Nutrition computation",
          "Computes basal metabolic rate, total daily energy expenditure, calorie target, "
          "macronutrient grams and the four meal allocations.",
          "NutrientsCalculator (findBMR, findTDEE, findDeficit, findSurplus, findProtein, "
          "findFat, findCarbs, macrosPercentage)"],
         ["4.0 Daily tracking and progress",
          "Resolves the day's tracking document, records weight and meal entries, recomputes "
          "totals and deficit, aggregates the seven-day weight series.",
          "DietPlanService.addWeight, updateMacros, getMetricsByDateRange, "
          "DietPlanTrackRepository"],
         ["5.0 AI meal recommendation",
          "Builds a prompt from the selected meal's calorie budget and the three filters, "
          "calls the language model and parses the response.",
          "AIFoodSuggestService, OpenRouterLLMService"]],
        widths=[1.5, 2.9, 2.7],
        font_size=7.0,
        caption="Process descriptions of the level-1 data-flow diagram")
    st += [h3("4.3.3 Level 2 \u2014 Daily Tracking Decomposition")]
    st += [T.body(
        "Process 4.0 decomposes into five sub-processes. Sub-process 4.1 resolves the "
        "document for the current date and creates it if the user has not yet opened the "
        "application that day; 4.2 applies a weight update and re-enters process 3.0; "
        "4.3 writes the recorded grams into the selected meal object; 4.4 re-sums the three "
        "macronutrients and recomputes consumed calories; and 4.5 assembles the metrics "
        "resource from the current document and the seven-day weight series.")]
    st += figure(A.dfd2(),
                 "Data-flow diagram, level 2 \u2014 decomposition of daily tracking and "
                 "progress")

    # ------------------------------------------------------------------
    st += [h2("4.4 Use Case Diagram and Actor Specifications")]
    st += [T.body(
        "The system has two human actors and one secondary (system) actor. The visitor may "
        "register and authenticate; the registered user inherits every other use case; the "
        "inference service participates only in the suggestion use case.")]
    st += figure(U.usecase(), "Unified use case diagram of the Macrova system")
    st += table(
        ["Actor", "Type", "Goal", "Use cases"],
        [["Visitor", "Primary, unauthenticated", "Create an account or start a session",
          "Register account, Log in"],
         ["Registered user", "Primary, authenticated", "Plan, track and review nutrition",
          "Maintain session, Create or update plan, Log daily macros, Update weight, Review "
          "dashboard and history, Request AI suggestions"],
         ["OpenRouter LLM", "Secondary, external", "Return structured food suggestions",
          "Request AI food suggestions"]],
        widths=[1.0, 1.2, 1.9, 3.1],
        caption="Actor-to-use-case responsibility matrix")
    st += table(
        ["ID", "Use case", "Primary actor", "Trigger"],
        [["UC-01", "Register account", "Visitor", "Submission of the sign-up form"],
         ["UC-02", "Log in and establish a session", "Visitor", "Submission of the log-in form"],
         ["UC-03", "Refresh the access token", "Registered user", "Expiry detected by the client interceptor"],
         ["UC-04", "Log out", "Registered user", "Selection of Sign Out in the profile menu"],
         ["UC-05", "Create or update a diet plan", "          Registered user", "Submission of the plan form"],
         ["UC-06", "Log daily meal macronutrients", "Registered user", "Selection of Update in a meal card"],
         ["UC-07", "Update body weight", "Registered user", "Selection of Update Weight"],
         ["UC-08", "Review dashboard metrics", "Registered user", "Navigation to /dashboard"],
         ["UC-09", "Browse plan history and archived days", "Registered user", "Navigation to /history"],
         ["UC-10", "Request AI food suggestions", "Registered user", "Selection of Get Suggestions"],
         ["UC-11", "Resume a past plan", "Registered user", "Selection of Continue this plan"]],
        widths=[0.55, 2.5, 1.4, 2.7],
        font_size=7.1,
        caption="Use case inventory")
    st += [h3("4.4.1 Use Case Specification \u2014 UC-02: Log In and Establish a Session")]
    st += table(
        ["Item", "Specification"],
        [["Actors", "Visitor (primary); AuthenticationFilter, CustomAuthenticationManager, "
                    "UserService, JWTTokenService (supporting)"],
         ["Preconditions", "The visitor has a registered account and the service is reachable "
                           "through the development proxy."],
         ["Trigger", "The visitor submits username and password on /login."],
         ["Main flow", "1. AuthService.login posts the credentials with credentials enabled. "
                       "2. AuthenticationFilter parses the JSON body into a User and builds a "
                       "UsernamePasswordAuthenticationToken. 3. CustomAuthenticationManager "
                       "loads the user and compares the raw password with the stored BCrypt "
                       "digest. 4. On success the filter generates a refresh token with a "
                       "24-hour expiry and writes it to an HttpOnly, SameSite=Lax cookie. "
                       "5. The client fetches the username, which triggers the interceptor to "
                       "call /user/refresh and obtain a 60-minute access token, then retries "
                       "the request with the bearer header. 6. The router navigates to "
                       "/dashboard."],
         ["Alternate flow", "If the username is unknown, CustomAuthenticationManager raises "
                            "BadCredentialsException so that the response does not reveal "
                            "whether the account exists; the filter writes HTTP 401 and the "
                            "client shows 'Invalid username or password!'."],
         ["Postconditions", "A refresh cookie is stored by the browser; an access token is "
                            "held in memory; the header displays the user's initial."]],
        widths=[1.1, 5.4],
        font_size=7.1,
        caption="Use case specification \u2014 UC-02 log in")
    st += [h3("4.4.2 Use Case Specification \u2014 UC-05: Create or Update a Diet Plan")]
    st += table(
        ["Item", "Specification"],
        [["Actors", "Registered user (primary); DietPlanFormComponent, DietPlanService, "
                    "DietPlanController, NutrientsCalculator (supporting)"],
         ["Preconditions", "No active plan exists (for creation) or a past plan identifier is "
                           "supplied through navigation state (for resumption)."],
         ["Main flow", "1. The component validates the fields and the direction of the target "
                       "weight. 2. It posts the plan to /diet-plan. 3. The controller "
                       "delegates to the service, which validates the body-mass index of the "
                       "target weight and the duration window. 4. The service stamps the owner "
                       "identifier, sets today's weight, marks the plan active and saves it. "
                       "5. It creates the day-1 tracking document, computing expenditure, "
                       "target, macronutrient grams and the four meal allocations. 6. The "
                       "client navigates to /dashboard."],
         ["Alternate flow", "A target weight whose body-mass index is below 18 for weight "
                            "loss (or above 25 for weight gain) raises BadRequestException; a "
                            "duration outside the derived window raises BadRequestException "
                            "carrying the permitted range. Both are rendered as a toast."],
         ["Postconditions", "One plan document with active = true and one tracking document "
                            "for the current date exist for the authenticated user."]],
        widths=[1.1, 5.4],
        font_size=7.1,
        caption="Use case specification \u2014 UC-05 create or update a diet plan")
    st += [h3("4.4.3 Use Case Specification \u2014 UC-06: Log Daily Meal Macronutrients")]
    st += table(
        ["Item", "Specification"],
        [["Actors", "Registered user (primary); DietPlanComponent, DietPlanService, "
                    "DietPlanController (supporting)"],
         ["Preconditions", "An active plan exists and the day's tracking document is loaded."],
         ["Main flow", "1. The user edits the protein, carbohydrate and fat fields of a meal "
                       "card. 2. The component posts the three figures to "
                       "/diet-plan/{category}/{dietPlanId}. 3. The controller validates the "
                       "category against the four permitted constants. 4. The service loads "
                       "today's document, writes the recorded values into the selected meal, "
                       "re-sums the three macronutrients across the four meals and recomputes "
                       "consumed calories as 4P + 9F + 4C. 5. The updated document is returned "
                       "and re-rendered."],
         ["Alternate flow", "An unknown category returns HTTP 400 'Invalid macro category'; a "
                            "missing document returns HTTP 404."],
         ["Postconditions", "The document records per-meal and aggregate values; the calorie "
                            "bar is coloured by the relationship between consumed, target and "
                            "expenditure."]],
        widths=[1.1, 5.4],
        font_size=7.1,
        caption="Use case specification \u2014 UC-06 log daily meal macronutrients")
    st += [h3("4.4.4 Use Case Specification \u2014 UC-10: Request AI Food Suggestions")]
    st += table(
        ["Item", "Specification"],
        [["Actors", "Registered user (primary); AIFoodSuggestComponent, "
                    "AIFoodSuggestService, DietPlanService, OpenRouterLLMService, external "
                    "model (secondary)"],
         ["Preconditions", "An active plan and a tracking document exist for the current date."],
         ["Main flow", "1. The user selects a meal, a dietary preference and a cuisine and "
                       "submits the form. 2. The service obtains the calorie budget of the "
                       "selected meal from the active plan's daily document. 3. It composes "
                       "the prompt 'Suggest me 5 healthy <cuisine> <diet> foods for <meal> "
                       "under <kcal> calories'. 4. The LLM service posts a two-message "
                       "conversation with a JSON-only system instruction, temperature 0.3 and "
                       "streaming disabled. 5. The content of the first choice is parsed into "
                       "a list of food objects and returned."],
         ["Alternate flow", "If no active plan exists the calorie budget defaults to 500 "
                            "kcal. If parsing fails, JsonProcessingException is translated to "
                            "HTTP 410 and the component displays an inline error message."],
         ["Postconditions", "Five food cards with calories and macronutrients are rendered, or "
                            "an explicit error state is shown."]],
        widths=[1.1, 5.4],
        font_size=7.1,
        caption="Use case specification \u2014 UC-10 request AI food suggestions")

    # ------------------------------------------------------------------
    st += [h2("4.5 Object-Oriented and Behavioural UML Models")]
    st += [h3("4.5.1 Class Model")]
    st += [T.body(
        "Figure 4.7 presents the persistent and embedded classes. Four document classes map "
        "one-to-one onto collections; three value objects are embedded rather than "
        "referenced. The value objects are deliberately simple: "
        "<font name='Mono' size='8'>Calories</font> carries a total and a recorded value, "
        "<font name='Mono' size='8'>Macros</font> groups three calorie objects, and "
        "<font name='Mono' size='8'>MealKcal</font> groups four macro objects. The "
        "composition chain <i>track \u2192 meal \u2192 macros \u2192 calories</i> is what "
        "allows a single document to answer every question the tracking screens ask.")]
    st += figure(U.class_diagram(), "Domain class diagram of documents, value objects and enumerations")

    st += [h3("4.5.2 Sequence Models")]
    st += [T.body(
        "Three sequence diagrams cover the flows with the most interaction. Figure 4.8 shows "
        "authentication, including the lazy acquisition of the access token: the "
        "authentication filter writes only the refresh cookie, and the client obtains an "
        "access token on the first protected request through the interceptor-driven refresh "
        "handshake. Figure 4.9 shows plan creation and the immediate seeding of the first "
        "tracking day. Figure 4.10 shows the suggestion flow, which is the only flow that "
        "leaves the process boundary.")]
    st += figure(U.seq_login(), "Sequence diagram \u2014 authentication and the access-token handshake")
    st += figure(U.seq_plan(), "Sequence diagram \u2014 diet-plan creation and day-1 track seeding")
    st += figure(U.seq_ai(), "Sequence diagram \u2014 AI food suggestion via OpenRouter")
    st += [T.body(
        "Figure 4.11 relates the two token lifetimes. The access token is deliberately short "
        "so that a leaked value has limited value; the refresh token is longer lived but is "
        "inaccessible to page scripts, and the client never stores either token in local "
        "storage.")]
    st += figure(A.tokens(), "Access and refresh token lifetimes and the refresh handshake")

    st += [h3("4.5.3 Activity Model")]
    st += [T.body(
        "Figure 4.12 describes the happy path and both rejection paths of plan creation. The "
        "diagram makes an important property of the design explicit: client-side validation "
        "and server-side validation are independent, and the server never trusts the client's "
        "decision.")]
    st += figure(U.activity_plan(), "Activity diagram \u2014 plan creation with client and server validation")

    st += [h3("4.5.4 State Model")]
    st += [T.body(
        "A plan has three observable states. It is created active, it remains active while "
        "the elapsed day count does not exceed its duration, and it becomes completed when "
        "the status endpoint detects that the duration has been exceeded. A completed plan "
        "can be cloned into a new active plan, which is the mechanism behind the "
        "'Continue this plan' action of the no-active-plan screen.")]
    st += figure(U.state_plan(), "State machine \u2014 lifecycle of a diet plan")

    # ------------------------------------------------------------------
    st += [h2("4.6 Entity\u2013Relationship Model")]
    st += [T.body(
        "Although MongoDB does not enforce referential integrity, the data model has a clear "
        "logical relationship structure in the sense of [15]: one user owns zero or more plans, and one plan owns "
        "zero or more tracking days. Both relationships are realised as identifier fields, "
        "and the service layer enforces ownership by always combining the identifier with "
        "the authenticated principal in the query predicate.")]
    st += figure(U.er(), "Document entity\u2013relationship model of the Macrova database")

    # ------------------------------------------------------------------
    st += [h2("4.7 Database Design and Data Dictionary")]
    st += [T.body(
        "The database <font name='Mono' size='8'>macrova</font> contains four collections. "
        "Collections are created implicitly on first write; there is no schema-migration "
        "tool in this release, and the Java document classes act as the schema of record. "
        "Table 4.9 summarises the collections; the following tables give the data dictionary "
        "for each.")]
    st += table(
        ["Collection", "Purpose", "Document count per user", "Growth pattern"],
        [["users", "One document per registered account, holding credentials",
          "1", "One per registration"],
         ["diet_plans", "One document per plan, holding body metrics, goal parameters and the "
                        "active flag",
          "n \u2265 1", "One per plan creation or resumption"],
         ["diet_plan_tracks", "One document per tracked calendar day of one plan, holding "
                              "targets, recorded values and the meal breakdown",
          "one per plan per tracked day", "One per day, per plan"],
         ["ai_food_suggests", "Model output mapped to a document class; the repository exists "
                              "for optional caching of suggestions",
          "0 in normal operation", "Only when suggestions are persisted explicitly"]],
        widths=[1.1, 3.0, 1.1, 1.3],
        font_size=7.1,
        caption="Collection overview of the macrova database")

    st += [h3("4.7.1 users")]
    st += table(
        ["Field", "BSON type", "Constraint / origin", "Purpose"],
        [["_id", "ObjectId", "Generated by the driver", "Primary key; referenced by "
                                                          "diet_plans.userId"],
         ["username", "String", "Unique in practice; checked by existsByUsername before "
                                "insertion", "Login identifier and the JWT subject claim"],
         ["email", "String", "Unique in practice; checked by existsByEmail", "Contact "
                                                                              "identifier shown to the user"],
         ["password", "String", "BCrypt digest produced by PasswordEncoder.encode", "Credential "
                                                                                     "verification; never returned by any endpoint"]],
        widths=[0.9, 0.8, 2.5, 2.3],
        font_size=7.2,
        caption="Data dictionary \u2014 collection users")

    st += [h3("4.7.2 diet_plans")]
    st += table(
        ["Field", "BSON type", "Constraint / domain", "Purpose"],
        [["_id", "ObjectId", "Driver-generated", "Plan identifier used by every track path"],
         ["title", "String", "Client-validated non-empty", "User-facing plan name"],
         ["plan", "String (enum)", "WEIGHT_LOSS, WEIGHT_GAIN", "Direction of the energy target"],
         ["age", "Int32", "18\u201365 (client and form constraints)", "BMR term"],
         ["gender", "String (enum)", "MALE, FEMALE", "Selects the BMR constant"],
         ["height", "Double", "140\u2013210 cm", "BMR term and BMI denominator"],
         ["weight", "Double", "40\u2013180 kg", "Mass at plan creation"],
         ["todayWeight", "Double", "Updated by addWeight", "Most recent measured mass"],
         ["goal", "String (enum)", "MILD (15), MODERATE (20), AGGRESSIVE (25)", "Deficit or "
                                                                            "surplus percentage"],
         ["targetWeight", "Double", "Direction-checked and BMI-checked", "Goal mass"],
         ["duration", "Int32", "Within the derived 7\u201328 day/kg window", "Planned length "
                                                                             "in days"],
         ["activity", "String (enum)", "SEDENTARY 1.2 \u2026 ATHLETE 1.9", "Multiplier applied "
                                                                           "to BMR"],
         ["userId", "String", "Owner identifier taken from the security context", "Tenancy key "
                                                                                  "for every query"],
         ["active", "Boolean", "true on creation", "Single active plan per user"],
         ["createdAt", "Date", "LocalDate.now() at creation", "Day-count origin and archive "
                                                              "ordering"]],
        widths=[0.85, 0.8, 2.55, 2.3],
        font_size=7.2,
        caption="Data dictionary \u2014 collection diet_plans")

    st += [h3("4.7.3 diet_plan_tracks")]
    st += table(
        ["Field", "BSON type", "Constraint / domain", "Purpose"],
        [["_id", "ObjectId", "Driver-generated", "Track identifier"],
         ["weight", "Double", "Copied from the plan and updated by addWeight", "Mass on that "
                                                                                 "day"],
         ["tdee", "Double", "findTDEE(age, weight, height, gender, activity)", "Expenditure "
                                                                                "for that day"],
         ["intake", "Embedded { taken, total }", "total = calorie target; taken = 4P + 9F + 4C",
          "Calorie budget and consumption"],
         ["protein / carbs / fat", "Embedded { taken, total }", "total in grams from the "
                                                                "macro split", "Macro budget and consumption"],
         ["mealKcal", "Embedded MealKcal", "breakfast, lunch, snack, dinner, each a Macros "
                                           "object", "Per-meal targets and entries"],
         ["dayCount", "Int32", "ChronoUnit.DAYS.between(createdAt, today) + 1", "Streak "
                                                                                "counter"],
         ["createdAt", "Date", "Date of the tracking day", "Day key and archive ordering"],
         ["dietPlanId", "String", "Identifier of the owning plan", "Join key and ownership "
                                                                   "check"]],
        widths=[0.95, 1.15, 2.5, 1.9],
        font_size=7.2,
        caption="Data dictionary \u2014 collection diet_plan_tracks")

    st += [h3("4.7.4 ai_food_suggests")]
    st += table(
        ["Field", "BSON type", "Constraint / domain", "Purpose"],
        [["_id", "ObjectId", "Driver-generated", "Suggestion identifier"],
         ["name", "String", "Returned by the model", "Food name rendered as a card title"],
         ["calories", "Embedded { taken, total }", "Model figure mapped to the shared value "
                                                   "object", "Energy content"],
         ["macronutrients", "Embedded Macros", "protein, fat, carbs", "Macro figures"],
         ["description", "String", "Returned by the model", "One-line preparation summary"]],
        widths=[1.0, 1.2, 2.4, 1.9],
        font_size=7.2,
        caption="Data dictionary \u2014 collection ai_food_suggests")

    st += [h3("4.7.5 Embedded Value Objects")]
    st += table(
        ["Value object", "Composition", "Serialised shape"],
        [["Calories", "taken : double, total : double",
          "<font name='Mono' size='7'>{\"taken\": 1148.0, \"total\": 1850.0}</font>"],
         ["Macros", "protein, fat, carbs : Calories",
          "<font name='Mono' size='7'>{\"protein\": {\u2026}, \"fat\": {\u2026}, \"carbs\": {\u2026}}</font>"],
         ["MealKcal", "breakfast, lunch, snack, dinner : Macros",
          "<font name='Mono' size='7'>{\"breakfast\": {\u2026}, \"lunch\": {\u2026}, \u2026}</font>"],
         ["MetricsDTO", "title, taken, duration, currentDay, currentWeight, intake, protein, "
                        "carbs, fat, days[], weights[]",
          "Flat projection returned by GET /diet-plan/metrics"]],
        widths=[1.0, 2.8, 2.7],
        font_size=7.2,
        caption="Embedded value objects and their serialised shapes")

    st += [h3("4.7.6 Query Inventory and Access Patterns")]
    st += table(
        ["Repository method", "Predicate / projection", "Used by"],
        [["UserRepository.findByUsername", "username equality", "Authentication, username lookup"],
         ["UserRepository.existsByUsername / existsByEmail", "Existence check", "Registration "
                                                                                "duplicate detection"],
         ["DietPlanRepository.findByUserId", "userId equality", "GET /diet-plan/all"],
         ["DietPlanRepository.findByIdAndUserId", "id and owner equality", "Every plan-scoped "
                                                                           "read"],
         ["DietPlanRepository.findByUserIdAndActiveIsTrue", "userId equality and active = true",
          "Active-plan resolution"],
         ["DietPlanRepository.findByActiveTrue", "active = true", "Any-active-plan probe"],
         ["DietPlanRepository.findDietPlansHistoryByUserId",
          "@Query projection of id, title, plan, weight, targetWeight, duration, active, "
          "sorted by createdAt descending", "History list"],
         ["DietPlanRepository.findFirstDietPlansHistoryByUserId", "Same projection, first "
                                                                  "document", "Resume a past plan"],
         ["DietPlanTrackRepository.findFirstByCreatedAtAndDietPlanId", "date and plan "
                                                                       "equality", "Current day's document"],
         ["DietPlanTrackRepository.findByDateRangeAndDietPlanId",
          "@Query with $gte and $lte on createdAt, sorted ascending", "Seven-day weight series"],
         ["DietPlanTrackRepository.findAllDietPlanOverview",
          "@Query projection of weight, tdee, intake, protein, carbs, fat, createdAt sorted "
          "descending", "Archived day list"]],
        widths=[2.2, 2.7, 1.6],
        font_size=7.0,
        caption="Repository query inventory and access patterns")

    # ------------------------------------------------------------------
    st += [h2("4.8 Input Design, Output Design and Interface Design System")]
    st += [h3("4.8.1 Input Design")]
    st += [T.body(
        "Input is collected through five forms. Table 4.16 lists the fields of the plan form, "
        "which is the most constrained, together with the validation applied in the component "
        "and the independent validation applied on the server. The remaining forms "
        "(registration, log-in, meal entry and weight update) are single-purpose and are "
        "described in the module section of Chapter 6.")]
    st += table(
        ["Field", "Control", "Client validation", "Server validation"],
        [["title", "Text input", "Non-empty", "Not validated (informational)"],
         ["plan", "Two-state toggle", "One of the two enumerations", "Drives the direction rules"],
         ["age", "Number input", "18 \u2264 age \u2264 65", "Used directly in the BMR equation"],
         ["gender", "Two-state toggle", "MALE or FEMALE", "Selects the BMR constant"],
         ["height", "Number input", "140 \u2264 height \u2264 210 cm", "Denominator of the BMI check"],
         ["weight", "Number input", "40 \u2264 weight \u2264 180 kg", "Numerator of the BMI check"],
         ["goal", "Three-state toggle", "MILD, MODERATE or AGGRESSIVE", "Percentage of deficit "
                                                                        "or surplus"],
         ["activity", "Five-state toggle", "One of the five enumerations", "Multiplier 1.2 to 1.9"],
         ["targetWeight", "Number input", "Lower than current weight for loss, higher for "
                                          "gain; \u2265 40 kg and \u2264 110 kg", "BMI of the "
                                                                               "target must be \u2265 18 or \u2264 25"],
         ["duration", "Number input", "14 \u2264 duration \u2264 730 days", "Must lie inside "
                                                                            "the derived 7\u201328 day/kg window"]],
        widths=[0.95, 1.1, 2.55, 1.9],
        font_size=7.1,
        caption="Input design and two-level validation of the diet-plan form")

    st += [h3("4.8.2 Output Design")]
    st += [T.body(
        "Output is delivered in three forms: JSON resources consumed by the client, derived "
        "visual components (progress bars, metric cards and a line chart) and textual "
        "messages carried by the toast component. Table 4.17 shows representative request "
        "and response bodies for the two most important resources.")]
    st += table(
        ["Endpoint", "Request body", "Response body"],
        [["POST /diet-plan",
          "<font name='Mono' size='6.8'>{title, plan, age, gender, height, weight, goal, "
          "targetWeight, duration, activity}</font>",
          "<font name='Mono' size='6.8'>{id, title, plan, \u2026, userId, active, createdAt}</font>"],
         ["POST /diet-plan/{category}/{id}",
          "<font name='Mono' size='6.8'>{protein:{taken,total}, fat:{taken,total}, "
          "carbs:{taken,total}}</font>",
          "<font name='Mono' size='6.8'>{id, weight, tdee, intake, protein, carbs, fat, "
          "mealKcal, dayCount, createdAt, dietPlanId}</font>"],
         ["GET /diet-plan/metrics",
          "None (principal resolved from the token)",
          "<font name='Mono' size='6.8'>{title, taken, duration, currentDay, currentWeight, "
          "intake, protein, carbs, fat, days[], weights[]}</font>"],
         ["POST /ai-food-suggest",
          "<font name='Mono' size='6.8'>{mealFilter, foodFilter, cuisineFilter}</font>",
          "<font name='Mono' size='6.8'>[{name, calories:{taken,total}, "
          "macronutrients:{protein,fat,carbs}, description}]</font>"],
         ["Error (any handler)",
          "Not applicable",
          "<font name='Mono' size='6.8'>{\"error\": [\"message\"]}</font> with 400, 401, 404 "
          "or 410"]],
        widths=[1.45, 2.9, 2.3],
        font_size=7.0,
        caption="Representative request and response bodies")

    st += [h3("4.8.3 Interface Design System")]
    st += [T.body(
        "The client uses a single stylesheet that declares design tokens as CSS custom "
        "properties; every component stylesheet consumes those tokens rather than literal "
        "colours. The palette is teal-based, with the primary colour reserved for forward "
        "actions and for the active navigation item. Table 4.18 lists the tokens that appear "
        "most often in the interface.")]
    st += table(
        ["Token", "Value", "Applied to"],
        [["--color-primary", "#1a9c8a", "Primary buttons, active navigation, progress fill, "
                                        "avatar"],
         ["--color-primary-dark", "#13786b", "Hover state, section headings"],
         ["--color-primary-light", "#e6f7f5", "Selected chips, pale panels, active nav "
                                              "background"],
         ["--color-text / --color-text-muted", "#1f2937 / #6b7280", "Body copy and secondary "
                                                                    "labels"],
         ["--color-bg / --color-surface", "#f8fafb / #ffffff", "Page background and cards"],
         ["--color-border", "#e2e8e6", "Card outlines, dividers, inputs"],
         ["--color-danger / --color-warning", "#dc2626 / #d97706", "Error toast, over-target "
                                                                   "calorie bar"],
         ["--radius-sm / -md / -lg", "6 / 8 / 12 px", "Inputs, buttons, cards"],
         ["--space-xs \u2026 --space-2xl", "4 \u2026 48 px", "Consistent rhythm across "
                                                            "sections"],
         ["--font-family", "Inter, system-ui, sans-serif", "All interface text"],
         ["--shadow-sm / -md", "Subtle elevation", "Auth card, profile drop-down"],
         ["Card measure", "max-width 52 rem, centred", "Dashboard and form containers"]],
        widths=[1.7, 1.8, 3.0],
        font_size=7.2,
        caption="Interface design tokens of the client application")
    st += note_box(
        "Interface figures in Chapter 6 are renderings reconstructed from the implemented "
        "Angular templates and their scoped stylesheets. They reproduce the layout, wording "
        "and colour tokens of the delivered screens; they are not photographic captures of a "
        "running browser session, because the documentation environment used to produce this "
        "report had no Java runtime or MongoDB instance available. The distinction is stated "
        "here once and is not repeated for every figure.", "Note on figures")
    return st
