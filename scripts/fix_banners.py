import os, re

files = [
    'Phase_I/src/main.cpp',
    'AutoTriage-DAA/Phase_I/src/main.cpp',
    'Phase_II/src/main.cpp',
    'AutoTriage-DAA/Phase_II/src/main.cpp',
    'Phase_II/src/scenario_benchmarks.cpp',
    'AutoTriage-DAA/Phase_II/src/scenario_benchmarks.cpp'
]

banner_p1 = r"""void print_banner() {
    std::cout << "\n===============================================================================\n";
    std::cout << "  AutoTriage-DAA\n";
    std::cout << "  Open Source Issue Triage and Developer Assignment Tool\n\n";
    std::cout << "  Design and Analysis of Algorithms -- PBL (Project 50)\n";
    std::cout << "  Developed by: Ritigya Mishra | SAP ID: 590028115 | Batch: B-9 (AI/ML)\n";
    std::cout << "  Course: B.Tech-CSE\n";
    std::cout << "===============================================================================\n\n";
}"""

banner_p2 = r"""void print_header() {
    std::cout << "\n===============================================================================\n";
    std::cout << "  AutoTriage-DAA\n";
    std::cout << "  Open Source Issue Triage and Developer Assignment Tool\n\n";
    std::cout << "  Design and Analysis of Algorithms -- PBL (Project 50)\n";
    std::cout << "  Developed by: Ritigya Mishra | SAP ID: 590028115 | Batch: B-9 (AI/ML)\n";
    std::cout << "  Course: B.Tech-CSE\n";
    std::cout << "===============================================================================\n\n";
}"""

banner_scen = r"""    std::cout << "\n===============================================================================\n";
    std::cout << "  AutoTriage-DAA | BENCHMARK DEMONSTRATION SCENARIOS (ISO C++17)\n";
    std::cout << "  Design and Analysis of Algorithms -- PBL (Project 50)\n";
    std::cout << "  Developed by: Ritigya Mishra | SAP ID: 590028115 | Batch: B-9 (AI/ML)\n";
    std::cout << "  Course: B.Tech-CSE\n";
    std::cout << "===============================================================================\n\n";"""

for fp in files:
    if not os.path.exists(fp):
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'print_banner()' in c:
        c = re.sub(r'void print_banner\(\)\s*\{[\s\S]*?\n\}', banner_p1, c)
    if 'print_header()' in c:
        c = re.sub(r'void print_header\(\)\s*\{[\s\S]*?\n\}', banner_p2, c)
    if 'scenario_benchmarks' in fp:
        c = re.sub(r'std::cout << "\s*\\n={20,}[\s\S]*?={20,}\\n\\n";', banner_scen, c)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)

print('Successfully fixed C++ banners!')
