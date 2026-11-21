# Academic Technical Report: AutoTriage-DAA (Project 50)
## Open Source Issue Triage and Developer Assignment Tool

**Course:** Design and Analysis of Algorithms (DAA — PBL)  
**Author:** Ritigya Mishra  
**SAP ID:** 590028115  
**Course & Batch:** B.Tech - Computer Science & Engineering (B.Tech-CSE) | Batch: B-9 (AI/ML)  
**Implementation Standard:** ISO C++17 (100% First-Principles Offline Implementation)  
**Academic Year:** 2026–2027 | **Evaluation Date:** 21 November 2026 (Final Submission)  

---

## 1. Executive Summary & Problem Formulation

### 1.1 Problem Context
Modern open-source software (OSS) ecosystems and enterprise repositories face severe triage and maintainer bottlenecks. Hundreds of defect reports, feature requests, and security tickets arrive continuously. Manual triage is slow, prone to human bias, and frequently results in:
1. Sub-optimal task allocations that fail to align required issue skills with developer proficiencies.
2. Maintainer burnout caused by unbalanced task overloading without respect to sprint capacity limits.
3. Starvation of lower-severity tasks due to ad-hoc priority handling.
4. Security regressions when emergency zero-day CVEs cannot preempt existing developer queues.

`AutoTriage-DAA` is an offline decision-support system that models and solves this multi-criteria challenge using foundational algorithmic techniques from the Design and Analysis of Algorithms curriculum.

### 1.2 Mathematical Formulation
The triage and scheduling domain is modeled formally as follows:

1. **Issue Backlog ($\mathcal{I}$):**  
   $$\mathcal{I} = \{i_1, i_2, \dots, i_n\}$$
   Each issue $i_u$ is characterized by a tuple:
   $$i_u = \langle \text{id}_u, \text{title}_u, \text{sev}_u, w_u, v_u, \text{dl}_u, \mathcal{S}_u, \mathcal{P}_u \rangle$$
   where:
   - $\text{sev}_u \in [1, 5]$: Priority severity (1: Trivial, 5: Blocker).
   - $w_u \in \mathbb{Z}^+$: Estimated effort in developer hours.
   - $v_u \in \mathbb{R}^+$: Business value / priority points.
   - $\text{dl}_u \in \mathbb{Z}^+$: SLA completion deadline in days.
   - $\mathcal{S}_u = \{s_1, \dots, s_k\}$: Set of required technical skill tags.
   - $\mathcal{P}_u \subseteq \{1, \dots, n\} \setminus \{u\}$: Set of prerequisite issue IDs.

2. **Developer Pool ($\mathcal{D}$):**  
   $$\mathcal{D} = \{d_1, d_2, \dots, d_m\}$$
   Each developer $d_v$ is characterized by:
   $$d_v = \langle \text{id}_v, \text{name}_v, C_v, \mathcal{K}_v \rangle$$
   where $C_v \in \mathbb{Z}^+$ is the available hour capacity for the sprint, and $\mathcal{K}_v$ is their verified skillset.

3. **Skill Compatibility Criterion:**  
   An issue $i_u$ can be assigned to developer $d_v$ if and only if the developer possesses all required skills:
   $$\mathcal{S}_u \subseteq \mathcal{K}_v$$

4. **Two Distinct Assignment Formulations:**
   - **Model A (One-to-One Maximum Bipartite Matching):** Meets the standard syllabus bipartite assignment specification. Constructs a bipartite graph $G = (U, V, E)$ where an edge $(u, v) \in E \iff \mathcal{S}_u \subseteq \mathcal{K}_v$ and $w_u \le C_v$. Each developer is matched to at most one issue, maximizing assignment cardinality via augmenting paths in $O(V \cdot E)$ time.
   - **Model B (Multi-Task Workload Capacity Allocation):** Handles production capacity packing. Solved via a greedy heuristic or discrete 0/1 Knapsack dynamic programming, where developers accumulate multiple tasks until their individual hour capacity $C_v$ (e.g., 40h) is exhausted.

---

## 2. Two-Tier System Architecture

To ensure industrial relevance while fulfilling all 46 lecture topics from Units I through VI of the common DAA syllabus, `AutoTriage-DAA` is partitioned into two functional tiers:

```
+-----------------------------------------------------------------------------+
|                               AutoTriage-DAA                                |
+-----------------------------------------------------------------------------+
                                       |
       +-------------------------------+-------------------------------+
       |                                                               |
       v                                                               v
+-------------------------------------+ +-------------------------------------+
|  Tier 1: Production Triage Engine   | |  Tier 2: Pedagogical DAA Workbench  |
+-------------------------------------+ +-------------------------------------+
| - Defensive CSV Tokenizer & 3-Color | | - Unit II: Strassen Matrix Mult     |
|   DFS Prerequisite Cycle Detection  | |   (O(n^2.807)), Kadane, Fast Power  |
| - Multi-Key Stable Merge Sort       | | - Unit IV: Matrix Chain Mult (MCM), |
| - Median-of-3 Defended Quick Sort   | |   LCS Similarity, OBST Tag Tree,    |
| - Kuhn DFS & Flow Bipartite Match   | |   Floyd-Warshall, Bellman-Ford,     |
| - 1D/2D 0/1 Knapsack Release DP     | |   Held-Karp Bitmask TSP DP          |
| - LC Branch & Bound Release Pruning | | - Unit V: N-Queens Backtracking,    |
| - Dijkstra Refactoring Shortest Path| |   Sum of Subsets, Reduced Cost TSP  |
| - 4-Way String Matchers (KMP, RK)   | | - Unit VI: Chinese Remainder Thm,   |
| - Online Preemptive Event Streaming | |   Polynomial Reductions (NP Proofs) |
+-------------------------------------+ +-------------------------------------+
```

---

## 3. Complete 46-Lecture Syllabus Integration Matrix

| Unit | Syllabus Topics & Concepts | Implemented Algorithm | Source File Reference | Formal Complexity | Domain Application in Project 50 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Unit I** | L1–L3: Asymptotic Analysis | Recurrences, Master Theorem, Invariants | `core/models.hpp` | $O, \Omega, \Theta, o, \omega$ | Formal derivations for all recursive modules |
| **Unit I** | L4–L6: Divide & Conquer, Merge Sort | Multi-Key Stable Merge Sort | `core/sorting.hpp` | $\Theta(n \log n)$ time, $O(n)$ space | Backlog ordering by Severity $\downarrow$, Deadline $\uparrow$, ID $\uparrow$ |
| **Unit I** | L7–L8: Quick Sort & Partitioning | Quick Sort (Median-of-3, Random, First) | `core/sorting.hpp` | Avg $\Theta(n \log n)$, Worst $O(n^2)$ | In-place backlog sorting with pivot defense |
| **Unit I** | L9–L10: Strassen's Matrix Mult | Strassen 7-Multiplication D&C | `algorithms/divide_and_conquer/strassen.hpp` | $\Theta(n^{\log_2 7}) \approx O(n^{2.807})$ | Developer co-maintenance intensity matrix ($M = C \cdot C^T$) |
| **Unit I** | L11: Maximum Subarray Problem | Kadane's Algorithm vs D&C Subarray | `algorithms/divide_and_conquer/max_subarray.hpp` | Kadane $\Theta(n)$, D&C $\Theta(n \log n)$ | Sprint burnout / peak bug churn window detection |
| **Unit I** | L12: Fast Power & Celebrity | Exponentiation by Squaring & Elimination | `algorithms/divide_and_conquer/fast_power.hpp`, `celebrity.hpp` | Power $\Theta(\log k)$, Celebrity $\Theta(n)$ | Markov transition chains & bottleneck maintainer detection |
| **Unit II** | L13–L14: Greedy Method & Knapsack | Fractional Knapsack (Value-Density) | `algorithms/greedy/fractional_knapsack.hpp` | $O(n \log n)$ time, $O(1)$ space | Emergency triage under divisible QA testing hours |
| **Unit II** | L15–L16: Activity Selection | Earliest Deadline First & Interval Partition | `algorithms/greedy/activity_selection.hpp`, `interval_partitioning.hpp` | $O(n \log n)$ time, Min-Heap | Single-reviewer scheduling & min CI server provisioning |
| **Unit II** | L17–L18: Huffman Codes | Greedy Prefix-Free Code Tree | `algorithms/greedy/huffman.hpp` | $O(n \log \Sigma)$ time | Lossless telemetry & crash stack trace compression |
| **Unit II** | L19–L20: Shortest Paths | Dijkstra's Algorithm with Min-Heap | `algorithms/greedy/dijkstra.hpp` | $O((V + E) \log V)$ | Minimum refactoring risk route through module DAG |
| **Unit II** | L21–L22: Minimum Spanning Trees | Kruskal's (DSU) & Prim's (Min-Heap) | `algorithms/greedy/mst.hpp` | Kruskal $O(E \log E)$, Prim $O((V+E)\log V)$ | Architectural refactoring backbone dependency tree |
| **Unit III** | L23–L24: Dynamic Programming Knapsack| 0/1 Knapsack 2D DP & 1D Space-Optimized | `algorithms/dynamic_programming/knapsack_01.hpp` | $\Theta(n \cdot W)$ time, $O(W)$ 1D space | Optimal discrete sprint release selection |
| **Unit III** | L25–L26: Matrix Chain Mult | Optimal Parenthesization DP | `algorithms/dynamic_programming/matrix_chain.hpp` | $\Theta(n^3)$ time, $\Theta(n^2)$ space | Optimizes relational database join sequences |
| **Unit III** | L27–L28: Longest Common Subseq | LCS DP with Subsequence Backtracking | `algorithms/dynamic_programming/lcs.hpp` | $\Theta(m \cdot n)$ time, $\Theta(m \cdot n)$ space | Duplicate bug report clustering & stack trace similarity |
| **Unit III** | L29–L30: Optimal BST | Dynamic Programming OBST | `algorithms/dynamic_programming/obst.hpp` | $\Theta(n^3)$ time, $\Theta(n^2)$ space | Minimizes expected lookup cost for non-uniform triage tags |
| **Unit III** | L31–L32: Bellman-Ford & Floyd | Single-Source & All-Pairs Shortest Paths | `algorithms/dynamic_programming/bellman_ford.hpp`, `floyd_warshall.hpp` | Bellman $\Theta(VE)$, Floyd $\Theta(V^3)$ | Technical-debt cycles & repository blast-radius engine |
| **Unit III** | L33: Traveling Salesperson | Held-Karp Bitmask DP | `algorithms/dynamic_programming/tsp_held_karp.hpp` | $\Theta(n^2 2^n)$ time, $\Theta(n 2^n)$ space | Optimal inspection tour for lead code auditor |
| **Unit IV** | L34–L35: Backtracking & N-Queens | N-Queens Constraint Satisfaction | `algorithms/backtracking_bb/n_queens.hpp` | $O(N!)$ worst case | Conflict-free reviewer placement benchmark |
| **Unit IV** | L36–L37: Sum of Subsets & Knapsack | Feasibility & Fractional Bound DFS Pruning | `algorithms/backtracking_bb/sum_of_subsets.hpp`, `knapsack_backtracking.hpp` | $O(2^n)$ worst case, pruned | Exact combinations fitting residual sprint hours |
| **Unit IV** | L38–L40: Branch & Bound | FIFO, LIFO, and Least-Cost (LC) B&B | `algorithms/backtracking_bb/knapsack_branch_and_bound.hpp`, `tsp_branch_and_bound.hpp` | Worst $O(2^n)$, LC best-first | Comparative state-space tree pruning analysis |
| **Unit V** | L41–L42: Maximum Flow & Matching | Edmonds-Karp Flow & Bipartite Reduction | `algorithms/flow_matching/ford_fulkerson.hpp`, `bipartite_matching.hpp` | Flow $O(V E^2)$, Matching $O(V \cdot E)$ | Syllabus developer assignment & repository throughput |
| **Unit V** | L43: Number Theory & Modular Arith | Chinese Remainder Theorem (CRT) | `algorithms/number_theory/crt.hpp` | $O(k \log M)$ time | Distributed commit audit trail synchronization |
| **Unit VI** | L44–L45: String Matching Automata | Naive, Rabin-Karp, DFA, KMP | `algorithms/string_matching/string_matchers.hpp` | KMP $\Theta(n+m)$, RK Avg $\Theta(n+m)$ | CVE signature matching & error log pattern search |
| **Unit VI** | L46: Complexity Theory & Reductions | Polynomial Reduction ($\text{Subset-Sum} \le_P \text{Knapsack}$) | `core/complexity_reductions.hpp` | Reduction $O(n)$, Verifier $O(2^n + nW)$ | Theoretical proof mapping and equivalence validation |

---

## 4. Key Algorithmic Mechanics & Theoretical Proofs

### 4.1 Multi-Key Merge Sort (Stability Invariant)
The issue backlog is sorted hierarchically:
$$\text{Key}(i_u) = \langle \text{sev}_u \downarrow, \text{dl}_u \uparrow, \text{id}_u \uparrow \rangle$$
- **Recurrence:** $T(n) = 2T(n/2) + \Theta(n)$
- **Master Theorem:** With $a=2, b=2, f(n)=\Theta(n)$, we have $n^{\log_2 2} = n^1 = \Theta(f(n))$, corresponding to Case 2. Thus, $T(n) = \Theta(n \log n)$.
- **Stability Guarantee:** During the merge phase, when $\text{Key}(L[i]) = \text{Key}(R[j])$, the element from the left subarray is selected first ($L[i]$). This guarantees that equal keys preserve their initial arrival order, satisfying the strict requirements of SLA scheduling.

### 4.2 Quick Sort Adversarial Defense (Median-of-Three)
Lomuto or Hoare partitioning selecting the first element yields $T(n) = T(n-1) + \Theta(n) = \Theta(n^2)$ on sorted or reverse-sorted backlogs.
Our implementation inspects:
$$\text{pivot} = \text{median}(\text{arr}[\text{low}], \text{arr}[\text{mid}], \text{arr}[\text{high}])$$
For sorted arrays, this selects the exact median, guaranteeing a balanced 50:50 partition:
$$T(n) = 2T(n/2) + \Theta(n) = \Theta(n \log n)$$
*Academic Boundary:* While Median-of-Three eliminates quadratic degradation on common ordered inputs, the theoretical worst-case remains $O(n^2)$ for adversarial permutations engineered against the median-of-three rule.

### 4.3 Maximum Bipartite Matching via Augmenting Paths
- **Graph Construction:** Bipartite graph $G = (U, V, E)$ where $U$ is the set of issues, $V$ is the set of developers, and $(u, v) \in E \iff \mathcal{S}_u \subseteq \mathcal{K}_v$.
- **Kuhn's Algorithm:** Operates by iteratively finding $M$-augmenting paths using DFS.
- **Berge's Lemma:** A matching $M$ is maximum if and only if $G$ contains no $M$-augmenting paths.
- **Time Complexity:** At most $|U|$ searches, each visiting at most $|E|$ edges: $O(|U| \cdot |E|) = O(V \cdot E)$.

### 4.4 0/1 Knapsack Dynamic Programming vs Least-Cost Branch & Bound
To construct the optimal sprint package within hour budget $W$:
- **Dynamic Programming (2D Table):**  
  $$K[i, w] = \begin{cases} 0 & \text{if } i=0 \text{ or } w=0 \\ K[i-1, w] & \text{if } w_i > w \\ \max(v_i + K[i-1, w - w_i], K[i-1, w]) & \text{if } w_i \le w \end{cases}$$
  Time: $\Theta(n \cdot W)$, Auxiliary Space: $\Theta(n \cdot W)$.
- **Space-Optimized 1D Array:** By iterating the capacity backwards from $W$ down to $w_i$:
  $$dp[w] = \max(dp[w], v_i + dp[w - w_i])$$
  Space is compressed from $\Theta(n \cdot W)$ to $O(W)$, preventing memory allocation bottlenecks on large sprint capacities.
- **Least-Cost (LC) Branch & Bound:** Explores a state-space tree where nodes are ordered by an upper bound calculated using fractional relaxation. Branches whose upper bound is strictly less than the current best discrete solution are pruned immediately.

### 4.5 Knuth-Morris-Pratt (KMP) Prefix Automaton
When searching for error tokens or CVE signatures across massive crash logs:
- **Prefix Function ($\pi$):** Computes the length of the longest proper prefix of pattern $P[0 \dots q]$ that is also a suffix of $P[0 \dots q]$:
  $$\pi[q] = \max \{ k : k < q \text{ and } P[0 \dots k-1] \text{ is a suffix of } P[0 \dots q] \}$$
- **Zero Backtracking:** The text pointer never moves backward. Mismatches cause the pattern pointer to jump via the $\pi$ table, achieving deterministic linear scan time:
  $$\Theta(n + m)$$

### 4.6 Complexity Reduction: $\text{Subset-Sum} \le_P \text{0/1 Knapsack}$
To verify the theoretical reduction:
1. **Polynomial-Time Mapping ($O(n)$):** Given an instance of Subset-Sum $(S = \{s_1, \dots, s_n\}, K)$:
   - Construct Knapsack instance with $n$ items where $w_i = s_i$, $v_i = s_i$, and $W = K$.
   - Set target value $V = K$.
   - This construction involves $n$ assignments, taking strict $O(n)$ deterministic time.
2. **Equivalence Theorem:** A subset $S' \subseteq S$ sums to $K \iff$ a knapsack packing achieves weight $\le K$ and value $\ge K$.
   - Since $w_i = v_i$, total weight $\le K$ and total value $\ge K$ forces the selected items to satisfy $\sum w_i = K$ and $\sum v_i = K$ simultaneously.
3. **Experimental Demonstration Verifier:** To experimentally confirm this equivalence on test instances, the verification routine independently computes the ground truth for both problems:
   - Solves Subset-Sum via exhaustive subset enumeration: $O(2^n)$.
   - Solves Knapsack via Dynamic Programming: $O(n \cdot W)$.
   - Total verification time: $O(2^n + nW)$.

---

## 5. Empirical Benchmark Scenarios & Measured Evidence

The project includes four official demonstration scenarios executed via `scenario_benchmarks.exe`. All reported values represent genuine measured variables exported to `scenario_benchmark_results.csv`:

```
+---------------------------------------------------------------------------------------------------+
| AutoTriage-DAA Measured Benchmark Evidence Table                                                  |
+------------------------------+---------------------------+-------------------+-------------+------+
| Scenario Context             | Algorithm Evaluated       | Measured Metric   | Value       | Unit |
+------------------------------+---------------------------+-------------------+-------------+------+
| Scenario 1: Normal Sprint    | Max Bipartite Matching    | Matched Issues    | 10          | count|
| (50 issues, 10 devs, 120h)   | Max Bipartite Matching    | Dev Utilization   | 100         | %    |
|                              | Max Bipartite Matching    | Backlog Assigned  | 20          | %    |
|                              | 0/1 Knapsack DP           | Discrete Value    | 1244        | pts  |
|                              | Fractional Knapsack       | Continuous Bound  | 1244.69     | pts  |
+------------------------------+---------------------------+-------------------+-------------+------+
| Scenario 2: Capacity Shock   | LC Branch & Bound         | Pruned Nodes      | 20          | nodes|
| (Hours cut 200h -> 80h)      | LC Branch & Bound         | Value Achieved    | 730         | pts  |
|                              | 0/1 Knapsack DP           | Exact DP Optimum  | 730         | pts  |
|                              | Dijkstra Dependency Route | Bypass Cost       | 29.0        | cost |
+------------------------------+---------------------------+-------------------+-------------+------+
| Scenario 3: Stress & Attack  | Quick Sort (Median-of-3)  | Comparisons       | 60678       | ops  |
| (5,000 pre-sorted array;     | Merge Sort (Stable)       | Comparisons       | 51420       | ops  |
|  50,001-char crash log)      | KMP String Search         | Comparisons       | 100005      | ops  |
|                              | Naive String Search       | Comparisons       | 299976      | ops  |
+------------------------------+---------------------------+-------------------+-------------+------+
| Scenario 4: Synthetic        | Dataset Scale             | Backlog Issues    | 120         | items|
| Enterprise & Online Stream   | Dataset Scale             | Maintainers       | 16          | devs |
| (80-hour dynamic event stream| Online Streaming Engine   | Competitive Ratio | 1.0000      | ratio|
|  with zero-day preemption)   | Preemption Engine         | Preemptions Fired | 7           | count|
+------------------------------+---------------------------+-------------------+-------------+------+
```

### Key Empirical Findings:
1. **Decoupled Match Rate:** In Scenario 1, the bipartite matcher pairs 10 issues across 10 developers. This yields 100% developer utilization ($10/10$) while assigning 20% of the backlog ($10/50$). Distinguishing both metrics prevents misleading reporting.
2. **Branch & Bound Efficiency:** Under capacity shock (Scenario 2), Least-Cost B&B pruned 20 state-space nodes, finding the exact discrete optimum of 730 points matching the DP baseline.
3. **Pathological String Attack:** On the repetitive 50,001-character crash log (`AAAA...AB`), Naive search performed 299,976 comparisons, whereas KMP completed in 100,005 comparisons with zero pointer backtracks.
4. **Adversarial Quick Sort:** Median-of-Three pivot selection successfully prevented extreme quadratic collapse on pre-sorted arrays ($N=5,000$), recording 60,678 comparisons against Merge Sort's 51,420.
5. **Dynamic Preemptive Streaming:** On the 120-issue synthetic enterprise stream, the online preemption heuristic achieved an empirical competitive ratio of 1.0000 relative to offline matching while immediately preempting 7 lower-priority tasks to preserve SLA on emergency CVEs.

---

## 6. Automated Test Harness Verification

The project includes 27 comprehensive automated test suites across Phase I and Phase II. All tests compile and run offline under `-std=c++17 -O3 -Wall -Wextra`:

### Summary of Passing Test Suites:
- **Phase I Core Engine (`test_runner.exe`):** **7/7 tests passed**
  - Test 1: Merge Sort Correctness & Multi-Key Stability
  - Test 2: Quick Sort Median-of-3 Adversarial Defense
  - Test 3: Kuhn Bipartite Matching vs Greedy Skill Matching
  - Test 4: Binary Search (Iterative $O(1)$ vs Recursive $O(\log n)$)
  - Test 5: Defensive Input Validation Rejection
  - Test 6: Boundary Dataset Ingestion
  - Test 7: Circular Prerequisite Dependency Cycle Detection (3-Color DFS)
- **Phase II Chunk 2 (`test_chunk2_dnc.exe`):** **4/4 tests passed** (Strassen, Kadane, Fast Power, Celebrity)
- **Phase II Chunk 3 (`test_chunk3_greedy.exe`):** **6/6 tests passed** (Fractional Knapsack, Activity Selection, Interval Partitioning, Huffman, Dijkstra, Kruskal/Prim MST)
- **Phase II Chunk 4 (`test_chunk4_dp.exe`):** **7/7 tests passed** (0/1 Knapsack 2D/1D, MCM, LCS, OBST, Bellman-Ford, Floyd-Warshall, Held-Karp TSP)
- **Phase II Chunk 5 (`test_chunk5_backtracking_bb.exe`):** **5/5 tests passed** (N-Queens, Sum of Subsets, Knapsack Backtracking, Knapsack B&B FIFO/LIFO/LC, TSP B&B)
- **Phase II Chunk 6 (`test_chunk6_flow_strings_crt.exe`):** **5/5 tests passed** (Edmonds-Karp Max Flow, Flow Bipartite Matching, Chinese Remainder Theorem, 4-Way String Matchers, Polynomial Reduction)
- **Phase II Scenarios (`scenario_benchmarks.exe`):** **4/4 demonstration scenarios completed successfully**

---

## 7. Ethical, Social, and Safety Considerations in Automated Triage

Algorithmic task assignment in software engineering involves sociotechnical responsibilities:

1. **Workload Fairness & Burnout Prevention:**
   Pure optimization algorithms can overburden top-performing developers by consistently loading them to their 40-hour limit. AutoTriage incorporates configurable damping thresholds and decouples 1-to-1 matching from multi-task packing to ensure sustainable workloads.
2. **Mitigating Bias in Developer Profiling:**
   Static skill taxonomies can trap junior engineers in repetitive minor tasks (Severity 1-2). AutoTriage supports shadow pairing allocations and uses SLA arrival order for tie-breaking rather than seniority alone.
3. **Preventing Severity Starvation:**
   Strict multi-key prioritization of Severity 5 blockers can perpetually starve technical debt, documentation, and refactoring tasks. AutoTriage includes a dynamic aging multiplier that increments an issue's effective priority for each sprint it remains unassigned.
4. **Human-in-the-Loop Override & Decision Explainability:**
   Algorithmic allocations are advisory recommendations. AutoTriage outputs full diagnostic logs explaining why assignments were made (skill matching, available hours, and augmenting path reassignments). Engineering leads maintain full override authority.
5. **Academic & Engineering Integrity:**
   Empirical reports strictly distinguish between Developer Utilization Rate ($10/10 = 100\%$) and Issue Backlog Assigned Rate ($10/50 = 20\%$) to present transparent, uninflated metrics.

---

## 8. Build, Reproduction, and Verification Commands

### Build Automation via GNU Make:
```bash
# Phase I
cd Phase_I
make clean && make all
./test_runner.exe
./main.exe

# Phase II
cd ../Phase_II
make clean && make all
make test
./scenario_benchmarks.exe
./main.exe
```

### Direct GCC Compilation (Strict ISO C++17):
```bash
# Compile Phase I
g++ -std=c++17 -O3 -Wall -Wextra -Iinclude src/main.cpp -o main.exe
g++ -std=c++17 -O3 -Wall -Wextra -Iinclude tests/test_runner.cpp -o test_runner.exe

# Compile Phase II Workbench & Scenarios
g++ -std=c++17 -O3 -Wall -Wextra -Iinclude src/main.cpp -o main.exe
g++ -std=c++17 -O3 -Wall -Wextra -Iinclude src/scenario_benchmarks.cpp -o scenario_benchmarks.exe
```

---

## 9. Conclusion

`AutoTriage-DAA` provides a comprehensive, ground-up implementation of all 46 lectures of the Design and Analysis of Algorithms syllabus. By separating the production triage engine from the curriculum workbench, maintaining strict ISO C++17 build compliance, and grounding all empirical claims in genuine executed code, the project delivers a mathematically sound, reproducible, and defensible academic submission.
