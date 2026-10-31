"""Preliminary pages: title page, certificate, declaration, acknowledgement,
abstract, table of contents, lists of figures and tables and abbreviations."""

from __future__ import annotations

from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle

import theme as T
from theme import (CONTENT_W, INK, MUTED, TEAL, TEAL_DARK, S, HRule, TOCLine,
                   bullets)

INSTITUTE = "SRM INSTITUTE OF SCIENCE AND TECHNOLOGY"
UNIT = "DIRECTORATE OF DISTANCE EDUCATION"
DEPT = "DEPARTMENT OF COMPUTER APPLICATIONS"
TITLE_L1 = "MACROVA: AN INTELLIGENT DIET,"
TITLE_L2 = "MACRONUTRIENT TRACKING AND"
TITLE_L3 = "AI FOOD RECOMMENDATION SYSTEM"


def _center(text, style="CoverSmall", space=4):
    return [Paragraph(text, S[style]), Spacer(1, space)]


def cover():
    st = []
    st += _center(INSTITUTE, "CoverSub", 2)
    st += _center("(Deemed to be University u/s 3 of UGC Act, 1956)", "CoverSmall", 6)
    st += _center(UNIT, "CoverSub", 2)
    st += _center(DEPT, "CoverSub", 10)
    st.append(HRule(width=CONTENT_W * 0.55, thickness=1.2, color=TEAL, space=16))
    st.append(Spacer(1, 26))
    st += _center(TITLE_L1, "CoverTitle", 2)
    st += _center(TITLE_L2, "CoverTitle", 2)
    st += _center(TITLE_L3, "CoverTitle", 12)
    st += _center("A full-stack web application built with Angular 19, Spring Boot 3.4 and MongoDB",
                  "CoverMeta", 26)
    st.append(Spacer(1, 20))
    st += _center("A PROJECT REPORT SUBMITTED IN PARTIAL FULFILMENT OF THE REQUIREMENTS<br/>"
                  "FOR THE AWARD OF THE DEGREE OF", "CoverMeta", 6)
    st += _center("BACHELOR OF COMPUTER APPLICATIONS", "CoverSub", 24)
    st += _center("Submitted by", "CoverMeta", 4)
    st += _center("<b>KARTHICK S</b>", "CoverMeta", 2)
    st += _center("Register No.: ____________________", "CoverSmall", 24)
    st += _center("Under the guidance of", "CoverMeta", 4)
    st += _center("<b>Dr. A. THIRUMURTHI RAJA</b> M.C.A., M.E., Ph.D.", "CoverMeta", 2)
    st += _center("Assistant Professor, SRMIST-DDE", "CoverSmall", 2)
    st += _center("Department of Computer Applications", "CoverSmall", 26)
    st += _center("ACADEMIC YEAR 2026 \u2013 2027", "CoverSub", 2)
    st += _center("OCTOBER 2026", "CoverSmall", 0)
    return st


def certificate():
    st = T.prelim("BONAFIDE CERTIFICATE")
    st.append(Paragraph(
        "This is to certify that the project report entitled <b>\u201cMACROVA: AN "
        "INTELLIGENT DIET, MACRONUTRIENT TRACKING AND AI FOOD RECOMMENDATION "
        "SYSTEM\u201d</b> is a bonafide record of the project work carried out by "
        "<b>Mr. KARTHICK S, Register No. ______________</b>, a student of the "
        "Department of Computer Applications, Directorate of Distance Education, SRM "
        "Institute of Science and Technology, in partial fulfilment of the requirements "
        "for the award of the degree of <b>Bachelor of Computer Applications</b>, under "
        "my supervision and guidance during the academic year 2026\u20132027.", S["Body"]))
    st.append(Spacer(1, 8))
    st.append(Paragraph(
        "The work reported herein was examined at the review stages and is found to be "
        "original. The source code, database design and documented interface behaviour "
        "were verified against the submitted repository.", S["Body"]))
    st.append(Spacer(1, 30))

    sig = Table(
        [[Paragraph("<b>PROJECT GUIDE</b>", S["TableCell"]),
          Paragraph("<b>HEAD OF THE DEPARTMENT</b>", S["TableCell"])],
         [Paragraph("Dr. A. Thirumurthi Raja<br/>M.C.A., M.E., Ph.D.<br/>"
                    "Assistant Professor, SRMIST-DDE", S["TableCell"]),
          Paragraph("Dr. A. Thirumurthi Raja<br/>Programme Coordinator<br/>"
                    "Department of Computer Applications (DDE), SRMIST", S["TableCell"])]],
        colWidths=[CONTENT_W / 2, CONTENT_W / 2])
    sig.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 16),
        ("TOPPADDING", (0, 0), (-1, 0), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    st.append(sig)
    st.append(Spacer(1, 34))
    exam = Table(
        [[Paragraph("<b>INTERNAL EXAMINER</b>", S["TableCell"]),
          Paragraph("<b>EXTERNAL EXAMINER</b>", S["TableCell"])],
         [Paragraph("_________________________", S["TableCell"]),
          Paragraph("_________________________", S["TableCell"])]],
        colWidths=[CONTENT_W / 2, CONTENT_W / 2])
    exam.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                              ("BOTTOMPADDING", (0, 0), (-1, 0), 22),
                              ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    st.append(exam)
    st.append(Spacer(1, 26))
    st.append(Paragraph("Date: ____________________&nbsp;&nbsp;&nbsp;&nbsp;"
                        "Place: Chennai", S["Body"]))
    return st


def declaration():
    st = T.prelim("DECLARATION")
    st.append(Paragraph(
        "I, <b>KARTHICK S</b> (Register No. ____________________), hereby declare that the "
        "project report entitled <b>\u201cMACROVA: AN INTELLIGENT DIET, MACRONUTRIENT "
        "TRACKING AND AI FOOD RECOMMENDATION SYSTEM\u201d</b> submitted to SRM Institute "
        "of Science and Technology in partial fulfilment of the requirements for the award "
        "of the degree of Bachelor of Computer Applications is a record of original "
        "software engineering work carried out by me under the supervision and guidance of "
        "<b>Dr. A. Thirumurthi Raja</b>, M.C.A., M.E., Ph.D., Assistant Professor, "
        "Department of Computer Applications, Directorate of Distance Education, SRMIST.",
        S["Body"]))
    st.append(Spacer(1, 6))
    st.append(Paragraph(
        "I further declare that every architectural description, database structure, "
        "algorithm, interface rendering and test observation documented in this report was "
        "derived directly from the source repository submitted with the project, and that "
        "this report or any part thereof has not been submitted earlier to any other "
        "University or Institution for the award of any degree, diploma or fellowship.",
        S["Body"]))
    st.append(Spacer(1, 40))
    st.append(Paragraph("KARTHICK S", S["Body"]))
    st.append(Paragraph("(Signature of the Candidate)", S["Small"]))
    st.append(Spacer(1, 20))
    st.append(Paragraph("Date: ____________________&nbsp;&nbsp;&nbsp;&nbsp;Place: Chennai",
                        S["Body"]))
    return st


def acknowledgement():
    st = T.prelim("ACKNOWLEDGEMENT")
    paras = [
        "I express my sincere gratitude to the management of SRM Institute of Science and "
        "Technology for providing the academic environment, laboratory access and library "
        "resources that made this project possible.",
        "I am deeply grateful to <b>Dr. A. Thirumurthi Raja</b>, Programme Coordinator, "
        "BCA/MCA, Directorate of Distance Education, and my project guide, for defining a "
        "rigorous standard for technical documentation, for insisting that every claimed "
        "feature be traceable to source code, and for reviewing the architecture and data "
        "model of this project at every stage.",
        "I thank the faculty members of the Department of Computer Applications for their "
        "comments during the internal reviews, particularly on the nutritional computation "
        "logic and on the security of the session model.",
        "I acknowledge the open-source community whose libraries made this project "
        "practical within a single semester: the Spring Boot and Spring Security projects, "
        "the Angular team, the MongoDB documentation team, and the maintainers of the "
        "Chart.js and java-jwt libraries. The nutrition formulae implemented in this "
        "project follow the published equations of Mifflin and St Jeor and the energy "
        "requirement guidance of the FAO/WHO/UNU expert consultation.",
        "Finally, I thank my family and friends for their patience during the long "
        "debugging sessions that produced the working system documented here.",
    ]
    for p in paras:
        st.append(Paragraph(p, S["Body"]))
        st.append(Spacer(1, 4))
    st.append(Spacer(1, 26))
    st.append(Paragraph("KARTHICK S", S["Body"]))
    return st


def abstract():
    st = T.prelim("ABSTRACT", toc=True)
    st.append(Paragraph(
        "Dietary adherence fails less often because people lack motivation than because "
        "they lack a numeric plan they can act on. A person who wishes to lose eight "
        "kilograms needs three numbers that ordinary fitness applications seldom compute "
        "together: a daily energy budget derived from that individual's own body metrics, "
        "a macronutrient split consistent with that budget, and a per-meal share of the "
        "split that can be compared against what was actually eaten. In practice these "
        "numbers are produced in spreadsheets, copied from generic online calculators, or "
        "estimated by mobile applications that either hide the underlying formula or "
        "present static advice that never changes as the user's weight changes.",
        S["Body"]))
    st.append(Paragraph(
        "<b>Macrova</b> is a web-based diet planning and macronutrient tracking platform "
        "that computes, stores and continuously re-derives these quantities for each "
        "registered user. The system is implemented as a two-tier web application: a "
        "single-page front end built with Angular 19 and TypeScript 5.7, and a stateless "
        "REST back end built with Spring Boot 3.4.4 on Java 21 and persisted in MongoDB. "
        "The back end is organised as a conventional layered Spring application "
        "(controllers, services, repositories and documents) inside the package "
        "<font name='Mono' size='8'>org.karthick.macrova</font>, with dedicated modules "
        "for user identity, diet planning, nutritional computation, and AI-assisted food "
        "recommendation.", S["Body"]))
    st.append(Paragraph(
        "The nutritional engine implements the Mifflin\u2013St Jeor basal metabolic rate "
        "equation, applies activity multipliers from 1.2 to 1.9 to obtain total daily "
        "energy expenditure, derives a calorie target through a goal-dependent deficit or "
        "surplus, splits that target into protein (30 %), fat (30 %) and carbohydrate "
        "(40 %) allocations, and finally apportions the macronutrients across breakfast "
        "(30 %), lunch (30 %), snack (15 %) and dinner (25 %). Every plan is validated "
        "against two independent safety rules: the target weight must correspond to a "
        "healthy body-mass index, and the requested duration must fall inside a window "
        "derived from the mass to be gained or lost, bounded by seven and twenty-eight "
        "days per kilogram.", S["Body"]))
    st.append(Paragraph(
        "A second contribution is the daily tracking model. Each tracking day is stored as "
        "a single self-contained document that embeds the calorie and macronutrient "
        "targets, the values recorded so far, and the per-meal breakdown. Recording a meal "
        "recomputes the daily totals and the calorie deficit server-side, so the dashboard, "
        "the progress screen and the historical archive always display the same derived "
        "figures without any client-side arithmetic. The application also exposes an "
        "AI-assisted meal suggestion feature that forwards a filtered prompt to a large "
        "language model through the OpenRouter inference API, with the calorie budget for "
        "the requested meal taken from the active plan.", S["Body"]))
    st.append(Paragraph(
        "Security is handled with JSON Web Tokens signed using HMAC512. A 60-minute access "
        "token is held only in browser memory, while a 24-hour refresh token is stored in "
        "an HttpOnly, SameSite=Lax cookie; a custom authentication filter, a JWT "
        "authentication filter and a dedicated exception filter form the request-security "
        "pipeline, and passwords are stored as BCrypt digests. The report documents the "
        "requirements, architecture, data-flow and UML models, database design, "
        "implementation of every module with source excerpts, twelve interface renderings, "
        "and a catalogue of functional, security and performance test cases together with "
        "the observed behaviour of the implemented endpoints.", S["Body"]))
    st.append(Spacer(1, 6))
    st.append(Paragraph(
        "<b>Keywords:</b> diet planning, macronutrient tracking, Mifflin\u2013St Jeor "
        "equation, total daily energy expenditure, REST API, Angular 19, Spring Boot 3.4, "
        "MongoDB, JSON Web Token, BCrypt, large language model, OpenRouter.", S["Body"]))
    return st


def toc(entries):
    st = T.prelim("TABLE OF CONTENTS", toc=True)
    st += T.toc_lines(entries)
    st.append(Spacer(1, 10))
    st.append(Paragraph(
        "Page numbers refer to the printed folio shown in the footer of each page; "
        "preliminary pages are numbered in lower-case roman numerals and the main body "
        "starts at page 1 with Chapter 1.", S["Small"]))
    return st


def lof(entries):
    st = T.prelim("LIST OF FIGURES", toc=True)
    if not entries:
        st.append(Paragraph("(figures are listed after the first layout pass)", S["Small"]))
    for label, text, page in entries:
        st.append(TOCLine(f"{label}  {text}", page, level=1, styles=S))
    return st


def lot(entries):
    st = T.prelim("LIST OF TABLES", toc=True)
    if not entries:
        st.append(Paragraph("(tables are listed after the first layout pass)", S["Small"]))
    for label, text, page in entries:
        st.append(TOCLine(f"{label}  {text}", page, level=1, styles=S))
    return st


ABBREVIATIONS = [
    ("AJAX", "Asynchronous JavaScript and XML"),
    ("API", "Application Programming Interface"),
    ("BCrypt", "Blowfish-based adaptive password hashing function"),
    ("BMI", "Body Mass Index (kg/m\u00b2)"),
    ("BMR", "Basal Metabolic Rate (kcal/day)"),
    ("CORS", "Cross-Origin Resource Sharing"),
    ("CRUD", "Create, Read, Update, Delete"),
    ("CSS", "Cascading Style Sheets"),
    ("DFD", "Data Flow Diagram"),
    ("DTO", "Data Transfer Object"),
    ("ER", "Entity\u2013Relationship"),
    ("HMAC", "Hash-based Message Authentication Code"),
    ("HTTP / HTTPS", "HyperText Transfer Protocol / HTTP Secure"),
    ("JSON", "JavaScript Object Notation"),
    ("JSP", "Jakarta Server Pages (not used in this project)"),
    ("JWT", "JSON Web Token (RFC 7519)"),
    ("kcal", "Kilocalorie"),
    ("LLM", "Large Language Model"),
    ("MVC", "Model\u2013View\u2013Controller"),
    ("NoSQL", "Not Only SQL (document database family)"),
    ("NFR / FR", "Non-Functional Requirement / Functional Requirement"),
    ("ORM", "Object\u2013Relational Mapping"),
    ("OWASP", "Open Worldwide Application Security Project"),
    ("PAL", "Physical Activity Level multiplier"),
    ("REST", "Representational State Transfer"),
    ("RBAC", "Role-Based Access Control"),
    ("SDK", "Software Development Kit"),
    ("SPA", "Single-Page Application"),
    ("SRS", "Software Requirements Specification"),
    ("TDEE", "Total Daily Energy Expenditure (kcal/day)"),
    ("UML", "Unified Modeling Language"),
    ("URI / URL", "Uniform Resource Identifier / Locator"),
    ("UAT", "User Acceptance Testing"),
    ("XSS", "Cross-Site Scripting"),
]


def abbreviations():
    st = T.prelim("ABBREVIATIONS AND ACRONYMS", toc=True)
    rows = [[Paragraph(f"<b>{a}</b>", S["TableCell"]), Paragraph(b, S["TableCell"])]
            for a, b in ABBREVIATIONS]
    t = Table(rows, colWidths=[CONTENT_W * 0.26, CONTENT_W * 0.74], repeatRows=0)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, T.RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 2.4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
    ]))
    st.append(t)
    return st
