"""Chapters 1 to 4: introduction, literature review, system analysis and system design."""


def build(doc):
    # ================================================================== CHAPTER 1
    doc.chapter_heading(1, "Introduction", key="ch1")

    doc.h2("1.1", "Overview of the Project", key="s1.1")
    doc.p(
        "Macrova is a web application that helps an individual plan, follow and review a diet. A user "
        "answers a short questionnaire about body measurements, activity and goal; the application "
        "estimates the energy that the user expends each day, converts that estimate into a daily "
        "calorie target by applying a chosen deficit or surplus, and further converts the calorie "
        "target into a protein, carbohydrate and fat budget in grams. The budget is then divided "
        "across the meals of the day, and the user records what was actually eaten against it. Every "
        "figure the application displays is therefore traceable to a published equation followed by a "
        "sequence of documented arithmetic steps."
    )
    doc.p(
        "The idea for the project came from a simple observation about the tools that a dieter "
        "actually uses. A spreadsheet is transparent but labour-intensive: every recalculation is "
        "manual and every mistake is the user's own. A commercial application is convenient but "
        "opaque: the plan arrives fully formed and the reasoning behind a target of, say, 1,850 "
        "kilocalories is never shown. Macrova was built to occupy the middle ground. The arithmetic "
        "is exposed in the interface at each step of plan construction, and the same arithmetic is "
        "isolated in one utility class in the source, so that a reader of this report can check the "
        "number on a screen against the equation that produced it."
    )
    doc.p(
        "The system is implemented as three tiers. The browser runs an Angular single-page client that "
        "renders twenty components across thirteen routes. A Spring Boot service on Java 21 exposes a "
        "JSON interface of twenty-six endpoints and implements the domain rules. A MongoDB instance "
        "stores three collections in normal operation: users, plans and daily tracking documents. A "
        "fourth collection exists for AI-generated suggestions and is deliberately not written to. "
        "The report documents the whole of that stack, from the equation to the colour of the buttons "
        "in the tracking screen."
    )

    doc.h2("1.2", "Background of the Study", key="s1.2")
    doc.p(
        "Weight management is, at the level of physics, an energy-balance problem. A person gains mass "
        "when energy intake exceeds energy expenditure and loses mass in the opposite case. The "
        "clinical literature refines that statement considerably, because the composition of the mass "
        "lost or gained depends on the macronutrient distribution of the diet, on the training "
        "stimulus and on the individual's hormonal state, but the balance itself remains the "
        "governing constraint. The practical consequence is that a dieting application needs two "
        "capabilities and not one: an estimate of expenditure, from which a target is derived, and a "
        "record of intake, from which adherence is measured."
    )
    doc.p(
        "Estimating expenditure is the more difficult of the two because it cannot be measured outside "
        "a laboratory without equipment. The accepted approach in clinical and sports practice is to "
        "predict the basal metabolic rate from readily available variables and then to scale it by an "
        "activity factor. The Mifflin\u2013St Jeor equation, published in 1990, is the prediction "
        "equation most widely recommended for healthy adults, and it requires only mass, height, age "
        "and sex. This project adopts that equation, together with the conventional five-level "
        "activity scale, and records the choice and its alternatives in Chapter 2."
    )
    doc.p(
        "Recording intake is, in principle, a database problem, but in practice it is a design "
        "problem. A user who must record a meal in six steps abandons the application within a week. "
        "Macrova therefore records intake at the level of the meal rather than at the level of the "
        "food: the tracking screen asks for three numbers per meal and nothing else. The trade-off is "
        "explicit and is discussed in Section 3.6: the application measures adherence to a "
        "macronutrient budget accurately, but it does not tell the user which foods to eat in order to "
        "meet that budget. The optional language-model feature of Chapter 6 is an attempt to soften "
        "that limitation without turning the application into a food database."
    )

    doc.h2("1.3", "Problem Statement", key="s1.3")
    doc.p(
        "The problem addressed by the project can be stated in four parts. First, the calculation of a "
        "personal calorie target is arithmetically simple but procedurally error-prone, because it "
        "involves four successive conversions, each with its own rounding convention, and an error in "
        "any one of them propagates silently into every figure the dieter sees. Second, the "
        "translation of a calorie target into meals requires a macronutrient policy, and most dieters "
        "do not have one; the consequence is a plan that meets the energy constraint while violating "
        "the protein requirement that would preserve lean mass. Third, adherence is invisible without "
        "a record, and a record is worthless unless it is easy enough to keep. Fourth, the "
        "nutritional advice available to a dieter from general-purpose language models is fluent but "
        "unverified, and there is no convenient way for a dieter to see that the calorie figure "
        "attached to a generated meal is a plausible guess rather than a measurement."
    )
    doc.p(
        "No single existing tool addresses all four parts together. Calorie-counting applications "
        "address the third part well and the first three badly: they contain a target that the user "
        "cannot reconstruct and a food database whose values the user cannot audit. Spreadsheets "
        "address the first part, since the formulas are visible, and fail at the third, because data "
        "entry is too laborious to sustain. Static diet charts address the second part only, and "
        "general-purpose chatbots address none of them reliably. Macrova is an attempt to build the "
        "small system in which all four parts are handled by design rather than by convention."
    )

    doc.h2("1.4", "Objectives of the Project", key="s1.4")
    doc.p(
        "The project set six objectives. They are stated here in the form in which they were adopted "
        "at the start of the work, and each is answered later in the report at the section named in "
        "parentheses."
    )
    doc.numbered([
        "To implement the Mifflin\u2013St Jeor prediction equation and the conventional activity "
        "factors as a single, documented, unit-testable utility, so that the energy estimate has one "
        "implementation and one explanation (Sections 10.2 and 10.3).",
        "To derive a daily calorie target from that estimate by applying a selectable deficit or "
        "surplus and a deterministic rounding rule, and to record the derivation in the stored plan "
        "so that the target can be reconstructed after the fact (Sections 10.4 and 7.3).",
        "To convert the calorie target into macronutrient gram targets under a selectable policy and "
        "to divide those targets across the meals of the day, so that a user knows what to eat at "
        "each meal rather than only what to eat in a day (Sections 10.5 and 10.6).",
        "To provide a plan-construction flow that persists its progress, so that a user who is "
        "interrupted does not lose the work already done, and so that backward navigation can be "
        "served from stored state (Section 10.9).",
        "To provide a daily record that a user can maintain in seconds, with per-meal logging and a "
        "weight entry, and immediate feedback on the proportion of the budget consumed (Sections 9.6 "
        "and 10.7).",
        "To integrate an optional language-model feature that suggests meals constrained by the "
        "computed calorie allowance of a specific meal, while keeping the model's output entirely "
        "outside the deterministic record of the user's plan (Sections 6.4 and 11.4).",
    ])
    doc.p(
        "A seventh objective emerged during implementation and is recorded because it shaped the "
        "document: to verify, rather than merely assert, that the delivered repository implements "
        "what the report describes. Chapter 11 is the result of that objective, and its most useful "
        "output is not the list of features that work but the list of six things that do not, or do "
        "not yet."
    )

    doc.h2("1.5", "Scope of the Project", key="s1.5")
    doc.p(
        "The scope is bounded deliberately, and the boundary is drawn in four places: the actors, the "
        "nutritional model, the input granularity and the deployment profile."
    )
    doc.p(
        "There is exactly one actor. Macrova serves an individual dieter who manages their own plan. "
        "There is no dietician role, no administrator role, no clinic and no supervision relationship. "
        "Every document in the database is owned by the user who created it and is reachable only "
        "through that ownership, which is why the identity module is the smallest in the system and "
        "the scoping rule in the service layer is the most heavily used."
    )
    doc.p(
        "The nutritional model is energy and macronutrients, and nothing else. The application does "
        "not model micronutrients, fibre, hydration, glycaemic index, allergies or medical conditions. "
        "It does not claim to be a clinical tool, and Section 3.6 states the exclusion explicitly. The "
        "consequence is a system that can be verified arithmetically, which a micronutrient model "
        "could not be without a food-composition table containing several thousand entries."
    )
    doc.p(
        "Intake is recorded as macronutrient grams per meal rather than as food items. This is the "
        "most consequential scope decision in the project. It makes the daily record quick enough to "
        "sustain and the arithmetic exact, at the cost of requiring the user to know the macronutrient "
        "content of their meal. A food database would remove that requirement and would introduce a "
        "second, far larger, verification problem; the trade-off is analysed in Section 3.5.3 and the "
        "enhancement is proposed in Chapter 12."
    )
    doc.p(
        "The deployment profile is a single-machine development profile. The service runs on an "
        "embedded container, the client on the Angular development server, and the database on a "
        "local instance. There is no container orchestration, no reverse proxy, no transport security "
        "and no production secrets management. That is a scope boundary rather than an oversight, and "
        "Chapter 11 records it as a limitation precisely because a reviewer should not read the "
        "security chapter as a description of a hardened deployment."
    )

    doc.h2("1.6", "Project Motivation", key="s1.6")
    doc.p(
        "Three motives sustained the work. The first is academic: the project sits at the intersection "
        "of two subjects taught in the programme, namely application development on a modern web "
        "stack and the disciplined specification of a software system. Building a system whose "
        "correctness is arithmetically checkable was a way of making the second subject concrete. If "
        "a reviewer can take the equation from Section 10.2, apply it to the values in Section 7.3 "
        "and obtain the figure displayed in Figure 9.6, then the report has demonstrated something "
        "about its own claims that a screenshot alone never could."
    )
    doc.p(
        "The second motive is practical. The author has followed a structured diet and has used both "
        "of the tool categories described in Section 1.3, and the failure mode of the spreadsheet is "
        "familiar: the effort of maintaining it exceeds the value of the information it contains "
        "within about a fortnight. The design decisions that follow, particularly the four-step "
        "wizard and the three-field meal card, were made in direct response to that experience rather "
        "than derived from a requirements catalogue."
    )
    doc.p(
        "The third motive is technical curiosity about the boundary between deterministic and "
        "generated computation. A diet application is an unusually good place to explore that "
        "boundary, because the part that must never be wrong, namely the arithmetic that governs the "
        "plan, is completely separable from the part that may reasonably be approximate, namely the "
        "suggestion of what to cook. The architecture of Chapter 4 preserves that separation "
        "structurally rather than by convention: the suggestion feature cannot write into a plan, "
        "because no code path allows it."
    )

    doc.h2("1.7", "Assumptions and Constraints", key="s1.7")
    doc.p(
        "The project rests on five assumptions about the user and the environment, each of which, if "
        "false, would change the design. It assumes that the user knows their own height, weight and "
        "age accurately; that the user can estimate the macronutrient content of a meal to within a "
        "few grams; that the user has a browser capable of running a modern single-page application; "
        "that the user's weight changes slowly enough for a weekly trend line to be meaningful; and "
        "that the user is not following a medically supervised diet, in which case the assumptions "
        "built into the prediction equation would not hold."
    )
    doc.p(
        "The constraints that limited the implementation are of three kinds. The technical constraints "
        "are those of a student project: a single developer, a single development machine, no "
        "cloud budget and no continuous-integration service. The result is a repository with one "
        "automated test and a local build, which Chapter 11 reports as a limitation rather than "
        "presenting the absence of tests as a design choice."
    )
    doc.p(
        "The data constraints are more interesting. The project had no access to a licensed "
        "food-composition database, and the freely available tables are either incomplete for Indian "
        "composite dishes or carry licensing terms that preclude redistribution in a student "
        "repository. That constraint produced the scope decision of Section 1.5: intake is recorded "
        "as macronutrient grams, for which no external table is needed, and the food-level detail is "
        "left to the optional suggestion feature, where the values are explicitly labelled as "
        "unverified."
    )
    doc.p(
        "The environmental constraints follow from the same cause. The application is reached over "
        "plain HTTP on the development server; the refresh cookie therefore cannot carry the secure "
        "attribute; and the cross-origin allow-list is pinned to one development origin. These are "
        "coded as configuration rather than as constants, but they are not parameterised by profile, "
        "which is why Chapter 12 proposes that change before any other security work."
    )

    doc.h2("1.8", "Organisation of the Report", key="s1.8")
    doc.p(
        "The report has twelve chapters and four appendices. Chapter 1 states the problem, the "
        "objectives and the boundaries. Chapter 2 reviews the literature in five areas that the design "
        "depends on: energy prediction, the behaviour of self-monitoring, the architecture of "
        "single-page clients, the design of resilient HTTP interfaces and the characteristics of "
        "generative models as sources of advice. Chapter 3 analyses the existing practice, defines the "
        "requirements in a numbered specification, and evaluates technical, economic and operational "
        "feasibility. Chapter 4 presents the design: the layered architecture, the data-flow and "
        "use-case models, the object and dynamic models, the data model, the interface design and the "
        "security design."
    )
    doc.p(
        "Chapters 5 to 10 document the implementation. Chapter 5 records the technologies, versions "
        "and justifications. Chapter 6 describes the eight modules and the behaviour each implements. "
        "Chapter 7 gives the data dictionary for every collection, with a worked example. Chapter 8 "
        "catalogues the interface and the client services. Chapter 9 presents the fifteen screens with "
        "an account of what each one shows. Chapter 10 derives the six algorithms from their "
        "equations, reproduces the code that implements them and states the pseudocode of the whole "
        "plan-and-track cycle. Chapter 11 reports the testing and verification exercise, including the "
        "ten findings it produced, and Chapter 12 concludes with the limitations and an ordered list "
        "of enhancements. The appendices give the endpoint reference, the requirement-to-artefact "
        "verification matrix, three source listings and a user guide."
    )

    # ================================================================== CHAPTER 2
    doc.chapter_heading(2, "Literature Review", key="ch2")
    doc.h2("2.1", "Introduction", key="s2.1")
    doc.p(
        "This chapter reviews the work on which the design of Macrova depends. It is organised by the "
        "question that each body of literature answers rather than by discipline, because the project "
        "draws on nutrition science, behavioural science and software engineering in roughly equal "
        "measure. For each of the fourteen reviews that follow, the source is identified, its central "
        "contribution is stated, and the specific design decision that it informs is named. The "
        "chapter then compares the reviewed work in a table, identifies the four gaps that this "
        "project addresses and closes with a summary."
    )

    doc.h2("2.2", "Review of Related Work", key="s2.2")
    doc.h3("2.2.1", "Predictive equations for resting energy expenditure", key="s2.2.1")
    doc.p(
        "<b>Author and year:</b> Mifflin, St Jeor, Hill, Scott, Daugherty and Koh, 1990."
    )
    doc.p(
        "The paper reports a cross-validation study of published equations for resting energy "
        "expenditure against indirect calorimetry in a sample of healthy adults, and proposes the "
        "equation now known by the authors' names. Its contribution is not the discovery of a new "
        "physiological mechanism but the demonstration that a four-variable linear model predicts "
        "measured expenditure more accurately across the range of body composition than the "
        "Harris\u2013Benedict equation that had been standard for seventy years."
    )
    doc.p(
        "<b>Relevance to the present work:</b> The equation is implemented verbatim as "
        "NutrientsCalculator.findBMR and reproduced in Listing 10.1. The choice of this equation over "
        "Harris\u2013Benedict is recorded in Section 10.2, and the sex-specific constants plus five "
        "and minus one hundred and sixty-one are held as conditional expressions rather than as a "
        "lookup table so that the source reads like the published formula."
    )
    doc.h3("2.2.2", "Re-evaluation of predictive equations in clinical practice",
         key="s2.2.2")
    doc.p("<b>Author and year:</b> Frankenfield, Roth-Yousey and Compher, 2005.")
    doc.p(
        "A systematic review comparing the accuracy of predictive equations against measured resting "
        "metabolic rate in non-obese and obese adults. It concludes that no equation is accurate for "
        "every individual, that the Mifflin\u2013St Jeor equation is the most consistently accurate in "
        "non-obese adults, and that in obese individuals the equations tend to over-predict, which in "
        "practice leads clinicians to use an adjusted body mass."
    )
    doc.p(
        "<b>Relevance to the present work:</b> Two design consequences follow. First, the application "
        "states the estimate as one, not as a measurement: the goal-selection screen shows the energy "
        "requirement with a leading approximation mark, and the abstract describes it as an estimate. "
        "Second, the surplus rule of Section 10.4 subtracts ten percentage points from the nominal "
        "intensity, which is a conservative correction consistent with the review's finding that "
        "prediction in the direction of gain is where overestimation is most consequential."
    )
    doc.h3("2.2.3", "Physical activity levels and total energy expenditure", key="s2.2.3")
    doc.p(
        "<b>Author and year:</b> Food and Agriculture Organization, World Health Organization and "
        "United Nations University, 2004."
    )
    doc.p(
        "The joint expert consultation report on human energy requirements sets out the factorial "
        "method by which resting expenditure is scaled to total expenditure through graded physical "
        "activity levels. It provides the canonical definitions of the sedentary, light, moderate, "
        "heavy and vigorous categories and the ranges of the multiplier associated with each."
    )
    doc.p(
        "<b>Relevance to the present work:</b> The five activity multipliers held in the Activity "
        "enumeration (1.2, 1.375, 1.55, 1.725 and 1.9) are the conventional values associated with "
        "the five levels used by the application. The enumeration holds the multiplier as its "
        "constructor argument, x, which is the pattern the report recommends for every physiological constant."
    )
    doc.h3("2.2.4", "Self-monitoring as the active ingredient of weight management",
         key="s2.2.4")
    doc.p("<b>Author and year:</b> Burke, Wang and Sevick, 2011.")
    doc.p(
        "A systematic review of self-monitoring interventions in weight-loss programmes. Its finding "
        "is that the frequency and consistency of self-monitoring, rather than the specific diet "
        "prescribed, predicts weight loss, and that participants who monitor more often lose more "
        "weight. It also documents the progressive decline in monitoring frequency that precedes "
        "withdrawal from a programme."
    )
    doc.p(
        "<b>Relevance to the present work:</b> This review is the strongest single justification for "
        "the design of the tracking screen in Section 9.6. The screen asks for three numbers per meal, "
        "commits each meal independently so that a partial record is still a record, and re-renders "
        "the whole day from one response so that the user receives feedback with no perceptible "
        "latency. The decline in frequency documented by the review is the behaviour that the "
        "resumable wizard and the one-tap weight update are intended to mitigate."
    )
    doc.h3("2.2.5", "The effect of goal setting and feedback on adherence", key="s2.2.5")
    doc.p("<b>Author and year:</b> Michie, Abraham, Whittington, McAteer and Gupta, 2009.")
    doc.p(
        "A meta-regression of behaviour-change techniques across interventions in healthy eating and "
        "physical activity. It identifies self-monitoring, goal setting and feedback on progress as "
        "the techniques with the largest and most consistent effect sizes, and notes that the "
        "combination of all three outperforms any one of them alone."
    )
    doc.p(
        "<b>Relevance to the present work:</b> The dashboard of Section 9.5 is an implementation of "
        "the combination: a target is set during plan construction, progress towards it is rendered "
        "as a percentage with a meter, and the weekly weight observations provide feedback on the "
        "outcome rather than on the behaviour. The percentage is computed on the server rather than in "
        "the client, which is a small decision with a large consequence for this technique: the "
        "feedback figure cannot diverge between two devices."
    )
    doc.h3("2.2.6", "Standalone components and signals in Angular", key="s2.2.6")
    doc.p("<b>Author and year:</b> Google Angular Team, 2024\u20132025.")
    doc.p(
        "The framework documentation for the standalone-component model and the signal-based "
        "reactivity primitives introduced in recent major versions. The documentation argues that the "
        "declarative dependency of a component on its inputs and of a template on a signal makes "
        "change propagation both cheaper and easier to reason about than the zone-based detection "
        "model that it complements."
    )
    doc.p(
        "<b>Relevance to the present work:</b> The client uses standalone components throughout: there "
        "is no NgModule in the repository except the bootstrap configuration, and every route loads a "
        "component directly. The username displayed in the header is a signal, and the avatar initial "
        "is a computed signal derived from it. The four wizard steps declare their inputs and outputs "
        "with the signal-based functions, which turns a mismatch between a step and its host into a "
        "compile error. Zone-based detection is nevertheless retained, because the HTTP client and the "
        "chart library both depend on it."
    )
    doc.h3("2.2.7", "Functional HTTP interceptors for cross-cutting concerns", key="s2.2.7")
    doc.p("<b>Author and year:</b> Google Angular Team, 2024.")
    doc.p(
        "The documentation of the functional interceptor API, which replaces class-based interceptors "
        "with functions registered in the application configuration. It documents the composition "
        "order of a chain of interceptors and the use of higher-order mapping operators to delay a "
        "request until an asynchronous precondition, such as a token refresh, has completed."
    )
    doc.p(
        "<b>Relevance to the present work:</b> Two functional interceptors are registered in the "
        "order base prefix followed by token attachment. The second uses switchMap to wait for a "
        "refresh and then dispatch the original request, and it skips the public authentication paths "
        "by inspecting the URL after the first interceptor has rewritten it. That ordering dependency "
        "is the reason the chain is registered in a specific sequence rather than arbitrarily, and it "
        "is documented in Section 8.6."
    )
    doc.h3("2.2.8", "Stateless authentication with JSON Web Tokens", key="s2.2.8")
    doc.p("<b>Author and year:</b> Jones, Bradley and Sakimura, 2015 (RFC 7519); Jones, Bradley and "
           "Sakimura, 2015 (RFC 7515).")
    doc.p(
        "The standards that define the token format and the signature that protects it. The token "
        "carries a set of claims, of which the subject, the issue time and the expiry are the ones "
        "this project depends on, and the signature allows a resource server to verify the token "
        "without retaining server-side state. The standards are explicit that a token cannot be "
        "withdrawn once issued, which is a property, not a defect, but one that has design "
        "consequences."
    )
    doc.p(
        "<b>Relevance to the present work:</b> The application issues two tokens: a short-lived access "
        "token carried in the authorisation header and a longer-lived refresh token carried in an "
        "HttpOnly cookie. The stateless property is what allows the security configuration to declare "
        "a stateless session policy, and the irreversibility of an issued token is precisely why "
        "Section 11.3 records the absence of refresh-token rotation and revocation as a finding rather "
        "than presenting sign-out as a complete session termination."
    )
    doc.h3("2.2.9", "Adaptive password hashing with BCrypt", key="s2.2.9")
    doc.p("<b>Author and year:</b> Provos and Mazi\u00e8res, 1999.")
    doc.p(
        "The paper that introduced the adaptive hashing scheme based on the Blowfish cipher. Its "
        "contribution is a work factor that can be increased as hardware becomes faster, combined with "
        "a per-password salt, so that the cost of an offline dictionary attack rises with the cost of "
        "legitimate authentication rather than remaining fixed."
    )
    doc.p(
        "<b>Relevance to the present work:</b> The password encoder bean is the Spring Security "
        "BCrypt implementation with the default work factor. The user entity stores the sixty-"
        "character output including the salt prefix, no response DTO contains the field, and the "
        "authentication manager compares through the encoder rather than by string equality, so the "
        "comparison is constant-time with respect to the hash."
    )
    doc.h3("2.2.10", "Spring Data repositories and projection queries", key="s2.2.10")
    doc.p("<b>Author and year:</b> Broadcom and VMware Tanzu, 2024\u20132025.")
    doc.p(
        "The reference documentation for the repository abstraction. It describes derivation of query "
        "methods from method names, the use of explicit query annotations where a derived name would "
        "be unwieldy, and the projection mechanism by which a query returns an interface or a DTO "
        "populated from a selected subset of fields rather than a complete document."
    )
    doc.p(
        "<b>Relevance to the present work:</b> Both repositories declare projection queries for the "
        "history screens. The plan history projection selects seven fields, and the tracking overview "
        "projection selects eight, so a page listing a hundred days transfers a hundred small objects "
        "rather than a hundred documents each containing four embedded meal tracks. Section 7.6 uses "
        "the same documentation to argue for the compound indexes that the projections would benefit "
        "from."
    )
    doc.h3("2.2.11", "Document databases for aggregate-oriented persistence", key="s2.2.11")
    doc.p("<b>Author and year:</b> Sadalage and Fowler, 2012.")
    doc.p(
        "The book that introduced the vocabulary of aggregate orientation for NoSQL stores. Its "
        "central claim is that the unit of consistency and the unit of retrieval should determine the "
        "document boundary, and that embedding is preferable to referencing when two pieces of data "
        "are always read together, whereas referencing is preferable when they are not."
    )
    doc.p(
        "<b>Relevance to the present work:</b> The decision to embed the four meal tracks, the three "
        "daily macro totals and the intake object inside a single daily tracking document is taken "
        "directly from this principle, because the tracking page reads all of them together. The plan "
        "identifier is held as a plain string reference rather than as a database reference, because "
        "the plan is read independently of the day and is the subject of its own projections. "
        "Section 7.1 records the reasoning in the authors' own terms."
    )
    doc.h3("2.2.12", "Large language models as constrained generators", key="s2.2.12")
    doc.p("<b>Author and year:</b> Bommasani et al., 2021.")
    doc.p(
        "The survey of foundation models that documents both the generality of large pre-trained "
        "models and their characteristic failure mode, namely the fluent production of plausible but "
        "incorrect content. It recommends constraining generation with a structured prompt and "
        "treating output as a candidate to be validated rather than as a fact."
    )
    doc.p(
        "<b>Relevance to the present work:</b> The suggestion feature follows both recommendations. "
        "The system message fixes an output schema in JSON, the user message carries a calorie "
        "allowance already computed by the deterministic part of the system, and the reply is parsed "
        "into objects and rendered as cards without ever being written into a plan. Section 11.4 "
        "records the residual risk: the schema instruction is a request, not a constraint, and the "
        "nutritional values are unvalidated."
    )
    doc.h3("2.2.13", "Nutritional misinformation and the limits of generated advice",
         key="s2.2.13")
    doc.p("<b>Author and year:</b> Open Worldwide Application Project, 2021, in its treatment of "
           "untrusted input and output; supplemented by the clinical-nutrition commentary on "
           "generated dietary advice.")
    doc.p(
        "The security guidance treats model output as untrusted data, and the nutrition commentary "
        "argues that plausible but unverified dietary recommendations are particularly dangerous in a "
        "domain where the reader may have an allergy, a comorbidity or a medication interaction that "
        "the generator cannot know about."
    )
    doc.p(
        "<b>Relevance to the present work:</b> The interface labels the results as suggestions, the "
        "prompt includes four filters including diet type, and the report states the limitation in the "
        "abstract, in Section 6.4, in Section 11.4 and again in Section 12.4. A future revision would "
        "add a restriction profile and a cross-check against a curated list, which is the ninth "
        "proposal of Chapter 12."
    )
    doc.h3("2.2.14", "Chart libraries and accessible data visualisation", key="s2.2.14")
    doc.p("<b>Author and year:</b> Chart.js Contributors, 2024.")
    doc.p(
        "The documentation for a canvas-based charting library that renders a data series with a "
        "declarative configuration object. It documents the responsive behaviour of a canvas chart, "
        "the axis configuration, and the accessibility limitations that follow from canvas rendering, "
        "which requires a textual alternative for users of assistive technology."
    )
    doc.p(
        "<b>Relevance to the present work:</b> The dashboard renders the weekly weight observations as "
        "a single-series line chart with a labelled axis. The accessibility limitation is real and is "
        "not mitigated in the delivered client; the six metric cards above the chart do provide the "
        "same information in text, which is the reason the chart was placed beneath them rather than "
        "above them."
    )

    doc.h2("2.3", "Comparative Study of the Reviewed Work", key="s2.3")
    doc.p(
        "The fourteen reviews span three disciplines, and Table 2.1 reduces them to a comparison on the "
        "dimensions that mattered for the design. The table is included because the literature review "
        "of a software project is often a list of summaries that never converge; here the final column "
        "names the artefact in which each source is realised."
    )
    doc.table(
        "Comparative summary of the reviewed literature",
        ["Source", "Discipline", "Central contribution", "Realised as"],
        [
            ["Mifflin et al., 1990", "Nutrition science",
             "Four-variable prediction of resting expenditure", "findBMR, Listing 10.1"],
            ["Frankenfield et al., 2005", "Clinical nutrition",
             "Accuracy limits of every prediction equation", "Conservative surplus rule, Section 10.4"],
            ["FAO/WHO/UNU, 2004", "Nutrition science", "Graded activity multipliers",
             "Activity enumeration, Table 10.2"],
            ["Burke et al., 2011", "Behavioural science", "Monitoring frequency predicts outcome",
             "Three-field meal card, Section 9.6"],
            ["Michie et al., 2009", "Behavioural science", "Goal, monitor and feedback combined",
             "Dashboard, Section 9.5"],
            ["Angular Team, 2025", "Software engineering", "Standalone components and signals",
             "Twenty components, Section 6.6"],
            ["Angular Team, 2024", "Software engineering", "Functional interceptor composition",
             "Two interceptors, Section 8.6"],
            ["RFC 7519 and RFC 7515", "Standards", "Stateless signed token", "JWTTokenService"],
            ["Provos and Mazi\u00e8res, 1999", "Security", "Adaptive password hashing",
             "Password encoder bean"],
            ["Spring Data, 2025", "Software engineering", "Derived queries and projections",
             "Two projection queries, Section 7.6"],
            ["Sadalage and Fowler, 2012", "Data engineering", "Aggregate orientation",
             "Embedded meal tracks, Section 7.1"],
            ["Bommasani et al., 2021", "Machine learning", "Constrained generation as a mitigation",
             "Schema-constrained prompt, Section 10.10"],
            ["OWASP, 2021", "Security", "Untrusted output must be treated as data",
             "No persistence of model output"],
            ["Chart.js, 2024", "Data visualisation", "Declarative canvas chart",
             "Weight trend chart, Figure 9.9"],
        ],
        widths=[20, 16, 32, 32], font_size=8.0)

    doc.h2("2.4", "Research Gaps Identified", key="s2.4")
    doc.p(
        "Reading the fourteen sources together reveals four gaps, and the project was shaped around "
        "them. The first is the gap between the accuracy of the published equations and the "
        "transparency of the applications that use them. The nutrition literature is explicit that a "
        "prediction carries an error band, and no consumer application reviewed for this project "
        "exposes the derivation that would let a user understand why their target is what it is."
    )
    doc.p(
        "The second gap is at the boundary between the behavioural literature and interface design. "
        "The reviews establish that monitoring, goal setting and feedback work, and they do not "
        "specify how few inputs a monitoring screen can have before the data become useless. Macrova "
        "resolves that design question by choosing three inputs per meal and committing each meal "
        "independently, and Section 9.10 states the cost of that choice: the application measures "
        "adherence to a budget but does not describe the meal that met it."
    )
    doc.p(
        "The third gap is the treatment of generated nutrition advice. The machine-learning "
        "literature recommends constrained generation and validation, and the clinical literature "
        "warns against unverified advice, and consumer applications that use language models rarely "
        "make the distinction visible to the user. Macrova makes it visible in the interface and "
        "structural in the code, and Chapter 11 quantifies what remains unsafe."
    )
    doc.p(
        "The fourth gap is documentary rather than technical. Student and small-team projects "
        "frequently report behaviour that the accompanying repository does not implement, because no "
        "verification step stands between the code and the prose. Chapter 11 of this report is an "
        "attempt to close that gap for this project, and it is the part of the work that the author "
        "would recommend to any subsequent project of the same kind."
    )

    doc.h2("2.5", "Summary of the Literature Review", key="s2.5")
    doc.p(
        "The literature supplies the project with a validated energy model, a validated behavioural "
        "rationale for its tracking design, established architectural patterns for its client and its "
        "interface, established security primitives for its authentication and an explicit warning "
        "about the class of feature that its suggestion module belongs to. What it does not supply, "
        "and what this project therefore had to decide, is how those elements combine into a small "
        "coherent system: which data are embedded and which are referenced, how many inputs a "
        "monitoring screen may ask for, how a plan is resumed after an interruption, and how a "
        "generated suggestion is prevented from contaminating a deterministic record. Chapter 4 "
        "presents the resulting design."
    )

    # ================================================================== CHAPTER 3
    doc.chapter_heading(3, "System Analysis", key="ch3")
    doc.h2("3.1", "Existing System Analysis", key="s3.1")
    doc.p(
        "Three classes of existing system were examined. The first is the spreadsheet, which is the "
        "most transparent and the least sustainable. The second is the commercial calorie-tracking "
        "application, which is the most sustainable and the least transparent. The third is the "
        "general-purpose conversational assistant, which is the most available and the least "
        "verifiable. Table 3.1 compares them against the six capabilities that the project requires."
    )
    doc.table(
        "Comparison of existing approaches against the required capabilities",
        ["Capability", "Spreadsheet", "Calorie-tracking application",
         "Conversational assistant"],
        [
            ["Energy estimate with a stated derivation", "Manual; correct if the formulas are",
             "Computed internally; not shown", "Stated fluently; not reproducible"],
            ["Macronutrient budget", "Manual", "Configurable preset", "Described in prose"],
            ["Per-meal plan", "Manual", "Yes, food-level", "Yes, food-level, unverified"],
            ["Daily record", "Manual entry, laborious", "Extensive food database",
             "Not retained between sessions"],
            ["Progress feedback", "Manual charts", "Yes, with trends", "None"],
            ["Auditability of the numbers", "Complete", "None", "None"],
        ],
        widths=[24, 24, 26, 26], font_size=8.2)
    doc.p(
        "The comparison clarifies what is unusual about the requirement. Auditability, which the "
        "spreadsheet alone provides, is a property of the calculation rather than of the data, and it "
        "does not require the data entry to be manual. The design of Macrova takes auditability from "
        "the first column and the interaction model from the second, and rejects the third entirely as "
        "a system of record."
    )

    doc.h2("3.2", "Limitations of the Existing System", key="s3.2")
    doc.p(
        "The limitations were identified by using each class of tool for the purpose it is designed "
        "for and recording where the use failed. They are stated as limitations of the approach rather "
        "than of any particular product, because the products change and the approaches do not."
    )
    doc.bullets([
        "A spreadsheet has no notion of a session. The formulas live in cells that the user can "
        "overwrite, and a single accidental edit changes every subsequent figure with no record of the "
        "change.",
        "A spreadsheet has no notion of a plan. The user holds one document in which past and present "
        "are mixed, so the comparison of this month's adherence with last month's requires manual "
        "versioning.",
        "A commercial application hides the derivation of its targets. A user cannot tell whether the "
        "1,850 kilocalories prescribed reflect a prediction equation, a population average or a "
        "commercial decision, and therefore cannot adjust the target intelligently when the estimate "
        "proves wrong.",
        "A commercial application requires a food-level record, which is accurate and slow. The "
        "measured consequence reported in the behavioural literature is a decline in monitoring "
        "frequency and eventual abandonment.",
        "A conversational assistant has no memory of a plan. Each conversation begins from nothing, so "
        "the assistant cannot know that the user's dinner allowance is 538 kilocalories rather than a "
        "round thousand.",
        "A conversational assistant produces nutrition figures without provenance. There is no "
        "mechanism by which the user can distinguish a value drawn from a composition table from a "
        "value generated because it was plausible in context.",
    ])

    doc.h2("3.3", "Proposed System", key="s3.3")
    doc.p(
        "The proposed system is a single-user web application with three tiers and eight functional "
        "modules. Its distinguishing property is that the deterministic and the generated parts of the "
        "system are separated by construction: the plan, the tracking record and every figure derived "
        "from them are produced by the utility class of Chapter 10, and the language model is confined "
        "to a leaf module whose output is never written to the database."
    )
    doc.p(
        "The user's interaction has five stages. Registration creates an account and a hashed "
        "credential. Authentication exchanges the credential for an access token held in memory and a "
        "refresh token held in an HttpOnly cookie. Plan construction is a four-step wizard whose state "
        "is persisted at every step, so that an interruption costs nothing. Tracking is a single "
        "screen on which each meal is committed independently and the weight is updated in place. "
        "Review covers the dashboard, which recomputes progress on every load, and the history "
        "screens, which present past plans and their daily records through projections."
    )
    doc.figure("usecase-diagram.png",
               "Use-case model of the proposed system showing the single actor and the fourteen "
               "use cases", width=5.4)

    doc.h2("3.4", "Advantages of the Proposed System", key="s3.4")
    doc.p(
        "Six advantages follow from the analysis and are claimed on the evidence of Chapters 7 to 10. "
        "They are stated with the section in which each can be checked, because an advantage claimed "
        "without a location is an advertisement."
    )
    doc.numbered([
        "Auditability. Every displayed figure is produced by a method in one class, and Chapter 10 "
        "reproduces each method beside the equation it implements, so the figure on the screen can be "
        "recomputed by hand.",
        "Resumability. The wizard persists at each step and identifies its draft by the pair of user "
        "and pending status, so a user can close the browser and return to the step at which they "
        "stopped, including after a reload, and can navigate backward without a client-side draft.",
        "Low-friction recording. The daily record consists of twelve numbers across four cards, each "
        "committed by a single button, and the whole day is re-rendered from the response so that the "
        "feedback is immediate.",
        "Exact aggregation. The daily totals are recomputed from the four meal tracks on every update "
        "rather than accumulated, which makes a repeated submission idempotent and prevents the "
        "inflation that an accumulating design would permit.",
        "Ownership by construction. No endpoint accepts a user identifier from the client. Every query "
        "is built from the identifier in the security context, so identifier guessing yields a "
        "not-found response rather than another user's data.",
        "Honest treatment of generated content. The suggestion feature is optional, its output is "
        "never persisted, and its limitations are stated in the interface, in the abstract and in the "
        "verification chapter.",
    ])

    doc.h2("3.5", "Feasibility Study", key="s3.5")
    doc.h3("3.5.1", "Technical Feasibility", key="s3.5.1")
    doc.p(
        "The technical requirements were assessed against the skills and the tooling available. The "
        "back end uses the Spring Boot stack, which the programme covers in its enterprise-"
        "application modules, and the persistence layer uses a document store whose query model is "
        "simpler than the relational model that the programme also teaches. The front end uses "
        "Angular, and the four features that the design depends on, namely standalone components, "
        "functional interceptors, signals and guards, are all documented and current."
    )
    doc.p(
        "The one component with genuine technical uncertainty is the integration with a language "
        "model, because its output is not deterministic and its availability depends on a third party. "
        "That uncertainty was isolated rather than eliminated: the adapter is behind an interface, the "
        "endpoint is a leaf in the dependency graph, and the rest of the system neither calls it nor "
        "depends on its success. The architecture that results is technically feasible in the strong "
        "sense that every part except the leaf is deterministic and testable."
    )
    doc.h3("3.5.2", "Economic Feasibility", key="s3.5.2")
    doc.p(
        "The direct cost of the project is zero for the software. Every dependency is open source "
        "under a permissive licence, the database is free, and the development tooling is free. The "
        "only recurring cost is the model-provider usage, which is billed per token and is optional: "
        "the application cannot start without the key, but the feature can be left unused once it has "
        "started. Table 3.2 records the estimated cost of a demonstration."
    )
    doc.table(
        "Economic assessment of the delivered system",
        ["Item", "Basis", "Estimated cost", "Note"],
        [
            ["Java, Spring Boot, Angular, MongoDB", "Open-source licences", "Nil",
             "No runtime licence fee at any scale"],
            ["ReportLab, python-docx, PyMuPDF, Matplotlib", "Open-source licences", "Nil",
             "Used only to produce this report"],
            ["Model-provider usage", "Per token, optional", "Under one rupee per suggestion set",
             "Five suggestions require a prompt of about sixty tokens and a reply of about six "
             "hundred"],
            ["Development machine", "Already owned", "Nil",
             "The application runs on a laptop with four gigabytes of memory"],
            ["Hosting, if deployed", "Single small virtual machine", "Under five hundred rupees per "
                                                                     "month",
             "Sufficient for a demonstration to a group"],
        ],
        widths=[26, 24, 22, 28], font_size=8.2)
    doc.p(
        "The conclusion is that the project is economically feasible in the sense that matters for a "
        "student project, namely that no part of it is gated behind a payment. The comparison that "
        "justifies the design is rather different: a food-composition dataset with redistribution "
        "rights would have cost more than the entire development budget, and that single cost is the "
        "reason the scope was drawn at macronutrient grams rather than at food items."
    )
    doc.h3("3.5.3", "Operational Feasibility", key="s3.5.3")
    doc.p(
        "Operational feasibility was assessed by asking whether the intended user would sustain the "
        "interaction. Three design properties answer the question. The daily record requires twelve "
        "numbers and four clicks, which is comparable to the effort of reading a nutrition label. The "
        "plan is constructed once and edited only through a new plan, so no maintenance burden "
        "accumulates. And the feedback loop is immediate, which the behavioural literature identifies "
        "as the property that sustains monitoring."
    )
    doc.p(
        "The operational risks are of two kinds. The first is the requirement that the user know the "
        "macronutrient content of their meals. That is a real burden, and it is the principal "
        "operational weakness of the design; the narrative of Section 3.2 explains why the alternative "
        "was rejected, and Chapter 12 proposes a curated food table as the first substantive "
        "enhancement. The second is the configuration requirement: the service refuses to start "
        "without three environment variables, which is a deliberate safety decision that raises the "
        "cost of a first run. Appendix D therefore documents the start-up sequence explicitly."
    )
    doc.h3("3.5.4", "Schedule and Effort Feasibility", key="s3.5.4")
    doc.p(
        "The work was planned in five phases over twelve weeks: analysis and requirements, design, "
        "implementation of the identity and plan modules, implementation of the tracking and "
        "suggestion modules, and verification and documentation. The actual effort distribution "
        "differed from the plan in one instructive respect: documentation began in the fourth week "
        "rather than at the end. Writing the data dictionary while the tracking module was still being "
        "built exposed the duplicated target computation recorded in Section 7.3, which would "
        "otherwise have been carried into the delivered system unnoticed."
    )

    doc.h2("3.6", "Software Requirements Specification", key="s3.6")
    doc.p(
        "The requirements are stated in the two conventional groups. Twenty functional requirements "
        "define what the system must do, and ten non-functional requirements define the qualities it "
        "must have. Each requirement carries an identifier that is used in the verification matrix of "
        "Appendix B, so that the requirement, the artefact that implements it and the result of the "
        "verification are linked by a single key."
    )
    doc.table(
        "Functional requirements",
        ["ID", "Requirement", "Priority"],
        [
            ["FR-01", "The system shall allow a new user to register with a unique username, an "
                      "e-mail address and a password.", "High"],
            ["FR-02", "The system shall reject a registration whose username or e-mail address is "
                      "already in use.", "High"],
            ["FR-03", "The system shall authenticate a registered user and reject an incorrect "
                      "credential without disclosing which element was wrong.", "High"],
            ["FR-04", "The system shall issue a short-lived access token and a longer-lived refresh "
                      "token on successful authentication.", "High"],
            ["FR-05", "The system shall issue a new access token from a valid refresh token and shall "
                      "clear the refresh token on request.", "High"],
            ["FR-06", "The system shall estimate total daily energy expenditure from age, sex, height, "
                      "weight and activity level.", "High"],
            ["FR-07", "The system shall derive a daily calorie target by applying a selected deficit "
                      "or surplus and a deterministic rounding rule.", "High"],
            ["FR-08", "The system shall derive macronutrient gram targets from the calorie target "
                      "under a selectable preset or a custom split.", "High"],
            ["FR-09", "The system shall record diet type, meal type, meal count and snack preference "
                      "for a plan.", "Medium"],
            ["FR-10", "The system shall activate a plan and create the first daily tracking document "
                      "on activation.", "High"],
            ["FR-11", "The system shall persist the state of a plan under construction and shall "
                      "resume it, including backward navigation.", "High"],
            ["FR-12", "The system shall divide the daily macro allowance across breakfast, lunch, "
                      "snack and dinner and store the per-meal budgets.", "High"],
            ["FR-13", "The system shall accept per-meal macronutrient intake and recompute the daily "
                      "totals from all four meals.", "High"],
            ["FR-14", "The system shall convert logged macronutrients into energy consumed and compute "
                      "the proportion of the target achieved.", "High"],
            ["FR-15", "The system shall accept a new body weight and update the plan and the current "
                      "day together.", "Medium"],
            ["FR-16", "The system shall expose the current weight, the day count, the macro targets "
                      "and the weekly weight observations for the dashboard.", "High"],
            ["FR-17", "The system shall determine whether a plan has exceeded its configured duration "
                      "and shall mark it inactive when it has.", "Medium"],
            ["FR-18", "The system shall list all plans of the user and the daily records of any one "
                      "plan, most recent first.", "Medium"],
            ["FR-19", "The system shall present a stored daily record in read-only form.", "Medium"],
            ["FR-20", "The system shall, on request and subject to configuration, return meal "
                      "suggestions constrained by the calorie allowance of a selected meal.", "Low"],
        ],
        widths=[8, 76, 16], font_size=8.0)
    doc.table(
        "Non-functional requirements",
        ["ID", "Requirement", "Category"],
        [
            ["NFR-01", "Passwords shall be stored only as adaptive hashes and shall never appear in a "
                       "response.", "Security"],
            ["NFR-02", "Every plan and tracking operation shall be confined to the authenticated user "
                       "without relying on a client-supplied identifier.", "Security"],
            ["NFR-03", "Authentication shall be stateless, with no server-side session between "
                       "requests.", "Architecture"],
            ["NFR-04", "A first-time user shall be able to reach an activated plan without external "
                       "guidance.", "Usability"],
            ["NFR-05", "Every screen shall offer a recoverable action when there is no data to "
                       "display.", "Usability"],
            ["NFR-06", "A dashboard load shall complete within one second on the development machine.",
             "Performance"],
            ["NFR-07", "A missing daily document shall be created on demand rather than requiring a "
                       "scheduled job.", "Reliability"],
            ["NFR-08", "All energy and macronutrient arithmetic shall be implemented in a single "
                       "documented class.", "Maintainability"],
            ["NFR-09", "The repository shall build from a clean checkout with the tools it declares.",
             "Portability"],
            ["NFR-10", "The interface between tiers shall be documented to the field level.",
             "Maintainability"],
        ],
        widths=[9, 73, 18], font_size=8.0)
    doc.p(
        "Table 3.4 states the ten non-functional requirements in the same form. Two observations about the "
        "specification are worth recording because they explain asymmetries "
        "in the rest of the report. First, the requirements contain no administrative function at all; "
        "there is no requirement for a teacher, a clinician or an operator to see another user's data, "
        "which is why the security design in Section 4.8 can be as simple as it is. Second, only one "
        "requirement is marked Low priority, and it is the only one whose implementation depends on a "
        "third party. That correspondence is deliberate: the project was not willing to make a "
        "high-priority requirement contingent on an external service."
    )
    doc.p(
        "The exclusions are as important as the inclusions. The system does not measure physical "
        "activity; it asks the user to select a category. It does not validate the macronutrient "
        "content that the user types. It does not model micronutrients, allergies or medical "
        "conditions. It does not provide a food database. It does not support more than one concurrent "
        "active plan per user. And it does not provide an administrative interface, a password reset "
        "or an account deletion. Each exclusion is a candidate enhancement in Chapter 12."
    )

    # ================================================================== CHAPTER 4
    doc.chapter_heading(4, "System Design", key="ch4")
    doc.h2("4.1", "Design Overview and Principles", key="s4.1")
    doc.p(
        "The design is a three-tier web application with a layered back end. Figure 4.3 presents the "
        "deployment view of the profile in which the work was carried out, and Figure 4.9 the "
        "authentication flow on which every other interaction depends. Eight principles governed "
        "the decisions that follow, and each is stated with the artefact in which it is realised, so "
        "that the design chapter can be checked against the implementation chapter rather than being "
        "read as aspiration."
    )
    doc.numbered([
        "One implementation of each rule. Energy and macronutrient arithmetic exists only in "
        "NutrientsCalculator, a final class with a private constructor and eighteen static methods "
        "(Section 10.1).",
        "Ownership resolved from the context, never from the request. UserSession reads the principal "
        "from the security context and every service call uses it (Section 8.1).",
        "State where it can be resumed. The plan under construction lives on the server, so the client "
        "holds no draft and a reload loses nothing (Section 10.9).",
        "Aggregates embedded, subjects referenced. The four meal tracks are embedded in the daily "
        "document; the plan is referenced by identifier (Section 7.1).",
        "Recompute rather than accumulate. Daily totals are derived from the meal tracks on every "
        "update, which makes the update idempotent (Section 10.6).",
        "Progressive disclosure of arithmetic. Each wizard step shows the figure it computed before "
        "asking for the next input (Section 9.4).",
        "Generated content is a leaf. The language model is reachable only from one controller and "
        "cannot write to any collection (Section 6.4).",
        "Every state has a screen. Loading, empty, expired, error and unknown-route states all resolve "
        "to designed components (Section 9.9).",
    ])
    doc.figure("architecture-clean.png",
               "Three-tier architecture of the application with the packages that implement each tier",
               width=5.4)

    doc.h2("4.2", "System Architecture", key="s4.2")
    doc.p(
        "The presentation tier is a single-page client. It holds no persistent state other than the "
        "access token in memory, and it derives every displayed value either from a response or from a "
        "signal. Its four services mirror the four resource groups of the interface, and its two "
        "interceptors handle the two cross-cutting concerns that every request shares: prefixing the "
        "path and attaching the token."
    )
    doc.p(
        "The application tier is a Spring Boot service organised by feature. Each of the four features "
        "owns a controller, a service, a repository and its DTOs, and six sibling packages hold the "
        "cross-cutting code: configuration, exception handling, security, shared value objects, "
        "utilities and the shared model. The service layer is the only layer that contains domain "
        "logic, and the controllers are deliberately thin: each controller method resolves the "
        "principal where it is needed, delegates to one service method and returns the result."
    )
    doc.p(
        "The data tier is a single MongoDB database named macrova with four collections. There is no "
        "replica set, so multi-document transactions are unavailable, which the design tolerates "
        "because the only multi-document write is plan activation and the read path repairs a partial "
        "activation on the next load (Section 7.6)."
    )
    doc.figure("component-diagram.png",
               "Component diagram showing the client components, the service classes and the shared "
               "infrastructure", width=5.1)
    doc.figure("deployment-diagram.png",
               "Deployment view of the development profile, with the browser, the development server "
               "and the two back-end processes", width=5.1)

    doc.h2("4.3", "Data Flow Diagrams", key="s4.3")
    doc.p(
        "The data-flow models are presented at three levels. The context diagram fixes the system "
        "boundary and the two external entities. The level-one diagram decomposes the system into five "
        "processes and four data stores. The level-two diagram expands the tracking process, which is "
        "the one whose internal flow is not obvious from the level-one diagram because it both reads "
        "and writes the same store within a single request."
    )
    doc.h3("4.3.1", "Level 0 Data Flow Diagram (Context Diagram)", key="s4.3.1")
    doc.p(
        "The context diagram shows the system as a single process with two external entities. The user "
        "supplies credentials, body measurements, goal selections, meal preferences, macronutrient "
        "intake and weights, and receives plans, tracking documents, metrics and suggestions. The "
        "model provider receives a prompt and returns a JSON array of suggestions, and is the only "
        "entity with which the system initiates communication."
    )
    doc.figure("dfd-level-0.png",
               "Context diagram showing the two external entities and the flows across the system "
               "boundary", width=5.3)
    doc.h3("4.3.2", "Level 1 Data Flow Diagram (Functional Decomposition)", key="s4.3.2")
    doc.p(
        "The first decomposition identifies five processes: identity, plan construction, tracking, "
        "reporting and suggestion. It identifies four data stores, of which three are written in "
        "normal operation. The flows between the processes are mediated by the stores rather than "
        "direct: plan construction writes the plan store, tracking reads it and writes the tracking "
        "store, and reporting reads both."
    )
    doc.figure("dfd-level-1.png",
               "Level-one data flow diagram with the five processes and the four data stores",
               width=5.3)
    doc.h3("4.3.3", "Level 2 Data Flow Diagram (Macro Tracking Refinement)", key="s4.3.3")
    doc.p(
        "The refinement of the tracking process shows the three steps that a single update performs; the "
        "suggestion flow of Figure 4.10 follows the same contractual pattern one tier further out. "
        "The process first resolves the plan from the authenticated user and the active status, then "
        "resolves the current day, creating it if the calendar day has changed, and then writes the "
        "submitted macros into the selected meal track, recomputes the daily totals and returns the "
        "complete document. The refinement matters because it explains why the client can re-render an "
        "entire page from one response: the process returns the aggregate, not the delta."
    )
    doc.figure("calculation-flow-clean.png",
               "Refinement of the tracking process, showing the energy and macro conversions performed "
               "in one update", width=5.3)

    doc.h2("4.4", "Use Case Diagram and Actor Specification", key="s4.4")
    doc.p(
        "There is one actor, the dieter, who is either anonymous or authenticated. Two use cases are "
        "available to the anonymous actor, namely registration and authentication, and the remaining "
        "twelve require an authenticated session. Table 4.1 specifies the first seven in the form "
        "normally used for a use-case specification, with the preconditions, the main flow, the "
        "alternate flow and the postcondition; Table 4.2 specifies the remaining seven more briefly, "
        "because their flows are short."
    )
    doc.table(
        "Use-case specification UC-01 to UC-07",
        ["ID", "Use case", "Actor", "Precondition and main flow", "Alternate and postcondition"],
        [
            ["UC-01", "Register", "Anonymous",
             "None. The actor supplies a username, an e-mail address and a password; the system checks "
             "uniqueness, hashes the password, stores the user and returns the DTO.",
             "A duplicate produces a 400 with a message; the account exists but is not signed in."],
            ["UC-02", "Sign in", "Anonymous",
             "A registered account. The actor supplies credentials; the filter verifies them through "
             "the authentication manager, sets the refresh cookie and returns an empty 200.",
             "A wrong credential yields a uniform 401; the session is not established."],
            ["UC-03", "Refresh the access token", "Anonymous with a cookie",
             "A valid refresh cookie. The system validates the token and returns a new access token.",
             "An absent or invalid cookie yields a 401; the client clears its state."],
            ["UC-04", "Construct a plan", "Authenticated",
             "No pending plan. The actor completes four steps in order; each step persists and "
             "advances the status; the fourth activates the plan.",
             "A step submitted with no pending plan yields a 400; the draft remains at the last "
             "committed step."],
            ["UC-05", "Resume a plan draft", "Authenticated",
             "A pending plan exists. The client requests the status; the system returns the status "
             "and the payload of the current step.",
             "If no draft exists the wizard renders the first step; the draft is unchanged."],
            ["UC-06", "Navigate backward in the wizard", "Authenticated",
             "A pending plan at a later step. The client posts the target status; the system returns "
             "the reconstructed payload of that step.",
             "A status ahead of the stored one is not served; the stored status is preserved."],
            ["UC-07", "Log a meal", "Authenticated",
             "An active plan. The actor submits three gram values for a category; the system writes "
             "the meal track, recomputes the totals and returns the document.",
             "An invalid category yields a 400; the document is unchanged."],
        ],
        widths=[7, 17, 11, 38, 27], font_size=7.9)
    doc.table(
        "Use-case specification UC-08 to UC-14",
        ["ID", "Use case", "Precondition", "Outcome"],
        [
            ["UC-08", "Update body weight", "An active plan and a current-day document",
             "The plan's current weight and the day's weight are both updated"],
            ["UC-09", "View the dashboard", "An authenticated session",
             "The metrics are returned or the actor is routed to the empty state on a 404"],
            ["UC-10", "View the tracking screen", "An active plan",
             "The plan and today's document are returned; the document is created if absent"],
            ["UC-11", "Browse plan history", "At least one plan",
             "A projection of all plans, most recent first"],
            ["UC-12", "Browse the days of a plan", "A plan identifier owned by the actor",
             "A projection of the plan's daily documents, most recent first"],
            ["UC-13", "Review a stored day", "An authenticated session",
             "The complete stored document, rendered read-only"],
            ["UC-14", "Request meal suggestions", "An authenticated session",
             "A list of suggestions, or an error routed to the error page"],
        ],
        widths=[8, 28, 30, 34], font_size=8.2)

    doc.h2("4.5", "Object-Oriented and Behavioural Models", key="s4.5")
    doc.h3("4.5.1", "Class Diagram", key="s4.5.1")
    doc.p(
        "The class model is organised around four aggregates. The user aggregate is a single entity. "
        "The plan aggregate is a plan entity with three embedded value objects and eight enumerated "
        "attributes. The tracking aggregate is a tracking entity with four value objects and six "
        "calorie objects nested two levels deep. The suggestion aggregate is a simple entity that is "
        "declared but not written. The shared package holds the value objects that cross aggregate "
        "boundaries, of which the macro and calorie pairs are the most used."
    )
    doc.figure("class-diagram.png",
               "Class diagram of the entities, the embedded value objects and the enumerations",
               width=5.0)
    doc.h3("4.5.2", "Sequence Diagram", key="s4.5.2")
    doc.p(
        "The sequence diagram of plan construction shows the interaction across four steps. Each "
        "request is authenticated by the filter chain before it reaches the controller, the controller "
        "delegates to the form service, the service resolves the user, loads the pending plan, "
        "mutates it and saves it, and the response carries the payload that the next step requires. "
        "The diagram makes visible the two properties that the design depends on: the plan is saved on "
        "every step, and the user identifier enters the flow from the security context rather than "
        "from the request body."
    )
    doc.figure("sequence-plan.png",
               "Sequence diagram of the four-step plan construction flow", width=5.2)
    doc.figure("auth-flow-clean.png",
               "Sequence of the authentication, token refresh and guarded request flows",
               width=5.3)
    doc.figure("ai-sequence-clean.png",
               "Sequence of the suggestion flow, from the client request to the rendered cards",
               width=5.3)
    doc.h3("4.5.3", "Activity Diagram", key="s4.5.3")
    doc.p(
        "The activity diagram of the tracking loop shows the decision that governs the whole "
        "interaction. On entering the tracking screen the client asks whether the plan has exceeded "
        "its duration; if it has, the flow branches to the empty state. Otherwise the plan is loaded, "
        "today's document is requested, and the user may iterate between logging a meal and updating "
        "the weight until they leave the screen. Every iteration returns to the same state, which is "
        "why the screen can be left and resumed without a save action."
    )
    doc.figure("activity-wizard.png",
               "Activity diagram of the wizard, showing the four forward steps, the backward "
               "transitions and the reservation of the draft", width=5.0)
    doc.h3("4.5.4", "State Machine Diagram", key="s4.5.4")
    doc.p(
        "Two state machines are defined. The form status machine governs the wizard and has five "
        "states: body metrics, goal selection, meal preference, preview and completed. Transitions are "
        "forward only through the creation endpoints and backward through the status endpoint, and "
        "every step writes the new state, so the machine's state is never held only in the client."
    )
    doc.p(
        "The plan status machine governs the lifecycle and has three states. A plan is created "
        "pending, becomes active when the wizard completes, and becomes inactive when the elapsed day "
        "count exceeds the configured duration. The transition to inactive is evaluated when the "
        "client asks, not by a scheduler, which has two consequences that the report records: a plan "
        "with no visits is never marked inactive, and the transition happens as part of a read "
        "request, so a GET endpoint has a side effect. Both consequences follow from the decision to "
        "avoid a scheduler in a single-instance deployment."
    )
    doc.figure("state-diagram.png",
               "State machine of the form status and the plan status, with the triggers of each "
               "transition", width=5.0)

    doc.h2("4.6", "Database Design", key="s4.6")
    doc.p(
        "The data model is document-oriented and aggregate-first. Four collections are declared, of "
        "which three are written in normal operation. The document boundaries were drawn by asking "
        "which values are always read together, and the answer is recorded in Chapter 7 together with "
        "the data dictionary and a worked example of a stored document. This section states only the "
        "shape of the model and the reasoning that produced it."
    )
    doc.p(
        "A user document owns everything. A plan document embeds its own targets, macros and "
        "preferences, and refers to its owner by identifier. A tracking document embeds the day's "
        "totals, the four meal tracks and the day's energy figures, and refers to its plan by "
        "identifier. The reference direction is deliberate: a plan is a subject in its own right, "
        "because the history screens list plans without touching their days, whereas a day is "
        "meaningless without its plan and is therefore embedded in nothing but itself."
    )
    doc.figure("domain-model-clean.png",
               "Domain model showing the four aggregates, their value objects and the reference "
               "between a day and its plan", width=5.3)

    doc.h2("4.7", "User Interface Design System", key="s4.7")
    doc.p(
        "The interface uses a small design system rather than a component library. Six primitives "
        "cover every screen: the card, the pill selector, the numeric field, the primary button, the "
        "metric card and the step indicator. The choice of a hand-built system over a library follows "
        "from the scope: twenty components and fifteen screens do not justify the weight of a full "
        "library, and a small system makes the visual language of Section 9.10 exactly as consistent "
        "as the report claims."
    )
    doc.table(
        "Design-system primitives and their use across the screens",
        ["Primitive", "Purpose", "Appears on"],
        [
            ["Card", "The single surface for grouped content; eight-pixel radius, one-pixel border, "
                     "white fill on a tinted canvas", "All eleven form and content screens"],
            ["Pill selector", "A single choice from two to five options, rendered as a row of rounded "
                              "buttons", "Wizard steps 1, 2, 3 and 4; suggestion filters"],
            ["Numeric field", "A labelled input with the required range stated in the label",
             "Wizard step 1; tracking summary; meal cards"],
            ["Primary button", "The one concluding action of a screen, full width where it completes a "
                               "form, in the brand colour", "Every screen except the dashboard and the "
                                                         "history drill-downs"],
            ["Metric card", "An uppercase label with a value and an inline unit",
             "Dashboard; tracking summary"],
            ["Step indicator", "Four numbered circles joined by rules, filled for completed steps",
             "All four wizard steps"],
        ],
        widths=[16, 44, 40], font_size=8.2)

    doc.h2("4.8", "Security Design", key="s4.8")
    doc.p(
        "The security design has four elements: how a password is stored, how a session is "
        "represented, how a request is authenticated and how data is confined to its owner. Table 4.3 "
        "summarises the decisions and, for each one, the weakness that remains after it."
    )
    doc.table(
        "Security decisions and their residual weaknesses",
        ["Concern", "Decision", "Residual weakness"],
        [
            ["Password storage", "BCrypt with a per-password salt, compared through the encoder",
             "No policy beyond an eight-character minimum enforced in the client"],
            ["Credential verification",
             "A custom authentication manager that translates an unknown username into a "
             "bad-credentials failure, so the response cannot enumerate accounts",
             "No throttling or lockout on repeated failure"],
            ["Access token", "HMAC-512 signed, short-lived, held in memory by the client and sent in "
                             "the authorisation header",
             "Cannot be revoked before expiry; the client's copy is readable by any script on the "
             "page"],
            ["Refresh token", "HMAC-512 signed, longer-lived, delivered as an HttpOnly, SameSite Lax "
                              "cookie and never read by client script",
             "Not rotated and not revocable; the secure attribute is absent in the development "
             "profile"],
            ["Sign-out", "The refresh cookie is overwritten with an empty value and a zero maximum "
                         "age", "The access token in memory remains valid until it expires"],
            ["Request authentication", "A filter verifies the bearer token and populates the security "
                                       "context; an exception filter translates verification failures "
                                       "into 401 responses",
             "A failure in the filter chain returns plain text rather than the JSON error shape"],
            ["Data confinement", "Every service resolves the user from the security context and builds "
                                 "the query from it",
             "The rule is applied by convention in each method rather than by a central check"],
            ["Cross-origin access", "An explicit allow-list with credentials permitted",
             "Pinned to the development origin"],
            ["Route protection", "A functional guard on eleven of the thirteen routes",
             "Two history routes are unguarded; the subsequent request still fails with 401"],
        ],
        widths=[16, 46, 38], font_size=8.0)
    doc.p(
        "The design maintains a single invariant that is worth isolating, because it is the property "
        "on which the whole security argument rests: <i>no controller accepts a user identifier from "
        "the client</i>. The identifier is obtained from the security context inside the service and "
        "used to build every query. Table 4.4 lists the queries that enforce the invariant; a reviewer "
        "can verify each one against the source, and Appendix B records the result of doing so."
    )
    doc.table(
        "Queries that enforce ownership, with the identifier each uses",
        ["Service method", "Query", "Identifier source"],
        [
            ["findDietPlanByUserId", "owner and status", "Security context"],
            ["getPendingDietPlan", "owner and pending status", "Security context"],
            ["findAllByUserId", "owner, projected", "Security context"],
            ["findPastDietPlan", "owner, most recent, projected", "Security context"],
            ["findDietPlanTrackByDietPlanId", "plan identifier resolved from a plan already scoped to "
                                              "the owner", "Plan resolved from the context"],
            ["findByDateRangeAndDietPlanId", "plan identifier and date range", "Plan resolved from the "
                                                                             "context"],
            ["getUsername", "identifier of the authenticated principal", "Security context"],
        ],
        widths=[26, 46, 28], font_size=8.2)
    return doc
