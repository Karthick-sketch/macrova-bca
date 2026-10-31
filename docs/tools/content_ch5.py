"""Chapter 5 - Technologies and tools."""

from __future__ import annotations

from reportlab.platypus import Paragraph, Spacer

import diagrams_arch as A
import theme as T
from theme import S, bullets, chapter, figure, h2, h3, numbered, table


def build():
    st = []
    st += chapter(5, "TECHNOLOGIES AND TOOLS")
    st += [h2("5.1 Introduction")]
    st += [T.body(
        "This chapter records the software, hardware, languages, frameworks and tools used to "
        "build and operate the system. Every version listed in Table 5.3 was read from the two "
        "build descriptors of the repository \u2014 <font name='Mono' size='8'>backend/pom.xml</font> "
        "and <font name='Mono' size='8'>frontend/package.json</font> \u2014 rather than "
        "recalled from general knowledge, so the table describes the delivered artefact "
        "rather than a typical stack. Version numbers for the frameworks are cross-checked "
        "against their reference documentation [16], [17], [18].")]

    st += [h2("5.2 Software Requirements")]
    st += table(
        ["Component", "Requirement", "Used for"],
        [["Operating system", "Windows 10/11, macOS 13+ or a Linux distribution with a "
                              "64-bit JDK", "Development and deployment host"],
         ["Java Development Kit", "JDK 21 (the Maven compiler release is 21)", "Compiling and "
                                                                               "running the back end"],
         ["Maven", "Maven 3.9 (wrapper included as mvnw/mvnw.cmd)", "Dependency resolution, "
                                                                    "build, test, packaging"],
         ["Node.js", "18.19+, 20.11+ or 22.x, as required by Angular 19", "Building and "
                                                                          "serving the client"],
         ["npm", "10.x", "Dependency installation, script execution"],
         ["MongoDB", "A local or hosted instance reachable on port 27017, database "
                     "<font name='Mono' size='7'>macrova</font>", "Persistence"],
         ["MongoDB Compass / mongosh", "Optional", "Inspecting collections and documents "
                                                   "during development"],
         ["Web browser", "Chromium 120+ or Firefox 120+", "Running the client and the "
                                                          "developer tools"],
         ["Git and a GitHub account", "Any recent version", "Version control and remote backup"],
         ["Postman or curl", "Optional", "Exercise of endpoints independently of the client"]],
        widths=[1.5, 2.8, 2.2],
        font_size=7.2,
        caption="Software requirements of the development and runtime environment")

    st += [h2("5.3 Hardware Requirements")]
    st += table(
        ["Resource", "Minimum", "Recommended", "Remark"],
        [["Processor", "Dual-core x86-64, 2.0 GHz", "Quad-core, 2.5 GHz or faster",
          "The Angular development server and the JVM compete for cores during a rebuild"],
         ["Memory", "4 GB", "8 GB or more", "Maven plus the JVM plus the Node process exceed "
                                           "4 GB when both hot reload and tests run"],
         ["Free disk", "3 GB", "10 GB", "Maven dependencies, node_modules and the MongoDB data "
                                        "directory"],
         ["Display", "1366 \u00d7 768", "1920 \u00d7 1080", "The dashboard is designed for a "
                                                            "content column of 52 rem"],
         ["Network", "Not required for local use", "4G or broadband",
          "Required only for dependency resolution and for the language-model call"],
         ["Server (deployment)", "One vCPU, 1 GB RAM", "Two vCPU, 2 GB RAM",
          "The service is stateless and memory-light; the database dominates the footprint"]],
        widths=[1.05, 1.6, 1.6, 2.25],
        font_size=7.2,
        caption="Hardware requirements for development and for deployment")

    st += [h2("5.4 Programming Languages and Data Formats")]
    st += [h3("5.4.1 Java 21")]
    st += [T.body(
        "The back end is written entirely in Java 21. The language level is exploited in "
        "three specific ways. Records are used for every request and response payload "
        "(<font name='Mono' size='8'>LoginRequest</font>, <font name='Mono' size='8'>MetricsDTO</font>, "
        "<font name='Mono' size='8'>DietPlanHistoryDTO</font>, "
        "<font name='Mono' size='8'>TrackingOverviewDTO</font> and others), which removes "
        "boilerplate and makes immutability the default. Text blocks are not used, but "
        "switch expressions and pattern matching for <i>instanceof</i> appear in the service "
        "layer. The standard <font name='Mono' size='8'>java.time</font> API supplies "
        "<font name='Mono' size='8'>LocalDate</font> and "
        "<font name='Mono' size='8'>ChronoUnit</font>, which the day-count arithmetic "
        "depends on.")]
    st += [h3("5.4.2 TypeScript 5.7")]
    st += [T.body(
        "The client is written in TypeScript with strict template checking and "
        "<font name='Mono' size='8'>strict</font> compiler options. Every HTTP payload has an "
        "interface in <font name='Mono' size='8'>core/models</font> "
        "(<font name='Mono' size='8'>DietPlan</font>, <font name='Mono' size='8'>DietPlanTrack</font>, "
        "<font name='Mono' size='8'>Metrics</font>, <font name='Mono' size='8'>Macros</font>, "
        "<font name='Mono' size='8'>AIFoodSuggest</font>, "
        "<font name='Mono' size='8'>Toast</font>), and the services declare typed observables "
        "so that a mismatch between the server contract and the template is a compile error "
        "rather than a runtime undefined.")]
    st += [h3("5.4.3 HTML5, CSS3 and JSON")]
    st += [T.body(
        "Templates are HTML5 with Angular's control-flow blocks "
        "(<font name='Mono' size='8'>@if</font>, <font name='Mono' size='8'>@for</font>) and "
        "two-way binding through <font name='Mono' size='8'>ngModel</font>. Styling is CSS3 "
        "with custom properties, flexbox and grid; no CSS framework is used, which keeps the "
        "bundle small and the design system explicit. JSON is the sole wire format: requests "
        "and responses are JSON, the MongoDB driver stores BSON that is isomorphic to the "
        "Java classes, and the language model is instructed to answer in JSON.")]

    st += [h2("5.5 Frameworks and Libraries")]
    st += [T.body(
        "Table 5.3 lists the frameworks and libraries with the versions declared in the "
        "build descriptors. Where a version is managed by a parent rather than declared, the "
        "table says so.")]
    st += table(
        ["Library / framework", "Version", "Module", "Role in the system"],
        [["Spring Boot", "3.4.4 (parent)", "back end", "Auto-configuration, embedded Tomcat, "
                                                       "dependency management"],
         ["spring-boot-starter-web", "managed", "back end", "Spring MVC, Jackson, validation "
                                                            "infrastructure"],
         ["spring-boot-starter-data-mongodb", "managed", "back end", "MongoTemplate, "
                                                                    "repository proxies, BSON mapping"],
         ["spring-boot-starter-security", "managed", "back end", "Filter chain, password "
                                                                 "encoder, security context"],
         ["spring-boot-starter-test", "managed (test scope)", "back end", "JUnit 5, AssertJ, "
                                                                        "Spring test context"],
         ["java-jwt (Auth0)", "4.5.0", "back end", "HMAC512 signing and verification of "
                                                   "access tokens"],
         ["Lombok", "1.18.38", "back end", "Getters, setters, constructors and builders on "
                                           "documents and DTOs"],
         ["ModelMapper", "3.2.2", "back end", "Mapping between documents and DTOs"],
         ["Angular", "19.2.x", "front end", "Component framework, routing, dependency "
                                            "injection, signals"],
         ["RxJS", "7.8.x", "front end", "Observable HTTP pipelines and operator composition"],
         ["Chart.js", "4.4.9", "front end", "Seven-day weight line chart on the dashboard"],
         ["jwt-decode", "4.0.0", "front end", "Reading the exp claim before use of a token"],
         ["zone.js", "0.15.x", "front end", "Change detection"],
         ["Angular CLI / build-angular", "19.2.x (dev)", "front end", "Build, serve, proxy and "
                                                                     "test harness"],
         ["Karma and Jasmine", "6.4 / 5.6 (dev)", "front end", "Unit-test runner and assertion "
                                                               "library"],
         ["OpenRouter chat-completions API", "v1 (external)", "integration", "Language-model "
                                                                           "inference behind the LLMService interface"]],
        widths=[1.8, 1.15, 0.85, 2.7],
        font_size=7.0,
        caption="Frameworks and libraries with declared versions")

    st += [h2("5.6 Development and Runtime Environment")]
    st += [T.body(
        "Development was carried out on a single workstation with the back end started through "
        "the Maven wrapper and the client through the Angular CLI. The two processes run on "
        "ports 8080 and 4200 respectively; a development proxy rewrites the "
        "<font name='Mono' size='8'>/api</font> prefix so that the browser sees one origin and "
        "the refresh cookie is treated as first-party. MongoDB runs locally on its default "
        "port. Table 5.4 records the configuration values that the runtime expects.")]
    st += table(
        ["Configuration item", "Default in the repository", "Override"],
        [["Server port", "8080 (Spring Boot default)", "server.port"],
         ["MongoDB URI", "mongodb://localhost:27017 (Spring Boot default; the property in "
                         "application.properties is commented out)", "spring.data.mongodb.uri"],
         ["Database name", "macrova (set in MongoConfig through MongoClientSettings)", "Source "
                                                                                      "change"],
         ["JWT signing secret", "Read from the JWT_SECRET environment variable", "Environment"],
         ["Access-token lifetime", "60 minutes (constant in JWTTokenService)", "Source change"],
         ["Refresh-token lifetime", "24 hours (constant in AuthenticationFilter)", "Source "
                                                                                   "change"],
         ["Refresh cookie", "Refresh-Token, HttpOnly, SameSite=Lax, path /", "Source change"],
         ["OpenRouter key", "Read from OPENROUTER_API_KEY", "Environment"],
         ["OpenRouter model", "Read from OPENROUTER_MODEL with a code default", "Environment"],
         ["Allowed client origin", "http://localhost:4200", "Source change (CORS configuration)"],
         ["Client base prefix", "/api (dev proxy target http://localhost:8080)", "proxy.conf.json"]],
        widths=[1.8, 3.1, 1.6],
        font_size=7.1,
        caption="Runtime configuration items and their overrides")
    st += figure(A.tech_stack(), "Technology stack of the delivered system, layer by layer")

    st += [h2("5.7 Summary of the Technology Selection")]
    st += [T.body(
        "The selection was driven by three constraints: zero licence cost, a single language "
        "per tier and a mature ecosystem for the two risky areas, namely security and "
        "document persistence. Spring Boot satisfies the second and third constraints for the "
        "back end because security, JSON binding and Mongo repositories are first-party "
        "starters; Angular satisfies them for the client because routing guards, HTTP "
        "interceptors and typed forms are core features rather than add-ons. Chart.js is the "
        "single third-party visual dependency, chosen because its canvas renderer produces a "
        "small, dependency-free line chart. The language model is deliberately the only "
        "component that depends on a remote service, and it is isolated behind an interface "
        "so that the system remains fully functional when the service is unavailable.")]
    return st
