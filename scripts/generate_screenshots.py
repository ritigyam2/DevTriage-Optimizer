import os, subprocess, re
from PIL import Image, ImageDraw, ImageFont

font_path = "C:/Windows/Fonts/consola.ttf"
font_size = 14
font = ImageFont.truetype(font_path, font_size)
title_font = ImageFont.truetype(font_path, 12)

def clean_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def render_terminal_screenshot(text_lines, title, output_paths):
    # Calculate dimensions
    max_line_len = max(len(l) for l in text_lines) if text_lines else 60
    max_line_len = max(max_line_len, len(title) + 20, 85)
    
    char_w = 8.4
    char_h = 19
    padding_x = 24
    padding_y = 16
    title_bar_h = 36
    
    img_w = int(max_line_len * char_w + padding_x * 2)
    img_h = int(len(text_lines) * char_h + padding_y * 2 + title_bar_h)
    
    # Create image
    img = Image.new('RGB', (img_w, img_h), color='#1E1E1E')
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([0, 0, img_w, title_bar_h], fill='#2D2D2D')
    draw.line([0, title_bar_h, img_w, title_bar_h], fill='#3C3C3C', width=1)
    
    # Window controls (circles)
    circle_y = 18
    draw.ellipse([16, circle_y - 6, 28, circle_y + 6], fill='#FF5F56')
    draw.ellipse([34, circle_y - 6, 46, circle_y + 6], fill='#FFBD2E')
    draw.ellipse([52, circle_y - 6, 64, circle_y + 6], fill='#27C93F')
    
    # Title text
    draw.text((80, 10), title, fill='#CCCCCC', font=title_font)
    
    # Terminal text
    y = title_bar_h + padding_y
    for line in text_lines:
        line_str = clean_ansi(line)
        # Simple syntax highlighting based on content
        color = '#D4D4D4'
        if 'PASSED' in line_str or '[SUCCESS]' in line_str:
            color = '#4EC9B0'
        elif '===' in line_str or '---' in line_str:
            color = '#569CD6'
        elif 'AutoTriage-DAA' in line_str or 'PROJECT 50' in line_str:
            color = '#9CDCFE'
        elif 'Ritigya Mishra' in line_str or '590028115' in line_str:
            color = '#CE9178'
        elif 'Test summary:' in line_str or 'Benchmark summary:' in line_str:
            color = '#4EC9B0'
        elif 'CRITICAL' in line_str or 'WARN' in line_str or 'rejected' in line_str or 'trapped' in line_str:
            color = '#D16969'
            
        draw.text((padding_x, y), line_str, fill=color, font=font)
        y += char_h
        
    for p in output_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        img.save(p, 'PNG')
    print(f"Generated: {os.path.basename(output_paths[0])} ({img_w}x{img_h})")

# Run programs to capture genuine outputs
print("Executing programs to capture real terminal outputs...")

# 1. Main Menu
res = subprocess.run(["AutoTriage-DAA/Phase_II/main.exe"], input="11\n", capture_output=True, text=True)
menu_lines = [l for l in res.stdout.splitlines() if "Select a module" not in l]
render_terminal_screenshot(menu_lines, "AutoTriage-DAA CLI - Main Workbench Menu (C++17)", 
                           ["screenshots/01_main_menu.png", "AutoTriage-DAA/screenshots/01_main_menu.png"])

# 2. Backlog Sorting (Module 1)
res = subprocess.run(["AutoTriage-DAA/Phase_II/main.exe"], input="1\n11\n", capture_output=True, text=True)
lines = res.stdout.splitlines()
m1_lines = []
capture = False
for l in lines:
    if "MODULE 1" in l:
        capture = True
    if capture:
        m1_lines.append(l)
        if "Day " in l and len(m1_lines) > 15:
            break
render_terminal_screenshot(m1_lines, "AutoTriage-DAA - Module 1: Multi-Key Merge Sort Backlog Triage",
                           ["screenshots/02_backlog_sorting.png", "AutoTriage-DAA/screenshots/02_backlog_sorting.png"])

# 3. Developer Assignment (Module 2)
res = subprocess.run(["AutoTriage-DAA/Phase_II/main.exe"], input="2\n11\n", capture_output=True, text=True)
lines = res.stdout.splitlines()
m2_lines = []
capture = False
for l in lines:
    if "MODULE 2" in l:
        capture = True
    if capture:
        m2_lines.append(l)
        if "Total Issues Assigned" in l:
            break
render_terminal_screenshot(m2_lines, "AutoTriage-DAA - Module 2: Developer-Issue Bipartite Assignment",
                           ["screenshots/03_developer_assignment.png", "AutoTriage-DAA/screenshots/03_developer_assignment.png"])

# 4. Knapsack Comparison (Module 3)
res = subprocess.run(["AutoTriage-DAA/Phase_II/main.exe"], input="3\n11\n", capture_output=True, text=True)
lines = res.stdout.splitlines()
m3_lines = []
capture = False
for l in lines:
    if "MODULE 3" in l:
        capture = True
    if capture:
        m3_lines.append(l)
        if "Selected Issues in DP Optimal Release" in l:
            m3_lines.append(lines[lines.index(l)+1])
            m3_lines.append(lines[lines.index(l)+2])
            break
render_terminal_screenshot(m3_lines, "AutoTriage-DAA - Module 3: Sprint Release Planning (DP vs LC B&B)",
                           ["screenshots/04_knapsack_comparison.png", "AutoTriage-DAA/screenshots/04_knapsack_comparison.png"])

# 5 & 6 & 7: Phase I Tests (Defensive Validation, Cycle Detection, and Full Suite)
res_p1 = subprocess.run(["AutoTriage-DAA/Phase_I/test_runner.exe"], capture_output=True, text=True)
p1_lines = res_p1.stdout.splitlines()

# 07_phase1_tests.png
render_terminal_screenshot(p1_lines, "AutoTriage-DAA - Phase I Automated Test Harness (7/7 Passed)",
                           ["screenshots/07_phase1_tests.png", "AutoTriage-DAA/screenshots/07_phase1_tests.png"])

# 05_invalid_input_validation.png
val_lines = [l for l in p1_lines if "TEST 5" in l or "RUNNING PHASE" in l or "Test summary" in l or "====" in l]
render_terminal_screenshot(val_lines, "AutoTriage-DAA - Defensive Input Validation Trap",
                           ["screenshots/05_invalid_input_validation.png", "AutoTriage-DAA/screenshots/05_invalid_input_validation.png"])

# 06_cycle_detection.png
cycle_lines = [l for l in p1_lines if "TEST 7" in l or "RUNNING PHASE" in l or "Test summary" in l or "====" in l]
render_terminal_screenshot(cycle_lines, "AutoTriage-DAA - Circular Prerequisite Cycle Detection",
                           ["screenshots/06_cycle_detection.png", "AutoTriage-DAA/screenshots/06_cycle_detection.png"])

# 8. Divide & Conquer Tests (Chunk 2)
res = subprocess.run(["AutoTriage-DAA/Phase_II/test_chunk2_dnc.exe"], capture_output=True, text=True)
render_terminal_screenshot(res.stdout.splitlines(), "AutoTriage-DAA - Unit II Divide & Conquer Test Suite",
                           ["screenshots/08_divide_conquer_tests.png", "AutoTriage-DAA/screenshots/08_divide_conquer_tests.png"])

# 9. Greedy Tests (Chunk 3)
res = subprocess.run(["AutoTriage-DAA/Phase_II/test_chunk3_greedy.exe"], capture_output=True, text=True)
render_terminal_screenshot(res.stdout.splitlines(), "AutoTriage-DAA - Unit III Greedy Methods Test Suite",
                           ["screenshots/09_greedy_tests.png", "AutoTriage-DAA/screenshots/09_greedy_tests.png"])

# 10. Dynamic Programming Tests (Chunk 4)
res = subprocess.run(["AutoTriage-DAA/Phase_II/test_chunk4_dp.exe"], capture_output=True, text=True)
render_terminal_screenshot(res.stdout.splitlines(), "AutoTriage-DAA - Unit IV Dynamic Programming Test Suite",
                           ["screenshots/10_dp_tests.png", "AutoTriage-DAA/screenshots/10_dp_tests.png"])

# 11. Backtracking & B&B Tests (Chunk 5)
res = subprocess.run(["AutoTriage-DAA/Phase_II/test_chunk5_backtracking_bb.exe"], capture_output=True, text=True)
render_terminal_screenshot(res.stdout.splitlines(), "AutoTriage-DAA - Unit V Backtracking & Branch and Bound Suite",
                           ["screenshots/11_backtracking_tests.png", "AutoTriage-DAA/screenshots/11_backtracking_tests.png"])

# 12. Flow, Strings, CRT Tests (Chunk 6)
res = subprocess.run(["AutoTriage-DAA/Phase_II/test_chunk6_flow_strings_crt.exe"], capture_output=True, text=True)
render_terminal_screenshot(res.stdout.splitlines(), "AutoTriage-DAA - Unit VI Flow, Strings & Complexity Reductions",
                           ["screenshots/12_flow_string_tests.png", "AutoTriage-DAA/screenshots/12_flow_string_tests.png"])

# 13, 14, 15, 16: Scenarios from scenario_benchmarks.exe
res_scen = subprocess.run(["AutoTriage-DAA/Phase_II/scenario_benchmarks.exe"], capture_output=True, text=True)
scen_lines = res_scen.stdout.splitlines()

def extract_section(lines, start_keyword, end_keyword):
    res_list = []
    capture = False
    for l in lines:
        if start_keyword in l:
            capture = True
        if capture:
            if end_keyword and end_keyword in l and l != start_keyword:
                break
            res_list.append(l)
    return res_list

# 13_scenario_normal.png
s1_lines = extract_section(scen_lines, "SCENARIO 1: NORMAL SPRINT OPERATION", "SCENARIO 2:")
render_terminal_screenshot(s1_lines, "AutoTriage-DAA - Scenario 1: Normal Sprint Operation (Balanced Backlog)",
                           ["screenshots/13_scenario_normal.png", "AutoTriage-DAA/screenshots/13_scenario_normal.png"])

# 14_capacity_shock.png
s2_lines = extract_section(scen_lines, "SCENARIO 2: CAPACITY & CONSTRAINT SHOCK", "SCENARIO 3:")
render_terminal_screenshot(s2_lines, "AutoTriage-DAA - Scenario 2: Capacity Shock (LC B&B Pruning & Dijkstra)",
                           ["screenshots/14_capacity_shock.png", "AutoTriage-DAA/screenshots/14_capacity_shock.png"])

# 15_adversarial_benchmark.png
s3_lines = extract_section(scen_lines, "SCENARIO 3: LARGE-SCALE STRESS", "SCENARIO 4:")
render_terminal_screenshot(s3_lines, "AutoTriage-DAA - Scenario 3: Adversarial Quick Sort & Pathological Strings",
                           ["screenshots/15_adversarial_benchmark.png", "AutoTriage-DAA/screenshots/15_adversarial_benchmark.png"])

# 16_streaming_simulation.png
s4_lines = extract_section(scen_lines, "SCENARIO 4: SYNTHETIC ENTERPRISE", "Benchmark summary:")
render_terminal_screenshot(s4_lines, "AutoTriage-DAA - Scenario 4: Synthetic Enterprise & Online Preemptive Streaming",
                           ["screenshots/16_streaming_simulation.png", "AutoTriage-DAA/screenshots/16_streaming_simulation.png"])

print("\nAll 16 terminal screenshots successfully rendered from live execution!")
