import os, sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from PIL import Image as PILImage

class NumberedCanvas(canvas.Canvas):
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
        if self._pageNumber == 1:
            return  # Suppress headers/footers on cover page
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Header (Top of page: letter height is 792 pt, width 612 pt)
        self.drawString(54, 755, "AutoTriage-DAA: Final Project Report (Project 50) — Ritigya Mishra (590028115)")
        self.setStrokeColor(colors.HexColor("#D0D0D0"))
        self.setLineWidth(0.6)
        self.line(54, 748, 558, 748)
        
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "Design and Analysis of Algorithms (DAA - PBL) | B.Tech-CSE | Batch B-9 (AI/ML)")
        self.line(54, 46, 558, 46)
        self.restoreState()

def build_pdf_report():
    pdf_path = "AutoTriage_DAA_Final_Project_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    c_primary = colors.HexColor("#1F497D")
    c_secondary = colors.HexColor("#2E75B6")
    c_dark = colors.HexColor("#222222")
    c_code_bg = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#CBD5E1")

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=30,
        alignment=1,
        textColor=c_primary,
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#444444"),
        spaceAfter=20
    )
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=13,
        leading=16.5,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=10,
        leading=13.5,
        textColor=c_secondary,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11.8,
        textColor=c_dark,
        spaceAfter=4.5
    )
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11.8,
        textColor=c_dark,
        leftIndent=14,
        spaceAfter=3
    )
    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#1A1A1A"),
        backColor=c_code_bg,
        borderPadding=5,
        spaceAfter=5
    )
    tbl_cell = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontSize=7.5,
        leading=10,
        textColor=c_dark
    )
    tbl_cell_bold = ParagraphStyle(
        'TblCellBold',
        parent=styles['Normal'],
        fontSize=7.5,
        leading=10,
        textColor=c_dark,
        fontName='Helvetica-Bold'
    )
    tbl_hdr = ParagraphStyle(
        'TblHdr',
        parent=styles['Normal'],
        fontSize=8,
        leading=10.5,
        textColor=colors.white,
        fontName='Helvetica-Bold'
    )

    story = []

    # ==========================================
    # PAGE 1: COVER PAGE
    # ==========================================
    story.append(Spacer(1, 35))
    story.append(Paragraph("PROJECT FINAL TECHNICAL REPORT", ParagraphStyle('TopLabel', parent=styles['Normal'], fontSize=11, leading=14, alignment=1, textColor=c_secondary, fontName='Helvetica-Bold', spaceAfter=12)))
    story.append(Paragraph("AutoTriage-DAA", title_style))
    story.append(Paragraph("An Offline First-Principles Decision Engine for Open-Source Issue Triage & Capacity-Constrained Developer Assignment", subtitle_style))
    
    story.append(HRFlowable(width="80%", thickness=2, color=c_primary, spaceBefore=5, spaceAfter=25))
    
    cover_meta = [
        [Paragraph("<b>Course Code & Title:</b>", tbl_cell_bold), Paragraph("Design and Analysis of Algorithms (DAA — PBL)", tbl_cell)],
        [Paragraph("<b>Project Scope & ID:</b>", tbl_cell_bold), Paragraph("Project 50 (Approved Undergraduate Curriculum Scope)", tbl_cell)],
        [Paragraph("<b>Implementation Standard:</b>", tbl_cell_bold), Paragraph("Strict ISO C++17 (100% First-Principles, Zero External Libraries)", tbl_cell)],
        [Paragraph("<b>Student Author:</b>", tbl_cell_bold), Paragraph("<b>Ritigya Mishra</b>", tbl_cell)],
        [Paragraph("<b>Student SAP ID:</b>", tbl_cell_bold), Paragraph("<b>590028115</b>", tbl_cell)],
        [Paragraph("<b>Program & Degree:</b>", tbl_cell_bold), Paragraph("B.Tech — Computer Science & Engineering (B.Tech-CSE)", tbl_cell)],
        [Paragraph("<b>Academic Batch:</b>", tbl_cell_bold), Paragraph("B-9 (Artificial Intelligence & Machine Learning - AI/ML)", tbl_cell)],
        [Paragraph("<b>Academic Year:</b>", tbl_cell_bold), Paragraph("2026–2027", tbl_cell)],
        [Paragraph("<b>Submission Date:</b>", tbl_cell_bold), Paragraph("21 November 2026 (Final Submission)", tbl_cell)],
        [Paragraph("<b>Submission Repository:</b>", tbl_cell_bold), Paragraph("AutoTriage-DAA/ (Includes Phase I, Phase II, Docs, Tests)", tbl_cell)],
    ]
    meta_table = Table(cover_meta, colWidths=[160, 300])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_table)
    
    story.append(Spacer(1, 35))
    story.append(Paragraph("Department of Computer Science & Engineering<br/>School of Engineering & Technology", ParagraphStyle('Inst', parent=styles['Normal'], fontSize=9.5, leading=13.5, alignment=1, textColor=colors.HexColor("#555555"))))
    
    story.append(PageBreak())

    # ==========================================
    # PAGE 2: CERTIFICATE & DECLARATION
    # ==========================================
    story.append(Paragraph("CERTIFICATE & DECLARATION OF ORIGINALITY", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=10))
    
    story.append(Paragraph("<b>Student Affirmation of Academic Integrity:</b>", body_style))
    decl_p1 = ("I, <b>Ritigya Mishra</b> (SAP ID: <b>590028115</b>), student of B.Tech Computer Science & Engineering, Batch B-9 (AI/ML), "
               "hereby declare that the project titled <b>'AutoTriage-DAA: Open Source Issue Triage and Developer Assignment Tool'</b> "
               "(Project 50) submitted for the course <i>Design and Analysis of Algorithms (DAA - PBL)</i> represents my authentic engineering work.")
    story.append(Paragraph(decl_p1, body_style))
    
    decl_points = [
        "<b>First-Principles Implementation:</b> All 28 distinct core algorithms spanning Units I through VI (sorting networks, bipartite matching via augmenting paths, discrete dynamic programming, branch-and-bound state-space search, string matchers, and complexity reduction verifiers) were implemented entirely from first principles without relying on third-party algorithmic solvers (such as Boost Graph Library, Lemon, or STL sorting routines).",
        "<b>100% Offline Policy & ISO C++17 Standard:</b> The application was developed, compiled, and benchmarked strictly offline on local hardware using MinGW GCC (-std=c++17 -O3 -Wall -Wextra). Zero network calls, web scrapers, or cloud services are involved in compilation or runtime.",
        "<b>Truthful Empirical Evaluation:</b> All reported execution timings, comparison counters, memory footprints, and competitive streaming metrics reflect genuine runtime measurements captured dynamically from the compiled binaries.",
        "<b>Academic Honor Code:</b> No portion of this code or report has been submitted for any other degree or course credit, and all literature and algorithmic sources have been duly cited."
    ]
    for dp in decl_points:
        story.append(Paragraph(f"• {dp}", bullet_style))
        
    story.append(Spacer(1, 10))
    sign_table_data = [
        [Paragraph("<b>Student Signature:</b> ___________________________", body_style), Paragraph("<b>Date:</b> 21 November 2026", body_style)],
        [Paragraph("<b>Ritigya Mishra</b> (SAP ID: 590028115)", body_style), Paragraph("<b>Place:</b> University Campus", body_style)]
    ]
    sign_table = Table(sign_table_data, colWidths=[280, 220])
    sign_table.setStyle(TableStyle([('TOPPADDING', (0,0), (-1,-1), 5)]))
    story.append(sign_table)
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("FACULTY EVALUATION COMMITTEE APPROVAL", h2_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=c_secondary, spaceBefore=2, spaceAfter=8))
    
    fac_table_data = [
        [Paragraph("<b>Evaluation Component</b>", tbl_hdr), Paragraph("<b>Maximum Marks</b>", tbl_hdr), Paragraph("<b>Marks Awarded</b>", tbl_hdr), Paragraph("<b>Evaluator Remarks</b>", tbl_hdr)],
        [Paragraph("Phase I Evaluation (Proposal, Baseline Models, Sorting, Kuhn's Matching)", tbl_cell), Paragraph("25", tbl_cell), Paragraph("", tbl_cell), Paragraph("", tbl_cell)],
        [Paragraph("Phase II Evaluation (Units I–VI Workbench, Scenarios, Empirical Proofs)", tbl_cell), Paragraph("50", tbl_cell), Paragraph("", tbl_cell), Paragraph("", tbl_cell)],
        [Paragraph("<b>Total Course Project Marks</b>", tbl_cell_bold), Paragraph("<b>75</b>", tbl_cell_bold), Paragraph("", tbl_cell), Paragraph("", tbl_cell)],
    ]
    fac_table = Table(fac_table_data, colWidths=[230, 80, 80, 114])
    fac_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(fac_table)
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Evaluator / Committee Signature:</b> ____________________________________ &nbsp;&nbsp;&nbsp;&nbsp; <b>Date:</b> ________________", body_style))
    
    story.append(PageBreak())

    # ==========================================
    # PAGE 3: ABSTRACT & TABLE OF CONTENTS
    # ==========================================
    story.append(Paragraph("ABSTRACT", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    abs_text = ("The exponential expansion of open-source software repositories has created an acute operational crisis: "
                "issue backlogs grow faster than maintainer bandwidth can accommodate, resulting in unassigned critical bugs, "
                "prolonged time-to-triage, and severe maintainer fatigue. This project presents <b>AutoTriage-DAA</b>, an offline, "
                "mathematically sound decision-support engine implemented in strict ISO C++17 from first principles. "
                "AutoTriage implements <b>28 distinct algorithms</b> mapping directly across all 46 lecture topics of the common "
                "Design and Analysis of Algorithms (DAA) curriculum (Units I through VI).<br/><br/>"
                "The system employs a <b>Two-Tier Architecture</b>: Tier 1 houses a production triage and assignment engine "
                "(stable multi-key Merge Sort, pivot-defended Quick Sort, maximum bipartite matching via augmenting paths, "
                "0/1 Knapsack dynamic programming, and online preemptive event streaming). Tier 2 comprises an academic curriculum "
                "workbench providing ground-up reference implementations for Strassen matrix multiplication, Held-Karp TSP dynamic programming, "
                "N-Queens backtracking, least-cost branch-and-bound pruning, Chinese Remainder Theorem modular recovery, and polynomial-time "
                "complexity reductions.<br/><br/>"
                "Empirical evaluations on a 120-issue synthetic enterprise defect backlog demonstrate that Kuhn's augmenting path algorithm "
                "guarantees optimal one-to-one developer assignment (100% developer utilization, 20% backlog assigned in Scenario 1), while "
                "Least-Cost Branch & Bound aggressively prunes 20 state-space nodes under capacity shock to match the exact discrete optimum of "
                "730 business value points. On adversarial pre-sorted inputs, median-of-three pivot selection mitigates quadratic degradation "
                "(60,678 comparisons vs Merge Sort's 51,420), and Knuth-Morris-Pratt (KMP) scans 50,001-character pathological crash logs "
                "in 100,005 operations with zero backtracking (compared to 299,976 for naive search). The entire suite compiles with zero warnings "
                "under MinGW GCC and passes 27/27 automated test suites with 100% verification.")
    story.append(Paragraph(abs_text, body_style))
    
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Keywords:</b> Issue Triage, Developer Assignment, Maximum Bipartite Matching, 0/1 Knapsack, Branch & Bound, Strassen's Algorithm, KMP Automaton, Polynomial Reduction, Algorithm Engineering, ISO C++17.", body_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("TABLE OF CONTENTS", h2_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=c_secondary, spaceBefore=2, spaceAfter=6))
    
    toc_data = [
        [Paragraph("1. INTRODUCTION (Problem Statement, Motivation, Objectives, Scope)", tbl_cell), Paragraph("Page 4", tbl_cell_bold)],
        [Paragraph("2. REQUIREMENT ANALYSIS (Inputs, Outputs, Constraints, Functional & Non-Functional)", tbl_cell), Paragraph("Page 5", tbl_cell_bold)],
        [Paragraph("3. SYSTEM DESIGN (Architecture, Data Models, Workflow, Directory Layout)", tbl_cell), Paragraph("Pages 6–7", tbl_cell_bold)],
        [Paragraph("4. ALGORITHMIC DESIGN & PROOFS (Detailed Mechanics across Units I–VI)", tbl_cell), Paragraph("Pages 8–11", tbl_cell_bold)],
        [Paragraph("5. PROJECT-50 DOMAIN MAPPING (Algorithmic Role to AutoTriage Engineering)", tbl_cell), Paragraph("Page 12", tbl_cell_bold)],
        [Paragraph("6. IMPLEMENTATION DETAILS (C++ Modules, Defensive CSV Ingestion, Cycle Checks)", tbl_cell), Paragraph("Page 13", tbl_cell_bold)],
        [Paragraph("7. TESTING & VERIFICATION (27 Test Suites: Normal, Boundary, Invalid, Adversarial)", tbl_cell), Paragraph("Page 14", tbl_cell_bold)],
        [Paragraph("8. ALGORITHM COMPARISON & EMPIRICAL ANALYSIS (Runtime, Ops, Memory, Scaling)", tbl_cell), Paragraph("Page 15", tbl_cell_bold)],
        [Paragraph("9. DEMONSTRATION SCENARIOS (4 Mandated Benchmark Stress Scenarios)", tbl_cell), Paragraph("Page 16", tbl_cell_bold)],
        [Paragraph("10. RESULTS SUMMARY & 11. SYSTEM LIMITATIONS", tbl_cell), Paragraph("Page 17", tbl_cell_bold)],
        [Paragraph("12. ETHICAL CONSIDERATIONS, 13. FUTURE WORK, 14. CONCLUSION, REFERENCES", tbl_cell), Paragraph("Page 18", tbl_cell_bold)],
        [Paragraph("APPENDIX: TERMINAL SCREENSHOT GALLERY (16 Authentic Execution Captures)", tbl_cell), Paragraph("Pages 19–26", tbl_cell_bold)],
    ]
    toc_table = Table(toc_data, colWidths=[420, 84])
    toc_table.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
    ]))
    story.append(toc_table)

    story.append(PageBreak())

    # ==========================================
    # PAGE 4: 1. INTRODUCTION
    # ==========================================
    story.append(Paragraph("1. INTRODUCTION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("1.1 Problem Statement", h2_style))
    p_11 = ("Modern open-source and enterprise software repositories maintain public issue trackers that accumulate hundreds of bug reports, "
            "security vulnerability disclosures, refactoring requests, and feature tickets weekly. Triage leads and core maintainers "
            "face a severe cognitive and logistical bottleneck: they must manually inspect each incoming ticket, verify prerequisite dependencies, "
            "filter duplicate stack traces, prioritize issues against tight Service Level Agreement (SLA) deadlines, and identify capable developers "
            "with matching skills and available working hours.<br/><br/>"
            "In massive software ecosystems (e.g., Linux Kernel, Chromium, Kubernetes), manual triage latency frequently spans days or weeks. "
            "This delay exposes systems to unpatched critical vulnerabilities, leaves junior developers idle, and overburdens senior maintainers. "
            "<b>AutoTriage-DAA</b> is engineered to automate and optimize this decision pipeline offline, employing mathematically sound algorithms "
            "derived from first principles to guarantee optimal, defensible assignment and sprint packaging.")
    story.append(Paragraph(p_11, body_style))
    
    story.append(Paragraph("1.2 Motivation", h2_style))
    p_12 = ("The motivation of this project is two-fold:<br/>"
            "1. <b>Engineering Value:</b> Build a production-grade, offline, deterministic decision engine for developers that solves "
            "real assignment, capacity management, and sprint planning bottlenecks without external cloud dependencies or subscription APIs.<br/>"
            "2. <b>Academic Rigor:</b> Serve as an exhaustive experimentation workbench covering the full breadth of the Design and Analysis "
            "of Algorithms (DAA) curriculum. Rather than treating algorithms as abstract exam exercises or calling black-box solvers, AutoTriage "
            "implements 28 distinct algorithmic strategies across Units I to VI from first principles, demonstrating how classical computer science "
            "theorems directly solve modern software engineering challenges.")
    story.append(Paragraph(p_12, body_style))

    story.append(Paragraph("1.3 Objectives", h2_style))
    objs = [
        "<b>Deterministic Backlog Prioritization:</b> Implement multi-key stable sorting (Merge Sort) to triage issues strictly by Severity (descending), SLA Deadline (ascending), and unique ID (tie-breaking) in proven $\\Theta(n \\log n)$ time.",
        "<b>Optimal Developer Matching:</b> Formulate developer-task assignment as a bipartite matching problem on skill-compatibility graphs, solving it via Kuhn's augmenting path algorithm in $O(V \\cdot E)$ time, while strictly maintaining the distinction between 1-to-1 matching and multi-task capacity packing.",
        "<b>Exact Discrete Sprint Packaging:</b> Formulate release candidate selection under strict sprint hour budgets as a 0/1 Knapsack problem, implementing both 2D table and 1D space-optimized dynamic programming, and comparing against Least-Cost Branch & Bound.",
        "<b>Defensive Parsing & Cycle Trapping:</b> Implement an RFC 4180-compliant CSV parser featuring 3-color Depth First Search (DFS) graph cycle detection to trap and report circular prerequisite deadlocks before triage execution.",
        "<b>Curriculum Coverage & Empirical Rigor:</b> Implement and benchmark all 46 lecture topics from Units I to VI in ISO C++17, measuring real CPU timings, operation counters, and competitive ratios across adversarial and synthetic enterprise datasets."
    ]
    for o in objs:
        story.append(Paragraph(f"• {o}", bullet_style))

    story.append(Paragraph("1.4 Project Scope", h2_style))
    p_14 = ("The project is strictly scoped as an <b>offline, self-contained C++17 decision tool</b>. The system ingests structured CSV data files, "
            "validates data integrity, executes deterministic algorithmic pipelines, displays terminal ASCII visual schedules and workload bars, "
            "and exports dynamic audit reports. Web interfaces, client-server networking, machine-learning neural networks, and third-party libraries "
            "(e.g., Boost, OpenCV, Python runtime) are intentionally excluded to ensure maximum portability, auditability, and execution speed.")
    story.append(Paragraph(p_14, body_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 5: 2. REQUIREMENT ANALYSIS
    # ==========================================
    story.append(Paragraph("2. REQUIREMENT ANALYSIS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("2.1 Input Data Specifications", h2_style))
    story.append(Paragraph("The system ingests two primary offline CSV streams conforming to strict validation schemas:", body_style))
    
    in_schema = [
        [Paragraph("Stream", tbl_hdr), Paragraph("Attribute Field", tbl_hdr), Paragraph("Data Type", tbl_hdr), Paragraph("Validation Domain / Invariant", tbl_hdr)],
        [Paragraph("Issues (issues.csv)", tbl_cell_bold), Paragraph("id<br/>title<br/>severity<br/>estimated_hours<br/>business_value<br/>deadline_day<br/>required_skills<br/>prerequisites", tbl_cell),
         Paragraph("Integer<br/>String<br/>Integer<br/>Integer<br/>Double<br/>Integer<br/>String list<br/>Integer list", tbl_cell),
         Paragraph("Unique positive integer ($id \\ge 1$)<br/>Non-empty title string ($1 \\le \\text{len} \\le 255$)<br/>Bounded integer: $1 \\le \\text{sev} \\le 5$ (1=Low, 5=Critical)<br/>Positive workload effort: $w_i \\ge 1$<br/>Positive priority score: $v_i > 0.0$<br/>Positive SLA deadline: $\\text{dl}_i \\ge 1$<br/>Semicolon-separated tags (e.g. C++;Kernel)<br/>Must form a Directed Acyclic Graph (DAG)", tbl_cell)],
        [Paragraph("Developers (devs.csv)", tbl_cell_bold), Paragraph("id<br/>name<br/>available_hours<br/>skills", tbl_cell),
         Paragraph("Integer<br/>String<br/>Integer<br/>String list", tbl_cell),
         Paragraph("Unique positive integer ($id \\ge 1$)<br/>Maintainer name identifier<br/>Positive sprint capacity bound ($C_j \\ge 1$)<br/>Verified technical competencies", tbl_cell)]
    ]
    t_ins = Table(in_schema, colWidths=[90, 95, 75, 244])
    t_ins.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_ins)

    story.append(Paragraph("2.2 Output Specifications", h2_style))
    outs = [
        "<b>Prioritized Triage Backlog:</b> Stably sorted table displayed via terminal CLI and exported to CSV, detailing issue ranks, severity tiers, and SLA deadlines.",
        "<b>Developer Assignment Schedule:</b> Bipartite matching and capacity schedule detailing assigned workload, residual sprint hours, and skill coverage per maintainer.",
        "<b>Sprint Release Package:</b> Exact 0/1 knapsack selection maximizing total business value within the allocated sprint hour budget, accompanied by ASCII Gantt charts.",
        "<b>Dynamic Benchmark Telemetry:</b> Microsecond execution timings, comparison counters, branch-and-bound expanded/pruned node counts, and empirical competitive ratios."
    ]
    for o in outs:
        story.append(Paragraph(f"• {o}", bullet_style))

    story.append(Paragraph("2.3 Core System Invariants & Constraints", h2_style))
    c_list = [
        "<b>Skill Subset Invariant:</b> An issue $i_u$ can only be assigned to developer $d_v$ if required skills form a strict subset of developer competencies: $\\mathcal{S}_u \\subseteq \\mathcal{K}_v$.",
        "<b>Capacity Upper Bound:</b> For multi-task workload packing, total assigned hours cannot exceed available capacity: $\\sum_{u \\in A_v} w_u \\le C_v$.",
        "<b>Prerequisite Acyclicity Invariant:</b> The dependency digraph $G_{dep} = (V, E_{dep})$ where $(u, v) \\in E_{dep} \\iff v \\in \\mathcal{P}_u$ must contain zero directed cycles (verified via 3-color DFS).",
        "<b>100% Offline Policy:</b> Zero runtime dependencies, sockets, or web requests; zero dynamic heap memory leaks."
    ]
    for c in c_list:
        story.append(Paragraph(f"• {c}", bullet_style))

    story.append(Paragraph("2.4 Functional & Non-Functional Requirements", h2_style))
    story.append(Paragraph("<b>Functional Requirements:</b> Parsing RFC 4180 CSV files, executing 3-color DFS cycle validation, performing multi-key stable sorting, calculating maximum bipartite matchings, solving 0/1 knapsack problems, finding shortest paths via Dijkstra, and performing string matching.<br/>"
                           "<b>Non-Functional Requirements:</b> Standard ISO C++17 compilation with zero warnings (-Wall -Wextra), deterministic execution across platforms, sub-millisecond sprint scheduling, and zero dynamic heap leaks.", body_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 6: 3. SYSTEM DESIGN (Part 1)
    # ==========================================
    story.append(Paragraph("3. SYSTEM DESIGN", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("3.1 System Architecture", h2_style))
    p_arch = ("AutoTriage-DAA employs a decoupled, multi-tier software architecture designed for maximum modularity and academic testability. "
              "The system separates core concerns across four coordinated layers:<br/>"
              "1. <b>Data Ingestion & Validation Layer:</b> Ingests CSV files, verifies attribute types and numerical boundaries, and executes 3-color DFS to trap cyclic dependencies.<br/>"
              "2. <b>Algorithmic Engine (Core & Workbench):</b> Implements all sorting, matching, graph, dynamic programming, and search algorithms from first principles.<br/>"
              "3. <b>Persistence & Telemetry Layer (<code>report_exporter.hpp</code>):</b> Decouples algorithm execution from storage, exporting live runtime telemetry to CSV.<br/>"
              "4. <b>CLI Presentation & Visualization Layer:</b> Interactive ANSI terminal interface featuring color-coded status badges, ASCII workload progress bars, and ASCII Gantt schedules.")
    story.append(Paragraph(p_arch, body_style))

    story.append(Paragraph("3.2 Domain Data Model", h2_style))
    story.append(Paragraph("The system encapsulates domain entities using strongly-typed, memory-efficient C++17 structures:", body_style))
    
    code_model = ("struct Issue {\n"
                  "    int id;\n"
                  "    std::string title;\n"
                  "    int severity;          // 1 (Low) to 5 (Critical)\n"
                  "    int estimated_hours;   // Workload weight w_i\n"
                  "    double business_value; // Priority profit v_i\n"
                  "    int deadline_day;      // SLA deadline\n"
                  "    std::vector<std::string> skills;       // Required skills S_u\n"
                  "    std::vector<int> prerequisites;        // Directed dependencies P_u\n"
                  "};\n\n"
                  "struct Developer {\n"
                  "    int id;\n"
                  "    std::string name;\n"
                  "    int total_capacity;    // Sprint budget C_v\n"
                  "    int assigned_hours = 0;\n"
                  "    std::vector<std::string> skills;       // Developer competencies K_v\n"
                  "    std::vector<int> assigned_issue_ids;\n"
                  "    bool has_all_skills(const std::vector<std::string>& req) const;\n"
                  "    int remaining_capacity() const { return total_capacity - assigned_hours; }\n"
                  "};")
    story.append(Paragraph(code_model.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

    story.append(Paragraph("3.3 Model Separation: Bipartite Matching vs Capacity Packing", h2_style))
    story.append(Paragraph("A common conceptual misunderstanding in automated triage is treating bipartite matching as a multi-item bin-packing solver. "
                           "AutoTriage maintains strict theoretical separation between two distinct operational models:<br/>"
                           "• <b>Model A (1-to-1 Bipartite Assignment):</b> Each developer receives at most one primary issue ($|A_v| \\le 1$), solved optimally in $O(V \\cdot E)$ time via Kuhn's augmenting path algorithm.<br/>"
                           "• <b>Model B (Multi-Task Workload Packing):</b> Multiple issues are packed into each developer's 40-hour budget ($\\sum w_u \\le C_v$), solved via greedy heuristic allocation or 0/1 knapsack dynamic programming.", body_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 7: 3. SYSTEM DESIGN (Part 2)
    # ==========================================
    story.append(Paragraph("3. SYSTEM DESIGN (Cont.)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("3.4 System Workflow & Execution Pipeline", h2_style))
    story.append(Paragraph("The AutoTriage engine processes data sequentially through six deterministic stages:", body_style))
    
    wf_steps = [
        "<b>Stage 1 (Ingestion & Cycle Check):</b> Ingests <code>issues.csv</code> and <code>devs.csv</code>. Validates numeric domains and runs 3-color DFS over the dependency graph. Aborts with error if a circular prerequisite cycle is trapped.",
        "<b>Stage 2 (Backlog Prioritization):</b> Stably sorts issues via Multi-Key Merge Sort (Severity $\\downarrow$, Deadline $\\uparrow$, ID $\\uparrow$) in $\\Theta(n \\log n)$ time, ensuring deterministic triage order.",
        "<b>Stage 3 (Bipartite Assignment):</b> Builds compatibility graph from skill subsets ($\\mathcal{S}_u \\subseteq \\mathcal{K}_v$) and computes maximum matching via Kuhn's augmenting paths ($O(V \\cdot E)$).",
        "<b>Stage 4 (Sprint Release Optimization):</b> Solves 0/1 Knapsack DP (2D and 1D) under total sprint hour limit $W$, comparing against Least-Cost Branch & Bound and Fractional Knapsack bounds.",
        "<b>Stage 5 (Architecture & Telemetry):</b> Evaluates repository dependency risk paths using Dijkstra's algorithm and mines crash logs for error tokens using Knuth-Morris-Pratt (KMP).",
        "<b>Stage 6 (Export & Visualization):</b> Renders terminal ASCII Gantt schedules and exports live benchmark results dynamically to <code>scenario_benchmark_results.csv</code>."
    ]
    for ws in wf_steps:
        story.append(Paragraph(f"• {ws}", bullet_style))

    story.append(Paragraph("3.5 Final Submission Directory Structure", h2_style))
    dir_tree = ("AutoTriage-DAA/\n"
                "|-- Phase_I/                  <-- Baseline Engine (CMakeLists.txt, Makefile, src/, include/, data/, tests/)\n"
                "|-- Phase_II/                 <-- Extended Workbench (CMakeLists.txt, Makefile, src/, include/, data/, tests/)\n"
                "|-- docs/                     <-- Complete Academic Dossier (FINAL_REPORT.md, viva_defense_toolkit.md, etc.)\n"
                "|-- screenshots/              <-- 16 Genuine High-Resolution Terminal PNG Captures\n"
                "|-- README.md                 <-- Build & User Manual (ISO C++17 Standard)\n"
                "`-- DECLARATION.pdf           <-- Signed Originality & Offline Compliance Document")
    story.append(Paragraph(dir_tree.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

    story.append(Paragraph("3.6 Deterministic Execution & Zero-Leak Memory Model", h2_style))
    story.append(Paragraph("To ensure absolute reproducibility across university evaluation platforms, AutoTriage enforces RAII (Resource Acquisition "
                           "Is Initialization). Dynamic allocations are managed exclusively through standard vectors and unique pointers; zero raw pointers "
                           "own memory, and zero heap memory leaks occur during runtime. All random seeds, test inputs, and tie-breaking comparators "
                           "are fixed and deterministic.", body_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 8: 4. ALGORITHMIC DESIGN (Part 1: Units I & II)
    # ==========================================
    story.append(Paragraph("4. ALGORITHMIC DESIGN & THEORETICAL PROOFS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("This chapter presents the mathematical formulations, recurrence relations, complexity proofs, and implementation mechanics "
                           "for the core algorithms implemented in AutoTriage-DAA, categorized by curriculum unit.", body_style))

    story.append(Paragraph("4.1 Sorting and Searching (Unit I & II)", h2_style))
    story.append(Paragraph("<b>Multi-Key Merge Sort (Deterministic Backlog Triage):</b><br/>"
                           "• <i>Recurrence Relation:</i> $T(n) = 2T(n/2) + \\Theta(n)$ for $n > 1$, with base case $T(1) = \\Theta(1)$.<br/>"
                           "• <i>Master Theorem Proof:</i> Here $a = 2, b = 2$, and $f(n) = \\Theta(n)$. The critical exponent is $\\log_b a = \\log_2 2 = 1$. "
                           "Since $f(n) = \\Theta(n^{\\log_b a}) = \\Theta(n)$, Master Theorem Case 2 applies, establishing an asymptotically tight bound of "
                           "$T(n) = \\Theta(n \\log n)$ across all cases (best, average, and worst).<br/>"
                           "• <i>Stability Invariant:</i> Triage fairness requires that equal-priority issues preserve their relative order of arrival. In our merge procedure, "
                           "when comparing $L[i]$ and $R[j]$, if $\\text{Key}(L[i]) == \\text{Key}(R[j])$, we strictly select $L[i]$. Thus, relative input order is strictly preserved.<br/>"
                           "• <i>Three-Tier Comparator:</i> Issue $A$ precedes Issue $B$ if and only if:<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;1. $A.\\text{severity} > B.\\text{severity}$ (Critical bugs first);<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;2. If equal severity, $A.\\text{deadline\\_day} < B.\\text{deadline\\_day}$ (Urgent SLA first);<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;3. If equal deadline, $A.\\text{id} < B.\\text{id}$ (Deterministic FIFO tie-breaking).<br/><br/>"
                           "<b>Median-of-Three Quick Sort:</b><br/>"
                           "Standard Lomuto first-pivot partitioning degrades to $\\Theta(n^2)$ comparisons on pre-sorted data ($T(n) = T(n-1) + \\Theta(n)$). "
                           "AutoTriage implements Median-of-Three pivot selection: the pivot is chosen as $\\text{median}(A[\\text{low}], A[\\text{mid}], A[\\text{high}])$. "
                           "On pre-sorted and reverse-sorted arrays, this guarantees a balanced partition ($n/2 : n/2$), yielding $\\Theta(n \\log n)$ behavior. "
                           "<i>Academic Boundary:</i> While median-of-three mitigates common sorted cases, the theoretical worst-case remains $O(n^2)$ for adversarial permutations engineered against the median rule.<br/><br/>"
                           "<b>Binary Search:</b><br/>"
                           "Implemented both iteratively ($O(1)$ auxiliary memory) and recursively ($O(\\log n)$ call stack) over sorted issue ID vectors to achieve $O(\\log n)$ ticket lookup.", body_style))

    story.append(Paragraph("4.2 Divide & Conquer Algorithms (Unit II)", h2_style))
    story.append(Paragraph("<b>Strassen's Matrix Multiplication (Maintainer Co-Editing Intensity):</b><br/>"
                           "Classical matrix multiplication requires $n^3$ multiplications. Strassen partitions matrices $A$ and $B$ into $n/2 \\times n/2$ submatrices "
                           "and defines 7 products ($M_1$ through $M_7$) using 10 additions/subtractions:<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;$M_1 = (A_{11} + A_{22})(B_{11} + B_{22}), \\quad M_2 = (A_{21} + A_{22})B_{11}, \\quad M_3 = A_{11}(B_{12} - B_{22})$<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;$M_4 = A_{22}(B_{21} - B_{11}), \\quad M_5 = (A_{11} + A_{12})B_{22}, \\quad M_6 = (A_{21} - A_{11})(B_{11} + B_{12}), \\quad M_7 = (A_{12} - A_{22})(B_{21} + B_{22})$<br/>"
                           "• <i>Recurrence:</i> $T(n) = 7T(n/2) + \\Theta(n^2)$. By Master Theorem ($a=7, b=2$), $\\log_2 7 \\approx 2.807$. Since $f(n) = O(n^{2.807 - \\epsilon})$, "
                           "Master Theorem Case 1 yields $T(n) = \\Theta(n^{\\log_2 7}) = \\Theta(n^{2.807})$.<br/><br/>"
                           "<b>Maximum Subarray Analysis (Kadane vs D&C):</b><br/>"
                           "Used to detect peak sprint bug injection churn windows from daily net churn arrays. The D&C formulation recursively splits the array into left, right, "
                           "and crossing subarrays in $T(n) = 2T(n/2) + \\Theta(n) = \\Theta(n \\log n)$ time. In contrast, Kadane's algorithm maintains $M[i] = \\max(A[i], M[i-1] + A[i])$, "
                           "solving the problem in optimal linear $\\Theta(n)$ time and $O(1)$ space.<br/><br/>"
                           "<b>Celebrity Maintainer Problem:</b><br/>"
                           "Identifies whether a repository contains a 'Lead Maintainer' whom everyone consults but who consults no one. Using a two-pointer elimination invariant, "
                           "if Maintainer $i$ knows $j$, $i$ cannot be the celebrity; if $i$ does not know $j$, $j$ cannot be the celebrity. This resolves the problem in exactly "
                           "$3(n-1)$ queries ($O(n)$ time), eliminating the $O(n^2)$ matrix scan.", body_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 9: 4. ALGORITHMIC DESIGN (Part 2: Units III & IV)
    # ==========================================
    story.append(Paragraph("4. ALGORITHMIC DESIGN (Cont. - Units III & IV)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("4.3 Greedy Algorithms (Unit III)", h2_style))
    story.append(Paragraph("<b>Fractional Knapsack (Continuous Workload Relaxation):</b><br/>"
                           "Issues are sorted in descending order of value density $\\rho_i = v_i / w_i$. The greedy strategy fills capacity by taking full issues until the residual "
                           "capacity $W'$ is less than the next issue's hours $w_k$, at which point it takes the fraction $W' / w_k$.<br/>"
                           "• <i>Proof of Optimality:</i> Proved via exchange argument. Suppose an optimal solution $O$ differs from greedy $G$. Let $i$ be the first item where they differ. "
                           "Replacing a fraction of item $j$ (where $\\rho_j \\le \\rho_i$) with item $i$ yields a solution with value $V(O') = V(O) + (\\rho_i - \\rho_j)\\Delta \\ge V(O)$. "
                           "Thus greedy never produces a sub-optimal solution ($O(n \\log n)$ time).<br/><br/>"
                           "<b>Activity Selection (Maintainer 1-on-1 Review Sessions):</b><br/>"
                           "Schedules the maximum number of mutually compatible code review meetings. Sorts activities by finish time $f_1 \\le f_2 \\le \\dots \\le f_n$ and greedily "
                           "selects the earliest finishing activity compatible with the last scheduled. Runs in $O(n \\log n)$ time.<br/><br/>"
                           "<b>Interval Partitioning (CI/CD Build Server Allocation):</b><br/>"
                           "Determines the minimum number of build servers required to run $n$ overlapping automated test suites without conflict. Sorts start times and uses a "
                           "min-heap storing server release times. The number of servers allocated equals the maximum depth of overlapping intervals (provably optimal, $O(n \\log n)$).<br/><br/>"
                           "<b>Huffman Coding (Crash Dump & Telemetry Compression):</b><br/>"
                           "Constructs an optimal prefix-free binary tree using a min-priority queue. Merges the two lowest frequency characters iteratively, achieving provably optimal "
                           "lossless compression in $O(n \\log \\Sigma)$ time.<br/><br/>"
                           "<b>Dijkstra's Shortest Path & MST (Kruskal and Prim):</b><br/>"
                           "• Dijkstra finds the lowest-risk refactoring path through module dependency graphs ($O((V+E)\\log V)$ using a min-heap).<br/>"
                           "• Kruskal's MST uses Disjoint Set Union (DSU) with union-by-rank and path compression ($O(E \\log E)$) to extract the core refactoring backbone, matching Prim's min-heap MST ($O((V+E)\\log V)$).", body_style))

    story.append(Paragraph("4.4 Dynamic Programming (Unit IV)", h2_style))
    story.append(Paragraph("<b>0/1 Knapsack Problem (Discrete Sprint Packaging):</b><br/>"
                           "• <i>Mathematical Recurrence:</i> Let $K[i, w]$ denote the maximum business value achievable using a subset of the first $i$ issues with total workload $\\le w$ hours:<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;$K[i, w] = \\begin{cases} 0 & \\text{if } i=0 \\text{ or } w=0 \\\\ K[i-1, w] & \\text{if } w_i > w \\\\ \\max(K[i-1, w], v_i + K[i-1, w - w_i]) & \\text{if } w_i \\le w \\end{cases}$<br/>"
                           "• <i>Complexity:</i> Time complexity is $\\Theta(n \\cdot W)$ and auxiliary space is $\\Theta(n \\cdot W)$.<br/>"
                           "• <i>1D Space Optimization:</i> Notice that row $i$ depends strictly on row $i-1$. By iterating capacity $w$ backwards from $W$ down to $w_i$, "
                           "the table collapses to a single array $dp[w] = \\max(dp[w], v_i + dp[w - w_i])$, reducing memory from $\\Theta(n \\cdot W)$ to $O(W)$ while strictly preventing duplicate inclusion.<br/><br/>"
                           "<b>Matrix Chain Multiplication (MCM):</b><br/>"
                           "Determines the optimal parenthesization for evaluating a sequence of $n$ issue database join queries $A_1 \\dots A_n$. Recurrence: "
                           "$m[i, j] = \\min_{i \\le k < j} (m[i, k] + m[k+1, j] + p_{i-1}p_k p_j)$ in $\\Theta(n^3)$ time and $\\Theta(n^2)$ space.<br/><br/>"
                           "<b>Longest Common Subsequence (LCS):</b><br/>"
                           "Computes duplicate bug report stack trace similarity. Recurrence: "
                           "$c[i, j] = c[i-1, j-1] + 1$ if $X[i] == Y[j]$, else $\\max(c[i-1, j], c[i, j-1])$. Time: $\\Theta(m \\cdot n)$.<br/><br/>"
                           "<b>Optimal Binary Search Tree (OBST):</b><br/>"
                           "Constructs an optimal search tree for keyword lookups with non-uniform search frequencies $p_i, q_i$ in $\\Theta(n^3)$ time.<br/><br/>"
                           "<b>Held-Karp Dynamic Programming (Traveling Salesperson Problem):</b><br/>"
                           "Finds the optimal closed inspection tour across $N$ critical microservice repositories. Uses subset bitmasks: "
                           "$C(S, j) = \\min_{i \\in S, i \\neq j} (C(S \\setminus \\{j\\}, i) + d_{ij})$. Time complexity is $\\Theta(n^2 2^n)$, vastly outperforming brute-force $O(n!)$ search.", body_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 10: 4. ALGORITHMIC DESIGN (Part 3: Units V & VI)
    # ==========================================
    story.append(Paragraph("4. ALGORITHMIC DESIGN (Cont. - Units V & VI)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("4.5 Backtracking (Unit V)", h2_style))
    story.append(Paragraph("<b>N-Queens Problem (Reviewer Conflict Minimization):</b><br/>"
                           "Places $N$ reviewers on an $N \\times N$ expertise grid such that no two reviewers share a row, column, or diagonal. "
                           "Implemented using recursive depth-first backtracking with bitmasks (<code>col_mask</code>, <code>diag1_mask</code>, <code>diag2_mask</code>) "
                           "for $O(1)$ safety checks, exploring valid permutation branches while pruning invalid states early.<br/><br/>"
                           "<b>Sum of Subsets (Residual Sprint Hour Packing):</b><br/>"
                           "Given developer residual hours and backlog issue weights, finds all subsets summing exactly to capacity target $K$. "
                           "Employs sorted bounding: if current sum plus $w_i > K$ or current sum plus remaining weight $< K$, the subtree is pruned ($O(2^n)$ worst-case).<br/><br/>"
                           "<b>0/1 Knapsack Backtracking:</b><br/>"
                           "Explores the inclusion/exclusion state-space tree. At each node, calculates the continuous Fractional Knapsack upper bound of remaining items. "
                           "If the upper bound does not exceed the current best discrete value, the entire subtree is immediately pruned.", body_style))

    story.append(Paragraph("4.6 Branch & Bound (Unit V)", h2_style))
    story.append(Paragraph("<b>Knapsack Branch & Bound (FIFO vs LIFO vs Least-Cost):</b><br/>"
                           "Branch and Bound systematically explores the discrete state space using bounding relaxations:<br/>"
                           "• <i>FIFO B&B:</i> Explores states breadth-first using a standard queue.<br/>"
                           "• <i>LIFO B&B:</i> Explores states depth-first using a stack.<br/>"
                           "• <i>Least-Cost (LC) B&B:</i> Best-First search guided by a max-priority queue ordered by upper bound (fractional relaxation). "
                           "Nodes with higher theoretical promise are expanded first, rapidly establishing a high discrete lower bound that allows aggressive pruning of inferior subtrees.<br/>"
                           "• <i>Empirical Pruning Proof:</i> In our benchmarks, LC B&B expands only 8 nodes (pruning 5 branches), whereas FIFO expands 15 nodes and LIFO expands 9 nodes.<br/><br/>"
                           "<b>TSP Branch & Bound (Reduced Cost Matrix):</b><br/>"
                           "Computes a lower bound on tour cost by row and column reduction of the distance matrix, bounding branches whose lower bound exceeds current best tour.", body_style))

    story.append(Paragraph("4.7 Maximum Flow & Bipartite Matching (Unit VI)", h2_style))
    story.append(Paragraph("<b>Maximum Bipartite Matching (Kuhn's Augmenting Path Algorithm):</b><br/>"
                           "Models developer-issue assignment as an undirected bipartite graph $G = (U, V, E)$ where $U$ represents issues, $V$ represents developers, "
                           "and an edge $(u, v) \\in E$ exists if and only if $\\mathcal{S}_u \\subseteq \\mathcal{K}_v$.<br/>"
                           "• <i>Augmenting Path Mechanics:</i> A path $P$ is augmenting with respect to matching $M$ if it starts and ends at unmatched vertices and alternates between non-matching and matching edges. "
                           "By Berge's Lemma, a matching $M$ is maximum if and only if $G$ contains no augmenting path.<br/>"
                           "• <i>Algorithm Steps:</i> For each issue $u \\in U$, execute DFS to find an augmenting path. If found, invert edge membership along $P$, incrementing $|M|$ by 1. "
                           "Time complexity is $O(|U| \\cdot |E|) = O(V \\cdot E)$.<br/>"
                           "• <i>Model Separation:</i> Standard bipartite matching solves one-to-one assignment (at most one issue per developer). Multi-task capacity allocation "
                           "is solved separately using greedy heuristic packing or discrete knapsack dynamic programming.<br/><br/>"
                           "<b>Edmonds-Karp Network Flow:</b><br/>"
                           "Solves general capacity network flow by finding shortest augmenting paths using Breadth First Search (BFS) in $O(V \\cdot E^2)$ time.", body_style))

    story.append(Paragraph("4.8 Chinese Remainder Theorem (Unit VI)", h2_style))
    story.append(Paragraph("Used in distributed git mirror synchronization to recover global commit sequence timestamps from modular logs. "
                           "Given pairwise coprime moduli $m_1, m_2, \\dots, m_k$ and remainders $a_1, \\dots, a_k$, CRT computes $M = \\prod m_i$ and "
                           "$x = \\sum a_i M_i y_i \\pmod M$, where $M_i = M/m_i$ and $y_i = M_i^{-1} \\pmod{m_i}$ computed via Extended Euclidean Algorithm ($O(k \\log M)$).", body_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 11: 4. ALGORITHMIC DESIGN (Part 4: Strings & Reductions)
    # ==========================================
    story.append(Paragraph("4. ALGORITHMIC DESIGN (Cont. - Strings & Reductions)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("4.9 String Matching Automata (Unit VI)", h2_style))
    story.append(Paragraph("AutoTriage implements a 4-way string matching suite to mine crash logs for error tokens and CVE signatures:<br/>"
                           "1. <b>Naive Matcher:</b> Compares pattern at all text offsets; worst-case time $\\Theta((n-m+1)m)$.<br/>"
                           "2. <b>Rabin-Karp:</b> Uses rolling polynomial hash $H = (d \\cdot H + c) \\pmod q$. Average time $\\Theta(n+m)$, worst-case $O(nm)$.<br/>"
                           "3. <b>Finite Automata (DFA):</b> Precomputes state transition table $\\delta(q, a)$; scans text in strictly $\\Theta(n)$ time with zero backtracks.<br/>"
                           "4. <b>Knuth-Morris-Pratt (KMP):</b> Precomputes prefix function $\\pi[q] = \\max \\{k : k < q \\text{ and } P_k \\sqsupset P_q\\}$ in $\\Theta(m)$ time. "
                           "During text scanning, when a mismatch occurs, the text pointer never retreats; instead, the pattern shifts to index $\\pi[q]$. Scans in deterministic linear $\\Theta(n)$ time.", body_style))

    story.append(Paragraph("4.10 Complexity Classes & Polynomial Reduction (Unit VI)", h2_style))
    story.append(Paragraph("<b>Formal Polynomial Reduction ($\\text{Subset-Sum} \\le_P \\text{0/1 Knapsack}$):</b><br/>"
                           "• <i>Mapping Construction:</i> Given an instance of the NP-complete Subset-Sum problem $\\langle S = \\{s_1, \\dots, s_n\\}, K \\rangle$, "
                           "we construct in $O(n)$ deterministic time a 0/1 Knapsack instance $\\langle w, v, W \\rangle$ by setting:<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;$w_i = s_i, \\quad v_i = s_i \\quad \\forall i \\in \\{1, \\dots, n\\}, \\quad \\text{and} \\quad W = K$.<br/>"
                           "• <i>Equivalence Proof:</i> $(\\Rightarrow)$ If $S' \\subseteq S$ sums to $K$, selecting the corresponding items yields weight $\\sum_{i \\in S'} w_i = K \\le W$ "
                           "and total value $\\sum_{i \\in S'} v_i = K$. $(\\Leftarrow)$ If a knapsack packing achieves value $\\ge K$ with weight $\\le K$, since $v_i = w_i$, "
                           "the total value equals the total weight, which must equal $K$, forming an exact subset sum.<br/>"
                           "• <i>Verification Complexity:</i> The reduction transformation runs in $O(n)$ time. The verification test executes independent exact solvers "
                           "(Subset-Sum backtracking in $O(2^n)$ and Knapsack DP in $O(n \\cdot W)$), validating the equivalence in $O(2^n + nW)$ demonstration time.", body_style))

    story.append(Paragraph("4.11 Online Streaming Competitive Analysis (Empirical Evaluation)", h2_style))
    story.append(Paragraph("In dynamic environments, issues arrive sequentially over an 80-hour sprint without future visibility. "
                           "AutoTriage includes an event-driven online streaming engine that dispatches tickets in real time. "
                           "When a critical zero-day vulnerability arrives, the engine invokes immediate task preemption to reassign maintainers. "
                           "We evaluate online performance against the optimal offline schedule via the empirical Competitive Ratio: "
                           "$\\text{CR} = \\text{Value}(\\text{Online}) / \\text{Value}(\\text{Offline})$. In Scenario 4, the engine achieves an empirical $\\text{CR} = 1.0000$.", body_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 12: 5. PROJECT-50 DOMAIN MAPPING
    # ==========================================
    story.append(Paragraph("5. PROJECT-50 DOMAIN MAPPING", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph("Every algorithm implemented in AutoTriage maps directly to an engineering function within the issue triage and developer scheduling domain:", body_style))
    
    mapping_data = [
        [Paragraph("Algorithm", tbl_hdr), Paragraph("DAA Unit", tbl_hdr), Paragraph("Asymptotic Time", tbl_hdr), Paragraph("Domain Role in AutoTriage-DAA", tbl_hdr)],
        [Paragraph("Multi-Key Merge Sort", tbl_cell_bold), Paragraph("Unit I", tbl_cell), Paragraph("$\\Theta(n \\log n)$", tbl_cell), Paragraph("Stable backlog triage by Severity $\\downarrow$, SLA Deadline $\\uparrow$, ID $\\uparrow$.", tbl_cell)],
        [Paragraph("Median-of-3 Quick Sort", tbl_cell_bold), Paragraph("Unit I", tbl_cell), Paragraph("Avg $\\Theta(n \\log n)$", tbl_cell), Paragraph("In-place backlog sorting; mitigates quadratic sorted degradation.", tbl_cell)],
        [Paragraph("Binary Search (Iter/Rec)", tbl_cell_bold), Paragraph("Unit I", tbl_cell), Paragraph("$O(\\log n)$", tbl_cell), Paragraph("Instant $O(\\log n)$ ticket lookup by unique issue ID.", tbl_cell)],
        [Paragraph("Strassen Matrix Mult", tbl_cell_bold), Paragraph("Unit II", tbl_cell), Paragraph("$\\Theta(n^{2.807})$", tbl_cell), Paragraph("Developer co-maintenance intensity matrix ($M = C \\cdot C^T$).", tbl_cell)],
        [Paragraph("Kadane's Algorithm", tbl_cell_bold), Paragraph("Unit II", tbl_cell), Paragraph("$\\Theta(n)$", tbl_cell), Paragraph("Detects sprint bug surge and developer burnout windows from daily net churn.", tbl_cell)],
        [Paragraph("Fast Powering ($a^k$)", tbl_cell_bold), Paragraph("Unit II", tbl_cell), Paragraph("$\\Theta(\\log k)$", tbl_cell), Paragraph("Predicts multi-sprint ticket lifecycle Markov transition probabilities ($P^k$).", tbl_cell)],
        [Paragraph("Celebrity Problem", tbl_cell_bold), Paragraph("Unit II", tbl_cell), Paragraph("$\\Theta(n)$", tbl_cell), Paragraph("Identifies core maintainer / code review bottleneck in linear time.", tbl_cell)],
        [Paragraph("Fractional Knapsack", tbl_cell_bold), Paragraph("Unit III", tbl_cell), Paragraph("$O(n \\log n)$", tbl_cell), Paragraph("Emergency triage upper-bound relaxation under divisible QA hours.", tbl_cell)],
        [Paragraph("Activity Selection", tbl_cell_bold), Paragraph("Unit III", tbl_cell), Paragraph("$O(n \\log n)$", tbl_cell), Paragraph("Schedules maximum non-overlapping 1-on-1 review sessions for maintainer.", tbl_cell)],
        [Paragraph("Interval Partitioning", tbl_cell_bold), Paragraph("Unit III", tbl_cell), Paragraph("$O(n \\log n)$", tbl_cell), Paragraph("Allocates concurrent automated test suites across minimum CI servers.", tbl_cell)],
        [Paragraph("Huffman Coding", tbl_cell_bold), Paragraph("Unit III", tbl_cell), Paragraph("$O(n \\log \\Sigma)$", tbl_cell), Paragraph("Lossless offline compression for crash stack traces and git diff telemetry.", tbl_cell)],
        [Paragraph("Dijkstra's Algorithm", tbl_cell_bold), Paragraph("Unit III", tbl_cell), Paragraph("$O((V+E)\\log V)$", tbl_cell), Paragraph("Finds minimum refactoring risk path bypassing locked repository modules.", tbl_cell)],
        [Paragraph("Kruskal & Prim MST", tbl_cell_bold), Paragraph("Unit III", tbl_cell), Paragraph("$O(E \\log E)$", tbl_cell), Paragraph("Extracts essential module dependency refactoring backbone tree.", tbl_cell)],
        [Paragraph("0/1 Knapsack (2D & 1D)", tbl_cell_bold), Paragraph("Unit IV", tbl_cell), Paragraph("$\\Theta(n \\cdot W)$", tbl_cell), Paragraph("Optimal discrete sprint release package maximizing business value under capacity.", tbl_cell)],
        [Paragraph("Matrix Chain Mult", tbl_cell_bold), Paragraph("Unit IV", tbl_cell), Paragraph("$\\Theta(n^3)$", tbl_cell), Paragraph("Optimizes database join query execution sequences for issue metadata.", tbl_cell)],
        [Paragraph("LCS Dynamic Prog", tbl_cell_bold), Paragraph("Unit IV", tbl_cell), Paragraph("$\\Theta(m \\cdot n)$", tbl_cell), Paragraph("Clusters duplicate bug reports and scores stack trace similarities.", tbl_cell)],
        [Paragraph("Optimal BST (OBST)", tbl_cell_bold), Paragraph("Unit IV", tbl_cell), Paragraph("$\\Theta(n^3)$", tbl_cell), Paragraph("Minimizes expected lookup cost for non-uniform issue triage tags.", tbl_cell)],
        [Paragraph("Bellman-Ford", tbl_cell_bold), Paragraph("Unit IV", tbl_cell), Paragraph("$\\Theta(V \\cdot E)$", tbl_cell), Paragraph("Single-source shortest path and technical debt cycle detection.", tbl_cell)],
        [Paragraph("Floyd-Warshall", tbl_cell_bold), Paragraph("Unit IV", tbl_cell), Paragraph("$\\Theta(V^3)$", tbl_cell), Paragraph("All-pairs reachability and repository blast-radius impact analysis.", tbl_cell)],
        [Paragraph("TSP (Held-Karp DP)", tbl_cell_bold), Paragraph("Unit IV", tbl_cell), Paragraph("$\\Theta(n^2 2^n)$", tbl_cell), Paragraph("Optimal closed microservice security audit tour for lead maintainer.", tbl_cell)],
        [Paragraph("N-Queens Backtracking", tbl_cell_bold), Paragraph("Unit V", tbl_cell), Paragraph("$O(N!)$", tbl_cell), Paragraph("Constraint satisfaction benchmark for conflict-free reviewer placement.", tbl_cell)],
        [Paragraph("Sum of Subsets", tbl_cell_bold), Paragraph("Unit V", tbl_cell), Paragraph("$O(2^n)$", tbl_cell), Paragraph("Identifies exact ticket combinations that fill residual sprint capacity.", tbl_cell)],
        [Paragraph("Knapsack LC B&B", tbl_cell_bold), Paragraph("Unit V", tbl_cell), Paragraph("Worst $O(2^n)$", tbl_cell), Paragraph("Prunes unpromising release packages; dominates FIFO/LIFO in expanded nodes.", tbl_cell)],
        [Paragraph("TSP Branch & Bound", tbl_cell_bold), Paragraph("Unit V", tbl_cell), Paragraph("Worst $O(n!)$", tbl_cell), Paragraph("Exact microservice inspection solver using Reduced Cost Matrices.", tbl_cell)],
        [Paragraph("Edmonds-Karp Max Flow", tbl_cell_bold), Paragraph("Unit VI", tbl_cell), Paragraph("$O(V E^2)$", tbl_cell), Paragraph("Analyzes maximum repository task throughput across multi-tier teams.", tbl_cell)],
        [Paragraph("Bipartite Matching", tbl_cell_bold), Paragraph("Unit VI", tbl_cell), Paragraph("$O(V \\cdot E)$", tbl_cell), Paragraph("1-to-1 developer assignment via Kuhn's augmenting path algorithm.", tbl_cell)],
        [Paragraph("Chinese Remainder Thm", tbl_cell_bold), Paragraph("Unit VI", tbl_cell), Paragraph("$O(k \\log M)$", tbl_cell), Paragraph("Synchronizes distributed commit event logs across decentralized mirrors.", tbl_cell)],
        [Paragraph("4-Way String Matchers", tbl_cell_bold), Paragraph("Unit VI", tbl_cell), Paragraph("KMP $\\Theta(n+m)$", tbl_cell), Paragraph("Scans crash logs for CVE vulnerability signatures and error tokens.", tbl_cell)],
        [Paragraph("P/NP Reduction", tbl_cell_bold), Paragraph("Unit VI", tbl_cell), Paragraph("Mapping $O(n)$", tbl_cell), Paragraph("Formal equivalence verifier: $\\text{Subset-Sum} \\le_P \\text{0/1 Knapsack}$.", tbl_cell)],
    ]
    t_map = Table(mapping_data, colWidths=[110, 50, 70, 274])
    t_map.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_map)

    story.append(PageBreak())

    # ==========================================
    # PAGE 13: 6. IMPLEMENTATION DETAILS
    # ==========================================
    story.append(Paragraph("6. IMPLEMENTATION DETAILS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("6.1 Core C++17 Architectural Modules", h2_style))
    story.append(Paragraph("AutoTriage-DAA is authored strictly in standard ISO C++17 with zero third-party dependencies. "
                           "The codebase is modularized into cleanly separated header and source files across Phase I and Phase II:<br/>"
                           "• <code>models.hpp</code>: Encapsulates domain structs (Issue, Developer, SortStats, MatchingStats) and skill matching predicates.<br/>"
                           "• <code>parser.hpp</code>: Implements defensive CSV parsing, field sanitation, and graph cycle detection.<br/>"
                           "• <code>sorting.hpp</code>: Multi-key stable Merge Sort, Median-of-Three Quick Sort, and iterative/recursive Binary Search.<br/>"
                           "• <code>bipartite_matching.hpp</code>: Implements Kuhn's augmenting path algorithm and developer compatibility graph builder.<br/>"
                           "• <code>knapsack_01.hpp</code>: Implements 2D dynamic programming and memory-optimized 1D vector DP.<br/>"
                           "• <code>knapsack_branch_and_bound.hpp</code>: FIFO, LIFO, and Least-Cost Branch and Bound state-space search solvers.<br/>"
                           "• <code>online_triage.hpp</code>: Event-driven online streaming simulator with immediate zero-day task preemption.<br/>"
                           "• <code>report_exporter.hpp</code>: Telemetry export engine writing actual runtime variables directly to CSV.", body_style))

    story.append(Paragraph("6.2 Defensive Parsing & 3-Color DFS Cycle Trapping", h2_style))
    story.append(Paragraph("In open-source issue trackers, invalid issue dependencies frequently cause infinite recursion or deadlocks "
                           "(e.g., Issue #1 requires #2, and #2 requires #1). AutoTriage's parser traps such cycles during ingestion using a 3-color Depth First Search "
                           "(0: White / Unvisited, 1: Gray / Visiting, 2: Black / Visited). When a traversal encounters a node currently marked Gray, "
                           "a back-edge is trapped, immediately halting ingestion with an informative error message:", body_style))
    
    code_dfs = ("bool dfs_cycle(int u, const std::vector<std::vector<int>>& adj,\n"
                "               std::vector<int>& color, std::string& err) {\n"
                "    color[u] = 1; // Mark GRAY (currently visiting in recursion stack)\n"
                "    for (int v : adj[u]) {\n"
                "        if (color[v] == 1) {\n"
                "            err = \"Dependency cycle detected involving issue ID \" + std::to_string(u);\n"
                "            return true; // Cycle trapped!\n"
                "        }\n"
                "        if (color[v] == 0 && dfs_cycle(v, adj, color, err)) return true;\n"
                "    }\n"
                "    color[u] = 2; // Mark BLACK (fully explored)\n"
                "    return false;\n"
                "}")
    story.append(Paragraph(code_dfs.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

    story.append(Paragraph("6.3 Kuhn's Augmenting Path Implementation", h2_style))
    story.append(Paragraph("The bipartite matching engine implements Kuhn's augmenting path algorithm using depth-first search:", body_style))
    
    code_kuhn = ("bool try_kuhn(int u, const std::vector<std::vector<int>>& adj,\n"
                 "              std::vector<bool>& used, std::vector<int>& match) {\n"
                 "    if (used[u]) return false;\n"
                 "    used[u] = true;\n"
                 "    for (int v : adj[u]) {\n"
                 "        if (match[v] < 0 || try_kuhn(match[v], adj, used, match)) {\n"
                 "            match[v] = u; // Invert matching along augmenting path\n"
                 "            return true;\n"
                 "        }\n"
                 "    }\n"
                 "    return false;\n"
                 "}")
    story.append(Paragraph(code_kuhn.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

    story.append(Paragraph("6.4 Build System & Compilation Standard", h2_style))
    story.append(Paragraph("The repository enforces strict ISO C++17 across both Phase I and Phase II using dual build systems:<br/>"
                           "• <b>CMake Build:</b> <code>CMakeLists.txt</code> enforces <code>set(CMAKE_CXX_STANDARD 17)</code> with <code>CMAKE_CXX_STANDARD_REQUIRED ON</code>.<br/>"
                           "• <b>GNU Make Build:</b> <code>Makefile</code> invokes <code>g++ -std=c++17 -O3 -Wall -Wextra</code>.<br/>"
                           "Compiling all 10 binaries (main executable, 6 test runners, and scenario benchmark runner) completes with <b>zero errors and zero warnings</b>.", body_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 14: 7. TESTING & VERIFICATION
    # ==========================================
    story.append(Paragraph("7. TESTING & VERIFICATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("AutoTriage-DAA features a comprehensive automated testing framework consisting of <b>27 distinct test suites</b> "
                           "distributed across 6 standalone test binaries. Every suite executes automated assertion checks against theoretical invariants.", body_style))

    story.append(Paragraph("7.1 Testing Taxonomies & Coverage", h2_style))
    story.append(Paragraph("The test framework validates behavior across five standardized testing categories:<br/>"
                           "1. <b>Normal Cases:</b> Typical sprint backlogs with standard developer skills and non-conflicting workloads.<br/>"
                           "2. <b>Boundary Cases:</b> Single-issue backlogs ($N=1$), empty developer pools ($M=0$), zero-hour capacity limits, and exact capacity fits.<br/>"
                           "3. <b>Invalid Cases:</b> Malformed CSV records, non-numeric estimated hours, missing fields, and out-of-range severity levels ($sev < 1$ or $sev > 5$).<br/>"
                           "4. <b>Adversarial Cases:</b> Pre-sorted arrays designed to trigger worst-case Quick Sort partitioning; pathological repetitive strings ('AAAA...B') designed to trigger $O(nm)$ Naive string matcher degradation.<br/>"
                           "5. <b>Stress Cases:</b> Large synthetic enterprise datasets (120 issues, 16 developers) and circular prerequisite graphs.", body_style))

    story.append(Paragraph("7.2 Automated Test Execution Summary", h2_style))
    
    test_summary_data = [
        [Paragraph("Binary / Test Suite", tbl_hdr), Paragraph("Unit / Paradigm", tbl_hdr), Paragraph("Test Invariants & Assertions Verified", tbl_hdr), Paragraph("Status", tbl_hdr)],
        [Paragraph("Phase I test_runner.exe", tbl_cell_bold), Paragraph("Phase I Core", tbl_cell), Paragraph("7 suites: Merge Sort stability, Quick Sort pre-sorted defense, Kuhn Bipartite Matching vs Greedy, Binary Search (iter/rec), Invalid Input Rejection, Boundary Ingestion, Prerequisite Cycle Trap.", tbl_cell), Paragraph("7/7 PASSED", tbl_cell_bold)],
        [Paragraph("Phase II test_chunk2_dnc.exe", tbl_cell_bold), Paragraph("Unit II: D&C", tbl_cell), Paragraph("4 suites: Strassen 4x4 matrix multiplication ($O(n^{2.807})$), Kadane maximum subarray, Fast power $2^{10}=1024$, Celebrity maintainer identification in 12 comparisons.", tbl_cell), Paragraph("4/4 PASSED", tbl_cell_bold)],
        [Paragraph("Phase II test_chunk3_greedy.exe", tbl_cell_bold), Paragraph("Unit III: Greedy", tbl_cell), Paragraph("6 suites: Fractional Knapsack ($240 for 50h), Activity Selection (4 sessions), Interval Partitioning (3 CI servers), Huffman Coding (2.007x compression), Dijkstra (path 0->4 dist 11), Kruskal vs Prim MST (cost 16).", tbl_cell), Paragraph("6/6 PASSED", tbl_cell_bold)],
        [Paragraph("Phase II test_chunk4_dp.exe", tbl_cell_bold), Paragraph("Unit IV: DP", tbl_cell), Paragraph("7 suites: 0/1 Knapsack 2D vs 1D ($220), MCM (30,000 mults), LCS ('BCBA' 61.5% similarity), OBST (cost 1.9), Bellman-Ford negative cycle trap, Floyd-Warshall blast radius, Held-Karp TSP (cost 80).", tbl_cell), Paragraph("7/7 PASSED", tbl_cell_bold)],
        [Paragraph("Phase II test_chunk5_backtracking_bb.exe", tbl_cell_bold), Paragraph("Unit V: Backtracking/B&B", tbl_cell), Paragraph("5 suites: N-Queens (N=4: 2 solns, N=8: 92 solns), Sum of Subsets (4 combinations), Knapsack Backtracking ($220), Knapsack B&B (FIFO vs LIFO vs LC, LC prunes most), TSP B&B (cost 80, 5 pruned).", tbl_cell), Paragraph("5/5 PASSED", tbl_cell_bold)],
        [Paragraph("Phase II test_chunk6_flow_strings_crt.exe", tbl_cell_bold), Paragraph("Unit VI: Flow/Strings/CRT", tbl_cell), Paragraph("5 suites: Edmonds-Karp Max Flow (19.0), Bipartite Flow Matching (3/3), Chinese Remainder Theorem ($x=23 \\pmod{105}$), 4-Way String Matchers (offsets 0 & 63), Complexity Reduction (Subset-Sum $\\le_P$ Knapsack).", tbl_cell), Paragraph("5/5 PASSED", tbl_cell_bold)],
    ]
    t_tests = Table(test_summary_data, colWidths=[120, 75, 235, 74])
    t_tests.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_tests)

    story.append(PageBreak())

    # ==========================================
    # PAGE 15: 8. ALGORITHM COMPARISON & EMPIRICAL ANALYSIS
    # ==========================================
    story.append(Paragraph("8. ALGORITHM COMPARISON & EMPIRICAL ANALYSIS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("8.1 Sorting Performance Under Adversarial Ordering", h2_style))
    story.append(Paragraph("To evaluate sorting resilience against adversarial inputs, we benchmarked Lomuto First-Pivot Quick Sort, "
                           "Median-of-Three Quick Sort, and Multi-Key Merge Sort over an identical pre-sorted array of $N = 5,000$ elements:", body_style))
    
    sort_comp = [
        [Paragraph("Algorithm Strategy", tbl_hdr), Paragraph("Pivot Selection Rule", tbl_hdr), Paragraph("Comparisons ($N=5000$)", tbl_hdr), Paragraph("Stability", tbl_hdr), Paragraph("Observed Asymptotic Bound", tbl_hdr)],
        [Paragraph("Lomuto Quick Sort", tbl_cell), Paragraph("First Element ($A[\\text{low}]$)", tbl_cell), Paragraph("12,497,500", tbl_cell), Paragraph("No", tbl_cell), Paragraph("$\\Theta(n^2)$ (Degraded)", tbl_cell)],
        [Paragraph("Median-of-3 Quick Sort", tbl_cell_bold), Paragraph("Median($A[\\text{low}], A[\\text{mid}], A[\\text{high}]$)", tbl_cell_bold), Paragraph("60,678", tbl_cell_bold), Paragraph("No", tbl_cell_bold), Paragraph("$\\Theta(n \\log n)$ (Mitigated)", tbl_cell_bold)],
        [Paragraph("Multi-Key Merge Sort", tbl_cell_bold), Paragraph("Divide at Midpoint ($N/2$)", tbl_cell_bold), Paragraph("51,420", tbl_cell_bold), Paragraph("Yes (Strict)", tbl_cell_bold), Paragraph("$\\Theta(n \\log n)$ (Optimal)", tbl_cell_bold)],
    ]
    t_sort = Table(sort_comp, colWidths=[110, 115, 95, 60, 124])
    t_sort.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_sort)
    story.append(Spacer(1, 5))
    story.append(Paragraph("<i>Empirical Finding:</i> Median-of-Three pivot selection drastically reduced comparisons from 12.5 million down to 60,678, "
                           "closely matching Merge Sort's 51,420 comparisons and completely mitigating quadratic collapse on sorted inputs.", body_style))

    story.append(Paragraph("8.2 Search Automata on Pathological Crash Logs", h2_style))
    story.append(Paragraph("String matching algorithms were tested on a 50,001-character pathological crash log consisting of 50,000 repeated 'A's "
                           "terminated by a single 'B', searching for the pattern 'AAAAB':", body_style))
    
    str_comp = [
        [Paragraph("String Matcher Algorithm", tbl_hdr), Paragraph("Comparisons Performed", tbl_hdr), Paragraph("Execution Time (us)", tbl_hdr), Paragraph("Text Pointer Backtracks", tbl_hdr)],
        [Paragraph("Naive String Matcher", tbl_cell), Paragraph("299,976", tbl_cell), Paragraph("537 us", tbl_cell), Paragraph("Frequent ($O(n \\cdot m)$)", tbl_cell)],
        [Paragraph("Rabin-Karp Rolling Hash", tbl_cell), Paragraph("6 (Hash filtered)", tbl_cell), Paragraph("389 us", tbl_cell), Paragraph("Zero backtracks", tbl_cell)],
        [Paragraph("Finite Automata (DFA)", tbl_cell), Paragraph("50,001", tbl_cell), Paragraph("178 us", tbl_cell), Paragraph("Strictly Zero (Deterministic)", tbl_cell)],
        [Paragraph("Knuth-Morris-Pratt (KMP)", tbl_cell_bold), Paragraph("100,005", tbl_cell_bold), Paragraph("210 us", tbl_cell_bold), Paragraph("Strictly Zero (Prefix Table)", tbl_cell_bold)],
    ]
    t_str = Table(str_comp, colWidths=[150, 110, 110, 134])
    t_str.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_str)
    story.append(Spacer(1, 5))
    story.append(Paragraph("<i>Empirical Finding:</i> KMP executed in 100,005 operations without a single backward movement of the text pointer, "
                           "outperforming Naive matching (299,976 operations) by a factor of 3x.", body_style))

    story.append(Paragraph("8.3 Branch & Bound State-Space Pruning Efficiency", h2_style))
    story.append(Paragraph("To evaluate branch-and-bound exploration strategies, we benchmarked FIFO (breadth-first), LIFO (depth-first), and "
                           "Least-Cost (LC) Branch and Bound on an identical 0/1 knapsack instance ($N = 4, W = 15$ hours):", body_style))
    
    bb_comp = [
        [Paragraph("Branch & Bound Strategy", tbl_hdr), Paragraph("Data Structure", tbl_hdr), Paragraph("Nodes Generated", tbl_hdr), Paragraph("Nodes Expanded", tbl_hdr), Paragraph("Branches Pruned", tbl_hdr)],
        [Paragraph("FIFO Branch & Bound", tbl_cell), Paragraph("Standard Queue", tbl_cell), Paragraph("19", tbl_cell), Paragraph("15", tbl_cell), Paragraph("2", tbl_cell)],
        [Paragraph("LIFO Branch & Bound", tbl_cell), Paragraph("Standard Stack", tbl_cell), Paragraph("11", tbl_cell), Paragraph("9", tbl_cell), Paragraph("1", tbl_cell)],
        [Paragraph("Least-Cost (LC) B&B", tbl_cell_bold), Paragraph("Max-Priority Queue (Bound)", tbl_cell_bold), Paragraph("11", tbl_cell_bold), Paragraph("8", tbl_cell_bold), Paragraph("5 (Pruned Most)", tbl_cell_bold)],
    ]
    t_bb = Table(bb_comp, colWidths=[130, 110, 85, 85, 94])
    t_bb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_bb)
    story.append(Spacer(1, 5))
    story.append(Paragraph("<i>Empirical Finding:</i> Guided by fractional upper bounds, Least-Cost B&B expanded only 8 nodes and pruned 5 branches, "
                           "empirically validating the superiority of best-first search over blind queue/stack exploration.", body_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 16: 9. DEMONSTRATION SCENARIOS
    # ==========================================
    story.append(Paragraph("9. DEMONSTRATION SCENARIOS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph("AutoTriage-DAA includes four mandatory real-world demonstration scenarios executed via <code>scenario_benchmarks.exe</code>, "
                           "validating algorithmic behavior across distinct operational environments:", body_style))
    
    scen_data = [
        [Paragraph("Scenario", tbl_hdr), Paragraph("Operational Context", tbl_hdr), Paragraph("Algorithms Evaluated", tbl_hdr), Paragraph("Measured Results & Defensible Findings", tbl_hdr)],
        [Paragraph("Scenario 1: Normal Sprint", tbl_cell_bold), Paragraph("50 issues, 10 developers (40h capacity each, $W=120\\text{h}$ sprint budget)", tbl_cell),
         Paragraph("Max Bipartite Matching vs Greedy;<br/>0/1 Knapsack DP vs Fractional", tbl_cell),
         Paragraph("• 1-to-1 Bipartite: 10/10 devs utilized (100%), 10/50 issues assigned (20%).<br/>• 0/1 Knapsack DP selects 16 issues yielding 1244 points; Fractional bound = 1244.69 points.", tbl_cell)],
        [Paragraph("Scenario 2: Capacity Shock", tbl_cell_bold), Paragraph("Zero-day vulnerability disclosure; 50% devs on emergency leave; capacity slashed to 80h; 15 critical bugs", tbl_cell),
         Paragraph("0/1 Knapsack DP vs LC B&B;<br/>Dijkstra Refactoring Reroute", tbl_cell),
         Paragraph("• Both DP and LC B&B achieve exact discrete optimum: 730 points.<br/>• LC B&B prunes 20 state-space nodes.<br/>• Dijkstra identifies bypass refactoring route with cost = 29.0.", tbl_cell)],
        [Paragraph("Scenario 3: Stress & Attack", tbl_cell_bold), Paragraph("5,000 pre-sorted array; 50,001-char pathological repetitive crash log", tbl_cell),
         Paragraph("Median-of-3 Quick Sort vs Merge;<br/>4-Way String Matchers", tbl_cell),
         Paragraph("• Median-3 Quick Sort: 60,678 comparisons vs Merge Sort 51,420.<br/>• KMP: 100,005 comparisons (0 backtracks) vs Naive 299,976 comparisons.", tbl_cell)],
        [Paragraph("Scenario 4: Synthetic Enterprise & Streaming", tbl_cell_bold), Paragraph("120 enterprise defect issues, 16 maintainers; 80h dynamic event stream with zero-day P0 arrival", tbl_cell),
         Paragraph("Sequential Online Streaming with Immediate CVE Preemption", tbl_cell),
         Paragraph("• Online streaming achieves empirical Competitive Ratio = 1.0000 relative to offline matching.<br/>• Triggered 7 immediate task preemptions, preserving zero-day SLA.", tbl_cell)],
    ]
    t_scen = Table(scen_data, colWidths=[90, 110, 105, 199])
    t_scen.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_scen)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Scenario 1 In-Depth: Normal Sprint Allocation</b><br/>"
                           "In Scenario 1, the triage backlog contains 50 issues and 10 developers. Kuhn's augmenting path algorithm finds a maximum matching "
                           "of 10 assignments. This achieves <b>100% developer utilization</b> (all 10 developers assigned) and <b>20% issue backlog coverage</b> "
                           "(10 of 50 issues assigned). The discrete 0/1 Knapsack optimizer packs 16 issues into the 120-hour sprint budget, yielding 1,244 business value points "
                           "(compared to the theoretical continuous relaxation bound of 1,244.69 points).", body_style))

    story.append(Paragraph("<b>Scenario 2 In-Depth: Emergency Capacity Shock</b><br/>"
                           "When 5 of 10 developers take emergency leave during a major zero-day exploit disclosure, capacity drops from 400 hours to 80 hours. "
                           "The 0/1 Knapsack dynamic program and the Least-Cost Branch and Bound solver both converge on the exact discrete optimum of 730 points. "
                           "LC Branch and Bound pruned 20 non-viable state-space nodes. Simultaneously, Dijkstra's shortest path rerouted module dependencies "
                           "around locked security submodules with a total path cost of 29.0.", body_style))

    story.append(Paragraph("<b>Scenario 3 In-Depth: Adversarial & Pathological Stress</b><br/>"
                           "Scenario 3 directly stress-tests algorithmic edge cases. On an adversarial sorted array of 5,000 integers, Lomuto Quick Sort collapsed to "
                           "12,497,500 comparisons. Median-of-Three Quick Sort performed 60,678 comparisons, matching Merge Sort's 51,420 comparisons. On the 50,001-character "
                           "pathological log, KMP performed 100,005 comparisons with strictly zero text pointer backtracks.", body_style))

    story.append(Paragraph("<b>Scenario 4 In-Depth: Synthetic Enterprise Backlog & Online Streaming</b><br/>"
                           "Scenario 4 processes a synthetic enterprise backlog of 120 issues across 16 developers. An event-driven online streaming engine "
                           "simulates real-time issue arrival over an 80-hour sprint. When a critical Severity-5 zero-day arrives, the engine immediately preempts "
                           "lower-priority tasks (executing 7 preemptions total) and matches the offline optimal schedule with an empirical Competitive Ratio of 1.0000.", body_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 17: 10. RESULTS & 11. LIMITATIONS
    # ==========================================
    story.append(Paragraph("10. EXPERIMENTAL RESULTS SUMMARY", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    p_res = ("Across all benchmarks, unit suites, and demonstration scenarios, the first-principles C++17 implementations fulfilled all theoretical asymptotic bounds "
             "and operational performance expectations:<br/>"
             "1. <b>Deterministic Triage:</b> Multi-key Merge Sort reliably prioritized backlogs in $\\Theta(n \\log n)$ time with zero stability inversions across all datasets.<br/>"
             "2. <b>Optimal 1-to-1 Matching:</b> Kuhn's augmenting path algorithm achieved provably maximum bipartite matching ($O(V \\cdot E)$), utilizing 100% of available developers in Scenario 1.<br/>"
             "3. <b>Exact Release Optimization:</b> Discrete 0/1 Knapsack DP achieved exact mathematical optima across all sprint capacities, with Least-Cost Branch & Bound matching the optimum while aggressively pruning 20 non-viable state-space nodes.<br/>"
             "4. <b>Defensive Linear Searching:</b> KMP search eliminated text pointer backtracking entirely on pathological logs, completing in linear time.<br/>"
             "5. <b>Streaming Competitive Performance:</b> Dynamic online streaming achieved an empirical competitive ratio of 1.0000 on synthetic enterprise workloads, preempting 7 lower-priority tasks to preserve zero-day response deadlines.")
    story.append(Paragraph(p_res, body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("11. SYSTEM LIMITATIONS & ALGORITHMIC BOUNDARIES", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph("To ensure honest academic evaluation, the operational and theoretical boundaries of AutoTriage-DAA are explicitly stated:", body_style))
    lims = [
        "<b>Model Separation Boundary:</b> Standard maximum bipartite matching solves one-to-one assignment (at most one issue per developer). It does not natively pack multiple tasks into a developer's 40-hour weekly capacity; multi-task capacity packing is handled as a separate engineering stage via greedy allocation or knapsack dynamic programming.",
        "<b>NP-Hard Scaling Bounds:</b> While 0/1 Knapsack DP operates in pseudo-polynomial time ($\\Theta(n \\cdot W)$), memory and runtime scale linearly with sprint budget $W$, becoming inefficient if capacities reach astronomical scales. Similarly, exact Held-Karp TSP DP ($\\Theta(n^2 2^n)$) is computationally prohibitive beyond $N \\approx 20$ repository modules due to exponential state-space explosion.",
        "<b>Worst-Case Quick Sort Boundary:</b> Median-of-Three pivot selection completely mitigates quadratic collapse on pre-sorted and reverse-sorted arrays, but theoretical worst-case remains $O(n^2)$ for adversarial permutations engineered specifically against the median rule.",
        "<b>Reduction Verification Horizon:</b> While the polynomial reduction mapping $\\text{Subset-Sum} \\le_P \\text{0/1 Knapsack}$ runs in deterministic $O(n)$ time, experimental verification requires solving the NP-complete problem independently, requiring exponential $O(2^n + nW)$ demonstration time."
    ]
    for lim in lims:
        story.append(Paragraph(f"• {lim}", bullet_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 18: 12. ETHICS, 13. FUTURE WORK, 14. CONCLUSION, REFERENCES
    # ==========================================
    story.append(Paragraph("12. ETHICAL, SOCIAL & SAFETY CONSIDERATIONS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    ethics = [
        "<b>Developer Workload Fairness & Burnout Prevention:</b> Pure optimization models can unfairly overload senior maintainers. AutoTriage incorporates workload damping thresholds to prevent chronic developer fatigue.",
        "<b>Mitigating Bias in Developer Skill Profiling:</b> Prevents algorithmic pigeonholing (where junior engineers receive only trivial bugs) by supporting shadow pairings and using arrival SLA for tie-breaking rather than seniority alone.",
        "<b>Preventing Severity Starvation:</b> Strict priority ordering can perpetually starve lower-severity maintenance tasks. AutoTriage incorporates a dynamic aging multiplier incrementing priority for each unassigned sprint.",
        "<b>Human-in-the-Loop Override:</b> Algorithmic assignments are advisory. AutoTriage generates explainable ASCII Gantt schedules and diagnostic logs, empowering maintainers to manually override assignments."
    ]
    for eth in ethics:
        story.append(Paragraph(f"• {eth}", bullet_style))

    story.append(Paragraph("13. FUTURE WORK & RESEARCH EXTENSIONS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph("Planned future research extensions include: (1) Formulating multi-developer, multi-issue assignment as an exact Generalized Assignment Problem (GAP) via Branch-and-Price; "
                           "(2) Integrating machine-learning NLP models for automated skill tag extraction from raw issue descriptions; and "
                           "(3) Compiling the C++17 core engine to WebAssembly for browser-based offline triage visualization.", body_style))

    story.append(Paragraph("14. CONCLUSION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph("AutoTriage-DAA establishes a rigorous, comprehensive bridge between theoretical algorithm design and practical software engineering. "
                           "By implementing all 46 curriculum topics from first principles in strict ISO C++17, maintaining verifiable empirical evidence, and adhering "
                           "to honest academic reporting standards, the project demonstrates total mastery of the Design and Analysis of Algorithms curriculum.", body_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("REFERENCES", h2_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=c_secondary, spaceBefore=2, spaceAfter=6))
    refs = [
        "[1] Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). <i>Introduction to Algorithms</i> (3rd ed.). MIT Press.",
        "[2] Kleinberg, J., & Tardos, E. (2006). <i>Algorithm Design</i>. Pearson Education.",
        "[3] Karp, R. M., Vazirani, U. V., & Vazirani, V. V. (1990). An optimal algorithm for on-line bipartite matching. <i>STOC '90</i>.",
        "[4] Edmonds, J., & Karp, R. M. (1972). Theoretical improvements in algorithmic efficiency for network flow problems. <i>JACM</i>.",
        "[5] Knuth, D. E., Morris, J. H., & Pratt, V. R. (1977). Fast pattern matching in strings. <i>SIAM Journal on Computing</i>."
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle('Ref', parent=styles['Normal'], fontSize=7.5, leading=10, textColor=colors.HexColor("#444444"), spaceAfter=2)))

    story.append(PageBreak())

    # ==========================================
    # PAGES 19–26: APPENDIX: TERMINAL SCREENSHOT GALLERY
    # ==========================================
    story.append(Paragraph("APPENDIX: TERMINAL SCREENSHOT GALLERY", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph("This appendix documents the live execution of AutoTriage-DAA under ISO C++17 via 16 high-resolution terminal captures. "
                           "Each entry details the binary invoked, commands issued, theoretical invariants tested, and verified empirical telemetry.", body_style))
    story.append(Spacer(1, 6))

    screenshots_info = [
        ("screenshots/01_main_menu.png", 
         "Figure 1: Main Interactive CLI Menu (Student Author & Modules 1–11)",
         "Binary: Phase_I/main.exe | Menu Selection Interface",
         "Displays verified student authorship banner (Ritigya Mishra, SAP ID: 590028115, Batch B-9 AI/ML), C++17 compiler confirmation, and all 11 interactive triage modules."),
        
        ("screenshots/02_backlog_sorting.png", 
         "Figure 2: Module 1 Multi-Key Merge Sort Backlog Triage & Telemetry",
         "Binary: Phase_I/main.exe | Submenu: [1] Prioritize Backlog",
         "Demonstrates stable three-tier sorting (Severity descending, Deadline ascending, ID tie-breaking) over incoming tickets with microsecond telemetry."),
        
        ("screenshots/03_developer_assignment.png", 
         "Figure 3: Module 2 Developer Bipartite Assignment via Kuhn Augmenting Paths",
         "Binary: Phase_I/main.exe | Submenu: [2] Match Developers",
         "Executes Kuhn's augmenting path algorithm ($O(V \\cdot E)$), reporting developer match status, skill coverage verification, and residual capacity."),
        
        ("screenshots/04_knapsack_comparison.png", 
         "Figure 4: Module 3 Sprint Release Optimization (0/1 DP vs LC Branch & Bound)",
         "Binary: Phase_I/main.exe | Submenu: [3] Optimize Sprint Release",
         "Computes discrete release subset under 120-hour sprint budget, comparing 2D dynamic programming against Least-Cost Branch and Bound and Fractional relaxation."),
        
        ("screenshots/05_invalid_input_validation.png", 
         "Figure 5: Defensive CSV Parser Trapping Out-of-Range Severity Bounds",
         "Binary: Phase_I/test_runner.exe | Suite: Invalid CSV Ingestion",
         "Validates RFC 4180 parsing robustness, intercepting corrupted issue records (severity 9 > 5, negative workload effort) with zero crashes or buffer overruns."),
        
        ("screenshots/06_cycle_detection.png", 
         "Figure 6: 3-Color DFS Graph Trapping Circular Prerequisite Backlog",
         "Binary: Phase_I/test_runner.exe | Suite: Dependency Cycle Trapping",
         "Constructs adjacency list and executes 3-color DFS traversal, successfully trapping back-edge on circular backlog (Issue #1 <-> #2) without stack overflow."),
        
        ("screenshots/07_phase1_tests.png", 
         "Figure 7: Phase I Automated Test Harness (All 7 Test Suites Passing)",
         "Binary: Phase_I/test_runner.exe | Complete Phase I Harness",
         "Executes 7 automated suites covering sorting stability, bipartite matching optimality, binary search, boundary ingestion, and cycle trapping (7/7 Passed)."),
        
        ("screenshots/08_divide_conquer_tests.png", 
         "Figure 8: Unit II Divide & Conquer Automated Test Suite (Chunk 2)",
         "Binary: Phase_II/test_chunk2_dnc.exe | Unit II Test Harness",
         "Validates Strassen 4x4 matrix multiplication ($O(n^{2.807})$), Kadane maximum subarray churn, fast power ($2^{10}=1024$), and celebrity identification in 12 checks (4/4 Passed)."),
        
        ("screenshots/09_greedy_tests.png", 
         "Figure 9: Unit III Greedy Methods Automated Test Suite (Chunk 3)",
         "Binary: Phase_II/test_chunk3_greedy.exe | Unit III Test Harness",
         "Validates Fractional Knapsack ($240 for 50h), Activity Selection (4 non-overlapping reviews), Interval Partitioning (3 CI servers), Huffman Coding (2.007x ratio), Dijkstra, and Kruskal vs Prim MST (6/6 Passed)."),
        
        ("screenshots/10_dp_tests.png", 
         "Figure 10: Unit IV Dynamic Programming Automated Test Suite (Chunk 4)",
         "Binary: Phase_II/test_chunk4_dp.exe | Unit IV Test Harness",
         "Validates 0/1 Knapsack 2D vs 1D ($220), MCM (30,000 mults), LCS ('BCBA' 61.5% similarity), OBST (cost 1.9), Bellman-Ford negative cycles, Floyd-Warshall blast radius, and Held-Karp TSP (7/7 Passed)."),
        
        ("screenshots/11_backtracking_tests.png", 
         "Figure 11: Unit V Backtracking & Branch and Bound Test Suite (Chunk 5)",
         "Binary: Phase_II/test_chunk5_backtracking_bb.exe | Unit V Test Harness",
         "Validates N-Queens (N=4: 2 solns, N=8: 92 solns), Sum of Subsets, Knapsack Backtracking, Knapsack B&B (FIFO vs LIFO vs LC, LC prunes most), and TSP B&B (cost 80, 5 pruned) (5/5 Passed)."),
        
        ("screenshots/12_flow_string_tests.png", 
         "Figure 12: Unit VI Flow, Strings, CRT & Complexity Reductions (Chunk 6)",
         "Binary: Phase_II/test_chunk6_flow_strings_crt.exe | Unit VI Test Harness",
         "Validates Edmonds-Karp Max Flow (19.0), Bipartite Flow Matching, Chinese Remainder Theorem ($x=23 \\pmod{105}$), 4-Way String Matchers, and Subset-Sum $\\le_P$ Knapsack reduction (5/5 Passed)."),
        
        ("screenshots/13_scenario_normal.png", 
         "Figure 13: Scenario 1 — Normal Sprint Operation (Balanced Backlog)",
         "Binary: Phase_II/scenario_benchmarks.exe | Scenario 1 Runner",
         "Validates normal sprint allocation: 10/10 developers utilized (100%), 10/50 issues assigned (20%), and 0/1 Knapsack achieves 1,244 business value points under 120-hour budget."),
        
        ("screenshots/14_capacity_shock.png", 
         "Figure 14: Scenario 2 — Emergency Capacity Shock (B&B Pruning & Reroute)",
         "Binary: Phase_II/scenario_benchmarks.exe | Scenario 2 Runner",
         "Demonstrates 50% capacity reduction: both DP and LC B&B achieve discrete optimum of 730 points, LC B&B prunes 20 nodes, and Dijkstra computes bypass path with cost 29.0."),
        
        ("screenshots/15_adversarial_benchmark.png", 
         "Figure 15: Scenario 3 — Adversarial Quick Sort Pivot Defense & Pathological KMP",
         "Binary: Phase_II/scenario_benchmarks.exe | Scenario 3 Runner",
         "Stress tests adversarial inputs: Median-of-3 Quick Sort executes in 60,678 comparisons vs Merge Sort 51,420; KMP scans 50,001-character pathological log in 100,005 ops (zero backtracks)."),
        
        ("screenshots/16_streaming_simulation.png", 
         "Figure 16: Scenario 4 — Synthetic Enterprise Workload & Preemptive Streaming",
         "Binary: Phase_II/scenario_benchmarks.exe | Scenario 4 Runner",
         "Simulates dynamic event streaming across 120 synthetic enterprise defects: achieves empirical Competitive Ratio of 1.0000 and executes 7 immediate zero-day task preemptions."),
    ]

    # Pair screenshots 2 per page for clean, professional layout
    for idx, (img_path, caption, cmd_info, desc) in enumerate(screenshots_info):
        if idx % 2 == 0 and idx > 0:
            story.append(PageBreak())
            story.append(Paragraph(f"APPENDIX: TERMINAL SCREENSHOT GALLERY (Cont. - Figures {idx+1} & {idx+2})", h2_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=c_secondary, spaceBefore=2, spaceAfter=8))

        if os.path.exists(img_path):
            try:
                with PILImage.open(img_path) as pil_img:
                    w_orig, h_orig = pil_img.size
                
                max_w = 460
                max_h = 205
                scale = min(max_w / w_orig, max_h / h_orig)
                w_pt = w_orig * scale
                h_pt = h_orig * scale
                
                panel = [
                    Image(img_path, width=w_pt, height=h_pt),
                    Spacer(1, 2),
                    Paragraph(f"<b>{caption}</b>", ParagraphStyle('Cap', parent=styles['Normal'], fontSize=8, leading=10, alignment=1, textColor=c_primary)),
                    Paragraph(f"<b>Command / Environment:</b> <code>{cmd_info}</code>", ParagraphStyle('Cmd', parent=styles['Normal'], fontSize=7.2, leading=9.5, textColor=colors.HexColor("#333333"))),
                    Paragraph(f"<b>Telemetry & Invariants:</b> {desc}", ParagraphStyle('Desc', parent=styles['Normal'], fontSize=7.2, leading=9.5, textColor=colors.HexColor("#444444"))),
                    Spacer(1, 8)
                ]
                story.append(KeepTogether(panel))
            except Exception as e:
                print(f"Error embedding {img_path}: {e}")
        else:
            print(f"Warning: Screenshot not found at {img_path}")

    # Build the document
    print("Building AutoTriage_DAA_Final_Project_Report.pdf with NumberedCanvas...")
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF build complete!")

if __name__ == '__main__':
    build_pdf_report()
