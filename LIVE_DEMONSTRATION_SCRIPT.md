# AutoTriage: 7-Minute Final Viva & Live Demonstration Script
**Author:** Ritigya Mishra | **Course:** Design and Analysis of Algorithms (DAA - PBL)  
**Standard:** Standalone C++17 Implementation (100% Offline, Zero External Libraries)  
**Preparation:** Ensure terminal is open in `c:\Users\user\OneDrive\Desktop\DAA PROJECT` before the evaluator sits down.

---

## 0. Pre-Flight Setup (Before the Professor Sits Down)
1. Open PowerShell or Command Prompt.
2. Ensure you are in the workspace folder:
   ```powershell
   cd "c:\Users\user\OneDrive\Desktop\DAA PROJECT"
   ```
3. Have your digital or printed copies ready:
   * [`AutoTriage_DAA_Final_Project_Report.pdf`](file:///c:/Users/user/OneDrive/Desktop/DAA%20PROJECT/AutoTriage_DAA_Final_Project_Report.pdf) (25-page comprehensive project report).
   * [`AutoTriage_DAA_Final_Presentation.pptx`](file:///c:/Users/user/OneDrive/Desktop/DAA%20PROJECT/AutoTriage_DAA_Final_Presentation.pptx) (12-slide final evaluation deck).
   * [`Declaration.pdf`](file:///c:/Users/user/OneDrive/Desktop/DAA%20PROJECT/AutoTriage-DAA/docs/Declaration.pdf) (Signed declaration of originality).

---

## Minute 0:00 – 1:00 | The Elevator Pitch & Architecture
**What to Say:**
> *"Good morning, Professor. Today I am presenting **AutoTriage (Project 50)**: an enterprise-grade algorithmic workbench designed to solve maintainer burnout and triage latency in open-source software ecosystems.  
> We have implemented **28 distinct first-principles algorithms** spanning all 6 units of the DAA curriculum—completely offline in C++17 with **zero external core libraries**.  
> The system operates under a **Two-Tier Architecture**: Tier 1 solves the real-world triage bottleneck via Kuhn's Matching, 1D Knapsack DP, Dijkstra, KMP, and Online Preemptive Streaming; Tier 2 provides rigorous academic implementations for Strassen, N-Queens, Held-Karp TSP, and NP reductions."*

---

## Minute 1:00 – 2:30 | Phase I Baseline & Verification
**What to Run:**
```powershell
cd Phase_I
.\test_runner.exe
```
**What to Say & Point to on Screen:**
> *"First, here is our Phase I verification harness running under C++17. All 7 test suites pass with a **100% success rate**.  
> In Test 2, notice our adversarial Quick Sort test: on a pre-sorted array of 2,000 items, standard Lomuto first-pivot collapses to 1,225 comparisons, whereas our student-authored **Median-of-3 pivoting** completes in only 286 comparisons—mitigating sorted adversarial degradation.  
> In Test 3, our student-authored **Kuhn's DFS Augmenting Path algorithm** computes the exact maximum bipartite matching from first principles.  
> In Test 7, notice our newly integrated **Circular Prerequisite Cycle Detection**: our DFS 3-color graph traversal traps cyclic dependencies (Issue #1 $\leftrightarrow$ Issue #2) and safely rejects corrupted data."*

---

## Minute 2:30 – 4:30 | Phase II 4-Scenario Stress Benchmarks
**What to Run:**
```powershell
cd ..\Phase_II
.\scenario_benchmarks.exe
```
**What to Say & Point to on Screen:**
> *"Now moving to Phase II, we execute our **Four Demonstration Scenarios**:  
> 1. **Scenario 1 (Normal Sprint):** Demonstrates 1-to-1 bipartite flow matching achieving **10/10 developers utilized (100%)** and **10/50 backlog issues assigned (20%)**, alongside 2D DP Knapsack maximizing discrete release value under 120 sprint hours.  
> 2. **Scenario 2 (Capacity Shock):** When capacity is slashed to 80 hours during an emergency, our **Least-Cost Branch & Bound** engine matches the exact dynamic programming optimum while pruning **20 unpromising state-space branches**. Meanwhile, Dijkstra's algorithm reroutes broken module dependencies around locked code.  
> 3. **Scenario 3 (Adversarial Attacks):** On a pathological 50,001-character crash log (`AAAA...AB`), Naive string matching wastes 299,976 comparisons due to text backtracking. Our **Knuth-Morris-Pratt (KMP) failure automaton** scans the text in 100,005 operations with **zero pointer backtracks**.  
> 4. **Scenario 4 (Synthetic Enterprise Backlog & Online Streaming):** We ingest our benchmark dataset of **120 synthetic enterprise issues** across 16 specialized maintainers. Notice the console output generates an **ASCII Developer Capacity Utilization Bar** and a **10-day Gantt Schedule Matrix**!"*

---

## Minute 4:30 – 5:30 | Online Streaming & Zero-Day Preemption
**What to Point to on Screen in Scenario 4:**
> *"Furthermore, in Scenario 4, we evaluate dynamic arrivals over an **80-hour simulated arrival stream**.  
> We measure an empirical competitive ratio of **$CR = 1.0000$** against the offline optimal matching.  
> Look at the Preemption Event Audit Trail: at Hour 28, when a Critical P0 Zero-Day vulnerability arrived and all senior engineers were booked, our engine automatically paused in-flight lower-priority task #108 on developer Elena, re-queued it, and immediately dispatched the emergency CVE—guaranteeing zero SLA latency."*

---

## Minute 5:30 – 6:30 | Interactive CLI Live Demo
**What to Run:**
```powershell
.\main.exe
```
**What to Do:**
1. Type `1` (Merge Sort Triage): Show the top 10 prioritized issues sorted stably by severity, deadline, and value.
2. Type `2` (Developer Assignment): Show the bipartite flow matching and real-time developer utilization bars.
3. Type `9` (Gantt Visualizer): Show the ASCII 10-day schedule timeline.
4. Type `7` (Verification & Complexity Suite): Show Celebrity Maintainer $O(n)$, Chinese Remainder Theorem, and the formal Polynomial Reduction proof ($\text{Subset-Sum} \le_P \text{0/1 Knapsack}$).

---

## Minute 6:30 – 7:00 | Conclusion & Inviting Examiner Questions
**What to Say:**
> *"In summary, AutoTriage satisfies every requirement of the 46-lecture DAA syllabus, compiles with **zero warnings under -Wall -Wextra**, and is backed by our comprehensive final project report, presentation deck, and viva defense toolkit.  
> I am now ready for code traces, whiteboard implementations, or any live modifications you would like me to perform. Thank you, Professor."*

---

## Defense Playbook (If the Professor Interrupts)

| Professor Interrupt / Question | Immediate Action & Response |
| :--- | :--- |
| *"Show me where you implemented Quick Sort partition."* | Open [`Phase_II/include/core/sorting.hpp`](file:///c:/Users/user/OneDrive/Desktop/DAA%20PROJECT/Phase_II/include/core/sorting.hpp#L84-L115). Point to lines 84–115: explain `select_pivot_index`, `MEDIAN_OF_THREE`, and Lomuto swap loop. |
| *"Why iterate backwards in 1D Knapsack DP?"* | *"Backward iteration from $W$ down to $wt[i]$ prevents overwriting the values of iteration $i-1$, preserving single-item 0/1 choice semantics in $O(W)$ space."* |
| *"Write Kuhn's DFS matching on the whiteboard right now."* | Grab the marker and write the 10-line `dfs_kuhn` function from [`viva_defense_toolkit.md`](file:///c:/Users/user/OneDrive/Desktop/DAA%20PROJECT/Phase_II/docs/viva_defense_toolkit.md#L38-L56). |
| *"Prove that Subset-Sum reduces to 0/1 Knapsack in polynomial time."* | *"Given $(S, T)$, construct knapsack with $w_i = v_i = s_i$ and capacity $W=T$. A subset sums to $T$ iff maximum value $\ge T$. Transformation takes $O(n)$ time."* |
| *"Why did you use Strassen on small developer matrices?"* | *"In our Two-Tier architecture, Strassen is an academic reference workbench demonstrating $\Theta(n^{2.807})$ divide-and-conquer mechanics; our code incorporates a base-case threshold at $N \le 64$ to bypass recursion overhead in practice."* |
