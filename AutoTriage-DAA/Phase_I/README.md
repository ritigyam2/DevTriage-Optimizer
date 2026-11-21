# AutoTriage-DAA: Phase I Project Package (Project 50)
**Course:** Design and Analysis of Algorithms (DAA - PBL)  
**Author:** Ritigya Mishra | **SAP ID:** 590028115 | **Batch:** B-9 (AI/ML) | **Course:** B.Tech-CSE  
**Implementation Standard:** C++17 (Strict ISO C++17 Offline Implementation)  

---

## 1. Executive Summary & Phase I Scope
`AutoTriage-DAA` is an offline decision-support tool that ingests open-source repository issue backlogs, categorizes tasks by severity, deadline SLA, and dependencies, and computes an optimal, capacity-constrained assignment of issues to qualified developers.

In Phase I, the primary focus is on establishing the foundational data models, defensive input parsers, baseline sorting engine (**Merge Sort** vs. **Quick Sort** with pivot attack defenses), search engine (**Iterative vs. Recursive Binary Search**), and primary developer assignment engine (**Maximum Bipartite Matching** via augmenting paths vs. **Greedy Skill Matching**).

---

## 2. Directory Structure of Phase I
```
Phase_I/
├── CMakeLists.txt              # Standard CMake build script (CMAKE_CXX_STANDARD 17)
├── Makefile                    # Offline GNU Makefile (-std=c++17)
├── README.md                   # This comprehensive evaluation guide
├── proposal.md                 # Official 1-Page Approved Proposal
├── include/
│   ├── models.hpp              # Domain structs: Issue, Developer, SortStats, MatchingStats
│   ├── parser.hpp              # Defensive CSV parser with 3-color DFS cycle detection
│   ├── sorting.hpp             # Student Merge Sort, Quick Sort (Median-3/Random/First), Binary Search
│   └── matching.hpp            # Student Maximum Bipartite Matching (Kuhn's DFS) & Greedy Matching
├── src/
│   └── main.cpp                # Interactive terminal CLI console with ANSI tables
├── data/
│   ├── normal_issues.csv       # Standard sprint backlog (20 realistic issues)
│   ├── normal_developers.csv   # Standard developer roster (8 developers, varied skills & capacities)
│   ├── boundary_issues.csv     # Boundary cases (single issue, exact capacity, zero-value tasks)
│   ├── invalid_issues.csv      # Invalid test inputs (severities > 5, negative hours, zero IDs)
│   └── cyclic_issues.csv       # Circular dependency test case (#1 <-> #2)
└── tests/
    └── test_runner.cpp         # Automated test harness verifying 7 test suites
```

---

## 3. Quick Start: Offline Compilation & Execution

### Option A: Using GNU Make
```powershell
cd Phase_I
make
./test_runner.exe
./main.exe
```

### Option B: Direct GCC Compilation (MinGW)
```powershell
cd Phase_I

# Compile interactive console
g++ -std=c++17 -O3 -Wall -Wextra -Iinclude src/main.cpp -o main.exe

# Compile automated test suite
g++ -std=c++17 -O3 -Wall -Wextra -Iinclude tests/test_runner.cpp -o test_runner.exe

# Run test suite
./test_runner.exe

# Launch interactive CLI
./main.exe
```

---

## 4. Algorithmic Implementations & Complexity Proofs

### 4.1 Multi-Key Priority Comparator
Sorts issues by three hierarchical keys:
1. **Primary Key:** `severity` descending (Critical 5 down to Trivial 1).
2. **Secondary Key:** `deadline_day` ascending (earlier SLA deadlines first).
3. **Tertiary Key:** `id` ascending (stable deterministic tie-breaking).

### 4.2 Merge Sort (Student-Authored)
* **Time Complexity:** $\Theta(n \log n)$ across Best, Average, and Worst cases.
* **Auxiliary Space:** $\Theta(n)$ for temporary subarray buffers.
* **Recurrence Relation:** $T(n) = 2T(n/2) + \Theta(n)$.
  * Solved via Master Theorem (Case 2): $a=2, b=2 \implies n^{\log_2 2} = n^1 = f(n) \implies \Theta(n \log n)$.
* **Stability:** Guaranteed stable. Equal keys retain their relative arrival order.

### 4.3 Quick Sort with Median-of-Three & Random Pivot
* **Time Complexity:** Average $\Theta(n \log n)$; Worst-Case $O(n^2)$ if degenerate.
* **Auxiliary Space:** $O(\log n)$ recursion stack.
* **Pivot Attack Defense:** Implements **Median-of-Three** (inspects `low`, `mid`, `high`) and **Randomized** pivot selection, mitigating common poor-pivot degradation on pre-sorted or reverse-sorted backlogs (noting that theoretical worst-case remains $O(n^2)$).

### 4.4 Maximum Bipartite Matching (Kuhn's Algorithm)
* **Mechanism:** Constructs a bipartite graph where edges exist iff $\mathcal{S}_i \subseteq \mathcal{K}_j$ and developer available hours $\ge$ issue effort.
* **Time Complexity:** $O(V \cdot E)$ where $V = N + M$ and $E \le N \cdot M$.
* **Optimality:** Guaranteed maximum cardinality assignment via Berge's Lemma (augmenting paths). Outperforms Greedy Skill Matching on constrained developer skillsets.

---

## 5. Automated Test Suite Results
Run `./test_runner.exe` to verify all 7 test suites pass with 100% success rate:
```text
=================================================================
  RUNNING PHASE I AUTOMATED TEST HARNESS (AutoTriage-DAA)
=================================================================

[TEST 1] Running Merge Sort Correctness & Stability Test... PASSED!
[TEST 2] Running Quick Sort Adversarial (Pre-sorted) Test... PASSED! (Median-of-3 Comparisons: 286 vs First-Pivot: 1225)
[TEST 3] Running Maximum Bipartite Matching vs Greedy Test... PASSED! (Bipartite Matched: 3 | Greedy Matched: 3)
[TEST 4] Running Binary Search (Iterative & Recursive) Test... PASSED!
[TEST 5] Running Defensive Input Validation Rejection Test... PASSED! (Correctly rejected with: "Line 2: Severity must be in range [1, 5]. Found: 9")
[TEST 6] Running Boundary Dataset Handling Test... PASSED!
[TEST 7] Running Circular Prerequisite Cycle Detection Test... PASSED! (Correctly rejected with: "Dependency cycle detected involving issue ID 1 -> 2 -> 1")

=================================================================
  ALL 7 TEST SUITES PASSED SUCCESSFULLY! (100% SUCCESS RATE)
=================================================================
```

---

## 6. Live Evaluation & Demonstration Script for Faculty

When presenting to the faculty evaluator:
1. **Show Directory Structure:** Demonstrate clean separation into `include/`, `src/`, `data/`, `tests/`.
2. **Execute Automated Tests:** Run `./test_runner.exe` to demonstrate 100% automated pass rate across all 7 test suites.
3. **Launch Interactive Console:** Run `./main.exe` and select:
   * **Option 1:** Display issues backlog and developer capacity tables.
   * **Option 2:** Demonstrate sorting benchmark: show Merge Sort stability vs. Quick Sort operation counts.
   * **Option 3:** Demonstrate assignment benchmark: show Maximum Bipartite Matching achieving optimal assignment over Greedy matching.
   * **Option 4:** Demonstrate Binary Search lookup (iterative $O(1)$ space vs recursive $O(\log n)$ stack).
   * **Option 5:** Load `data/invalid_issues.csv` and `data/cyclic_issues.csv` to prove defensive validation rejects malformed inputs and dependency cycles without crashes.
   * **Option 6:** Review live loop invariants and augmenting path theorems.

---

## 7. Compliance Statement
This submission strictly adheres to the offline policy and the ISO C++17 build requirement. All core logic has been independently implemented from first principles without third-party algorithmic libraries. Phase I is officially verified, timestamped, and ready for evaluation.
