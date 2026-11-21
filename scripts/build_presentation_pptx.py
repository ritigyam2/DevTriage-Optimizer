import os, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==========================================================
# PALETTE & DESIGN SYSTEM (16:9 Modern Professional Navy)
# ==========================================================
C_DARK_NAVY   = RGBColor(15, 30, 60)      # #0F1E3C - Primary Dark / Hero BG
C_NAVY        = RGBColor(31, 73, 125)     # #1F497D - Primary Accent / Headers
C_SLATE_BLUE  = RGBColor(46, 117, 182)    # #2E75B6 - Secondary Accent
C_LIGHT_BLUE  = RGBColor(235, 243, 250)   # #EBF3FA - Card / Highlight BG
C_WHITE       = RGBColor(255, 255, 255)   # #FFFFFF - Crisp Card Background
C_BG_PAGE     = RGBColor(248, 250, 252)   # #F8FAFC - Off-white Slide BG
C_CHARCOAL    = RGBColor(30, 41, 59)      # #1E293B - Primary Body Text
C_MUTED       = RGBColor(100, 116, 139)   # #64748B - Secondary / Meta Text
C_BORDER      = RGBColor(203, 213, 225)   # #CBD5E1 - Border Line
C_GREEN       = RGBColor(16, 185, 129)    # #10B981 - Success / Pass Badge
C_AMBER       = RGBColor(245, 158, 11)    # #F59E0B - Highlight / Note
C_LIGHT_GREEN = RGBColor(236, 253, 245)   # #ECFDF5 - Success BG

FONT_TITLE = "Calibri"
FONT_BODY  = "Calibri"

def add_header(slide, tracker_text, title_text, subtitle_text=""):
    """Standardized top header banner for content slides."""
    # Top Tracker / Category pill
    tb_tr = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
    tf_tr = tb_tr.text_frame
    tf_tr.word_wrap = True
    tf_tr.margin_left = tf_tr.margin_top = tf_tr.margin_right = tf_tr.margin_bottom = 0
    p_tr = tf_tr.paragraphs[0]
    p_tr.text = tracker_text.upper()
    p_tr.font.name = FONT_BODY
    p_tr.font.size = Pt(9.5)
    p_tr.font.bold = True
    p_tr.font.color.rgb = C_SLATE_BLUE

    # Main Slide Title
    tb_ti = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.55))
    tf_ti = tb_ti.text_frame
    tf_ti.word_wrap = True
    tf_ti.margin_left = tf_ti.margin_top = tf_ti.margin_right = tf_ti.margin_bottom = 0
    p_ti = tf_ti.paragraphs[0]
    p_ti.text = title_text
    p_ti.font.name = FONT_TITLE
    p_ti.font.size = Pt(22)
    p_ti.font.bold = True
    p_ti.font.color.rgb = C_NAVY

    # Optional Subtitle
    if subtitle_text:
        tb_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.25), Inches(11.7), Inches(0.35))
        tf_sub = tb_sub.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle_text
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = C_MUTED

    # Header Divider Line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.65), Inches(11.733), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = C_BORDER
    line.line.color.rgb = C_BORDER

def add_footer(slide, current_slide, total_slides=12):
    """Standardized footer banner."""
    # Footer line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = C_BORDER
    line.line.color.rgb = C_BORDER

    # Left metadata
    tb_left = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(8.0), Inches(0.3))
    tf_left = tb_left.text_frame
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_right = tf_left.margin_bottom = 0
    p_l = tf_left.paragraphs[0]
    p_l.text = "AutoTriage-DAA (Project 50) | Ritigya Mishra (SAP: 590028115) | B.Tech-CSE Batch B-9 (AI/ML)"
    p_l.font.name = FONT_BODY
    p_l.font.size = Pt(8.5)
    p_l.font.color.rgb = C_MUTED

    # Right slide number
    tb_right = slide.shapes.add_textbox(Inches(10.533), Inches(7.05), Inches(2.0), Inches(0.3))
    tf_right = tb_right.text_frame
    tf_right.margin_left = tf_right.margin_top = tf_right.margin_right = tf_right.margin_bottom = 0
    p_r = tf_right.paragraphs[0]
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.text = f"Slide {current_slide} of {total_slides}"
    p_r.font.name = FONT_BODY
    p_r.font.size = Pt(8.5)
    p_r.font.color.rgb = C_MUTED

def add_card(slide, left, top, width, height, bg_color=C_WHITE, border_color=C_BORDER):
    """Creates a card container shape."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    return card

def add_speaker_notes(slide, notes_text):
    """Adds speaker notes to a slide."""
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text

# ==========================================================
# PRESENTATION GENERATOR FUNCTION
# ==========================================================
def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ------------------------------------------------------
    # SLIDE 1: TITLE SLIDE (Dark Hero Style)
    # ------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_DARK_NAVY
    bg1.line.fill.background()

    # Category Pill
    pill1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.1), Inches(3.2), Inches(0.38))
    pill1.fill.solid()
    pill1.fill.fore_color.rgb = C_NAVY
    pill1.line.color.rgb = C_SLATE_BLUE
    tf_p1 = pill1.text_frame
    tf_p1.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_p1 = tf_p1.paragraphs[0]
    p_p1.alignment = PP_ALIGN.CENTER
    p_p1.text = "DESIGN & ANALYSIS OF ALGORITHMS — PBL"
    p_p1.font.name = FONT_BODY
    p_p1.font.size = Pt(9.5)
    p_p1.font.bold = True
    p_p1.font.color.rgb = RGBColor(220, 235, 255)

    # Main Title
    tb_t1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(11.333), Inches(1.2))
    tf_t1 = tb_t1.text_frame
    tf_t1.word_wrap = True
    p_t1 = tf_t1.paragraphs[0]
    p_t1.text = "AutoTriage-DAA"
    p_t1.font.name = FONT_TITLE
    p_t1.font.size = Pt(44)
    p_t1.font.bold = True
    p_t1.font.color.rgb = C_WHITE

    # Subtitle
    tb_sub1 = s1.shapes.add_textbox(Inches(1.0), Inches(2.85), Inches(11.333), Inches(0.9))
    tf_sub1 = tb_sub1.text_frame
    tf_sub1.word_wrap = True
    p_sub1 = tf_sub1.paragraphs[0]
    p_sub1.text = "An Offline First-Principles Decision Engine for Open-Source Issue Triage & Capacity-Constrained Developer Assignment"
    p_sub1.font.name = FONT_BODY
    p_sub1.font.size = Pt(17)
    p_sub1.font.color.rgb = RGBColor(190, 210, 235)

    # Accent divider
    div1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(3.95), Inches(11.333), Inches(0.03))
    div1.fill.solid()
    div1.fill.fore_color.rgb = C_SLATE_BLUE
    div1.line.fill.background()

    # Metadata Grid Cards
    meta_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.3), Inches(11.333), Inches(2.2))
    meta_box.fill.solid()
    meta_box.fill.fore_color.rgb = RGBColor(22, 42, 80)
    meta_box.line.color.rgb = RGBColor(45, 75, 125)

    tb_meta = s1.shapes.add_textbox(Inches(1.3), Inches(4.5), Inches(10.7), Inches(1.8))
    tf_meta = tb_meta.text_frame
    tf_meta.word_wrap = True

    def add_meta_row(tf, label, val):
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        run_lbl = p.add_run()
        run_lbl.text = f"{label:<28}:  "
        run_lbl.font.bold = True
        run_lbl.font.size = Pt(11.5)
        run_lbl.font.color.rgb = RGBColor(140, 185, 235)
        run_val = p.add_run()
        run_val.text = val
        run_val.font.size = Pt(11.5)
        run_val.font.color.rgb = C_WHITE
        p.space_after = Pt(4)

    add_meta_row(tf_meta, "Project Allocation", "Project 50 (Undergraduate PBL Scope)")
    add_meta_row(tf_meta, "Student Author", "Ritigya Mishra (SAP ID: 590028115)")
    add_meta_row(tf_meta, "Academic Program", "B.Tech — Computer Science & Engineering | Batch B-9 (AI/ML)")
    add_meta_row(tf_meta, "Implementation Standard", "Strict ISO C++17 (-std=c++17 -O3 -Wall -Wextra, 100% First-Principles)")
    add_meta_row(tf_meta, "Evaluation Date", "21 November 2026 | Final Project Submission & Viva Defense")

    add_speaker_notes(s1,
        "Good morning, respected professors and evaluation committee members. "
        "My name is Ritigya Mishra, SAP ID 590028115 from Batch B-9 (AI/ML). "
        "Today, I present AutoTriage-DAA, an offline first-principles decision engine developed for Project 50. "
        "The project is engineered entirely in standard ISO C++17 from first principles without external algorithmic libraries. "
        "It solves the dual challenge of open-source issue triaging and capacity-constrained developer scheduling while providing "
        "an exhaustive implementation workbench covering all 46 lecture topics from Units I to VI of our DAA curriculum."
    )

    # ------------------------------------------------------
    # SLIDE 2: PROBLEM & MOTIVATION
    # ------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Context & Real-World Challenge", "Problem Statement & Operational Motivation",
               "Why automated, first-principles algorithmic triage is critical for modern software ecosystems.")
    add_footer(s2, 2)

    # Left Card: The Real-World Crisis
    add_card(s2, Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.8))
    tb_p2l = s2.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.1), Inches(4.4))
    tf_p2l = tb_p2l.text_frame
    tf_p2l.word_wrap = True

    p = tf_p2l.paragraphs[0]
    p.text = "THE OPEN-SOURCE BACKLOG BOTTLENECK"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(12)

    points_l = [
        ("Exponential Issue Volume: ", "Modern repositories (Linux, Kubernetes, Chromium) receive hundreds of bug tickets, vulnerability alerts, and PRs weekly."),
        ("Manual Triage Latency: ", "Triage leads spend days manually inspecting prerequisites, filtering duplicates, and assessing SLA deadlines."),
        ("Security Exposure: ", "Critical zero-day security vulnerabilities linger unassigned while maintainers parse trivial defects."),
        ("Maintainer Burnout: ", "Ad-hoc task distribution overburdens senior maintainers while junior developers remain under-allocated.")
    ]
    for bold_prefix, text in points_l:
        p = tf_p2l.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + bold_prefix
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = C_CHARCOAL
        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_CHARCOAL
        p.space_after = Pt(8)

    # Right Card: Why First-Principles DAA?
    add_card(s2, Inches(6.933), Inches(1.85), Inches(5.6), Inches(4.8))
    tb_p2r = s2.shapes.add_textbox(Inches(7.183), Inches(2.05), Inches(5.1), Inches(4.4))
    tf_p2r = tb_p2r.text_frame
    tf_p2r.word_wrap = True

    p = tf_p2r.paragraphs[0]
    p.text = "WHY FIRST-PRINCIPLES ALGORITHMS?"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(12)

    points_r = [
        ("Deterministic Provability: ", "Unlike probabilistic AI models or heuristic scripts, classical DAA provides mathematical guarantees on optimality, stability, and runtime."),
        ("100% Offline Policy: ", "Zero dependence on cloud APIs, external network calls, or third-party proprietary solvers (e.g., Boost, CPLEX, Lemon)."),
        ("Asymptotic Predictability: ", "Strict runtime bounds: Merge Sort operates in proven Θ(n log n), Kuhn matching runs in O(V · E), and KMP scans in linear Θ(n)."),
        ("Dual-Role Impact: ", "Solves practical software engineering bottlenecks while functioning as a comprehensive pedagogical workbench.")
    ]
    for bold_prefix, text in points_r:
        p = tf_p2r.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + bold_prefix
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = C_CHARCOAL
        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_CHARCOAL
        p.space_after = Pt(8)

    add_speaker_notes(s2,
        "Turning to slide 2: In large software repositories, maintainers face a massive backlog bottleneck. "
        "Manual triage leads to days of delay, creating severe security risks when zero-day vulnerabilities sit unassigned. "
        "Furthermore, arbitrary task assignment leads to senior maintainer burnout. "
        "While many contemporary projects throw black-box heuristics or LLMs at this problem, AutoTriage-DAA demonstrates "
        "that classical algorithm design provides deterministic, provable, and offline guarantees. "
        "Every single algorithm is authored from scratch to ensure predictable performance and complete transparency."
    )

    # ------------------------------------------------------
    # SLIDE 3: OBJECTIVES & CONSTRAINTS
    # ------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "System Requirements", "Core Objectives & Mathematical Invariants",
               "Defining clear engineering goals and the formal constraints governing the triage engine.")
    add_footer(s3, 3)

    # Card 1: Core Objectives (Top Half)
    add_card(s3, Inches(0.8), Inches(1.85), Inches(11.733), Inches(2.35))
    tb_s3t = s3.shapes.add_textbox(Inches(1.05), Inches(2.0), Inches(11.2), Inches(2.05))
    tf_s3t = tb_s3t.text_frame
    tf_s3t.word_wrap = True

    p = tf_s3t.paragraphs[0]
    p.text = "CORE ENGINEERING OBJECTIVES"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(6)

    objs = [
        ("1. Deterministic Backlog Triage: ", "Sort issues using a 3-key stable comparator (Severity ↓, Deadline ↑, ID ↑) in Θ(n log n) time."),
        ("2. Optimal Developer Assignment: ", "Compute maximum bipartite matching on skill compatibility graphs using Kuhn's augmenting path algorithm (O(V · E))."),
        ("3. Discrete Sprint Packaging: ", "Maximize business value within fixed sprint hour budgets via 0/1 Knapsack DP and Least-Cost Branch & Bound."),
        ("4. Defensive Ingestion & Deadlock Prevention: ", "Trap circular prerequisite dependencies via 3-color DFS graph cycle detection during CSV ingestion.")
    ]
    for bold_prefix, text in objs:
        p = tf_s3t.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + bold_prefix
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = C_CHARCOAL
        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_CHARCOAL
        p.space_after = Pt(4)

    # Card 2: Mathematical Invariants & Constraints (Bottom Half)
    add_card(s3, Inches(0.8), Inches(4.35), Inches(11.733), Inches(2.45))
    tb_s3b = s3.shapes.add_textbox(Inches(1.05), Inches(4.5), Inches(11.2), Inches(2.15))
    tf_s3b = tb_s3b.text_frame
    tf_s3b.word_wrap = True

    p = tf_s3b.paragraphs[0]
    p.text = "GOVERNING MATHEMATICAL CONSTRAINTS & INVARIANTS"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(6)

    consts = [
        ("Skill Subset Invariant: ", "An issue u can only be assigned to developer v if required skills form a subset of maintainer competencies: S_u ⊆ K_v. Strict intersection ≠ ∅ is rejected to prevent mismatched task delegation."),
        ("Workload Capacity Upper Bound: ", "For multi-task workload packing, total assigned hours cannot exceed available sprint capacity: Σ_{u ∈ A_v} w_u ≤ C_v."),
        ("Prerequisite Acyclicity Invariant: ", "The dependency digraph G_dep = (V, E_dep) must form a strict Directed Acyclic Graph (DAG). Any cycle (u ↔ v) is trapped before execution."),
        ("Strict ISO C++17 Standard: ", "Compiled under -std=c++17 -O3 -Wall -Wextra with zero compiler warnings and zero dynamic heap memory leaks.")
    ]
    for bold_prefix, text in consts:
        p = tf_s3b.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + bold_prefix
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = C_CHARCOAL
        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_CHARCOAL
        p.space_after = Pt(4)

    add_speaker_notes(s3,
        "On slide 3, we establish our core objectives and mathematical invariants. "
        "Notice the precision of our constraints: We enforce that required skills must be a strict subset of developer skills (S_u ⊆ K_v). "
        "A developer cannot be assigned a task if they only possess partial skills. "
        "Additionally, we enforce that task prerequisite dependencies must form a strict Directed Acyclic Graph. "
        "If a repository administrator accidentally introduces a circular dependency—say Issue 1 requires 2, and 2 requires 1—our 3-color DFS "
        "catches this during ingestion and halts gracefully instead of causing runtime infinite recursion."
    )

    # ------------------------------------------------------
    # SLIDE 4: SYSTEM ARCHITECTURE
    # ------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "System Design", "Two-Tier Architecture & Decoupled Layers",
               "Clean separation between the production decision engine and the academic syllabus workbench.")
    add_footer(s4, 4)

    # Left Container: Tier 1 vs Tier 2
    add_card(s4, Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.8))
    tb_s4l = s4.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.1), Inches(4.4))
    tf_s4l = tb_s4l.text_frame
    tf_s4l.word_wrap = True

    p = tf_s4l.paragraphs[0]
    p.text = "TWO-TIER SYSTEM ARCHITECTURE"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    p = tf_s4l.add_paragraph()
    r1 = p.add_run()
    r1.text = "TIER 1: Production Triage Engine (Phase I)\n"
    r1.font.bold = True
    r1.font.size = Pt(10.5)
    r1.font.color.rgb = C_SLATE_BLUE
    r2 = p.add_run()
    r2.text = "Focused operational tool providing stable backlog prioritization, 1-to-1 Kuhn matching, 0/1 Knapsack sprint packaging, and preemptive online streaming.\n\n"
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = C_CHARCOAL

    r3 = p.add_run()
    r3.text = "TIER 2: Curriculum Algorithm Workbench (Phase II)\n"
    r3.font.bold = True
    r3.font.size = Pt(10.5)
    r3.font.color.rgb = C_SLATE_BLUE
    r4 = p.add_run()
    r4.text = "Exhaustive experimentation platform implementing all 46 syllabus topics (Strassen, Held-Karp TSP, N-Queens, B&B pruning, KMP, CRT, NP-reductions) isolated cleanly from production code.\n\n"
    r4.font.size = Pt(9.5)
    r4.font.color.rgb = C_CHARCOAL

    r5 = p.add_run()
    r5.text = "Key Architectural Value: "
    r5.font.bold = True
    r5.font.size = Pt(9.5)
    r5.font.color.rgb = C_CHARCOAL
    r6 = p.add_run()
    r6.text = "Production triage is never bloated by academic toys; workbench algorithms remain independently runnable and testable."
    r6.font.size = Pt(9.5)
    r6.font.color.rgb = C_CHARCOAL

    # Right Container: 4 Functional Layers
    add_card(s4, Inches(6.933), Inches(1.85), Inches(5.6), Inches(4.8))
    tb_s4r = s4.shapes.add_textbox(Inches(7.183), Inches(2.05), Inches(5.1), Inches(4.4))
    tf_s4r = tb_s4r.text_frame
    tf_s4r.word_wrap = True

    p = tf_s4r.paragraphs[0]
    p.text = "FOUR DECOUPLED FUNCTIONAL LAYERS"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    layers = [
        ("Layer 1: Ingestion & Validation", "RFC 4180 CSV parser, numeric domain sanitation, and 3-color DFS dependency graph cycle detection."),
        ("Layer 2: Core Algorithmic Engine", "First-principles sorting, augmenting path bipartite flow, discrete dynamic programming, and branch-and-bound search."),
        ("Layer 3: Persistence & Telemetry", "Decoupled via report_exporter.hpp; writes true runtime variables dynamically to CSV without polluting stdout."),
        ("Layer 4: Presentation & CLI", "Interactive ANSI terminal menus, color-coded urgency badges, workload bars, and ASCII Gantt schedules.")
    ]
    for title, desc in layers:
        p = tf_s4r.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + title + ":\n  "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = C_CHARCOAL
        r2 = p.add_run()
        r2.text = desc + "\n"
        r2.font.size = Pt(9)
        r2.font.color.rgb = C_MUTED
        p.space_after = Pt(4)

    add_speaker_notes(s4,
        "Slide 4 illustrates our system architecture. We deliberately adopted a Two-Tier Architecture. "
        "Tier 1 contains the production triage decision engine—clean, focused, and fast. "
        "Tier 2 houses our academic algorithm workbench, where we implement and benchmark the full spectrum of the syllabus. "
        "Furthermore, our four-layer design strictly decouples persistence from computation. "
        "Algorithms execute purely in memory, while report_exporter.hpp writes genuine telemetry out to CSV, ensuring clean separation of concerns."
    )

    # ------------------------------------------------------
    # SLIDE 5: END-TO-END WORKFLOW
    # ------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "System Execution", "End-to-End Operational Workflow Pipeline",
               "Tracking data deterministically from raw CSV ingestion to optimal schedule visualization.")
    add_footer(s5, 5)

    # 6 Step Horizontal/Vertical Flow Cards
    flow_steps = [
        ("Stage 1: Defensive Ingestion", "Parser reads issues.csv & devs.csv. Validates fields; executes 3-color DFS. Traps circular prerequisites.", C_LIGHT_BLUE),
        ("Stage 2: Backlog Prioritization", "Multi-Key Merge Sort orders issues by Severity ↓, Deadline ↑, and ID ↑ in tight Θ(n log n) time.", C_LIGHT_BLUE),
        ("Stage 3: 1-to-1 Matching", "Constructs bipartite graph from S_u ⊆ K_v. Kuhn's augmenting paths find maximum 1-to-1 match (O(VE)).", C_WHITE),
        ("Stage 4: Sprint Optimization", "0/1 Knapsack DP selects discrete subset maximizing business value under sprint hour limit W.", C_WHITE),
        ("Stage 5: Architecture & Search", "Dijkstra calculates lowest-risk refactoring bypass; KMP scans crash dumps in linear Θ(n) time.", C_WHITE),
        ("Stage 6: Export & ASCII Gantt", "Generates terminal ASCII Gantt timeline and exports verified runtime telemetry directly to CSV.", C_LIGHT_GREEN)
    ]

    col_w = Inches(3.64)
    row_h = Inches(2.25)
    x_offsets = [Inches(0.8), Inches(4.84), Inches(8.88)]
    y_offsets = [Inches(1.85), Inches(4.35)]

    for idx, (title, desc, bg) in enumerate(flow_steps):
        r = idx // 3
        c = idx % 3
        card = add_card(s5, x_offsets[c], y_offsets[r], col_w, row_h, bg_color=bg)
        
        tb = s5.shapes.add_textbox(x_offsets[c] + Inches(0.2), y_offsets[r] + Inches(0.2), col_w - Inches(0.4), row_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_NAVY
        p.space_after = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_CHARCOAL

    add_speaker_notes(s5,
        "Slide 5 traces the end-to-end data pipeline. When the application starts: "
        "In Stage 1, raw CSV data is defensively tokenized and scanned for dependency cycles. "
        "In Stage 2, issues are stably sorted by our multi-key comparator. "
        "In Stage 3, developer compatibility is modeled as a bipartite graph and matched via Kuhn's algorithm. "
        "In Stage 4, sprint packaging is optimized using 0/1 Knapsack dynamic programming. "
        "In Stage 5, module refactoring risk is routed via Dijkstra, and crash logs are mined with KMP. "
        "Finally, Stage 6 renders human-readable ASCII Gantt timelines and exports live telemetry to disk. "
        "The entire pipeline completes in milliseconds."
    )

    # ------------------------------------------------------
    # SLIDE 6: CORE TRIAGE + DEVELOPER ASSIGNMENT
    # ------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Core Algorithms", "Backlog Sorting & Developer Assignment",
               "Examining the two fundamental algorithms driving Phase I triage and maintainer scheduling.")
    add_footer(s6, 6)

    # Left Card: Multi-Key Merge Sort
    add_card(s6, Inches(0.8), Inches(1.85), Inches(5.6), Inches(3.2))
    tb_s6l = s6.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.1), Inches(2.8))
    tf_s6l = tb_s6l.text_frame
    tf_s6l.word_wrap = True

    p = tf_s6l.paragraphs[0]
    p.text = "MULTI-KEY STABLE MERGE SORT"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(8)

    ms_points = [
        ("Master Theorem Proof: ", "T(n) = 2T(n/2) + Θ(n). Critical exponent log_2 2 = 1. By Case 2, runtime is asymptotically tight at Θ(n log n) across best, average, and worst cases."),
        ("Three-Tier Comparator: ", "Prioritizes Severity ↓, then SLA Deadline ↑, then ID ↑ for deterministic tie-breaking."),
        ("Strict Stability Invariant: ", "When Key(L[i]) == Key(R[j]), selects L[i], preserving identical relative arrival order.")
    ]
    for b_prefix, txt in ms_points:
        p = tf_s6l.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + b_prefix
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = C_CHARCOAL
        r2 = p.add_run()
        r2.text = txt
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_CHARCOAL
        p.space_after = Pt(4)

    # Right Card: Kuhn's Augmenting Path Matching
    add_card(s6, Inches(6.933), Inches(1.85), Inches(5.6), Inches(3.2))
    tb_s6r = s6.shapes.add_textbox(Inches(7.183), Inches(2.05), Inches(5.1), Inches(2.8))
    tf_s6r = tb_s6r.text_frame
    tf_s6r.word_wrap = True

    p = tf_s6r.paragraphs[0]
    p.text = "KUHN'S AUGMENTING PATH MATCHING"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(8)

    kuhn_points = [
        ("Bipartite Graph Formulation: ", "G = (U, V, E) where U = Issues, V = Developers. Edge exists iff S_u ⊆ K_v."),
        ("Berge's Lemma Guarantee: ", "Matching M is maximum iff G contains zero augmenting paths. Finds maximum matching in O(V · E) time via DFS path inversion."),
        ("Scenario 1 Benchmark: ", "Assigns 10/10 available developers (100% developer utilization, 20% backlog coverage).")
    ]
    for b_prefix, txt in kuhn_points:
        p = tf_s6r.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + b_prefix
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = C_CHARCOAL
        r2 = p.add_run()
        r2.text = txt
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_CHARCOAL
        p.space_after = Pt(4)

    # Bottom Full-Width Card: Model Separation Callout
    add_card(s6, Inches(0.8), Inches(5.2), Inches(11.733), Inches(1.6), bg_color=C_LIGHT_BLUE, border_color=C_SLATE_BLUE)
    tb_s6b = s6.shapes.add_textbox(Inches(1.05), Inches(5.3), Inches(11.2), Inches(1.4))
    tf_s6b = tb_s6b.text_frame
    tf_s6b.word_wrap = True

    p = tf_s6b.paragraphs[0]
    p.text = "CRITICAL THEORETICAL DISTINCTION: MODEL A vs MODEL B"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(4)

    p2 = tf_s6b.add_paragraph()
    r1 = p2.add_run()
    r1.text = "• Model A (1-to-1 Bipartite Assignment): "
    r1.font.bold = True
    r1.font.size = Pt(9.5)
    r1.font.color.rgb = C_CHARCOAL
    r2 = p2.add_run()
    r2.text = "Solves 1-issue-to-1-developer matching via Kuhn's algorithm. Evaluates maintainer coverage.\n"
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = C_CHARCOAL

    r3 = p2.add_run()
    r3.text = "• Model B (Multi-Task Workload Packing): "
    r3.font.bold = True
    r3.font.size = Pt(9.5)
    r3.font.color.rgb = C_CHARCOAL
    r4 = p2.add_run()
    r4.text = "Packs multiple issues into each developer's 40-hour sprint budget via Greedy/0-1 Knapsack DP. Bipartite matching is never misrepresented as a multi-item bin-packer."
    r4.font.size = Pt(9.5)
    r4.font.color.rgb = C_CHARCOAL

    add_speaker_notes(s6,
        "Slide 6 discusses our core triage and developer assignment mechanics. "
        "For backlog sorting, we chose Multi-Key Merge Sort because it guarantees Θ(n log n) under all cases and strictly maintains stability. "
        "For developer matching, Kuhn's augmenting path algorithm finds the maximum 1-to-1 matching in O(V · E) time. "
        "I want to draw your attention to the callout at the bottom: In our project, we maintain a strict academic separation between "
        "Model A (1-to-1 matching) and Model B (capacity packing). "
        "In Scenario 1, our bipartite matching assigns 10 out of 10 developers. That represents 100% developer utilization, "
        "even though 10 out of 50 total backlog issues were assigned (20% backlog coverage). "
        "Maintaining this distinction demonstrates theoretical clarity."
    )

    # ------------------------------------------------------
    # SLIDE 7: DAA SYLLABUS INTEGRATION
    # ------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Curriculum Mapping", "DAA Syllabus Integration Matrix (Units I–VI)",
               "Integrating all 46 course lecture topics into AutoTriage without cluttering the product narrative.")
    add_footer(s7, 7)

    # 6 Unit Cards in a 2x3 Grid
    units_data = [
        ("Unit I: Sorting & Searching", [
            "Multi-Key Merge Sort (Stable Θ(n log n))",
            "Median-of-3 Quick Sort (Mitigates collapse)",
            "Binary Search (Iterative O(1) & Recursive O(log n))"
        ]),
        ("Unit II: Divide & Conquer", [
            "Strassen Matrix Mult (Θ(n^2.807) co-editing matrix)",
            "Kadane Algorithm (Linear Θ(n) bug churn surge)",
            "Fast Exponentiation (Θ(log k) Markov transitions)",
            "Celebrity Problem (Linear O(n) review bottleneck)"
        ]),
        ("Unit III: Greedy Methods", [
            "Fractional Knapsack (Continuous QA relaxation)",
            "Activity Selection (Review meeting scheduling)",
            "Interval Partitioning (CI build server allocation)",
            "Huffman Coding (Lossless crash log compression)",
            "Dijkstra & Kruskal/Prim MST (Refactoring tree)"
        ]),
        ("Unit IV: Dynamic Programming", [
            "0/1 Knapsack (2D & 1D space-optimized Θ(nW))",
            "Matrix Chain Multiplication (Θ(n^3) join queries)",
            "LCS Dynamic Programming (Duplicate stack traces)",
            "Optimal BST & Floyd-Warshall Blast Radius",
            "Held-Karp TSP DP (Θ(n^2 2^n) microservice tour)"
        ]),
        ("Unit V: Backtracking & B&B", [
            "N-Queens (Bitmask reviewer conflict placement)",
            "Sum of Subsets (Residual sprint hour combinations)",
            "0/1 Knapsack Backtracking (Fractional bound)",
            "Knapsack B&B (Least-Cost dominates FIFO/LIFO)",
            "TSP Branch & Bound (Reduced Cost Matrix)"
        ]),
        ("Unit VI: Advanced Paradigms", [
            "Edmonds-Karp Max Flow (O(V E^2) team throughput)",
            "Kuhn Bipartite Matching (O(V E) 1-to-1 matching)",
            "Chinese Remainder Theorem (Distributed commit logs)",
            "4-Way String Matchers (KMP Θ(n), DFA, Rabin-Karp)",
            "P/NP Reduction (Subset-Sum ≤_P 0/1 Knapsack)"
        ]),
    ]

    for idx, (unit_title, algs) in enumerate(units_data):
        r = idx // 3
        c = idx % 3
        card = add_card(s7, x_offsets[c], y_offsets[r], col_w, row_h)
        
        tb = s7.shapes.add_textbox(x_offsets[c] + Inches(0.15), y_offsets[r] + Inches(0.15), col_w - Inches(0.3), row_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = unit_title
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_NAVY
        p.space_after = Pt(6)

        for alg in algs:
            p2 = tf.add_paragraph()
            p2.text = "• " + alg
            p2.font.size = Pt(8.5)
            p2.font.color.rgb = C_CHARCOAL
            p2.space_after = Pt(2)

    add_speaker_notes(s7,
        "On slide 7, we summarize how the entire DAA syllabus integrates into AutoTriage. "
        "Rather than spending 28 disjoint slides on 28 algorithms, we structured our implementation into a cohesive 6-unit matrix. "
        "Every single lecture topic from Units I through VI has a direct first-principles implementation in our Phase II workbench: "
        "from Strassen matrix multiplication to Huffman coding, Held-Karp dynamic programming, Least-Cost branch and bound, "
        "Chinese Remainder Theorem, KMP string matching, and formal polynomial reductions. "
        "Each implementation is backed by standalone unit tests."
    )

    # ------------------------------------------------------
    # SLIDE 8: IMPORTANT ALGORITHM COMPARISONS
    # ------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Empirical Evaluation", "Key Algorithmic Head-to-Head Comparisons",
               "Evaluating competing paradigms on adversarial, pathological, and discrete benchmark instances.")
    add_footer(s8, 8)

    # 3 Comparison Columns
    col3_w = Inches(3.64)
    c_x = [Inches(0.8), Inches(4.84), Inches(8.88)]

    # Comp 1: Sorting on Pre-sorted Data (N = 5,000)
    add_card(s8, c_x[0], Inches(1.85), col3_w, Inches(4.8))
    tb_c1 = s8.shapes.add_textbox(c_x[0] + Inches(0.2), Inches(2.05), col3_w - Inches(0.4), Inches(4.4))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True

    p = tf_c1.paragraphs[0]
    p.text = "SORTING ADVERSARIAL STRESS\n(N = 5,000 Pre-Sorted Elements)"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    p_s1 = tf_c1.add_paragraph()
    p_s1.text = "• Lomuto First-Pivot:\n  12,497,500 comparisons\n  Degrades to Θ(n^2)\n\n" \
                "• Median-of-3 Quick Sort:\n  60,678 comparisons\n  Mitigates sorted collapse\n\n" \
                "• Multi-Key Merge Sort:\n  51,420 comparisons\n  Guaranteed Θ(n log n)\n\n" \
                "Finding: Median-of-3 eliminates quadratic degradation on sorted arrays, closely tracking Merge Sort."
    p_s1.font.size = Pt(9.5)
    p_s1.font.color.rgb = C_CHARCOAL

    # Comp 2: String Matchers on 50,001-char Crash Log
    add_card(s8, c_x[1], Inches(1.85), col3_w, Inches(4.8))
    tb_c2 = s8.shapes.add_textbox(c_x[1] + Inches(0.2), Inches(2.05), col3_w - Inches(0.4), Inches(4.4))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True

    p = tf_c2.paragraphs[0]
    p.text = "PATHOLOGICAL STRING SEARCH\n(50,001-char 'AAAA...B' Log)"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    p_s2 = tf_c2.add_paragraph()
    p_s2.text = "• Naive Matcher:\n  299,976 comparisons (537 us)\n  Frequent pointer backtracks\n\n" \
                "• Rabin-Karp Rolling Hash:\n  6 comparisons (389 us)\n  Hash filtered false matches\n\n" \
                "• Knuth-Morris-Pratt (KMP):\n  100,005 ops (210 us)\n  Strictly ZERO backtracks\n\n" \
                "Finding: KMP's π-prefix table eliminates backtracking, running 3x faster than Naive search."
    p_s2.font.size = Pt(9.5)
    p_s2.font.color.rgb = C_CHARCOAL

    # Comp 3: Branch & Bound Pruning Efficiency
    add_card(s8, c_x[2], Inches(1.85), col3_w, Inches(4.8))
    tb_c3 = s8.shapes.add_textbox(c_x[2] + Inches(0.2), Inches(2.05), col3_w - Inches(0.4), Inches(4.4))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True

    p = tf_c3.paragraphs[0]
    p.text = "BRANCH & BOUND PRUNING\n(0/1 Knapsack N = 4, W = 15h)"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    p_s3 = tf_c3.add_paragraph()
    p_s3.text = "• FIFO B&B (Queue):\n  15 nodes expanded (19 generated)\n  2 branches pruned\n\n" \
                "• LIFO B&B (Stack):\n  9 nodes expanded (11 generated)\n  1 branch pruned\n\n" \
                "• Least-Cost (LC) B&B:\n  8 nodes expanded (11 generated)\n  5 branches pruned (Most)\n\n" \
                "Finding: Priority-queue upper bounding in LC B&B aggressively prunes suboptimal state-space subtrees."
    p_s3.font.size = Pt(9.5)
    p_s3.font.color.rgb = C_CHARCOAL

    add_speaker_notes(s8,
        "Slide 8 presents our empirical head-to-head algorithm comparisons: "
        "First, on sorting: When fed 5,000 pre-sorted elements, Lomuto Quick Sort collapsed to 12.5 million comparisons. "
        "Median-of-three pivot selection reduced this to 60,678 comparisons, closely tracking Merge Sort's 51,420. "
        "Second, on string matching: Searching a pathological 50,001-character log, KMP executed in 100,005 operations with strictly zero backtracks. "
        "Third, in Branch and Bound: Least-Cost search guided by fractional upper bounds expanded only 8 nodes and pruned 5 branches, "
        "demonstrating clear empirical superiority over FIFO and LIFO queue exploration."
    )

    # ------------------------------------------------------
    # SLIDE 9: TESTING STRATEGY & DEFENSIVE ENGINEERING
    # ------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Quality Assurance", "Testing Strategy & Defensive Engineering",
               "Comprehensive validation across 27 automated test suites and 5 standardized test categories.")
    add_footer(s9, 9)

    # Left Container: 5 Testing Categories
    add_card(s9, Inches(0.8), Inches(1.85), Inches(6.0), Inches(4.8))
    tb_s9l = s9.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.5), Inches(4.4))
    tf_s9l = tb_s9l.text_frame
    tf_s9l.word_wrap = True

    p = tf_s9l.paragraphs[0]
    p.text = "5-TIER TEST TAXONOMY"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    tax_points = [
        ("1. Normal Cases: ", "Balanced backlogs, standard developer profiles, non-conflicting schedules."),
        ("2. Boundary Cases: ", "N=1 single issue, empty developer pool (M=0), exact capacity fits, zero remaining hours."),
        ("3. Invalid Cases: ", "Corrupt CSV lines, non-numeric workload hours, out-of-bounds severity (sev = 9 > 5), negative capacity bounds."),
        ("4. Adversarial Cases: ", "Pre-sorted arrays targeting Quick Sort collapse; pathological repeated strings ('AAAA...B') targeting string matchers."),
        ("5. Stress & Graph Cycles: ", "120-issue synthetic enterprise datasets and circular prerequisite loops (Issue #1 <-> #2).")
    ]
    for b_prefix, txt in tax_points:
        p = tf_s9l.add_paragraph()
        r1 = p.add_run()
        r1.text = b_prefix
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = C_CHARCOAL
        r2 = p.add_run()
        r2.text = txt
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_CHARCOAL
        p.space_after = Pt(6)

    # Right Container: Automated Test Harness Badges
    add_card(s9, Inches(7.1), Inches(1.85), Inches(5.433), Inches(4.8))
    tb_s9r = s9.shapes.add_textbox(Inches(7.35), Inches(2.05), Inches(4.933), Inches(4.4))
    tf_s9r = tb_s9r.text_frame
    tf_s9r.word_wrap = True

    p = tf_s9r.paragraphs[0]
    p.text = "AUTOMATED TEST HARNESS EXECUTION"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    suites_info = [
        ("Phase I test_runner.exe: ", "7/7 Suites Passed (Sorting, Kuhn, Cycle Trap)"),
        ("Phase II test_chunk2_dnc.exe: ", "4/4 Suites Passed (Strassen, Kadane, Power)"),
        ("Phase II test_chunk3_greedy.exe: ", "6/6 Suites Passed (Knapsack, Activity, Dijkstra)"),
        ("Phase II test_chunk4_dp.exe: ", "7/7 Suites Passed (Knapsack, MCM, LCS, TSP)"),
        ("Phase II test_chunk5_backtracking_bb.exe: ", "5/5 Suites Passed (N-Queens, B&B Prune)"),
        ("Phase II test_chunk6_flow_strings_crt.exe: ", "5/5 Suites Passed (Flow, KMP, CRT, Reduction)")
    ]
    for b_p, s_t in suites_info:
        p = tf_s9r.add_paragraph()
        r1 = p.add_run()
        r1.text = "✓ " + b_p
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = C_GREEN
        r2 = p.add_run()
        r2.text = s_t
        r2.font.size = Pt(9)
        r2.font.color.rgb = C_CHARCOAL
        p.space_after = Pt(4)

    p_stat = tf_s9r.add_paragraph()
    p_stat.text = "\nTOTAL AUTOMATED TEST VERDICT:\n27 / 27 Test Suites Passing (100% Success Rate)"
    p_stat.font.bold = True
    p_stat.font.size = Pt(10.5)
    p_stat.font.color.rgb = C_NAVY

    add_speaker_notes(s9,
        "Slide 9 outlines our testing rigor. We structured testing around a formal 5-tier taxonomy: "
        "Normal, Boundary, Invalid, Adversarial, and Stress cases. "
        "In total, AutoTriage-DAA includes 27 distinct automated test suites distributed across 6 standalone test binaries. "
        "Every single suite compiles without warnings under standard GCC C++17 and passes 100% of its assertions. "
        "Crucially, our defensive CSV parser traps corrupt inputs and circular dependencies gracefully before any algorithm executes."
    )

    # ------------------------------------------------------
    # SLIDE 10: EMPIRICAL RESULTS & TELEMETRY
    # ------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Telemetry & Performance", "Empirical Telemetry & Performance Findings",
               "Genuine runtime metrics dynamically captured from compiled C++17 binaries.")
    add_footer(s10, 10)

    # 4 Stat Callout Cards
    stat_boxes = [
        ("60,678", "Quick Sort Comparisons", "Median-of-3 pivot on 5,000 sorted elements (vs 12.5M Lomuto collapse)", C_LIGHT_BLUE),
        ("100,005", "KMP Search Operations", "Linear scan across 50,001-character pathological log with 0 backtracks", C_LIGHT_BLUE),
        ("20 Nodes", "LC B&B State-Space Pruned", "Pruned non-viable search branches in Scenario 2 capacity shock", C_LIGHT_GREEN),
        ("1.0000", "Empirical Competitive Ratio", "Online streaming simulation matched offline optimal value on enterprise data", C_LIGHT_GREEN)
    ]
    sb_w = Inches(2.78)
    sb_h = Inches(1.8)
    sb_x = [Inches(0.8), Inches(3.78), Inches(6.76), Inches(9.74)]

    for idx, (num, label, desc, bg) in enumerate(stat_boxes):
        add_card(s10, sb_x[idx], Inches(1.85), sb_w, sb_h, bg_color=bg)
        tb = s10.shapes.add_textbox(sb_x[idx] + Inches(0.15), Inches(1.95), sb_w - Inches(0.3), sb_h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = num
        p1.font.bold = True
        p1.font.size = Pt(22)
        p1.font.color.rgb = C_NAVY

        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.bold = True
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_CHARCOAL
        p2.space_after = Pt(2)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = C_MUTED

    # Bottom Table: Telemetry Matrix
    add_card(s10, Inches(0.8), Inches(3.9), Inches(11.733), Inches(2.85))
    tb_t10 = s10.shapes.add_textbox(Inches(1.05), Inches(4.05), Inches(11.2), Inches(2.55))
    tf_t10 = tb_t10.text_frame
    tf_t10.word_wrap = True

    p = tf_t10.paragraphs[0]
    p.text = "DYNAMIC BENCHMARK TELEMETRY & PERSISTENCE SUMMARY"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(8)

    rows_info = [
        ("Benchmark Metric", "Observed Telemetry", "Theoretical Asymptotic Bound", "Defensible Engineering Insight"),
        ("Triage Sorting Latency", "1.4 ms for N=120 issues", "Tight Θ(n log n)", "Zero order inversions; deterministic multi-key tie breaking"),
        ("1-to-1 Bipartite Matching", "0.8 ms for 50 issues / 10 devs", "O(V · E) via Kuhn DFS", "100% developer utilization (10/10 devs matched)"),
        ("0/1 Knapsack Discrete DP", "1,244 business points (W=120h)", "Exact Pseudo-Poly Θ(nW)", "Closely tracks continuous Fractional bound of 1244.69"),
        ("Dynamic CSV Persistence", "scenario_benchmark_results.csv", "Decoupled via report_exporter", "Zero hardcoded strings; exports genuine runtime variables")
    ]
    for r_idx, (c1, c2, c3, c4) in enumerate(rows_info):
        p = tf_t10.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{c1:<25} | {c2:<28} | {c3:<25} | {c4}"
        r1.font.name = "Courier New" if r_idx > 0 else FONT_BODY
        r1.font.bold = (r_idx == 0)
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = C_NAVY if r_idx == 0 else C_CHARCOAL
        p.space_after = Pt(3)

    add_speaker_notes(s10,
        "Slide 10 highlights our empirical telemetry and benchmark results. "
        "Notice that our benchmarks are 100% dynamic: scenario_benchmarks.cpp exports calculated variables directly to CSV. "
        "For example, in Scenario 1, our 0/1 Knapsack dynamic program achieves 1,244 business value points under a 120-hour budget, "
        "closely tracking the continuous fractional relaxation bound of 1,244.69 points. "
        "In Scenario 2, under severe capacity reduction, Least-Cost Branch and Bound pruned 20 nodes, matching the exact DP optimum of 730 points. "
        "Across all datasets, execution times remain under a few milliseconds, proving offline viability."
    )

    # ------------------------------------------------------
    # SLIDE 11: LIVE DEMONSTRATION SCENARIOS
    # ------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Validation Scenarios", "Four Mandated Live Demonstration Scenarios",
               "Stress-testing the triage decision engine under realistic operational environments.")
    add_footer(s11, 11)

    # 4 Scenarios in 2x2 Grid
    scen_cards = [
        ("Scenario 1: Normal Sprint Operation",
         "Operational Context: 50 backlog issues, 10 developers (40h each), 120h sprint budget.\n"
         "• Kuhn Augmenting Matching: 10/10 developers utilized (100% dev utilization, 20% backlog coverage).\n"
         "• 0/1 Knapsack DP: Selects 16 issues yielding 1,244 points (Fractional bound: 1,244.69).\n"
         "• Verifies stable, balanced backlog allocation without developer over-subscription.", C_WHITE),

        ("Scenario 2: Emergency Capacity Shock",
         "Operational Context: Zero-day CVE disclosure; 50% maintainers on emergency leave; capacity slashed to 80h.\n"
         "• 0/1 Knapsack DP vs LC B&B: Both hit exact discrete optimum of 730 points.\n"
         "• LC B&B Pruning: Pruned 20 state-space nodes, demonstrating best-first search efficiency.\n"
         "• Dijkstra Rerouting: Identifies lowest-risk refactoring path bypassing locked modules (cost: 29.0).", C_WHITE),

        ("Scenario 3: Adversarial & Pathological Stress",
         "Operational Context: 5,000 pre-sorted elements; 50,001-character pathological repetitive crash log.\n"
         "• Median-of-3 Quick Sort: 60,678 comparisons vs 12.5M Lomuto collapse.\n"
         "• KMP Search: 100,005 operations with 0 backtracks (3x faster than Naive search).\n"
         "• Demonstrates algorithmic resilience against engineered worst-case inputs.", C_WHITE),

        ("Scenario 4: Synthetic Enterprise & Streaming",
         "Operational Context: 120 synthetic enterprise defects, 16 maintainers; 80h dynamic event stream.\n"
         "• Online Preemptive Streaming: Achieves empirical Competitive Ratio = 1.0000 vs offline optimum.\n"
         "• Zero-Day Preemption: Triggered 7 immediate task preemptions to preserve critical response SLAs.\n"
         "• Validates real-time event handling over large synthetic enterprise defect backlogs.", C_LIGHT_GREEN)
    ]

    sc_w = Inches(5.6)
    sc_h = Inches(2.25)
    sc_x = [Inches(0.8), Inches(6.933)]
    sc_y = [Inches(1.85), Inches(4.35)]

    for idx, (title, desc, bg) in enumerate(scen_cards):
        r = idx // 2
        c = idx % 2
        card = add_card(s11, sc_x[c], sc_y[r], sc_w, sc_h, bg_color=bg)
        
        tb = s11.shapes.add_textbox(sc_x[c] + Inches(0.2), sc_y[r] + Inches(0.15), sc_w - Inches(0.4), sc_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_NAVY
        p.space_after = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9)
        p2.font.color.rgb = C_CHARCOAL

    add_speaker_notes(s11,
        "Slide 11 details our four live demonstration scenarios executed by scenario_benchmarks.exe: "
        "Scenario 1 models normal sprint planning, achieving 100% developer utilization and 1,244 business points. "
        "Scenario 2 simulates an emergency capacity shock where 50% of maintainers take emergency leave during a CVE crisis. "
        "Here, Least-Cost B&B prunes 20 nodes to hit the exact 730-point optimum, and Dijkstra routes around locked modules. "
        "Scenario 3 tests adversarial inputs, proving that Median-of-3 Quick Sort and KMP withstand quadratic degradation attacks. "
        "Finally, Scenario 4 simulates an 80-hour dynamic event stream over 120 enterprise issues, achieving a competitive ratio of 1.0000 "
        "and executing 7 immediate preemptions for zero-day bugs."
    )

    # ------------------------------------------------------
    # SLIDE 12: LIMITATIONS, ETHICS & CONCLUSION
    # ------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Summary & Reflection", "System Limitations, Ethics & Final Conclusion",
               "Transparent boundary definitions, ethical maintainer safeguards, and concluding assessment.")
    add_footer(s12, 12)

    # Left Container: Limitations & Algorithmic Boundaries
    add_card(s12, Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.8))
    tb_s12l = s12.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.1), Inches(4.4))
    tf_s12l = tb_s12l.text_frame
    tf_s12l.word_wrap = True

    p = tf_s12l.paragraphs[0]
    p.text = "SYSTEM LIMITATIONS & BOUNDARIES"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    lims = [
        ("Model Separation Boundary: ", "Bipartite matching solves 1-to-1 assignment. Packing multiple tasks into a 40-hour budget is handled separately via Knapsack DP."),
        ("NP-Hard Scaling Bounds: ", "0/1 Knapsack DP is pseudo-polynomial (Θ(nW)), scaling with budget W. Exact Held-Karp TSP DP (Θ(n^2 2^n)) is computationally restricted to N ≤ 20 modules."),
        ("Quick Sort Worst-Case: ", "Median-of-three eliminates quadratic degradation on sorted arrays, but theoretical worst case remains O(n^2) for specially engineered permutations."),
        ("Reduction Verification Horizon: ", "Polynomial reduction construction is deterministic O(n), but empirical verification requires exponential O(2^n + nW) demonstration time.")
    ]
    for b_prefix, txt in lims:
        p = tf_s12l.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + b_prefix
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = C_CHARCOAL
        r2 = p.add_run()
        r2.text = txt
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_CHARCOAL
        p.space_after = Pt(6)

    # Right Container: Ethics & Conclusion
    add_card(s12, Inches(6.933), Inches(1.85), Inches(5.6), Inches(4.8))
    tb_s12r = s12.shapes.add_textbox(Inches(7.183), Inches(2.05), Inches(5.1), Inches(4.4))
    tf_s12r = tb_s12r.text_frame
    tf_s12r.word_wrap = True

    p = tf_s12r.paragraphs[0]
    p.text = "ETHICAL SAFEGUARDS & CONCLUSION"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    ethics_conclusion = [
        ("Maintainer Burnout Damping: ", "Incorporates workload caps to prevent algorithmic overloading of senior maintainers."),
        ("Anti-Pigeonholing & Fairness: ", "Uses arrival SLA rather than seniority for tie-breaking, ensuring junior engineers receive growth tasks."),
        ("Starvation Prevention: ", "Dynamic aging multiplier elevates neglected low-severity maintenance tasks over successive sprints."),
        ("Human-in-the-Loop Override: ", "Algorithmic schedules remain strictly advisory; triage leads retain full manual override."),
        ("Concluding Statement: ", "AutoTriage-DAA establishes a rigorous bridge between theoretical algorithms and production engineering, fulfilling all 46 course topics in clean, verified ISO C++17.")
    ]
    for b_prefix, txt in ethics_conclusion:
        p = tf_s12r.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + b_prefix
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = C_CHARCOAL
        r2 = p.add_run()
        r2.text = txt
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_CHARCOAL
        p.space_after = Pt(5)

    add_speaker_notes(s12,
        "To conclude on slide 12: We maintain complete academic honesty regarding system limitations. "
        "We do not overclaim: Bipartite matching is one-to-one; Knapsack DP is pseudo-polynomial; and Quick Sort worst-case remains O(n^2). "
        "From an ethical standpoint, AutoTriage incorporates burnout damping, anti-pigeonholing, and dynamic aging to prevent issue starvation. "
        "Most importantly, algorithmic schedules are advisory: Maintainers retain full override control. "
        "AutoTriage-DAA successfully demonstrates that first-principles DAA algorithms can power high-performance, deterministic software engineering. "
        "Thank you, and I now welcome any questions from the committee."
    )

    # Save presentation
    output_pptx = "AutoTriage_DAA_Final_Presentation.pptx"
    print(f"Saving presentation to {output_pptx}...")
    prs.save(output_pptx)
    print("Presentation generated successfully!")

if __name__ == '__main__':
    build_presentation()
