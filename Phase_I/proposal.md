# Phase I Project Proposal: Open Source Issue Triage and Developer Assignment Tool
**Author:** Ritigya Mishra | **Course:** Design and Analysis of Algorithms (DAA - PBL)  
**Project ID:** Project 50  
**Implementation Standard:** C++17 (100% Student-Authored Offline Implementation)  
**Evaluation:** Phase I (25 / 25 Marks)  

---

## 1. Product Title & Executive Overview
**Product Title:** `AutoTriage-DAA`: Offline Repository Issue Triage and Capacity-Constrained Developer Assignment System.  
**Core Objective:** An offline decision system that ingests open-source repository issue backlogs, computes multi-criteria priority scores, filters and categorizes tasks, and executes an optimal, capacity-constrained two-sided assignment of issues to qualified developers.

---

## 2. Target Users & Real-World Problem Need
* **Target Users:** Open-source project maintainers, release managers, and triage teams.
* **Real-World Problem Need:** Major open-source repositories suffer from severe backlog bloat. Manual triage is slow, prone to human error, and frequently assigns high-severity issues to developers lacking specific domain expertise or available sprint hours.
* **Engineering Solution:** An automated, offline algorithmic engine replacing ad-hoc assignment with provably optimal Maximum Bipartite Matching and multi-key stable sorting.

---

## 3. Formal Input and Output Specifications

### 3.1 Input Specification
The system consumes two clean offline CSV data streams:
1. **Issues Stream (`issues.csv`):**
   * `id`: Positive unique integer.
   * `title`: String describing the issue.
   * `severity`: Integer from 1 (trivial) to 5 (critical blocker).
   * `estimated_hours`: Positive integer representing required effort $w_i$.
   * `business_value`: Positive real number representing priority value $v_i$.
   * `deadline_day`: Integer SLA deadline.
   * `required_skills`: Semicolon-separated skill tags (e.g., `C++;Kernel;Networking`).
   * `prerequisites`: Semicolon-separated prerequisite issue IDs.
2. **Developers Stream (`developers.csv`):**
   * `id`: Positive unique integer.
   * `name`: String developer identifier.
   * `available_hours`: Integer capacity bound $C_j$.
   * `skills`: Semicolon-separated verified skills $K_j$.

### 3.2 Output Specification
1. **Prioritized Backlog Table:** Issues sorted stably by Multi-Key criteria (Severity $\downarrow$, Deadline $\uparrow$, ID $\uparrow$).
2. **Assignment Schedule:** Mapping $\mathcal{A}: \mathcal{I} \to \mathcal{D}$ displaying developer allocations, remaining capacities, and SLA status.
3. **Comparative Analysis Report:** Side-by-side metrics comparing:
   * Merge Sort vs Quick Sort (Wall-clock time $\mu s$, comparison counts, swap counts).
   * Maximum Bipartite Matching vs Greedy Skill Matching (Assignment percentage, developer utilization balance, execution time).

---

## 4. System Constraints
1. **Strict Offline Execution:** Operates 100% locally with zero network or cloud dependencies.
2. **Skill Feasibility Constraint:** An issue $i$ can be assigned to developer $d_j$ if and only if $\mathcal{S}_i \subseteq \mathcal{K}_j$.
3. **Capacity Feasibility Constraint:** For every developer $d_j$, the sum of estimated hours of assigned issues cannot exceed capacity: $\sum_{i \in \mathcal{A}_j} w_i \le C_j$.
4. **Precedence Constraint:** Dependent issues cannot be scheduled prior to completion of prerequisite issues.
5. **No Core Algorithm Libraries:** All sorting, searching, graph traversal, and matching routines are authored from scratch without `std::sort`, `std::binary_search`, or external graph libraries.

---

## 5. Primary and Alternative Algorithms

| Operational Role | Primary Algorithm | Alternative / Comparison Algorithm | Selection Rationale |
| :--- | :--- | :--- | :--- |
| **Workload & Backlog Sorting** | **Merge Sort** ($\Theta(n \log n)$ stable) | **Quick Sort** with Median-of-Three & Randomized Pivot | Merge Sort preserves relative arrival order for identical priorities; Quick Sort provides in-place speed comparisons and worst-case stress analysis. |
| **Developer-Issue Assignment** | **Maximum Bipartite Matching** (via Augmenting Paths / Kuhn's Algorithm) | **Greedy Skill-First Matching** (Heuristic) | Bipartite Matching guarantees maximum cardinality assignment; Greedy matching illustrates how locally optimal picks cause early bottlenecking. |
| **Fast Workload Retrieval** | **Iterative Binary Search** ($\Theta(\log n)$, $O(1)$ space) | **Recursive Binary Search** ($\Theta(\log n)$, $O(\log n)$ stack) | Evaluates memory footprint and recursion stack overhead. |

---

## 6. Success Criteria & Measurable Indicators
1. **Assignment Optimality:** Maximum Bipartite Matching achieves $\ge 95\%$ assignment rate on balanced backlogs (compared to $\le 75\%$ for Greedy matching).
2. **Computational Efficiency:** Sub-millisecond execution ($< 5\text{ ms}$) on standard sprint backlogs ($N=100$ issues, $M=20$ developers).
3. **Defensive Robustness:** 100% graceful rejection of invalid inputs (negative hours, circular prerequisites, out-of-range severities) with zero segmentation faults.
4. **Offline Reproducibility:** Single-command compilation and test execution via Makefile.

---

## 7. Declaration of Originality and Compliance
I hereby declare that this project proposal complies strictly with the non-negotiable offline policy. All core algorithms have been and will be developed independently from first principles. I am fully prepared to defend, trace, and modify any portion of this code live during evaluation.

**Student Name:** Ritigya Mishra &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Roll Number:** ________________________  
**Date:** 21 November 2026 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Faculty Signature:** ________________________
