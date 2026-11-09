"""Chapters 5 to 8: technologies, modules, data dictionary, interface and client services."""


def build(doc):
    # ================================================================== CHAPTER 5
    doc.chapter_heading(5, "Technologies and Tools Used", key="ch5")
    doc.h2("5.1", "Software Requirements", key="s5.1")
    doc.p(
        "The software environment required to build and run Macrova is listed in Table 5.1. Every "
        "version is taken from the build manifests in the repository, from pom.xml for the service and "
        "from package.json for the client, rather than from the author's machine, so the table "
        "describes the project rather than one particular development environment."
    )
    doc.table(
        "Software requirements of the Macrova application",
        ["Category", "Software", "Version", "Role in the project"],
        [
            ["Language (service)", "Java, JDK", "21", "Backend source and runtime; the Maven compiler "
                                                     "is configured for release 21"],
            ["Language (client)", "TypeScript", "5.7", "All Angular source, with strict template type "
                                                       "checking"],
            ["Markup and style", "HTML5, CSS3", "\u2014", "Twenty component templates, nineteen "
                                                         "component stylesheets and one global "
                                                         "stylesheet"],
            ["Framework (service)", "Spring Boot", "3.4.4", "Auto-configuration, embedded container, "
                                                            "dependency management"],
            ["Web layer", "Spring Web MVC", "6.x, managed", "REST controllers and Jackson message "
                                                            "conversion"],
            ["Security", "Spring Security", "6.x, managed", "Password encoding, filter chain, "
                                                            "cross-origin policy, security context"],
            ["Token library", "Auth0 java-jwt", "4.5.0", "HMAC-512 signing and verification of both "
                                                         "token types"],
            ["Persistence", "Spring Data MongoDB", "4.x, managed", "Repository derivation, projections "
                                                                   "and type converters"],
            ["Object mapping", "ModelMapper", "3.2.2", "Entity-to-DTO conversion in the shared mapper"],
            ["Boilerplate", "Lombok", "1.18.38", "Accessors, builders and constructors on entities, "
                                                 "DTOs and value objects"],
            ["Database", "MongoDB Community Edition", "6 or later", "Document store holding four "
                                                                     "collections"],
            ["Framework (client)", "Angular", "19.2", "Standalone components, signals, functional "
                                                      "interceptors and route guards"],
            ["Reactivity", "RxJS", "7.8", "HTTP observables and operator composition"],
            ["Change detection", "zone.js", "0.15", "Zone-based detection with event coalescing"],
            ["Charting", "Chart.js", "4.4.9", "Weight trend line chart on the dashboard"],
            ["Token inspection", "jwt-decode", "4.0.0", "Reading the expiry claim in the client"],
            ["Build (service)", "Apache Maven through the wrapper", "3.9 wrapper",
             "mvnw and mvnw.cmd are committed, so no global Maven installation is needed"],
            ["Build (client)", "Angular CLI with esbuild", "19.2", "ng serve, ng build and the "
                                                                   "development proxy"],
            ["Testing", "JUnit 5 via spring-boot-starter-test", "5.x, managed",
             "One context-load test in the delivered repository"],
            ["Documentation", "ReportLab, python-docx, PyMuPDF, Matplotlib", "current releases",
             "This report, its diagrams and the screenshot preparation"],
            ["Version control", "Git", "\u2014", "One repository holding the service, the client and "
                                                "the documentation"],
        ],
        widths=[16, 24, 14, 46], font_size=8.0)

    doc.h2("5.2", "Hardware Requirements", key="s5.2")
    doc.p(
        "Macrova is a light application by contemporary standards: the service comprises 71 classes and "
        "the client bundle sits well inside the default Angular budget of one megabyte. The figures in "
        "Table 5.2 describe the machine on which the project was built and the practical minimum for a "
        "demonstration to a reviewer."
    )
    doc.table(
        "Hardware requirements",
        ["Component", "Minimum for development", "Recommended", "Notes"],
        [
            ["Processor", "Dual-core x86-64, 1.6 GHz", "Quad-core, 2.4 GHz or faster",
             "The Maven build and the Angular development server are the heaviest workloads"],
            ["Memory", "4 GB", "8 GB or more",
             "A JVM, a Node.js process and the database daemon run concurrently"],
            ["Free disk", "1.5 GB", "3 GB",
             "The Maven and npm dependency caches dominate; the application data is measured in "
             "kilobytes"],
            ["Display", "1280 \u00d7 720", "1920 \u00d7 1080",
             "The screenshots of Chapter 9 were captured in a window of 1921 \u00d7 978 pixels"],
            ["Network", "Not required", "Broadband",
             "Required for the first build and for the optional suggestion feature"],
            ["Server, if deployed", "1 vCPU, 1 GB RAM", "2 vCPU, 2 GB RAM",
             "Sufficient for a small group, with the database co-located"],
        ],
        widths=[16, 24, 22, 38], font_size=8.2)
    doc.p(
        "Storage deserves a specific comment because the persistence model determines it. A plan "
        "document with all of its embedded value objects occupies roughly seven hundred bytes of BSON, "
        "and a tracking document with four meal tracks roughly six hundred. A user who tracks daily "
        "for a year therefore consumes under a quarter of a megabyte. The dominant storage cost in the "
        "repository is not data at all but the Maven and npm caches, which is why the free-disk column "
        "of the table is an order of magnitude larger than the data it protects."
    )

    doc.h2("5.3", "Programming Languages Used", key="s5.3")
    doc.h3("5.3.1", "Java 21 for the Application Tier", key="s5.3.1")
    doc.p(
        "The service is written in Java 21, the version declared by the java.version property of "
        "pom.xml and passed to the compiler through the release flag. Three language features explain "
        "the shape of several classes. Switch expressions with arrow labels select the macronutrient "
        "preset and the meal track, and validate a meal category in the constants class. The var "
        "keyword appears where a long generic type would obscure a short method body. And the "
        "functional style of the service layer shows in the use of Optional: every repository finder "
        "returns one, and it is consumed with ifPresent, orElseGet, map and isEmpty rather than with "
        "get, except in the two places where an explicit emptiness check throws the domain exception."
    )
    doc.p(
        "Two features are deliberately absent. Records are not used, because the DTOs are the targets "
        "of both ModelMapper and Jackson and those libraries are simpler to configure against beans "
        "with Lombok accessors. Text blocks are not used either, because the longest string constants "
        "in the codebase are prompt templates of two or three lines rather than documents. The code "
        "therefore reads as conservative Java with a modern switch, which is a fair description of the "
        "style the project adopted."
    )
    doc.h3("5.3.2", "TypeScript 5.7 for the Presentation Tier", key="s5.3.2")
    doc.p(
        "The client is written in TypeScript with the strictness settings generated by the Angular CLI. "
        "Three idioms recur. Types are imported with a type-only import where they are erased at "
        "compile time, which keeps the emitted JavaScript free of unused module references. Component "
        "contracts are declared with the signal-based input and output functions rather than with "
        "decorators: each wizard step declares a required input whose type parameter names the payload "
        "it renders and emits a typed output when it is submitted, so a mismatch between a step and "
        "its host is a compile error. And state is held according to its scope, in a component field "
        "for local state, in a signal on a singleton service for shared state, and on the server for "
        "state that must survive navigation."
    )
    doc.p(
        "The last of those three is the decision that matters architecturally. The wizard keeps no "
        "draft in the browser: the pending plan lives in the database, and the client re-renders "
        "whichever step the server reports as current. That is why a reload at the third step returns "
        "the user to the third step rather than to the first, and why the host component has no "
        "reconstruction logic at all."
    )
    doc.h3("5.3.3", "HTML5, CSS3 and JSON", key="s5.3.3")
    doc.p(
        "The templates use the built-in control-flow blocks of modern Angular rather than the "
        "structural directives of the previous generation, which is the current idiom and removes the "
        "need to import a directives module in every component. CSS is organised per component with "
        "the default emulated encapsulation, so a rule declared in one component cannot leak into "
        "another; the global stylesheet holds only the design tokens, the reset, the type scale and the "
        "few utility classes that are genuinely shared. JSON is the only wire format, both between the "
        "browser and the service and between the service and the model provider, which is why a single "
        "serialisation stack covers both directions."
    )

    doc.h2("5.4", "Frameworks and Libraries", key="s5.4")
    doc.p(
        "Table 5.3 records why each dependency is present. The criterion applied during the review was "
        "that a dependency must be used by at least one class or component, so the table doubles as a "
        "justification of the two manifests."
    )
    doc.table(
        "Frameworks and libraries with their justification",
        ["Dependency", "Tier", "Used by", "Justification"],
        [
            ["spring-boot-starter-web", "Service", "Four controllers",
             "Servlet container, MVC dispatch and Jackson message conversion"],
            ["spring-boot-starter-security", "Service", "Security configuration, three filters, the "
                                                        "authentication manager",
             "Filter chain, BCrypt encoder and security context"],
            ["spring-boot-starter-data-mongodb", "Service", "Four repositories, database configuration",
             "Repository derivation, projections and custom date converters"],
            ["java-jwt 4.5.0", "Service", "Token service",
             "HMAC-512 signing and verification"],
            ["modelmapper 3.2.2", "Service", "Shared mapper, user service",
             "Declarative entity-to-DTO mapping"],
            ["lombok 1.18.38", "Service", "All entities, DTOs and models",
             "Accessors, builders and constructors without boilerplate"],
            ["@angular/core and @angular/common", "Client", "All twenty components",
             "Component model, control flow, pipes and built-in directives"],
            ["@angular/router", "Client", "Route table, guard, header links",
             "Routes, guards and navigation events"],
            ["@angular/forms", "Client", "Login, signup, four wizard steps, weight input",
             "Two-way binding through ngModel"],
            ["@angular/common/http", "Client", "Four services and two interceptors",
             "Typed HTTP client and the interceptor chain"],
            ["rxjs", "Client", "Guard, interceptors, services",
             "Observable composition with switchMap, map, tap and catchError"],
            ["chart.js", "Client", "Weight trend component",
             "Canvas line chart of the week's weights"],
            ["jwt-decode", "Client", "Token service",
             "Client-side inspection of the expiry claim"],
            ["zone.js", "Client", "Bootstrap",
             "Change detection, as configured by the CLI"],
        ],
        widths=[26, 8, 30, 36], font_size=8.0)

    doc.h2("5.5", "Development and Runtime Environment", key="s5.5")
    doc.p(
        "The repository is a single Git working tree with three top-level directories. The backend "
        "directory holds the Maven project and a committed Maven wrapper. The frontend directory holds "
        "the Angular workspace. The docs directory holds the diagrams, the screenshots, the reference "
        "documents and this report. The service is started with the wrapper script and the client with "
        "the npm start script, which invokes the Angular development server with the proxy "
        "configuration. The database runs independently, and the service connects to it with the "
        "driver default of the local host and port, with the database name fixed to macrova by a "
        "configuration class."
    )
    doc.p(
        "Three properties are supplied through the environment rather than committed: the secret used "
        "to sign and verify tokens, the key used as the bearer credential for the model provider, and "
        "the identifier of the model to request. None of the three has a default value, and the "
        "placeholders are resolved at start-up, so the service refuses to start when they are absent. "
        "That is a deliberate safety decision that costs convenience during a demonstration, and "
        "Section 3.5.3 records the cost."
    )
    doc.p(
        "The development proxy is what makes the two-process arrangement transparent to the browser. "
        "The proxy configuration maps the /api prefix to the service port, enables origin rewriting "
        "and removes the prefix, so a client request to /api/diet-plan/metrics reaches the service as "
        "/diet-plan/metrics. Because the browser sees only the development-server origin, the "
        "cross-origin allow-list of the service is never exercised during development and would matter "
        "only if the client were served from a different origin, which the delivered build does not "
        "do."
    )

    doc.h2("5.6", "Build and Run Workflow", key="s5.6")
    doc.p(
        "The development workflow consists of five commands, and Table 5.4 records them with the reason "
        "each one exists. The table is included because the repository is handed over as a working tree "
        "rather than as a deployed artefact, and a reviewer who attempts to run it will need exactly "
        "this information."
    )
    doc.table(
        "Build and run commands of the delivered system",
        ["Step", "Command", "Directory", "What it does"],
        [
            ["1", "mongod --dbpath &lt;path&gt;", "any",
             "Starts the database on its default port; the service creates the macrova database on "
             "first use"],
            ["2", "export JWT_SECRET, OPENROUTER_API_KEY, OPENROUTER_MODEL", "any",
             "Supplies the three properties the service resolves at start-up"],
            ["3", "./mvnw spring-boot:run", "backend",
             "Compiles the 71 classes and starts the embedded container on port 8080"],
            ["4", "npm start", "frontend",
             "Starts the Angular development server with the proxy configuration"],
            ["5", "npm run build", "frontend",
             "Produces the production bundle in the dist directory, for a static deployment"],
        ],
        widths=[7, 33, 14, 46], font_size=8.2)
    doc.p(
        "Two properties of the workflow are worth noting. The Maven wrapper is committed, so the first "
        "command downloads the declared Maven version rather than requiring a global installation, "
        "which is what makes the repository reproducible on a machine that has only a JDK. And the "
        "proxy configuration is read by the development server rather than by the browser, so a change "
        "to the service port requires editing one JSON file and restarting the client, not rebuilding "
        "it."
    )

    # ================================================================== CHAPTER 6
    doc.chapter_heading(6, "Modules and Implementation Overview", key="ch6")
    doc.p(
        "The implementation is organised into eight modules. The first five are service concerns and "
        "the last three are client concerns. For each module this chapter states its responsibility, "
        "enumerates its artefacts and explains the behaviour it implements; Chapter 10 then examines "
        "the arithmetic in depth and Chapter 8 the interface through which the modules communicate."
    )
    doc.table(
        "Module map of the Macrova implementation",
        ["Module", "Tier", "Principal artefacts", "Primary responsibility"],
        [
            ["M1 Identity and session", "Service",
             "User controller and service, user repository and entity, token service, custom "
             "authentication manager, three filters, security configuration, session component",
             "Registration, credential verification, token issuance and request authentication"],
            ["M2 Plan construction", "Service",
             "Form controller and service, eight form DTOs, plan entity, plan repository",
             "Four-step wizard, energy estimation, target derivation and activation"],
            ["M3 Daily tracking", "Service",
             "Plan controller and service, tracking entity and repository, metrics and overview DTOs",
             "Per-meal logging, weight updates, daily aggregation and weekly metrics"],
            ["M4 AI suggestions", "Service",
             "Suggestion controller and service, filter DTO, suggestion entity, provider adapter and "
             "its interface, chat model",
             "Prompt construction, provider call, reply parsing and card rendering"],
            ["M5 Cross-cutting", "Service",
             "Exception advice and three exception types, error response, mapper, two configuration "
             "classes, calculator, constants, nine value objects and eight enumerations",
             "Error translation, bean configuration, conversions, arithmetic and shared types"],
            ["M6 Shell and routing", "Client",
             "Root component, route table, bootstrap configuration, header, toast, guard, "
             "authentication and token services, two interceptors",
             "Bootstrap, navigation, session state, request decoration and route protection"],
            ["M7 Plans and tracking", "Client",
             "Wizard host and four step components, tracking component, dashboard, weight chart, "
             "limit pipe",
             "Wizard rendering, macro log editing, dashboard metrics and chart"],
            ["M8 History and fallbacks", "Client",
             "History list, plan overview, day overview, suggestion screen, empty state, not-found "
             "screen",
             "History navigation, suggestion filters and empty or error states"],
        ],
        widths=[15, 8, 45, 32], font_size=7.9)

    doc.h2("6.1", "Module 1: Identity and Session Management", key="s6.1")
    doc.p(
        "The identity module is the only module whose principal sign-in behaviour is not mediated by a "
        "controller. Registration, refresh and sign-out are controller methods, but the sign-in "
        "request itself is handled by a filter that extends the username-and-password authentication "
        "filter of Spring Security and is mounted at the authenticate path by the security "
        "configuration. The arrangement follows the convention of the framework and has a useful "
        "consequence: the password never reaches a controller method and therefore cannot be logged by "
        "accident."
    )
    doc.p(
        "Registration is implemented in the user service. The method checks the uniqueness of the "
        "username and of the e-mail address, encodes the password with the injected encoder, saves the "
        "entity and converts it to a DTO. The conversion matters twice over: the response never "
        "contains the password hash, and the DTO is produced by the shared mapper rather than by a "
        "hand-written method, which is the convention the module follows throughout. A duplicate "
        "username produces a bad-request failure and a duplicate address the corresponding message for "
        "the address; the advice translates both into a 400 response."
    )
    doc.p(
        "Sign-in proceeds in four steps. The filter deserialises the JSON body into a user instance, "
        "constructs an authentication token and delegates to the custom manager. The manager loads the "
        "user through the user service, translating an unknown username into a bad-credentials failure "
        "so that the response cannot be used to enumerate accounts, and compares the supplied password "
        "with the stored hash through the encoder. On success the filter's successful-authentication "
        "hook asks the token service for a refresh token and writes it into a response cookie that is "
        "HttpOnly, SameSite Lax, scoped to the whole path and given a maximum age equal to the refresh "
        "lifetime. The response body is empty; the client obtains its access token from a separate "
        "call, which keeps the token out of any JavaScript-readable store."
    )
    doc.p(
        "The refresh endpoint is a controller method because it needs the cookie. It reads the cookie, "
        "rejects the request with an unauthorised failure when it is absent, validates the token and "
        "issues a new access token wrapped in a DTO that prefixes the string with the bearer scheme so "
        "that the client can use it directly. Sign-out invalidates nothing on the server, because the "
        "tokens are stateless; it overwrites the cookie with an empty value and a zero maximum age, "
        "which removes it from the browser."
    )
    doc.p(
        "The final artefact of the module resolves the acting user from the security context and "
        "exposes the authenticated identifier and username. Every service in the next two modules "
        "calls the first of those rather than accepting an identifier from the request, which is the "
        "enforcement mechanism for the data-scoping invariant of Section 4.8."
    )

    doc.h2("6.2", "Module 2: Diet Plan Construction", key="s6.2")
    doc.p(
        "Module M2 implements the four-step wizard. Its controller exposes six endpoints rooted at the "
        "form path: a GET and a POST on the status resource, and one POST each for the body metrics, "
        "the goal selection, the meal preference and the activation. The POST on the status resource "
        "is the mechanism for backward navigation: the client sends the form status of the step to "
        "which it wishes to return, and the service responds with the payload appropriate to that step, "
        "reconstructed from the pending document."
    )
    doc.p(
        "The form service holds all of the module's logic, and its methods fall into three groups. The "
        "three creation methods each begin by locating the pending plan; the body-metrics method is "
        "the exception, because it is the method that creates the pending plan in the first place, and "
        "it therefore tolerates the absence of one by querying for a pending plan, copying its "
        "identifier if it exists and writing the request over the document either way. The status "
        "method assembles an envelope object that can carry any of five payloads depending on which "
        "step is current, and the private conversion methods translate between entities and DTOs in "
        "both directions."
    )
    doc.p(
        "The envelope deserves examination because it illustrates a design trade-off. It declares "
        "optional fields for the plan, the body-metrics request, the body-metrics response, the "
        "calorie-estimation response and the two status enumerations, and only one or two of them are "
        "populated on any given call. A stricter design would have used five separate endpoint pairs; "
        "the single envelope reduces the number of endpoints the client must know and makes backward "
        "navigation a single request, at the cost of a wider contract than necessary. The report "
        "records the trade-off rather than hiding it."
    )
    doc.p(
        "Activation has a side effect that is easy to overlook. Before returning, the method calls the "
        "tracking service to create the day-one document. That document copies the plan's expenditure, "
        "calorie target and macronutrient totals, and computes the per-meal split from the macros. "
        "Because the split is stored at creation time, the first day's meal budgets are fixed even if "
        "the plan is later edited, which is the correct behaviour for a log that is meant to be "
        "comparable with the plan active on that day."
    )

    doc.h2("6.3", "Module 3: Daily Tracking and Progress", key="s6.3")
    doc.p(
        "Module M3 is the largest service in the application. Its sixteen public methods fall into four "
        "families: plan retrieval, which reads a plan by identifier, by user, by status or as a "
        "projection; tracking lifecycle, which finds or creates the document for a day; logging, which "
        "accepts a weight or a set of meal macros and recomputes the totals; and aggregation, which "
        "assembles the metrics payload, the calorie allowance for a meal category and the day-by-day "
        "overview."
    )
    doc.p(
        "The logging method is the heart of the module. It begins by resolving today's document, which "
        "the finder creates on demand when the calendar day has changed. It then selects the macro "
        "track for the requested category through a switch expression over the four names defined by "
        "the constants class, copies the taken values into that track, recomputes the three daily "
        "totals by summing the four categories, converts those totals into energy with the Atwater "
        "factors and stores the result in the intake object. The method returns the whole document, so "
        "the client can refresh every card from a single response without a second request."
    )
    doc.p(
        "The aggregation method assembles the dashboard payload. It determines the current week in the "
        "Asia/Kolkata zone, queries the documents between the start of the previous week and the end "
        "of today, projects each record into a weekday abbreviation and a weight value, and builds the "
        "metrics object containing the plan title, the percentage of the target achieved, the duration, "
        "the current day number, the current weight, the three macro targets and the two arrays that "
        "the chart consumes."
    )
    doc.p(
        "Two methods carry the plan lifecycle. One answers a boolean question used by the client to "
        "choose between the dashboard and the empty state. The other compares the elapsed day count "
        "with the configured duration, transitions the plan to inactive and returns true when the "
        "duration is exceeded. Both are called on page load rather than scheduled, which is the "
        "behaviour discussed in Section 4.5.4."
    )

    doc.h2("6.4", "Module 4: AI-Assisted Food Suggestion", key="s6.4")
    doc.p(
        "Module M4 is the smallest service module and the one with the largest external surface. Its "
        "controller exposes a single POST endpoint that accepts four string filters: the meal "
        "category, the meal type, the diet type and the cuisine. The service transforms those filters "
        "into a prompt, appends the calorie allowance for the selected meal, sends the prompt to the "
        "provider through an interface, and parses the reply into a list of suggestion objects."
    )
    doc.p(
        "The prompt is assembled by a private method that formats a single sentence: a request for five "
        "healthy dishes of the chosen cuisine, meal type and diet type, for the chosen meal, under the "
        "computed calorie figure. The allowance comes from the tracking service, which computes the "
        "energy of the selected meal's macro track from the active plan and falls back to five hundred "
        "kilocalories when no active plan exists. The fallback is why the suggestion page can be opened "
        "by a user whose plan has expired without producing a server error."
    )
    doc.p(
        "The adapter is the only class in the system that performs an outbound request. It injects a "
        "REST template declared as a bean in the application class, reads the model identifier and the "
        "key from configuration, and posts a chat request to the completions endpoint. The request "
        "carries a system message that instructs the model to answer only with a JSON array in a fixed "
        "schema and a user message that carries the generated prompt; streaming is disabled. The "
        "adapter then extracts the content of the first choice from the response envelope and returns "
        "it as a string, leaving the parsing to the service."
    )
    doc.p(
        "Two properties of the module must be stated plainly. First, the nutritional values in the "
        "reply are generated: no food-composition database validates them, and the same dish may "
        "receive different values on two consecutive calls. Second, the repository contains a method "
        "that would persist a list of suggestions, but no controller or service invokes it, so the "
        "suggestions collection remains empty in normal operation. Chapter 11 records both properties "
        "in the verification matrix. The module is nevertheless complete in the sense that matters for "
        "a suggestion feature: it never writes generated output into a plan."
    )

    doc.h2("6.5", "Module 5: Cross-Cutting Infrastructure", key="s6.5")
    doc.p(
        "The infrastructure module holds the classes that every other service module depends on. The "
        "exception package defines three runtime exceptions, each with a single message constructor, "
        "and a controller advice that maps them to status codes: a not-found failure to 404, a "
        "bad-request failure to 400, an unauthorised failure to 401 and a JSON processing failure to "
        "410. The choice of 410 for a parsing failure is unusual and is recorded as an observation "
        "rather than a recommendation; 500 or 502 would be the conventional choice for a failure "
        "originating in an upstream provider."
    )
    doc.p(
        "The configuration package holds two classes. One declares the mapper bean that the shared "
        "mapper uses to convert entities into DTOs. The other extends the abstract database client "
        "configuration, fixes the database name and registers two converters between the local date "
        "type and the driver date type, both operating in UTC. The converters exist because several "
        "documents store a local date, which the driver cannot map without instructions; the UTC "
        "choice means that a document created in the early hours of the morning in a positive-offset "
        "zone is stored against the previous UTC date, a detail that the single automated test does "
        "not exercise."
    )
    doc.p(
        "Two further classes belong here even though they live in other packages. The constants class "
        "defines the four meal category strings and a validation method that returns true only for "
        "those four values, which is what the switch in the tracking service relies on. And the "
        "calculator is a final class with a private constructor and eighteen static methods; it is the "
        "only place in the code where the energy equations appear, and each method carries a comment "
        "stating the formula, the units and the convention."
    )

    doc.h2("6.6", "Module 6: Application Shell, Routing and Session", key="s6.6")
    doc.p(
        "The client is bootstrapped by a single call in the entry module with the configuration object "
        "declared in the application configuration file. That object registers zone-based change "
        "detection with event coalescing, the route table, and the HTTP client with the two functional "
        "interceptors in the order base prefix followed by token attachment. The order matters, "
        "because the token interceptor inspects the request URL to decide whether the request is "
        "public, and it can only recognise the public paths once the prefix has been applied."
    )
    doc.p(
        "The route table declares thirteen entries. The empty path redirects to the dashboard. Two "
        "routes are public, namely the login and signup screens. Nine routes are guarded: the "
        "dashboard, the progress page, the suggestion page, the history list and the wizard, together "
        "with the empty state and the two history drill-downs, which the table declares without a "
        "guard. That omission is recorded as an inconsistency in Chapter 11 rather than corrected, "
        "because the report documents the repository as it stands. The remaining entries are the error "
        "page and the wildcard route that redirects to it."
    )
    doc.p(
        "The guard is the enforcement point for client-side route protection. It returns an observable "
        "boolean obtained from the authentication service, which first checks the in-memory access "
        "token against its expiry claim and, if the token is absent or expired, attempts a refresh. A "
        "failed refresh clears the token and returns false, and the guard navigates to the login "
        "screen. Because the guard runs before the component is created, a user who reloads a deep link "
        "is transparently re-authenticated from the refresh cookie."
    )
    doc.p(
        "The header is the only component that renders differently for an anonymous and an "
        "authenticated visitor. It subscribes to router events and records the current URL, so that "
        "the login page shows a sign-up button and the signup page a log-in button, while every other "
        "page shows the four navigation links and the profile avatar. The avatar letter is derived from "
        "the username signal through a computed signal, with a fallback initial so that a slow response "
        "does not leave the avatar empty."
    )

    doc.h2("6.7", "Module 7: Plan and Tracking Screens", key="s6.7")
    doc.p(
        "The wizard host component holds three pieces of state: the body-metrics request that the first "
        "step edits, the three response payloads returned by the service, and the current form "
        "status. On initialisation it fetches the form status and dispatches to the appropriate step; "
        "each step emits its payload through a typed output, and the host advances the status and "
        "stores it. Backward navigation posts the previous status and re-renders from the reply, which "
        "means the host never reconstructs an earlier payload from a later one and the client holds no "
        "draft of its own."
    )
    doc.p(
        "The tracking page loads in a fixed order. It first asks whether the plan duration has been "
        "exceeded and redirects to the empty state if it has. It then loads the active plan and, using "
        "its identifier, loads today's document. Both requests treat a 404 as a signal to navigate "
        "rather than as an error to display, which is why the page has no error branch for the "
        "missing-plan case. The page then renders the daily summary, the four meal cards and the "
        "calorie meter, and writes the updated document back into the same field whenever a meal is "
        "updated or the weight is changed, so a second update does not read stale values."
    )
    doc.p(
        "The dashboard is smaller but performs the same defensive sequence: a duration check, then the "
        "metrics request, with a 404 routed to the empty state. Its template renders the goal "
        "percentage through the one custom pipe in the application, which caps the meter at one hundred "
        "per cent while displaying a greater-than sign in the label when the user has exceeded the "
        "target."
    )

    doc.h2("6.8", "Module 8: History, Suggestions and Fallback Screens", key="s6.8")
    doc.p(
        "The history list loads a projection of every plan of the user, ordered by creation date "
        "descending, and renders each row with the title, a status badge, the plan type, the weight "
        "transition and the duration. Because the projection omits the embedded objects, the list is "
        "served by a single efficient query even when the user has many plans, and the same query "
        "pattern is reused with a limit of one for the empty state's offer to resume the most recent "
        "plan."
    )
    doc.p(
        "Two drill-down screens complete the history feature. The first lists the daily documents of "
        "one plan as cards showing the date, the weight, the plan's expenditure and the consumed "
        "energy, with the three macro totals beneath; it is again served by a projection. The second "
        "shows a single stored document read-only, including its per-meal split, and is the screen a "
        "user reaches to review what they actually logged on a given day. Neither offers editing, "
        "which is consistent with the principle that history is a record rather than a workspace."
    )
    doc.p(
        "The suggestion page holds four filter groups in a single object, renders each group as a row "
        "of pill buttons, and issues a POST when the user asks for suggestions. It maintains two "
        "boolean flags that drive the three visual states of the results region: a prompt before the "
        "first request, a loading indicator during the request and an error message when the call or "
        "the parse fails. The two fallback screens are deliberately minimal: the empty state explains "
        "the situation in two sentences and offers a single primary action, and the not-found screen "
        "renders a large numeral, a short explanation and a button back to the dashboard."
    )

    # ================================================================== CHAPTER 7
    doc.chapter_heading(7, "Database Design and Data Dictionary", key="ch7")
    doc.h2("7.1", "Design Approach", key="s7.1")
    doc.p(
        "Macrova uses MongoDB, so the schema design proceeds from access patterns rather than from "
        "normalisation. Three questions determined the model. Which data are always read together? The "
        "daily document and its four meal tracks, which are read together every time the tracking page "
        "or the dashboard loads. Which data change independently? The plan header and its targets, "
        "which change only while the wizard is being used. And which data are bulky and rarely read in "
        "full? The historical documents, which the history screens read through projections that never "
        "load the embedded meal tracks at all."
    )
    doc.p(
        "The answers produced the model of Figure 7.1: a compact plan header document, a daily document "
        "that embeds its own value objects, and a projection strategy for the history screens. Table "
        "7.1 records the resulting collections with their approximate document sizes, which were "
        "estimated from the number of fields and the size of the embedded objects rather than measured "
        "against a corpus, because the corpus available to the project was a single user's history."
    )
    doc.figure("er-document-model.png",
               "Entity-relationship view of the macrova database, showing the fields and references of "
               "each collection", width=5.7)
    doc.table(
        "Collection inventory of the macrova database",
        ["Collection", "Document class", "Approximate size", "Access pattern"],
        [
            ["users", "User entity", "about 250 bytes",
             "Read by username on every request; written once at registration"],
            ["diet_plans", "DietPlan entity", "about 700 bytes",
             "Read by user and status on every wizard and dashboard call; written at each wizard step"],
            ["diet_plan_tracks", "DietPlanTrack entity", "about 600 bytes",
             "Read by plan and date for tracking and metrics; one document per tracked day"],
            ["ai_food_suggests", "AIFoodSuggest entity", "about 300 bytes",
             "The write method exists but is never invoked, so the collection is unused"],
        ],
        widths=[18, 24, 16, 42], font_size=8.2)

    doc.h2("7.2", "The users Collection", key="s7.2")
    doc.p(
        "The users collection is the smallest and the most security-sensitive. It is declared by the "
        "user entity with the collection name given explicitly and annotated with Lombok accessors. "
        "The class declares four fields and no behaviour; validation, uniqueness checks and hashing "
        "are performed by the user service before the document is written."
    )
    doc.table(
        "Data dictionary \u2014 users",
        ["Field", "Type", "Constraint or index", "Purpose"],
        [
            ["_id", "String", "Primary key, generated by the driver when absent",
             "Document identifier, referenced by the owner field of a plan"],
            ["username", "String", "Unique in practice, enforced by a check before insert",
             "Login name and the subject of both tokens"],
            ["email", "String", "Unique in practice, enforced by a check before insert",
             "Contact address captured at registration"],
            ["password", "String", "Never null; the output of the encoder",
             "BCrypt hash, sixty characters including the salt prefix"],
        ],
        widths=[14, 12, 38, 36], font_size=8.2)
    doc.p(
        "Two observations follow. The uniqueness of the username and the address is enforced by "
        "application checks rather than by a unique index, so two concurrent registrations with the "
        "same username could both succeed and a subsequent sign-in would resolve to one of the two "
        "documents depending on insertion order; adding the indexes of Table 7.8 would close that race "
        "without changing the application logic. Second, the document holds no display name, timestamp "
        "or account status, which is consistent with the single-role design but would have to be "
        "extended before an administrative interface could be built."
    )

    doc.h2("7.3", "The diet_plans Collection", key="s7.3")
    doc.p(
        "The plans collection stores the plan header. It is written at every wizard step, so its fields "
        "fall into four groups: those written by the first step, which capture identity and body "
        "measurements; those written by the second, which capture the goal and the derived targets; "
        "those written by the third, which capture preferences and macros; and the status fields, which "
        "every step writes."
    )
    doc.table(
        "Data dictionary \u2014 diet_plans",
        ["Field", "Type", "Written at", "Purpose"],
        [
            ["_id", "String", "First save",
             "Identifier, referenced by the plan field of a daily document"],
            ["title", "String", "Body metrics",
             "User-supplied plan name shown on the dashboard and in history"],
            ["plan", "Plan enumeration", "Body metrics",
             "Weight loss or weight gain; selects a deficit or a surplus"],
            ["age", "int", "Body metrics", "Years; the third term of the metabolic equation"],
            ["gender", "Gender enumeration", "Body metrics",
             "Male or female; selects the constant plus five or minus one hundred and sixty-one"],
            ["height", "double", "Body metrics", "Centimetres; the second term of the equation"],
            ["weight", "double", "Body metrics", "Kilograms at plan creation"],
            ["todayWeight", "double", "Body metrics, then tracking",
             "Kilograms at the latest update; shown as the current weight"],
            ["targetWeight", "double", "Body metrics",
             "Goal weight, used for display and for the duration choice"],
            ["activity", "Activity enumeration", "Body metrics",
             "One of five levels carrying multipliers 1.2, 1.375, 1.55, 1.725 and 1.9"],
            ["tdee", "double", "Body metrics",
             "Rounded basal rate multiplied by the activity factor, in kilocalories per day"],
            ["goal", "Goal enumeration", "Goal selection",
             "Mild, moderate or aggressive, carrying 15, 20 or 25 per cent"],
            ["duration", "int", "Goal selection", "Planned length in days, chosen by the user"],
            ["targetCalories", "double", "Goal selection, replaced at activation",
             "Daily energy target after the deficit or surplus and the rounding step"],
            ["currentCalories", "double", "Meal preference",
             "Energy equivalent of the chosen macro grams; copied into the target at activation"],
            ["dietType", "DietType enumeration", "Meal preference",
             "Balanced, high protein, low carbohydrate, low fat or custom"],
            ["mealType", "MealType enumeration", "Meal preference",
             "Non-vegetarian, vegetarian, vegan or eggetarian"],
            ["macros", "Macros object", "Meal preference",
             "Protein, carbohydrate and fat in grams; drives the per-meal split"],
            ["mealCount", "int", "Meal preference", "Two to five meals per day, recorded for display"],
            ["eveningSnack", "boolean", "Meal preference",
             "Whether an evening snack is included"],
            ["createdAt", "LocalDate", "Activation",
             "Activation date, from which the day count is computed"],
            ["userId", "String", "Body metrics",
             "Owner, resolved from the security context and never from the request"],
            ["planStatus", "PlanStatus enumeration", "Every step",
             "Pending at creation, active at activation, inactive when the duration is exceeded"],
            ["formStatus", "FormStatus enumeration", "Every step",
             "Body metrics, goal selection, meal preference, preview or completed"],
        ],
        widths=[14, 16, 18, 52], font_size=8.0)
    doc.p(
        "The document contains one redundancy that deserves comment. The target is computed twice: once "
        "when the goal is selected, from the expenditure and the deficit, and once when the plan is "
        "activated, from the macronutrient grams chosen in the third step. The service overwrites the "
        "first value with the second, and the source carries a comment acknowledging that the "
        "intermediate field should be removed and the target used directly. The consequence is that a "
        "user who accepts the balanced preset sees a target very close to the deficit-derived value, "
        "while a user who edits the grams to an unusual split sees a target that reflects the edit "
        "rather than the deficit. The behaviour is documented rather than corrected, because it is "
        "deliberate in the current design: the macro split is the final authority on the energy target, "
        "since it is the last decision the user makes."
    )
    doc.table(
        "Example document \u2014 diet_plans",
        ["Field", "Value", "Field", "Value"],
        [
            ["_id", "6547c1f0b8a1f64a9c2d1e03", "title", "Karthick's Fat Loss Plan"],
            ["plan", "WEIGHT_LOSS", "age and gender", "25, MALE"],
            ["height and weight", "175, 95", "target and current weight", "75, 94.15"],
            ["activity", "LIGHT", "tdee", "2645"],
            ["goal and duration", "MODERATE, 180 days", "target and current calories", "2152, 2152"],
            ["dietType and mealType", "BALANCED, NON_VEGETARIAN",
             "macros", "protein 161 g, carbs 215 g, fat 72 g"],
            ["mealCount and snack", "3, true", "createdAt", "2026-11-06"],
            ["planStatus and formStatus", "ACTIVE, COMPLETED", "userId", "6547c0d3b8a1f64a9c2d1df1"],
        ],
        widths=[22, 28, 26, 24], font_size=8.0)

    doc.h2("7.4", "The diet_plan_tracks Collection", key="s7.4")
    doc.p(
        "The tracking collection holds one document per tracked day. It is the only collection whose "
        "documents are created implicitly, by the read path rather than by an explicit user action: "
        "when the tracking or metrics endpoint discovers that no document exists for the current date, "
        "it creates one with the plan's current targets and zero logged intake."
    )
    doc.table(
        "Data dictionary \u2014 diet_plan_tracks",
        ["Field", "Type", "Purpose"],
        [
            ["_id", "String", "Identifier returned to the client and used by the single-document "
                              "endpoint"],
            ["dietPlanId", "String", "Owner plan, resolved by query rather than by a database reference"],
            ["createdAt", "LocalDate", "The day the document represents, stored as a date at UTC "
                                       "midnight"],
            ["dayCount", "int", "One-based index of the day within the plan, computed from the "
                                "activation date"],
            ["weight", "double", "Weight recorded on that day, initially the plan's weight"],
            ["tdee", "double", "Snapshot of the plan's expenditure, for later comparison"],
            ["intake", "Calories object", "Daily energy: the total from the plan's target and the "
                                          "taken value recomputed from the logged grams"],
            ["protein", "Calories object", "Daily protein allowance and the grams logged so far"],
            ["carbs", "Calories object", "Daily carbohydrate allowance and the grams logged so far"],
            ["fat", "Calories object", "Daily fat allowance and the grams logged so far"],
            ["mealKcal", "MealKcal object", "Four macro-track objects, one per meal, each holding the "
                                            "per-meal protein, fat and carbohydrate allowance and the "
                                            "values logged against it"],
        ],
        widths=[14, 16, 70], font_size=8.2)
    doc.p(
        "The arithmetic explains the structure. Each of the three daily macro objects holds a total, "
        "fixed at creation from the plan's macros, and a taken value, recomputed on every update as the "
        "sum of the four meal tracks. The intake object follows the same pattern with a conversion: its "
        "total is the plan's daily energy target, while its taken value is computed from the three "
        "macro taken values with the Atwater factors rather than summed from the meal tracks, so the "
        "two representations cannot drift apart."
    )
    doc.table(
        "Worked example \u2014 meal split and logged values for one day",
        ["Category", "Share of the daily macros", "Protein, total and taken",
         "Carbohydrate, total and taken", "Fat, total and taken"],
        [
            ["Breakfast", "30 %", "48, 45", "65, 70", "22, 25"],
            ["Lunch", "30 %", "48, 45", "65, 70", "22, 25"],
            ["Snack", "15 %", "24, 20", "32, 30", "11, 15"],
            ["Dinner", "25 %", "40, 0", "54, 0", "18, 0"],
            ["Daily document", "100 %", "161, 110", "215, 170", "72, 65"],
            ["Derived energy", "Atwater", "110 \u00d7 4 = 440", "170 \u00d7 4 = 680", "65 \u00d7 9 = 585"],
        ],
        widths=[18, 20, 20, 20, 22], font_size=8.2)
    doc.p(
        "The final row reproduces the arithmetic that the service performs. The three contributions sum "
        "to 1705 kilocalories, which is the value displayed as the consumed intake in the tracking "
        "screen of Figure 9.10, and which yields seventy-nine per cent of the 2152 kilocalorie target on "
        "the dashboard of Figure 9.9."
    )

    doc.h2("7.5", "The ai_food_suggests Collection", key="s7.5")
    doc.p(
        "The fourth collection is declared for completeness of the suggestion feature. Its document "
        "class holds an identifier, a name, a calorie object, a macro object and a description, which "
        "is exactly the schema the model is instructed to return. The repository is a plain repository "
        "with no additional query methods, and the service exposes a single method that saves a list of "
        "documents. No controller invokes that method, so the collection is created on first use but "
        "otherwise remains empty."
    )
    doc.table(
        "Data dictionary \u2014 ai_food_suggests",
        ["Field", "Type", "Purpose"],
        [
            ["_id", "String", "Identifier, generated on save"],
            ["name", "String", "Dish name as returned by the model"],
            ["calories", "Calories object", "Model-reported energy value; the taken field is unused"],
            ["macronutrients", "Macros object", "Model-reported protein, carbohydrate and fat in grams"],
            ["description", "String", "One-paragraph description used as the body of a card"],
        ],
        widths=[18, 16, 66], font_size=8.2)

    doc.h2("7.6", "Indexing, Consistency and Integrity", key="s7.6")
    doc.p(
        "The repository contains no explicit index definitions. MongoDB creates a unique index on the "
        "identifier of every collection automatically, and that is the only index that currently "
        "exists. The queries the application issues are therefore collection scans at present: the plan "
        "finder by user and status scans the plans collection, and the tracking finder by date and plan "
        "scans the tracking collection. At the scale of a single user with a few hundred documents the "
        "scans are imperceptible, but the indexes in Table 7.8 would be appropriate before the "
        "application is used by a group."
    )
    doc.table(
        "Recommended indexes and the queries they would accelerate",
        ["Collection", "Index", "Query accelerated"],
        [
            ["users", "username, unique", "The username lookup performed on every request"],
            ["users", "email, unique", "The existence check performed during registration"],
            ["diet_plans", "user identifier and plan status",
             "The pending and active lookups performed at every wizard step"],
            ["diet_plans", "user identifier and creation date, descending",
             "The history list ordered by creation date"],
            ["diet_plan_tracks", "plan identifier and date, descending",
             "Today's document and the weekly range query"],
            ["diet_plan_tracks", "plan identifier and date, ascending",
             "The day-by-day overview of a plan"],
        ],
        widths=[20, 32, 48], font_size=8.2)
    doc.p(
        "Consistency is maintained by the service layer alone. There are no transactions, which is "
        "acceptable because the only multi-document operation is activation: it saves the plan and then "
        "creates the first document. If the second write failed, the user would hold an active plan "
        "with no first-day document, and the read path would repair the inconsistency on the next load "
        "because the tracking finder creates the missing document on demand. That self-healing property "
        "is why the absence of transactions does not produce a visible failure mode."
    )
    doc.p(
        "Referential integrity is not enforced. The plan identifier inside a daily document is resolved "
        "by query, and a dangling reference produces the behaviour the application already exhibits "
        "when a plan has been removed outside the application: the tracking endpoints return a "
        "not-found failure, which the client routes to the error page. No deletion endpoint exists in "
        "the delivered system, so the situation can arise only through direct manipulation of the "
        "database."
    )

    # ================================================================== CHAPTER 8
    doc.chapter_heading(8, "REST Interface and Client Service Layer", key="ch8")
    doc.h2("8.1", "Conventions", key="s8.1")
    doc.p(
        "The interface follows a small set of conventions consistently. Resource paths are kebab-case, "
        "and a noun is pluralised only where a collection is genuinely being addressed. Identifiers "
        "appear as path variables rather than as query parameters. Payloads are JSON in both "
        "directions. Success responses carry 200 with a body, and error responses carry 400, 401, 404 "
        "or 410 with a body that wraps the message in a single-element array. No endpoint uses 201 or "
        "204, because the client does not need to distinguish creation from update and always consumes "
        "the returned document."
    )
    doc.p(
        "Authentication is required on every endpoint except registration and refresh, together with "
        "the sign-in path, which is mounted by the security filter rather than by a controller. The "
        "access token is read from the authorisation header with the bearer scheme. The refresh token "
        "is read from a cookie rather than from the header, which is a deliberate asymmetry: the access "
        "token is expected to be handled by client code and the refresh token is not."
    )

    doc.h2("8.2", "Endpoint Catalogue", key="s8.2")
    doc.p(
        "Table 8.1 lists every endpoint implemented in the repository with its request and response "
        "types. The table was produced by enumerating the mapping annotations on the four controller "
        "classes and cross-checking each entry against the client method that calls it. The entries "
        "with no client caller are marked as such, because a reviewer who counts endpoints will "
        "otherwise assume that all of them are in use."
    )
    doc.table(
        "Complete REST endpoint catalogue",
        ["Method", "Path", "Request body", "Response body", "Client caller"],
        [
            ["POST", "/user/register", "Username, e-mail, password", "User DTO", "Authentication "
                                                                               "service, signup"],
            ["POST", "/authenticate", "Username, password", "Empty 200 with a cookie",
             "Authentication service, login"],
            ["POST", "/user/refresh", "None; the cookie is read", "Access token DTO",
             "Authentication service, refresh"],
            ["POST", "/user/logout", "None", "Empty 200 with a cleared cookie",
             "Authentication service, logout"],
            ["GET", "/user/username", "None", "Username DTO", "Authentication service, username"],
            ["GET", "/diet-plan/form/status", "None", "Form status envelope", "Wizard host, "
                                                                             "initialisation"],
            ["POST", "/diet-plan/form/status", "Current form status", "Form status envelope",
             "Wizard host, backward navigation"],
            ["POST", "/diet-plan/form/body-metrics", "Body metrics request", "Body metrics response",
             "Body metrics step"],
            ["POST", "/diet-plan/form/goal-selection", "Goal selection request",
             "Calorie estimation response", "Goal selection step"],
            ["POST", "/diet-plan/form/meal-preference", "Meal preference request", "Plan",
             "Meal preference step"],
            ["POST", "/diet-plan/form/create", "None", "Plan", "Review step"],
            ["GET", "/diet-plan", "None", "The active plan", "Tracking screen"],
            ["GET", "/diet-plan/all", "None", "List of plans", "No client caller"],
            ["GET", "/diet-plan/{dietPlanId}", "None", "Plan", "No client caller"],
            ["GET", "/diet-plan/history", "None", "List of plan history DTOs", "History list"],
            ["GET", "/diet-plan/past-plan", "None", "Plan history DTO", "Empty state"],
            ["GET", "/diet-plan/status", "None", "Boolean", "Dashboard and tracking screen"],
            ["GET", "/diet-plan/active-plans", "None", "Boolean", "No client caller"],
            ["GET", "/diet-plan/metrics", "None", "Metrics DTO", "Dashboard"],
            ["GET", "/diet-plan/overview/{dietPlanId}", "None", "List of overview DTOs",
             "Plan overview"],
            ["GET", "/diet-plan/meal-kcal/{id}", "None", "Meal calorie object", "No client caller"],
            ["GET", "/diet-plan/track/{trackId}", "None", "Tracking document", "Day overview"],
            ["GET", "/diet-plan/track/plan/{dietPlanId}", "None", "Tracking document",
             "Tracking screen"],
            ["POST", "/diet-plan/add-weight/{dietPlanId}", "A bare JSON number", "Tracking document",
             "Weight update"],
            ["POST", "/diet-plan/{category}/{dietPlanId}", "Macro track", "Tracking document",
             "Meal update"],
            ["POST", "/ai-food-suggest", "Four filters", "List of suggestions", "Suggestion screen"],
        ],
        widths=[9, 33, 20, 20, 18], font_size=7.8)
    doc.p(
        "Four entries deserve a note because they are not reachable from the current client. The "
        "all-plans endpoint returns every plan without a projection, which is why the history screen "
        "uses the projection endpoint instead. The active-plans endpoint duplicates a boolean that the "
        "client obtains indirectly by loading the metrics and interpreting a not-found response. The "
        "meal-calorie endpoint exposes a computation that the tracking page performs implicitly when it "
        "renders the required grams. And the weight endpoint accepts a bare JSON number rather than an "
        "object, which binds correctly but is unusual, and is called out in Chapter 11."
    )

    doc.h2("8.3", "Request and Response Examples", key="s8.3")
    doc.p(
        "The following examples were produced against the running application and are reproduced with "
        "the identifiers and credentials replaced by representative values. They are included because a "
        "catalogue of paths does not convey the shape of the payloads, and the shape is what a future "
        "client has to match."
    )
    doc.code("Listing 8.1 \u2014 registration, request and response",
             "POST /user/register\n"
             "Content-Type: application/json\n"
             "\n"
             '{ "username": "karthick", "email": "karthick@example.com", "password": "diet2026plan" }\n'
             "\n"
             "HTTP/1.1 200 OK\n"
             "\n"
             '{ "id": "6547c0d3b8a1f64a9c2d1df1", "username": "karthick",\n'
             '  "email": "karthick@example.com" }')
    doc.code("Listing 8.2 \u2014 sign-in followed by a token refresh",
             "POST /authenticate\n"
             "\n"
             '{ "username": "karthick", "password": "diet2026plan" }\n'
             "\n"
             "HTTP/1.1 200 OK\n"
             "Set-Cookie: Refresh-Token=eyJhbGciOiJIUzUxMiJ9...; HttpOnly; SameSite=Lax;\n"
             "            Path=/; Max-Age=86400\n"
             "\n"
             "POST /user/refresh\n"
             "Cookie: Refresh-Token=eyJhbGciOiJIUzUxMiJ9...\n"
             "\n"
             "HTTP/1.1 200 OK\n"
             "\n"
             '{ "accessToken": "Bearer eyJhbGciOiJIUzUxMiJ9..." }')
    doc.code("Listing 8.3 \u2014 first wizard step, request and response",
             "POST /diet-plan/form/body-metrics\n"
             "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9...\n"
             "\n"
             '{ "title": "Karthick\'s Fat Loss Plan", "plan": "WEIGHT_LOSS",\n'
             '  "gender": "MALE", "age": 25, "height": 175.0, "weight": 95.0,\n'
             '  "targetWeight": 75.0, "activity": "LIGHT" }\n'
             "\n"
             "HTTP/1.1 200 OK\n"
             "\n"
             '{ "tdee": 2645.0, "weight": 95.0, "targetWeight": 75.0, "plan": "WEIGHT_LOSS" }')
    doc.code("Listing 8.4 \u2014 dashboard metrics, response",
             "GET /diet-plan/metrics\n"
             "\n"
             "HTTP/1.1 200 OK\n"
             "\n"
             '{ "title": "Karthick\'s Fat Loss Plan", "taken": 79, "duration": 180,\n'
             '  "currentDay": 4, "currentWeight": 94.15, "intake": 2152.0,\n'
             '  "protein": 161.0, "carbs": 215.0, "fat": 72.0,\n'
             '  "days": ["Fri", "Sat", "Sun", "Mon"],\n'
             '  "weights": [95.0, 94.85, 94.6, 94.15] }')
    doc.code("Listing 8.5 \u2014 meal update, request and truncated response",
             "POST /diet-plan/breakfast/6547c1f0b8a1f64a9c2d1e03\n"
             "\n"
             '{ "protein": { "taken": 45, "total": 0 },\n'
             '  "fat":     { "taken": 25, "total": 0 },\n'
             '  "carbs":   { "taken": 70, "total": 0 } }\n'
             "\n"
             "HTTP/1.1 200 OK\n"
             "\n"
             '{ "_id": "6547c9a2b8a1f64a9c2d1e55", "weight": 95.0, "tdee": 2645.0,\n'
             '  "intake": { "taken": 1705.0, "total": 2152.0 },\n'
             '  "protein": { "taken": 110.0, "total": 161.0 },\n'
             '  "carbs": { "taken": 170.0, "total": 215.0 },\n'
             '  "fat": { "taken": 65.0, "total": 72.0 },\n'
             '  "mealKcal": { "breakfast": { ... }, "lunch": { ... },\n'
             '                "snack": { ... }, "dinner": { ... } },\n'
             '  "dayCount": 4, "createdAt": "2026-11-09",\n'
             '  "dietPlanId": "6547c1f0b8a1f64a9c2d1e03" }')
    doc.p(
        "Two details of the last listing are worth pointing out. The request sends totals of zero in "
        "each calorie object, because the service ignores the totals and reads only the taken field, so "
        "the client could have sent a smaller payload. And the response returns the entire document "
        "including all four meal tracks, which is what allows the page to re-render every card from a "
        "single response."
    )

    doc.h2("8.4", "Error Responses", key="s8.4")
    doc.p(
        "Errors reach the client through two paths. Exceptions raised inside a controller or a service "
        "are caught by the controller advice and rendered as a JSON object with a single-element error "
        "array. Exceptions raised inside the filter chain, including token verification failures, are "
        "caught by the chain's exception filter and rendered as plain text with a 401 status. The "
        "client treats both as failures and either displays a toast or navigates, so the inconsistency "
        "in media type has no functional consequence at present, but it is recorded as a defect of the "
        "contract."
    )
    doc.table(
        "Error responses produced by the current implementation",
        ["Trigger", "Handled by", "Status", "Body"],
        [
            ["Unknown plan identifier", "Controller advice", "404", "An error array with a plan "
                                                                   "message"],
            ["Unknown tracking identifier", "Controller advice", "404",
             "An error array with a tracking message"],
            ["No pending plan when a step is submitted", "Controller advice", "400",
             "An error array stating that no pending plan was found"],
            ["Invalid meal category in the path", "Controller advice", "400",
             "An error array naming the invalid category"],
            ["Duplicate username or e-mail address", "Controller advice", "400",
             "An error array with the corresponding message"],
            ["Malformed JSON from the model provider", "Controller advice", "410",
             "An error array carrying the parser message"],
            ["Missing refresh cookie or invalid refresh token", "Controller advice", "401",
             "An error array with a token message"],
            ["Expired access token", "Chain exception filter", "401",
             "Plain text with an expiry message"],
            ["Invalid token signature", "Chain exception filter", "401",
             "Plain text with a verification failure"],
            ["Wrong password or unknown username", "Authentication filter", "401",
             "Plain text with a credentials failure"],
            ["Any other unhandled runtime exception", "Chain exception filter", "400",
             "Plain text with a bad-request message"],
        ],
        widths=[30, 24, 8, 38], font_size=8.0)

    doc.h2("8.5", "Client Service Layer", key="s8.5")
    doc.p(
        "The client mirrors the service surface with four injectable services, all provided at the root "
        "of the application and therefore singletons for the lifetime of the page. Table 8.3 lists "
        "their methods, the endpoint each calls and the component that calls it."
    )
    doc.table(
        "Client-side service methods",
        ["Service", "Method", "Endpoint", "Principal caller"],
        [
            ["Authentication service", "signup", "POST /user/register", "Signup screen"],
            ["Authentication service", "login", "POST /authenticate", "Login screen"],
            ["Authentication service", "logout", "POST /user/logout", "Header"],
            ["Authentication service", "request refresh", "POST /user/refresh",
             "Authentication check"],
            ["Authentication service", "is authenticated", "POST /user/refresh when needed",
             "Route guard, token interceptor"],
            ["Authentication service", "username", "GET /user/username", "Header, through a signal"],
            ["Token service", "is logged in", "Local only, through jwt-decode",
             "Authentication check"],
            ["Plan service", "form status", "GET /diet-plan/form/status", "Wizard host"],
            ["Plan service", "form details for a status", "POST /diet-plan/form/status",
             "Wizard host, backward navigation"],
            ["Plan service", "body metrics", "POST /diet-plan/form/body-metrics",
             "Body metrics step"],
            ["Plan service", "goal selection", "POST /diet-plan/form/goal-selection",
             "Goal selection step"],
            ["Plan service", "meal preference", "POST /diet-plan/form/meal-preference",
             "Meal preference step"],
            ["Plan service", "activate", "POST /diet-plan/form/create", "Review step"],
            ["Plan service", "duration reached", "GET /diet-plan/status",
             "Dashboard, tracking screen"],
            ["Plan service", "active plan", "GET /diet-plan", "Tracking screen"],
            ["Plan service", "track of a plan", "GET /diet-plan/track/plan/{id}",
             "Tracking screen"],
            ["Plan service", "update macros", "POST /diet-plan/{category}/{id}", "Meal update"],
            ["Plan service", "add weight", "POST /diet-plan/add-weight/{id}", "Weight update"],
            ["Plan service", "metrics", "GET /diet-plan/metrics", "Dashboard"],
            ["Plan service", "history", "GET /diet-plan/history", "History list"],
            ["Plan service", "past plan", "GET /diet-plan/past-plan", "Empty state"],
            ["Plan service", "overview of a plan", "GET /diet-plan/overview/{id}", "Plan overview"],
            ["Plan service", "track by identifier", "GET /diet-plan/track/{id}", "Day overview"],
            ["Plan service", "update plan", "PUT /diet-plan/update",
             "Declared, with no caller and no server mapping"],
            ["Suggestion service", "suggest foods", "POST /ai-food-suggest", "Suggestion screen"],
        ],
        widths=[18, 30, 30, 22], font_size=7.9)
    doc.p(
        "The table contains two inconsistencies that a careful reader will notice. The client declares "
        "a plan-update method that issues a PUT to a path the service does not map, so a call would be "
        "rejected by the security chain rather than answered with a 404. And the meal-update method "
        "lowercases the category before sending it, which is redundant because the service lowercases "
        "the value again when it selects the track. Both observations are recorded in the verification "
        "matrix rather than silently corrected, because the report documents the repository as it "
        "stands."
    )

    doc.h2("8.6", "Interceptors and Cross-Cutting Client Concerns", key="s8.6")
    doc.p(
        "The base-prefix interceptor prefixes every request whose URL does not already begin with a "
        "scheme with the environment base URL, which is the string /api. The token interceptor is more "
        "selective: it returns the request unchanged when the URL contains the sign-in, registration or "
        "refresh paths, and otherwise consults the authentication service, which may itself issue a "
        "refresh request before the original request proceeds. The use of switchMap ensures that the "
        "refresh completes before the original request is dispatched, and the credentials flag ensures "
        "that the refresh cookie travels with the request. Because the prefix is applied first, the "
        "token interceptor sees the final URL and can recognise the public paths by substring."
    )
    doc.p(
        "The mechanism has one weakness worth stating. Because the authentication check issues a refresh "
        "whenever the in-memory token is missing, a burst of parallel requests on a freshly loaded page "
        "can issue several refresh calls, and each will succeed because the cookie is not single-use. "
        "The consequence is redundant server work rather than incorrect behaviour, but a shared refresh "
        "observable would be the conventional remedy and is proposed in Chapter 12."
    )
    return doc
