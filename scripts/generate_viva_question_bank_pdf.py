import os, sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

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
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1F497D"))
        
        # Header (Top of page: letter height is 792 pt, width 612 pt)
        self.drawString(54, 755, "AutoTriage-DAA: Top 50 Viva Question Bank & Defense Guide (Project 50)")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawRightString(558, 755, "Course: CSEG3053_4 | Ritigya Mishra (590028115)")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 748, 558, 748)
        
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "Department of Computer Science & Engineering | Design & Analysis of Algorithms")
        self.line(54, 46, 558, 46)
        self.restoreState()

def build_viva_question_bank_pdf():
    pdf_path = "AutoTriage_DAA_Viva_Question_Bank_Top50.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    c_primary = colors.HexColor("#1F497D")
    c_secondary = colors.HexColor("#2E75B6")
    c_dark = colors.HexColor("#1E293B")
    c_code_bg = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#CBD5E1")
    c_accent = colors.HexColor("#0F766E")
    c_highlight = colors.HexColor("#B45309")

    # Typography styles
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Heading1'],
        fontSize=23,
        leading=28,
        alignment=1,
        textColor=c_primary,
        spaceAfter=10
    )
    cover_subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#334155"),
        spaceAfter=16
    )
    section_h1 = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    q_title = ParagraphStyle(
        'QTitle',
        parent=styles['Heading2'],
        fontSize=10,
        leading=13.5,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'QBody',
        parent=styles['Normal'],
        fontSize=8.3,
        leading=11.6,
        textColor=c_dark,
        spaceAfter=4
    )
    say_style = ParagraphStyle(
        'SayStyle',
        parent=styles['Normal'],
        fontSize=8.3,
        leading=11.6,
        textColor=colors.HexColor("#065F46"),
        spaceAfter=4
    )
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#475569")
    )

    story = []

    # ==================== COVER PAGE ====================
    story.append(Spacer(1, 20))
    story.append(Paragraph("PROJECT-BASED EVALUATION (PBL)", ParagraphStyle('PBL', parent=styles['Normal'], fontSize=11, leading=14, alignment=1, textColor=c_accent, spaceAfter=8)))
    story.append(Paragraph("AutoTriage-DAA: Open Source Issue Triage and Developer Assignment Tool", cover_title_style))
    story.append(Paragraph("TOP 50 TECHNICAL VIVA PROBABLE QUESTIONS & COMPREHENSIVE DEFENSE GUIDE<br/><b>Mastering Algorithm Design, Asymptotic Complexity, Code Verification & Whiteboard Proofs</b>", cover_subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=4, spaceAfter=14))

    meta_table_data = [
        [Paragraph("<b>Course Code:</b>", body_style), Paragraph("CSEG3053_4 (Design and Analysis of Algorithms - PBL)", body_style),
         Paragraph("<b>Evaluation Date:</b>", body_style), Paragraph("Saturday, 21 November 2026", body_style)],
        [Paragraph("<b>Student Author:</b>", body_style), Paragraph("<b>Ritigya Mishra</b>", body_style),
         Paragraph("<b>SAP ID:</b>", body_style), Paragraph("<b>590028115</b>", body_style)],
        [Paragraph("<b>Academic Program:</b>", body_style), Paragraph("B.Tech — Computer Science & Engineering", body_style),
         Paragraph("<b>Batch / Specialization:</b>", body_style), Paragraph("Batch B-9 (Artificial Intelligence & Machine Learning)", body_style)],
        [Paragraph("<b>Project Specification:</b>", body_style), Paragraph("Project 50 (Autonomous Issue Triage Workbench)", body_style),
         Paragraph("<b>Implementation Standard:</b>", body_style), Paragraph("100% Offline Standalone C++17 (Zero Core External Libs)", body_style)],
        [Paragraph("<b>Format / Schedule:</b>", body_style), Paragraph("Solo Evaluation (8-Min Demo + 4-Min Technical Viva)", body_style),
         Paragraph("<b>Repository:</b>", body_style), Paragraph("github.com/ritigyam2/DevTriage-Optimizer", body_style)]
    ]
    t_meta = Table(meta_table_data, colWidths=[110, 150, 100, 144])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # Examiner Guidelines & FAQ Overview Box
    faq_box_content = [
        [Paragraph("<b>OFFICIAL EXAMINER GUIDELINES & FAQ SUMMARY (CSEG3053_4)</b>", ParagraphStyle('BoxH', parent=styles['Normal'], fontSize=9.5, leading=13, textColor=c_primary))],
        [Paragraph(
            "According to the official project-based evaluation guidelines and FAQ file provided by the department:<br/>"
            "• <b>Evaluation Structure:</b> Strictly individual (solo) evaluation. 8 minutes dedicated to project demonstration, 4 minutes for technical viva (12 minutes total).<br/>"
            "• <b>Primary Focus:</b> Core DAA concepts, algorithmic thinking, problem-solving, algorithm selection justification, time/space complexity, and code understanding.<br/>"
            "• <b>Code Ingestion & Live Alteration:</b> Evaluators are explicitly permitted to ask students to run custom inputs, trace intermediate states, and perform minor on-the-spot code modifications to verify genuine code authorship.<br/>"
            "• <b>Academic Integrity:</b> Complete line-by-line understanding of all data structures, algorithmic paradigms, and edge-case handling is mandatory.<br/>"
            "• <b>Key Viva Priority:</b> <i>'Focus on why an algorithm works, how it works, when to use it, and how to analyze its efficiency. A visually impressive project without a sound understanding of its algorithms will not be sufficient.'</i>",
            body_style
        )]
    ]
    t_faq = Table(faq_box_content, colWidths=[504])
    t_faq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_faq)
    story.append(Spacer(1, 14))

    # Structure of Question Bank Table
    cat_summary = [
        [Paragraph("<b>Category</b>", body_style), Paragraph("<b>Algorithmic Syllabus Focus</b>", body_style), Paragraph("<b>Questions</b>", body_style)],
        [Paragraph("Category 1", body_style), Paragraph("Project Architecture, Motivation, and System Design", body_style), Paragraph("Q1 – Q5", body_style)],
        [Paragraph("Category 2", body_style), Paragraph("Divide and Conquer Algorithms (Strassen, Celebrity, Subarray)", body_style), Paragraph("Q6 – Q10", body_style)],
        [Paragraph("Category 3", body_style), Paragraph("Sorting, Searching, and Pivoting Mechanics", body_style), Paragraph("Q11 – Q15", body_style)],
        [Paragraph("Category 4", body_style), Paragraph("Greedy Paradigms and Optimality Proofs (Knapsack, Activity, MST)", body_style), Paragraph("Q16 – Q20", body_style)],
        [Paragraph("Category 5", body_style), Paragraph("Dynamic Programming Formulations & Space Optimizations", body_style), Paragraph("Q21 – Q26", body_style)],
        [Paragraph("Category 6", body_style), Paragraph("Backtracking & Branch and Bound State Space Pruning", body_style), Paragraph("Q27 – Q31", body_style)],
        [Paragraph("Category 7", body_style), Paragraph("Network Flow and Maximum Bipartite Matching", body_style), Paragraph("Q32 – Q36", body_style)],
        [Paragraph("Category 8", body_style), Paragraph("String Matching and Modular Arithmetic (KMP, CRT)", body_style), Paragraph("Q37 – Q41", body_style)],
        [Paragraph("Category 9", body_style), Paragraph("Computational Complexity and Polynomial Reductions (P, NP, NP-C)", body_style), Paragraph("Q42 – Q45", body_style)],
        [Paragraph("Category 10", body_style), Paragraph("Defensive Engineering, Whiteboard Live Coding & FAQ Tactics", body_style), Paragraph("Q46 – Q50", body_style)]
    ]
    t_cat = Table(cat_summary, colWidths=[80, 340, 84])
    t_cat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_cat)

    story.append(PageBreak())

    # Helper function to generate question block
    def add_q(q_num, title, intent, concept, filepath, complexity, code_snip, what_to_say):
        content = []
        content.append(Paragraph(f"<b>Q{q_num}: {title}</b>", q_title))
        
        info_table_data = [
            [Paragraph("<b>Examiner Intent:</b>", meta_style), Paragraph(intent, body_style)],
            [Paragraph("<b>Core Concept:</b>", meta_style), Paragraph(concept, body_style)],
            [Paragraph("<b>Relevant File:</b>", meta_style), Paragraph(f"<code>{filepath}</code>", meta_style)],
            [Paragraph("<b>Complexity:</b>", meta_style), Paragraph(f"<b>Time:</b> {complexity[0]} | <b>Space:</b> {complexity[1]}", meta_style)],
        ]
        t_info = Table(info_table_data, colWidths=[90, 414])
        t_info.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#F1F5F9")),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        content.append(t_info)
        content.append(Spacer(1, 4))
        
        if code_snip:
            code_table = [[Paragraph(f"<pre>{code_snip}</pre>", code_style)]]
            t_code = Table(code_table, colWidths=[504])
            t_code.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94A3B8")),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ]))
            content.append(t_code)
            content.append(Spacer(1, 4))
            
        content.append(Paragraph(f"<b>What to Say in Viva:</b> {what_to_say}", say_style))
        content.append(Spacer(1, 6))
        return KeepTogether(content)

    # ==================== CATEGORY 1: ARCHITECTURE & SYSTEM DESIGN ====================
    story.append(Paragraph("Category 1: Project Architecture, Motivation, and System Design", section_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=8))

    story.append(add_q(
        1, "What exact problem does AutoTriage-DAA solve, and what motivated this project?",
        "Evaluates high-level problem understanding, engineering relevance, and problem-solving motivation.",
        "Solves open-source maintainer burnout, triage latency, and sub-optimal sprint resource allocation by automating backlog ranking, 1-to-1 skill matching, and discrete sprint release packing.",
        "Phase_I/src/main.cpp | Phase_II/src/main.cpp",
        ("O(N log N) triage, O(V * E) matching", "O(N + M) memory footprint"),
        None,
        "\"AutoTriage automates issue triage and developer allocation in software projects. Maintainers face high triage latency and skill mismatches. We implemented 28 first-principles algorithms in C++17 to stably rank backlogs, optimally match maintainers via flow networks, pack releases via knapsack DP, and preempt emergency zero-days in real time.\""
    ))

    story.append(add_q(
        2, "Explain your Two-Tier System Architecture. Why separate Tier 1 and Tier 2?",
        "Assesses structural clarity, software engineering design, and pedagogical syllabus mapping.",
        "Tier 1 acts as the production triage engine (Merge Sort, Kuhn Bipartite Matching, 1D Knapsack DP, Dijkstra, KMP, Online Streaming). Tier 2 acts as the academic DAA workbench (Strassen, N-Queens, OBST, Held-Karp TSP, P/NP Reductions).",
        "AutoTriage-DAA/README.md | docs/AutoTriage_DAA_Final_Project_Report.pdf",
        ("Modular execution across 6 curriculum units", "Tier 1: O(N) space | Tier 2: O(N^2) space"),
        None,
        "\"We adopted a Two-Tier architecture: Tier 1 solves genuine production triage needs with optimal asymptotic choices like Kuhn's matching and 1D Knapsack DP. Tier 2 implements rigorous academic benchmarks spanning all 6 units of the syllabus—such as Strassen matrix multiplication and Held-Karp TSP—proving theoretical depth without compromising engineering pragmatism.\""
    ))

    story.append(add_q(
        3, "Explain your CSV data model, parsing architecture, and internal representations.",
        "Tests data modeling, defensive parsing, and low-level C++ memory handling.",
        "DataParser parses issues and developers into strongly typed C++ structs: Issue (id, title, severity [1..5], deadline, hours, value, skills, prerequisites) and Developer (id, name, capacity, skills, efficiency, assigned_hours).",
        "Phase_I/include/models.hpp | Phase_I/include/parser.hpp",
        ("O(L) parsing time where L is character length", "O(N * S) where S is average skill count"),
        "struct Issue {\n    int id, severity, deadline_days, estimated_hours, business_value;\n    std::string title, component;\n    std::vector<std::string> skills;\n    std::vector<int> prerequisites;\n};",
        "\"We created custom CSV parsers with strict defensive schemas. Input data is validated on every row: severity must be within [1, 5], hours must be positive, and comma-separated skills are parsed into std::vector<std::string>. Malformed rows trigger human-readable errors identifying the exact line number without crashing.\""
    ))

    story.append(add_q(
        4, "Why did you build this in 100% offline standard C++17 with zero external libraries?",
        "Proves academic integrity, first-principles implementation, and compliance with guidelines.",
        "External libraries like Boost.Graph, Eigen, or Graphviz obscure algorithmic mechanics. Writing algorithms from first principles in standard C++17 guarantees full control over state-space memory, cache locality, and algorithmic transparency.",
        "CMakeLists.txt | Makefile",
        ("Compilation: g++ -std=c++17 -O3 -Wall -Wextra", "Zero runtime shared library dependencies"),
        None,
        "\"To satisfy university evaluation standards, every single data structure—augmenting path trees, dynamic programming tables, heaps, disjoint-set forests, and KMP automata—was written from scratch. This guarantees that our performance results reflect our own algorithms rather than black-box library optimizations.\""
    ))

    story.append(add_q(
        5, "Walk through the end-to-end lifecycle of an issue in AutoTriage.",
        "Verifies end-to-end workflow coherence and algorithm integration.",
        "Ingestion -> Defensive Validation -> Multi-Key Stable Merge Sort -> Release Selection (0/1 Knapsack DP) -> Developer Skill Matching (Kuhn's Augmenting Path Flow) -> 10-Day ASCII Gantt Scheduling.",
        "Phase_II/src/main.cpp (Options 1 -> 3 -> 2 -> 9)",
        ("Pipeline throughput: 120 issues processed in under 2 ms", "O(N + M) memory footprint"),
        None,
        "\"When an issue enters AutoTriage: (1) DataParser validates its schema; (2) Multi-Key Merge Sort stably ranks it; (3) 0/1 Knapsack DP decides if it fits within the sprint hour budget; (4) Kuhn's bipartite matching maps it to a qualified maintainer; and (5) the Gantt visualizer schedules it across a 10-day sprint horizon.\""
    ))

    story.append(PageBreak())

    # ==================== CATEGORY 2: DIVIDE & CONQUER ====================
    story.append(Paragraph("Category 2: Divide and Conquer Algorithms", section_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=8))

    story.append(add_q(
        6, "Explain Strassen’s Matrix Multiplication. How does it save operations, and what is your cutoff threshold?",
        "Tests understanding of D&C subproblem reduction and practical vs theoretical crossover.",
        "Standard matrix multiplication computes 8 recursive sub-multiplications in O(n^3). Strassen devises 7 auxiliary products (M1..M7) using clever linear combinations of submatrices, reducing the recurrence to T(n) = 7T(n/2) + O(n^2), yielding Theta(n^{log_2 7}) approx Theta(n^{2.807}).",
        "Phase_II/include/algorithms/divide_and_conquer/strassen.hpp",
        ("T(n) = Theta(n^{2.807})", "O(n^2) auxiliary matrix allocation"),
        "void strassen_multiply(const Matrix& A, const Matrix& B, Matrix& C, int n) {\n    if (n <= 64) { standard_multiply(A, B, C, n); return; }\n    // Partition into A11, A12... Compute M1 to M7\n    // C11 = M1 + M4 - M5 + M7, etc.\n}",
        "\"Strassen trades one expensive matrix multiplication for 18 matrix additions. By reducing 8 recursive calls to 7, the asymptotic complexity drops from O(n^3) to O(n^2.807). In our implementation, we enforce an empirical cutoff threshold at N <= 64, below which standard multiplication runs to eliminate recursive stack and allocation overhead.\""
    ))

    story.append(add_q(
        7, "Explain the Maximum Subarray problem. Why does Divide & Conquer require crossing-midpoint logic?",
        "Evaluates mastery of divide, conquer, and combine steps.",
        "To find the contiguous period of highest issue velocity, the array is halved. The optimal subarray lies either entirely in the left half, entirely in the right half, or crosses the midpoint. The crossing sum is found by computing maximum suffix on left and maximum prefix on right in O(n) total time.",
        "Phase_II/include/algorithms/divide_and_conquer/max_subarray.hpp",
        ("Divide & Conquer: O(n log n) | Kadane's DP: O(n)", "D&C Space: O(log n) call stack"),
        "SubarrayResult max_crossing_sum(const vector<int>& a, int low, int mid, int high) {\n    int left_sum = -INF, sum = 0;\n    for (int i = mid; i >= low; --i) { sum += a[i]; if (sum > left_sum) left_sum = sum; }\n    int right_sum = -INF; sum = 0;\n    for (int j = mid + 1; j <= high; ++j) { sum += a[j]; if (sum > right_sum) right_sum = sum; }\n    return {left_sum + right_sum, ...};\n}",
        "\"The divide step splits the array at midpoint. The conquer step recursively evaluates the left and right halves. The crucial combine step computes the maximum crossing subarray by expanding outward from mid to low, and mid+1 to high in linear O(n) time, yielding recurrence T(n) = 2T(n/2) + O(n) = O(n log n).\""
    ))

    story.append(add_q(
        8, "Explain Fast Exponentiation (Binary Powering). What recurrence governs its complexity?",
        "Checks logarithmic divide and conquer concepts and modular arithmetic.",
        "Computes a^n by squaring: if n is even, a^n = (a^{n/2})^2; if n is odd, a^n = a * (a^{(n-1)/2})^2. Recurrence T(n) = T(n/2) + O(1), yielding Theta(log n) multiplications instead of O(n) naive loops.",
        "Phase_II/include/algorithms/divide_and_conquer/fast_power.hpp",
        ("Time: Theta(log n)", "Space: O(log n) recursive or O(1) iterative"),
        "long long fast_power(long long base, long long exp, long long mod) {\n    long long res = 1; base %= mod;\n    while (exp > 0) {\n        if (exp % 2 == 1) res = (res * base) % mod;\n        base = (base * base) % mod;\n        exp /= 2;\n    }\n    return res;\n}",
        "\"Fast exponentiation cuts the exponent in half at each step. By squaring intermediate bases, we reduce the multiplicative complexity from linear O(n) to logarithmic O(log n). We use this to compute exponential bug propagation curves and modular inverses for CRT.\""
    ))

    story.append(add_q(
        9, "Explain the Celebrity Maintainer identification algorithm. How is it solved in O(n) with 3(n-1) queries?",
        "Tests candidate elimination, pointer mechanics, and verification passes.",
        "A celebrity maintainer knows nobody, but is known by everybody. Using two pointers (i=0, j=n-1), query knows(i, j): if i knows j, i cannot be a celebrity; if i doesn't know j, j cannot be a celebrity. Eliminate one candidate per query until 1 remains. Then verify the candidate with 2(n-1) checks.",
        "Phase_II/include/algorithms/divide_and_conquer/celebrity.hpp",
        ("Time: O(n) using at most 3(n-1) queries", "Space: O(1) auxiliary"),
        "int find_celebrity(int n) {\n    int i = 0, j = n - 1;\n    while (i < j) { if (knows(i, j)) i++; else j--; }\n    int cand = i;\n    for (int k = 0; k < n; ++k) {\n        if (k != cand && (knows(cand, k) || !knows(k, cand))) return -1;\n    }\n    return cand;\n}",
        "\"In an n-person matrix, naive search takes O(n^2). Our elimination pass uses the invariant that every query knows(i, j) permanently eliminates either i or j. In exactly n-1 queries, a single candidate remains. We then verify candidate row and column in 2(n-1) queries, achieving an optimal O(n) bound with zero extra memory.\""
    ))

    story.append(add_q(
        10, "State the Master Theorem and apply it to Merge Sort, Strassen, and Binary Search.",
        "Verifies formal mathematical competence and recurrence relations.",
        "Master Theorem solves T(n) = aT(n/b) + f(n). Let c = log_b(a). Case 1: f(n) = O(n^{c - eps}) -> T(n) = Theta(n^c). Case 2: f(n) = Theta(n^c log^k n) -> T(n) = Theta(n^c log^{k+1} n). Case 3: f(n) = Omega(n^{c + eps}) -> T(n) = Theta(f(n)).",
        "Phase_I/include/sorting.hpp | Phase_II/include/algorithms/divide_and_conquer/strassen.hpp",
        ("Merge Sort: Theta(n log n)", "Strassen: Theta(n^{2.807}) | Binary Search: Theta(log n)"),
        None,
        "\"Merge Sort has a=2, b=2, f(n)=O(n). log_2(2)=1, so f(n)=Theta(n^1) falls in Case 2, giving Theta(n log n). Strassen has a=7, b=2, f(n)=O(n^2). log_2(7) approx 2.807, so f(n)=O(n^{2.807 - eps}) falls in Case 1, yielding Theta(n^{2.807}). Binary Search has a=1, b=2, f(n)=O(1), falling in Case 2, giving Theta(log n).\""
    ))

    story.append(PageBreak())

    # ==================== CATEGORY 3: SORTING, SEARCHING, PIVOTING ====================
    story.append(Paragraph("Category 3: Sorting, Searching, and Pivoting Mechanics", section_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=8))

    story.append(add_q(
        11, "Why is Stability strictly required in issue triage sorting? How does Merge Sort guarantee it?",
        "Tests knowledge of sorting invariants and multi-key ranking.",
        "A sorting algorithm is stable if items with identical keys preserve their relative input order. If two critical issues have Severity=5, the issue submitted first must stay ahead. Quick Sort and Heap Sort are unstable; Merge Sort preserves FIFO submission order.",
        "Phase_I/include/sorting.hpp",
        ("Time: Best/Avg/Worst Theta(N log N)", "Space: O(N) auxiliary merge buffer"),
        "// In merge step:\nif (left[i].severity >= right[j].severity) {\n    arr[k++] = left[i++]; // Strict '>=' preserves stability for ties!\n} else {\n    arr[k++] = right[j++];\n}",
        "\"In bug tracking, stability guarantees fairness: equal-priority bugs remain ordered by their arrival timestamp. In Merge Sort, stability is preserved at the merge step: whenever a left element has equal key to a right element, the left element is selected first ('>=' comparison), preventing priority inversion.\""
    ))

    story.append(add_q(
        12, "Why does naive Quick Sort collapse to O(n^2) on pre-sorted data? How does Median-of-3 mitigate this?",
        "Tests pivot selection, adversarial inputs, and worst-case complexity nuances.",
        "Lomuto partition with first-element pivot on sorted data creates extremely unbalanced partitions (0 and n-1 elements), yielding T(n) = T(n-1) + O(n) = O(n^2). Median-of-3 selects the median of arr[low], arr[mid], arr[high], ensuring a balanced pivot on sorted or reverse-sorted data. Note: worst-case remains O(n^2) theoretically on specifically constructed pathological inputs.",
        "Phase_I/include/sorting.hpp | Phase_II/include/core/sorting.hpp",
        ("Best/Avg: O(N log N) | Worst: O(N^2)", "Space: O(log N) stack depth"),
        "int median_of_three(vector<Issue>& arr, int low, int high) {\n    int mid = low + (high - low) / 2;\n    if (arr[mid].id < arr[low].id) swap(arr[low], arr[mid]);\n    if (arr[high].id < arr[low].id) swap(arr[low], arr[high]);\n    if (arr[high].id < arr[mid].id) swap(arr[mid], arr[high]);\n    swap(arr[mid], arr[high]); // Place pivot at high\n    return high;\n}",
        "\"On a pre-sorted array of 2,000 items, naive first-pivot collapsed to 1,225 comparisons, whereas our student-authored Median-of-3 completed in only 286 comparisons. Median-of-3 guarantees that the pivot is never the minimum or maximum of those three values, mitigating common sorted traps, though worst-case remains O(n^2).\""
    ))

    story.append(add_q(
        13, "Compare Iterative vs Recursive Binary Search. How do you prevent integer overflow in midpoint calculation?",
        "Checks low-level arithmetic hygiene, call-stack overhead, and search logic.",
        "Calculating mid as (low + high) / 2 causes integer overflow when low + high > 2^{31}-1. The correct algebraic equivalent is low + (high - low) / 2. Iterative search uses O(1) auxiliary space, while recursive search consumes O(log n) stack frames.",
        "Phase_I/include/sorting.hpp (binary_search_iterative & recursive)",
        ("Time: Theta(log N) best/avg/worst", "Space: Iterative O(1) | Recursive O(log N)"),
        "int binary_search_iterative(const vector<Issue>& arr, int target_id) {\n    int low = 0, high = (int)arr.size() - 1;\n    while (low <= high) {\n        int mid = low + (high - low) / 2; // Prevents 32-bit integer overflow!\n        if (arr[mid].id == target_id) return mid;\n        else if (arr[mid].id < target_id) low = mid + 1;\n        else high = mid - 1;\n    }\n    return -1;\n}",
        "\"We compute mid as low + (high - low) / 2 to avoid overflow. We benchmarked both iterative and recursive implementations across 10,000 queries: both achieve logarithmic search, but the iterative loop eliminates function prologue/epilogue overhead and operates in strictly O(1) space.\""
    ))

    story.append(add_q(
        14, "How does AutoTriage perform Multi-Key Sorting across Severity, Deadline, and Business Value?",
        "Tests comparator formulation, tie-breaking logic, and strict weak ordering.",
        "AutoTriage uses a lexicographical multi-key comparator: primary key is Severity (descending), secondary key is Deadline Days (ascending for urgency), tertiary key is Business Value (descending).",
        "Phase_I/include/sorting.hpp | Phase_II/include/core/sorting.hpp",
        ("Time: O(K * N log N) where K is number of keys", "Space: O(N) auxiliary"),
        "bool compare_multi_key(const Issue& a, const Issue& b) {\n    if (a.severity != b.severity) return a.severity > b.severity;\n    if (a.deadline_days != b.deadline_days) return a.deadline_days < b.deadline_days;\n    return a.business_value > b.business_value;\n}",
        "\"Our custom comparator enforces strict weak ordering: it checks primary priority (Severity) first. If and only if severities match, it breaks ties using earliest deadline. If deadlines also match, it prioritizes higher business value. This produces an unambiguous, optimal triage order.\""
    ))

    story.append(add_q(
        15, "LIVE MODIFICATION: How would you invert the triage priority to run lowest-effort issues first?",
        "Simulates live examiner code modification request from FAQ Q17.",
        "To switch to Shortest Job First (SJF) or minimum effort triage, modify the comparator to sort by estimated_hours ascending.",
        "Phase_I/include/sorting.hpp",
        ("Complexity unchanged: O(N log N)", "O(N) space"),
        "// Live code modification in sorting.hpp:\nbool compare_shortest_job_first(const Issue& a, const Issue& b) {\n    if (a.estimated_hours != b.estimated_hours) \n        return a.estimated_hours < b.estimated_hours;\n    return a.severity > b.severity;\n}",
        "\"To prioritize quick wins, I would change the primary comparator check to return a.estimated_hours < b.estimated_hours, keeping severity as the secondary tie-breaker. The Merge Sort framework executes identically with O(N log N) runtime.\""
    ))

    story.append(PageBreak())

    # ==================== CATEGORY 4: GREEDY ALGORITHMS ====================
    story.append(Paragraph("Category 4: Greedy Paradigms and Optimality Proofs", section_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=8))

    story.append(add_q(
        16, "Why is Fractional Knapsack solvable by Greedy, while discrete 0/1 Knapsack fails?",
        "Tests greedy choice property, optimal substructure, and counter-example construction.",
        "Fractional Knapsack exhibits the greedy choice property: taking the maximum value-to-weight ratio item is always part of an optimal solution because divisible items leave no unusable slack. Discrete 0/1 Knapsack fails because indivisible items can leave gaps where combinations of smaller ratio items yield higher total value.",
        "Phase_II/include/algorithms/greedy/fractional_knapsack.hpp",
        ("Time: O(N log N) due to sorting", "Space: O(1) auxiliary"),
        "// Counterexample for discrete greedy:\n// Capacity = 50. Item 1: wt=30, val=60 (ratio 2.0). Items 2 & 3: wt=25, val=45 each (ratio 1.8).\n// Greedy takes Item 1 (val 60, remaining 20 cannot fit 2 or 3). Optimum takes Items 2 & 3 (total val 90)!",
        "\"Fractional Knapsack satisfies the greedy choice property: sorting by value-per-hour ratio guarantees optimality because any capacity slack is filled fractionally. For discrete 0/1 Knapsack, greedy fails because an item with slightly higher ratio can consume space that could have held two items with higher combined value. Hence, 0/1 requires Dynamic Programming.\""
    ))

    story.append(add_q(
        17, "Prove that Activity Selection sorted by Earliest Finish Time yields maximum compatible activities.",
        "Tests formal mathematical proof by induction / 'greedy stays ahead' technique.",
        "Let S = {a1, a2.. ak} be the greedy schedule sorted by finish time f1 <= f2... Let O = {o1, o2.. om} be an optimal schedule. If a1 != o1, since f(a1) <= f(o1), we can replace o1 with a1 in O without conflicting with o2..om. By induction, greedy stays ahead at every step, proving |S| = |O|.",
        "Phase_II/include/algorithms/greedy/activity_selection.hpp",
        ("Time: O(N log N) sorting + O(N) single scan", "Space: O(N) output vector"),
        "vector<Activity> schedule_reviews(vector<Activity>& acts) {\n    sort(acts.begin(), acts.end(), [](auto& a, auto& b){ return a.finish < b.finish; });\n    vector<Activity> sel = { acts[0] };\n    int last_f = acts[0].finish;\n    for (size_t i = 1; i < acts.size(); ++i) {\n        if (acts[i].start >= last_f) { sel.push_back(acts[i]); last_f = acts[i].finish; }\n    }\n    return sel;\n}",
        "\"We prove this using the 'greedy stays ahead' principle: sorting by earliest finish time leaves the maximum possible remaining time for subsequent activities. If an alternative optimal solution begins with another activity, substituting our greedy choice preserves compatibility, proving greedy is always optimal in O(N log N) time.\""
    ))

    story.append(add_q(
        18, "Explain Interval Partitioning for CI/CD test runners. How does it achieve minimum machines?",
        "Checks priority queue implementation and graph coloring interval concepts.",
        "Finds the minimum number of parallel build servers to schedule all test suites without overlap. The theoretical lower bound is the depth d (maximum overlapping intervals at any point). Sorting intervals by start time and assigning to the earliest available server using a min-heap guarantees exactly d machines.",
        "Phase_II/include/algorithms/greedy/interval_partitioning.hpp",
        ("Time: O(N log N) using std::priority_queue", "Space: O(d) heap size where d is depth"),
        "int min_ci_servers(vector<Interval>& tasks) {\n    sort(tasks.begin(), tasks.end(), [](auto& a, auto& b){ return a.start < b.start; });\n    priority_queue<int, vector<int>, greater<int>> min_heap;\n    for (const auto& task : tasks) {\n        if (!min_heap.empty() && min_heap.top() <= task.start) min_heap.pop();\n        min_heap.push(task.end);\n    }\n    return min_heap.size(); // Exactly equals interval depth d!\n}",
        "\"Interval partitioning finds the minimum number of parallel CI machines equal to the chromatic number of the interval graph. By sorting tasks by start time and querying a min-heap of active server finish times, we reuse servers immediately when a test completes, achieving the optimal depth d in O(N log N) time.\""
    ))

    story.append(add_q(
        19, "Explain Huffman Lossless Encoding. Why is the prefix-free property mandatory for decompression?",
        "Tests min-heap tree construction, prefix property, and compression ratio.",
        "Huffman builds a binary tree bottom-up by repeatedly merging the two lowest-frequency characters using a min-heap. Variable-length codes are assigned: frequent characters get short bitstrings. The prefix-free property (no codeword is a prefix of another) ensures instantaneous, unambiguous decoding without delimiters.",
        "Phase_II/include/algorithms/greedy/huffman.hpp",
        ("Time: O(K log K) where K is unique characters", "Space: O(K) tree nodes"),
        "// Huffman Tree Node merge in min_heap:\nNode* left = min_heap.top(); min_heap.pop();\nNode* right = min_heap.top(); min_heap.pop();\nNode* parent = new Node('\\0', left->freq + right->freq, left, right);\nmin_heap.push(parent);",
        "\"In our benchmark on issue crash logs, Huffman encoding compressed 552 bits to 275 bits, achieving a 2.007x lossless compression ratio. Because every character sits exclusively at a leaf node of the binary tree, no codeword is a prefix of another, allowing linear O(N) decompression.\""
    ))

    story.append(add_q(
        20, "Compare Kruskal’s vs Prim’s Minimum Spanning Tree algorithms. Which is preferred for sparse graphs?",
        "Tests graph representations, Disjoint Set Union (DSU), and greedy edge selection.",
        "Kruskal sorts all edges and uses Disjoint Set Union with path compression and union-by-rank to prevent cycles in O(E log E) time. Prim grows a single tree using a min-heap of cut-crossing edges in O(E log V) time. For sparse graphs where E approx V, Kruskal is preferred; for dense graphs where E approx V^2, Prim with adjacency matrix is faster.",
        "Phase_II/include/algorithms/greedy/mst.hpp",
        ("Kruskal: O(E log V) | Prim: O(E log V)", "Space: O(V) for DSU parent array or Min-Heap"),
        "int find_root(int i, vector<int>& parent) {\n    if (parent[i] == i) return i;\n    return parent[i] = find_root(parent[i], parent); // Path Compression!\n}",
        "\"Both Kruskal and Prim produced the identical minimum spanning tree cost of 16 in our module refactoring tests. Kruskal is an edge-centric greedy algorithm relying on Disjoint Set Union with path compression. For sparse dependency graphs, Kruskal is highly cache-friendly and easier to implement.\""
    ))

    story.append(PageBreak())

    # ==================== CATEGORY 5: DYNAMIC PROGRAMMING ====================
    story.append(Paragraph("Category 5: Dynamic Programming Formulations & Space Optimizations", section_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=8))

    story.append(add_q(
        21, "Formulate the 0/1 Knapsack DP recurrence. Why MUST the 1D space-optimized array iterate backwards?",
        "A classic viva question testing 1D state collapsing and single-choice invariants.",
        "Recurrence: dp[i][w] = max(dp[i-1][w], dp[i-1][w - wt[i]] + val[i]). To compress this to 1D array dp[w], we must iterate backwards from W down to wt[i]. Forward iteration would overwrite dp[w - wt[i]] with the value from the CURRENT item, inadvertently solving Unbounded Knapsack (allowing multiple inclusions of the same item).",
        "Phase_II/include/algorithms/dynamic_programming/knapsack_01.hpp",
        ("Time: Theta(N * W)", "Space: 2D is O(N * W) | 1D is O(W)"),
        "// 1D Space-Optimized Knapsack DP:\nvector<int> dp(W + 1, 0);\nfor (int i = 0; i < N; ++i) {\n    for (int w = W; w >= wt[i]; --w) { // MUST BE BACKWARDS!\n        dp[w] = max(dp[w], dp[w - wt[i]] + val[i]);\n    }\n}",
        "\"In 2D DP, computing state (i, w) depends on row i-1. When collapsing to a single 1D array of size W, backward iteration from W down to wt[i] ensures that dp[w - wt[i]] still holds the value from iteration i-1. Iterating forward would use the newly updated value, which would allow the same issue to be selected multiple times.\""
    ))

    story.append(add_q(
        22, "Explain Matrix Chain Multiplication (MCM). Why can't we just multiply matrices left-to-right?",
        "Checks matrix dimension multiplication costs and Catalan number state space.",
        "Matrix multiplication is associative ((AB)C = A(BC)) but the scalar multiplication cost varies dramatically. Multiplying A (10x100), B (100x5), C (5x50): (AB)C costs 10*100*5 + 10*5*50 = 7,500 operations. A(BC) costs 100*5*50 + 10*100*50 = 75,000 operations (10x slower!). DP finds the optimal split k in O(n^3) time.",
        "Phase_II/include/algorithms/dynamic_programming/matrix_chain.hpp",
        ("Time: Theta(N^3)", "Space: Theta(N^2) table"),
        "for (int len = 2; len <= n; ++len) {\n    for (int i = 1; i <= n - len + 1; ++i) {\n        int j = i + len - 1; m[i][j] = INF;\n        for (int k = i; k < j; ++k) {\n            int q = m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j];\n            if (q < m[i][j]) { m[i][j] = q; s[i][j] = k; }\n        }\n    }\n}",
        "\"MCM minimizes scalar arithmetic operations when evaluating composite dependency transformations. In our test, the optimal split (((A1 A2) A3) A4) reduced multiplications from 75,000 to 30,000. DP solves this by evaluating sub-chains of increasing length L from 2 to n in O(n^3) time.\""
    ))

    story.append(add_q(
        23, "Explain Longest Common Subsequence (LCS). How does AutoTriage compute bug report similarity?",
        "Tests subsequence vs substring formulation and similarity metrics.",
        "LCS identifies shared sequential tokens between two crash stack traces without requiring contiguous placement. Recurrence: if s1[i-1] == s2[j-1], dp[i][j] = 1 + dp[i-1][j-1]; else dp[i][j] = max(dp[i-1][j], dp[i][j-1]). Similarity is computed as 2 * LCS_len / (len1 + len2).",
        "Phase_II/include/algorithms/dynamic_programming/lcs.hpp",
        ("Time: Theta(M * N)", "Space: Full O(M * N) or Rolling O(min(M, N))"),
        "int lcs(const string& X, const string& Y) {\n    int m = X.size(), n = Y.size();\n    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));\n    for (int i = 1; i <= m; ++i) {\n        for (int j = 1; j <= n; ++j) {\n            if (X[i-1] == Y[j-1]) dp[i][j] = 1 + dp[i-1][j-1];\n            else dp[i][j] = max(dp[i-1][j], dp[i][j-1]);\n        }\n    }\n    return dp[m][n];\n}",
        "\"LCS detects duplicate issue submissions by comparing call-stack traces. In our automated test, stack traces X and Y produced an LCS length of 4 ('BCBA'), yielding a similarity metric of 61.5%. This enables automatic clustering of duplicate bug reports.\""
    ))

    story.append(add_q(
        24, "Explain Optimal Binary Search Tree (OBST). Why does it require access probabilities?",
        "Tests cost computation, search frequencies, and subtree roots.",
        "When keys have non-uniform search frequencies (some keywords are searched 90% of the time), a balanced BST is not optimal. OBST minimizes the expected search cost sum_{i=1}^n p_i * (depth(k_i) + 1) using dynamic programming over subtrees [i..j] in O(n^3) time.",
        "Phase_II/include/algorithms/dynamic_programming/obst.hpp",
        ("Time: O(N^3) | Knuth optimization: O(N^2)", "Space: Theta(N^2)"),
        "// e[i][j] = min_{i <= r <= j} (e[i][r-1] + e[r+1][j] + w(i, j))\n// where w(i, j) = sum of probabilities from i to j.",
        "\"Unlike AVL or Red-Black trees which optimize worst-case depth, OBST optimizes average-case retrieval time for known query distributions. Frequently triaged keywords like 'Segfault' and 'CVE' are placed near the root, achieving an expected search cost of 1.9 in our automated benchmark.\""
    ))

    story.append(add_q(
        25, "Compare Dijkstra vs Bellman-Ford vs Floyd-Warshall. When does Dijkstra fail?",
        "A favorite viva question comparing single-source vs all-pairs shortest paths.",
        "Dijkstra solves single-source shortest path with non-negative edge weights using a Min-Heap in O(E log V). It fails on negative edges because its greedy finalized-distance assumption is violated. Bellman-Ford handles negative weights and detects negative cycles in O(V * E) by relaxing all edges V-1 times. Floyd-Warshall computes all-pairs shortest paths in O(V^3).",
        "Phase_II/include/algorithms/dynamic_programming/bellman_ford.hpp | floyd_warshall.hpp",
        ("Dijkstra: O(E log V) | Bellman-Ford: O(V * E)", "Floyd-Warshall: Theta(V^3) time, Theta(V^2) space"),
        "// Floyd-Warshall DP recurrence:\nfor (int k = 0; k < V; ++k)\n    for (int i = 0; i < V; ++i)\n        for (int j = 0; j < V; ++j)\n            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);",
        "\"Dijkstra is greedy and assumes that once a vertex is extracted from the priority queue, its distance is final; negative edge weights invalidate this invariant. Bellman-Ford runs V-1 relaxation passes to accommodate negative costs, and a V-th pass detects negative cycles. Floyd-Warshall uses DP to compute the entire blast radius matrix in O(V^3) time.\""
    ))

    story.append(add_q(
        26, "Explain the Held-Karp Dynamic Programming algorithm for TSP. How does it beat O(n!)?",
        "Tests bitmask representation, subproblem memoization, and factorial reduction.",
        "Naive TSP explores (n-1)! / 2 tours. Held-Karp defines dp(mask, u) as the minimum cost to visit all vertices in bitmask ending at u. Recurrence: dp(mask, u) = min_{v in mask, v != u} (dp(mask \\setminus {u}, v) + dist[v][u]). There are 2^n subsets and n vertices, yielding O(n^2 2^n) time.",
        "Phase_II/include/algorithms/dynamic_programming/tsp_held_karp.hpp",
        ("Time: Theta(N^2 * 2^N)", "Space: Theta(N * 2^N) bitmask memo table"),
        "int tsp(int mask, int u) {\n    if (mask == (1 << n) - 1) return dist[u][0]; // Return to start\n    if (memo[mask][u] != -1) return memo[mask][u];\n    int ans = INF;\n    for (int v = 0; v < n; ++v) {\n        if (!(mask & (1 << v))) ans = min(ans, dist[u][v] + tsp(mask | (1 << v), v));\n    }\n    return memo[mask][u] = ans;\n}",
        "\"Held-Karp replaces factorial brute-force with exponential bitmask dynamic programming. For N=16, 16! is over 20 trillion tours, whereas N^2 2^N is approximately 16 million operations—making the calculation computationally feasible in offline memory.\""
    ))

    story.append(PageBreak())

    # ==================== CATEGORY 6: BACKTRACKING & B&B ====================
    story.append(Paragraph("Category 6: Backtracking and Branch & Bound State Space Pruning", section_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=8))

    story.append(add_q(
        27, "Contrast Backtracking vs Branch & Bound. What is the fundamental operational difference?",
        "Checks conceptual distinction between feasibility search and optimization search.",
        "Backtracking uses Depth-First Search (DFS) with bounding/feasibility checks to find one or all valid solutions (typically decision or enumeration problems like N-Queens or Sum of Subsets). Branch & Bound uses Breadth-First or Best-First Search with an upper/lower bounding function to find an optimal solution, aggressively pruning subtrees whose bound cannot beat the current best.",
        "Phase_II/include/algorithms/backtracking_bb/knapsack_branch_and_bound.hpp",
        ("Backtracking: DFS, O(N) memory", "Branch & Bound: Best-First, O(2^N) priority queue"),
        None,
        "\"Backtracking is depth-first and abandons a path the moment it violates feasibility constraints. Branch & Bound is best-first and uses heuristic relaxation (such as Fractional Knapsack) to calculate an upper bound for every node. If a node's upper bound is less than our current best known discrete solution, the entire subtree is pruned without visiting.\""
    ))

    story.append(add_q(
        28, "Explain the N-Queens problem. How do diagonal attack check formulas work in O(1)?",
        "Tests array-based state representation and constant-time safety verification.",
        "Instead of scanning the whole board in O(N), we track three boolean lookup arrays: cols[c], diag1[r - c + N - 1] (top-left to bottom-right), and diag2[r + c] (top-right to bottom-left). A position is safe if and only if all three flags are false.",
        "Phase_II/include/algorithms/backtracking_bb/n_queens.hpp",
        ("Time: O(N!)", "Space: O(N) recursion stack and bit arrays"),
        "bool is_safe(int r, int c, int n) {\n    return !cols[c] && !diag1[r - c + n - 1] && !diag2[r + c];\n}\n// In backtrack: cols[c] = diag1[...] = diag2[...] = true; solve(r + 1); cols[c] = ... = false;",
        "\"Rather than checking board diagonals with a loop, our implementation maps diagonals to mathematical invariants: row - col is constant along major diagonals, and row + col is constant along anti-diagonals. This reduces the safety check to an O(1) lookup, allowing N=8 to find all 92 solutions in milliseconds.\""
    ))

    story.append(add_q(
        29, "Explain Sum of Subsets Backtracking. What bounding condition prunes dead-end branches?",
        "Tests pruning conditions and sorted state-space tree traversal.",
        "Given set S and target T, sort S ascending. At level i: if current_sum + S[i] > T, prune all subsequent elements (since they are even larger). Also, if current_sum + remaining_sum < T, prune immediately because even taking every remaining element cannot reach target T.",
        "Phase_II/include/algorithms/backtracking_bb/sum_of_subsets.hpp",
        ("Time: Worst-case O(2^N), Avg-case heavily pruned", "Space: O(N) recursion depth"),
        "void backtrack_subset(int i, int current_sum, int remaining_sum) {\n    if (current_sum == target) { record_solution(); return; }\n    if (i >= n || current_sum + S[i] > target || current_sum + remaining_sum < target) return; // PRUNE!\n    // Branch 1: Include S[i]\n    backtrack_subset(i + 1, current_sum + S[i], remaining_sum - S[i]);\n    // Branch 2: Exclude S[i]\n    backtrack_subset(i + 1, current_sum, remaining_sum - S[i]);\n}",
        "\"Sum of Subsets uses two powerful bounding conditions: first, sorting the set allows us to break early when an element exceeds the remaining deficit; second, if the sum of all remaining elements cannot bridge the gap to T, the branch is immediately abandoned. In our test, this pruned over 70% of the state space.\""
    ))

    story.append(add_q(
        30, "Compare FIFO, LIFO, and Least-Cost (LC) Branch & Bound for Knapsack. Why is LC superior?",
        "Directly relates to Scenario 2 benchmark results and state-space pruning.",
        "FIFO uses a standard queue (BFS); LIFO uses a stack (DFS-like). Least-Cost (LC) uses a priority queue ordered by upper bound (derived from Fractional Knapsack). LC expands the most promising node first, rapidly discovering high-quality integer solutions that immediately raise the global lower bound, pruning inferior nodes earlier.",
        "Phase_II/include/algorithms/backtracking_bb/knapsack_branch_and_bound.hpp",
        ("LC B&B: Generates fewer nodes than FIFO/LIFO", "Priority queue space: O(2^N) worst-case"),
        "// In Scenario 2 (Capacity Shock - 80h limit):\n// 0/1 Knapsack DP: Exact value 730\n// Least-Cost B&B: Exact value 730 | Nodes pruned: 20 nodes\n// FIFO B&B: Generated 19 nodes, expanded 15\n// LC B&B: Generated 11 nodes, expanded only 8!",
        "\"In our Scenario 2 capacity shock test, Least-Cost B&B matched the exact DP optimum of 730 while pruning 20 state-space nodes. By expanding nodes with highest relaxed fractional bound first, LC discovers the near-optimal solution almost immediately, pruning 47% more nodes than FIFO BFS.\""
    ))

    story.append(add_q(
        31, "Explain TSP Branch and Bound using Reduced Cost Matrix. How is the lower bound computed?",
        "Checks matrix reduction mechanics, row/column subtractions, and bounding.",
        "At each node, row reduction subtracts the minimum element of each row from all elements in that row; column reduction does the same for columns. The sum of all subtracted values is added to the parent's lower bound. When choosing edge (u, v), set row u and col v to infinity and reduce the remaining submatrix.",
        "Phase_II/include/algorithms/backtracking_bb/tsp_branch_and_bound.hpp",
        ("Time: Worst-case O(2^N * N^2), Pruned in practice", "Space: O(N^2) per tree node"),
        "int reduce_matrix(Matrix& mat, int n) {\n    int reduction_cost = 0;\n    // Subtract row minimums\n    for (int i = 0; i < n; ++i) { int rmin = find_row_min(mat, i); subtract_row(mat, i, rmin); reduction_cost += rmin; }\n    // Subtract col minimums\n    for (int j = 0; j < n; ++j) { int cmin = find_col_min(mat, j); subtract_col(mat, j, cmin); reduction_cost += cmin; }\n    return reduction_cost;\n}",
        "\"Reduced Cost Matrix calculates a rigorous lower bound: every row and column in a valid tour must contain at least one exit and entry edge. By subtracting the minimum cost from each row and column, the sum of reductions represents the minimum cost that must be incurred from that state forward, enabling aggressive pruning.\""
    ))

    story.append(PageBreak())

    # ==================== CATEGORY 7: NETWORK FLOW & MATCHING ====================
    story.append(Paragraph("Category 7: Network Flow and Maximum Bipartite Matching", section_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=8))

    story.append(add_q(
        32, "Explain Edmonds-Karp Maximum Flow. Why does BFS guarantee polynomial termination over DFS?",
        "Tests augmenting path algorithms, residual graphs, and O(V E^2) proof.",
        "Ford-Fulkerson using DFS can take O(E * |f|) time with rational capacities and may fail to terminate on irrational capacities. Edmonds-Karp uses BFS to select the shortest augmenting path (minimum number of edges) from source to sink. This guarantees that the shortest path distance to any vertex monotonically increases, yielding an upper bound of O(V * E) augmentations and O(V E^2) total time.",
        "Phase_II/include/algorithms/flow_matching/ford_fulkerson.hpp",
        ("Time: O(V * E^2)", "Space: O(V^2) residual capacity matrix"),
        "int edmonds_karp(int s, int t) {\n    int max_flow = 0;\n    vector<int> parent(V);\n    while (bfs_find_augmenting_path(s, t, parent)) {\n        int path_flow = find_bottleneck_capacity(s, t, parent);\n        augment_residual_graph(s, t, parent, path_flow);\n        max_flow += path_flow;\n    }\n    return max_flow;\n}",
        "\"Edmonds-Karp replaces Ford-Fulkerson's arbitrary DFS with BFS. By always augmenting along the shortest path in terms of edge count, each edge can become a bottleneck at most V/2 times. With E edges, the total number of augmentations is strictly bounded by O(V * E), proving O(V E^2) polynomial runtime.\""
    ))

    story.append(add_q(
        33, "Explain Kuhn’s Algorithm for Maximum Bipartite Matching. How does alternating path reversal work?",
        "Core question on Phase I matching engine and augmenting path mechanics.",
        "A matching M is maximum if and only if it contains no augmenting path (Berge's Lemma). Kuhn's algorithm runs DFS from each unmatched left vertex. If an augmenting path ending in an unmatched right vertex is found, the edges along the path are reversed: matched edges become unmatched, and unmatched edges become matched, increasing the matching cardinality by exactly 1.",
        "Phase_I/include/matching.hpp | Phase_II/include/algorithms/flow_matching/bipartite_matching.hpp",
        ("Time: O(V * E)", "Space: O(V) match array and visited flags"),
        "bool dfs_kuhn(int u, const vector<vector<int>>& adj, vector<int>& match, vector<bool>& vis) {\n    for (int v : adj[u]) {\n        if (vis[v]) continue;\n        vis[v] = true;\n        if (match[v] < 0 || dfs_kuhn(match[v], adj, match, vis)) {\n            match[v] = u; // Augmenting path reversed!\n            return true;\n        }\n    }\n    return false;\n}",
        "\"Kuhn's algorithm is based on Berge's Lemma: an alternating path starting and ending at unmatched vertices can be inverted to yield one additional matched edge. If a candidate developer is already matched, Kuhn recursively searches if that developer's current task can be reassigned to another valid developer, guaranteeing maximum bipartite cardinality in O(V * E) time.\""
    ))

    story.append(add_q(
        34, "Explain why Scenario 1 shows 100% developer utilization but 20% issue assigned.",
        "Critical conceptual question directly tested in our audit and truth table.",
        "In Scenario 1, there are 10 developers and 50 backlog issues. Under standard 1-to-1 bipartite matching semantics, each developer is assigned at most 1 issue. Therefore: Developer Utilization = 10 matched / 10 total developers = 100%. Issue Coverage = 10 assigned / 50 total issues = 20%. Multi-issue workload capacity allocation is solved separately via Knapsack DP.",
        "Phase_II/src/scenario_benchmarks.cpp (Scenario 1)",
        ("Bipartite Matching: 1-to-1 cardinality", "Capacity packing: Multi-issue 0/1 Knapsack"),
        None,
        "\"This was a deliberate distinction in our engineering audit: under classical 1-to-1 bipartite matching, each developer receives at most one issue. With 10 developers and 50 issues, 10 matches utilize 100% of our available engineers, which naturally covers exactly 20% of the backlog. Multi-issue sprint packing is handled separately by our Knapsack engine.\""
    ))

    story.append(add_q(
        35, "How does the Max-Flow Min-Cut Theorem apply to software engineering pipelines?",
        "Checks theoretical translation to real-world software architecture.",
        "The Max-Flow Min-Cut theorem states that the maximum amount of flow passing from source to sink equals the minimum total capacity of edges that, if removed, disconnect the source from the sink. In a CI/CD build or team velocity pipeline, the min-cut identifies the exact bottleneck stages restricting overall deployment throughput.",
        "Phase_II/include/algorithms/flow_matching/ford_fulkerson.hpp",
        ("Max-Flow = Min-Cut capacity", "Cut verification: O(V + E) BFS on residual graph"),
        None,
        "\"By running BFS on the final residual graph from the source, the set of reachable vertices S and unreachable vertices T defines the minimum cut. The edges crossing from S to T represent the exact team skills or CI test servers where investing additional resources will directly increase project throughput.\""
    ))

    story.append(add_q(
        36, "WHITEBOARD LIVE CODING: Write Kuhn’s DFS matching function from scratch.",
        "Mandatory live coding test from Examiner Guidelines Section 4.",
        "Ten-line recursive DFS pattern utilizing match and visited tracking arrays.",
        "Phase_I/include/matching.hpp",
        ("Time: O(V * E)", "Space: O(V)"),
        "bool dfs_kuhn(int u, const vector<vector<int>>& adj, vector<int>& match, vector<bool>& visited) {\n    for (int v : adj[u]) {\n        if (!visited[v]) {\n            visited[v] = true;\n            if (match[v] == -1 || dfs_kuhn(match[v], adj, match, visited)) {\n                match[v] = u;\n                return true;\n            }\n        }\n    }\n    return false;\n}",
        "\"(Write the 10-line function above on the whiteboard). This function loops over all candidate developers v compatible with issue u. If developer v is unassigned or if v's current assignment can be successfully rerouted via an alternating augmenting path, we update match[v] = u and return true.\""
    ))

    story.append(PageBreak())

    # ==================== CATEGORY 8: STRING MATCHING & NUMBER THEORY ====================
    story.append(Paragraph("Category 8: String Matching and Modular Arithmetic", section_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=8))

    story.append(add_q(
        37, "Compare the 4 string matching algorithms: Naive, Rabin-Karp, Finite Automata, and KMP.",
        "Tests pattern matching mechanics, preprocessing costs, and text scans.",
        "Naive: O(m(n-m+1)) time, O(1) space, backtracks text pointer. Rabin-Karp: O(n+m) avg using rolling hash, O(m*n) worst due to hash collisions. Finite Automata: O(m * Sigma) preprocessing, O(n) text scan with 0 backtracks. KMP: O(m) preprocessing via pi-table, O(n) text scan with 0 backtracks and independent of alphabet size Sigma.",
        "Phase_II/include/algorithms/string_matching/string_matchers.hpp",
        ("Preprocessing: KMP O(m) | FA O(m * Sigma)", "Matching: KMP O(n) guaranteed"),
        None,
        "\"Naive string matching backtracks both text and pattern pointers upon mismatch. Rabin-Karp hashes substrings in O(1) but suffers from spurious collisions. Finite Automata achieves O(n) matching but has O(m * Sigma) transition table overhead. KMP achieves optimal O(m) preprocessing and O(n) search with zero text backtracks regardless of alphabet size.\""
    ))

    story.append(add_q(
        38, "Explain KMP’s Failure Function (pi-table / LPS). How does it avoid text backtracks?",
        "Checks deep technical mastery of prefix function and automaton theory.",
        "The LPS array stores the length of the Longest Proper Prefix of pattern[0..i] that is also a Suffix of pattern[0..i]. When mismatch occurs at pattern index j, the text pointer does NOT move backward; instead, pattern pointer shifts to pi[j-1]. The characters prior to pi[j-1] are mathematically guaranteed to match the preceding text.",
        "Phase_II/include/algorithms/string_matching/string_matchers.hpp",
        ("LPS Computation: Theta(M) time", "Matching: Theta(N) operations"),
        "vector<int> compute_pi_table(const string& P) {\n    int m = P.size(); vector<int> pi(m, 0);\n    for (int i = 1, k = 0; i < m; ++i) {\n        while (k > 0 && P[k] != P[i]) k = pi[k - 1];\n        if (P[k] == P[i]) ++k;\n        pi[i] = k;\n    }\n    return pi;\n}",
        "\"The pi-table preprocesses self-similarities within the pattern in linear O(m) time. When a mismatch occurs, the LPS value informs us of the longest prefix already matched by the suffix ending at the mismatch. We slide the pattern forward without ever retreating the text pointer, guaranteeing strict O(n) scan time.\""
    ))

    story.append(add_q(
        39, "Explain the Scenario 3 Adversarial String Matching experiment (50,001 chars). What happened?",
        "Directly references our live benchmark findings on pathological logs.",
        "Text: 50,000 'A's followed by 'B'. Pattern: 500 'A's followed by 'B'. Naive matching matches 500 characters, mismatches on 'B', and slides forward by only 1 character, repeating 500 comparisons thousands of times (totaling 299,976 comparisons). KMP uses the LPS table to recognize that all 499 preceding characters match, advancing without backtracking in 100,005 operations (3x faster).",
        "Phase_II/src/scenario_benchmarks.cpp (Scenario 3)",
        ("Naive: 299,976 comparisons (heavy backtracking)", "KMP: 100,005 operations (0 backtracks)"),
        None,
        "\"In Scenario 3, we subjected both algorithms to a pathological 50,001-character crash log. Naive matching wasted 299,976 comparisons due to constant pointer resets. KMP processed the identical log in 100,005 operations with exactly zero pointer backtracks, empirically proving the power of linear prefix automata.\""
    ))

    story.append(add_q(
        40, "Explain the Chinese Remainder Theorem (CRT). What mathematical condition is required?",
        "Tests number theory, Extended Euclidean algorithm, and modular inverses.",
        "CRT finds a unique integer x modulo M = prod m_i satisfying a system of congruences x equiv a_i pmod{m_i}, provided all moduli m_i are pairwise coprime (gcd(m_i, m_j) = 1 for all i != j). Solution: x = sum (a_i * M_i * y_i) mod M, where M_i = M / m_i and y_i = M_i^{-1} mod m_i computed via Extended Euclidean.",
        "Phase_II/include/algorithms/number_theory/crt.hpp",
        ("Time: O(k log(max m_i)) where k is congruences", "Space: O(1) auxiliary"),
        "long long crt_solve(const vector<long long>& a, const vector<long long>& m) {\n    long long M = 1, x = 0;\n    for (long long mod : m) M *= mod;\n    for (size_t i = 0; i < a.size(); ++i) {\n        long long Mi = M / m[i];\n        long long yi = modular_inverse(Mi, m[i]);\n        x = (x + a[i] * Mi % M * yi % M) % M;\n    }\n    return (x + M) % M;\n}",
        "\"In distributed microservices, servers emit periodic heartbeats at different coprime cycle intervals. In our Chunk 6 test, synchronizing heartbeat offsets (x = 2 mod 3, x = 3 mod 5, x = 2 mod 7) used CRT to find the unique global synchronization epoch x = 23 mod 105 in logarithmic time via Extended Euclidean modular inverses.\""
    ))

    story.append(add_q(
        41, "Explain Rabin-Karp Rolling Hash. How does Horner’s rule compute hash updates in O(1)?",
        "Checks hash collision management and constant-time rolling window mechanics.",
        "Given window text[i..i+m-1], its hash is sum_{j=0}^{m-1} text[i+j] * d^{m-1-j} mod q. To slide the window to i+1: subtract the leading character (text[i] * d^{m-1}), multiply by radix d, add the incoming character text[i+m], and take modulo q. This update runs in O(1) time.",
        "Phase_II/include/algorithms/string_matching/string_matchers.hpp",
        ("Hash update: O(1) per character", "Worst case: O(n * m) if all hashes collide"),
        "// Rolling hash update:\nhash = (d * (hash - text[i] * h) + text[i + m]) % q;\nif (hash < 0) hash += q;",
        "\"Rabin-Karp transforms substring comparison into integer arithmetic. Using Horner's rule, rolling the window to the next character requires only subtracting the high-order term and adding the low-order term in O(1) time. When hashes match, we perform a character check to eliminate spurious collisions.\""
    ))

    story.append(PageBreak())

    # ==================== CATEGORY 9: COMPLEXITY & REDUCTIONS ====================
    story.append(Paragraph("Category 9: Computational Complexity and Polynomial Reductions", section_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=8))

    story.append(add_q(
        42, "Define the complexity classes P, NP, NP-Complete, and NP-Hard. Where does Knapsack sit?",
        "Foundational DAA theoretical question mandated by syllabus Unit 6.",
        "P: Decision problems solvable in polynomial time O(n^k) by a deterministic Turing machine. NP: Problems verifiable in polynomial time by a deterministic Turing machine (or solvable in polynomial time by a non-deterministic Turing machine). NP-Hard: At least as hard as every problem in NP. NP-Complete: Both in NP and NP-Hard. 0/1 Knapsack is NP-Complete (decision version).",
        "Phase_II/include/core/complexity_reductions.hpp",
        ("P subseteq NP", "NP-Complete = NP cap NP-Hard"),
        None,
        "\"P contains problems solvable in polynomial time, like Merge Sort O(n log n). NP contains problems where a candidate certificate can be verified in polynomial time. NP-Complete problems are the hardest problems in NP: if any NPC problem has a polynomial solution, then P = NP. Discrete 0/1 Knapsack is NP-Complete; Fractional Knapsack is in P.\""
    ))

    story.append(add_q(
        43, "Prove that Subset-Sum polynomial-time reduces to 0/1 Knapsack (Subset-Sum <=_P 0/1 Knapsack).",
        "Essential viva proof demonstrating reduction construction and bidirectional equivalence.",
        "Given Subset-Sum instance: set S = {s1..sn} and target T. Construct Knapsack instance: n items with weights w_i = s_i, values v_i = s_i, and knapsack capacity W = T. We ask: can we achieve value at least V = T? Proof: (=>) If subset S' sums to T, sum_{i in S'} w_i = T <= W and sum_{i in S'} v_i = T >= V (YES). (<=) If knapsack has value >= T with weight <= T, since w_i = v_i, total weight = total value = T, so selected items sum to T (YES).",
        "Phase_II/include/core/complexity_reductions.hpp",
        ("Reduction mapping time: Theta(N) polynomial", "Verification of solution: O(N) linear"),
        "KnapsackInstance reduce_subset_sum_to_knapsack(const vector<int>& S, int T) {\n    KnapsackInstance kp;\n    kp.W = T; kp.target_val = T;\n    for (int s : S) { kp.weights.push_back(s); kp.values.push_back(s); }\n    return kp; // Construction takes exactly O(n) linear time!\n}",
        "\"To reduce Subset-Sum to 0/1 Knapsack, we map each element s_i to an item with weight s_i and value s_i, setting capacity W = T and target value V = T. This transformation takes linear O(n) time. A valid subset summing to T exists if and only if the knapsack can achieve value >= T, proving Subset-Sum <=_P 0/1 Knapsack.\""
    ))

    story.append(add_q(
        44, "What is the distinction between Reduction Construction Complexity and Solution Verification Complexity?",
        "Key technical precision point highlighted in our professor audit.",
        "The polynomial reduction construction itself f: I_{SS} -> I_{KP} runs in strictly O(n) time and space. However, solving the resulting instance or exhaustively verifying all candidate solutions takes exponential time O(2^n) or pseudo-polynomial time O(nW). A reduction requires only that the mapping function f is polynomial, NOT that the problem is easy to solve.",
        "Phase_II/include/core/complexity_reductions.hpp",
        ("Mapping Construction: O(N) polynomial", "Exhaustive verification: O(2^N) or O(N * W)"),
        None,
        "\"A common viva trap is confusing reduction construction with instance solving. The reduction mapping merely translates the problem formulation, which takes O(n) time. Solving the resulting 0/1 Knapsack instance remains NP-hard. Our Chunk 6 verifier formally checks this bidirectional equivalence across both YES and NO instances.\""
    ))

    story.append(add_q(
        45, "Why is 0/1 Knapsack O(n W) called 'Pseudo-Polynomial' rather than true polynomial time?",
        "Advanced theoretical question testing understanding of numeric input length.",
        "In complexity theory, input size is measured by the number of bits needed to encode the input. The capacity W requires k = log_2 W bits to represent. Therefore, O(n W) = O(n * 2^k), which is exponential in the input size of W. If W grows exponentially with respect to input bit length, the algorithm takes exponential time. Hence, it is pseudo-polynomial.",
        "Phase_II/include/algorithms/dynamic_programming/knapsack_01.hpp",
        ("Pseudo-polynomial: O(n * W) = O(n * 2^{bit_length})", "Polynomial only if W is bounded by poly(n)"),
        None,
        "\"Complexity is defined with respect to the input length in bits. A capacity W of 1,000,000 takes only 20 bits to store, yet requires 1,000,000 loop iterations. Because runtime is exponential in the bit-length of W, 0/1 Knapsack is pseudo-polynomial—not strongly polynomial. If W is small, DP runs fast; if W is astronomical, Branch & Bound or approximation is required.\""
    ))

    story.append(PageBreak())

    # ==================== CATEGORY 10: DEFENSIVE ENGINEERING & VIVA TACTICS ====================
    story.append(Paragraph("Category 10: Defensive Engineering, Whiteboard Live Coding & FAQ Tactics", section_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=8))

    story.append(add_q(
        46, "How does your Circular Prerequisite Dependency Detection work? Explain the 3-color DFS traversal.",
        "Tests graph cycle detection, topological sorting prerequisites, and deadlock prevention.",
        "Issue prerequisites form a directed graph G=(V, E). A circular dependency (A requires B, B requires A) is a directed cycle that creates an unresolvable deadlock. We use 3-color DFS: White (unvisited = 0), Gray (currently visiting on active call stack = 1), Black (fully processed = 2). If a DFS traversal encounters a Gray vertex, a back-edge exists, proving a cycle.",
        "Phase_I/include/parser.hpp (check_circular_dependencies)",
        ("Time: O(V + E)", "Space: O(V) color tracking array"),
        "bool dfs_cycle(int u, const vector<vector<int>>& adj, vector<int>& color) {\n    color[u] = 1; // GRAY: visiting\n    for (int v : adj[u]) {\n        if (color[v] == 1) return true; // BACK-EDGE DETECTED! CYCLE!\n        if (color[v] == 0 && dfs_cycle(v, adj, color)) return true;\n    }\n    color[u] = 2; // BLACK: visited\n    return false;\n}",
        "\"In Phase I Test 7, our newly implemented cycle detector trapped a circular prerequisite between Issue #1 and Issue #2. Using standard 3-color DFS traversal, any edge pointing to a Gray node indicates a back-edge to an active ancestor in the recursion stack, guaranteeing detection of circular deadlocks in linear O(V + E) time.\""
    ))

    story.append(add_q(
        47, "Explain Scenario 4’s Online Streaming Simulation. How did you measure an empirical competitive ratio of 1.0000?",
        "Tests online algorithms, competitive analysis, and real-time preemption.",
        "An online algorithm processes an arrival stream without knowledge of future requests. Competitive ratio CR = Value(Online) / Value(Offline Optimal). In Scenario 4, 20 issues arrive dynamically over an 80-hour simulated week. Emergency P0 zero-days preempt in-flight lower-priority tasks on busy developers. The online engine matched all 20 offline optimal assignments, achieving CR = 1.0000.",
        "Phase_II/src/scenario_benchmarks.cpp (Scenario 4) | include/algorithms/online_streaming/online_triage.hpp",
        ("Online Time: O(1) per task dispatch", "7 real-time zero-day preemptions logged"),
        None,
        "\"In Scenario 4, we simulated an 80-hour arrival stream. When an emergency CVE arrived at Hour 28 and all senior maintainers were booked, our online triage engine paused task #108 on developer Elena, re-queued it, and immediately dispatched the emergency CVE. Because our preemptive strategy avoided any SLA breaches, our empirical competitive ratio matched the offline optimum at 1.0000.\""
    ))

    story.append(add_q(
        48, "How do you allocate the 12-minute evaluation slot (8 min demo + 4 min viva) according to Examiner Guidelines?",
        "Directly addresses official guidelines timing and demonstration structure.",
        "Minute 0-1: Problem Statement & Two-Tier Architecture. Minute 1-2.5: Phase I Test Harness (7/7 tests). Minute 2.5-4.5: Phase II 4 Demonstration Scenarios (benchmarks, pruning, KMP speedup, Gantt chart). Minute 4.5-5.5: Online Streaming Preemption. Minute 5.5-6.5: Interactive CLI. Minute 6.5-7: Conclusion & Inviting Viva Questions. Minutes 7-12: Technical Viva & Whiteboard Defense.",
        "LIVE_DEMONSTRATION_SCRIPT.md | docs/viva_defense_toolkit.md",
        ("Demo: Strictly 8 minutes", "Viva: 4 minutes technical defense"),
        None,
        "\"We prepared a timed 7-minute live demonstration script followed by 1 minute for clean transition. We immediately show the working C++17 terminals rather than wasting time on UI slides, highlighting the 7 Phase I tests, the 4 Phase II stress scenarios, and our online preemption logs, reserving the final 4 minutes entirely for technical examiner questions.\""
    ))

    story.append(add_q(
        49, "What if the project encounters an unexpected bug during the live evaluation? (FAQ Q19)",
        "Directly addresses Examiner FAQ Q19 on live demonstration contingencies.",
        "According to FAQ Q19: 'Explain the issue, demonstrate available functionality, and discuss your approach.' Do not panic or restart blindly. Identify the failing assertion, explain the invariant, fall back to the pre-compiled standalone test executables (test_chunk2 through test_chunk6), and show the working source code logic.",
        "Phase_I/tests/test_runner.cpp | Phase_II/src/scenario_benchmarks.cpp",
        ("Pre-compiled modular test binaries ready on disk", "Full test logs and screenshots available in docs/"),
        None,
        "\"If an unexpected terminal glitch occurs, I would calmly explain the exact state invariant, demonstrate our modular chunk executables (test_chunk2 through test_chunk6) which isolate each algorithm independently, and walk the examiner through the source code and pre-compiled CSV benchmarks in scenario_benchmark_results.csv.\""
    ))

    story.append(add_q(
        50, "How do you defend code authorship and AI tool usage under Examiner FAQ Q16?",
        "Critical integrity question addressing Examiner FAQ Q16 and solo ownership.",
        "FAQ Q16 states: 'AI tools may assist learning, development, and debugging, but you must fully understand and explain your submitted code.' Defense: demonstrate line-by-line understanding, explain every data structure decision, reproduce canonical functions on the whiteboard from memory, and explain why specific optimizations (like Median-of-3 or 1D Knapsack) were designed.",
        "docs/Declaration.pdf | docs/AutoTriage_DAA_Final_Project_Report.pdf",
        ("Academic Integrity: 100% solo code ownership", "Signed Declaration of Originality on file"),
        None,
        "\"I personally designed, implemented, and debugged the architecture and data structures in this repository. Every algorithm—from Kuhn's augmenting path traversal to 1D Knapsack DP and KMP's failure table—was built from first principles. I am fully prepared to write any algorithm on the whiteboard, trace any execution with custom examiner numbers, or modify the code live in front of the panel.\""
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Top 50 Viva Question Bank PDF generated: {pdf_path}")

if __name__ == "__main__":
    build_viva_question_bank_pdf()
