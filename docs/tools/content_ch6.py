"""Chapter 6 - Implementation."""

from __future__ import annotations

from reportlab.platypus import Paragraph, Spacer

import screens as SC
import theme as T
from theme import S, bullets, chapter, code_block, figure, h2, h3, note_box, numbered, table


def build():
    st = []
    st += chapter(6, "IMPLEMENTATION")

    # ------------------------------------------------------------------
    st += [h2("6.1 Implementation Overview")]
    st += [T.body(
        "The implementation is organised into eleven modules. Nine belong to the back end and "
        "two to the client; the boundary between them is the JSON contract described in "
        "Section 4.8. Table 6.1 lists the modules with the concrete artefacts that realise "
        "them and the number of source files each occupies, as counted in the repository.")]
    st += table(
        ["Module", "Tier", "Principal artefacts", "Files"],
        [["M1 Account registration and identity", "back end",
          "UserController, UserService, User, UserRepository, UserDTO", "6"],
         ["M2 Authentication, tokens and session", "back end",
          "SecurityConfig, AuthenticationFilter, JWTAuthenticationFilter, "
          "ExceptionHandlerFilter, CustomAuthenticationManager, JWTTokenService, "
          "SecurityConstants, UserSession", "8"],
         ["M3 Plan authoring and validation", "back end",
          "DietPlanController, DietPlanService (validation half), DietPlan, BodyMetricsRequest, "
          "BodyMetricsResponse", "6"],
         ["M4 Nutritional computation", "back end",
          "NutrientsCalculator, MacrosConstants, Calories, Macros, MealKcal", "5"],
         ["M5 Daily tracking and recomputation", "back end",
          "DietPlanService (tracking half), DietPlanTrack, DietPlanTrackRepository", "3"],
         ["M6 Metrics, status and reporting", "back end",
          "DietPlanService (metrics half), MetricsDTO, DietPlansHistoryDTO, "
          "DietPlanOverviewDTO", "4"],
         ["M7 AI food suggestion", "back end",
          "AIFoodSuggestController, AIFoodSuggestService, AIFoodSuggest, FilterDTO, "
          "LLMService, OpenRouterLLMService, ChatModel, MessageModel", "8"],
         ["M8 Error handling, mapping and configuration", "back end",
          "ApplicationExceptionHandler, ErrorResponse, BadRequestException, "
          "EntityNotFoundException, UnauthorizedException, Mapper, ModelMapperConfig, "
          "MongoConfig", "9"],
         ["M9 Client shell, routing and interception", "front end",
          "AppComponent, app.routes.ts, authGuard, TokenInterceptor, "
          "BaseUrlPrefixInterceptor, HeaderComponent, ToastComponent", "12"],
         ["M10 Client feature screens", "front end",
          "LoginComponent, SignupComponent, DashboardComponent, WeightTrackComponent, "
          "DietPlanComponent, DietPlanFormComponent, AIFoodSuggestComponent, "
          "DietPlansListComponent, DietPlanOverviewComponent, DietPlanTrackOverviewComponent, "
          "NoActiveDietPlanComponent, PageNotFoundComponent", "24"],
         ["M11 Service layer and models", "front end",
          "AuthService, DietPlanService, AIFoodSuggestService, DietPlanModel, Macros, Metrics, "
          "Toast, enumerations", "14"]],
        widths=[1.55, 0.7, 3.6, 0.55],
        font_size=6.9,
        caption="Module decomposition of the implementation")

    # ------------------------------------------------------------------
    st += [h2("6.2 Module Descriptions")]

    st += [h3("6.2.1 M1 \u2014 Account Registration and Identity")]
    st += [T.body(
        "Registration is handled by <font name='Mono' size='8'>POST /user/register</font>. "
        "The controller receives a <font name='Mono' size='8'>UserDTO</font>, and the service "
        "performs two independent existence checks before hashing: "
        "<font name='Mono' size='8'>existsByUsername</font> and "
        "<font name='Mono' size='8'>existsByEmail</font>. A duplicate raises "
        "<font name='Mono' size='8'>BadRequestException</font> with the offending field named "
        "in the message. The password is encoded with "
        "<font name='Mono' size='8'>BCryptPasswordEncoder</font> and only the digest is "
        "persisted. The endpoint is one of the two paths permitted without authentication, "
        "and it deliberately returns the created document without the password field.")]
    st += [T.body(
        "For the client, the sign-up form performs its own validation before any request is "
        "issued, and each rule has its own message. The username must be between three and "
        "twenty characters, must contain only letters and digits and must not begin with a "
        "digit. The e-mail address must match a simple "
        "<font name='Mono' size='8'>local@domain.tld</font> pattern. The password must be "
        "between eight and twenty characters and alphanumeric. A violation raises the toast "
        "component with the specific message, for example 'Password must be at least 8 "
        "characters long'. The form posts to the public registration path, so the token "
        "interceptor passes the request through untouched. On success the component navigates "
        "to <font name='Mono' size='8'>/dashboard</font>, but registration does not establish a "
        "session: the route guard then finds no valid access token and no refresh cookie, and "
        "redirects to the log-in screen, so the effective behaviour of a successful sign-up is a "
        "return to log-in with the account created.")]

    st += [h3("6.2.2 M2 \u2014 Authentication, Tokens and Session")]
    st += [T.body(
        "Authentication is implemented as a Spring Security filter pipeline of three custom "
        "filters placed around the framework's own. "
        "<font name='Mono' size='8'>ExceptionHandlerFilter</font> is registered before the "
        "authentication filter and wraps the remainder of the chain in a try-catch that "
        "translates token failures into plain-text responses: an expired token becomes HTTP "
        "401 with the body 'Access token expired', any other verification failure becomes 401 "
        "with 'JWT verification failed', and any other runtime exception becomes 400. "
        "<font name='Mono' size='8'>AuthenticationFilter</font> extends "
        "<font name='Mono' size='8'>UsernamePasswordAuthenticationFilter</font>, is bound to "
        "the path <font name='Mono' size='8'>/authenticate</font>, parses the JSON body into a "
        "<font name='Mono' size='8'>User</font>, and delegates the credential comparison to "
        "<font name='Mono' size='8'>CustomAuthenticationManager</font>. On success it does not "
        "return an access token: it generates the refresh token and writes it into an HttpOnly, "
        "SameSite=Lax cookie named <font name='Mono' size='8'>Refresh-Token</font> with a "
        "24-hour max-age. The access token is obtained separately from "
        "<font name='Mono' size='8'>POST /user/refresh</font>, which reads the cookie, verifies "
        "it and returns a 60-minute token in the response body.")]
    st += [T.body(
        "<font name='Mono' size='8'>JWTAuthenticationFilter</font> runs after the "
        "authentication filter on every request; it skips the two public paths, extracts the "
        "bearer header, verifies the signature and populates the security context with a "
        "<font name='Mono' size='8'>UsernamePasswordAuthenticationToken</font> whose principal "
        "is the username. Downstream, "
        "<font name='Mono' size='8'>UserSession</font> turns that principal into an owner "
        "identifier by looking the user up and returning the string form of the "
        "<font name='Mono' size='8'>ObjectId</font>; every repository predicate is built from "
        "that value. This is the single mechanism by which tenancy is enforced.")]
    st += [T.body(
        "The session is stateless: "
        "<font name='Mono' size='8'>SessionCreationPolicy.STATELESS</font> is configured, CSRF "
        "is disabled because no cookie-authenticated state-changing endpoint exists apart from "
        "refresh and log-out, and CORS is opened only to "
        "<font name='Mono' size='8'>http://localhost:4200</font> with credentials allowed.")]

    st += [h3("6.2.3 M3 \u2014 Plan Authoring and Validation")]
    st += [T.body(
        "Plan creation is a single service method, "
        "<font name='Mono' size='8'>DietPlanService.createDietPlan</font>, which sequences five "
        "steps: validate, stamp today's weight, stamp the owner and the active flag, persist the "
        "plan, and seed the first tracking document. The validation step is described in "
        "Algorithm 6.2. Because <font name='Mono' size='8'>updateDietPlan</font> simply "
        "delegates to <font name='Mono' size='8'>createDietPlan</font>, a plan update is "
        "semantically a new plan with the same fields: it receives a new identifier, a new "
        "creation date and a new day-1 track. The client uses this to implement resumption of "
        "an archived plan.")]
    st += [T.body(
        "The controller exposes the plan endpoints with explicit status semantics: "
        "<font name='Mono' size='8'>POST /diet-plan</font> returns the stored document, "
        "<font name='Mono' size='8'>PUT /diet-plan/update</font> the replaced document, "
        "<font name='Mono' size='8'>POST /diet-plan/tdee</font> a preview of expenditure "
        "without persistence, and the read endpoints return either a document or a list of "
        "projections. The TDEE preview exists so that the form can show the user the "
        "expenditure implied by the entered metrics before any commitment is made.")]

    st += [h3("6.2.4 M4 \u2014 Nutritional Computation")]
    st += [T.body(
        "<font name='Mono' size='8'>NutrientsCalculator</font> is a final class with a private "
        "constructor and twelve static methods; it holds no state and has no injected "
        "dependency, which makes it directly callable from a unit test. The methods fall into "
        "four groups: body indices (<font name='Mono' size='8'>findBMR</font>, "
        "<font name='Mono' size='8'>findBMI</font>, <font name='Mono' size='8'>findTDEE</font>), "
        "duration bounds (<font name='Mono' size='8'>findMinimumDuration</font>, "
        "<font name='Mono' size='8'>findMaximumDuration</font>), energy targets "
        "(<font name='Mono' size='8'>findDeficit</font>, <font name='Mono' size='8'>findSurplus</font>, "
        "<font name='Mono' size='8'>roundCalories</font>) and macronutrient allocation "
        "(<font name='Mono' size='8'>findProtein</font>, <font name='Mono' size='8'>findFat</font>, "
        "<font name='Mono' size='8'>findCarbs</font>, <font name='Mono' size='8'>macrosPercentage</font>, "
        "<font name='Mono' size='8'>calcTakenDeficit</font>, <font name='Mono' size='8'>calcTotalDeficit</font>). "
        "The enumerations carry the domain constants: "
        "<font name='Mono' size='8'>Activity</font> maps each level to its multiplier, "
        "<font name='Mono' size='8'>Goal</font> maps mild, moderate and aggressive to 15, 20 "
        "and 25, and <font name='Mono' size='8'>Gender</font> selects the sign term of the "
        "Mifflin\u2013St Jeor equation.")]

    st += [h3("6.2.5 M5 \u2014 Daily Tracking and Recomputation")]
    st += [T.body(
        "Tracking is built on one invariant: a tracking document always exists for the current "
        "date when a screen needs one. The resolver "
        "<font name='Mono' size='8'>findDietPlanTrackByDietPlanId</font> first verifies "
        "ownership of the plan, then looks up the document for "
        "<font name='Mono' size='8'>LocalDate.now()</font>, and if the lookup is empty it calls "
        "<font name='Mono' size='8'>createDietPlanTrack</font> instead of raising an error. The "
        "new document copies the plan's current weight, computes the elapsed day count as the "
        "number of days between the plan's creation date and today plus one, and is then "
        "filled by <font name='Mono' size='8'>processDietPlan</font>.")]
    st += [T.body(
        "<font name='Mono' size='8'>processDietPlan</font> is the point at which the two halves "
        "of the system meet. It computes expenditure from the plan's age, height, gender and "
        "activity together with the <i>track's</i> weight, converts expenditure into an intake "
        "target through the goal, derives the three macronutrient gram targets from that intake, "
        "and finally splits each target across the four meals. Because the method reads the "
        "weight from the track rather than the plan, a weight update on a given day changes that "
        "day's targets while leaving earlier days untouched.")]
    st += [T.body(
        "Meal entry is handled by <font name='Mono' size='8'>updateMacros</font>. It resolves "
        "today's document, selects the meal object by category using a switch expression over "
        "the four constants in <font name='Mono' size='8'>MacrosConstants</font>, copies the "
        "three recorded values, re-sums the daily totals in "
        "<font name='Mono' size='8'>adjustMacros</font> and finally recomputes consumed calories "
        "with the 4-9-4 conversion. An unknown category is not rejected by a switch expression "
        "with a default branch pointing at the snack; the controller validates the category "
        "against <font name='Mono' size='8'>MacrosConstants.validateMacro</font> before the "
        "service is called, so a typo becomes HTTP 400 rather than a silent write.")]

    st += [h3("6.2.6 M6 \u2014 Metrics, Status and Reporting")]
    st += [T.body(
        "The dashboard is served by one resource, "
        "<font name='Mono' size='8'>GET /diet-plan/metrics</font>, whose assembly is described "
        "in Algorithm 6.5. The service resolves the active plan, ensures today's document "
        "exists, obtains the seven-day window in the Asia/Kolkata zone, maps each document in "
        "that window to a three-letter weekday label and a weight, and finally projects the "
        "current document into a flat <font name='Mono' size='8'>MetricsDTO</font>. The "
        "percentage of the calorie goal is computed on the server as "
        "<font name='Mono' size='8'>round(taken / total \u00d7 100)</font> so that the client "
        "never divides.")]
    st += [T.body(
        "Two further endpoints support the plan lifecycle. "
        "<font name='Mono' size='8'>GET /diet-plan/status</font> compares the elapsed day count "
        "with the planned duration and, when the duration has been exceeded, sets "
        "<font name='Mono' size='8'>active = false</font> and returns true; the client uses this "
        "to route the user to the no-active-plan screen. "
        "<font name='Mono' size='8'>GET /diet-plan/active-plans</font> answers whether any "
        "plan in the database is active, which the router guard uses on a cold start. The "
        "archive is served by the history projection, the past-plan lookup and the overview "
        "query described in Table 4.15.")]

    st += [h3("6.2.7 M7 \u2014 AI Food Suggestion")]
    st += [T.body(
        "The suggestion module is a thin orchestration layer over an interface. "
        "<font name='Mono' size='8'>AIFoodSuggestService.suggestFood</font> obtains the calorie "
        "budget for the requested meal from "
        "<font name='Mono' size='8'>DietPlanService.getCaloriesByMealCategory</font>, builds the "
        "prompt, calls <font name='Mono' size='8'>LLMService.foodSuggestChat</font> and parses "
        "the response into a list of "
        "<font name='Mono' size='8'>AIFoodSuggest</font> objects with Jackson's "
        "<font name='Mono' size='8'>TypeReference</font>. The budget calculation re-uses the "
        "meal split: the snack, for example, is 15 per cent of each macro target, and the "
        "method converts those grams back into kilocalories with "
        "<font name='Mono' size='8'>calcTotalDeficit</font>. When no active plan exists the "
        "method catches <font name='Mono' size='8'>EntityNotFoundException</font> and returns a "
        "default budget of 500 kcal, which keeps the suggestion screen usable before a plan is "
        "created.")]
    st += [T.body(
        "<font name='Mono' size='8'>OpenRouterLLMService</font> is the only class that knows the "
        "provider. It posts a two-message conversation to "
        "<font name='Mono' size='8'>https://openrouter.ai/api/v1/chat/completions</font> with a "
        "bearer key read from configuration, a system message that fixes the JSON schema and "
        "ends with <font name='Mono' size='8'>/no_think</font> to suppress reasoning output, a "
        "temperature of 0.3 and streaming disabled. It then walks the response tree "
        "<font name='Mono' size='8'>choices[0].message.content</font> and returns the text of "
        "that node. Any malformed content surfaces as "
        "<font name='Mono' size='8'>JsonProcessingException</font>, which the global handler "
        "maps to HTTP 410 and the client renders as an inline error beneath the filter row.")]

    st += [h3("6.2.8 M8 \u2014 Error Handling, Mapping and Configuration")]
    st += [T.body(
        "Four exception types carry the domain's failure vocabulary: "
        "<font name='Mono' size='8'>EntityNotFoundException</font> (404), "
        "<font name='Mono' size='8'>BadRequestException</font> (400), "
        "<font name='Mono' size='8'>UnauthorizedException</font> (401) and Jackson's "
        "<font name='Mono' size='8'>JsonProcessingException</font> (410). "
        "<font name='Mono' size='8'>ApplicationExceptionHandler</font> is a "
        "<font name='Mono' size='8'>@ControllerAdvice</font> that maps each to an "
        "<font name='Mono' size='8'>ErrorResponse</font> record whose single field is a list of "
        "strings, so the body is always "
        "<font name='Mono' size='8'>{\"error\":[\"\u2026\"]}</font>. Client-side failures are "
        "handled separately by the toast component, which holds one message and one severity "
        "and dismisses itself after a timeout.")]
    st += [T.body(
        "Cross-cutting configuration is minimal by design. "
        "<font name='Mono' size='8'>ModelMapperConfig</font> registers a single mapper bean "
        "used to convert entities to DTOs where the shapes differ; "
        "<font name='Mono' size='8'>MongoConfig</font> builds a "
        "<font name='Mono' size='8'>MongoClientSettings</font> that names the database "
        "<font name='Mono' size='8'>macrova</font> explicitly, so the database name does not "
        "depend on the connection string; and "
        "<font name='Mono' size='8'>Mapper</font> in the shared package converts between "
        "<font name='Mono' size='8'>LocalDate</font> and <font name='Mono' size='8'>Date</font> "
        "for the range queries.")]

    st += [h3("6.2.9 M9 and M10 \u2014 Client Shell and Feature Screens")]
    st += [T.body(
        "The client is a standalone-component Angular application with no NgModule. The root "
        "component renders the header and a single router outlet. The header is hidden on the "
        "two authentication screens, which is why the log-in page is a full-height centred card "
        "rather than a page inside the shell. Routes are declared in "
        "<font name='Mono' size='8'>app.routes.ts</font>: the empty path redirects to "
        "<font name='Mono' size='8'>/dashboard</font>, the wildcard path redirects to the "
        "<font name='Mono' size='8'>not-found</font> route, and every component is imported "
        "eagerly rather than lazily, which is a deliberate simplification for an application of "
        "this size. Six routes are protected by "
        "<font name='Mono' size='8'>AuthGuard</font>: dashboard, progress, meals, history, "
        "diet-plan-form and no-active-plan. The two archive detail routes "
        "(<font name='Mono' size='8'>history/:id</font> and "
        "<font name='Mono' size='8'>history/track/:id</font>) carry no guard; they remain safe "
        "because the token interceptor still attaches the credential and because the service "
        "scopes every read to the authenticated owner, but the omission is an inconsistency that "
        "a later revision should correct.")]
    st += [T.body(
        "Two functional interceptors form the client half of the session protocol. "
        "<font name='Mono' size='8'>BaseUrlPrefixInterceptor</font> prefixes every relative URL "
        "with <font name='Mono' size='8'>/api</font>, which the development proxy rewrites to "
        "the service root. <font name='Mono' size='8'>TokenInterceptor</font> passes the three "
        "public paths through untouched; for every other request it asks "
        "<font name='Mono' size='8'>AuthService.isAuthenticated()</font>, which refreshes the "
        "access token when it is absent or expired, then clones the request with the bearer "
        "header and <font name='Mono' size='8'>withCredentials: true</font>. The combination is "
        "what makes the refresh cookie effective while keeping the access token in memory "
        "only.")]
    st += [T.body(
        "Feature state is held in Angular signals rather than in a store library. Each screen "
        "keeps its own signal for the loaded resource and derives its displays from it, which "
        "keeps the data flow one-directional and removes the need for a global store in an "
        "application of this size. Shared presentation is limited to the header, the toast and "
        "the design tokens; every other component owns its stylesheet.")]

    # ------------------------------------------------------------------
    st += [h2("6.3 Core Algorithms and Pseudocode")]
    st += [T.body(
        "Six algorithms carry the domain logic. They are presented as pseudocode in the order "
        "in which they execute during the life of a plan, and each is followed by the "
        "corresponding source excerpt in Section 6.4.")]

    st += [h3("6.3.1 Algorithm 6.1 \u2014 Derivation of Daily Targets")]
    st += code_block(
        """INPUT : age, gender, height (cm), weight (kg), activity, goal, plan
OUTPUT: tdee, intake, protein, fat, carbs (grams), mealKcal

1  bmr   <- 10*weight + 6.25*height - 5*age + (gender = MALE ? 5 : -161)
2  tdee  <- bmr * activity.multiplier
3  if plan = WEIGHT_LOSS then
4      intake <- round50(round(tdee) - pct(tdee, goal.percent))
5  else
6      intake <- round50(round(tdee) + pct(tdee, goal.percent - 10))
7  protein <- round(pct(intake, 30) / 4)
8  fat     <- round(pct(intake, 30) / 9)
9  carbs   <- round(pct(intake, 40) / 4)
10 mealKcal <- for each meal m in (breakfast 30, lunch 30, snack 15, dinner 25):
11                scale(protein, fat, carbs) by m.percent
12 return tdee, intake, protein, fat, carbs, mealKcal""",
        "Pseudocode for Algorithm 6.1")
    st += [T.body(
        "Three details of the pseudocode deserve comment because they are easy to misread in "
        "the source. First, the surplus branch subtracts ten percentage points from the goal "
        "before applying it, so a mild goal of 15 per cent produces a surplus of 5 per cent of "
        "expenditure; the offset exists because a gain plan also adds the energy cost of "
        "tissue synthesis, which the equation does not model. Second, the calorie target is "
        "rounded to the nearest fifty or hundred so that targets read as 1,850 rather than "
        "1,847. Third, the four meal percentages sum to one hundred, so the meal targets always "
        "reconstruct the daily target exactly; rounding is applied per macronutrient and may "
        "introduce a difference of one or two grams, which is visible in the interface and is "
        "acceptable.")]

    st += [h3("6.3.2 Algorithm 6.2 \u2014 Validation of a Plan Request")]
    st += code_block(
        """INPUT : plan request (plan, height, weight, targetWeight, duration)
OUTPUT: accepted, or BadRequestException carrying the permitted range

1  bmi <- weight_target / (height/100)^2
2  if plan = WEIGHT_LOSS and bmi < 18 then
3      reject(targetWeight + "kg is not the healthy weight")
4  if plan = WEIGHT_GAIN and bmi > 25 then
5      reject(targetWeight + "kg is not the healthy weight")
6  mass <- |weight - targetWeight|
7  min  <- plan = WEIGHT_LOSS ? ceil(mass * 7) : ceil(mass * 14)
8  max  <- ceil(mass * 28)
9  if duration < min or duration > max then
10     reject(min + "-" + max + " days are the healthy duration")
11 accept""",
        "Pseudocode for Algorithm 6.2")
    st += [T.body(
        "The duration bounds are derived rather than configured. A loss plan permits one "
        "kilogram per week at the fastest, which is seven days per kilogram, and a quarter of a "
        "kilogram per week at the slowest, which is twenty-eight days per kilogram; a gain plan "
        "permits half a kilogram per week at the fastest, which is fourteen days per kilogram, "
        "and shares the same slow bound. For a user of 76.5 kg aiming at 70 kg, the mass "
        "difference is 6.5 kg, so the permitted window is 46 to 182 days; a request for 30 days "
        "is rejected with the message '46-182 days are the healthy duration'.")]

    st += [h3("6.3.3 Algorithm 6.3 \u2014 Resolution and Seeding of the Current Day")]
    st += code_block(
        """INPUT : dietPlanId
OUTPUT: today's DietPlanTrack (existing or newly created)

1  plan <- findPlanByIdAndOwner(dietPlanId)      // 404 if absent or foreign
2  day  <- LocalDate.now()
3  track <- repository.findFirstByCreatedAtAndDietPlanId(day, plan.id)
4  if track is present then return track
5  dayCount <- DAYS.between(plan.createdAt, day) + 1
6  track <- new DietPlanTrack(plan.todayWeight, day, dayCount, plan.id)
7  processDietPlan(plan, track)                  // Algorithm 6.1
8  return repository.save(track)""",
        "Pseudocode for Algorithm 6.3")
    st += [T.body(
        "Step 1 is the ownership gate. Because the lookup combines the plan identifier with the "
        "authenticated user identifier, a request for another user's plan behaves exactly like "
        "a request for a plan that does not exist, and the client receives 404 rather than a "
        "hint that the identifier is valid. Step 7 is the only place where a tracking document "
        "obtains its targets.")]

    st += [h3("6.3.4 Algorithm 6.4 \u2014 Entry of a Meal and Recomputation of Totals")]
    st += code_block(
        """INPUT : dietPlanId, category, macros{protein,fat,carbs}.taken
OUTPUT: updated DietPlanTrack

1  track <- resolveCurrentDay(dietPlanId)        // Algorithm 6.3
2  meal  <- switch category of
3             "breakfast" -> track.mealKcal.breakfast
4             "lunch"     -> track.mealKcal.lunch
5             "dinner"    -> track.mealKcal.dinner
6             "snack"     -> track.mealKcal.snack
7  meal.protein.taken <- input.protein
8  meal.fat.taken     <- input.fat
9  meal.carbs.taken   <- input.carbs
10 for each macro in (protein, fat, carbs):
11     track.macro.taken <- sum over the four meals of macro.taken
12 track.intake.taken  <- 4 * protein.taken + 9 * fat.taken + 4 * carbs.taken
13 return repository.save(track)""",
        "Pseudocode for Algorithm 6.4")
    st += [T.body(
        "The recomputation is deliberately total rather than incremental: the service sums all "
        "four meals on every write instead of adding the difference. A sum over four objects "
        "is inexpensive, and it makes the operation idempotent, so a repeated submission of the "
        "same values cannot compound an error. Line 12 uses the energy densities rather than "
        "the calorie targets, so the recorded calorie figure is a function of the recorded "
        "grams alone.")]

    st += [h3("6.3.5 Algorithm 6.5 \u2014 Assembly of the Dashboard Metrics")]
    st += code_block(
        """INPUT : authenticated user
OUTPUT: MetricsDTO

1  plan  <- findActivePlanOfUser()               // 404 if none
2  track <- resolveCurrentDay(plan.id)           // Algorithm 6.3
3  (from, to) <- [today - 7 days 00:00, today 23:59:59.999] in Asia/Kolkata
4  days <- [], weights <- []
5  for each t in repository.findByDateRangeAndDietPlanId(from, to, plan.id):
6      days.append(shortWeekdayName(t.createdAt))
7      weights.append(t.weight)
8  taken <- round(track.intake.taken / track.intake.total * 100)
9  return { title: plan.title, taken, duration: plan.duration,
10          currentDay: track.dayCount, currentWeight: track.weight,
11          intake: track.intake.total, protein: track.protein.total,
12          carbs: track.carbs.total, fat: track.fat.total, days, weights }""",
        "Pseudocode for Algorithm 6.5")
    st += [T.body(
        "The seven-day window is computed with an explicit zone rather than with the server's "
        "default zone. This matters because the tracking documents are keyed by "
        "<font name='Mono' size='8'>LocalDate</font>: without an explicit zone the window can "
        "shift by a day on a host configured for UTC, and a Sunday entry can appear under "
        "Monday. The series therefore contains one point per tracked day inside the window, "
        "which may be fewer than seven if the user did not open the application on some days; "
        "the chart renders the points it receives rather than fabricating gaps.")]

    st += [h3("6.3.6 Algorithm 6.6 \u2014 Construction and Parsing of the Suggestion Call")]
    st += code_block(
        """INPUT : mealFilter, foodFilter, cuisineFilter
OUTPUT: list of AIFoodSuggest

1  kcal   <- caloriesOfMeal(mealFilter)          // 500 when no active plan
2  prompt <- "Suggest me 5 healthy {cuisine} cuisine {food} foods for {meal}
              under {kcal} calories."
3  system <- "Respond in JSON with this format: '{ name: string, calories: number,
              macronutrients: { protein, carbs, fat }, description: string }[]'.
              No other output. /no_think"
4  response <- POST openrouter/chat/completions
5                { model, messages: [system, prompt], temperature: 0.3, stream: false }
6  text <- response.choices[0].message.content
7  foods <- deserialise(text, List<AIFoodSuggest>)
8  return foods                       // JsonProcessingException -> HTTP 410""",
        "Pseudocode for Algorithm 6.6")
    st += [T.body(
        "The system message is doing three jobs at once: it fixes the schema, forbids "
        "surrounding prose, and suppresses the model's reasoning trace. The temperature of 0.3 "
        "trades variety for schema compliance, and the absence of a token limit means the "
        "provider applies its own default. Because the contract is enforced only by the prompt, "
        "the parse step is the real validation: a reply wrapped in a Markdown fence fails to "
        "deserialise, and the failure is surfaced rather than silently dropped.")]

    # ------------------------------------------------------------------
    st += [h2("6.4 Source Code Excerpts")]
    st += [T.body(
        "The excerpts below are reproduced from the repository with only whitespace and "
        "import statements removed. Each is followed by a short explanation of the decision it "
        "embodies.")]
    st += [h3("6.4.1 The Nutritional Engine")]
    st += code_block(
        """public static double findBMR(int age, double weight, double height, Gender gender) {
  return 10 * weight + 6.25 * height - 5 * age
      + (gender == Gender.MALE ? 5 : -161);
}

public static double findBMI(double height, double weight) {
  return (weight / (height * height)) * 10_000;
}

public static double findTDEE(int age, double weight, double height,
                              Gender gender, Activity activity) {
  return findBMR(age, weight, height, gender) * activity.getValue();
}""",
        "Basal metabolic rate, body-mass index and total daily energy expenditure")
    st += [T.body(
        "The three methods are deliberately free of rounding: they return the raw double and "
        "leave rounding to the caller that needs it. "
        "<font name='Mono' size='8'>findBMI</font> multiplies by ten thousand to convert "
        "centimetres to metres, so the method's unit contract is stated in its parameter names "
        "rather than assumed.")]

    st += [h3("6.4.2 Energy Targets and Duration Bounds")]
    st += code_block(
        """public static int findMinimumDuration(double mass, Plan plan) {
  return (int) Math.ceil(Plan.WEIGHT_LOSS.equals(plan) ? mass * 7 : (mass / 0.5) * 7);
}

public static int findMaximumDuration(double mass) {
  return (int) Math.ceil((mass / 0.25) * 7);
}

public static long roundCalories(long kcal) {
  long round = (kcal / 100) * 100;
  long difference = kcal - round;
  return round + (difference > 50 ? 100 : (difference > 0 ? 50 : 0));
}

public static long findDeficit(double tdee, int percent) {
  return roundCalories(Math.round(tdee - percentageOf(tdee, percent)));
}

public static long findSurplus(double tdee, int percent) {
  return roundCalories(Math.round(tdee) + percentageOf(tdee, percent - 10));
}""",
        "Duration window, calorie rounding and the deficit and surplus targets")
    st += [T.body(
        "The rounding helper is the most idiosyncratic method in the class: a remainder above "
        "fifty rounds up to the next hundred, a remainder between one and fifty rounds up to "
        "the next fifty, and a remainder of zero is left alone. Targets are therefore always "
        "multiples of fifty, which the interface exploits by formatting them without decimals. "
        "The surplus method's subtraction of ten percentage points is the only asymmetry "
        "between the two directions and is the reason a moderate gain plan of twenty per cent "
        "produces a ten per cent surplus.")]

    st += [h3("6.4.3 Macro Targets and Meal Split")]
    st += code_block(
        """public static double findProtein(double deficit) {
  return Double.valueOf(Math.round(percentageOf(deficit, 30) / 4.0));
}

public static double findFat(double deficit) {
  return Double.valueOf(Math.round(percentageOf(deficit, 30) / 9.0));
}

public static double findCarbs(double deficit) {
  return Double.valueOf(Math.round(percentageOf(deficit, 40) / 4.0));
}

public static Macros macrosPercentage(Macros macros, int percent) {
  return new Macros(
    percentageOf(macros.getProtein().getTotal(), percent),
    percentageOf(macros.getFat().getTotal(), percent),
    percentageOf(macros.getCarbs().getTotal(), percent));
}""",
        "Macronutrient gram targets and proportional scaling for a meal")
    st += [T.body(
        "Each macro method takes the calorie budget and returns grams, dividing by the energy "
        "density of the nutrient: four for protein and carbohydrate, nine for fat. "
        "<font name='Mono' size='8'>macrosPercentage</font> performs the meal split by scaling "
        "the <i>total</i> field of each macro rather than the taken field, which guarantees that "
        "meal targets and daily targets are consistent by construction.")]

    st += [h3("6.4.4 Plan Validation and Creation")]
    st += code_block(
        """private void validateDietPlan(DietPlan dietPlan) {
  double bmi = NutrientsCalculator.findBMI(dietPlan.getHeight(), dietPlan.getTargetWeight());
  if ((Plan.WEIGHT_LOSS.equals(dietPlan.getPlan()) && bmi < 18) ||
      (Plan.WEIGHT_GAIN.equals(dietPlan.getPlan()) && bmi > 25)) {
    throw new BadRequestException(dietPlan.getTargetWeight() + "kg is not the healthy weight");
  }
  double mass = dietPlan.getWeight() - dietPlan.getTargetWeight();
  int min = NutrientsCalculator.findMinimumDuration(mass, dietPlan.getPlan());
  int max = NutrientsCalculator.findMaximumDuration(mass);
  if (dietPlan.getDuration() < min || dietPlan.getDuration() > max) {
    throw new BadRequestException(min + "-" + max + " days are the healthy duration");
  }
}

public DietPlan createDietPlan(DietPlan dietPlan) {
  validateDietPlan(dietPlan);
  dietPlan.setTodayWeight(dietPlan.getWeight());
  dietPlan.setUserId(userSession.getAuthenticatedUserId());
  dietPlan.setActive(true);
  dietPlannerRepository.save(dietPlan);
  createDietPlanTrack(dietPlan);
  return dietPlan;
}""",
        "Validation and creation of a diet plan")
    st += [T.body(
        "The signed difference <font name='Mono' size='8'>mass</font> is passed to the duration "
        "methods without an absolute value; both bound methods multiply by a positive factor, "
        "and a negative mass can only arise when the target lies on the wrong side of the "
        "current weight, which the client prevents and which the body-mass index rule rejects "
        "in most cases. The creation method mutates the incoming entity rather than constructing "
        "a copy, which is safe because the entity is request-scoped and is not referenced after "
        "the response.")]

    st += [h3("6.4.5 Track Seeding and Target Processing")]
    st += code_block(
        """public DietPlanTrack findDietPlanTrackByDietPlanId(String dietPlanId) {
  DietPlan dietPlan = findDietPlanById(dietPlanId);
  return dietPlanTrackRepository
      .findFirstByCreatedAtAndDietPlanId(LocalDate.now(), dietPlanId)
      .orElseGet(() -> createDietPlanTrack(dietPlan));
}

private void processDietPlan(DietPlan dietPlan, DietPlanTrack dietPlanTrack) {
  dietPlanTrack.setTdee(NutrientsCalculator.findTDEE(
      dietPlan.getAge(), dietPlanTrack.getWeight(), dietPlan.getHeight(),
      dietPlan.getGender(), dietPlan.getActivity()));
  double intake = getIntake(dietPlanTrack.getTdee(), dietPlan.getGoal(), dietPlan.getPlan());
  dietPlanTrack.setIntake(new Calories(intake));
  dietPlanTrack.setProtein(new Calories(NutrientsCalculator.findProtein(intake)));
  dietPlanTrack.setFat(new Calories(NutrientsCalculator.findFat(intake)));
  dietPlanTrack.setCarbs(new Calories(NutrientsCalculator.findCarbs(intake)));
  dietPlanTrack.setMealKcal(splitForMealKcal(dietPlanTrack));
}""",
        "On-demand seeding of a tracking day and derivation of its targets")
    st += [T.body(
        "The single-argument constructor of <font name='Mono' size='8'>Calories</font> "
        "initialises the target and leaves the recorded field at the Java default of zero, so a "
        "day that has not yet been filled shows a zero-per-cent bar rather than a full one. "
        "That is the honest presentation: the target is known the moment the plan exists, while "
        "the recorded value is unknown until the user confirms what was eaten. Every write "
        "thereafter recomputes the recorded fields as described in Algorithm 6.4.")]

    st += [h3("6.4.6 Weight Update and Meal Entry")]
    st += code_block(
        """public DietPlanTrack addWeight(String dietPlanId, double weight) {
  DietPlan dietPlan = findDietPlanById(dietPlanId);
  dietPlan.setTodayWeight(weight);
  dietPlannerRepository.save(dietPlan);
  DietPlanTrack dietPlanTrack = findDietPlanTrackByDietPlanId(dietPlanId);
  dietPlanTrack.setWeight(weight);
  processDietPlan(dietPlan, dietPlanTrack);
  return dietPlanTrackRepository.save(dietPlanTrack);
}

public DietPlanTrack updateMacros(String dietPlanId, String category, Macros macros) {
  DietPlanTrack dietPlanTrack = findDietPlanTrackByDietPlanId(dietPlanId);
  Macros dietPlanMacros = getMacrosByCategory(dietPlanTrack.getMealKcal(), category);
  dietPlanMacros.getProtein().setTaken(macros.getProtein().getTaken());
  dietPlanMacros.getFat().setTaken(macros.getFat().getTaken());
  dietPlanMacros.getCarbs().setTaken(macros.getCarbs().getTaken());
  adjustMacros(dietPlanTrack);
  dietPlanTrack.getIntake().setTaken(calcDeficitTaken(dietPlanTrack));
  return dietPlanTrackRepository.save(dietPlanTrack);
}""",
        "Weight update with full recomputation, and meal entry with total recomputation")
    st += [T.body(
        "The weight update writes to three places in a fixed order: the plan's "
        "<font name='Mono' size='8'>todayWeight</font>, which the next day's seeding will "
        "inherit; the current track's weight, which the chart reads; and the derived targets, "
        "which <font name='Mono' size='8'>processDietPlan</font> recomputes. The meal entry "
        "mutates the meal object inside the document and then recomputes the aggregates; because "
        "the document is embedded, saving the outer object persists the change to the embedded "
        "object without any explicit update statement.")]

    st += [h3("6.4.7 Metrics Projection")]
    st += code_block(
        """public MetricsDTO getMetricsByDateRange() {
  List<String> days = new ArrayList<>();
  List<Double> weights = new ArrayList<>();
  Date[] dateRange = getOneWeekDateRange();
  DietPlan dietPlan = findDietPlanByUserId();
  DietPlanTrack dietPlanTrack = findDietPlanTrackByDietPlanId(dietPlan.getId());
  dietPlanTrackRepository
      .findByDateRangeAndDietPlanId(dateRange[0], dateRange[1], dietPlan.getId())
      .forEach(track -> {
        days.add(getDayName(track.getCreatedAt()));
        weights.add(track.getWeight());
      });
  return buildMetrics(dietPlanTrack, dietPlan.getTitle(), dietPlan.getDuration(), days, weights);
}

private Date[] getOneWeekDateRange() {
  ZoneId zoneId = ZoneId.of("Asia/Kolkata");
  LocalDate today = LocalDate.now(zoneId);
  return new Date[] {
      Date.from(today.minusWeeks(1).atStartOfDay(zoneId).toInstant()),
      Date.from(today.atTime(LocalTime.MAX).atZone(zoneId).toInstant()) };
}""",
        "Assembly of the seven-day window and of the metrics projection")
    st += [T.body(
        "Two lists are filled in parallel rather than a list of objects being mapped on the "
        "client, which keeps the payload small and the chart's input shape simple. The window "
        "starts at the first instant of the day seven days ago rather than at "
        "midnight of today minus seven, so a plan whose first day is exactly a week old "
        "contributes a point.")]

    st += [h3("6.4.8 The Security Filter Chain")]
    st += code_block(
        """AuthenticationFilter authenticationFilter =
    new AuthenticationFilter(customAuthenticationManager, jwtTokenService);
authenticationFilter.setFilterProcessesUrl("/authenticate");
http
  .csrf(csrf -> csrf.disable())
  .cors(cors -> cors.configurationSource(corsConfigurationSource()))
  .authorizeHttpRequests(auth -> auth
      .requestMatchers(HttpMethod.POST,
                       SecurityConstants.REGISTER_PATH,
                       SecurityConstants.REFRESH_PATH).permitAll()
      .anyRequest().authenticated())
  .addFilterBefore(new ExceptionHandlerFilter(), AuthenticationFilter.class)
  .addFilter(authenticationFilter)
  .addFilterAfter(new JWTAuthenticationFilter(jwtTokenService), AuthenticationFilter.class)
  .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS));
return http.build();""",
        "Construction of the stateless security filter chain")
    st += [T.body(
        "The ordering is the substance of the configuration. The exception filter must precede "
        "everything that can throw a token exception, the authentication filter must run before "
        "the JWT filter because it writes the cookie the latter's flow depends on, and the "
        "authorisation rule must run last. Permit-all is granted by HTTP method as well as by "
        "path, so a hypothetical <font name='Mono' size='8'>GET /user/register</font> would "
        "still require a token.")]

    st += [h3("6.4.9 Issue of the Refresh Cookie")]
    st += code_block(
        """@Override
protected void successfulAuthentication(HttpServletRequest request,
                                        HttpServletResponse response,
                                        FilterChain chain,
                                        Authentication auth) {
  String refreshToken = jwtTokenService.generateToken(
      auth.getName(), SecurityConstants.REFRESH_TOKEN_EXPIRATION);
  ResponseCookie cookie = ResponseCookie
      .from(SecurityConstants.REFRESH_TOKEN_HEADER, refreshToken)
      .httpOnly(true)
      .sameSite("Lax")
      .secure(false)
      .path("/")
      .maxAge(SecurityConstants.REFRESH_TOKEN_EXPIRATION)
      .build();
  response.setHeader(HttpHeaders.SET_COOKIE, cookie.toString());
}""",
        "Issue of the refresh token as an HttpOnly cookie")
    st += [T.body(
        "<font name='Mono' size='8'>httpOnly</font> removes the cookie from the reach of "
        "scripts, so a cross-site scripting flaw cannot exfiltrate the long-lived credential; "
        "<font name='Mono' size='8'>SameSite=Lax</font> prevents it from being sent on "
        "cross-site sub-requests while still allowing top-level navigation; and the path of "
        "the root makes it available to the refresh endpoint regardless of the deployment "
        "prefix. The <font name='Mono' size='8'>secure</font> flag is false because the "
        "development environment is served over plain HTTP; Section 7.7 records this as a known "
        "deviation from the OWASP guidance for production.")]

    st += [h3("6.4.10 The Token Interceptor of the Client")]
    st += code_block(
        """const PUBLIC_URLS = ['/authenticate', '/user/register', '/user/refresh'];

export const TokenInterceptor: HttpInterceptorFn = (req, next) => {
  if (PUBLIC_URLS.some((url) => req.url.includes(url))) {
    return next(req);
  }
  const authService = inject(AuthService);
  return authService.isAuthenticated().pipe(
    switchMap((isAuth) => {
      if (isAuth) {
        const token = authService.getAccessToken();
        const cloneReq = req.clone({
          setHeaders: { Authorization: `Bearer ${token}` },
          withCredentials: true,
        });
        return next(cloneReq);
      }
      return next(req);
    }),
  );
};""",
        "Functional HTTP interceptor that attaches the access token")
    st += [T.body(
        "<font name='Mono' size='8'>isAuthenticated()</font> is an observable rather than a "
        "boolean because it may have to perform a network call to refresh an expired token; "
        "the <font name='Mono' size='8'>switchMap</font> makes the interceptor wait for that "
        "call and then continue with the original request. The three public URLs are matched "
        "by substring, which also covers the prefixed forms produced by "
        "<font name='Mono' size='8'>BaseUrlPrefixInterceptor</font>.")]

    st += [h3("6.4.11 Repository Projections")]
    st += code_block(
        """public interface DietPlanRepository extends MongoRepository<DietPlan, String> {
  @Query(
    value = "{ userId:  ?0 }",
    fields = "{ _id: 1, title: 1, plan: 1, weight: 1, targetWeight: 1, duration: 1, active: 1 }",
    sort = "{ createdAt:  -1 }"
  )
  List<DietPlansHistoryDTO> findDietPlansHistoryByUserId(String userId);

  Optional<DietPlan> findByIdAndUserId(String id, String userId);

  Optional<DietPlan> findByUserIdAndActiveIsTrue(String userId);

  Optional<DietPlan> findByActiveTrue();
}""",
        "Derived queries and a field-projected history query")
    st += [T.body(
        "The history query returns a projection rather than documents because the archive "
        "screen needs seven fields and none of the body metrics. Because the projection "
        "includes the identifier under the name <font name='Mono' size='8'>_id</font>, the "
        "client receives it as <font name='Mono' size='8'>id</font> after Jackson's mapping, "
        "which is what the navigation links use.")]

    st += [h3("6.4.12 Global Exception Translation")]
    st += code_block(
        """@ControllerAdvice
public class ApplicationExceptionHandler {
  @ExceptionHandler
  public ResponseEntity<ErrorResponse> handleEntityNotFoundException(EntityNotFoundException e) {
    return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new ErrorResponse(e.getMessage()));
  }

  @ExceptionHandler
  public ResponseEntity<ErrorResponse> handleBadRequestException(BadRequestException e) {
    return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new ErrorResponse(e.getMessage()));
  }

  @ExceptionHandler
  public ResponseEntity<ErrorResponse> handleJsonProcessingException(JsonProcessingException e) {
    return ResponseEntity.status(HttpStatus.GONE).body(new ErrorResponse(e.getMessage()));
  }
}""",
        "Translation of domain exceptions into JSON error responses")
    st += [T.body(
        "The choice of 410 Gone for a malformed model response is unusual and deliberate: the "
        "resource that the client asked for is genuinely unavailable, and a 5xx code would "
        "wrongly suggest a defect in the service. Every handler returns the same body shape, "
        "so the client's error branch is written once.")]

    # ------------------------------------------------------------------
    st += [T.body("", "Body")]
    st += [h2("6.5 Screen Walkthroughs")]
    st += [T.body(
        "This section walks through the twelve interface states of the delivered client. As "
        "stated in the note at the end of Chapter 4, the figures are renderings reconstructed "
        "from the templates and scoped stylesheets, reproduced at the reference width of the "
        "application's centred content column.")]

    SCREENS = [
        ("Login", SC.login,
         "The log-in screen is the only entry point for an existing account. The card is "
         "centred vertically and horizontally, carries the product mark, and exposes exactly "
         "two fields plus a primary action. The footnote is a single line in which the lead "
         "text and the link are laid out with an explicit advance so that the two do not "
         "overlap at small widths. The card is hidden from the application shell, so the "
         "header is absent."),
        ("Sign up", SC.signup,
         "Registration collects three fields: a username, an e-mail address and a password. "
         "Three families of rule are enforced before the request is sent — a username of "
         "three to twenty alphanumeric characters that does not begin with a digit, an e-mail "
         "matching the local@domain pattern, and a password of eight to twenty alphanumeric "
         "characters. A violation raises the toast shown at the foot of the card, which names "
         "the specific rule that failed, rather than a browser-native validation bubble, so the "
         "message is styled and announced consistently with every other error in the "
         "application."),
        ("Dashboard", SC.dashboard,
         "The dashboard is the landing page after authentication. It answers four questions at "
         "a glance: how much of today's calorie budget has been used (the 62 per cent bar), how "
         "many consecutive days have been tracked (the 12 of 60 streak), what the macro targets "
         "are (the three metric cards), and how body weight has moved over the last week (the "
         "line chart, which falls from 75.6 kg to 74.2 kg across the seven labelled weekdays). "
         "The chart is rendered by Chart.js on a canvas whose height is fixed so that the "
         "caption cannot collide with the axis labels."),
        ("Progress", SC.progress,
         "The progress screen is the tracking surface. The daily summary card repeats the "
         "calorie position and offers the weight-update control; beneath it, four meal cards "
         "show the required grams for protein, carbohydrate and fat alongside editable fields "
         "for what was actually eaten, with an Update action per card. The requirement figures "
         "are the 30/30/15/25 split of the daily targets, so breakfast shows 32 g of protein "
         "where the daily target is 107 g."),
        ("Diet plan form", SC.plan_form,
         "The plan form is the most constrained screen. Direction (loss or gain), gender, goal "
         "and activity are segmented controls rather than drop-downs, which makes the permitted "
         "values visible without interaction; age, height, weight, target weight and duration "
         "are numeric inputs with bounds stated in the labels. The helper line beneath the "
         "duration field states the permitted window for the current mass difference, and the "
         "toast at the foot illustrates the rejection of a target weight on the wrong side of "
         "the current weight."),
        ("Meals", SC.meals,
         "The suggestion screen combines three filters \u2014 meal, dietary preference and "
         "cuisine \u2014 with a single primary action. Each returned food is rendered as a card "
         "with its energy and its three macronutrient figures, so the user can compare "
         "candidates against the remaining budget of the selected meal without leaving the "
         "page."),
        ("Plan history", SC.history,
         "The history screen lists every plan of the authenticated user in reverse "
         "chronological order. Each row carries the title, the direction, the starting and "
         "target weights, the planned duration and a status pill that distinguishes the active "
         "plan from completed ones; the row itself is a link to the archived day list."),
        ("Plan overview", SC.overview,
         "The plan overview lists the tracking days of one plan. Each entry shows the date, the "
         "weight recorded on that day, the expenditure computed for it and the intake and macro "
         "values that were in force, which is what makes the archive auditable after the plan "
         "has ended."),
        ("Tracked day", SC.track_detail,
         "A tracked day is presented read-only, in the same visual language as the progress "
         "screen but without the Update actions. The read-only form is a deliberate design "
         "decision: history is evidence, and an application that allowed a past day to be "
         "edited would undermine the integrity of the weight trend."),
        ("No active plan", SC.no_plan,
         "When no plan is active, the guarded routes redirect here. The screen offers two "
         "mutually exclusive paths: create a new plan, or continue the most recent archived "
         "plan, which pre-fills the form from the last plan and submits it as a new plan. The "
         "illustration is the repository's own asset, not a stock image."),
        ("Page not found", SC.not_found,
         "The wildcard route renders a minimal 404 page with a single action back to the "
         "dashboard. It exists so that a mistyped URL cannot produce a blank outlet."),
        ("Session states", SC.dropdown,
         "The profile menu exposes the signed-in identity and the two session actions. The "
         "figure also shows the failure toast raised by an incorrect password and the table "
         "that summarises how each client state maps to a session state: no cookie, refresh "
         "cookie only, and access token present."),
    ]
    for i, (name, fn, text) in enumerate(SCREENS, start=1):
        st += [h3(f"6.5.{i} Screen 6.{i} \u2014 {name}")]
        st += figure(fn(), f"Interface rendering \u2014 {name.lower()} screen")
        st.append(T.body(text))

    return st
