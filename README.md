# DevTriage-Optimizer

A C++17 command-line project for exploring issue prioritisation, developer assignment, and sprint planning under capacity constraints.

The program works with local CSV inputs and demonstration scenarios. It does not connect to GitHub or another issue-tracking service.

## Problem Model

The project separates the workflow into several algorithmic tasks:

1. **Prioritisation:** sort issues using severity, deadline, and stable tie-breaking rules.
2. **Developer assignment:** model skill compatibility as a bipartite graph and use augmenting paths to find a matching.
3. **Sprint selection:** use 0/1 Knapsack dynamic programming and branch-and-bound approaches to select work within a fixed capacity.
4. **Dependency validation:** detect cycles in issue prerequisite graphs using depth-first search.
5. **Graph and log analysis:** provide shortest-path and string-matching implementations for the demonstration scenarios.

## Algorithms

The Phase II workbench contains implementations from several DAA topics:

- Divide and conquer: Merge Sort, Quick Sort, Strassen multiplication, maximum subarray, fast exponentiation
- Greedy methods: Fractional Knapsack, Activity Selection, Huffman coding, Dijkstra, and minimum spanning trees
- Dynamic programming: 0/1 Knapsack, Matrix Chain Multiplication, LCS, Optimal BST, Bellman-Ford, Floyd-Warshall, and Held-Karp TSP
- Backtracking and branch and bound: N-Queens, Sum of Subsets, Knapsack, and TSP
- Graph algorithms: bipartite matching and maximum flow
- String matching: Naive, Rabin-Karp, DFA, and KMP
- Number theory and complexity: Chinese Remainder Theorem and a polynomial-reduction example

## Repository Structure

The standalone project is under `AutoTriage-DAA/`.

```text
AutoTriage-DAA/
├── Phase_I/
│   ├── include/
│   ├── src/
│   ├── tests/
│   └── data/
├── Phase_II/
│   ├── include/
│   │   ├── core/
│   │   └── algorithms/
│   ├── src/
│   ├── tests/
│   └── data/
├── docs/
└── screenshots/
```

Phase I contains the initial prioritisation and assignment program. Phase II extends the workbench with additional algorithm implementations, test programs, and scenario benchmarks. The example issue and developer records are synthetic.

## Build

Requirements:

- A C++ compiler with C++17 support
- CMake 3.10 or later, or GNU Make

Using CMake:

```bash
git clone https://github.com/ritigyam2/DevTriage-Optimizer.git
cd DevTriage-Optimizer/AutoTriage-DAA

cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

The project also includes Makefiles in the root project directory and in each phase.

## Project Documentation

- [AutoTriage-DAA/README.md](AutoTriage-DAA/README.md) — phase-level build and usage notes
- [Final project report](AutoTriage_DAA_Final_Project_Report.pdf)
- [Presentation](AutoTriage_DAA_Final_Presentation.pptx)
- [Live demonstration script](LIVE_DEMONSTRATION_SCRIPT.md)
- [Screenshots](screenshots/)

## Scope and Limitations

This is an offline algorithmic prototype using local and synthetic inputs. It demonstrates algorithm design and compares approaches on controlled scenarios; it does not establish performance on a live issue tracker or production engineering team.

## License

See [LICENSE](LICENSE).
