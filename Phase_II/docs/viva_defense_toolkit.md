# Project 50: AutoTriage — Viva Defense Toolkit & Live Coding Masterbook
**Author:** Ritigya Mishra | **Course:** Design and Analysis of Algorithms (DAA)  
**Standard:** Rigorous, mathematically sound, first-principles C++17 implementation.

---

## Executive Viva Defense Strategy
When facing the evaluation panel:
1. **Lead with Mathematical Rigor:** Define problem instances using formal notation ($G=(V, E)$, state spaces, asymptotic bounds $O, \Omega, \Theta$).
2. **Emphasize First-Principles Implementation:** Clarify immediately that zero core algorithm libraries were imported; sorting, trees, heaps, flow networks, and dynamic programming tables are written directly from memory.
3. **Contrast Competing Paradigms:** For every problem, explain why a particular paradigm was selected over alternatives (e.g., Dynamic Programming vs Greedy, Branch & Bound vs Backtracking, Kuhn vs Edmonds-Karp).

---

## Part 1: Five-Minute Live Coding Blackbook
Canonical, bug-free C++ templates ready to be reproduced on a whiteboard or blank terminal in under 5 minutes.

### 1.1 Quick Sort with Median-of-3 & Lomuto Partition
```cpp
#include <vector>
#include <algorithm>

int median_of_three(std::vector<int>& arr, int low, int high) {
    int mid = low + (high - low) / 2;
    if (arr[mid] < arr[low]) std::swap(arr[low], arr[mid]);
    if (arr[high] < arr[low]) std::swap(arr[low], arr[high]);
    if (arr[high] < arr[mid]) std::swap(arr[mid], arr[high]);
    std::swap(arr[mid], arr[high]); // Place pivot at high
    return high;
}

int partition(std::vector<int>& arr, int low, int high) {
    median_of_three(arr, low, high);
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; ++j) {
        if (arr[j] <= pivot) {
            ++i;
            std::swap(arr[i], arr[j]);
        }
    }
    std::swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quick_sort(std::vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quick_sort(arr, low, pi - 1);
        quick_sort(arr, pi + 1, high);
    }
}
```

### 1.2 Kuhn's DFS Bipartite Matching
```cpp
#include <vector>

bool dfs_kuhn(int u, const std::vector<std::vector<int>>& adj, 
              std::vector<int>& match, std::vector<bool>& visited) {
    for (int v : adj[u]) {
        if (visited[v]) continue;
        visited[v] = true;
        // If v is unmatched, or we can find an augmenting path for its current match
        if (match[v] < 0 || dfs_kuhn(match[v], adj, match, visited)) {
            match[v] = u;
            return true;
        }
    }
    return false;
}

int max_bipartite_matching(int n_left, int n_right, const std::vector<std::vector<int>>& adj) {
    std::vector<int> match(n_right, -1);
    int max_matches = 0;
    for (int u = 0; u < n_left; ++u) {
        std::vector<bool> visited(n_right, false);
        if (dfs_kuhn(u, adj, match, visited)) {
            max_matches++;
        }
    }
    return max_matches;
}
```

### 1.3 0/1 Knapsack with 1D Space Optimization
```cpp
#include <vector>
#include <algorithm>

int knapsack_01_space_optimized(int W, const std::vector<int>& wt, const std::vector<int>& val) {
    int n = wt.size();
    std::vector<int> dp(W + 1, 0);
    for (int i = 0; i < n; ++i) {
        // Reverse iteration preserves values from the previous iteration i-1
        for (int w = W; w >= wt[i]; --w) {
            dp[w] = std::max(dp[w], dp[w - wt[i]] + val[i]);
        }
    }
    return dp[W];
}
```

### 1.4 Dijkstra's SSSP with Min-Heap
```cpp
#include <vector>
#include <queue>
#include <limits>

const double INF = std::numeric_limits<double>::infinity();

struct Edge { int to; double weight; };

std::vector<double> dijkstra(int n, int src, const std::vector<std::vector<Edge>>& adj) {
    std::vector<double> dist(n, INF);
    // Min-heap: pair<distance, u>
    std::priority_queue<std::pair<double, int>, 
                        std::vector<std::pair<double, int>>, 
                        std::greater<std::pair<double, int>>> pq;
    dist[src] = 0.0;
    pq.push({0.0, src});

    while (!pq.empty()) {
        double d = pq.top().first;
        int u = pq.top().second;
        pq.pop();

        if (d > dist[u]) continue; // Stale heap entry

        for (const auto& edge : adj[u]) {
            if (dist[u] + edge.weight < dist[edge.to]) {
                dist[edge.to] = dist[u] + edge.weight;
                pq.push({dist[edge.to], edge.to});
            }
        }
    }
    return dist;
}
```

### 1.5 Knuth-Morris-Pratt (KMP) String Search
```cpp
#include <vector>
#include <string>

std::vector<int> compute_pi(const std::string& pat) {
    int m = pat.size();
    std::vector<int> pi(m, 0);
    int k = 0;
    for (int q = 1; q < m; ++q) {
        while (k > 0 && pat[k] != pat[q]) k = pi[k - 1];
        if (pat[k] == pat[q]) ++k;
        pi[q] = k;
    }
    return pi;
}

std::vector<int> kmp_search(const std::string& text, const std::string& pat) {
    std::vector<int> pi = compute_pi(pat);
    std::vector<int> matches;
    int n = text.size(), m = pat.size();
    int q = 0;
    for (int i = 0; i < n; ++i) {
        while (q > 0 && pat[q] != text[i]) q = pi[q - 1];
        if (pat[q] == text[i]) ++q;
        if (q == m) {
            matches.push_back(i - m + 1);
            q = pi[q - 1]; // Reset to longest proper prefix
        }
    }
    return matches;
}
```

### 1.6 Strassen's 7 Multiplication Equations
Given $2 \times 2$ block partition:
$$A = \begin{pmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{pmatrix}, \quad B = \begin{pmatrix} B_{11} & B_{12} \\ B_{21} & B_{22} \end{pmatrix}$$
$$M_1 = (A_{11} + A_{22})(B_{11} + B_{22})$$
$$M_2 = (A_{21} + A_{22})B_{11}$$
$$M_3 = A_{11}(B_{12} - B_{22})$$
$$M_4 = A_{22}(B_{21} - B_{11})$$
$$M_5 = (A_{11} + A_{12})B_{22}$$
$$M_6 = (A_{21} - A_{11})(B_{11} + B_{12})$$
$$M_7 = (A_{12} - A_{22})(B_{21} + B_{22})$$
Reconstruction:
$$C_{11} = M_1 + M_4 - M_5 + M_7$$
$$C_{12} = M_3 + M_5$$
$$C_{21} = M_2 + M_4$$
$$C_{22} = M_1 - M_2 + M_3 + M_6$$

### 1.7 Disjoint Set Union (DSU) with Path Compression & Union by Rank
```cpp
#include <vector>

struct DSU {
    std::vector<int> parent, rank;
    DSU(int n) : parent(n), rank(n, 0) {
        for (int i = 0; i < n; ++i) parent[i] = i;
    }
    int find(int i) {
        if (parent[i] != i) parent[i] = find(parent[i]); // Path compression
        return parent[i];
    }
    bool unite(int i, int j) {
        int root_i = find(i);
        int root_j = find(j);
        if (root_i == root_j) return false;
        // Union by rank
        if (rank[root_i] < rank[root_j]) parent[root_i] = root_j;
        else if (rank[root_i] > rank[root_j]) parent[root_j] = root_i;
        else {
            parent[root_j] = root_i;
            rank[root_i]++;
        }
        return true;
    }
};
```

---

## Part 2: Step-by-Step Paper Trace Worksheets

### Worksheet 1: Merge Sort Recurrence & Tree Trace
**Input Array:** `[38, 27, 43, 3, 9, 82, 10]` ($n=7$)
```
Level 0:                         [38, 27, 43, 3, 9, 82, 10]
                               /                            \
Level 1:            [38, 27, 43, 3]                       [9, 82, 10]
                    /             \                       /         \
Level 2:       [38, 27]         [43, 3]                [9, 82]      [10]
               /      \         /     \                /     \        |
Level 3:     [38]    [27]     [43]    [3]            [9]     [82]   [10]
               \      /         \     /                \     /        |
Merge L2:      [27, 38]         [3, 43]                [9, 82]      [10]
                    \             /                       \         /
Merge L1:            [3, 27, 38, 43]                       [9, 10, 82]
                               \                            /
Merge L0:                        [3, 9, 10, 27, 38, 43, 82]
```
- **Recurrence:** $T(n) = 2T(n/2) + \Theta(n)$
- **Master Theorem Case 2:** $a=2, b=2 \implies n^{\log_2 2} = n^1 \implies T(n) = \Theta(n \log n)$.

---

### Worksheet 2: Kuhn's Augmenting Path Step-by-Step
**Graph:** Left $U = \{u_0, u_1, u_2\}$, Right $V = \{v_0, v_1, v_2\}$  
**Edges:** $(u_0, v_0), (u_0, v_1), (u_1, v_0), (u_2, v_1)$

1. **Step 1 ($u_0$):** Explores $v_0$. $v_0$ is free $\implies$ Match: `v_0 = u_0`. Matches: 1.
2. **Step 2 ($u_1$):** Explores $v_0$. $v_0$ is matched to $u_0$. DFS calls `dfs(u_0)`.
   - $u_0$ tries next edge: $v_1$. $v_1$ is free $\implies$ `v_1 = u_0`.
   - Backtrack: `v_0 = u_1`. Matches: 2.
3. **Step 3 ($u_2$):** Explores $v_1$. $v_1$ is matched to $u_0$. DFS calls `dfs(u_0)`.
   - $u_0$ has no other free edges. DFS returns false.
   - $u_2$ cannot augment.
4. **Final Matching:** `{(u_1, v_0), (u_0, v_1)}`. Size = 2.

---

### Worksheet 3: Knapsack Branch & Bound State Space Tree
**Parameters:** Capacity $W = 15$. Items:
- Item 0: $w_0=2, v_0=10$ (Density = 5.0)
- Item 1: $w_1=4, v_1=10$ (Density = 2.5)
- Item 2: $w_2=6, v_2=12$ (Density = 2.0)
- Item 3: $w_3=9, v_3=18$ (Density = 2.0)

**Upper Bound Calculation:**
At Node $(i, \text{curr\_w}, \text{curr\_v})$:
$$\text{Bound} = \text{curr\_v} + \text{FractionalKnapsackRemaining}(W - \text{curr\_w})$$

**Node Exploration Comparison:**
- **FIFO (Queue):** 15 nodes expanded. Explores suboptimal branches before pruning occurs.
- **LIFO (Stack):** 9 nodes expanded. Explores deep paths quickly, updating lower bound early.
- **Least-Cost (Priority Queue):** **8 nodes expanded**. Always branches on the highest upper bound; prunes unpromising subtrees immediately upon finding optimal solution ($v=38$).

---

### Worksheet 4: KMP Failure Function Construction ($\pi$ Table)
**Pattern:** `A B A B C A B A B` ($m=9$)
```
Index q:    0   1   2   3   4   5   6   7   8
Char P[q]:  A   B   A   B   C   A   B   A   B
pi[q]:      0   0   1   2   0   1   2   3   4
```
**Trace:**
- $q=0 (A):$ Base case, $\pi[0] = 0$.
- $q=1 (B):$ $P[1] \ne P[0] \implies \pi[1] = 0$.
- $q=2 (A):$ $P[2] == P[0] \implies k=1, \pi[2] = 1$.
- $q=3 (B):$ $P[3] == P[1] \implies k=2, \pi[3] = 2$.
- $q=4 (C):$ $P[4] \ne P[2]$, $k=\pi[1]=0$, $P[4] \ne P[0] \implies \pi[4] = 0$.
- $q=5 (A):$ $P[5] == P[0] \implies \pi[5] = 1$.
- $q=6 (B):$ $P[6] == P[1] \implies \pi[6] = 2$.
- $q=7 (A):$ $P[7] == P[2] \implies \pi[7] = 3$.
- $q=8 (B):$ $P[8] == P[3] \implies \pi[8] = 4$.

---

## Part 3: Top 25 Toughest Viva Voce Questions & Professor-Grade Answers

### Q1: What is the formal difference between $O(g(n))$, $\Omega(g(n))$, and $\Theta(g(n))$?
> **Answer:**
> - $f(n) \in O(g(n)) \iff \exists c > 0, n_0 \ge 0$ such that $0 \le f(n) \le c g(n)$ for all $n \ge n_0$ (Asymptotic Upper Bound).
> - $f(n) \in \Omega(g(n)) \iff \exists c > 0, n_0 \ge 0$ such that $0 \le c g(n) \le f(n)$ for all $n \ge n_0$ (Asymptotic Lower Bound).
> - $f(n) \in \Theta(g(n)) \iff f(n) \in O(g(n)) \land f(n) \in \Omega(g(n))$, meaning $c_1 g(n) \le f(n) \le c_2 g(n)$ for all $n \ge n_0$ (Asymptotically Tight Bound).

### Q2: Why does Quick Sort have worst-case $O(n^2)$ time while Merge Sort is strictly $\Theta(n \log n)$?
> **Answer:**
> Merge Sort guarantees a balanced $n/2, n/2$ partition at every step, yielding $T(n) = 2T(n/2) + \Theta(n) = \Theta(n \log n)$. Quick Sort's partition balance depends on the pivot. If the pivot is the extreme element (minimum or maximum), the subproblems split into sizes $0$ and $n-1$, yielding $T(n) = T(n-1) + \Theta(n) = \Theta(n^2)$.

### Q3: How does Median-of-3 prevent this $O(n^2)$ degeneration?
> **Answer:**
> By evaluating the first, middle, and last elements and choosing the median, it is mathematically impossible to select the smallest or largest element as pivot unless all three are identical. This guarantees at least one element on each side of the partition on presorted or reverse-presorted inputs.

### Q4: State the Master Theorem for divide-and-conquer recurrences. When does it fail?
> **Answer:**
> For $T(n) = a T(n/b) + f(n)$ where $a \ge 1, b > 1$:
> 1. If $f(n) = O(n^{\log_b a - \epsilon})$ for $\epsilon > 0$, then $T(n) = \Theta(n^{\log_b a})$.
> 2. If $f(n) = \Theta(n^{\log_b a} \log^k n)$ for $k \ge 0$, then $T(n) = \Theta(n^{\log_b a} \log^{k+1} n)$.
> 3. If $f(n) = \Omega(n^{\log_b a + \epsilon})$ and regularity condition holds ($a f(n/b) \le c f(n)$ for $c < 1$), then $T(n) = \Theta(f(n))$.
> **Failure condition:** It fails when $f(n)$ is asymptotically smaller or larger than $n^{\log_b a}$ by a non-polynomial factor (e.g., $T(n) = 2T(n/2) + n / \log n$), or when $b$ is not a constant (e.g., $T(n) = T(\sqrt{n})$).

### Q5: What is the optimal substructure property in Dynamic Programming?
> **Answer:**
> A problem exhibits optimal substructure if an optimal solution to the overall problem contains within it optimal solutions to its subproblems. For example, in shortest paths, if path $P = u \dots v \dots w$ is the shortest path from $u$ to $w$, then the sub-path $v \dots w$ must be the shortest path from $v$ to $w$.

### Q6: Contrast Memoization (Top-Down) and Tabulation (Bottom-Up).
> **Answer:**
> Top-Down with Memoization uses recursion and evaluates only subproblems necessary to solve the root query, but incurs stack frame overhead and potential recursion stack overflow. Bottom-Up Tabulation solves all subproblems iteratively in topological order, eliminates recursion overhead, and enables spatial optimizations (e.g., reducing $O(nW)$ space to $O(W)$).

### Q7: Why does Dijkstra's algorithm fail on graphs with negative edge weights?
> **Answer:**
> Dijkstra relies on the Greedy Choice Property: once a vertex $u$ is extracted from the min-heap (marked visited), its distance `dist[u]` is finalized and assumed optimal. If a negative edge exists elsewhere in the graph, an alternative path through that edge could reduce the distance to an already-finalized vertex, which Dijkstra never revisits. Bellman-Ford solves this by relaxing all $|E|$ edges $|V|-1$ times.

### Q8: How does Bellman-Ford detect negative weight cycles?
> **Answer:**
> In any graph without negative weight cycles, the shortest path contains at most $|V|-1$ edges. If relaxation occurs on the $|V|$-th iteration (`dist[u] + w < dist[v]`), there must exist a cycle whose total weight is strictly negative.

### Q9: What is the time and space complexity of the Floyd-Warshall algorithm?
> **Answer:**
> Time complexity is $\Theta(V^3)$ via three nested loops over vertices $k, i, j$. Space complexity is $\Theta(V^2)$ for the distance matrix $D^{(k)}[i][j] = \min(D^{(k-1)}[i][j], D^{(k-1)}[i][k] + D^{(k-1)}[k][j])$.

### Q10: Why is Strassen's matrix multiplication faster than the standard $O(n^3)$ algorithm?
> **Answer:**
> Standard multiplication uses 8 block multiplications: $T(n) = 8T(n/2) + \Theta(n^2) \implies n^{\log_2 8} = n^3$. Strassen cleverly recombines additions and subtractions to use only 7 multiplications: $T(n) = 7T(n/2) + \Theta(n^2) \implies n^{\log_2 7} \approx n^{2.807}$.

### Q11: In Fractional Knapsack, why is the Greedy Strategy provably optimal, whereas it fails for 0/1 Knapsack?
> **Answer:**
> Fractional Knapsack exhibits the matroid property and satisfies the greedy-choice property: taking maximal fractions of the item with the highest value-to-weight ratio $\frac{v_i}{w_i}$ never precludes taking smaller density items later. In 0/1 Knapsack, taking a high-density item may leave unusable leftover capacity, leading to a suboptimal total value (e.g., $W=5$, items: $(w=3, v=6), (w=3, v=5), (w=5, v=9)$).

### Q12: Explain the role of the $\pi$ table in the Knuth-Morris-Pratt (KMP) algorithm.
> **Answer:**
> The $\pi[q]$ value stores the length of the longest proper prefix of pattern $P[0 \dots q]$ that is also a suffix of $P[0 \dots q]$. When a mismatch occurs at $P[q]$ against text character $T[i]$, instead of restarting matching at $T[i - q + 1]$, the search pointer resumes matching from pattern index $P[\pi[q-1]]$, ensuring the text pointer $i$ never decrements.

### Q13: What is the difference between Backtracking and Branch & Bound?
> **Answer:**
> - **Backtracking:** Employs Depth-First Search (DFS) on the state space tree. It prunes branches using feasibility/bounding conditions, but typically explores only one path at a time and is suited for constraint satisfaction (e.g., N-Queens, Sudoku).
> - **Branch and Bound:** Explores state space trees using BFS, DFS, or Best-First (LC) strategies. It evaluates rigorous numerical upper and lower bounds on optimization problems, pruning any node whose bound is worse than the current global best known solution.

### Q14: How does Least-Cost (LC) Branch & Bound choose the next node to expand?
> **Answer:**
> It uses an evaluation function $\hat{c}(x)$ (or upper bound $\hat{u}(x)$ for maximization) stored in a priority queue. It always extracts the node with the highest potential upper bound, enabling early convergence toward the global optimum and pruning large subtrees before they are generated.

### Q15: What is an Augmenting Path in bipartite matching? State Berge's Lemma.
> **Answer:**
> An augmenting path with respect to a matching $M$ is an alternating path that begins and ends at free (unmatched) vertices. **Berge's Lemma:** A matching $M$ is maximum if and only if there exists no augmenting path with respect to $M$.

### Q16: How does Kuhn's algorithm find a maximum bipartite matching? What is its complexity?
> **Answer:**
> Kuhn's algorithm iterates over each unmatched vertex $u \in U$ and runs a DFS to discover an augmenting path. If found, it flips matched and unmatched edges along the path, increasing matching cardinality by 1. Time complexity is $O(|V| \cdot |E|)$.

### Q17: How is Bipartite Matching reduced to the Maximum Flow problem?
> **Answer:**
> Construct directed flow network $G' = (V \cup \{s, t\}, E')$:
> 1. Add source $s$ with directed edges $(s, u)$ of capacity 1 for all $u \in U$.
> 2. Direct all original edges $(u, v)$ from $U$ to $V$ with capacity 1.
> 3. Add sink $t$ with directed edges $(v, t)$ of capacity 1 for all $v \in V$.
> The value of the maximum $s-t$ flow equals the cardinality of the maximum bipartite matching.

### Q18: What is the Chinese Remainder Theorem and what conditions are required?
> **Answer:**
> CRT states that if moduli $m_1, m_2, \dots, m_k$ are pairwise coprime ($\gcd(m_i, m_j) = 1$ for all $i \ne j$), then the system of simultaneous congruences $x \equiv a_i \pmod{m_i}$ has a unique solution modulo $M = \prod_{i=1}^k m_i$. Solved via Extended Euclidean Algorithm computing modular inverses $M_i^{-1} \pmod{m_i}$ where $M_i = M / m_i$.

### Q19: Define P, NP, NP-Complete, and NP-Hard formally.
> **Answer:**
> - **$\mathbf{P}$:** The class of decision problems solvable by a deterministic Turing machine in polynomial time $O(n^k)$.
> - **$\mathbf{NP}$:** The class of decision problems verifiable by a deterministic Turing machine in polynomial time given a certificate.
> - **$\mathbf{NP-Hard}$:** A problem $H$ is NP-hard if for every problem $L \in \text{NP}$, $L \le_P H$ (polynomial-time reducible). $H$ need not be in NP.
> - **$\mathbf{NP-Complete}$:** A problem $C$ is NP-complete if $C \in \text{NP}$ and $C$ is NP-hard.

### Q20: What is a Polynomial-Time Reduction ($A \le_P B$)?
> **Answer:**
> A reduction from decision problem $A$ to $B$ is a function $f: \Sigma^* \to \Sigma^*$ computable in polynomial time such that for every instance $x$, $x \in A \iff f(x) \in B$. If $B \in \text{P}$, then $A \in \text{P}$.

### Q21: Prove how Subset-Sum reduces to 0/1 Knapsack in polynomial time.
> **Answer:**
> Given a Subset-Sum instance $(S = \{s_1, \dots, s_n\}, T)$:
> Construct a 0/1 Knapsack instance with $n$ items where:
> - Weight $w_i = s_i$
> - Value $v_i = s_i$
> - Knapsack Capacity $W = T$
> Ask: Is there a selection of items with total value $\ge T$?
> Since total weight $\le W = T$ and total value $\ge T$, and $w_i = v_i$, the total weight must equal $T$. Thus a subset sums to $T$ if and only if the knapsack can achieve value $T$. The reduction takes $O(n)$ time.

### Q22: What is the difference between Prim's and Kruskal's algorithms for MST?
> **Answer:**
> - **Prim's Algorithm:** Grows a single tree from an arbitrary root vertex, adding the minimum-weight cut edge connecting the tree to a non-tree vertex via min-heap. Time: $O((V+E)\log V)$. Best for dense graphs.
> - **Kruskal's Algorithm:** Forest-based; sorts all edges globally by weight and adds edges that do not form a cycle using Disjoint Set Union (DSU). Time: $O(E \log E) = O(E \log V)$. Best for sparse graphs.

### Q23: Why does Path Compression in DSU yield nearly linear $\alpha(n)$ amortized time?
> **Answer:**
> Path compression flattens the tree during `find(x)` operations by attaching every traversed node directly to the root. Combined with union by rank, the amortized cost per operation is $O(\alpha(n))$ where $\alpha$ is the Inverse Ackermann Function, which is $\le 4$ for all practical inputs ($n < 10^{80}$).

### Q24: What is the Held-Karp algorithm and why is it superior to brute force?
> **Answer:**
> Held-Karp solves the Traveling Salesperson Problem using Dynamic Programming with bitmasks:
> $$C(S, j) = \min_{i \in S, i \ne j} \{ C(S \setminus \{j\}, i) + \text{dist}(i, j) \}$$
> Space: $\Theta(n 2^n)$, Time: $\Theta(n^2 2^n)$. Brute force permutation check takes $O(n!)$. For $n=20$, $n! \approx 2.4 \times 10^{18}$ operations (impossible), whereas $n^2 2^n \approx 4.1 \times 10^8$ operations (computable in seconds).

### Q25: What is the Celebrity Problem and how does the two-pointer technique solve it in $O(n)$?
> **Answer:**
> A celebrity is known by everyone but knows no one. Standard verification requires an adjacency matrix of $n \times n$ ($O(n^2)$ comparisons).
> **Two-Pointer Elimination:** Initialize $i=0, j=n-1$.
> Query `knows(i, j)`:
> - If `true`, $i$ cannot be a celebrity (celebrity knows no one) $\implies ++i$.
> - If `false`, $j$ cannot be a celebrity (everyone knows celebrity) $\implies --j$.
> Exactly $n-1$ queries eliminate $n-1$ candidates, leaving one candidate $C$. A final verification passes through $C$ in $2(n-1)$ queries $\implies O(n)$ total comparisons.

---

## Part 4: 10 Unseen Live Modification Challenges & Solutions

If the examiner asks: *"Your code works, but now modify it on the spot to do X..."*

### Challenge 1: "Modify 0/1 Knapsack to return the exact list of chosen item IDs, not just the max value."
**Solution:** Use the 2D DP table and backtrack from $(n, W)$:
```cpp
std::vector<int> selected_items;
int w = W;
for (int i = n; i > 0; --i) {
    if (dp[i][w] != dp[i - 1][w]) {
        selected_items.push_back(items[i - 1].id);
        w -= items[i - 1].weight;
    }
}
```

### Challenge 2: "Modify Dijkstra's algorithm to print the actual shortest path, not just distances."
**Solution:** Introduce a `parent` array initialized to -1:
```cpp
std::vector<int> parent(n, -1);
// Inside relaxation:
if (dist[u] + edge.weight < dist[edge.to]) {
    dist[edge.to] = dist[u] + edge.weight;
    parent[edge.to] = u;
    pq.push({dist[edge.to], edge.to});
}
// Path recovery:
std::vector<int> path;
for (int curr = target; curr != -1; curr = parent[curr]) path.push_back(curr);
std::reverse(path.begin(), path.end());
```

### Challenge 3: "Modify Kuhn's bipartite matching to support developer capacity $C_v > 1$."
**Solution:** Expand each developer $v$ into $C_v$ duplicate virtual nodes $v_{1}, v_{2}, \dots, v_{C_v}$, each connected to the same issue edges, OR modify Edmonds-Karp flow network by setting capacity of edge $(v, t) = C_v$.

### Challenge 4: "Modify KMP to return the count of occurrences without storing indices."
**Solution:**
```cpp
int count = 0;
// Inside KMP loop when q == m:
if (q == m) {
    count++;
    q = pi[q - 1];
}
return count;
```

### Challenge 5: "Detect and reconstruct the negative weight cycle in Bellman-Ford."
**Solution:** Keep track of the vertex $x$ that relaxed on the $n$-th iteration, then walk backwards $n$ times along `parent[x]` to ensure entry into the cycle, and collect vertices until returning to start.

### Challenge 6: "Convert Fractional Knapsack to handle priority ties with issue severity."
**Solution:** Custom comparator in sorting:
```cpp
std::sort(items.begin(), items.end(), [](const Item& a, const Item& b) {
    double r1 = (double)a.value / a.weight;
    double r2 = (double)b.value / b.weight;
    if (std::abs(r1 - r2) > 1e-9) return r1 > r2;
    return a.severity_rank > b.severity_rank; // Tie breaker
});
```

### Challenge 7: "Modify N-Queens to print only the first valid solution and terminate immediately."
**Solution:** Change return type of `solve_n_queens_util` from `void` to `bool`, and early-return `true` upon reaching column $N$.

### Challenge 8: "Implement early exit in Strassen when matrices are sparse (> 70% zeroes)."
**Solution:** Check zero count of sub-blocks; if a sub-block is zero, skip its corresponding multiplication in $M_1 \dots M_7$ directly.

### Challenge 9: "Add cycle detection to Kruskal's algorithm to verify input graph connectivity."
**Solution:** Count successful unites in DSU. An MST on $V$ vertices must execute exactly $V-1$ successful edge unites. If `edges_united < V - 1`, the graph is disconnected.

### Challenge 10: "Modify Floyd-Warshall to identify which pairs of nodes have negative infinity distance."
**Solution:** After standard 3-loop execution:
```cpp
for (int i = 0; i < V; ++i) {
    for (int j = 0; j < V; ++j) {
        for (int k = 0; k < V; ++k) {
            if (dist[k][k] < 0 && dist[i][k] < INF && dist[k][j] < INF) {
                dist[i][j] = -INF;
            }
        }
    }
}
```
