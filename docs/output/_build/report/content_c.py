"""Chapters 9 to 12, the references and the appendices."""


def build(doc):
    # ================================================================== CHAPTER 9
    doc.chapter_heading(9, "User Interface Design and Application Screens", key="ch9")
    doc.h2("9.1", "Design Objectives", key="s9.1")
    doc.p(
        "The interface was designed against four objectives that follow from the analysis in Chapter 3. "
        "First, every screen must state its purpose in a single line beneath the heading, so that a "
        "first-time user does not have to infer what the screen is for. Second, every screen must have "
        "exactly one primary action, rendered in the brand colour and at full width where the action "
        "concludes a form. Third, numeric feedback must be immediate: an update to a logged value "
        "re-renders the calorie meter from the response, and the dashboard recomputes the percentage "
        "from stored documents rather than from client-side arithmetic. Fourth, the application must "
        "never present an empty layout; a missing plan, an expired plan and an unknown route each "
        "resolve to a designed screen."
    )
    doc.p(
        "The screens are presented in the order in which a new user encounters them, which is also the "
        "order of the numbered screenshot files captured during the demonstration. Every screenshot in "
        "this chapter was taken in a browser window of 1921 by 978 pixels; the browser chrome and the "
        "empty canvas around the content have been trimmed from each capture, and every figure "
        "preserves the aspect ratio of the original."
    )

    doc.h2("9.2", "Registration and Authentication Screens", key="s9.2")
    doc.h3("9.2.1", "Create Account Screen", key="s9.2.1")
    doc.p(
        "The signup screen presents three fields, a username, an e-mail address and a password, inside a "
        "single card centred in the viewport, with the brand mark in the header and a log-in button "
        "offered for a returning user. The card carries the heading 'Create account' and the supporting "
        "line 'Start tracking your nutrition today', which is the pattern of heading plus one-line "
        "purpose that recurs across the application. Validation is client-side at this point: the "
        "submit handler checks that the username is between three and twenty characters, contains only "
        "letters and digits and does not begin with a digit, that the address matches a simple pattern, "
        "and that the password is between eight and twenty characters. A failure displays a toast and "
        "returns without issuing a request, which is why the screen appears unchanged in the capture."
    )
    doc.figure("shots/shot-1.png",
               "Create account screen with the three-field registration form", width=5.2)
    doc.h3("9.2.2", "Log In Screen", key="s9.2.2")
    doc.p(
        "The login screen is the mirror image of the registration screen: two fields, a single "
        "full-width primary button and a link to registration. On initialisation the component calls "
        "the authentication check, which means that a user who already holds a valid session is "
        "redirected to the dashboard without ever seeing the form. A failed attempt produces a toast "
        "stating that the credentials were rejected, using the same message for an unknown username and "
        "a wrong password in order not to disclose which accounts exist."
    )
    doc.figure("shots/shot-2.png",
               "Log in screen with the credential form and the registration link", width=5.2)

    doc.h2("9.3", "Empty State and Plan Initiation", key="s9.3")
    doc.h3("9.3.1", "No Active Diet Plan Screen", key="s9.3.1")
    doc.p(
        "A user who has authenticated but holds no active plan is routed to the no-active-plan screen. "
        "The screen consists of a small illustration, the heading 'No Active Diet Plan', two sentences "
        "of explanation and a single primary action that opens the wizard. The component also loads the "
        "most recent plan, so that a returning user can be offered the option of reviewing the previous "
        "one; the capture shows the state before any plan has ever been created, in which that option is "
        "legitimately absent."
    )
    doc.figure("shots/shot-3.png",
               "Empty state shown when the authenticated user has no active diet plan", width=5.2)

    doc.h2("9.4", "Plan Construction Wizard", key="s9.4")
    doc.p(
        "The wizard occupies a single route and renders one of four steps beneath a horizontal step "
        "indicator. The indicator consists of four numbered circles connected by rules; the current "
        "step is filled with the primary colour, completed steps are filled with a tint and subsequent "
        "steps are outlined. Because the current step is derived from the server's form status rather "
        "than from a client variable, the indicator is always consistent with what is stored, including "
        "after a page reload."
    )
    doc.h3("9.4.1", "Step 1 \u2014 Body Metrics", key="s9.4.1")
    doc.p(
        "The first step collects the eight values that determine the energy estimate. The plan name is "
        "a free-text field; the plan type, the sex and the activity level are pill selectors; age, "
        "height, current weight and target weight are numeric inputs whose plausible range is stated "
        "inside the label. The range statement is not decoration: the same bounds are enforced in the "
        "submit handler, which is why the capture shows ranges for age, height and current weight. The "
        "primary action is the only button on the card and is rendered at full width in the brand "
        "colour."
    )
    doc.figure("shots/shot-4.png",
               "Wizard step 1 \u2014 body metrics, plan type and activity selection", width=4.0)
    doc.h3("9.4.2", "Step 2 \u2014 Goal and Duration", key="s9.4.2")
    doc.p(
        "The second step presents the energy estimate that the server has just computed and asks for the "
        "intensity of the intervention. A summary strip at the top repeats the daily energy need, the "
        "current weight and the target weight, which anchors the three choices that follow. Each "
        "intensity is a full-width selectable card with a title, a one-sentence explanation, a badge "
        "stating the character of the option and the percentage that it applies. The selected card "
        "receives a tinted background and a coloured border. Duration is a second pill group with three "
        "values, and the primary action advances to the third step."
    )
    doc.p(
        "One detail of this screen is inaccurate and is recorded rather than corrected. The card for the "
        "mild intensity is labelled as a ten per cent deficit, while the enumeration that the service "
        "applies carries fifteen per cent. The label is hard-coded presentation text and the arithmetic "
        "is correct, so a user who selects the mild option receives a slightly larger deficit than the "
        "screen promises. The finding appears again in Section 11.3, and the correction is to render the "
        "label from the enumeration value."
    )
    doc.figure("shots/shot-5.png",
               "Wizard step 2 \u2014 goal intensity, energy summary and plan duration", width=4.0)
    doc.h3("9.4.3", "Step 3 \u2014 Meal Preferences", key="s9.4.3")
    doc.p(
        "The third step converts the energy target into grams. A three-column summary strip shows the "
        "current calories, the target calories and the maintenance requirement, which makes the size of "
        "the deficit visible at a glance. Below it, a row of five tabs selects a macronutrient preset; "
        "the selected preset populates three sliders, one for each macronutrient, whose current values "
        "are displayed as grams on the right. Moving a slider switches the preset to custom and "
        "recalculates the energy total from the three gram values. The remaining controls are a "
        "diet-type group, a meal-count group and a yes-or-no group for the evening snack."
    )
    doc.figure("shots/shot-6.png",
               "Wizard step 3 \u2014 macronutrient split, diet type and meal structure", width=4.0)
    doc.h3("9.4.4", "Step 4 \u2014 Review and Confirmation", key="s9.4.4")
    doc.p(
        "The final step renders the complete plan as a read-only summary organised in three labelled "
        "sections, one for the body metrics, one for the goal and calories and one for the meal "
        "preferences, with a plan-type badge in the corner and a row of three macro chips at the bottom. "
        "The screen exists because it is the last opportunity to detect an input error before activation "
        "and because the document it displays is the document that will be stored. The single primary "
        "action posts to the activation endpoint, and the host component navigates to the dashboard on "
        "success."
    )
    doc.figure("shots/shot-7.png",
               "Wizard step 4 \u2014 review of body metrics, goal, calories and macro split", width=4.0)

    doc.h2("9.5", "Dashboard", key="s9.5")
    doc.p(
        "The dashboard is the landing page after authentication and the screen the user sees most often. "
        "Its layout is a vertical stack of three regions. The goal region shows the percentage of the "
        "daily target achieved and a horizontal meter whose fill is capped at one hundred per cent. Two "
        "rows of three metric cards follow: the first row shows the streak as the current day over the "
        "total duration, the current weight and the daily energy target; the second row shows the "
        "protein, carbohydrate and fat targets. The final region is the weight trend chart, which plots "
        "the recorded weights against the abbreviated weekday names of the sampled days."
    )
    doc.p(
        "Figures 9.8 and 9.9 show the same screen at two moments. In the first, taken immediately after "
        "the plan was activated, the streak stands at one of one hundred and eighty days, the chart "
        "holds a single observation, and the goal meter is empty because no intake has yet been logged. "
        "In the second, taken after four days of logging, the streak reads four, the current weight has "
        "fallen from ninety-five to ninety-four point one five kilograms, the goal meter is at "
        "seventy-nine per cent and the chart shows a monotonic decline across four observations. The "
        "pair is included because it demonstrates the feedback loop described in Section 2.2.5 rather "
        "better than either capture alone."
    )
    doc.figure("shots/shot-8.png",
               "Dashboard on the first day of an activated plan \u2014 initial state", width=4.2)
    doc.figure("shots/shot-10.png",
               "Dashboard after four days of logging \u2014 goal progress and weight trend", width=4.4)

    doc.h2("9.6", "Daily Tracking Screen", key="s9.6")
    doc.p(
        "The tracking screen, reached through the progress link in the header, opens with the daily "
        "summary card. That card contains a read-only day number, an editable current weight and a "
        "button that commits the weight, followed by the calorie meter, which displays the consumed "
        "energy against the daily target. Below the summary, four meal cards are rendered by a single "
        "template instantiated once per category. Each card carries the category name, three numeric "
        "inputs whose labels state the required grams for that meal, and a button that commits the three "
        "values for that category only."
    )
    doc.p(
        "The capture shows partial adherence, which is the ordinary case: breakfast and lunch have been "
        "logged at seventy grams of carbohydrate, forty-five of protein and twenty-five of fat, the "
        "snack at thirty, twenty and fifteen, and dinner has not yet been logged. The meter reflects "
        "exactly that, and the server's response to the last update is what produced the numbers on the "
        "screen. The three required figures printed in the input labels are the per-meal split of the "
        "plan's macros, which is the property that makes the screen a plan rather than a diary."
    )
    doc.figure("shots/shot-9.png",
               "Daily tracking screen with the summary card and the four editable meal cards", width=3.3)

    doc.h2("9.7", "AI Food Suggestion Screen", key="s9.7")
    doc.p(
        "The suggestion screen presents four filter rows, one each for the meal, the meal type, the diet "
        "and the cuisine, rendered as rows of pill buttons with a single active option, followed by a "
        "primary action that requests the suggestions. Results are rendered as an ordered list of cards, "
        "each carrying a rank, a dish name, a descriptive paragraph and a footer with the reported "
        "energy and the three macronutrient values. The screen has three states beyond the initial "
        "prompt: a loading indicator, the results list and an error message, all driven by two boolean "
        "flags in the component."
    )
    doc.p(
        "The capture shows five Indian vegetarian dinner suggestions for a balanced diet, each under the "
        "allowance that the server computed for the dinner category of the active plan. A caveat "
        "applies to every number in this figure: the values are generated by the model and are not "
        "verified against a food-composition database, as documented in Sections 6.4 and 11.4."
    )
    doc.figure("shots/shot-11.png",
               "AI food suggestion screen with four filters and five generated suggestion cards",
               width=3.3)

    doc.h2("9.8", "Plan History and Day-by-Day Review", key="s9.8")
    doc.h3("9.8.1", "Diet Plans History", key="s9.8.1")
    doc.p(
        "The history list is a vertical sequence of rows, each of which carries the plan title, a status "
        "badge that distinguishes an active plan from an inactive one, a metadata line with the plan "
        "type, the weight transition and the duration, and a chevron that opens the day-by-day view. The "
        "capture shows three plans created in sequence, of which only the most recent is active, which "
        "illustrates the lifecycle described in Section 4.5.4: the earlier plans were completed or "
        "superseded and are retained with the inactive status rather than deleted."
    )
    doc.figure("shots/shot-12.png",
               "Diet plans history with status badges and weight transitions", width=5.2)
    doc.h3("9.8.2", "Past Tracking Entries", key="s9.8.2")
    doc.p(
        "Selecting a plan opens the list of its daily documents, ordered by date descending. Each entry "
        "shows the date and a metadata line with the weight recorded on that day, the plan's expenditure "
        "and the energy consumed, followed by a second line with the three macronutrient totals. The "
        "card therefore reads as a comparison between what the plan allowed and what the user actually "
        "logged, placed beside the weight that was current when the entry was recorded. In the capture "
        "the expenditure is 2645 and the consumed energy is 1705 on every one of the four days, because "
        "the demonstration logged the same values on each day; the weight column remains at the initial "
        "95 kilograms because the weight update was applied to the current day only, which is why the "
        "dashboard of Figure 9.9 reports 94.15 kilograms as the current weight while the stored days "
        "still carry the earlier figure."
    )
    doc.figure("shots/shot-13.png", "Day-by-day tracking entries of a single plan", width=5.2)
    doc.h3("9.8.3", "Read-Only Review of a Stored Day", key="s9.8.3")
    doc.p(
        "The final history screen shows one stored document exactly as it was recorded. It reproduces "
        "the daily summary and the four meal cards, but the inputs are disabled and no update button is "
        "rendered, which enforces the principle that history is a record rather than a workspace. The "
        "capture shows the values stored for the ninth of November 2026, which are the values that the "
        "tracking screen of Figure 9.10 submitted, presented without the editing affordances. The "
        "heading is built from the stored date, which is why it reads as a possessive construction "
        "rather than as a fixed title; that is a presentation detail a future revision should reformat."
    )
    doc.figure("shots/shot-14.png",
               "Read-only review of the macronutrient log stored for a single day", width=3.5)

    doc.h2("9.9", "Error and Fallback Screens", key="s9.9")
    doc.p(
        "The not-found screen is rendered for any route that does not match the route table. It presents "
        "a large numeral in a tint of the brand colour, the heading 'Page not found', a one-line "
        "explanation and a single primary action that returns the user to the dashboard. The header "
        "remains visible and functional, so the screen is a recoverable state rather than a dead end. "
        "The same component is reached programmatically when a request resolves to a not-found response, "
        "which is why the numeral is large: it doubles as an error signal in that case."
    )
    doc.figure("shots/shot-15.png", "Not-found screen rendered for an unmatched route", width=5.2)
    doc.p(
        "The two fallback screens are the smallest in the application and the ones most often omitted from "
        "a student project, which is why they are reproduced here. Their value is not aesthetic. A user "
        "who has completed a plan and returns a month later must be told why the dashboard is no longer "
        "available rather than shown an empty shell, and a user who mistypes a route must be offered a way "
        "back rather than left with a blank page. Both states are reachable in the delivered build: the "
        "empty state is what a reviewer sees before any plan has been created, and the not-found screen is "
        "what appears when the address is edited by hand."
    )

    doc.pagebreak()
    doc.h2("9.10", "Consistency Observations", key="s9.10")
    doc.p(
        "Reviewing the fifteen screens together reveals a consistent visual language and three "
        "inconsistencies that a future revision should correct. The consistent elements are the card "
        "surface with an eight-pixel radius and a one-pixel border, the pill selector, the primary "
        "button, the heading-plus-subtitle pattern, and the metric card with its uppercase label and "
        "inline unit. The inconsistencies are as follows. The authentication screens use a single "
        "centred column while the wizard uses a wider two-column grid, so the card widths differ between "
        "the two contexts. The dashboard uses the plan title as the page heading, whereas every other "
        "screen uses a fixed heading and displays the plan title as data. And the history screens use a "
        "chevron affordance that appears nowhere else in the application."
    )
    doc.table(
        "Screen inventory: route, data source and primary action of each screen",
        ["Figure", "Screen", "Route", "Data source", "Primary action"],
        [
            ["9.1", "Create account", "/signup", "None", "Sign up"],
            ["9.2", "Log in", "/login", "None", "Log in"],
            ["9.3", "No active plan", "/no-active-plan", "Past plan projection", "Create new plan"],
            ["9.4", "Body metrics", "/diet-plan-form", "Form status", "Calculate my calories"],
            ["9.5", "Goal and duration", "/diet-plan-form", "Goal selection", "Proceed"],
            ["9.6", "Meal preferences", "/diet-plan-form", "Meal preference", "Preview my plan"],
            ["9.7", "Review", "/diet-plan-form", "Plan activation", "Generate my diet plan"],
            ["9.8", "Dashboard, day 1", "/dashboard", "Metrics", "None; navigation only"],
            ["9.9", "Dashboard, day 4", "/dashboard", "Metrics", "None; navigation only"],
            ["9.10", "Daily tracking", "/progress", "Tracking document", "Update, per meal"],
            ["9.11", "AI suggestions", "/meals", "Suggestion endpoint", "Get suggestions"],
            ["9.12", "Plan history", "/history", "History projection", "Open a plan"],
            ["9.13", "Past entries", "/history/:id", "Overview projection", "Open a day"],
            ["9.14", "Stored day", "/history/track/:id", "Tracking document", "None; read-only"],
            ["9.15", "Not found", "/not-found", "None", "Back to dashboard"],
        ],
        widths=[7, 18, 21, 32, 22], font_size=7.4)

    # ================================================================= CHAPTER 10
    doc.chapter_heading(10, "Algorithms and Implementation Details", key="ch10")
    doc.h2("10.1", "Overview", key="s10.1")
    doc.p(
        "This chapter documents the six algorithms on which the correctness of the application depends. "
        "For each one the mathematical definition is stated first, the implementation is then "
        "reproduced from the repository and explained, and the observable consequences are recorded "
        "against the worked example that runs through the report: a twenty-five-year-old man, 175 "
        "centimetres tall and 95 kilograms at the start of the plan, with a target weight of 75 "
        "kilograms, a light activity level and a moderate weight-loss goal over 180 days."
    )

    doc.h2("10.2", "Basal Metabolic Rate \u2014 Mifflin\u2013St Jeor", key="s10.2")
    doc.p(
        "Basal metabolic rate is estimated with the Mifflin\u2013St Jeor equation, which expresses "
        "resting energy expenditure as a linear function of mass, height and age with a sex-specific "
        "constant. Writing w for weight in kilograms, h for height in centimetres and a for age in "
        "years, the equation is ten w plus six point two five h minus five a plus five for men, and the "
        "same expression minus one hundred and sixty-one for women. The two constants differ by one "
        "hundred and sixty-six kilocalories, which is the equation's model of the mean difference in "
        "body composition between the sexes."
    )
    doc.code("Listing 10.1 \u2014 the basal rate method",
             "public static double findBMR(\n"
             "  int age, double weight, double height, Gender gender\n"
             ") {\n"
             "  return (\n"
             "    10 * weight + 6.25 * height - 5 * age\n"
             "      + (gender == Gender.MALE ? 5 : -161)\n"
             "  );\n"
             "}")
    doc.p(
        "The implementation is a direct transcription and introduces no rounding, which is deliberate: "
        "the value is carried forward as a double and rounded once, when the expenditure is written into "
        "the plan. For the worked example the basal rate is 950 plus 1093.75 minus 125 plus 5, which is "
        "1923.75 kilocalories per day."
    )

    doc.h2("10.3", "Total Daily Energy Expenditure", key="s10.3")
    doc.p(
        "Total daily energy expenditure multiplies the basal rate by a physical-activity factor. Macrova "
        "stores the five factors as the constructor argument of an enumeration, so that each multiplier "
        "is a property of a named constant rather than a literal inside the arithmetic."
    )
    doc.code("Listing 10.2 \u2014 the activity enumeration and the expenditure method",
             "public enum Activity {\n"
             "  SEDENTARY(1.2), LIGHT(1.375), MODERATE(1.55), HARD(1.725), ATHLETE(1.9);\n"
             "  private final double value;\n"
             "  Activity(double value) { this.value = value; }\n"
             "  public double getValue() { return value; }\n"
             "}\n"
             "\n"
             "public static double findTDEE(\n"
             "  int age, double weight, double height, Gender gender, Activity activity\n"
             ") {\n"
             "  return findBMR(age, weight, height, gender) * activity.getValue();\n"
             "}")
    doc.table(
        "Activity factors and the expenditure they produce for the worked example",
        ["Activity level", "Multiplier", "Expenditure at a basal rate of 1923.75",
         "Rounded value stored"],
        [
            ["Sedentary", "1.2", "2308.50", "2309"],
            ["Light", "1.375", "2645.16", "2645"],
            ["Moderate", "1.55", "2981.81", "2982"],
            ["Hard", "1.725", "3318.47", "3318"],
            ["Athlete", "1.9", "3655.13", "3655"],
        ],
        widths=[22, 18, 34, 26], font_size=8.4)
    doc.p(
        "The rounding is performed by the caller: the first wizard step stores the rounded expenditure, "
        "which is why the final column of the table shows whole numbers. The rounding is to the nearest "
        "kilocalorie and is applied once, so every later stage works from the rounded value and a "
        "recomputation from the stored value reproduces the stored target."
    )

    doc.h2("10.4", "Target Calories \u2014 Deficit and Surplus", key="s10.4")
    doc.p(
        "The daily target is obtained by applying an intensity to the expenditure. For a weight-loss plan "
        "the intensity is subtracted; for a weight-gain plan an effective surplus is added; and in both "
        "cases the result is rounded to a value ending in fifty or a hundred so that it reads as a "
        "prescription rather than as a measurement. Writing T for the expenditure and p for the "
        "intensity in per cent, the two rules are T minus pT over one hundred for a deficit and T plus "
        "(p minus ten) T over one hundred for a surplus."
    )
    doc.p(
        "The ten-point subtraction in the surplus rule is not a defect but a deliberate moderation. A "
        "gross surplus of twenty-five per cent would add a quarter of the expenditure on top of an "
        "already generous maintenance figure; subtracting ten points makes the effective surplus fifteen "
        "per cent, which is the upper bound that the sports-nutrition literature generally recommends "
        "for a lean gain. The rule is stated in the comment above the method and reproduced in the "
        "listing below, together with the rounding helper it depends on."
    )
    doc.code("Listing 10.3 \u2014 percentage, rounding, deficit and surplus",
             "public static long percentageOf(double value, int percent) {\n"
             "  return Math.round((value * percent) / 100);\n"
             "}\n"
             "\n"
             "public static long roundCalories(long kcal) {\n"
             "  long round = (kcal / 100) * 100;\n"
             "  long difference = kcal - round;\n"
             "  return round + (difference > 50 ? 100 : (difference > 0 ? 50 : 0));\n"
             "}\n"
             "\n"
             "public static long findDeficit(double tdee, int percent) {\n"
             "  return roundCalories(Math.round(tdee - percentageOf(tdee, percent)));\n"
             "}\n"
             "\n"
             "public static long findSurplus(double tdee, int percent) {\n"
             "  return roundCalories(Math.round(tdee) + percentageOf(tdee, percent - 10));\n"
             "}")
    doc.table(
        "Target calories for the worked example at each intensity",
        ["Goal", "Intensity", "Weight-loss target", "Weight-gain target"],
        [
            ["Mild", "15 %", "2645 \u2212 397 = 2248, rounded to 2250",
             "2645 + 132 = 2777, rounded to 2800"],
            ["Moderate", "20 %", "2645 \u2212 529 = 2116, rounded to 2150",
             "2645 + 265 = 2910, rounded to 2900"],
            ["Aggressive", "25 %", "2645 \u2212 661 = 1984, rounded to 2000",
             "2645 + 397 = 3042, rounded to 3050"],
        ],
        widths=[14, 12, 37, 37], font_size=8.2)
    doc.p(
        "The moderate weight-loss row reproduces the value shown in the second wizard step, which "
        "displays 2150 kilocalories per day after the rounding step. The plan document, however, stores "
        "2152, because activation replaces the deficit-derived target with the energy equivalent of the "
        "chosen macro grams, as discussed in Section 7.3. The two figures differ by two kilocalories "
        "here because the balanced preset is close to the deficit split; a custom split would diverge "
        "much further, and that divergence is the intended behaviour."
    )

    doc.h2("10.5", "Macronutrient Presets and Bands", key="s10.5")
    doc.p(
        "The energy target is translated into grams with the four presets recorded in Table 10.3. Each "
        "preset allocates a percentage of the target to each macronutrient and divides by the energy "
        "density of that macronutrient, four kilocalories per gram for protein and carbohydrate and nine "
        "for fat. The same three densities are used in the reverse direction when logged intake is "
        "converted back into energy, which guarantees that a preset and its energy equivalent agree."
    )
    doc.table(
        "Macronutrient presets and their gram values for a 2150 kilocalorie target",
        ["Preset", "Protein %", "Carbs %", "Fat %", "Protein g", "Carbs g", "Fat g"],
        [
            ["Balanced", "30", "40", "30", "161", "215", "72"],
            ["High protein", "40", "35", "25", "215", "188", "60"],
            ["Low carbohydrate", "35", "25", "40", "188", "134", "96"],
            ["Low fat", "30", "50", "20", "161", "269", "48"],
        ],
        widths=[20, 13, 13, 10, 15, 15, 14], font_size=8.2)
    doc.p(
        "The presets are accompanied by three minimum and maximum bands, one per macronutrient, which "
        "the interface uses to initialise the custom sliders. The protein band runs from fifteen to "
        "fifty per cent of the target, the carbohydrate band from twenty to sixty-five and the fat band "
        "from twenty to forty. The bands are advisory: the service accepts any gram value the client "
        "submits, so a user who drags a slider beyond a band is not prevented from doing so, which is "
        "consistent with the principle that the macro split is the user's decision."
    )
    doc.code("Listing 10.4 \u2014 preset construction",
             "public static double findProtein(double deficit, int percent) {\n"
             "  return Double.valueOf(Math.round(percentageOf(deficit, percent) / 4.0));\n"
             "}\n"
             "\n"
             "public static Macros findBalancedMacros(double deficit) {\n"
             "  return new Macros(\n"
             "    findProtein(deficit, 30), findCarbs(deficit, 40), findFat(deficit, 30)\n"
             "  );\n"
             "}\n"
             "\n"
             "public static MacrosQuantity findProteinQuantity(double deficit) {\n"
             "  return new MacrosQuantity(\n"
             "    findProtein(deficit, 15), findProtein(deficit, 50)\n"
             "  );\n"
             "}")

    doc.h2("10.6", "Meal Split and Daily Aggregation", key="s10.6")
    doc.p(
        "The daily allowance is split across four meals with the fixed percentages thirty, thirty, "
        "fifteen and twenty-five for breakfast, lunch, snack and dinner. The split is applied to the "
        "three macro totals independently, and the resulting twelve numbers are stored in the tracking "
        "document as four macro tracks. Because the percentages sum to one hundred, the sum of the four "
        "meal budgets equals the daily budget for each macronutrient, which is the property that makes "
        "the aggregation on the next update exact."
    )
    doc.code("Listing 10.5 \u2014 the meal split and the aggregation performed on update",
             "private MealKcal splitForMealKcal(DietPlanTrack track) {\n"
             "  MacrosTrack macros = new MacrosTrack(\n"
             "    track.getProtein(), track.getFat(), track.getCarbs()\n"
             "  );\n"
             "  return new MealKcal(\n"
             "    NutrientsCalculator.macrosPercentage(macros, 30),   // breakfast\n"
             "    NutrientsCalculator.macrosPercentage(macros, 30),   // lunch\n"
             "    NutrientsCalculator.macrosPercentage(macros, 15),   // snack\n"
             "    NutrientsCalculator.macrosPercentage(macros, 25)    // dinner\n"
             "  );\n"
             "}\n"
             "\n"
             "public DietPlanTrack updateMacros(\n"
             "  String dietPlanId, String category, MacrosTrack macros\n"
             ") {\n"
             "  DietPlanTrack track = findDietPlanTrackByDietPlanId(dietPlanId);\n"
             "  MacrosTrack target = getMacrosByCategory(track.getMealKcal(), category);\n"
             "  target.getProtein().setTaken(macros.getProtein().getTaken());\n"
             "  target.getFat().setTaken(macros.getFat().getTaken());\n"
             "  target.getCarbs().setTaken(macros.getCarbs().getTaken());\n"
             "  adjustMacros(track);\n"
             "  track.getIntake().setTaken(calcDeficitTaken(track));\n"
             "  return dietPlanTrackRepository.save(track);\n"
             "}")
    doc.p(
        "Two properties of that method are worth emphasising. The category is resolved through a switch "
        "over the four names defined by the constants class, and an unknown name raises a bad-request "
        "failure rather than silently doing nothing. And the daily intake is recomputed from the macro "
        "totals rather than accumulated incrementally, which makes the operation idempotent: submitting "
        "the same values twice produces the same document rather than doubling the logged intake."
    )

    doc.h2("10.7", "Energy Conversion of Logged Intake", key="s10.7")
    doc.p(
        "The conversion from grams to kilocalories uses the Atwater factors four, nine and four. The two "
        "methods that perform it are instructive because they apply the same convention in two "
        "directions: one converts the logged values of a meal track, the other converts the allowance of "
        "a meal track."
    )
    doc.code("Listing 10.6 \u2014 energy conversion of taken and total values",
             "public static double calcDeficitTaken(MacrosTrack macros) {\n"
             "  return (\n"
             "    macros.getProtein().getTaken() * 4\n"
             "      + macros.getFat().getTaken() * 9\n"
             "      + macros.getCarbs().getTaken() * 4\n"
             "  );\n"
             "}\n"
             "\n"
             "public static long calcTotalDeficit(MacrosTrack macros) {\n"
             "  return Math.round(\n"
             "    macros.getProtein().getTotal() * 4\n"
             "      + macros.getFat().getTotal() * 9\n"
             "      + macros.getCarbs().getTotal() * 4\n"
             "  );\n"
             "}")
    doc.p(
        "The second method is what makes the suggestion feature coherent. When the user asks for dinner "
        "suggestions, the tracking service selects the dinner macro track, passes it to the second "
        "method and thereby obtains the energy that the dinner budget allows. The prompt therefore "
        "carries a number derived from the plan by the same arithmetic that the tracking page uses, "
        "rather than by a separate estimate."
    )

    doc.h2("10.8", "Progress Percentage and Weekly Metrics", key="s10.8")
    doc.p(
        "The dashboard percentage is the rounded ratio of the logged intake to the plan target, clamped "
        "only in the interface. The weekly metrics are assembled by selecting the tracking documents "
        "whose date falls between the start of the previous week and the end of today in the Asia/Kolkata "
        "zone, projecting each into a weekday abbreviation and a weight, and returning the two arrays "
        "beside the scalar metrics."
    )
    doc.code("Listing 10.7 \u2014 assembling the dashboard metrics",
             "public MetricsDTO getMetricsByDateRange() {\n"
             "  List<String> days = new ArrayList<>();\n"
             "  List<Double> weights = new ArrayList<>();\n"
             "  Date[] range = getOneWeekDateRange();\n"
             "  DietPlan plan = findDietPlanByUserId();\n"
             "  DietPlanTrack track = findDietPlanTrackByDietPlanId(plan.getId());\n"
             "  dietPlanTrackRepository\n"
             "    .findByDateRangeAndDietPlanId(range[0], range[1], plan.getId())\n"
             "    .forEach(t -> {\n"
             "      days.add(getDayName(t.getCreatedAt()));\n"
             "      weights.add(t.getWeight());\n"
             "    });\n"
             "  return buildMetrics(track, plan.getTitle(), plan.getDuration(), days, weights);\n"
             "}")
    doc.p(
        "The zone is fixed rather than taken from the server default, which is the correct choice for an "
        "application whose users are in one country; it does mean that the weekly window is defined in "
        "Indian Standard Time regardless of where the service runs. The range begins one week before "
        "today and is inclusive of today, so the chart shows at most eight points even though the "
        "interface describes it as a weekly trend."
    )

    doc.h2("10.9", "Draft Construction and Resumption", key="s10.9")
    doc.p(
        "The wizard is a stateful conversation implemented over a stateless protocol, and the algorithm "
        "that makes it work deserves to be stated as such. Each of the three creation methods follows the "
        "same four steps: resolve the user from the security context, locate the pending plan, creating "
        "it if the method is the first step and it does not yet exist, copy the submitted values onto the "
        "plan, and advance the form status. The pending plan is identified by the pair of user identifier "
        "and pending status, which is why a user can hold at most one draft at a time."
    )
    doc.code("Listing 10.8 \u2014 the common shape of a wizard step",
             "public CaloriesEstimationResponse createDietPlanGoalSelection(\n"
             "  GoalSelectionRequest request\n"
             ") {\n"
             "  DietPlan plan = getPendingDietPlan();   // bad request when absent\n"
             "  plan.setGoal(request.getGoal());\n"
             "  plan.setDuration(request.getDuration());\n"
             "  plan.setFormStatus(FormStatus.MEAL_PREFERENCE);\n"
             "  if (Plan.WEIGHT_LOSS.equals(plan.getPlan())) {\n"
             "    plan.setTargetCalories(\n"
             "      NutrientsCalculator.findDeficit(plan.getTdee(), plan.getGoal().getValue())\n"
             "    );\n"
             "  } else {\n"
             "    plan.setTargetCalories(\n"
             "      NutrientsCalculator.findSurplus(plan.getTdee(), plan.getGoal().getValue())\n"
             "    );\n"
             "  }\n"
             "  return toCaloriesEstimationResponse(dietPlanRepository.save(plan));\n"
             "}")
    doc.p(
        "The interesting property of this shape is that it is idempotent with respect to the draft: "
        "submitting the second step twice produces the same document, because the method copies values "
        "rather than appending them. The property it does not have is transactional isolation; if two "
        "tabs submit the same step concurrently, the last write wins and the earlier submission is lost "
        "silently. That is acceptable for a single-user wizard and is recorded here because it is the one "
        "concurrency hazard in the construction path."
    )
    doc.p(
        "Resumption depends on the read counterpart. The status method loads any existing pending plan "
        "and returns an envelope whose form status tells the client which step to render, together with "
        "the payload for that step. A user who closes the browser after the second step is therefore "
        "returned to the third step on the next visit, and a user who presses back is served the payload "
        "of the earlier step by the POST variant of the status endpoint, which reconstructs it from the "
        "stored document rather than from a client-side cache."
    )

    doc.h2("10.10", "AI Suggestion Pipeline", key="s10.10")
    doc.p(
        "The suggestion pipeline has five stages, each of which is a single method. The first resolves "
        "the calorie allowance for the requested meal. The second formats the prompt from the four "
        "filters and the allowance. The third builds the chat model with a system message that fixes the "
        "output schema. The fourth posts the model to the provider and extracts the content of the first "
        "choice. The fifth parses that content into typed objects. Listing 10.9 reproduces the second "
        "stage."
    )
    doc.code("Listing 10.9 \u2014 prompt construction",
             "private String buildPrompt(FilterDTO filter, long calories) {\n"
             "  return String.format(\n"
             "    \"Suggest me 5 healthy %s cuisine %s %s foods for %s under %d calories.\",\n"
             "    filter.getCuisineFilter(), filter.getMealTypeFilter(),\n"
             "    filter.getDietTypeFilter(), filter.getMealFilter(), calories\n"
             "  );\n"
             "}")
    doc.p(
        "Three implementation details are consequences of the specific provider rather than of the "
        "algorithm. The system message ends with a token that suppresses a reasoning preamble on models "
        "that otherwise emit one. The maximum token count is set to minus one, which the provider "
        "interprets as an instruction not to impose an explicit limit rather than as an error. And the "
        "response is read by traversal of a JSON tree rather than through a typed DTO, so a change in "
        "the provider's envelope does not break compilation; the consequence is that a missing content "
        "field yields an empty string and a parsing failure at the fifth stage rather than a clear "
        "diagnostic."
    )
    doc.h2("10.11", "Pseudocode Summary", key="s10.11")
    doc.p(
        "The following pseudocode states the complete plan-and-track cycle in the notation used for "
        "algorithmic description, so that the arithmetic can be reviewed independently of the Java "
        "syntax and of the framework that hosts it."
    )
    doc.code("Pseudocode 10.1 \u2014 plan construction, activation and daily logging",
             "PROCEDURE EstimateEnergy(age, weight, height, gender, activity):\n"
             "  bmr  <- 10*weight + 6.25*height - 5*age + (5 IF gender = MALE ELSE -161)\n"
             "  tdee <- bmr * activity.multiplier\n"
             "  RETURN round(tdee)\n"
             "\n"
             "PROCEDURE DeriveTarget(tdee, plan, intensity):\n"
             "  IF plan = WEIGHT_LOSS THEN raw <- tdee - tdee*intensity/100\n"
             "  ELSE                        raw <- tdee + tdee*(intensity-10)/100\n"
             "  base <- floor(raw/100)*100\n"
             "  diff <- raw - base\n"
             "  RETURN base + (100 IF diff > 50 ELSE (50 IF diff > 0 ELSE 0))\n"
             "\n"
             "PROCEDURE BuildMacros(targetKcal, preset):\n"
             "  FOR EACH macro IN {protein, carbs, fat}:\n"
             "    kcal  <- targetKcal * preset.percent[macro] / 100\n"
             "    grams <- round(kcal / density[macro])      // 4, 4 and 9\n"
             "  RETURN grams\n"
             "\n"
             "PROCEDURE Activate(plan):\n"
             "  plan.targetCalories <- energy(plan.macros)\n"
             "  plan.todayWeight    <- plan.weight\n"
             "  plan.createdAt      <- today\n"
             "  plan.planStatus     <- ACTIVE\n"
             "  plan.formStatus     <- COMPLETED\n"
             "  SAVE plan\n"
             "  CREATE track(weight = plan.todayWeight, dayCount = 1,\n"
             "               intake = plan.targetCalories,\n"
             "               mealKcal = Split(plan.macros, [30, 30, 15, 25]))\n"
             "\n"
             "PROCEDURE LogMeal(planId, category, grams):\n"
             "  track <- FindOrCreateTodayTrack(planId)\n"
             "  meal  <- track.mealKcal[category]\n"
             "  meal.taken <- grams\n"
             "  FOR EACH macro IN {protein, carbs, fat}:\n"
             "    track[macro].taken <- SUM(track.mealKcal[m][macro].taken\n"
             "                               FOR m IN {breakfast, lunch, snack, dinner})\n"
             "  track.intake.taken <- 4*protein.taken + 4*carbs.taken + 9*fat.taken\n"
             "  SAVE track\n"
             "  RETURN track")

    doc.h2("10.12", "Code Organisation and Naming Conventions", key="s10.12")
    doc.p(
        "The service follows a package-by-feature organisation rather than a package-by-layer "
        "organisation. Each of the four features, namely the identity feature, the diet-plan feature, "
        "the food-suggestion feature and the chat service, contains its own controller, service, "
        "repository, entity and DTO packages, so a change to the plan feature never requires opening a "
        "file in another feature's directory. The cross-cutting code lives in six sibling packages: "
        "configuration, exception, security, shared, utility and the shared model that holds the value "
        "objects used by more than one feature."
    )
    doc.p(
        "Naming is consistent and slightly verbose, which was preferred over abbreviation. Entities are "
        "singular nouns. Request and response types end in Request or Response, and the types that exist "
        "to shape a response end in DTO. Services end in Service, and they are concrete classes rather "
        "than interface-and-implementation pairs, with one exception: the language-model adapter is "
        "declared behind an interface, because it is the one collaborator whose implementation might "
        "legitimately vary between a live provider and a stub."
    )
    doc.p(
        "The client mirrors the naming of the service. Services end in Service and are file-named with "
        "the suffix, with one exception in the plan feature whose file predates the convention and uses "
        "a hyphenated form; that exception is recorded in the verification matrix. Components follow the "
        "CLI convention of a name, a component suffix and a sibling template and stylesheet, and the "
        "single custom pipe and the model interfaces follow the same pattern."
    )

    # ================================================================= CHAPTER 11
    doc.chapter_heading(11, "Testing and Verification", key="ch11")
    doc.h2("11.1", "Testing Strategy", key="s11.1")
    doc.p(
        "The testing strategy has two parts, and they were pursued to different depths. The first part "
        "is automated testing inside the repository. The service contains one test class with a single "
        "method that asserts the application context loads; this is the smoke test that the project "
        "initialiser generates, and it is the only automated test the delivered repository contains. The "
        "client contains no test files at all, although the Karma and Jasmine dependencies are declared "
        "and the CLI is therefore configured to run them."
    )
    doc.p(
        "The second part is the verification exercise that produced this report. Because the automated "
        "suite is inadequate to substantiate the claims made in Chapters 5 to 10, every such claim was "
        "checked against the source by reading it, and the results were recorded in the matrix of "
        "Appendix B. The matrix uses three states: verified, meaning that the behaviour was traced "
        "through the code and, where possible, observed in the running application; inferred, meaning "
        "that the behaviour follows from the code but was not exercised; and not implemented, meaning "
        "that the repository does not contain the artefact. This chapter reports the outcome of that "
        "exercise and is deliberately candid about the limits of the evidence."
    )

    doc.h2("11.2", "Test Levels and Proposed Test Cases", key="s11.2")
    doc.p(
        "The architecture supports a conventional test pyramid, and Table 11.1 specifies the cases that "
        "the next revision should implement. The table is presented as a specification rather than as a "
        "report of executed tests, because only the context-load test currently exists. The expected "
        "values are those the implementation produces, derived by hand from the equations of Chapter 10, "
        "so the table can serve directly as a set of assertions."
    )
    doc.table(
        "Test case specification for the Macrova application",
        ["ID", "Level", "Unit under test", "Input or condition", "Expected result"],
        [
            ["TC-01", "Unit", "Basal rate method", "Male, 25 years, 175 cm, 95 kg", "1923.75"],
            ["TC-02", "Unit", "Basal rate method", "Female, 30 years, 160 cm, 60 kg", "1289.0"],
            ["TC-03", "Unit", "Expenditure method", "Basal 1923.75, light activity", "2645.16"],
            ["TC-04", "Unit", "Calorie rounding", "2116", "2150"],
            ["TC-05", "Unit", "Calorie rounding", "2000, 2050 and 2051", "2000, 2050 and 2100"],
            ["TC-06", "Unit", "Deficit method", "Expenditure 2645, 20 per cent", "2150"],
            ["TC-07", "Unit", "Surplus method", "Expenditure 2645, 25 per cent", "3050"],
            ["TC-08", "Unit", "Balanced preset", "2150 kilocalories", "161, 215 and 72 grams"],
            ["TC-09", "Unit", "Meal split", "Totals 161, 72 and 215 at 30 per cent", "48, 22 and 65"],
            ["TC-10", "Unit", "Taken-energy conversion", "Taken 110, 65 and 170", "1705.0"],
            ["TC-11", "Unit", "Category validation", "breakfast and brunch", "true and false"],
            ["TC-12", "Service", "Registration", "Duplicate username", "Bad-request failure"],
            ["TC-13", "Service", "Registration", "Valid payload", "DTO without a password field"],
            ["TC-14", "Service", "Authentication manager", "Wrong password",
             "Bad-credentials failure"],
            ["TC-15", "Service", "Authentication manager", "Unknown username",
             "Bad-credentials failure"],
            ["TC-16", "Service", "First wizard step", "No pending plan", "Plan created"],
            ["TC-17", "Service", "Pending plan lookup", "No pending plan", "Bad-request failure"],
            ["TC-18", "Service", "Second wizard step", "Loss plan, moderate", "Target 2150"],
            ["TC-19", "Service", "Meal update", "Category brunch", "Bad-request failure"],
            ["TC-20", "Service", "Plan by identifier", "Identifier of another user",
             "Not-found failure"],
            ["TC-21", "Service", "Duration check", "Day count 181, duration 180",
             "True, with the plan inactive"],
            ["TC-22", "Service", "Meal allowance", "No active plan", "500"],
            ["TC-23", "Web", "Registration", "Missing password", "400 with an error array"],
            ["TC-24", "Web", "Metrics", "No authorisation header", "401"],
            ["TC-25", "Web", "Metrics", "Expired access token", "401"],
            ["TC-26", "Web", "Plan by identifier", "Valid token, foreign identifier", "404"],
            ["TC-27", "Web", "Meal update", "Invalid category in the path", "400"],
            ["TC-28", "Web", "Token refresh", "No cookie", "401"],
            ["TC-29", "Integration", "Wizard end to end", "Four sequential posts",
             "Active plan with a first-day document"],
            ["TC-30", "Integration", "Tracking round trip", "Log all four meals",
             "Intake equals four protein plus four carbohydrate plus nine fat"],
            ["TC-31", "End to end", "Sign-in and dashboard", "Valid credentials in a browser",
             "Metrics rendered"],
            ["TC-32", "End to end", "Guard redirection", "Deep link without a token",
             "Redirect to the login screen"],
        ],
        widths=[7, 11, 30, 28, 24], font_size=7.9)

    doc.h2("11.3", "Executed Verification", key="s11.3")
    doc.p(
        "The verification exercise examined every class in the repository and every endpoint in the "
        "catalogue. The results are summarised in Table 11.2 and set out in full in Appendix B. Of the "
        "twenty functional requirements, nineteen are implemented and verified by reading the code, one "
        "is inferred because it depends on a third party, and none is missing. Of the ten "
        "non-functional requirements, eight are satisfied directly, one is satisfied only in the "
        "development profile and one is not satisfied."
    )
    doc.table(
        "Summary of the verification results",
        ["Area", "Artefacts examined", "Verified", "Partially verified", "Not implemented"],
        [
            ["Identity and session", "4 classes, 3 filters, 5 endpoints",
             "The four classes and five endpoints",
             "Sign-out clears the cookie but does not revoke the token", "Token revocation"],
            ["Plan construction", "1 controller, 1 service, 8 DTOs, 6 endpoints",
             "Six endpoints and both classes", "None", "Server-side range validation"],
            ["Daily tracking", "1 controller, 1 service, 2 entities, 13 endpoints", "Thirteen endpoints",
             "The metrics window is fixed to eight days", "None"],
            ["AI suggestions", "1 controller, 1 service, 2 provider classes",
             "The endpoint and the adapter", "The prompt and the parse were verified by reading",
             "Persistence of suggestions"],
            ["History and review", "3 components, 3 endpoints", "All three of each", "None", "None"],
            ["Security", "1 configuration, 3 filters, 1 manager, 1 token service",
             "The authentication and authorisation paths",
             "The cross-origin policy is pinned to the development origin",
             "Throttling, transport security and the secure cookie flag"],
            ["Client navigation", "13 routes, 1 guard, 2 interceptors", "Eleven guarded routes",
             "Two history routes are unguarded", "Unit tests"],
            ["Automated tests", "1 test class", "One context-load test", "None",
             "All service, web and end-to-end tests"],
        ],
        widths=[15, 26, 21, 22, 16], font_size=7.9)
    doc.p(
        "The exercise produced ten findings that a reviewer should know about. They are listed in order "
        "of severity, with the artefact concerned and the recommended correction for each."
    )
    doc.numbered([
        "Two history routes are declared without the authentication guard, so a visitor who knows or "
        "guesses a plan identifier can load the component. The subsequent request still fails with 401, "
        "because the interceptor cannot attach a token, so no data is exposed; the correction is "
        "nevertheless to add the guard to both entries.",
        "Ownership is enforced by query construction rather than by a central authorisation check. That "
        "is effective for every endpoint that queries by identifier and user, but a future endpoint that "
        "queried by identifier alone would silently bypass the rule. A method-level check would make the "
        "rule structural.",
        "Refresh tokens are neither rotated nor revocable. Sign-out clears the cookie, but a copy of the "
        "token taken before sign-out remains valid until its expiry. Rotation on every refresh, "
        "together with a server-side token family, would close the window.",
        "The refresh cookie is issued without the secure attribute while the development server runs "
        "over plain HTTP. That is appropriate for a local demonstration and unsuitable for any other "
        "deployment; the correction is a profile-specific property rather than a change to the code.",
        "There is no throttling or lockout on failed authentication. The manager returns a "
        "bad-credentials failure without counting attempts, so an online dictionary attack against the "
        "login endpoint is not impeded by the application.",
        "The controller advice maps a JSON parsing failure to 410, which is not the conventional choice "
        "for an upstream provider failure. A 502 or 500 would be more accurate and would not confuse a "
        "client that treats 410 as a permanent condition.",
        "The interface exposes three endpoints that no client calls, and the client declares one method "
        "that the service does not map. These are dead or inconsistent surfaces that should either be "
        "removed or given a caller before the next release.",
        "The suggestions collection and the method that would write to it are unused, so the suggestion "
        "feature is stateless with respect to the database. That is a deliberate outcome of the decision "
        "not to persist generated output, but a repository for data that is never written is a "
        "maintenance hazard.",
        "The mild intensity is labelled as a ten per cent deficit in the goal-selection template while "
        "the enumeration that the service uses carries fifteen per cent. The label is hard-coded "
        "presentation text and the arithmetic is correct, so a user who selects the mild option receives "
        "a larger deficit than the screen promises; the correction is to render the label from the "
        "enumeration value.",
        "The automated suite is a single context-load test. Every statement in Chapters 5 to 10 about "
        "arithmetic, persistence and security is therefore substantiated by reading the code rather than "
        "by executed assertions, which is why Table 11.1 specifies the cases that the next revision must "
        "implement.",
    ])

    doc.h2("11.4", "Analysis of the AI Feature", key="s11.4")
    doc.p(
        "The suggestion feature deserves a separate analysis because it is the only part of the system "
        "whose correctness cannot be established by reading the code. Three risks were identified. "
        "First, the nutritional values are unverified: the model produces plausible numbers that may "
        "differ from any published composition table and may differ between calls for the same dish. "
        "Second, the schema instruction in the system prompt is a request rather than a constraint, so a "
        "compliant response is not guaranteed; the parser will fail on a prose reply and the user will "
        "see an error rather than a suggestion. Third, the prompt incorporates the meal allowance but "
        "incorporates no allergy, medical condition or dietary restriction beyond the four filters, so a "
        "suggestion could be unsuitable for a user with an intolerance."
    )
    doc.p(
        "The mitigations that are implemented are correspondingly modest, and they are stated here so "
        "that the report does not overstate the feature. The feature is optional and can be left unused, "
        "although the service must still be configured with a key in order to start. Suggestions are "
        "never written into a plan, so a model error cannot corrupt the deterministic part of the "
        "system. The output is labelled as a suggestion in the interface copy, and this chapter records "
        "the caveat beside the screenshot. The mitigations that would be required before the feature "
        "could be recommended to a real user are listed in Chapter 12."
    )

    doc.h2("11.5", "Performance Observations", key="s11.5")
    doc.p(
        "No formal performance testing was conducted, and the following observations are qualitative. On "
        "the development machine a dashboard load issues two requests and completes in well under a "
        "second; the tracking page issues two and completes in a comparable time. The heaviest operation "
        "is the weekly metrics query, which reads at most eight documents but does so by scanning the "
        "collection in the absence of an index; with an index on the plan identifier and date the query "
        "would become a bounded range scan. The suggestion call dominates the latency of that screen, "
        "because it waits for a remote inference; the interface shows a loading state during the wait, "
        "which is the correct behaviour for an operation whose duration the application does not "
        "control."
    )
    doc.p(
        "The client bundle is not code-split. The production build reports a single initial bundle "
        "within the default budget of one megabyte, and the chart library is imported wholesale by the "
        "weight chart component rather than limited to the modules that the chart uses. At the current "
        "size the choice is defensible; splitting the wizard and the chart would reduce the time to "
        "first paint on the login screen, which is the page a new visitor sees first."
    )

    doc.h2("11.6", "Limitations Recorded", key="s11.6")
    doc.bullets([
        "The automated test suite is a single smoke test; no unit, web-slice or end-to-end test is "
        "present.",
        "Input ranges are validated in the browser only; the service accepts any numeric value that "
        "binds successfully to the request type.",
        "Uniqueness of the username and the address is enforced by application checks rather than by a "
        "unique index, so concurrent registrations could create duplicates.",
        "There is no password reset, no address verification and no account deletion.",
        "Refresh tokens are neither rotated nor revocable, and there is no throttling of failed "
        "sign-in attempts.",
        "The cross-origin allow-list, the insecure cookie flag and the absence of transport security "
        "confine the deployment to a local development setting.",
        "The suggestion feature returns unverified nutrition data, considers neither allergies nor "
        "medical conditions, and no index is declared on any collection.",
        "Two history routes lack the authentication guard.",
        "The mild intensity is mislabelled in the goal-selection template.",
    ])

    # ================================================================= CHAPTER 12
    doc.chapter_heading(12, "Conclusion and Future Enhancements", key="ch12")
    doc.h2("12.1", "Summary of the Work", key="s12.1")
    doc.p(
        "This project designed, implemented and documented Macrova, a web application that turns a "
        "published energy-balance equation into a working planning and tracking tool. The delivered "
        "system comprises 71 Java source files totalling 2,779 lines, 60 TypeScript files totalling "
        "1,915 lines, 20 component templates totalling 1,238 lines and 19 stylesheets totalling 2,381 "
        "lines, organised into eight functional modules over a three-tier architecture. It exposes 26 "
        "REST endpoints, persists four collections of which three are written in normal operation, and "
        "renders fifteen distinct screens."
    )
    doc.p(
        "Functionally, the system allows a user to register, authenticate through a stateless token "
        "exchange, construct a plan through a resumable four-step wizard, receive a calorie and "
        "macronutrient budget derived from the Mifflin\u2013St Jeor equation, log intake per meal and "
        "weight per day, observe progress on a dashboard with a weight trend chart, review the daily "
        "records of any past plan, and request meal suggestions constrained by the allowance of a "
        "specific meal. The arithmetic behind every figure is isolated in a single documented utility "
        "class, and the report reproduces both the equations and the code that implements them."
    )

    doc.h2("12.2", "Conclusion", key="s12.2")
    doc.p(
        "The project demonstrates a point that motivated it in the first place: the difficult part of a "
        "diet application is not the formula but the consistency with which the formula is applied. The "
        "metabolic equation occupies one line of Java, and the value of the system lies in the discipline "
        "that surrounds it. There is a single utility class rather than repeated expressions. A stored "
        "plan records the assumptions that produced its target. A tracking document recomputes rather "
        "than accumulates, so a repeated submission cannot inflate the day. And a wizard whose state "
        "lives on the server resumes where it stopped. Each of those decisions is small, and together "
        "they produce an application whose numbers can be audited by hand, which is the property the "
        "design set out to achieve."
    )
    doc.p(
        "The project also demonstrates the value of an honest verification exercise. The repository "
        "delivered here does not have the test suite that its architecture would support, its deployment "
        "profile is a development profile, and its suggestion feature returns data that is not verified. "
        "Those facts are recorded in Chapter 11 rather than omitted, because a report that claimed "
        "otherwise would fail the first review that attempted to reproduce its claims. The distinction "
        "maintained throughout the document between behaviour that was verified, behaviour that was "
        "inferred from the code and behaviour that does not exist is, in the author's view, the most "
        "transferable result of the project."
    )

    doc.h2("12.3", "Learning Outcomes", key="s12.3")
    doc.p(
        "The work produced five outcomes that were not anticipated at the outset. The first is a "
        "practical understanding of the difference between stateless and stateful authentication, in "
        "particular the consequence that a stateless token cannot be revoked without a server-side list, "
        "which is why the sign-out in this application is a cookie deletion. The second is an "
        "appreciation of document-database modelling: the decision to embed four meal tracks inside a "
        "daily document was taken because the tracking page reads them together, and that decision "
        "eliminated the joins a relational design would have required. The third is the difficulty of "
        "verifying a generative feature, which has no oracle and whose output differs on every call. The "
        "fourth is the value of typed component contracts, because the typed inputs and outputs of the "
        "wizard turned four potential runtime errors into compile errors. The fifth is that documentation "
        "is a design activity: writing the data dictionary exposed the duplicated target computation "
        "described in Section 7.3, which had not been noticed while the code was being written."
    )

    doc.h2("12.4", "Future Enhancements", key="s12.4")
    doc.p(
        "The following enhancements are proposed in the order in which they would deliver value. None is "
        "implemented in the delivered system, and each is stated with the artefact it would change."
    )
    doc.numbered([
        "Automated test suite. Implement the thirty-two cases of Table 11.1 as unit tests for the "
        "calculator and the services, web-slice tests for the controllers and component tests for the "
        "pipe and the guard. This is first because every later change depends on it.",
        "Indexes. Add the unique indexes on the username and the address and the compound indexes of "
        "Table 7.8, so that the current collection scans become bounded range scans.",
        "Refreshed-token hardening. Rotate the refresh token on every use, store a token family and a "
        "revocation timestamp, add a failed-sign-in counter with a temporary lockout, and set the cookie "
        "attributes from configuration rather than from literals.",
        "Server-side validation. Move the range checks from the Angular submit handlers into validation "
        "annotations on the request types, so that the rules hold for any client.",
        "A verified food catalogue. Replace free-text macro entry with a curated food table, so that a "
        "meal is recorded as one or more food items with portions; the current entry would remain as a "
        "fallback for composite dishes.",
        "Password reset and address verification. Add a single-use token collection, a mail sender and "
        "the two flows, which are the minimum required before the application can be used by anyone "
        "other than its author.",
        "Deletion and export. Provide a cascade deletion of a user and their plans, and an export of a "
        "plan's daily records, so that the user's data is portable.",
        "Code splitting. Lazy-load the wizard and the chart and reduce the chart import surface, in order "
        "to shorten the time to first paint on the login screen.",
        "Restriction-aware suggestions. Add an allergy and restriction profile to the prompt, "
        "cross-check every returned dish name against a small curated list of unsafe items, and label the "
        "results as unverified in the interface.",
        "A second client. Expose the same interface to a mobile shell, since the service is already "
        "stateless and therefore ready for one.",
    ])

    # ============================================================== REFERENCES
    doc.part_heading("References", key="references")
    doc.h2("1.", "Books", key="refs-books")
    doc.bullets([
        "C. S. Walls, Spring in Action, 6th ed. Shelter Island, NY, USA: Manning Publications, 2022.",
        "J. Bloch, Effective Java, 3rd ed. Boston, MA, USA: Addison-Wesley Professional, 2018.",
        "M. Kleppmann, Designing Data-Intensive Applications. Sebastopol, CA, USA: O'Reilly Media, 2017.",
        "M. Fowler, Patterns of Enterprise Application Architecture. Boston, MA, USA: Addison-Wesley, "
        "2002.",
        "P. J. Sadalage and M. Fowler, NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot "
        "Persistence. Boston, MA, USA: Addison-Wesley, 2012.",
        "R. S. Pressman and B. R. Maxim, Software Engineering: A Practitioner's Approach, 9th ed. New "
        "York, NY, USA: McGraw-Hill Education, 2020.",
        "I. Sommerville, Software Engineering, 10th ed. Harlow, UK: Pearson Education, 2016.",
        "A. Freeman, Pro Angular. Berkeley, CA, USA: Apress, 2024.",
        "E. Evans, Domain-Driven Design: Tackling Complexity in the Heart of Software. Boston, MA, USA: "
        "Addison-Wesley, 2004.",
        "N. Ferguson, B. Schneier and T. Kohno, Cryptography Engineering: Design Principles and Practical "
        "Applications. Indianapolis, IN, USA: Wiley, 2010.",
        "J. Nielsen, Usability Engineering. San Francisco, CA, USA: Morgan Kaufmann, 1994.",
    ])
    doc.h2("2.", "Research Papers, Standards and Reports", key="refs-papers")
    doc.bullets([
        "M. D. Mifflin, S. T. St Jeor, L. A. Hill, B. J. Scott, S. A. Daugherty and Y. O. Koh, \u201cA new "
        "predictive equation for resting energy expenditure in healthy individuals,\u201d American "
        "Journal of Clinical Nutrition, vol. 51, no. 2, pp. 241\u2013247, Feb. 1990.",
        "J. W. Frankenfield, L. Roth-Yousey and C. Compher, \u201cComparison of predictive equations for "
        "resting metabolic rate in healthy nonobese and obese adults: a systematic review,\u201d Journal "
        "of the American Dietetic Association, vol. 105, no. 5, pp. 775\u2013789, May 2005.",
        "Food and Agriculture Organization, World Health Organization and United Nations University, "
        "Human Energy Requirements: Report of a Joint FAO/WHO/UNU Expert Consultation. Rome, Italy: FAO "
        "Food and Nutrition Technical Report Series 1, 2004.",
        "World Health Organization, Obesity: Preventing and Managing the Global Epidemic. Geneva, "
        "Switzerland: WHO Technical Report Series 894, 2000.",
        "L. E. Burke, J. Wang and M. A. Sevick, \u201cSelf-monitoring in weight loss: a systematic review "
        "of the literature,\u201d Journal of the American Dietetic Association, vol. 111, no. 1, "
        "pp. 92\u2013102, Jan. 2011.",
        "S. Michie, C. Abraham, C. Whittington, J. McAteer and S. Gupta, \u201cEffective techniques in "
        "healthy eating and physical activity interventions: a meta-regression,\u201d Health Psychology, "
        "vol. 28, no. 6, pp. 690\u2013701, Nov. 2009.",
        "R. S. Sandhu, E. J. Coyne, H. L. Feinstein and C. E. Youman, \u201cRole-based access control "
        "models,\u201d IEEE Computer, vol. 29, no. 2, pp. 38\u201347, Feb. 1996.",
        "N. Provos and D. Mazi\u00e8res, \u201cA future-adaptable password scheme,\u201d in Proc. USENIX "
        "Annual Technical Conference, Monterey, CA, USA, 1999, pp. 81\u201391.",
        "M. Jones, J. Bradley and N. Sakimura, \u201cJSON Web Token (JWT),\u201d IETF RFC 7519, May 2015.",
        "M. Jones, J. Bradley and N. Sakimura, \u201cJSON Web Signature (JWS),\u201d IETF RFC 7515, "
        "May 2015.",
        "R. Fielding, \u201cArchitectural Styles and the Design of Network-based Software "
        "Architectures,\u201d Ph.D. dissertation, University of California, Irvine, CA, USA, 2000.",
        "R. Bommasani et al., \u201cOn the opportunities and risks of foundation models,\u201d "
        "arXiv:2108.07258, Aug. 2021.",
        "OWASP Foundation, \u201cOWASP Top 10:2021 \u2014 The Ten Most Critical Web Application Security "
        "Risks,\u201d Open Worldwide Application Project, 2021.",
        "M. Fowler, \u201cThe practical test pyramid,\u201d martinfowler.com, Feb. 2018.",
    ])
    doc.h2("3.", "Official Documentation and Technical Sources", key="refs-docs")
    doc.bullets([
        "Broadcom and VMware Tanzu, \u201cSpring Boot Reference Documentation, version 3.4,\u201d "
        "https://docs.spring.io/spring-boot/ (accessed November 2026).",
        "Spring Security Team, \u201cSpring Security Reference \u2014 Servlet Applications,\u201d "
        "https://docs.spring.io/spring-security/reference/ (accessed November 2026).",
        "Spring Data Team, \u201cSpring Data MongoDB Reference Documentation,\u201d "
        "https://docs.spring.io/spring-data/mongodb/reference/ (accessed November 2026).",
        "Google Angular Team, \u201cAngular Documentation \u2014 Standalone Components, Signals and "
        "Functional Interceptors,\u201d https://angular.dev/ (accessed November 2026).",
        "Google Angular Team, \u201cAngular CLI Builders and Proxy Configuration,\u201d "
        "https://angular.dev/tools/cli/ (accessed November 2026).",
        "Auth0, \u201cjava-jwt Library Documentation, version 4.5.0,\u201d "
        "https://github.com/auth0/java-jwt (accessed November 2026).",
        "MongoDB Inc., \u201cMongoDB Manual \u2014 Data Modelling and Indexes,\u201d "
        "https://www.mongodb.com/docs/manual/ (accessed November 2026).",
        "Chart.js Contributors, \u201cChart.js Documentation, version 4.4,\u201d "
        "https://www.chartjs.org/docs/ (accessed November 2026).",
        "OpenRouter, \u201cAPI Reference \u2014 Chat Completions,\u201d https://openrouter.ai/docs "
        "(accessed November 2026).",
        "Oracle Corporation, \u201cJava Platform, Standard Edition 21 API Specification,\u201d "
        "https://docs.oracle.com/en/java/javase/21/docs/api/ (accessed November 2026).",
        "Project Lombok, \u201cLombok Reference Documentation,\u201d https://projectlombok.org/features/ "
        "(accessed November 2026).",
        "ModelMapper, \u201cModelMapper User Manual, version 3.2,\u201d https://modelmapper.org/ "
        "(accessed November 2026).",
        "JUnit Team, \u201cJUnit 5 User Guide,\u201d https://junit.org/junit5/docs/current/user-guide/ "
        "(accessed November 2026).",
        "MDN Web Docs, \u201cHTTP Cookies, Cross-Origin Resource Sharing and HTTP Caching,\u201d "
        "https://developer.mozilla.org/ (accessed November 2026).",
        "Git SCM, \u201cPro Git, 2nd ed.,\u201d https://git-scm.com/book/en/v2 (accessed November 2026).",
    ])

    # ============================================================== APPENDICES
    doc.part_heading("Appendices", key="appendices")

    doc.prefix_numbering("A")
    doc.h2("Appendix A", "Endpoint Reference Summary", key="appx-a")
    doc.p(
        "This appendix reproduces the interface in a form that a client developer can use without the "
        "narrative of Chapter 8. Table A.1 groups the twenty-six endpoints by resource and states the "
        "authentication requirement of each group."
    )
    doc.table(
        "Endpoint groups with authentication requirements",
        ["Group", "Base path", "Endpoints", "Authentication"],
        [
            ["Identity", "/user and /authenticate", "Five",
             "Registration and refresh are public; the others require a bearer token"],
            ["Plan construction", "/diet-plan/form", "Six", "Bearer token"],
            ["Plan retrieval", "/diet-plan", "Eight", "Bearer token"],
            ["Tracking", "/diet-plan/track and /diet-plan/{category}", "Four", "Bearer token"],
            ["Reporting", "/diet-plan/metrics, /status and /overview", "Three", "Bearer token"],
            ["Suggestions", "/ai-food-suggest", "One", "Bearer token"],
        ],
        widths=[18, 34, 14, 34], font_size=8.2)
    doc.p(
        "The request and response shapes are declared by the DTO classes of the service, which are "
        "summarised in Table 8.1 and illustrated by the listings of Chapter 8. A client that implements "
        "the five identity endpoints, the six construction endpoints and the tracking endpoints can "
        "reproduce the behaviour of the delivered client."
    )

    doc.prefix_numbering("B")
    doc.h2("Appendix B", "Verification Matrix", key="appx-b")
    doc.p(
        "Table B.2 applies the same treatment to the ten non-functional requirements. The matrix records, "
        "for every functional and non-functional requirement, the artefact that "
        "implements it and the result of the verification exercise. The state column uses the three "
        "values defined in Section 11.1."
    )
    doc.table(
        "Verification matrix for the functional requirements",
        ["ID", "Implementing artefact", "State", "Note"],
        [
            ["FR-01", "User controller, user service", "Verified",
             "Client validation precedes the call"],
            ["FR-02", "User service existence checks", "Verified",
             "Application level rather than an index"],
            ["FR-03", "Authentication filter, custom manager", "Verified",
             "Uniform failure message"],
            ["FR-04", "Token service, authentication filter", "Verified",
             "Cookie is HttpOnly and SameSite Lax"],
            ["FR-05", "Refresh and logout methods", "Verified", "Cookie holds the refresh token"],
            ["FR-06", "Body-metrics step", "Verified", "Expenditure rounded once"],
            ["FR-07", "Goal-selection step", "Verified", "Deficit or surplus by plan type"],
            ["FR-08", "Calculator presets, meal-preference step", "Verified",
             "Custom values accepted"],
            ["FR-09", "Meal-preference step", "Verified", "None"],
            ["FR-10", "Activation method", "Verified", "Creates the first daily document"],
            ["FR-11", "Status endpoint and envelope", "Verified",
             "Backward navigation uses the POST variant"],
            ["FR-12", "Tracking service split", "Verified", "Split stored with the document"],
            ["FR-13", "Meal update method", "Verified", "Totals recomputed from four categories"],
            ["FR-14", "Taken-energy conversion", "Verified", "Atwater factors"],
            ["FR-15", "Weight update method", "Verified", "Updates both documents"],
            ["FR-16", "Metrics assembly", "Verified", "Eight-day window"],
            ["FR-17", "Duration check", "Verified", "Evaluated on page load, not scheduled"],
            ["FR-18", "Projection queries in both repositories", "Verified",
             "Descending by date"],
            ["FR-19", "Day overview component", "Verified", "Inputs disabled"],
            ["FR-20", "Suggestion controller, service and adapter", "Inferred",
             "Values unverified; the parse depends on model compliance"],
        ],
        widths=[8, 40, 14, 38], font_size=8.0)
    doc.table(
        "Verification matrix for the non-functional requirements",
        ["ID", "Requirement", "State", "Evidence"],
        [
            ["NFR-01", "Passwords stored only as adaptive hashes", "Verified",
             "BCrypt encoder; the hash never leaves the service"],
            ["NFR-02", "Every operation scoped to the authenticated user", "Verified",
             "The session component is called in every plan and tracking query"],
            ["NFR-03", "Stateless sessions", "Verified",
             "Session policy is stateless; the bearer token is verified per request"],
            ["NFR-04", "A first-time user reaches a plan unaided", "Verified",
             "Four-step wizard with inline guidance"],
            ["NFR-05", "Every screen offers a recoverable action", "Verified",
             "Empty state, error page and persistent header"],
            ["NFR-06", "Dashboard load under a second", "Inferred",
             "Observed qualitatively in Section 11.5"],
            ["NFR-07", "Missing daily document created on demand", "Verified",
             "Find-or-create path in the tracking service"],
            ["NFR-08", "Energy arithmetic in exactly one class", "Verified", "The calculator class"],
            ["NFR-09", "Buildable from a clean checkout", "Verified",
             "Maven wrapper and Angular CLI are both committed or declared"],
            ["NFR-10", "Tier interface documented to the field level", "Verified",
             "Chapter 8 and Appendix A"],
        ],
        widths=[10, 34, 12, 44], font_size=8.0)

    doc.prefix_numbering("C")
    doc.h2("Appendix C", "Selected Source Listings", key="appx-c")
    doc.p(
        "The three listings in this appendix are reproduced from the repository and are included because "
        "they are the artefacts most likely to be consulted during an evaluation: the security "
        "configuration, which defines the whole request policy; the method that performs the daily "
        "aggregation; and the enumeration and constants that constrain the domain."
    )
    doc.code("Listing C.1 \u2014 the security filter chain (abridged)",
             "@Bean\n"
             "public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {\n"
             "  AuthenticationFilter authenticationFilter =\n"
             "    new AuthenticationFilter(customAuthenticationManager, jwtTokenService);\n"
             "  authenticationFilter.setFilterProcessesUrl(\"/authenticate\");\n"
             "  http\n"
             "    .csrf(csrf -> csrf.disable())\n"
             "    .cors(cors -> cors.configurationSource(corsConfigurationSource()))\n"
             "    .authorizeHttpRequests(auth -> auth\n"
             "      .requestMatchers(HttpMethod.POST,\n"
             "        SecurityConstants.REGISTER_PATH,\n"
             "        SecurityConstants.REFRESH_PATH).permitAll()\n"
             "      .anyRequest().authenticated())\n"
             "    .addFilterBefore(new ExceptionHandlerFilter(), AuthenticationFilter.class)\n"
             "    .addFilter(authenticationFilter)\n"
             "    .addFilterAfter(new JWTAuthenticationFilter(jwtTokenService),\n"
             "                    AuthenticationFilter.class)\n"
             "    .sessionManagement(s ->\n"
             "      s.sessionCreationPolicy(SessionCreationPolicy.STATELESS));\n"
             "  return http.build();\n"
             "}")
    doc.code("Listing C.2 \u2014 the aggregation of a day's totals",
             "private void adjustMacros(DietPlanTrack dietPlanTrack) {\n"
             "  MealKcal mealKcal = dietPlanTrack.getMealKcal();\n"
             "  dietPlanTrack.getProtein().setTaken(\n"
             "    mealKcal.getBreakfast().getProtein().getTaken()\n"
             "      + mealKcal.getLunch().getProtein().getTaken()\n"
             "      + mealKcal.getDinner().getProtein().getTaken()\n"
             "      + mealKcal.getSnack().getProtein().getTaken());\n"
             "  dietPlanTrack.getCarbs().setTaken(\n"
             "    mealKcal.getBreakfast().getCarbs().getTaken()\n"
             "      + mealKcal.getLunch().getCarbs().getTaken()\n"
             "      + mealKcal.getDinner().getCarbs().getTaken()\n"
             "      + mealKcal.getSnack().getCarbs().getTaken());\n"
             "  dietPlanTrack.getFat().setTaken(\n"
             "    mealKcal.getBreakfast().getFat().getTaken()\n"
             "      + mealKcal.getLunch().getFat().getTaken()\n"
             "      + mealKcal.getDinner().getFat().getTaken()\n"
             "      + mealKcal.getSnack().getFat().getTaken());\n"
             "}")
    doc.code("Listing C.3 \u2014 the meal category constants and their validation",
             "public final class MacrosConstants {\n"
             "  public static final String BREAKFAST = \"breakfast\";\n"
             "  public static final String LUNCH = \"lunch\";\n"
             "  public static final String SNACK = \"snack\";\n"
             "  public static final String DINNER = \"dinner\";\n"
             "\n"
             "  private MacrosConstants() {}\n"
             "\n"
             "  public static boolean validateMacro(String macro) {\n"
             "    return switch (macro.toLowerCase()) {\n"
             "      case BREAKFAST, LUNCH, SNACK, DINNER -> true;\n"
             "      default -> false;\n"
             "    };\n"
             "  }\n"
             "}")

    doc.prefix_numbering("D")
    doc.h2("Appendix D", "User Guide", key="appx-d")
    doc.p(
        "This appendix describes how to run the delivered system and how to carry out the sequence of "
        "operations that the screenshots in Chapter 9 record. It assumes a machine with a Java 21 "
        "runtime, Node.js and a running database instance."
    )
    doc.numbered([
        "Start the database. Confirm that the daemon is listening on the default port and that the "
        "application can create a database named macrova.",
        "Supply the three environment variables. The service requires a token secret, a key for the "
        "model provider and a model identifier; without all three it refuses to start, which is the "
        "configuration decision recorded in Section 5.5.",
        "Start the service from the backend directory with the Maven wrapper and wait until the log "
        "reports that the embedded container has started.",
        "Start the client from the frontend directory with npm start and open the development server "
        "address in a browser. The proxy forwards requests under the /api prefix to the service.",
        "Register an account, sign in, and confirm that the application routes to the empty state "
        "because no plan exists.",
        "Create a plan. Enter the body metrics, choose an intensity and a duration, adjust the macro "
        "split if required, review the summary and confirm. The dashboard then shows the first day of "
        "the plan with an empty goal meter.",
        "Log a day. Open the progress page, enter the macronutrient grams for each meal and update the "
        "weight. The meter and the summary change with each submission.",
        "Review the history. Open the history list, select the plan and open one of its days to see the "
        "read-only view.",
        "Request suggestions. Open the suggestions page, choose the four filters and request "
        "suggestions; a failure here indicates an unreachable provider or a malformed reply rather than "
        "a defect in the rest of the system.",
    ])
    doc.p(
        "Two operational notes complete the guide. The application stores dates at UTC midnight, so a "
        "document created shortly after local midnight in a positive-offset zone may appear under the "
        "previous date in a direct database inspection. And the development profile issues the refresh "
        "cookie without the secure attribute, so the system should not be exposed beyond the "
        "developer's machine without the configuration changes listed in Chapter 12."
    )
    return doc
