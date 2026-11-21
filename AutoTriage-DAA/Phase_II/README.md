# AutoTriage-DAA: Phase II Complete Integrated Workbench (Project 50)
**Course:** Design and Analysis of Algorithms (DAA - PBL)  
**Author:** Ritigya Mishra | **SAP ID:** 590028115 | **Batch:** B-9 (AI/ML) | **Course:** B.Tech-CSE  
**Implementation Standard:** C++17 (Strict ISO C++17 Offline Implementation)  

---

## 1. Executive Summary & Product Scope
`AutoTriage-DAA` is an offline software engineering triage and developer assignment decision system. Designed for open-source repository maintainers and release leads, it transforms raw issue backlogs, bug reports, and dependency links into optimal sprint release plans and developer assignments.

Simultaneously, `Phase_II` serves as a **Complete Syllabus Workbench**, containing student-authored, ground-up implementations of all 46 lecture topics from Units I through VI of the Design and Analysis of Algorithms curriculum.

---

## 2. Directory Structure of Phase II
```
Phase_II/
├── CMakeLists.txt                      # CMake build script (CMAKE_CXX_STANDARD 17)
├── Makefile                            # Offline GNU Makefile (-std=c++17)
├── README.md                           # This comprehensive documentation guide
├── scenario_benchmark_results.csv      # Exported benchmark metrics across 4 scenarios
├── assignment_plan_report.csv          # Exported triage backlog and assignment report
├── data/
│   ├── synthetic_enterprise_issues.csv # Synthetic enterprise defect dataset (120 issues)
│   └── synthetic_enterprise_developers.csv # Synthetic developer profile dataset (16 devs)
├── include/
│   ├── core/
│   │   ├── models.hpp                  # Domain entities: Issue, Developer, SortStats
│   │   ├── parser.hpp                  # Defensive CSV parser with 3-color DFS cycle detection
│   │   ├── sorting.hpp                 # Multi-key Merge Sort & Median-of-3 Quick Sort
│   │   ├── report_exporter.hpp         # Architecture decoupling: dedicated CSV/report persistence
│   │   ├── visualizer.hpp              # ASCII Sprint Capacity & Gantt matrix
│   │   └── complexity_reductions.hpp   # Polynomial reduction: Subset-Sum <=_P 0/1 Knapsack
│   └── algorithms/
│       ├── divide_and_conquer/         # Unit II: Strassen, Max Subarray, Fast Power, Celebrity
│       ├── greedy/                     # Unit III: Fractional Knapsack, Activity, Interval, Huffman, Dijkstra, MST
│       ├── dynamic_programming/        # Unit IV: 0/1 Knapsack, MCM, LCS, OBST, Bellman-Ford, Floyd, TSP
│       ├── backtracking_bb/            # Unit V: N-Queens, Sum of Subsets, Knapsack B&B (FIFO/LIFO/LC), TSP B&B
│       ├── flow_matching/              # Unit VI: Edmonds-Karp Max Flow, Bipartite Matching
│       ├── number_theory/              # Unit VI: Chinese Remainder Theorem (CRT)
│       ├── online_streaming/           # Online competitive triage & preemption engine
│       └── string_matching/            # Unit VI: 4-Way Suite (Naive, Rabin-Karp, DFA, KMP)
├── src/
│   ├── main.cpp                        # Interactive 11-module CLI application
│   └── scenario_benchmarks.cpp         # 4 Mandatory Demonstration Scenarios runner
├── docs/
│   ├── final_report.md                 # Complete academic report with complexity tables & ethics
│   └── viva_defense_toolkit.md         # 5-min code templates, trace sheets & 25 viva Q&As
└── tests/
    ├── test_chunk2_dnc.cpp             # Unit II test suite (4/4 tests passing)
    ├── test_chunk3_greedy.cpp          # Unit III test suite (6/6 tests passing)
    ├── test_chunk4_dp.cpp              # Unit IV test suite (7/7 tests passing)
    ├── test_chunk5_backtracking_bb.cpp # Unit V test suite (5/5 tests passing)
    └── test_chunk6_flow_strings_crt.cpp# Unit VI test suite (5/5 tests passing)
```

---

## 3. Quick Start: Offline Compilation & Execution

### Option A: Using GNU Make (Compiles Everything under C++17)
```powershell
cd Phase_II
make

# Run interactive application
./main.exe

# Run the 4 mandatory demonstration scenarios
./scenario_benchmarks.exe

# Run complete test suite (all 5 test binaries)
make test
```

### Option B: Direct GCC Compilation (MinGW)
```powershell
cd Phase_II

# Compile interactive workbench
g++ -std=c++17 -O3 -Wall -Wextra -Iinclude src/main.cpp -o main.exe

# Compile scenario benchmarks
g++ -std=c++17 -O3 -Wall -Wextra -Iinclude src/scenario_benchmarks.cpp -o scenario_benchmarks.exe

# Execute
./main.exe
./scenario_benchmarks.exe
```

---

## 4. Complete Syllabus Workbench Coverage (Units I – VI)

| Unit & Lecture | Implemented Algorithm | File Location | Complexity Bounds | Domain Role in Project 50 |
| :--- | :--- | :--- | :--- | :--- |
| **Unit I (L1–L10)** | Asymptotic Analysis & Recurrences | `core/models.hpp`, `docs/final_report.md` | $O, \Omega, \Theta, o, \omega$ | Formal derivations for all recursive submodules via Master Theorem. |
| **Unit II (L11–L12)** | Merge Sort & Quick Sort | `core/sorting.hpp` | Merge: $\Theta(n \log n)$<br/>Quick: Avg $\Theta(n \log n)$ | Backlog prioritization; Median-of-3 eliminates anti-quicksort attacks. |
| **Unit II (L13)** | Strassen's Matrix Multiplication | `algorithms/divide_and_conquer/strassen.hpp` | Classical: $O(n^3)$<br/>Strassen: $\Theta(n^{2.807})$ | Developer co-maintenance intensity matrix ($M = C \times C^T$). |
| **Unit II (L14)** | Maximum Subarray Problem | `algorithms/divide_and_conquer/max_subarray.hpp` | D&C: $\Theta(n \log n)$<br/>Kadane: $\Theta(n)$ | Detects peak sprint bug surge / burnout interval from daily net churn. |
| **Unit II (L15)** | Fast Exponentiation / Powering | `algorithms/divide_and_conquer/fast_power.hpp` | $\Theta(\log k)$ | Markov-chain prediction of issue lifecycles ($P^k$) across sprints. |
| **Unit II (L16)** | Celebrity Problem | `algorithms/divide_and_conquer/celebrity.hpp` | $\Theta(n)$ comparisons | Identifies single Core Maintainer / review bottleneck in $O(n)$. |
| **Unit III (L17)** | Fractional Knapsack | `algorithms/greedy/fractional_knapsack.hpp` | $O(n \log n)$ | Emergency triage under divisible QA testing / bug investigation hours. |
| **Unit III (L18)** | Activity Selection | `algorithms/greedy/activity_selection.hpp` | $O(n \log n)$ | Single maintainer non-overlapping 1-on-1 code review scheduling. |
| **Unit III (L19)** | Huffman Coding | `algorithms/greedy/huffman.hpp` | $O(n \log \Sigma)$ | Lossless offline compression for massive git diffs and crash logs. |
| **Unit III (L20)** | Interval Partitioning | `algorithms/greedy/interval_partitioning.hpp` | $O(n \log n)$ (Min-Heap) | Allocates all overlapping test jobs across minimum CI servers ($d$). |
| **Unit III (L21)** | Dijkstra's Shortest Path | `algorithms/greedy/dijkstra.hpp` | $O((V+E)\log V)$ | Computes minimum refactoring risk path through module dependency DAG. |
| **Unit III (L22–L23)** | Kruskal's & Prim's MST | `algorithms/greedy/mst.hpp` | Kruskal: $O(E \log E)$<br/>Prim: $O((V+E)\log V)$ | Refactoring backbone; Kruskal uses DSU with rank & path compression. |
| **Unit IV (L24)** | 0/1 Knapsack (DP 2D + 1D) | `algorithms/dynamic_programming/knapsack_01.hpp` | $\Theta(n \cdot W)$ time<br/>$O(W)$ 1D space | Optimal sprint release selection with item backtracking recovery. |
| **Unit IV (L25)** | Matrix Chain Multiplication | `algorithms/dynamic_programming/matrix_chain.hpp` | $\Theta(n^3)$ | Optimizes relational join query execution sequences. |
| **Unit IV (L26)** | Longest Common Subsequence | `algorithms/dynamic_programming/lcs.hpp` | $\Theta(m \cdot n)$ | Duplicate bug report clustering & stack trace similarity scoring. |
| **Unit IV (L27)** | Optimal Binary Search Tree | `algorithms/dynamic_programming/obst.hpp` | $\Theta(n^3)$ | Minimizes expected lookup cost for non-uniform triage tags. |
| **Unit IV (L28)** | Bellman-Ford Algorithm | `algorithms/dynamic_programming/bellman_ford.hpp` | $\Theta(V \cdot E)$ | Single-source shortest paths and technical-debt cycle detection. |
| **Unit IV (L29)** | TSP (Held-Karp Bitmask DP) | `algorithms/dynamic_programming/tsp_held_karp.hpp` | $\Theta(n^2 2^n)$ | Optimal closed microservice inspection tour for lead maintainer. |
| **Unit IV (L30)** | Floyd-Warshall All-Pairs | `algorithms/dynamic_programming/floyd_warshall.hpp` | $\Theta(V^3)$ | All-pairs reachability and repository module blast-radius engine. |
| **Unit V (L32–L33)** | N-Queens Backtracking | `algorithms/backtracking_bb/n_queens.hpp` | $O(N!)$ worst case | Constraint satisfaction benchmark: conflict-free reviewer placement. |
| **Unit V (L34)** | Sum of Subsets Backtracking | `algorithms/backtracking_bb/sum_of_subsets.hpp` | $O(2^n)$ worst case | Pruned search for exact combinations fitting residual sprint hours. |
| **Unit V (L35)** | 0/1 Knapsack Backtracking | `algorithms/backtracking_bb/knapsack_backtracking.hpp` | $O(2^n)$ pruned | Exact sprint selection using fractional knapsack upper bounding. |
| **Unit V (L36–L37)** | Branch & Bound Suite (FIFO, LIFO, LC) | `algorithms/backtracking_bb/knapsack_branch_and_bound.hpp` | Worst $O(2^n)$ | Comparative pruning: proves Least-Cost B&B expands fewest nodes. |
| **Unit V (L38)** | TSP Branch & Bound | `algorithms/backtracking_bb/tsp_branch_and_bound.hpp` | Worst $O((n-1)!)$ | Exact microservice inspection solver using Reduced Cost Matrices. |
| **Unit VI (L39)** | Edmonds-Karp Max Flow | `algorithms/flow_matching/ford_fulkerson.hpp` | $O(V \cdot E^2)$ | Repository throughput: issue flow through skill tiers to developer capacity. |
| **Unit VI (L40)** | Max Bipartite Matching | `algorithms/flow_matching/bipartite_matching.hpp` | $O(V \cdot E)$ | Optimal two-sided assignment via reduction to Max Flow. |
| **Unit VI (L41)** | Chinese Remainder Theorem | `algorithms/number_theory/crt.hpp` | $O(k \log M)$ | Verifies distributed event log counters and tamper-proof commit signatures. |
| **Unit VI (L42–L45)** | 4-Way String Matchers | `algorithms/string_matching/string_matchers.hpp` | Naive, RK, DFA, KMP | Search for CVE signatures and error tokens in crash logs. |
| **Unit VI (L46)** | P/NP Reductions | `core/complexity_reductions.hpp` | $O(n)$ reduction | Formal proof verifier: $\text{Subset-Sum} \le_P \text{0/1 Knapsack}$. |

---

## 5. Four Mandatory Demonstration Scenarios

Run `./scenario_benchmarks.exe` to execute the official scenarios:

### Scenario 1: Normal Operation (Balanced Backlog)
* **Backlog:** 50 issues, 10 developers (40h capacity each).
* **Comparison 1 (Developer Assignment):** Under standard 1-to-1 bipartite matching semantics (one issue per developer), Max Bipartite Flow Matching achieves **100% developer utilization** (10/10 devs) and **20% issue backlog assignment** (10/50 issues), reallocating tasks via augmenting paths, while Greedy matching hits early bottlenecks on specialized skills.
* **Comparison 2 (Sprint Release Package):** 0/1 Knapsack DP selects exact discrete package of **16 issues** yielding **1244 business value points**, while Fractional Knapsack gives the theoretical upper bound of **1244.69 points**.

### Scenario 2: Capacity Shock (Emergency Release Triage)
* **Context:** Critical Zero-Day CVE disclosed 48h before release; $50\%$ of senior devs on emergency leave; capacity slashed from 200h to 80h; flood of 15 critical bugs.
* **Comparison 1 (Optimization under Shock):** 0/1 Knapsack DP achieves **730 points**; Least-Cost Branch & Bound reaches the identical **730 points** while aggressively pruning **20 state-space branches**; Fractional Knapsack yields **734 points**.
* **Comparison 2 (Dependency Rerouting):** Dijkstra bypasses the locked module, finding an alternative refactoring path: `Module 0 -> 2 -> 3 -> 4 -> 5` with risk cost = **29.0**.

### Scenario 3: Large-Scale Stress & Adversarial Shock
* **Sorting Pivot Attack ($N=5,000$ Pre-Sorted Array):** Median-of-Three Quick Sort mitigates sorted/reverse-sorted degradation (60,678 comparisons vs Merge Sort's 51,420 comparisons), noting that theoretical worst-case remains $O(n^2)$.
* **String Matchers on Repetitive Crash Log (50,001 Characters `AAAA...AB`):**
  * Naive Matcher degrades catastrophically: **299,976 comparisons**.
  * Rabin-Karp skips non-matching windows via rolling hash: **6 comparisons**.
  * Finite Automata (DFA) & KMP scan text in strict linear $\Theta(n)$ time with **zero text backtracking** (100,005 comparisons).

### Scenario 4: Synthetic Enterprise Benchmark Dataset & Online Streaming Preemption Engine
* **Dataset Scale:** 120 synthetic enterprise defect issues across 8 modules; 16 maintainers with diverse skill matrices.
* **Dynamic Online Triage:** Evaluates issues arriving sequentially under incomplete information with zero-day emergency preemption (7 preemptions triggered).
* **Empirical Competitive Ratio:** Achieves an empirical competitive ratio of **1.0000** on the synthetic enterprise workload relative to offline optimal.

---

## 6. Verification and Test Results
All 5 automated test binaries and benchmarks pass with a **100% success rate**:
* `test_chunk2_dnc.exe`: 4/4 tests passed (Strassen, Max Subarray, Fast Power, Celebrity).
* `test_chunk3_greedy.exe`: 6/6 tests passed (Fractional Knapsack, Activity Selection, Interval Partitioning, Huffman, Dijkstra, MST).
* `test_chunk4_dp.exe`: 7/7 tests passed (0/1 Knapsack 2D+1D, MCM, LCS, OBST, Bellman-Ford, Floyd-Warshall, TSP Held-Karp).
* `test_chunk5_backtracking_bb.exe`: 5/5 tests passed (N-Queens, Sum of Subsets, Knapsack Backtracking, Knapsack B&B FIFO/LIFO/LC, TSP B&B).
* `test_chunk6_flow_strings_crt.exe`: 5/5 tests passed (Edmonds-Karp Max Flow, Bipartite Flow Matching, CRT, 4-Way String Matchers, P/NP Reductions).
* `scenario_benchmarks.exe`: All 4 scenarios passed and exported strictly measured runtime variables to `scenario_benchmark_results.csv`.
* `main.exe`: All 11 interactive operational modules verified.

---

## 7. Compliance Statement
Phase II strictly complies with the Non-Negotiable Offline Policy and the C++17 build requirement. All algorithms, data structures, and test suites were implemented from first principles in portable ISO C++17 with zero external algorithmic dependencies.
