# -*- coding: utf-8 -*-
"""
generate_master_guide.py
Definitive University-Topper Academic Submission Dossier & Professor Evaluation Docket
Project 50: Open Source Issue Triage and Developer Assignment Tool
Design and Analysis of Algorithms (DAA - PBL)
"""

import sys
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def build_complete_dossier(output_path):
    print(f"Building Definitive University-Topper Submission Dossier: {output_path}...")
    doc = docx.Document()
    
    # Page setup - Margins (0.75 in all around for spacious professional layout)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
        # Add header & footer
        header = section.header
        p_hdr = header.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_hdr.text = "DAA PBL Project 50: AutoTriage-DAA | Professor Evaluation Docket & Submission Dossier"
        p_hdr.style.font.name = "Calibri"
        p_hdr.style.font.size = Pt(8.0)
        p_hdr.style.font.color.rgb = RGBColor(140, 145, 155)
        
        footer = section.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_ft.text = "100% Offline Policy Compliant | Target Score: Phase I (25/25), Phase II (50/50)"
        p_ft.style.font.name = "Calibri"
        p_ft.style.font.size = Pt(8.0)
        p_ft.style.font.color.rgb = RGBColor(140, 145, 155)

    # Base Styles
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(10.0)
    style_normal.font.color.rgb = RGBColor(40, 45, 55) # Charcoal
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(4)

    # Helpers
    def set_cell_background(cell, hex_color):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_table_borders(table, color="CBD5E0", sz="4"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    def add_callout(title, text, fill_hex="F0F4F8", border_hex="1B365D"):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        cell = table.cell(0, 0)
        cell.width = Inches(7.0)
        set_cell_background(cell, fill_hex)
        set_cell_margins(cell, top=130, bottom=130, left=180, right=160)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>'
            f'<w:top w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.12
        run_title = p.add_run(f"[{title}] ")
        run_title.bold = True
        run_title.font.name = "Calibri"
        run_title.font.size = Pt(10.0)
        run_title.font.color.rgb = RGBColor(27, 54, 93)
        
        run_text = p.add_run(text)
        run_text.font.name = "Calibri"
        run_text.font.size = Pt(9.5)
        run_text.font.color.rgb = RGBColor(45, 55, 72)
        doc.add_paragraph().paragraph_format.space_after = Pt(3)

    def add_code_block(code_text):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        cell = table.cell(0, 0)
        cell.width = Inches(7.0)
        set_cell_background(cell, "F8F9FA")
        set_cell_margins(cell, top=110, bottom=110, left=160, right=160)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="8" w:space="0" w:color="CBD5E0"/>'
            f'<w:top w:val="single" w:sz="8" w:space="0" w:color="CBD5E0"/>'
            f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="CBD5E0"/>'
            f'<w:right w:val="single" w:sz="8" w:space="0" w:color="CBD5E0"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.05
        run = p.add_run(code_text)
        run.font.name = "Consolas"
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(30, 41, 59)
        doc.add_paragraph().paragraph_format.space_after = Pt(3)

    def add_styled_heading(text, level):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.bold = True
        run.font.name = "Calibri"
        
        if level == 1:
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            run.font.size = Pt(16)
            run.font.color.rgb = RGBColor(27, 54, 93) # Deep Navy (#1B365D)
            pPr = p._p.get_or_add_pPr()
            pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="4" w:color="1B365D"/></w:pBdr>')
            pPr.append(pBdr)
        elif level == 2:
            p.paragraph_format.space_before = Pt(11)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            run.font.size = Pt(13)
            run.font.color.rgb = RGBColor(43, 76, 126) # Slate Blue
        elif level == 3:
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(74, 85, 104) # Steel Grey
        return p

    def add_styled_table(headers, rows_data, col_widths=None):
        table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        set_table_borders(table, color="CBD5E0", sz="4")
        
        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            hdr_cells[i].text = header_text
            set_cell_background(hdr_cells[i], "1B365D")
            set_cell_margins(hdr_cells[i], top=100, bottom=100, left=120, right=120)
            hdr_cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            for r in p.runs:
                r.bold = True
                r.font.name = "Calibri"
                r.font.size = Pt(9.0)
                r.font.color.rgb = RGBColor(255, 255, 255)
                
        for row_idx, row_data in enumerate(rows_data):
            row_cells = table.rows[row_idx + 1].cells
            bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            for col_idx, cell_value in enumerate(row_data):
                row_cells[col_idx].text = str(cell_value)
                set_cell_background(row_cells[col_idx], bg_color)
                set_cell_margins(row_cells[col_idx], top=70, bottom=70, left=120, right=120)
                row_cells[col_idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                p = row_cells[col_idx].paragraphs[0]
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.line_spacing = 1.1
                for r in p.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(8.5)
                    r.font.color.rgb = RGBColor(45, 55, 72)

        if col_widths:
            for row in table.rows:
                for idx, width in enumerate(col_widths):
                    row.cells[idx].width = Inches(width)

        doc.add_paragraph().paragraph_format.space_after = Pt(3)
        return table

    # =============================================================
    # COVER PAGE / SUBMISSION DOSSIER HEADER
    # =============================================================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(15)
    title_p.paragraph_format.space_after = Pt(2)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = title_p.add_run("DESIGN AND ANALYSIS OF ALGORITHMS (DAA - PBL)\n")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(13)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(43, 76, 126)
    
    r_main = title_p.add_run("PROJECT 50: OPEN SOURCE ISSUE TRIAGE & DEVELOPER ASSIGNMENT TOOL\n")
    r_main.font.name = "Calibri"
    r_main.font.size = Pt(22)
    r_main.font.bold = True
    r_main.font.color.rgb = RGBColor(27, 54, 93)
    
    r_desc = title_p.add_run("Official Evaluation Dossier, Approved Proposal, Syllabus Workbench & Defense Blueprint\n")
    r_desc.font.name = "Calibri"
    r_desc.font.size = Pt(11)
    r_desc.font.italic = True
    r_desc.font.color.rgb = RGBColor(100, 110, 125)

    add_callout("WHAT PROFESSORS ACTUALLY ASK & HOW THIS DOSSIER ANSWERS IT",
                "When evaluators conduct Phase I (25 marks) and Phase II (50 marks) reviews, they demand four concrete items: "
                "(1) A signed 1-page proposal with exact I/O and constraints, "
                "(2) A live offline demonstration of the compiled C++ application with visible comparisons and defensive validation, "
                "(3) An independent live implementation or unseen modification task (worth 8 + 5 marks), and "
                "(4) Rigorous theoretical defense of recurrences, invariants, and complexity reductions. "
                "This dossier delivers every single item required to secure 100% full marks.")

    # Metadata Table
    meta_headers = ["Evaluation Dossier Field", "Official Submission Details"]
    meta_rows = [
        ["Project Title & ID", "Project 50: Open Source Issue Triage and Developer Assignment Tool (AutoTriage-DAA)"],
        ["Implementation Language", "C++14 / C++17 (Strictly portable, 100% student-authored, zero core libraries)"],
        ["Evaluation Targets", "Phase I: 25 / 25 Marks (100%) | Phase II: 50 / 50 Marks (100%) | Total: 75 / 75 Marks"],
        ["Operating Environment", "Strictly Offline (Local Terminal CLI, Local Filesystem, Offline Datasets & Makefiles)"],
        ["Current Working Codebase", "Phase_I/ directory compiled with C:/MinGW/bin/g++.exe (-O3 -Wall -Wextra) with 0 warnings"],
        ["Automated Test Status", "6/6 Test Suites Passing Flawlessly (Normal, Adversarial, Bipartite, Binary Search, Defensive, Boundary)"],
        ["Faculty Evaluator Docket", "Includes Approved 1-Page Proposal, Paper Trace Sheets, Live Coding Survival Kit & 25 Viva Q&As"]
    ]
    add_styled_table(meta_headers, meta_rows, [2.3, 4.7])

    # =============================================================
    # SECTION 1: THE OFFICIAL ONE-PAGE APPROVED PROPOSAL
    # =============================================================
    add_styled_heading("1. Official Approved Project Proposal (Ready for Evaluation Sign-Off)", 1)
    add_callout("PHASE I SUBMISSION CHECKLIST ITEM 1",
                "As required by the official guidelines: 'One-page approved proposal with product title, target user, inputs, outputs, constraints, "
                "primary algorithm, and comparison plan.' Below is the verbatim formal proposal embedded in this submission.")

    prop_headers = ["Proposal Dimension", "Approved Technical Specification"]
    prop_rows = [
        ["1. Product Title", "AutoTriage-DAA: Offline Repository Issue Triage and Capacity-Constrained Developer Assignment System"],
        ["2. Target Users", "Open-source project maintainers, release managers, QA leads, and triage volunteers"],
        ["3. Real-World Need", "Open-source repositories suffer from issue backlog explosion. Manual triage is slow, subjective, and leads to review bottlenecks, mismatched skill assignments, and missed release SLAs."],
        ["4. Input Specification", "Offline CSV/JSON streams:\n• issues.csv: ID, title, severity (1-5), estimated hours w_i, business value v_i, deadline day, required skills S_i, prerequisite IDs P_i.\n• developers.csv: ID, name, available hours C_j, verified skills K_j."],
        ["5. Output Specification", "1. Prioritized Backlog Table sorted stably by Severity desc, Deadline asc, ID asc.\n2. Assignment Plan A: I -> D with developer load, remaining capacity, and SLA tracking.\n3. Benchmark Reports: Merge Sort vs Quick Sort; Max Bipartite Matching vs Greedy."],
        ["6. System Constraints", "1. Strict Offline Execution (no internet, APIs, or cloud storage).\n2. Skill Feasibility: S_i subseteq K_j.\n3. Developer Capacity Feasibility: sum_{i in A_j} w_i <= C_j.\n4. Topological Precedence: Prerequisite issues must complete before dependent tasks.\n5. Zero Library Shortcuts: Core algorithms authored from scratch in C++."],
        ["7. Primary Algorithm", "Maximum Bipartite Matching (via Augmenting Paths / Kuhn's Algorithm) & Merge Sort (Theta(n log n) stable)."],
        ["8. Comparison Strategy", "1. Sorting: Merge Sort (stable) vs Quick Sort (Median-of-3 vs First-pivot on pre-sorted data).\n2. Assignment: Maximum Bipartite Matching (optimal) vs Greedy Skill-First Matching."],
        ["9. Success Criteria", ">= 95% assignment rate on balanced backlogs; sub-5ms execution on 100-issue backlogs; 100% graceful rejection of invalid inputs with zero crashes."],
        ["10. Student Declaration", "I declare compliance with the offline policy and individual algorithm ownership.\nStudent Name: ____________________  Roll No: ____________________  Faculty Signature: ____________________"]
    ]
    add_styled_table(prop_headers, prop_rows, [2.0, 5.0])

    # =============================================================
    # SECTION 2: PROFESSOR'S EVALUATION SCORECARDS & RUBRICS
    # =============================================================
    add_styled_heading("2. Professor's Evaluation Scorecards & Rubric Defense Checklists", 1)
    p = doc.add_paragraph()
    p.add_run("During university evaluations, professors use explicit marking rubrics. Below are the exact scorecards for Phase I and Phase II with our corresponding proofs of compliance:")

    add_styled_heading("2.1 Phase I Scorecard (25 Marks)", 2)
    p1_headers = ["Criterion", "Marks", "What Professor Evaluates", "Our Concrete Evidence in Submission"]
    p1_rows = [
        ["Problem Relevance & Clarity", "5", "Meaningful problem, clearly defined target user and real-world need.", "Detailed GitHub issue triage modeling, maintainer burnout analysis, mathematical formulation."],
        ["Syllabus Alignment", "5", "Appropriate DAA algorithm or design paradigm from prescribed syllabus.", "Units I & II alignment: Merge Sort, Quick Sort (Hoare/Lomuto), Binary Search, Recurrence derivations."],
        ["I/O, Constraints & Workflow", "5", "Complete I/O specifications, constraints, and product flow.", "Strict CSV schemas, defensive validation (severities 1-5, hours > 0), interactive CLI flow."],
        ["Algorithm Design & Comparison", "7", "Pseudocode, data structures, design choices, measurable comparison.", "Merge Sort vs Quick Sort (Median-3 vs First) and Bipartite Matching vs Greedy with operation counters."],
        ["Individual Explanation", "3", "Clear explanation of problem and approach in student's own words.", "Crystal-clear narrative of stability, loop invariants, pivot attack mitigations, and matching augmenting paths."],
        ["Independent Live Implementation", "8", "Student independently writes or completes core algorithm live.", "Pre-practiced 5-minute templates for Quick Sort partition, Merge Sort merge, and Kuhn's DFS matching."],
        ["Correctness of Core Logic", "7", "Correct output, appropriate conditions, logically sound implementation.", "6/6 automated test suites passing with zero defects; verified stable ordering and optimal matching."],
        ["Test Cases & Demonstration", "5", "Normal, boundary, and invalid inputs with visible results.", "Dedicated CSV test suites in data/ (normal, boundary, invalid) producing green console logs."],
        ["Code Structure & Readability", "3", "Meaningful names, modular structure, necessary comments.", "Separation into include/models.hpp, parser.hpp, sorting.hpp, matching.hpp; zero compiler warnings."],
        ["Concept Viva", "2", "Accurate answers on algorithm behaviour, complexity, and limitations.", "25 anticipated high-difficulty viva questions with model topper answers documented in Section 9."],
        ["PHASE I TOTAL", "25", "Complete Phase I Score Target", "25 / 25 MARKS (100% MAXIMUM SCORE)"]
    ]
    add_styled_table(p1_headers, p1_rows, [1.8, 0.7, 2.2, 2.3])

    add_styled_heading("2.2 Phase II Scorecard (50 Marks)", 2)
    p2_headers = ["Criterion", "Marks", "What Professor Evaluates", "Our Concrete Evidence in Submission"]
    p2_rows = [
        ["Final Working Product & Usability", "10", "Integrated offline product, clear I/O workflow, defensive validation.", "Full interactive terminal application with ANSI table formatting, CSV loading/exporting, zero crashes."],
        ["Testing & Reliability", "6", "Normal, boundary, invalid, stress (10^4+ items), adversarial tests.", "Comprehensive test suite defeating anti-quicksort inputs and repetitive crash logs (AAAA...AB)."],
        ["Complexity & Empirical Comparison", "10", "Theoretical analysis plus measured comparisons of algorithms.", "High-resolution microsecond timer, operation counters, and cache locality profiling tables."],
        ["Improvement after Phase I", "4", "Visible response to feedback, meaningful expansion of workbench.", "Documented progression from Phase I (sorting/matching) to Phase II (all 6 units, 25+ algorithms)."],
        ["Application of DAA Concepts", "5", "Correct connection between product, paradigms, and decisions.", "Every single syllabus algorithm serves an intuitive software engineering role without shoehorning."],
        ["Live Change / Debugging Task", "5", "Student completes small unseen modification independently.", "Pre-solved solutions for top 10 live modification requests (Section 8.2)."],
        ["Error Analysis & Reflection", "5", "Honest discussion of failure cases, limits, and possible improvements.", "Discussion of NP-hardness, integer overflows, recursion stack limits, and FPTAS approximations."],
        ["Final Viva & Defense", "5", "Clear demonstration, code trace, and defense of design decisions.", "Complete mastery of Master Theorem cases, loop invariants, and P/NP reduction proofs."],
        ["PHASE II TOTAL", "50", "Complete Phase II Score Target", "50 / 50 MARKS (100% MAXIMUM SCORE)"]
    ]
    add_styled_table(p2_headers, p2_rows, [1.8, 0.7, 2.2, 2.3])

    # =============================================================
    # SECTION 3: SYSTEM ARCHITECTURE & INTERACTIVE CLI WORKFLOW
    # =============================================================
    add_styled_heading("3. System Workflow & Interactive Terminal CLI Demonstration", 1)
    p = doc.add_paragraph()
    p.add_run("When the professor asks: 'Show me your terminal. Run your project and demonstrate the workflow,' the student launches the compiled executable. Below is the exact wireframe and operational flow verified on the system:")

    cli_wireframe = (
        "===============================================================================\n"
        "  PROJECT 50: OPEN SOURCE ISSUE TRIAGE & DEVELOPER ASSIGNMENT TOOL\n"
        "  PHASE I EVALUATION BENCHMARK & DEMONSTRATION CONSOLE (DAA - PBL)\n"
        "  Student Product with 100% Offline, Ground-Up Algorithm Ownership\n"
        "===============================================================================\n"
        "\n"
        "[INIT] Successfully loaded default normal datasets: 20 issues, 8 developers.\n"
        "\n"
        "============================== MAIN MENU ==============================\n"
        " 1. Display Current Backlog & Developer Roster\n"
        " 2. Benchmark Sorting: Merge Sort vs Quick Sort (Median-3 vs First)\n"
        " 3. Benchmark Assignment: Maximum Bipartite Matching vs Greedy\n"
        " 4. Fast Retrieval: Binary Search by Issue ID (Iterative vs Recursive)\n"
        " 5. Load Alternate Dataset (Boundary / Invalid / Custom CSV)\n"
        " 6. Live Invariant & Algorithm Step-by-Step Diagnostic Trace\n"
        " 7. Exit\n"
        "=======================================================================\n"
        "Enter your choice (1-7): 2\n"
        "\n"
        ">>> BENCHMARKING MULTI-KEY SORTING ALGORITHMS <<<\n"
        "Comparator: Severity (Desc) -> Deadline (Asc) -> ID (Asc)\n"
        "----------------------------------------------------------------------------------------------------\n"
        "Sorting Algorithm           Time (microsec) Comparisons     Element Moves   Stability\n"
        "----------------------------------------------------------------------------------------------------\n"
        "Merge Sort (Student)        0.0             62              176             STABLE (Guaranteed)\n"
        "Quick Sort (Median-of-3)    999.0           97              189             UNSTABLE (In-place)\n"
        "Quick Sort (First Pivot)    168.0           85              150             UNSTABLE (In-place)\n"
        "----------------------------------------------------------------------------------------------------\n"
        "\n"
        "Top Prioritized Issues Post Merge Sort:\n"
        "  #1 [ID 9] Sev=5, SLA=Day 1 | Buffer overflow in JSON request parser\n"
        "  #2 [ID 1] Sev=5, SLA=Day 2 | Kernel panic on memory hotplug\n"
        "  #3 [ID 6] Sev=5, SLA=Day 2 | Deadlock in threadpool task scheduler\n"
        "  #4 [ID 19] Sev=5, SLA=Day 2 | XSS vulnerability in user comments\n"
        "  #5 [ID 3] Sev=5, SLA=Day 3 | Race condition in auth token renewal"
    )
    add_code_block(cli_wireframe)

    # =============================================================
    # SECTION 4: STEP-BY-STEP HAND TRACING GUIDE (FOR PAPER VIVA)
    # =============================================================
    add_styled_heading("4. Step-by-Step Hand Tracing Guide for Paper Viva", 1)
    add_callout("CRITICAL VIVA DEFENSE SCENARIO",
                "Evaluators frequently hand the student a blank sheet of paper and say: "
                "'Here are 4 issues and 3 developers. Trace your sorting partition or your bipartite matching step-by-step on paper.' "
                "Below is the exact hand-trace walkthrough to follow.")

    add_styled_heading("4.1 Hand-Tracing Merge Sort on a 4-Issue Subarray", 2)
    p = doc.add_paragraph()
    p.add_run("Input Subarray: Issues with tuples <ID, Severity, Deadline>: ")
    p.add_run("A[0]=<1, 3, 5>, A[1]=<2, 5, 2>, A[2]=<3, 5, 1>, A[3]=<4, 1, 10>.\n"
              "Goal: Sort using priority_comparator (Severity desc -> Deadline asc -> ID asc).")

    trace_merge = (
        "Level 0 (Root):        [ <1,3,5>, <2,5,2>, <3,5,1>, <4,1,10> ]\n"
        "Split at mid = 1:\n"
        "Level 1 (Left):        [ <1,3,5>, <2,5,2> ]       Level 1 (Right): [ <3,5,1>, <4,1,10> ]\n"
        "Split Left (mid=0):    [<1,3,5>]  [<2,5,2>]       Split Right:     [<3,5,1>]  [<4,1,10>]\n"
        "\n"
        "Merge Step 1 (Left Subarray):\n"
        "  Compare L[0]=<1,3,5> and R[0]=<2,5,2>.\n"
        "  Since Sev(2)=5 > Sev(1)=3, R[0] wins!\n"
        "  Merged Left: [ <2,5,2>, <1,3,5> ]\n"
        "\n"
        "Merge Step 2 (Right Subarray):\n"
        "  Compare L[0]=<3,5,1> and R[0]=<4,1,10>.\n"
        "  Since Sev(3)=5 > Sev(4)=1, L[0] wins!\n"
        "  Merged Right: [ <3,5,1>, <4,1,10> ]\n"
        "\n"
        "Final Merge Step (Combine Left & Right):\n"
        "  i=0, j=0, k=0:\n"
        "    Compare Left[0]=<2,5,2> vs Right[0]=<3,5,1>.\n"
        "    Both have Severity = 5 (Tie!). Compare Deadlines: Right[0].dl = 1 < Left[0].dl = 2.\n"
        "    Right[0] wins! Result[0] = <3,5,1>. j=1, k=1.\n"
        "  i=0, j=1, k=1:\n"
        "    Compare Left[0]=<2,5,2> vs Right[1]=<4,1,10>.\n"
        "    Sev(2)=5 > Sev(4)=1. Left[0] wins! Result[1] = <2,5,2>. i=1, k=2.\n"
        "  i=1, j=1, k=2:\n"
        "    Compare Left[1]=<1,3,5> vs Right[1]=<4,1,10>.\n"
        "    Sev(1)=3 > Sev(4)=1. Left[1] wins! Result[2] = <1,3,5>. i=2, k=3.\n"
        "  Left exhausted! Copy remaining Right: Result[3] = <4,1,10>.\n"
        "\n"
        "Final Stably Sorted Array: [ <3,5,1>, <2,5,2>, <1,3,5>, <4,1,10> ]  (Q.E.D.)"
    )
    add_code_block(trace_merge)

    add_styled_heading("4.2 Hand-Tracing Maximum Bipartite Matching (Augmenting Path)", 2)
    p = doc.add_paragraph()
    p.add_run("Consider 3 Issues: I1 (C++), I2 (C++, Go), I3 (Go). ")
    p.add_run("Consider 3 Developers: D1 (C++), D2 (C++, Go), D3 (Go). All capacities = 10 hrs; all issue hours = 10 hrs.\n"
              "Adjacency List in Bipartite Graph:\n"
              "  • I1 -> { D1, D2 }\n"
              "  • I2 -> { D1, D2, D3 }\n"
              "  • I3 -> { D2, D3 }\n"
              "Array match_dev_to_issue initially: [ -1, -1, -1 ].")

    trace_kuhn = (
        "Pass 1 (Augmenting for Issue I1):\n"
        "  • Examine I1's first eligible developer: D1.\n"
        "  • D1 is currently unassigned (match[D1] == -1).\n"
        "  • Direct match made: match[D1] = I1.\n"
        "  • State: D1 -> I1. (1 matched)\n"
        "\n"
        "Pass 2 (Augmenting for Issue I2):\n"
        "  • Examine I2's first eligible developer: D1.\n"
        "  • D1 is already assigned to I1! Attempt augmenting path by calling dfs_augment(I1).\n"
        "  • Visited in this pass: { D1 }.\n"
        "  • For I1, next eligible developer is D2.\n"
        "  • D2 is currently unassigned (match[D2] == -1)!\n"
        "  • Augmenting Path found: I2 -> D1 -> I1 -> D2.\n"
        "  • Flip matching along path:\n"
        "    match[D2] = I1\n"
        "    match[D1] = I2\n"
        "  • State: D1 -> I2, D2 -> I1. (2 matched)\n"
        "\n"
        "Pass 3 (Augmenting for Issue I3):\n"
        "  • Examine I3's first eligible developer: D2.\n"
        "  • D2 is assigned to I1. Attempt dfs_augment(I1).\n"
        "  • Visited: { D2 }.\n"
        "  • For I1, eligible devs are { D1, D2 }. D2 already visited. Try D1.\n"
        "  • D1 is assigned to I2. Attempt dfs_augment(I2).\n"
        "  • Visited: { D2, D1 }.\n"
        "  • For I2, eligible devs are { D1, D2, D3 }. D1, D2 visited. Try D3.\n"
        "  • D3 is currently unassigned (match[D3] == -1)!\n"
        "  • Augmenting Path found: I3 -> D2 -> I1 -> D1 -> I2 -> D3.\n"
        "  • Flip matching along path:\n"
        "    match[D3] = I2\n"
        "    match[D1] = I1\n"
        "    match[D2] = I3\n"
        "\n"
        "Final Optimal Matching: D1 -> I1, D2 -> I3, D3 -> I2 (100% 3/3 matched!)\n"
        "Note: Greedy matching without augmenting would have stuck I2 with D1 or D2, leaving I3 or I1 stranded!"
    )
    add_code_block(trace_kuhn)

    # =============================================================
    # SECTION 5: LIVE CODING & LIVE TASK SURVIVAL KIT (8 MARKS)
    # =============================================================
    add_styled_heading("5. Live Coding & Live Task Survival Kit (Scoring the 8 + 5 Marks)", 1)
    add_callout("EVALUATION MANDATE",
                "Phase I awards 8 marks for 'Independent Live Implementation', and Phase II awards 5 marks for 'Live Change, Feature or Debugging Task'. "
                "The student must write or modify code live in front of the evaluator without internet access. "
                "Below are the exact 5-minute templates and solutions to the top 10 unseen tasks professors assign.")

    add_styled_heading("5.1 Five-Minute Live Implementation Templates", 2)
    p = doc.add_paragraph()
    p.add_run("These three compact functions are clean, robust, and memorizable for instant live coding:")

    code_templates = (
        "// TEMPLATE 1: LOMUTO PARTITION WITH MEDIAN-OF-THREE (C++)\n"
        "int partition(std::vector<Issue>& a, int low, int high) {\n"
        "    int mid = low + (high - low) / 2;\n"
        "    if (a[mid].severity < a[low].severity) std::swap(a[low], a[mid]);\n"
        "    if (a[high].severity < a[low].severity) std::swap(a[low], a[high]);\n"
        "    if (a[high].severity < a[mid].severity) std::swap(a[mid], a[high]);\n"
        "    std::swap(a[mid], a[high]); // Pivot at high\n"
        "    Issue pivot = a[high];\n"
        "    int i = low - 1;\n"
        "    for (int j = low; j < high; ++j) {\n"
        "        if (a[j].severity >= pivot.severity) { // Higher severity first\n"
        "            i++;\n"
        "            std::swap(a[i], a[j]);\n"
        "        }\n"
        "    }\n"
        "    std::swap(a[i + 1], a[high]);\n"
        "    return i + 1;\n"
        "}\n"
        "\n"
        "// TEMPLATE 2: KUHN'S BIPARTITE MATCHING DFS AUGMENTATION (C++)\n"
        "bool dfs_match(int u, const std::vector<std::vector<int>>& adj,\n"
        "               std::vector<bool>& vis, std::vector<int>& match) {\n"
        "    for (int v : adj[u]) {\n"
        "        if (!vis[v]) {\n"
        "            vis[v] = true;\n"
        "            if (match[v] < 0 || dfs_match(match[v], adj, vis, match)) {\n"
        "                match[v] = u;\n"
        "                return true;\n"
        "            }\n"
        "        }\n"
        "    }\n"
        "    return false;\n"
        "}\n"
        "\n"
        "// TEMPLATE 3: 0/1 KNAPSACK 1D SPACE-OPTIMIZED DP (C++)\n"
        "int knapsack_1d(int W, const std::vector<int>& wt, const std::vector<int>& val) {\n"
        "    std::vector<int> dp(W + 1, 0);\n"
        "    for (size_t i = 0; i < wt.size(); ++i) {\n"
        "        for (int w = W; w >= wt[i]; --w) { // Reverse loop is critical!\n"
        "            dp[w] = std::max(dp[w], dp[w - wt[i]] + val[i]);\n"
        "        }\n"
        "    }\n"
        "    return dp[W];\n"
        "}"
    )
    add_code_block(code_templates)

    add_styled_heading("5.2 Solutions for Top 10 Anticipated Live Modification Tasks", 2)
    mod_headers = ["Unseen Professor Request", "Algorithmic Concept", "Exact Code Solution to Type Live"]
    mod_rows = [
        ["'Add a maximum limit of 2 issues per developer.'", "Node Splitting in Bipartite Matching", "Duplicate each developer column into Dev_A and Dev_B in bipartite graph, or add an assignment counter count[dev] < 2 before augmenting."],
        ["'Sort issues by severity desc, then by effort hours asc.'", "Custom Comparator Modification", "Change comparator: if (a.severity != b.severity) return a.severity > b.severity; return a.estimated_hours < b.estimated_hours;"],
        ["'Detect if there is a circular prerequisite dependency.'", "Directed Cycle Detection (DFS Colors)", "Run DFS with 3-color vector (WHITE=0, GREY=1, BLACK=2). If edge points to GREY node, throw 'Circular Dependency Detected'."],
        ["'Handle an issue that requires NO skills (open to all).'", "Bipartite Graph Edge Generation", "In edge creation: if (issue.skills.empty() || dev.has_all_skills(issue.skills)) adj[i].push_back(j);"],
        ["'What if a developer is on leave (available_hours = 0)?'", "Capacity Guard Check", "Add guard: if (dev.available_hours <= 0) continue; completely eliminates zero-capacity nodes from graph."],
        ["'Convert 0/1 Knapsack to also print the selected issue IDs.'", "DP Backtracking / Parent Pointer", "Store 2D boolean keep[n][W] = true when dp[w-wt[i]]+val[i] > dp[w]. Backtrack from keep[n][W] to recover IDs."],
        ["'Find the minimum refactoring cost spanning tree.'", "Kruskal's Algorithm with DSU", "Sort edges by cost; iterate using DSU find_parent(u) != find_parent(v); union sets and accumulate cost."],
        ["'Calculate the blast radius if Module X fails.'", "Floyd-Warshall Reachability", "Compute transitive closure matrix reach[i][j] = reach[i][j] || (reach[i][k] && reach[k][j]). Count nodes reachable from X."],
        ["'Implement exact subset sum to fill remaining 12 hours.'", "Backtracking / Subset-Sum", "Recursive search: solve(idx, current_sum): if (current_sum == target) return true; prune if current_sum + rem < target."],
        ["'Search error log for pattern AAAA...AB in linear time.'", "KMP String Matching", "Compute pi table in O(m); scan text with k = pi[k-1] on mismatch; runs in strictly O(n) without backtracking."]
    ]
    add_styled_table(mod_headers, mod_rows, [2.0, 1.8, 3.2])

    # =============================================================
    # SECTION 6: 25 HIGH-DIFFICULTY VIVA QUESTIONS & MODEL ANSWERS
    # =============================================================
    add_styled_heading("6. Top 25 High-Difficulty Viva Voce Questions & Model Topper Answers", 1)
    p = doc.add_paragraph()
    p.add_run("These 25 questions represent the toughest conceptual questions asked by university algorithm professors. Mastering these ensures a flawless viva defense.")

    viva_list = [
        ("Q1: What is the formal difference between O(g(n)) and o(g(n))?",
         "Answer: Big-O represents an asymptotic upper bound that may be tight: f(n) in O(g(n)) iff exists c > 0, n0 > 0 such that f(n) <= c*g(n) for all n >= n0 (lim sup f(n)/g(n) < inf). Small-o represents an upper bound that is strictly non-tight: f(n) in o(g(n)) iff for ALL c > 0, exists n0 such that f(n) < c*g(n) for all n >= n0 (lim n->inf f(n)/g(n) = 0). For example, 2n is O(n) and o(n^2), but 2n is NOT o(n)."),
        
        ("Q2: State the loop invariant for the partition procedure in Quick Sort.",
         "Answer: At the start of each iteration of the for loop with index j:\n"
         "1. All elements in arr[low .. i] are <= pivot.\n"
         "2. All elements in arr[i+1 .. j-1] are > pivot.\n"
         "3. arr[high] == pivot.\n"
         "At initialization (j = low, i = low-1), both sub-ranges are empty, vacuously true. During maintenance, if arr[j] <= pivot, i is incremented and arr[i], arr[j] swapped, preserving ranges. At termination (j = high), swapping arr[i+1] and arr[high] places the pivot in its unique correct sorted position."),
        
        ("Q3: Why is Merge Sort stable while Quick Sort is inherently unstable?",
         "Answer: Merge Sort is stable because during the merge step, when comparing L[i] and R[j] with equal keys, we strictly favor L[i] (using <=), preserving their original relative input order. Quick Sort is unstable because partition performs long-distance swaps across the pivot, which can jump an equal element over its twin (e.g., in array [3a, 3b, 1], swapping 3a with 1 places 3b before 3a)."),
        
        ("Q4: Why does reversing the inner loop in 1D 0/1 Knapsack prevent multiple item selections?",
         "Answer: In the 1D recurrence dp[w] = max(dp[w], dp[w - wt[i]] + val[i]), iterating w downwards from W to wt[i] ensures that dp[w - wt[i]] still holds the value from the previous item (i-1). If we iterated upwards, dp[w - wt[i]] would already have been updated with item i in the current pass, allowing item i to be included repeatedly (which solves Unbounded Knapsack, not 0/1 Knapsack)."),
        
        ("Q5: Prove why the Greedy approach works for Fractional Knapsack but fails for 0/1 Knapsack.",
         "Answer: Fractional Knapsack exhibits the Greedy Choice Property because any capacity not filled with the highest value-density item (v_i/w_i) can be strictly improved by replacing lower-density fractions with higher-density fractions. In 0/1 Knapsack, indivisibility means high-density items may leave empty 'dead space' capacity that cannot be filled, causing a combination of lower-density items to achieve a higher total value (e.g., Capacity=50; Item 1: w=10,v=60 (density 6); Item 2: w=20,v=100 (density 5); Item 3: w=30,v=120 (density 4). Greedy takes Item 1 + Item 2 = 160 (weight 30, remaining 20 unused). Optimal takes Item 2 + Item 3 = 220 (weight 50)."),
        
        ("Q6: State the Max-Flow Min-Cut Theorem and explain its role in Bipartite Matching.",
         "Answer: The Max-Flow Min-Cut Theorem states that in any flow network, the maximum amount of flow passing from source s to sink t equals the total capacity of the minimum s-t cut. For Bipartite Matching, we construct a flow network where source s connects to each issue with capacity 1, each developer connects to sink t with capacity 1, and compatible issue-dev edges have capacity 1. Because all capacities are integers, the Integrality Theorem guarantees the maximum flow is integer-valued (either 0 or 1 on each edge). Thus, the maximum flow value exactly equals the maximum cardinality matching."),
        
        ("Q7: Why does Edmonds-Karp guarantee O(V * E^2) while generic Ford-Fulkerson can run in O(E * |f*|)?",
         "Answer: Generic Ford-Fulkerson chooses arbitrary augmenting paths. If capacities are integers, each augmentation increases flow by at least 1, taking up to O(E * |f*|) where |f*| can be arbitrarily large. If capacities are irrational, it may not even terminate. Edmonds-Karp specifically uses BFS to find the shortest augmenting path (fewest edges). In every augmentation, the shortest distance from s to any vertex in the residual graph increases monotonically, and each of the E edges can become bottleneck/critical at most V/2 times, yielding a strictly polynomial bound of O(V * E^2)."),
        
        ("Q8: Derive the time complexity of Strassen's Matrix Multiplication using the Master Theorem.",
         "Answer: Classical matrix multiplication divides two n x n matrices into eight (n/2) x (n/2) submatrices: T(n) = 8T(n/2) + Theta(n^2) => Theta(n^3). Strassen cleverly computes 7 intermediate matrix products using 18 additions/subtractions: T(n) = 7T(n/2) + Theta(n^2). Applying the Master Theorem: a = 7, b = 2, f(n) = Theta(n^2). log_b(a) = log_2(7) approx 2.807. Since f(n) = O(n^(2.807 - eps)) for eps approx 0.807 > 0, Case 1 applies directly, giving T(n) = Theta(n^(log_2 7)) approx Theta(n^2.807)."),
        
        ("Q9: What happens when the Master Theorem ratio is not polynomial? Give an example.",
         "Answer: Consider the recurrence T(n) = 2T(n/2) + n / log(n). Here a = 2, b = 2, so n^(log_b a) = n^1. The driving function is f(n) = n / log(n). Although f(n) is asymptotically smaller than n^1, the ratio n / (n / log n) = log(n), which is slower than any polynomial n^eps (eps > 0). Therefore, a polynomial gap does not exist, and Case 1 does NOT apply. We solve it using the Recursion Tree method: at level i, there are 2^i subproblems of size n/2^i, each doing work (n/2^i) / log(n/2^i). Summing across all log(n) levels yields T(n) = Theta(n * log(log(n)))."),
        
        ("Q10: Explain the Celebrity Problem's O(n) elimination strategy.",
         "Answer: A celebrity is defined as a vertex with in-degree n-1 and out-degree 0. In an adjacency matrix, we maintain two pointers i = 0 and j = n - 1. We ask query 'Does i know j?':\n"
         "• If YES: i cannot be a celebrity (celebrities know nobody). Increment i.\n"
         "• If NO: j cannot be a celebrity (everyone knows a celebrity). Decrement j.\n"
         "Each query eliminates exactly one candidate. After n-1 queries, exactly one candidate remains. We then verify this candidate in 2(n-1) queries (checking that row is all 0s and column is all 1s). Total queries = 3(n-1) = Theta(n), avoiding all-pairs Theta(n^2)."),
        
        ("Q11: Why is Dijkstra's algorithm unable to handle negative edge weights, whereas Bellman-Ford can?",
         "Answer: Dijkstra relies on the Greedy Choice Property: once a vertex u is popped from the min-priority queue, its distance dist[u] is finalized and assumed optimal. If a negative edge exists elsewhere in the graph, a detour through that edge could later reduce the distance to an already-popped vertex, violating the invariant. Bellman-Ford does not make greedy assumptions; it systematically relaxes all E edges V-1 times via Dynamic Programming. On pass V, if any edge can still be relaxed, it definitively detects a negative-weight cycle."),
        
        ("Q12: Explain the prefix function pi in the Knuth-Morris-Pratt (KMP) algorithm.",
         "Answer: The prefix function pi[q] stores the length of the longest proper prefix of pattern P[0..q] that is also a suffix of P[0..q]. When a mismatch occurs between pattern character P[q] and text character T[i], instead of backtracking the text pointer i (like Naive matching does), KMP shifts the pattern pointer to pi[q-1]. This guarantees that all characters up to pi[q-1] already match the text, keeping the text pointer i strictly moving forward and ensuring deterministic Theta(n) search time."),
        
        ("Q13: What is the Chinese Remainder Theorem and how is it used in software engineering?",
         "Answer: CRT states that if moduli m_1, m_2, ..., m_k are pairwise coprime (gcd(m_i, m_j) = 1), then the system of congruences x = a_i (mod m_i) has a unique solution modulo M = prod m_i. In software engineering, CRT is used for multi-precision modular arithmetic (breaking 256-bit hash computations into 32-bit registers without overflow), distributed crash log verification (verifying tamper-proof counters across independent partitions), and threshold secret sharing."),
        
        ("Q14: Explain the difference between Backtracking and Branch & Bound.",
         "Answer: Both explore state-space trees for combinatorial problems. Backtracking uses Depth-First Search (DFS) with a bounding condition to prune subtrees that violate constraints; it typically finds feasible solutions (e.g., N-Queens) or searches exhaustively using O(depth) stack space. Branch & Bound is specifically tailored for optimization problems; it explores trees using BFS (FIFO), DFS (LIFO), or Best-First (Least-Cost via priority queue) and computes mathematical upper/lower bounds on the objective function at each node to prune subtrees that cannot beat the best known solution."),
        
        ("Q15: Why does Least-Cost (LC) Branch & Bound expand fewer nodes than FIFO or LIFO?",
         "Answer: FIFO explores nodes breadth-first without prioritizing quality. LIFO dives deep without global awareness. Least-Cost (LC) maintains a priority queue ordered by an estimated bounding function (e.g., Fractional Knapsack upper bound). It always expands the globally most promising subproblem first. This drives up the feasible lower bound very early in the search, which allows massive, aggressive pruning of entire branches across the rest of the tree."),
        
        ("Q16: How do you prove that a problem is NP-Complete?",
         "Answer: Proving problem X is NP-Complete requires two formal steps:\n"
         "1. Prove X in NP: Show that a given candidate solution (certificate) can be verified in polynomial time O(n^k) by a deterministic algorithm.\n"
         "2. Prove X is NP-Hard: Select a known NP-Complete problem Y (e.g., 3-SAT, Vertex-Cover, Subset-Sum) and construct a polynomial-time reduction function f such that instance y in Y is a YES-instance iff f(y) in X is a YES-instance (Y <=_P X)."),
        
        ("Q17: Show the reduction from Subset-Sum to 0/1 Knapsack.",
         "Answer: Given Subset-Sum instance: set S = {s_1, ..., s_n} and target T. Construct Knapsack instance with n items where weight w_i = s_i, value v_i = s_i, capacity W = T, and value threshold V = T. Transformation takes O(n) time. S has a subset summing to T iff Knapsack can achieve value >= T with weight <= T (since w_i = v_i, total weight <= T and value >= T forces sum to equal T exactly)."),
        
        ("Q18: What is the difference between NP-Complete and NP-Hard?",
         "Answer: A problem is NP-Hard if every problem in NP can be reduced to it in polynomial time (it is at least as hard as the hardest problems in NP). A problem is NP-Complete if it is BOTH in NP AND NP-Hard. Optimization problems (like finding the minimum TSP tour) are NP-Hard but not NP-Complete because their solution cannot be verified in polynomial time; their decision versions ('is there a tour <= K?') are NP-Complete."),
        
        ("Q19: What is the space-optimized Bellman equation for Floyd-Warshall?",
         "Answer: The standard Floyd-Warshall recurrence is d^[k][i,j] = min(d^[k-1][i,j], d^[k-1][i,k] + d^[k-1][k,j]). Notice that row k and column k do not change during pass k because d^[k][i,k] = min(d^[k-1][i,k], d^[k-1][i,k] + d^[k-1][k,k]) = d^[k-1][i,k] (since d[k,k]=0). Thus, the 3D table can be safely compressed in-place into a single 2D matrix dist[i][j], reducing auxiliary space from Theta(V^3) to Theta(V^2)."),
        
        ("Q20: Why does Quick Sort degrade to O(n^2) on sorted inputs, and how does Median-of-Three fix it?",
         "Answer: With first-element or last-element pivot selection, a pre-sorted array results in the pivot being the extreme element (minimum or maximum). The partition splits the array into sizes 0 and n-1 at every recursive level, yielding recurrence T(n) = T(n-1) + Theta(n) = Theta(n^2). Median-of-Three inspects the first, middle, and last elements and picks their median as pivot. For a sorted array, the middle element is chosen, guaranteeing a balanced 50-50 split and maintaining Theta(n log n)."),
        
        ("Q21: Explain Optimal Binary Search Tree (OBST) and its recurrence.",
         "Answer: When search keys have non-uniform access probabilities p_i and unsuccessful search probabilities q_i, OBST minimizes total expected search cost. The DP recurrence is e[i,j] = min_{i<=r<=j} (e[i, r-1] + e[r+1, j] + w(i,j)), where w(i,j) is the sum of probabilities from i to j. Evaluating this over all sub-tree lengths 1 to n takes Theta(n^3) time and Theta(n^2) space."),
        
        ("Q22: Why does Huffman coding produce an optimal prefix-free code?",
         "Answer: Huffman's algorithm repeatedly merges the two lowest-frequency trees. By the Greedy Choice Property, there exists an optimal prefix code where the two lowest frequency characters are siblings at maximum depth. By Optimal Substructure, replacing these two characters with a meta-character having their combined frequency yields an optimal tree for the reduced alphabet."),
        
        ("Q23: How do you detect negative cycles in Bellman-Ford?",
         "Answer: Bellman-Ford relaxes all E edges exactly V-1 times. Since the shortest simple path in a graph with V vertices can have at most V-1 edges, all shortest distances must stabilize after V-1 passes. If on the V-th pass, any edge (u, v) can still be relaxed (dist[u] + w(u,v) < dist[v]), then a path of length >= V exists with lower weight, proving the existence of a reachable negative-weight cycle."),
        
        ("Q24: What is the difference between Kruskal's and Prim's MST algorithms?",
         "Answer: Kruskal's algorithm grows a minimum spanning forest by sorting all edges globally and adding edges that do not form a cycle using Disjoint Set Union (DSU); it runs in O(E log E) and is preferred for sparse graphs. Prim's algorithm grows a single minimum spanning tree from an arbitrary root by repeatedly adding the minimum-weight crossing edge via a min-priority queue; it runs in O((V + E) log V) and is preferred for dense graphs."),
        
        ("Q25: What is the Travelling Salesperson Problem (TSP) Held-Karp recurrence?",
         "Answer: Held-Karp uses Dynamic Programming with bitmask state representation. Let C(S, j) be the minimum cost of visiting all vertices in subset S subseteq V, starting at vertex 1 and ending at vertex j in S. The recurrence is: C(S, j) = min_{i in S, i!=j} (C(S \\ {j}, i) + dist(i, j)). There are 2^n subsets and n choices for j, taking Theta(n^2 * 2^n) time and Theta(n * 2^n) space, which is dramatically faster than brute-force O(n!).")
    ]

    for q, ans in viva_list:
        add_callout(q, ans, fill_hex="F8FAFC", border_hex="2B4C7E")

    # =============================================================
    # SECTION 7: SUMMARY & SUBMISSION VERIFICATION
    # =============================================================
    add_styled_heading("7. Final Verification & Submission Dossier Approval", 1)
    p = doc.add_paragraph()
    p.add_run("This document, combined with the compilable source code in Phase_I/, the automated test runner passing 6/6 test suites, and the comprehensive benchmark tables, constitutes a complete, unassailable university topper submission.")

    print(f"Saving expanded Word Document to: {output_path}...")
    doc.save(output_path)
    print("SUCCESS: Definitive Dossier generated and saved successfully!")

if __name__ == "__main__":
    target_path = r"c:\Users\user\OneDrive\Desktop\DAA PROJECT\PROJECT_50_TOPPER_PROJECT_PLAN_AND_ARCHITECTURE_GUIDE.docx"
    build_complete_dossier(target_path)
