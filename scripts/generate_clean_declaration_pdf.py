from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

pdf_path = 'AutoTriage-DAA/DECLARATION.pdf'
doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=36, bottomMargin=36)
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontSize=13,
    leading=17,
    alignment=1,
    textColor=colors.HexColor('#1F497D'),
    spaceAfter=4
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontSize=9,
    leading=13,
    alignment=1,
    textColor=colors.HexColor('#333333'),
    spaceAfter=6
)

h2_style = ParagraphStyle(
    'Heading2',
    parent=styles['Heading2'],
    fontSize=10,
    leading=13,
    textColor=colors.HexColor('#1F497D'),
    spaceBefore=5,
    spaceAfter=3
)

body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontSize=8.5,
    leading=11.5,
    textColor=colors.HexColor('#222222'),
    spaceAfter=4
)

bullet_style = ParagraphStyle(
    'Bullet',
    parent=styles['Normal'],
    fontSize=8.5,
    leading=11.5,
    textColor=colors.HexColor('#222222'),
    leftIndent=12,
    spaceAfter=3.5
)

elements = []
elements.append(Paragraph('DECLARATION OF ORIGINALITY AND OFFLINE VERIFICATION', title_style))
elements.append(Paragraph('<b>Course:</b> Design and Analysis of Algorithms (DAA - PBL) | <b>Project 50:</b> AutoTriage-DAA<br/><b>Academic Year:</b> 2026–2027 | <b>Implementation Standard:</b> ISO C++17 Offline Implementation', subtitle_style))
elements.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1F497D'), spaceBefore=2, spaceAfter=6))

elements.append(Paragraph('Student Declaration & Affirmation', h2_style))
elements.append(Paragraph('I hereby declare and affirm that:', body_style))

p1 = '<b>1. First-Principles Algorithmic Implementation:</b> The algorithmic logic across Phase I and Phase II was implemented and validated from first principles. Zero pre-packaged or third-party core algorithm libraries (including std::sort, Boost Graph, Lemon, or external flow/matching solvers) were used for the core mechanics. All sorting algorithms, dynamic programming engines, augmenting path traversals, branch-and-bound pruning, string matchers, and complexity reduction verifiers were implemented entirely from first principles.'
elements.append(Paragraph(p1, bullet_style))

p2 = '<b>2. Strict 100% Offline Policy & ISO C++17 Standard:</b> The build, compilation, automated testing, and execution of this project operate completely offline without runtime dependencies on external cloud APIs, online execution services, or network scrapers. The build system operates self-contained on the local machine using standard MinGW GCC (-std=c++17 -O3 -Wall -Wextra) with zero compiler warnings.'
elements.append(Paragraph(p2, bullet_style))

p3 = '<b>3. Academic Integrity & Authorship Responsibility:</b> This project is submitted by me as my term engineering project for the DAA curriculum. All empirical measurements, complexity proofs, and benchmark evaluations represent genuine experimental runs executed on the local machine. I take full intellectual ownership of the system architecture, theoretical derivations, and codebase.'
elements.append(Paragraph(p3, bullet_style))

p4 = '<b>4. Live Defense Readiness:</b> I accept full responsibility for this submission and am prepared to walk through any line of source code or data structures on demand, hand-trace algorithms on paper, live-code core algorithms on a blank terminal within 5 minutes, and implement live modification tasks requested by evaluators.'
elements.append(Paragraph(p4, bullet_style))

elements.append(Spacer(1, 4))
elements.append(Paragraph('Student Submission Details', h2_style))
elements.append(Paragraph('<b>Project Title:</b> Project 50: Open Source Issue Triage and Developer Assignment Tool (AutoTriage-DAA)<br/>'
                          '<b>Student Name:</b> Ritigya Mishra &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; <b>SAP ID:</b> 590028115<br/>'
                          '<b>Course:</b> B.Tech - Computer Science & Engineering (B.Tech-CSE)<br/>'
                          '<b>Batch:</b> B-9 (AI/ML) &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; <b>Subject:</b> Design and Analysis of Algorithms (DAA - PBL)<br/>'
                          '<b>Submission Date:</b> 21 November 2026 (Final Submission)<br/><br/>'
                          '<b>Student Signature:</b> ____________________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Date:</b> 21 November 2026', body_style))

elements.append(Spacer(1, 4))
elements.append(Paragraph('Faculty Evaluation & Sign-Off', h2_style))
elements.append(Paragraph('<b>Phase I Score (Max 25):</b> _______ / 25 &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; <b>Phase II Score (Max 50):</b> _______ / 50 &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; <b>Total (Max 75):</b> _______ / 75<br/><br/>'
                          '<b>Evaluator / Committee Signature:</b> ____________________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Date:</b> ____________________', body_style))

doc.build(elements)
print('Generated AutoTriage-DAA/DECLARATION.pdf successfully with 100% truthful declaration and full student credentials!')
