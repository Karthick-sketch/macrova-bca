"""Chapter 8, references."""

from __future__ import annotations

from reportlab.platypus import Paragraph, Spacer

import theme as T
from theme import S, bullets, chapter, figure, h2, h3, note_box, numbered, table


def build():
    st = []
    st += chapter(8, "CONCLUSION AND FUTURE SCOPE")
    st += [h2("8.1 Summary of the Work")]
    st += [T.body(
        "The project set out to replace a manual diet-planning workflow with a system that "
        "computes, stores and audits nutritional targets. The delivered application, Macrova, is "
        "a two-tier system: an Angular 19 single-page client of eleven routes and a Spring Boot "
        "3.4.4 service of twenty-three handlers persisting to MongoDB across four collections. "
        "It registers users with hashed credentials, issues and refreshes signed tokens, accepts "
        "a validated diet plan, derives energy and macronutrient targets from published "
        "equations, seeds and maintains one tracking document per day, records per-meal intake, "
        "recomputes totals and targets on every change, reports progress through a dashboard "
        "with a seven-day weight trend, archives every plan with its days, and offers "
        "AI-assisted meal suggestions constrained by the selected meal's remaining budget and "
        "three filters.")]
    st += [T.body(
        "The work is documented at three levels. The design is expressed in thirteen diagrams "
        "\u2014 architecture, package, three levels of data flow, use case, class, three "
        "sequence, activity, state and entity-relationship \u2014 supported by data "
        "dictionaries and a query inventory. The implementation is described module by module "
        "with six algorithms in pseudocode and twelve source excerpts. The verification is "
        "recorded as twenty-three unit-level cases, thirty-seven endpoint checks, a "
        "twenty-eight-case acceptance catalogue and a twelve-point security review, with three "
        "worked nutritional profiles recomputed independently.")]

    st += [h2("8.2 Achievement of Objectives")]
    st += table(
        ["Objective", "Outcome", "Evidence in this report"],
        [["O1 Deterministic nutritional engine",
          "Achieved. Mifflin\u2013St Jeor, activity multiplier, goal-adjusted target, 30/30/40 "
          "macro split and 30/30/15/25 meal split are implemented in one stateless class.",
          "Sections 6.2.4, 6.4.1\u20136.4.3; Tables 7.3, 7.4"],
         ["O2 Safe plan validation",
          "Achieved. Body-mass index and a derived duration window are enforced on the server, "
          "with the permitted range returned in the message.",
          "Sections 6.3.2, 6.4.4; AT-09, AT-10"],
         ["O3 Daily tracking model",
          "Achieved. One self-contained document per day, created on demand, with total "
          "recomputation on every write.",
          "Sections 6.2.5, 6.3.3, 6.3.4; AT-12, AT-13, AT-17"],
         ["O4 Aggregate progress reporting",
          "Achieved. One metrics resource carries title, elapsed day, duration, weight, targets "
          "and the seven-day series.",
          "Sections 6.3.5, 6.4.7; AT-15"],
         ["O5 Plan lifecycle",
          "Achieved. One active plan per user, automatic retirement after the duration, "
          "projected history and cloning of a past plan.",
          "Sections 6.2.6, 4.5.4; AT-18 to AT-22"],
         ["O6 Token-based security",
          "Achieved with two recorded deviations: the development cookie omits Secure, and "
          "there is no rate limiting on the authentication endpoint.",
          "Sections 6.2.2, 6.4.8, 6.4.9; Table 7.7"],
         ["O7 AI-assisted suggestions",
          "Achieved. A schema-fixed prompt, a temperature of 0.3, typed parsing and an explicit "
          "410 error state.",
          "Sections 6.2.7, 6.3.6, 6.4.10; AT-23 to AT-25"],
         ["O8 Responsive interface",
          "Achieved. Eleven routes, four guarded, two interceptors, a design-token stylesheet "
          "and a charted progress view.",
          "Sections 6.2.9, 6.5; Table 7.8"]],
        widths=[1.5, 3.0, 1.9],
        font_size=7.0,
        caption="Traceability of objectives to delivered capability and evidence")

    st += [h2("8.3 Limitations of the Present Work")]
    st += bullets([
        "<b>Automated testing.</b> The repository contains one context-load test. Every other "
        "result in Chapter 7 was obtained manually and is not re-executed on change. This is the "
        "most consequential limitation of the release.",
        "<b>Single-instance assumptions.</b> The service is stateless, but the refresh strategy "
        "assumes a single signing secret and no revocation list, so a compromised token remains "
        "valid until expiry.",
        "<b>Index management.</b> No index is declared on "
        "<font name='Mono' size='8'>diet_plan_tracks</font>; the range query relies on a "
        "collection scan bounded by the plan.",
        "<b>Estimation error.</b> The energy model inherits the error of predictive equations, "
        "which the literature puts at roughly ten per cent for an individual [2], and to which "
        "under-reporting of intake adds a systematic bias [6]. The application "
        "presents its outputs as arithmetic guidance, not as measurement.",
        "<b>Dependence on a single inference provider.</b> The abstraction allows replacement, "
        "but only one implementation exists, and prompt behaviour is model-specific.",
        "<b>No localisation and no accessibility audit.</b> The interface is English-only and "
        "has not been tested with a screen reader, although the markup uses semantic elements "
        "and labelled controls.",
        "<b>Cookie scope.</b> The refresh cookie is scoped to the path root and not to the "
        "refresh endpoint specifically, which is broader than necessary.",
    ])

    st += [h2("8.4 Future Scope")]
    st += numbered([
        "<b>Automated test suite.</b> Promote the twenty-three unit cases and the "
        "thirty-seven endpoint checks into JUnit 5 tests against an embedded or containerised "
        "MongoDB, add component tests for the four stateful screens, and gate the build on "
        "coverage of the utility class.",
        "<b>Indexing and archival.</b> Declare a compound index on "
        "(<font name='Mono' size='8'>dietPlanId</font>, "
        "<font name='Mono' size='8'>createdAt</font>) and a unique index on "
        "<font name='Mono' size='8'>username</font> and "
        "<font name='Mono' size='8'>email</font>, and move tracking documents older than a "
        "completed plan into a cold collection.",
        "<b>Refresh-token rotation and revocation.</b> Rotate the refresh token on every use, "
        "record a token family identifier, and revoke the family on reuse, which closes the "
        "theft window that a static refresh token leaves open.",
        "<b>Rate limiting and lockout.</b> Apply a per-address and per-account limit to "
        "<font name='Mono' size='8'>/authenticate</font> and add an incremental delay after "
        "repeated failures.",
        "<b>Food database integration.</b> Replace free-text meal entry with a search over a "
        "nutrition database so that grams are derived from portions rather than estimated.",
        "<b>Photographic estimation.</b> Accept a meal photograph, estimate portion sizes with a "
        "vision model and pre-fill the meal card for user confirmation.",
        "<b>Wearable ingestion.</b> Replace the activity multiplier with measured step counts "
        "and heart-rate-derived expenditure, which would reduce the dominant error term.",
        "<b>Longitudinal analytics.</b> Add a monthly view with adherence percentages, a moving "
        "average of weight, and a projection of the target date from the observed rate.",
        "<b>Multi-language support and accessibility conformance.</b> Extract interface strings "
        "into a translation catalogue and audit the client against WCAG 2.2 level AA, including "
        "a keyboard-only and screen-reader pass.",
        "<b>Deployment hardening.</b> Terminate TLS in front of the service, enable the Secure "
        "and SameSite=Strict attributes, externalise every secret, and add structured logging "
        "with a correlation identifier per request.",
    ])

    st += [h2("8.5 Conclusion")]
    st += [T.body(
        "Macrova demonstrates that a domain as small as diet planning still repays disciplined "
        "engineering. The arithmetic could have been written in a controller and the plan stored "
        "as a flat record; instead the equations live in one class whose every branch is "
        "reproducible by hand, the derived values live beside the inputs that produced them, and "
        "the ownership of every document is decided by the authenticated principal rather than "
        "by the request. The result is a system whose numbers can be audited, whose history "
        "cannot be rewritten by a later plan, and whose failure modes are explicit \u2014 400 for "
        "an unsafe goal, 404 for a foreign identifier, 401 for a stale token, 410 for a "
        "malformed model reply.")]
    st += [T.body(
        "The project also shows where the boundary of a single-semester effort lies. The design "
        "and the manual verification are complete; the automated regression suite, the index "
        "declarations and the production hardening of the cookie are not. Naming those gaps "
        "precisely, rather than claiming a finished product, is part of the same discipline that "
        "produced the rest of the system: a report of what was built should be as auditable as "
        "the arithmetic inside it.")]
    return st


# ---------------------------------------------------------------------------
# References
# ---------------------------------------------------------------------------
REFS = [
    "M. D. Mifflin, S. T. St Jeor, L. A. Hill, B. J. Scott, S. A. Daugherty and Y. O. Koh, "
    "\u201cA new predictive equation for resting energy expenditure in healthy individuals,\u201d "
    "<i>The American Journal of Clinical Nutrition</i>, vol. 51, no. 2, pp. 241\u2013247, 1990.",
    "J. Frankenfield, L. Roth-Yousey and C. Compher, \u201cComparison of predictive equations "
    "for resting metabolic rate in healthy non-obese and obese adults: a systematic review,\u201d "
    "<i>Journal of the American Dietetic Association</i>, vol. 105, no. 5, pp. 775\u2013789, 2005.",
    "Food and Agriculture Organization, World Health Organization and United Nations University, "
    "<i>Human Energy Requirements: Report of a Joint FAO/WHO/UNU Expert Consultation</i>, FAO Food "
    "and Nutrition Technical Report Series 1, Rome, 2004.",
    "A. Keys, F. Fidanza, M. J. Karvonen, N. Kimura and H. L. Taylor, \u201cIndices of relative "
    "weight and obesity,\u201d <i>Journal of Chronic Diseases</i>, vol. 25, no. 6, "
    "pp. 329\u2013343, 1972.",
    "B. E. Ainsworth, W. L. Haskell, S. D. Herrmann, N. Meckes, D. R. Bassett, C. Tudor-Locke "
    "et al., \u201c2011 Compendium of Physical Activities: a second update of codes and MET "
    "values,\u201d <i>Medicine and Science in Sports and Exercise</i>, vol. 43, no. 8, "
    "pp. 1575\u20131581, 2011.",
    "L. A. Goldberg, R. A. S. Black and S. A. Jebb, \u201cCritical evaluation of energy intake "
    "data using fundamental principles of energy physiology,\u201d <i>European Journal of "
    "Clinical Nutrition</i>, vol. 45, no. 12, pp. 569\u2013581, 1991.",
    "M. Jones, J. Bradley and N. Sakimura, \u201cJSON Web Token (JWT),\u201d RFC 7519, Internet "
    "Engineering Task Force, 2015.",
    "D. Hardt, Ed., \u201cThe OAuth 2.0 Authorization Framework,\u201d RFC 6749, Internet "
    "Engineering Task Force, 2012.",
    "OWASP Foundation, <i>OWASP Application Security Verification Standard 4.0.3</i>, 2021.",
    "R. T. Fielding, \u201cArchitectural Styles and the Design of Network-based Software "
    "Architectures,\u201d Ph.D. dissertation, University of California, Irvine, 2000.",
    "M. Fowler, <i>Patterns of Enterprise Application Architecture</i>. Boston, MA: "
    "Addison-Wesley, 2002.",
    "M. Kleppmann, <i>Designing Data-Intensive Applications</i>. Sebastopol, CA: O\u2019Reilly "
    "Media, 2017.",
    "J. Nielsen, \u201cEnhancing the explanatory power of usability heuristics,\u201d in "
    "<i>Proceedings of the ACM CHI Conference on Human Factors in Computing Systems</i>, 1994, "
    "pp. 152\u2013158.",
    "I. Sommerville, <i>Software Engineering</i>, 10th ed. Boston, MA: Pearson, 2016.",
    "R. Elmasri and S. B. Navathe, <i>Fundamentals of Database Systems</i>, 7th ed. Boston, MA: "
    "Pearson, 2016.",
    "Broadcom Inc., <i>Spring Boot Reference Documentation</i>, version 3.4.4, 2025. [Online]. "
    "Available: https://docs.spring.io/spring-boot/",
    "Google LLC, <i>Angular Documentation</i>, version 19, 2025. [Online]. "
    "Available: https://angular.dev/",
    "MongoDB Inc., <i>MongoDB Manual</i>, version 7.0, 2025. [Online]. "
    "Available: https://www.mongodb.com/docs/manual/",
]


def references():
    st = list(T.prelim("REFERENCES", toc=True, level=0))
    for i, r in enumerate(REFS, start=1):
        st.append(Paragraph(f"[{i}]&nbsp;&nbsp;{r}", S["Ref"]))
        st.append(Spacer(1, 2.4))
    return st
