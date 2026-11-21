# Project 50: Open Source Issue Triage and Developer Assignment Tool (AutoTriage)

**University-Topper Reference Implementation for Design and Analysis of Algorithms (DAA)**  
**Evaluation Target:** Phase I (25 Marks) + Phase II (50 Marks) = 75 / 75 Marks (100% Score)  
**Curriculum Alignment:** Complete 46-Lecture DAA Syllabus (Units I through VI)  
**Strict Policy:** 100% Offline, Zero External Core Algorithm Libraries, Clean Standard C++14/C++17  

---

## 1. Executive Summary & Architecture Overview

AutoTriage is an enterprise-grade, mathematically verified algorithmic engine designed to solve the multidimensional triage bottleneck in large-scale open-source ecosystems.

Incoming issue tickets must be categorized, prioritized, and matched against maintainer skill vectors, working capacities, and dependency constraints. AutoTriage implements **28 distinct first-principles algorithms** spanning all standard algorithmic paradigms to perform automated triage, optimal developer assignment, dependency risk analysis, and crash signature mining.

### Dual-Phase Project Organization

```
DAA PROJECT/
│
├── README.md                                              <-- [Root Project Navigation & Build Guide]
├── PROJECT_50_TOPPER_PROJECT_PLAN_AND_ARCHITECTURE_GUIDE.docx <-- [Official Word Document (38 Tables/Callouts)]
│
├── Phase_I/                                               <-- [Phase I Frozen Package - 25 Marks]
│   ├── proposal.md                                        <-- Formal Approved 1-Page Proposal
│   ├── Makefile / CMakeLists.txt                          <-- Build Automation for Phase I
│   ├── README.md                                          <-- Phase I Specification & User Manual
│   ├── include/                                           <-- Header-Only Core Engine
│   │   ├── models.hpp                                     <-- Issue & Developer Entity Structs
│   │   ├── parser.hpp                                     <-- Resilient CSV Data Stream Ingestion
│   │   ├── sorting.hpp                                    <-- Merge Sort, Quick Sort (3 Pivots), Binary Search
│   │   └── matching.hpp                                   <-- Kuhn's DFS Augmenting Path vs Greedy Matching
│   ├── src/main.cpp                                       <-- Phase I Interactive Terminal Application
│   ├── tests/test_runner.cpp                              <-- Phase I Automated Test Suite (6 Suites Passed)
│   └── data/                                              <-- Normal, Boundary, and Invalid Datasets
│
└── Phase_II/                                              <-- [Phase II Extended Workbench - 50 Marks]
    ├── Makefile / CMakeLists.txt                          <-- Phase II Multi-Binary Build Automation
    ├── README.md                                          <-- Complete Phase II Algorithmic Specification
    ├── docs/
    │   ├── final_report.md                                <-- Formal Academic Technical Report
    │   └── viva_defense_toolkit.md                        <-- Live Coding Templates, Traces & 25 Q&As
    ├── include/
    │   ├── core/                                          <-- Models, Parser, Sorting & Reductions
    │   └── algorithms/
    │       ├── divide_and_conquer/                        <-- Strassen, Kadane, Fast Power, Celebrity
    │       ├── greedy/                                    <-- Frac Knapsack, Activity, Interval, Huffman, Dijkstra, MST
    │       ├── dynamic_programming/                       <-- 0/1 Knapsack (1D/2D), MCM, LCS, OBST, Bellman-Ford, Floyd-Warshall, TSP
    │       ├── backtracking_bb/                           <-- N-Queens, Sum of Subsets, Knapsack B&B (FIFO/LIFO/LC), TSP B&B
    │       ├── flow_matching/                             <-- Edmonds-Karp Max Flow, Flow-Based Matching
    │       ├── number_theory/                             <-- Chinese Remainder Theorem (CRT)
    │       └── string_matching/                           <-- 4-Way Suite (Naive, Rabin-Karp, DFA, KMP)
    ├── src/
    │   ├── main.cpp                                       <-- Full Interactive 8-Module Engine
    │   └── scenario_benchmarks.cpp                        <-- 3 Mandatory Real-World Stress Scenarios
    └── tests/                                             <-- Exhaustive Chunk Test Suites (Chunks 2–6)
```

---

## 2. 46-Lecture Curriculum Mapping (Units I to VI)

AutoTriage maps each lecture from the DAA curriculum to a specific module in `Phase_II`:

| DAA Unit | Syllabus Lecture Topic | Core Algorithm Implemented | File Reference |
| :--- | :--- | :--- | :--- |
| **Unit I** | L1–L3: Analysis of Algorithms | Asymptotic Bound Formalism ($O, \Omega, \Theta$) | `Phase_II/include/core/models.hpp` |
| **Unit I** | L4–L6: Divide & Conquer, Merge Sort | Merge Sort (Recursive & Bottom-Up) | `Phase_II/include/core/sorting.hpp` |
| **Unit I** | L7–L8: Quick Sort & Partitioning | Quick Sort (Median-of-3, Random, First) | `Phase_II/include/core/sorting.hpp` |
| **Unit I** | L9–L10: Strassen's Matrix Multiplication | Classical $O(n^3)$ vs Strassen $O(n^{2.807})$ | `Phase_II/include/algorithms/divide_and_conquer/strassen.hpp` |
| **Unit I** | L11: Maximum Subarray Analysis | Kadane $O(n)$ vs D&C $O(n \log n)$ | `Phase_II/include/algorithms/divide_and_conquer/max_subarray.hpp` |
| **Unit I** | L12: Fast Power & Celebrity Problem | Binary Exponentiation & 2-Pointer Elimination | `Phase_II/include/algorithms/divide_and_conquer/fast_power.hpp`, `celebrity.hpp` |
| **Unit II** | L13–L14: Greedy Method & Knapsack | Fractional Knapsack (Value-Density) | `Phase_II/include/algorithms/greedy/fractional_knapsack.hpp` |
| **Unit II** | L15–L16: Activity Selection & Scheduling | Interval Scheduling & Server Partitioning | `Phase_II/include/algorithms/greedy/activity_selection.hpp`, `interval_partitioning.hpp` |
| **Unit II** | L17–L18: Huffman Codes & Compression | Optimal Prefix-Free Tree & Bitstream Encoding | `Phase_II/include/algorithms/greedy/huffman.hpp` |
| **Unit II** | L19–L20: Single-Source Shortest Paths | Dijkstra's Algorithm with Min-Heap | `Phase_II/include/algorithms/greedy/dijkstra.hpp` |
| **Unit II** | L21–L22: Minimum Spanning Trees | Kruskal's MST (DSU) & Prim's MST (Min-Heap) | `Phase_II/include/algorithms/greedy/mst.hpp` |
| **Unit III** | L23–L24: Dynamic Programming & Knapsack | 0/1 Knapsack 2D Table & 1D Space-Optimized Array | `Phase_II/include/algorithms/dynamic_programming/knapsack_01.hpp` |
| **Unit III** | L25–L26: Matrix Chain Multiplication | DP MCM $\Theta(n^3)$ with Optimal Parens Recovery | `Phase_II/include/algorithms/dynamic_programming/matrix_chain.hpp` |
| **Unit III** | L27–L28: Longest Common Subsequence | LCS Matrix with Subsequence Backtracking | `Phase_II/include/algorithms/dynamic_programming/lcs.hpp` |
| **Unit III** | L29–L30: Optimal Binary Search Trees | Dynamic Programming OBST $\Theta(n^3)$ | `Phase_II/include/algorithms/dynamic_programming/obst.hpp` |
| **Unit III** | L31–L32: Shortest Paths & Negative Cycles | Bellman-Ford $\Theta(VE)$ & Floyd-Warshall $\Theta(V^3)$ | `Phase_II/include/algorithms/dynamic_programming/bellman_ford.hpp`, `floyd_warshall.hpp` |
| **Unit III** | L33: Traveling Salesperson Problem | Held-Karp Bitmask DP $\Theta(n^2 2^n)$ | `Phase_II/include/algorithms/dynamic_programming/tsp_held_karp.hpp` |
| **Unit IV** | L34–L35: Backtracking & N-Queens | N-Queens Constraint Satisfaction Solver | `Phase_II/include/algorithms/backtracking_bb/n_queens.hpp` |
| **Unit IV** | L36–L37: Sum of Subsets & Knapsack | Feasibility & Fractional Bound DFS Pruning | `Phase_II/include/algorithms/backtracking_bb/sum_of_subsets.hpp`, `knapsack_backtracking.hpp` |
| **Unit IV** | L38–L40: Branch and Bound Strategies | FIFO vs LIFO vs Least-Cost (LC) B&B + TSP B&B | `Phase_II/include/algorithms/backtracking_bb/knapsack_branch_and_bound.hpp`, `tsp_branch_and_bound.hpp` |
| **Unit V** | L41–L42: Maximum Flow & Matching | Edmonds-Karp Flow $O(V E^2)$ & Bipartite Reduction | `Phase_II/include/algorithms/flow_matching/ford_fulkerson.hpp`, `bipartite_matching.hpp` |
| **Unit V** | L43: Number Theory & Modular Arithmetic | Chinese Remainder Theorem via Extended Euclidean | `Phase_II/include/algorithms/number_theory/crt.hpp` |
| **Unit VI** | L44–L45: String Matching Automata | 4-Way Suite: Naive, Rabin-Karp, DFA, KMP | `Phase_II/include/algorithms/string_matching/string_matchers.hpp` |
| **Unit VI** | L46: Complexity Theory & Reductions | Polynomial Reduction ($\text{Subset-Sum} \le_P \text{Knapsack}$) | `Phase_II/include/core/complexity_reductions.hpp` |

---

## 3. Quickstart: Building & Running

### Prerequisites
- Operating System: Windows / Linux / macOS
- Compiler: GCC/MinGW (g++ supporting `-std=c++14` or higher)
- Build System: `make` or `cmake` (or direct compilation commands)

### 3.1 Phase I: Build & Execute
```bash
# Navigate to Phase I directory
cd Phase_I

# Compile using GNU Make
make

# Or compile directly with g++
g++ -std=c++14 -O3 -Wall -Wextra -Iinclude src/main.cpp -o main.exe
g++ -std=c++14 -O3 -Wall -Wextra -Iinclude tests/test_runner.cpp -o test_runner.exe

# Run the automated test suite
./test_runner.exe

# Launch the interactive CLI
./main.exe
```

### 3.2 Phase II: Build & Execute All Algorithmic Modules
```bash
# Navigate to Phase II directory
cd Phase_II

# Compile all binaries using GNU Make
make

# Or run tests directly
make test

# Launch the full interactive 11-module workbench
./main.exe

# Execute the 4 Demonstration Stress & Real-World Scenarios
./scenario_benchmarks.exe
```

### 3.3 Running Individual Paradigm Test Suites
```bash
cd Phase_II
./test_chunk2_dnc.exe                 # Divide & Conquer Test Suite
./test_chunk3_greedy.exe              # Greedy Algorithms Test Suite
./test_chunk4_dp.exe                  # Dynamic Programming Test Suite
./test_chunk5_backtracking_bb.exe     # Backtracking & Branch and Bound Suite
./test_chunk6_flow_strings_crt.exe    # Flow, Strings, CRT & Reduction Suite
```

---

## 4. Key Empirical Findings

1. **Least-Cost (LC) Branch & Bound Dominance:**
   On identical 0/1 Knapsack instances, Least-Cost B&B expanded only **8 nodes**, compared to **15 nodes** for FIFO (BFS) and **9 nodes** for LIFO (DFS), empirically verifying that best-first upper-bounding minimizes search tree exploration.
2. **Adversarial Resilience:**
   On pre-sorted inputs ($N=2,000$), Lomuto First-Pivot collapsed to $1,999,000$ comparisons ($\Theta(n^2)$), while Median-of-3 pivoting completed in $26,450$ comparisons ($\Theta(n \log n)$) — an improvement of **$75.5\times$**.
3. **Linear String Search on Pathological Logs:**
   On a $50,001$-character repetitive log, Naive search required $299,976$ comparisons, whereas Knuth-Morris-Pratt (KMP) scanned the text in $100,005$ operations with **zero pointer backtracks**.
4. **Bipartite Matching Optimality:**
   Kuhn's DFS Augmenting Path algorithm achieved a $+33.3\%$ increase in triage throughput over greedy heuristics, matching the maximum capacity computed by Edmonds-Karp network flow.

---

## 5. Documentation & Viva Preparation
- **Comprehensive Project Guide:** `PROJECT_50_TOPPER_PROJECT_PLAN_AND_ARCHITECTURE_GUIDE.docx`
- **Formal Academic Report:** `Phase_II/docs/final_report.md`
- **Oral Viva & Live Coding Toolkit:** `Phase_II/docs/viva_defense_toolkit.md` (Includes 7 five-minute coding templates, 5 paper worksheets, 25 high-difficulty viva Q&As, and 10 unseen live modification solutions).

---

## 6. Academic Compliance Statement
This project strictly adheres to university project guidelines:
- Zero external libraries used for core algorithm mechanics (e.g., `<algorithm>` sort, standard graph libraries, or network flow packages are excluded; all sorting networks, heaps, tables, augmenting paths, and prefix automata are coded from scratch).
- 100% offline self-contained codebase.
- Verified compilation under standard compiler flags: `-std=c++14 -O3 -Wall -Wextra` with **zero warnings**.
