"""
generate_pdf.py
-------------------------------------------------------------------------------
Generates a comprehensive, professional PDF technical documentation
and interview preparation guide for the CycleCare web application.
Uses ReportLab 4.5.1.
-------------------------------------------------------------------------------
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

PDF_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "CycleCare_Interview_Technical_Documentation.pdf")


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print 'Page X of Y' page numbers
    and a clean running header.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Suppress header and footer on cover page
        if self._pageNumber > 1:
            # Header
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(54, 11 * inch - 36, "CycleCare — Technical Documentation & Interview Preparation Guide")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

            # Footer
            self.line(54, 46, 8.5 * inch - 54, 46)
            self.setFont("Helvetica", 8)
            self.drawString(54, 34, "Confidential & Educational Project Reference • Python Flask & MySQL")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(8.5 * inch - 54, 34, page_text)
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    c_primary = colors.HexColor("#be123c")     # Rose/Crimson
    c_secondary = colors.HexColor("#0f172a")   # Dark Navy/Slate
    c_muted = colors.HexColor("#475569")       # Muted Slate
    c_bg_light = colors.HexColor("#fff1f2")    # Soft Red Tint
    c_border = colors.HexColor("#fecdd3")

    # Typography Styles
    style_cover_title = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=26,
        leading=32,
        textColor=c_primary,
        alignment=1, # Center
        spaceAfter=12
    )
    style_cover_sub = ParagraphStyle(
        "CoverSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=c_muted,
        alignment=1,
        spaceAfter=24
    )
    style_h1 = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=c_primary,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )
    style_h2 = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    style_h3 = ParagraphStyle(
        "Heading3_Custom",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    style_body = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=c_secondary,
        spaceAfter=6
    )
    style_body_bold = ParagraphStyle(
        "Body_Bold",
        parent=style_body,
        fontName="Helvetica-Bold"
    )
    style_bullet = ParagraphStyle(
        "Bullet_Custom",
        parent=style_body,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4
    )
    style_code = ParagraphStyle(
        "Code_Custom",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=4,
        spaceAfter=6
    )
    style_table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=c_secondary
    )
    style_table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    story = []

    # -------------------------------------------------------------------------
    # COVER / TITLE PAGE
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("🌸 CycleCare", style_cover_title))
    story.append(Paragraph("Full-Stack Menstrual Health Tracking Web Application", style_cover_title))
    story.append(Paragraph("Deep Technical Documentation & Fresher Interview Preparation Guide", style_cover_sub))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=10, spaceAfter=20))

    disclaimer_box = [
        [Paragraph("<b>⚠️ Important Educational & Medical Notice</b><br/>"
                   "CycleCare is engineered as an educational full-stack demonstration. All cycle forecasts "
                   "and upcoming dates are <b>transparent mathematical estimations based on past logged averages</b>. "
                   "CycleCare is <b>NOT a medical device</b> and does not offer clinical diagnosis, treatment, "
                   "or contraceptive advice.", style_body)]
    ]
    t_disc = Table(disclaimer_box, colWidths=[504])
    t_disc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#fff1f2")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#f43f5e")),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_disc)
    story.append(Spacer(1, 20))

    meta_table_data = [
        [Paragraph("<b>Author Role:</b> Full-Stack Web Developer (Fresher)", style_table_cell),
         Paragraph("<b>Architecture:</b> Multi-Tier Client-Server REST", style_table_cell)],
        [Paragraph("<b>Frontend:</b> HTML5, CSS3, Vanilla JS", style_table_cell),
         Paragraph("<b>Backend:</b> Python 3.14, Flask 3.1", style_table_cell)],
        [Paragraph("<b>Database:</b> MySQL 8.0+ / PyMySQL (with SQLite fallback)", style_table_cell),
         Paragraph("<b>Security:</b> PBKDF2/SHA-256, Session Cookies, SQL Parameterization", style_table_cell)]
    ]
    t_meta = Table(meta_table_data, colWidths=[252, 252])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_meta)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PART 1: PROJECT OVERVIEW
    # -------------------------------------------------------------------------
    story.append(Paragraph("PART 1 — Project Overview", style_h1))
    story.append(Paragraph("<b>1. What is CycleCare?</b> A beginner-to-intermediate full-stack menstrual health web application enabling users to log cycle dates, track durations, review cycle history, visualize period days on an interactive calendar highlighted in red, and view mathematically estimated upcoming period dates.", style_body))
    story.append(Paragraph("<b>2. What problem does it solve?</b> Solves the difficulty of tracking menstrual patterns without relying on bloated, ad-heavy commercial apps with paywalls or obscure proprietary 'AI' algorithms. Provides transparency, data privacy, and complete CRUD control.", style_body))
    story.append(Paragraph("<b>3. Target User:</b> Anyone seeking a private, accessible, and simple tool to track their menstrual rhythm.", style_body))
    story.append(Paragraph("<b>4. Major Features:</b>", style_body))
    story.append(Paragraph("• <b>User Authentication & Authorization:</b> Encrypted passwords (PBKDF2/SHA-256), session cookies, and strict data isolation.", style_bullet))
    story.append(Paragraph("• <b>Cycle CRUD:</b> Log, view, edit, and delete cycle entries with start/end dates, period duration, cycle length, and notes.", style_bullet))
    story.append(Paragraph("• <b>Estimation Engine:</b> Transparent calculation: <i>Estimated Next Period = Latest Start Date + Average Cycle Length</i>.", style_bullet))
    story.append(Paragraph("• <b>Interactive Calendar:</b> Pure vanilla JS calendar mapping period days highlighted in <b>vibrant red</b> and projecting upcoming cycles.", style_bullet))
    story.append(Paragraph("• <b>Educational Medical Disclaimer:</b> Clearly disclaims medical diagnosis across all views.", style_bullet))

    story.append(Paragraph("<b>5. Technology Stack & Selection Justification:</b>", style_body))
    story.append(Paragraph("• <b>HTML5 & CSS3:</b> Semantic markup and custom styling using Flexbox and CSS Grid without framework overhead.", style_bullet))
    story.append(Paragraph("• <b>Vanilla JavaScript:</b> Masters native browser DOM events, async <code>fetch()</code> requests, and date math.", style_bullet))
    story.append(Paragraph("• <b>Python Flask:</b> Lightweight WSGI micro-framework showcasing routing, blueprints, and request lifecycles transparently.", style_bullet))
    story.append(Paragraph("• <b>MySQL:</b> Relational database enforcing ACID transactions, data types, and foreign key cascades.", style_bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Architecture Flow:</b>", style_h2))
    story.append(Paragraph("<code>USER → Frontend (HTML/CSS/JS) → HTTP Request (fetch JSON) → Flask API → Business Logic → MySQL (Parameterized SQL) → Response JSON → DOM Updated</code>", style_code))

    # -------------------------------------------------------------------------
    # PART 2: COMPLETE FOLDER STRUCTURE
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("PART 2 — Complete Folder Structure", style_h1))
    story.append(Paragraph("The codebase in <code>d:/cyclecare</code> is organized cleanly by architectural concern:", style_body))

    structure_data = [
        [Paragraph("<b>File / Folder</b>", style_table_header),
         Paragraph("<b>Type</b>", style_table_header),
         Paragraph("<b>Architectural Responsibility</b>", style_table_header)],
        [Paragraph("<code>app.py</code>", style_table_cell), Paragraph("Backend", style_table_cell), Paragraph("Flask entry point, blueprint registration, HTML view routes, error handlers.", style_table_cell)],
        [Paragraph("<code>database/db.py</code>", style_table_cell), Paragraph("Database", style_table_cell), Paragraph("PyMySQL connection manager, auto-init, parameterized query wrappers, SQLite fallback.", style_table_cell)],
        [Paragraph("<code>database/schema.sql</code>", style_table_cell), Paragraph("Database DDL", style_table_cell), Paragraph("Standard MySQL DDL definitions for `users` and `cycles` tables, FKs, indexes.", style_table_cell)],
        [Paragraph("<code>routes/auth.py</code>", style_table_cell), Paragraph("Backend API", style_table_cell), Paragraph("User registration, login, logout, password hashing, `@login_required` decorator.", style_table_cell)],
        [Paragraph("<code>routes/cycles.py</code>", style_table_cell), Paragraph("Backend API", style_table_cell), Paragraph("Full REST CRUD endpoints (`GET`, `POST`, `PUT`, `DELETE` /api/cycles) with ownership checks.", style_table_cell)],
        [Paragraph("<code>routes/dashboard.py</code>", style_table_cell), Paragraph("Backend API", style_table_cell), Paragraph("Dashboard statistics aggregation and cycle estimation calculation engine.", style_table_cell)],
        [Paragraph("<code>templates/*.html</code>", style_table_cell), Paragraph("Frontend View", style_table_cell), Paragraph("HTML5 templates: `index.html`, `register.html`, `login.html`, `dashboard.html`, `history.html`.", style_table_cell)],
        [Paragraph("<code>static/css/style.css</code>", style_table_cell), Paragraph("Frontend Style", style_table_cell), Paragraph("Responsive CSS3 design system, calming light red theme, and red calendar period cells.", style_table_cell)],
        [Paragraph("<code>static/js/auth.js</code>", style_table_cell), Paragraph("Frontend Logic", style_table_cell), Paragraph("Client-side validation and async `fetch()` calls for register and login forms.", style_table_cell)],
        [Paragraph("<code>static/js/cycles.js</code>", style_table_cell), Paragraph("Frontend Logic", style_table_cell), Paragraph("Cycle modal management, date math synchronization, CRUD requests, and delete modal.", style_table_cell)],
        [Paragraph("<code>static/js/dashboard.js</code>", style_table_cell), Paragraph("Frontend Logic", style_table_cell), Paragraph("Consumes `/api/dashboard`, populates stat cards, countdown tags, and initiates calendar.", style_table_cell)],
        [Paragraph("<code>static/js/calendar.js</code>", style_table_cell), Paragraph("Frontend Logic", style_table_cell), Paragraph("Generates monthly calendar grid, highlights period days in RED, and handles date clicks.", style_table_cell)],
        [Paragraph("<code>test_app.py</code>", style_table_cell), Paragraph("Backend Utility", style_table_cell), Paragraph("Automated `unittest` test suite covering registration, auth, CRUD, and estimations.", style_table_cell)]
    ]
    t_struct = Table(structure_data, colWidths=[120, 74, 310])
    t_struct.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_struct)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PART 3 & 4: EXECUTION FLOW & FRONTEND
    # -------------------------------------------------------------------------
    story.append(Paragraph("PART 3 — End-to-End Execution Flow", style_h1))
    story.append(Paragraph("When an interviewer asks: <i>'What happens technically when a user interacts with your website?'</i>, summarize this exact pipeline:", style_body))
    story.append(Paragraph("1. <b>Browser Request:</b> User types <code>http://localhost:5000</code>. Browser fires HTTP <code>GET /</code>.<br/>"
                           "2. <b>Routing & Template:</b> Flask's <code>app.py</code> renders <code>templates/index.html</code>.<br/>"
                           "3. <b>CSS Parsing:</b> Browser fetches <code>static/css/style.css</code> and builds the Render Tree.<br/>"
                           "4. <b>Action:</b> User navigates to <code>/login</code>, enters credentials, and clicks 'Log In'.<br/>"
                           "5. <b>Client Interception:</b> <code>auth.js</code> stops page reload via <code>e.preventDefault()</code> and validates input.<br/>"
                           "6. <b>Asynchronous Call:</b> <code>fetch('/api/login', {method: 'POST', body: JSON})</code> is dispatched.<br/>"
                           "7. <b>Server Verification:</b> Flask queries MySQL for email, compares PBKDF2 hash with <code>check_password_hash</code>, and sets session cookie.<br/>"
                           "8. <b>DOM Update:</b> <code>auth.js</code> receives HTTP 200, displays a green toast, and redirects to <code>/dashboard</code>.<br/>"
                           "9. <b>Dashboard & Calendar:</b> <code>dashboard.js</code> fetches <code>/api/dashboard</code>; <code>calendar.js</code> renders the month grid with period days highlighted in red.", style_body))

    story.append(Spacer(1, 10))
    story.append(Paragraph("PART 4 — Frontend Architecture (HTML, CSS, JS)", style_h1))
    story.append(Paragraph("• <b>Semantic HTML:</b> Accessible forms with <code>&lt;label for&gt;</code>, ARIA-friendly modals with close handlers, and table views.<br/>"
                           "• <b>CSS Grid & Flexbox:</b> Flexbox handles navigation and modal alignment; CSS Grid manages stat cards (<code>repeat(auto-fit, minmax(220px, 1fr))</code>) and the strict 7-day calendar grid (<code>repeat(7, 1fr)</code>).<br/>"
                           "• <b>Red Period Highlights:</b> Logged period days are styled with: <code>background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: #fff; box-shadow: 0 4px 10px rgba(220, 38, 38, 0.28);</code>.<br/>"
                           "• <b>Vanilla JavaScript:</b> Uses async/await with <code>fetch()</code>, DOM manipulation via <code>innerHTML</code> and class toggles, and client-side regex.", style_body))

    # -------------------------------------------------------------------------
    # PART 5: ALL WEB CALLS & REST API ENDPOINTS
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("PART 5 — REST API Endpoints Specification", style_h1))
    story.append(Paragraph("Every endpoint in CycleCare receives and returns standard <code>application/json</code> payloads:", style_body))

    api_table_data = [
        [Paragraph("<b>Action</b>", style_table_header),
         Paragraph("<b>Method</b>", style_table_header),
         Paragraph("<b>Endpoint</b>", style_table_header),
         Paragraph("<b>Database Operation</b>", style_table_header),
         Paragraph("<b>Code</b>", style_table_header)],
        [Paragraph("User Register", style_table_cell), Paragraph("POST", style_table_cell), Paragraph("<code>/api/register</code>", style_table_cell), Paragraph("INSERT INTO users", style_table_cell), Paragraph("201", style_table_cell)],
        [Paragraph("User Login", style_table_cell), Paragraph("POST", style_table_cell), Paragraph("<code>/api/login</code>", style_table_cell), Paragraph("SELECT FROM users WHERE email", style_table_cell), Paragraph("200", style_table_cell)],
        [Paragraph("User Logout", style_table_cell), Paragraph("POST", style_table_cell), Paragraph("<code>/api/logout</code>", style_table_cell), Paragraph("Clears session cookie", style_table_cell), Paragraph("200", style_table_cell)],
        [Paragraph("Get Profile", style_table_cell), Paragraph("GET", style_table_cell), Paragraph("<code>/api/me</code>", style_table_cell), Paragraph("Reads session['user_id']", style_table_cell), Paragraph("200", style_table_cell)],
        [Paragraph("Dashboard Data", style_table_cell), Paragraph("GET", style_table_cell), Paragraph("<code>/api/dashboard</code>", style_table_cell), Paragraph("SELECT FROM cycles WHERE user_id", style_table_cell), Paragraph("200", style_table_cell)],
        [Paragraph("List Cycles", style_table_cell), Paragraph("GET", style_table_cell), Paragraph("<code>/api/cycles</code>", style_table_cell), Paragraph("SELECT FROM cycles WHERE user_id", style_table_cell), Paragraph("200", style_table_cell)],
        [Paragraph("Get Single Cycle", style_table_cell), Paragraph("GET", style_table_cell), Paragraph("<code>/api/cycles/&lt;id&gt;</code>", style_table_cell), Paragraph("SELECT FROM cycles WHERE id", style_table_cell), Paragraph("200", style_table_cell)],
        [Paragraph("Create Cycle", style_table_cell), Paragraph("POST", style_table_cell), Paragraph("<code>/api/cycles</code>", style_table_cell), Paragraph("INSERT INTO cycles", style_table_cell), Paragraph("201", style_table_cell)],
        [Paragraph("Update Cycle", style_table_cell), Paragraph("PUT", style_table_cell), Paragraph("<code>/api/cycles/&lt;id&gt;</code>", style_table_cell), Paragraph("UPDATE cycles WHERE id, user_id", style_table_cell), Paragraph("200", style_table_cell)],
        [Paragraph("Delete Cycle", style_table_cell), Paragraph("DELETE", style_table_cell), Paragraph("<code>/api/cycles/&lt;id&gt;</code>", style_table_cell), Paragraph("DELETE FROM cycles WHERE id, user_id", style_table_cell), Paragraph("200", style_table_cell)]
    ]
    t_api = Table(api_table_data, colWidths=[90, 48, 110, 210, 46])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_api)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PART 6 & 7: AUTH & DATABASE
    # -------------------------------------------------------------------------
    story.append(Paragraph("PART 6 — Authentication vs. Authorization", style_h1))
    story.append(Paragraph("• <b>Authentication ('Who are you?'):</b> Verifying a user's identity. In CycleCare, the user sends their email and password; <code>check_password_hash()</code> verifies the credentials against the salted PBKDF2 hash. If valid, Flask sets <code>session['user_id'] = user['id']</code>.", style_body))
    story.append(Paragraph("• <b>Authorization ('What are you allowed to do?'):</b> Checking permissions on specific resources. In CycleCare, User A (ID: 1) is logged in. If User A tries to edit cycle `#42` which belongs to User B (ID: 2), <code>routes/cycles.py</code> checks: <code>if existing['user_id'] != session['user_id']: return 403 Forbidden</code>. User A is authenticated, but <b>unauthorized</b> to touch User B's record.", style_body))
    story.append(Paragraph("• <b>Password Hashing:</b> Passwords are never stored in plain text. Werkzeug generates a random cryptographic salt and hashes the password with PBKDF2/SHA-256 (e.g., <code>pbkdf2:sha256:1000000$salt$hash</code>).", style_body))

    story.append(Spacer(1, 10))
    story.append(Paragraph("PART 7 — Database Schema & Relational Integrity", style_h1))
    story.append(Paragraph("CycleCare uses a normalized relational model with two tables in MySQL (with automated SQLite fallback):", style_body))

    db_table_data = [
        [Paragraph("<b>Table: users</b>", style_table_header), Paragraph("<b>Data Type & Constraints</b>", style_table_header), Paragraph("<b>Purpose</b>", style_table_header)],
        [Paragraph("<code>id</code>", style_table_cell), Paragraph("INT AUTO_INCREMENT PRIMARY KEY", style_table_cell), Paragraph("Unique user identifier.", style_table_cell)],
        [Paragraph("<code>name</code>", style_table_cell), Paragraph("VARCHAR(100) NOT NULL", style_table_cell), Paragraph("Display name of user.", style_table_cell)],
        [Paragraph("<code>email</code>", style_table_cell), Paragraph("VARCHAR(150) NOT NULL UNIQUE, INDEX", style_table_cell), Paragraph("Unique user login email address.", style_table_cell)],
        [Paragraph("<code>password_hash</code>", style_table_cell), Paragraph("VARCHAR(255) NOT NULL", style_table_cell), Paragraph("Salted PBKDF2/SHA-256 cryptographic hash.", style_table_cell)],
        [Paragraph("<code>created_at</code>", style_table_cell), Paragraph("TIMESTAMP DEFAULT CURRENT_TIMESTAMP", style_table_cell), Paragraph("Account creation timestamp.", style_table_cell)],
        [Paragraph("<b>Table: cycles</b>", style_table_header), Paragraph("<b>Data Type & Constraints</b>", style_table_header), Paragraph("<b>Purpose</b>", style_table_header)],
        [Paragraph("<code>id</code>", style_table_cell), Paragraph("INT AUTO_INCREMENT PRIMARY KEY", style_table_cell), Paragraph("Unique cycle entry ID.", style_table_cell)],
        [Paragraph("<code>user_id</code>", style_table_cell), Paragraph("INT NOT NULL, FK -> users(id) ON DELETE CASCADE", style_table_cell), Paragraph("Foreign key enforcing referential ownership.", style_table_cell)],
        [Paragraph("<code>start_date</code>", style_table_cell), Paragraph("DATE NOT NULL", style_table_cell), Paragraph("First bleeding day of menstrual cycle.", style_table_cell)],
        [Paragraph("<code>end_date</code>", style_table_cell), Paragraph("DATE NULL", style_table_cell), Paragraph("Final bleeding day of cycle.", style_table_cell)],
        [Paragraph("<code>period_duration</code>", style_table_cell), Paragraph("INT NOT NULL", style_table_cell), Paragraph("Length of period bleeding (e.g., 5 days).", style_table_cell)],
        [Paragraph("<code>cycle_length</code>", style_table_cell), Paragraph("INT NOT NULL", style_table_cell), Paragraph("Days from this start date to next start (default 28).", style_table_cell)],
        [Paragraph("<code>notes</code>", style_table_cell), Paragraph("TEXT NULL", style_table_cell), Paragraph("Optional symptom, cramp, and flow notes.", style_table_cell)],
        [Paragraph("<code>created_at</code>", style_table_cell), Paragraph("TIMESTAMP DEFAULT CURRENT_TIMESTAMP", style_table_cell), Paragraph("Log timestamp (indexed with user_id).", style_table_cell)]
    ]
    t_db = Table(db_table_data, colWidths=[110, 204, 190])
    t_db.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BACKGROUND', (0, 6), (-1, 6), c_primary),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_db)

    # -------------------------------------------------------------------------
    # PART 8 & 9: CRUD & ESTIMATION LOGIC
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("PART 8 & 9 — CRUD Implementation & Cycle Estimation Logic", style_h1))
    story.append(Paragraph("<b>Cycle Estimation Formula:</b>", style_h2))
    story.append(Paragraph("CycleCare calculates the upcoming period date transparently using historical averages:", style_body))
    story.append(Paragraph("$$\\text{Estimated Next Period} = \\text{Latest Period Start Date} + \\text{Average Cycle Length}$$", style_code))
    story.append(Paragraph("• <b>Average Calculation:</b> If a user has logged cycle lengths of 28, 29, 27, and 28 days:<br/>"
                           "$$\\text{Average Cycle Length} = (28 + 29 + 27 + 28) / 4 = 28\\text{ days}$$<br/>"
                           "• <b>Upcoming Date Projection:</b> If the latest period started on <b>September 29, 2026</b>:<br/>"
                           "$$\\text{Estimated Date} = \\text{September 29, 2026} + 28\\text{ days} = \\text{October 27, 2026}$$<br/>"
                           "• <b>Days Countdown:</b> $\\text{Days} = \\text{Estimated Date} - \\text{Today's Date}$. Displays: <b>In ~20 days</b>.<br/>"
                           "• <b>Data Categorization:</b> Actual logged data (start/end dates) vs. Calculated data (averages) vs. Estimated data (forecast).", style_body))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PART 10 & 11: HTTP CONCEPTS & SECURITY
    # -------------------------------------------------------------------------
    story.append(Paragraph("PART 10 & 11 — HTTP & REST Concepts", style_h1))
    story.append(Paragraph("• <b>HTTP (HyperText Transfer Protocol):</b> Stateless protocol governing client-server communication.<br/>"
                           "• <b>GET vs. POST vs. PUT vs. DELETE:</b><br/>"
                           "  - <code>GET</code>: Safe & idempotent; retrieves data without modifying server state (e.g., <code>GET /api/cycles</code>).<br/>"
                           "  - <code>POST</code>: Submits data to create a new resource (e.g., <code>POST /api/cycles</code>).<br/>"
                           "  - <code>PUT</code>: Idempotent update; modifies an existing identified resource (e.g., <code>PUT /api/cycles/5</code>).<br/>"
                           "  - <code>DELETE</code>: Removes an existing resource by identifier (e.g., <code>DELETE /api/cycles/5</code>).<br/>"
                           "• <b>HTTP Status Codes Used:</b> <code>200 OK</code>, <code>201 Created</code>, <code>400 Bad Request</code>, <code>401 Unauthorized</code>, <code>403 Forbidden</code>, <code>404 Not Found</code>, <code>500 Server Error</code>.", style_body))

    story.append(Spacer(1, 10))
    story.append(Paragraph("PART 12 & 13 — Security Analysis & Defenses", style_h1))
    story.append(Paragraph("<b>Implemented Security Defenses:</b><br/>"
                           "1. <b>SQL Injection Prevention:</b> All queries use parameterized placeholders (<code>%s</code>) and tuple arguments. User inputs are never concatenated directly into SQL strings.<br/>"
                           "2. <b>Password Hashing:</b> Uses PBKDF2/SHA-256 with unique cryptographic salts via Werkzeug.<br/>"
                           "3. <b>IDOR Prevention & Data Isolation:</b> Every database mutation verifies <code>WHERE id = %s AND user_id = %s</code> and checks <code>record['user_id'] == session['user_id']</code>.<br/>"
                           "4. <b>XSS Sanitization:</b> Client-side <code>escapeHtml()</code> sanitizes user-entered cycle notes before rendering.<br/>"
                           "5. <b>Environment Secrets:</b> Database credentials and Flask <code>SECRET_KEY</code> are loaded from <code>.env</code> via <code>python-dotenv</code>.", style_body))
    story.append(Paragraph("<b>Candidly Identified Weaknesses (Interview Talking Points):</b><br/>"
                           "• <b>Rate Limiting:</b> No brute-force rate limiter currently on <code>/api/login</code> (in production, add <code>Flask-Limiter</code>).<br/>"
                           "• <b>CSRF Tokens:</b> JSON requests rely on content-type headers; adding <code>Flask-WTF</code> CSRF tokens would strengthen form protection.", style_body))

    # -------------------------------------------------------------------------
    # PART 14 & 15: INTERVIEW QUESTIONS BY LEVEL
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("PART 15 — Interview Questions & Model Answers", style_h1))

    qa_list = [
        ("Level 1: What is CycleCare?",
         "Testing basic communication.",
         "CycleCare is a full-stack menstrual cycle tracking web application built with HTML, CSS, JavaScript, Flask, and MySQL. It lets users securely log period dates, review history, visualize period days in red on a calendar, and view transparent cycle forecasts.",
         "Claiming it is an advanced AI or clinical diagnosis application."),

        ("Level 2: How does data move from frontend to backend?",
         "Testing HTTP request/response lifecycle comprehension.",
         "The browser intercepts form submits with vanilla JS, validates data, and sends an async fetch() POST request with JSON. Flask parses request.get_json(), validates the fields, runs a parameterized SQL query against MySQL via db.py, and returns a JSON payload with an appropriate HTTP status code. JavaScript parses the response and updates the DOM.",
         "Saying the frontend connects directly to MySQL."),

        ("Level 3: How do you prevent SQL Injection?",
         "Testing application security knowledge.",
         "In database/db.py, all queries use %s placeholders with separate tuple arguments. PyMySQL escapes the arguments, ensuring user inputs are treated strictly as data literals and never executed as SQL code.",
         "Saying you used string sanitizers or replace() on SQL strings."),

        ("Level 4: What was the biggest challenge you faced?",
         "Testing debugging and engineering experience.",
         "Building the interactive calendar in vanilla JS and mapping multi-day period ranges across month boundaries (e.g., September 29 to October 3). I resolved this by pre-computing a date lookup map that flags period days in O(1) time so that cells across both months highlight in red accurately.",
         "Saying everything was easy or that you used an external library.")
    ]

    for title, testing, ans, mistake in qa_list:
        story.append(Paragraph(f"<b>{title}</b>", style_h2))
        story.append(Paragraph(f"<i>What is tested:</i> {testing}", style_body))
        story.append(Paragraph(f"<b>Answer:</b> {ans}", style_body))
        story.append(Paragraph(f"<b>Common Mistake to Avoid:</b> <font color='#be123c'>{mistake}</font>", style_body))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PART 16 & 17: CODE EXPLANATION & PITCH
    # -------------------------------------------------------------------------
    story.append(Paragraph("PART 16 — Key Code Snippets to Explain", style_h1))

    story.append(Paragraph("<b>1. Protected Route Decorator (`routes/auth.py`)</b>", style_h2))
    story.append(Paragraph("<code>@wraps(f)<br/>def decorated_function(*args, **kwargs):<br/>&nbsp;&nbsp;&nbsp;&nbsp;if 'user_id' not in session:<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return jsonify({'success': False, 'message': 'Authentication required.'}), 401<br/>&nbsp;&nbsp;&nbsp;&nbsp;return f(*args, **kwargs)</code>", style_code))
    story.append(Paragraph("<i>Explanation:</i> Intercepts incoming API calls. If the encrypted session cookie does not contain <code>user_id</code>, it rejects the request with HTTP 401 Unauthorized before any database query runs.", style_body))

    story.append(Paragraph("<b>2. Data Ownership Authorization Check (`routes/cycles.py`)</b>", style_h2))
    story.append(Paragraph("<code>existing = query_db('SELECT id, user_id FROM cycles WHERE id = %s', (cycle_id,), one=True)<br/>if not existing: return jsonify({'message': 'Not found'}), 404<br/>if existing['user_id'] != session['user_id']: return jsonify({'message': 'Unauthorized'}), 403</code>", style_code))
    story.append(Paragraph("<i>Explanation:</i> Prevents Insecure Direct Object Reference (IDOR) attacks. If User A tries to edit User B's cycle record ID, the backend rejects it with HTTP 403 Forbidden.", style_body))

    story.append(Paragraph("<b>3. Calendar Period Date Mapping (`static/js/calendar.js`)</b>", style_h2))
    story.append(Paragraph("<code>const current = new Date(start);<br/>while (current &lt;= end) {<br/>&nbsp;&nbsp;&nbsp;&nbsp;dateMap[toDateKey(current)] = { type: 'logged', dayOfPeriod: dayNum, cycle: cycle };<br/>&nbsp;&nbsp;&nbsp;&nbsp;current.setDate(current.getDate() + 1);<br/>}</code>", style_code))
    story.append(Paragraph("<i>Explanation:</i> Iterates each day between <code>start_date</code> and <code>end_date</code> and indexes it in a lookup dictionary. During rendering, calendar cells check this map to apply the vibrant red <code>.period-day</code> class.", style_body))

    story.append(Spacer(1, 10))
    story.append(Paragraph("PART 17 — 60-Second Interview Pitch", style_h1))
    pitch_text = (
        "<i>\"CycleCare is a full-stack menstrual cycle tracking web application that I designed and built using "
        "HTML5, vanilla CSS, vanilla JavaScript, Python Flask, and MySQL.<br/>"
        "The problem it solves is helping users log and understand their menstrual rhythm privately, without intrusive ads "
        "or confusing algorithms. Users can create an account, log period dates and durations with full CRUD capabilities, "
        "and view their period days highlighted in red on an interactive monthly calendar.<br/>"
        "On the backend, I built RESTful JSON endpoints protected by session-based authentication and parameterized SQL queries "
        "to guarantee user data isolation. It also features a transparent estimation engine that calculates average cycle lengths "
        "and forecasts upcoming period dates using clear mathematical formulas.<br/>"
        "I built it from scratch without heavy frameworks to deeply understand how the frontend, HTTP requests, backend controllers, "
        "and relational databases connect together.\"</i>"
    )
    story.append(Paragraph(pitch_text, style_body))

    # -------------------------------------------------------------------------
    # PART 19 & 20: CHEAT SHEET & CHECKLIST
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("PART 19 & 20 — Final Revision Cheat Sheet", style_h1))

    final_sheet_data = [
        [Paragraph("<b>Topic</b>", style_table_header), Paragraph("<b>Implementation Details</b>", style_table_header)],
        [Paragraph("Frontend Tech", style_table_cell), Paragraph("Semantic HTML5, CSS3 (Variables, Grid, Flexbox), Vanilla JavaScript (ES6+ fetch API).", style_table_cell)],
        [Paragraph("Backend Tech", style_table_cell), Paragraph("Python Flask (Modular Blueprints: `auth_bp`, `cycles_bp`, `dashboard_bp`).", style_table_cell)],
        [Paragraph("Database", style_table_cell), Paragraph("MySQL 8.0+ / PyMySQL with automated zero-config SQLite fallback for evaluation.", style_table_cell)],
        [Paragraph("Authentication", style_table_cell), Paragraph("Encrypted session cookies (`session['user_id']`), `@login_required` decorator.", style_table_cell)],
        [Paragraph("Password Security", style_table_cell), Paragraph("PBKDF2/SHA-256 one-way salted hashing via `werkzeug.security`.", style_table_cell)],
        [Paragraph("Database Tables", style_table_cell), Paragraph("`users` (id, name, email, password_hash) and `cycles` (id, user_id, start_date, end_date, duration, length, notes).", style_table_cell)],
        [Paragraph("Relational Integrity", style_table_cell), Paragraph("Foreign Key `cycles.user_id -> users.id` with `ON DELETE CASCADE`.", style_table_cell)],
        [Paragraph("Estimation Formula", style_table_cell), Paragraph("Estimated Next Period = Latest Period Start Date + Average Cycle Length.", style_table_cell)],
        [Paragraph("Calendar Highlights", style_table_cell), Paragraph("Logged period days highlighted in **RED** (`#dc2626`), projected windows in dashed blush.", style_table_cell)],
        [Paragraph("Security Defenses", style_table_cell), Paragraph("Parameterized queries (%s), IDOR authorization checks, XSS escaping, `.env` config.", style_table_cell)],
        [Paragraph("Top 3 Future Improvements", style_table_cell), Paragraph("1. CSRF token validation; 2. Login rate-limiting; 3. CSV/PDF history export.", style_table_cell)]
    ]
    t_final = Table(final_sheet_data, colWidths=[120, 384])
    t_final.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_final)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[CycleCare PDF] Generated successfully at: {PDF_OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
