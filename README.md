# DevTriage-Optimizer

**High-Throughput Algorithmic Decision Engine for Issue Triage and Capacity-Constrained Developer Allocation**

[Language: ISO C++17] | [Build: Passing (27/27 Suites)] | [Memory: RAII Zero-Leak] | [License: MIT]

---

## Executive Overview

DevTriage-Optimizer is a high-performance, offline algorithmic decision engine implemented in standard ISO C++17 from first principles. It resolves the multidimensional triage and developer assignment bottleneck in modern software engineering workflows.

In large-scale repositories (e.g., Linux Kernel, Kubernetes, Chromium), issue backlogs accumulate faster than maintainers can manually inspect them. DevTriage-Optimizer automates this lifecycle offline with deterministic, provably optimal algorithms:
1. Prioritizes issue backlogs deterministically via multi-key stable sorting.
2. Models developer-task assignment as a bipartite graph and solves it optimally via Kuhn's augmenting path algorithm.
3. Packages discrete sprint releases under capacity constraints using 0/1 Knapsack Dynamic Programming and Least-Cost Branch and Bound.
4. Traps circular prerequisite dependencies during CSV ingestion using 3-color Depth First Search (DFS).
5. Reroutes architectural refactoring dependencies using Dijkstra's shortest paths and mines crash logs using the Knuth-Morris-Pratt (KMP) automaton.

The codebase adheres strictly to first-principles design: zero external algorithmic solvers, zero cloud API dependencies, and zero third-party optimization libraries.

---

## Resume Impact Highlights (MNC Internship & Placement Ready)

The following bullet points summarize the technical achievements of this project for technical resumes:

* **High-Throughput Algorithm Engineering:** Engineered an offline algorithmic decision engine in ISO C++17 implementing 28 first-principles algorithms spanning Network Flow, Dynamic Programming, and Branch and Bound; reduced backlog triage latency to under 5ms for 1,000+ issues without external libraries.
* **Bipartite Assignment Modeling:** Formulated developer assignment as maximum bipartite matching on skill compatibility graphs via Kuhn's augmenting path algorithm (O(VE)), achieving 100% developer utilization while decoupling 1-to-1 matching from multi-task knapsack capacity packing.
* **Defensive Graph Engineering:** Designed an RFC 4180-compliant CSV parser with 3-color DFS graph cycle detection to trap circular prerequisite dependencies, eliminating infinite recursion and deadlock risks during ingestion.
* **Discrete Optimization & Pruning:** Implemented 0/1 Knapsack Dynamic Programming (2D table and 1D space-optimized) alongside Least-Cost Branch and Bound, achieving exact discrete optima while pruning 20 state-space nodes under a 50% capacity shock.
* **Adversarial Resilience:** Defended against worst-case inputs: engineered Median-of-Three Quick Sort reducing comparisons from 12.5M to 60,678 on 5,000 pre-sorted elements; built a KMP string matching automaton scanning 50,001-character pathological logs with zero pointer backtracks.
* **Automated Quality Assurance:** Built an automated testing framework comprising 27 test suites across 6 standalone binaries, covering Normal, Boundary, Invalid, Adversarial, and Stress scenarios with a 100% pass rate.

---

## System Architecture

The engine employs a decoupled, four-tier architecture designed for modularity, testability, and cache locality:

```
[Raw Data Streams] ---> [Data Ingestion & Validation Layer]
                         * RFC 4180 CSV Tokenizer
                         * Numeric Domain Sanitation
                         * 3-Color DFS Cycle Trapping (DAG Invariant)
                                      |
                                      v
[Algorithmic Engine] <--- [Domain Entity Data Model]
  * Multi-Key Stable Merge Sort (Backlog Triage: Sev v, Deadline ^, ID ^)
  * Kuhn Bipartite Matching (1-to-1 Assignment: S_u subset of K_v)
  * 0/1 Knapsack DP & Least-Cost B&B (Discrete Sprint Hour Packaging)
  * Dijkstra Shortest Path (Module Refactoring Risk Reroute)
  * KMP Linear Automaton (Crash Dump Error & CVE Signature Mining)
                                      |
                                      v
[Telemetry & Persistence] ---> [CLI Presentation Layer]
  * report_exporter.hpp          * Interactive ANSI Terminal
  * Dynamic CSV Benchmarks       * Color-Coded Urgency Badges
  * Zero Heap Leaks (RAII)       * ASCII Gantt Timelines & Workload Bars
```

### Architectural Concern Separation
* **Tier 1 (Production Engine):** Fast, deterministic issue prioritization, bipartite matching, sprint packing, and online preemptive event streaming.
* **Tier 2 (Algorithm Workbench):** Isolated first-principles reference implementations spanning all 46 lecture topics of the Design and Analysis of Algorithms curriculum (Units I through VI).
* **Persistence Decoupling:** Algorithmic computation is decoupled from storage via `report_exporter.hpp`, writing calculated runtime variables directly to CSV without console pollution.

---

## Algorithmic Complexity & Systems Mapping

| Module / Algorithm | Paradigm | Time Complexity | Space Complexity | Engineering Role |
| :--- | :--- | :--- | :--- | :--- |
| **Multi-Key Merge Sort** | Divide & Conquer | Theta(n log n) | O(n) | Stable triage by Severity, SLA Deadline, and deterministic ID tie-breaking. |
| **Median-of-3 Quick Sort** | Divide & Conquer | Avg Theta(n log n) | O(log n) | In-place backlog sorting; eliminates quadratic degradation on pre-sorted data. |
| **Kuhn Bipartite Matching** | Augmenting Path | O(V * E) | O(V) | Optimal 1-to-1 developer assignment on skill compatibility graphs. |
| **0/1 Knapsack DP (2D/1D)** | Dynamic Programming | Theta(n * W) | O(W) (1D) | Optimal discrete sprint packaging maximizing business value under capacity. |
| **Least-Cost Branch & Bound** | State-Space Search | Worst O(2^n) | O(2^n) | Best-first search guided by fractional bounds; aggressively prunes subtrees. |
| **3-Color DFS Cycle Trapper** | Graph Theory | O(V + E) | O(V) | Traps back-edges during CSV ingestion to prevent circular dependency deadlocks. |
| **Dijkstra Shortest Path** | Greedy / Min-Heap | O((V+E) log V) | O(V) | Computes minimum refactoring risk paths bypassing locked repository modules. |
| **Knuth-Morris-Pratt (KMP)** | String Automaton | Theta(n + m) | Theta(m) | Scans crash stack traces for CVE signatures with strictly zero backtracks. |
| **Strassen Matrix Mult** | Divide & Conquer | Theta(n^2.807) | Theta(n^2) | Computes maintainer co-editing intensity matrices faster than cubic O(n^3). |
| **Held-Karp TSP DP** | Dynamic Programming | Theta(n^2 2^n) | Theta(n 2^n) | Exact closed microservice security inspection tours across repository nodes. |
| **P/NP Polynomial Reduction**| Complexity Theory | Mapping O(n) | O(n) | Formal equivalence verifier: Subset-Sum reduces to 0/1 Knapsack in polynomial time. |

---

## Empirical Benchmarks & Comparative Telemetry

All benchmarks reflect genuine runtime execution on local hardware compiled under `-std=c++17 -O3`:

### 1. Adversarial Sorting Benchmark (N = 5,000 Pre-Sorted Integers)
* **Lomuto First-Pivot Quick Sort:** 12,497,500 comparisons (Degrades to Theta(n^2)).
* **Median-of-Three Quick Sort:** 60,678 comparisons (Mitigates sorted collapse).
* **Multi-Key Merge Sort:** 51,420 comparisons (Guaranteed Theta(n log n) stable baseline).
* *Finding:* Median-of-Three pivot selection eliminates quadratic degradation on sorted arrays, closely tracking Merge Sort.

### 2. Pathological String Search (50,001-Character Repetitive 'AAAA...B' Log)
* **Naive String Matcher:** 299,976 comparisons (Frequent text pointer backtracks, 537 microseconds).
* **Rabin-Karp Rolling Hash:** 6 comparisons (Hash filtered false matches, 389 microseconds).
* **Knuth-Morris-Pratt (KMP):** 100,005 operations (Strictly zero text pointer backtracks, 210 microseconds).
* *Finding:* KMP's precomputed prefix table executes 3x faster than Naive search under pathological crash dumps.

### 3. Branch and Bound Pruning Efficiency (0/1 Knapsack N = 4, W = 15 Hours)
* **FIFO Branch and Bound:** 15 nodes expanded, 19 generated, 2 branches pruned.
* **LIFO Branch and Bound:** 9 nodes expanded, 11 generated, 1 branch pruned.
* **Least-Cost (LC) Branch and Bound:** 8 nodes expanded, 11 generated, 5 branches pruned (Pruned most).
* *Finding:* Best-first search guided by continuous fractional relaxation upper bounds dominates blind queue/stack exploration.

---

## Demonstration Scenarios

The engine includes four mandatory operational stress scenarios:

* **Scenario 1 (Normal Sprint Operation):** 50 issues, 10 developers (40h capacity each), 120h budget. Kuhn matching achieves 10/10 developer utilization (100% developer utilization, 20% backlog coverage). 0/1 Knapsack DP selects 16 issues yielding 1,244 business points (Fractional bound: 1,244.69).
* **Scenario 2 (Emergency Capacity Shock):** Zero-day CVE disclosure; 50% developers on emergency leave (capacity slashed to 80h). LC Branch and Bound prunes 20 state-space nodes, matching the exact DP optimum of 730 points. Dijkstra routes around locked modules with path cost 29.0.
* **Scenario 3 (Adversarial Stress and Attack):** Stress-tests algorithmic edge cases against 5,000 pre-sorted elements and a 50,001-character pathological log, proving resilience against algorithmic complexity attacks.
* **Scenario 4 (Synthetic Enterprise Backlog & Streaming):** Simulates an 80-hour dynamic event stream over 120 synthetic enterprise defects across 16 developers. Achieves an empirical Competitive Ratio of 1.0000 against the offline optimal schedule while executing 7 immediate task preemptions for critical zero-day bugs.

---

## Defensive Engineering & Reliability Invariants

1. **Skill Subset Invariant:** An issue u can only be assigned to maintainer v if required skills form a strict subset of maintainer competencies: S_u subset of K_v. Loose non-empty intersection is rejected.
2. **Prerequisite DAG Invariant:** Dependency graphs must be acyclic. A 3-color DFS traversal (White, Gray, Black) detects and traps back-edges, reporting cycle paths before task execution.
3. **Model Separation:** Strict distinction between Model A (1-to-1 bipartite assignment) and Model B (multi-task capacity packing). Bipartite matching is never misrepresented as a multi-item bin-packer.
4. **Memory Safety & Resource Management:** Enforces RAII (Resource Acquisition Is Initialization). Zero raw owning pointers, zero memory leaks, and deterministic resource deallocation.

---

## Automated Test Framework

AutoTriage includes 27 automated test suites across 6 standalone test binaries:

* `Phase_I/test_runner`: 7 suites covering Merge Sort stability, Quick Sort defense, Kuhn matching optimality, Binary Search, boundary handling, and cycle detection (7/7 Passed).
* `Phase_II/test_chunk2_dnc`: 4 suites covering Strassen, Kadane, Fast Power, and Celebrity problem (4/4 Passed).
* `Phase_II/test_chunk3_greedy`: 6 suites covering Fractional Knapsack, Activity Selection, Interval Partitioning, Huffman, Dijkstra, and Kruskal/Prim MST (6/6 Passed).
* `Phase_II/test_chunk4_dp`: 7 suites covering 0/1 Knapsack 2D/1D, MCM, LCS, OBST, Bellman-Ford, Floyd-Warshall, and Held-Karp TSP (7/7 Passed).
* `Phase_II/test_chunk5_backtracking_bb`: 5 suites covering N-Queens, Sum of Subsets, Knapsack Backtracking, Knapsack B&B, and TSP B&B (5/5 Passed).
* `Phase_II/test_chunk6_flow_strings_crt`: 5 suites covering Edmonds-Karp Flow, Bipartite Flow, Chinese Remainder Theorem, 4-Way String Matchers, and Complexity Reductions (5/5 Passed).

Total Test Status: **27 / 27 Suites Passing (100% Success Rate)**.

---

## Quickstart & Build Instructions

### Prerequisites
* C++ Compiler supporting ISO C++17 (GCC 7+, Clang 5+, or MSVC 2017+)
* CMake 3.10+ or GNU Make

### Building with CMake
```bash
# Clone the repository
git clone https://github.com/ritigyam2/DevTriage-Optimizer.git
cd DevTriage-Optimizer/AutoTriage-DAA

# Configure and build
mkdir build && cd build
cmake ..
cmake --build .

# Run automated test suites
ctest --output-on-failure
```

### Building with GNU Make
```bash
cd AutoTriage-DAA

# Compile all modules and test harnesses
make all

# Execute all test suites
make test

# Clean build artifacts
make clean
```

### Running the Interactive Decision Engine
```bash
# Launch interactive workbench CLI
./Phase_II/main

# Run mandated demonstration scenarios
./Phase_II/scenario_benchmarks
```

---

## Repository Layout

```text
DevTriage-Optimizer/
|-- README.md                                  <-- Master MNC-ready documentation
|-- LICENSE                                    <-- MIT License
|-- AutoTriage-DAA/                            <-- Official standalone submission package
|   |-- README.md                              <-- Submission navigation guide
|   |-- CMakeLists.txt                         <-- Root C++17 CMake configuration
|   |-- Makefile                               <-- Root GNU Makefile
|   |-- Phase_I/                               <-- Baseline production triage engine
|   |   |-- include/                           <-- Header-only core models, parser, sorting, matching
|   |   |-- src/main.cpp                       <-- Phase I CLI
|   |   |-- tests/test_runner.cpp              <-- Phase I automated test suite
|   |   `-- data/                              <-- Normal, boundary, invalid, and cyclic CSV datasets
|   |-- Phase_II/                              <-- Extended algorithmic workbench
|   |   |-- include/
|   |   |   |-- core/                          <-- Models, parser, sorting, visualizer, reductions
|   |   |   `-- algorithms/                    <-- D&C, Greedy, DP, B&B, Flow, Strings, CRT, Online
|   |   |-- src/main.cpp                       <-- Phase II 11-module workbench CLI
|   |   |-- src/scenario_benchmarks.cpp        <-- 4 Mandated demonstration scenarios runner
|   |   |-- tests/                             <-- Automated unit test suites (Chunks 2 through 6)
|   |   `-- data/                              <-- Synthetic enterprise defect and developer CSVs
|   |-- docs/                                  <-- Complete academic dossier
|   |   |-- AutoTriage_DAA_Final_Project_Report.pdf <-- Authoritative 25-page report
|   |   |-- AutoTriage_DAA_Final_Presentation.pptx  <-- 12-slide product presentation
|   |   |-- Declaration.pdf                    <-- Signed academic originality declaration
|   |   `-- viva_defense_toolkit.md            <-- Examiner Q&A, paper traces & live coding templates
|   `-- screenshots/                           <-- 14 High-resolution terminal evidence captures
```

---

## Author & Academic Information

* **Developer:** Ritigya Mishra
* **SAP ID:** 590028115
* **Program:** B.Tech — Computer Science & Engineering (B.Tech-CSE)
* **Specialization:** Artificial Intelligence & Machine Learning (AI/ML), Batch B-9
* **Institution:** Department of Computer Science & Engineering
* **Course:** Design and Analysis of Algorithms (DAA — PBL)
* **Project Reference:** Project 50: Open Source Issue Triage and Developer Assignment Tool
