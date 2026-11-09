"""Preliminary-page prose and data, shared by the PDF and DOCX renderers."""

TITLE_LINES = [
    "MACROVA: A WEB-BASED DIET AND MACRONUTRIENT",
    "TRACKING APPLICATION WITH RULE-BASED ENERGY",
    "ESTIMATION AND AI-ASSISTED MEAL SUGGESTIONS",
]
TITLE_ONE_LINE = " ".join(TITLE_LINES)

STUDENT = "KARTHICK S"
REGNUM = "DC2431006010XXX"
GUIDE = "Dr. A. Thirumurthi Raja M.C.A., M.E., Ph.D.,"
MONTH = "NOVEMBER 2026"

CERTIFICATE = [
    "This is to certify that the project report titled \u201c" + TITLE_ONE_LINE +
    "\u201d is a bonafide record of the independent project work carried out by " + STUDENT +
    " (Register Number " + REGNUM + ") in the Department of Computer Applications, Directorate of "
    "Distance Education, SRM Institute of Science and Technology, in partial fulfillment of the "
    "requirements for the award of the degree of Bachelor of Computer Applications, under my "
    "guidance and supervision.",
    "The work described in this report has been verified against the accompanying software "
    "repository. Chapters 5 to 10 of the report describe the modules, the data model and the "
    "algorithms exactly as they are implemented in that repository, and Chapter 11 distinguishes "
    "the behaviour that was verified from the behaviour that is only inferred from the source.",
    "To the best of my knowledge, the work reported herein is original, and it has not been "
    "submitted earlier, either in part or in full, for the award of any other degree or diploma of "
    "this or any other institution.",
]

DECLARATION = [
    "I, " + STUDENT + " (Register Number " + REGNUM + "), hereby declare that the project report "
    "entitled \u201c" + TITLE_ONE_LINE + "\u201d submitted to SRM Institute of Science and "
    "Technology in partial fulfillment of the requirements for the award of the degree of Bachelor "
    "of Computer Applications is a record of original software engineering work carried out by me "
    "under the supervision and guidance of Dr. A. Thirumurthi Raja, M.C.A., M.E., Ph.D., Assistant "
    "Professor and Programme Coordinator, Department of Computer Applications, Directorate of "
    "Distance Education.",
    "I further declare that the source code submitted with this report is my own work, that the "
    "screens reproduced in Chapter 9 are captures of that code running on my own machine, and that "
    "the figures and tables were prepared by me specifically for this report. This project report, "
    "or any part thereof, has not been submitted earlier to any other university or institution for "
    "the award of any degree, diploma or fellowship.",
]

ACKNOWLEDGEMENT = [
    "I am grateful to Dr. T. R. Paarivendhar, Chancellor, SRM Institute of Science and Technology, "
    "and to the Director of the Directorate of Distance Education, for the institutional support "
    "that made this project possible.",
    "I record my sincere thanks to my guide, Dr. A. Thirumurthi Raja, Assistant Professor and "
    "Programme Coordinator, for his sustained attention to this work. His insistence that a claim "
    "in a report must be traceable to a line of code is the single instruction that shaped the "
    "verification chapter of this document more than any other.",
    "I thank the faculty members of the Department of Computer Applications who reviewed the "
    "project at successive stages and whose comments changed the design of the tracking module in "
    "particular.",
    "I acknowledge the maintainers of the open-source projects on which Macrova is built, in "
    "particular the Spring and Angular communities, whose documentation made the security and "
    "reactivity design of this application tractable for an undergraduate project.",
    "Finally, I thank my parents and my friends for their patience and encouragement throughout the "
    "period of this work.",
]

ABSTRACT = [
    "Dietary adherence, rather than the selection of a particular diet, is the variable that "
    "determines the outcome of most weight-management programmes, and adherence in turn depends on "
    "feedback that the user can understand and trust. The tools available to an individual dieter "
    "usually sit at one of two extremes: a spreadsheet in which every figure must be recalculated "
    "by hand, or a commercial application that prescribes a plan without exposing the arithmetic "
    "that produced it. Macrova is a web application that occupies the space between the two. Every "
    "kilocalorie and every gram of macronutrient shown to the user is produced by a documented rule "
    "and is stored against the plan that generated it, so that the numbers can be audited after the "
    "fact.",
    "The system is implemented as a three-tier application. The presentation tier is a single-page "
    "client written in Angular 19 with standalone components, signals and functional HTTP "
    "interceptors. The application tier is a Spring Boot 3.4.4 service on Java 21 organised into "
    "packages for identity, diet planning, food suggestion, shared value objects, exception handling "
    "and stateless token security. The data tier is MongoDB, reached through Spring Data MongoDB, "
    "with one collection per aggregate: users, diet_plans and diet_plan_tracks, together with a "
    "fourth collection for suggestions that the delivered build does not write to. The tiers "
    "communicate only through a JSON interface whose twenty-six endpoints are enumerated and "
    "cross-checked against the controller classes in this report.",
    "Energy requirements are computed with the Mifflin\u2013St Jeor basal metabolic rate equation and "
    "multiplied by one of five activity factors to obtain total daily energy expenditure. Weight-loss "
    "targets apply a deficit of fifteen, twenty or twenty-five per cent, weight-gain targets apply a "
    "surplus of the same nominal intensity moderated by ten percentage points, and both results are "
    "rounded to a value ending in fifty or one hundred. Four macronutrient presets translate the "
    "energy target into gram targets, and a fixed split of thirty, thirty, fifteen and twenty-five "
    "per cent across breakfast, lunch, snack and dinner produces the per-meal budget against which "
    "the user logs intake.",
    "A four-step wizard persists each step, so that the construction of a plan is resumable and "
    "backward navigation can be served from the stored document rather than from a client-side "
    "draft. Activating a plan creates the first day's tracking document, which is then updated "
    "whenever the user records intake or a new body weight. Logged macronutrients are converted back "
    "into energy with the Atwater factors, the percentage of the daily target achieved is recomputed "
    "on every update, and the weekly weight observations are rendered as a trend chart. History "
    "screens expose every past plan and its day-by-day records through projections that avoid "
    "loading the embedded meal tracks.",
    "An optional feature integrates a large language model through a chat-completions endpoint. The "
    "prompt is assembled from four filters and from the calorie allowance that the plan computes for "
    "the selected meal, and the JSON reply is parsed into suggestion cards. The report is explicit "
    "about the limits of that path: the nutritional values are generated and are not validated "
    "against a food-composition database, the parse depends on the model honouring an instructed "
    "schema, and the persistence method that would cache suggestions exists but is never invoked.",
    "Security is implemented with stateless JSON Web Tokens: BCrypt password hashing, a custom "
    "authentication manager, a sign-in filter that issues an HMAC-512 signed refresh token as an "
    "HttpOnly cookie, a bearer verification filter and an exception-translating filter. Every plan "
    "and tracking operation is scoped to the authenticated principal inside the service layer, so "
    "guessing an identifier does not expose another user's data. The report also records the "
    "concrete weaknesses of the present configuration, among them the absence of refresh-token "
    "rotation and revocation, a cross-origin allow-list pinned to the development origin and "
    "input ranges that are enforced in the browser only.",
    "The delivered system comprises 71 Java source files (2,779 lines), 60 TypeScript files (1,915 "
    "lines), 20 component templates (1,238 lines) and 19 stylesheets (2,381 lines), together with "
    "the twenty-six endpoints, three collections written in normal operation and a shared model of "
    "value objects and enumerations. The report closes with a verification chapter that maps every "
    "documented behaviour to the artefact that implements it, a summary of the limitations that "
    "remain, and an ordered list of enhancements that the present architecture can accommodate.",
]

KEYWORDS = ("macronutrient tracking, Mifflin\u2013St Jeor equation, total daily energy expenditure, "
            "Angular 19 standalone components, Spring Boot 3.4.4, Spring Security, JSON Web Token, "
            "MongoDB, Spring Data, Chart.js, large language model, diet plan wizard, software "
            "verification.")

ABBREV = [
    ("API", "Application Programming Interface"),
    ("BCrypt", "Blowfish-based adaptive password-hashing function"),
    ("BMR", "Basal Metabolic Rate"),
    ("BMI", "Body Mass Index"),
    ("CORS", "Cross-Origin Resource Sharing"),
    ("CSS", "Cascading Style Sheets"),
    ("DFD", "Data Flow Diagram"),
    ("DTO", "Data Transfer Object"),
    ("ER", "Entity\u2013Relationship"),
    ("FR", "Functional Requirement"),
    ("HMAC", "Hash-based Message Authentication Code"),
    ("HTML", "Hypertext Markup Language"),
    ("HTTP", "Hypertext Transfer Protocol"),
    ("JSON", "JavaScript Object Notation"),
    ("JVM", "Java Virtual Machine"),
    ("JWT", "JSON Web Token"),
    ("LLM", "Large Language Model"),
    ("MVC", "Model\u2013View\u2013Controller"),
    ("NFR", "Non-Functional Requirement"),
    ("REST", "Representational State Transfer"),
    ("SPA", "Single-Page Application"),
    ("SRS", "Software Requirements Specification"),
    ("TDEE", "Total Daily Energy Expenditure"),
    ("UML", "Unified Modeling Language"),
    ("URI", "Uniform Resource Identifier"),
    ("XSS", "Cross-Site Scripting"),
]

SIGN_GUIDE = "Dr. A. Thirumurthi Raja\nAssistant Professor,\nSRMIST-DDE"
SIGN_HOD = ("Dr. A. Thirumurthi Raja\nProgramme Coordinator,\nDepartment of Computer Applications,\n"
            "Directorate of Distance Education (DDE),\nSRMIST")
