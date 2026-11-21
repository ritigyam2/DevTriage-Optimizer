#include "../include/algorithms/dynamic_programming/knapsack_01.hpp"
#include "../include/algorithms/dynamic_programming/matrix_chain.hpp"
#include "../include/algorithms/dynamic_programming/lcs.hpp"
#include "../include/algorithms/dynamic_programming/obst.hpp"
#include "../include/algorithms/dynamic_programming/bellman_ford.hpp"
#include "../include/algorithms/dynamic_programming/floyd_warshall.hpp"
#include "../include/algorithms/dynamic_programming/tsp_held_karp.hpp"

#include <iostream>
#include <cassert>
#include <vector>
#include <cmath>

void test_knapsack_01() {
    std::cout << "[TEST 1] Running 0/1 Knapsack (2D vs 1D Space-Optimized) Test...";

    std::vector<KnapsackItem> items = {
        {1, 10, 60.0},
        {2, 20, 100.0},
        {3, 30, 120.0}
    };
    int capacity = 50;

    Knapsack01Result res_2d = Knapsack01Workbench::solve_2d(items, capacity);
    Knapsack01Result res_1d = Knapsack01Workbench::solve_1d_space_optimized(items, capacity);

    // Discrete 0/1 choice selects Item 2 + Item 3 = $220.0 with weight 50
    assert(std::fabs(res_2d.max_value - 220.0) < 1e-4);
    assert(std::fabs(res_1d.max_value - 220.0) < 1e-4);
    assert(res_2d.total_weight_used == 50);

    // Verify backtracked item IDs are exactly [2, 3]
    assert(res_2d.selected_item_ids.size() == 2);
    assert(res_2d.selected_item_ids[0] == 2);
    assert(res_2d.selected_item_ids[1] == 3);

    std::cout << " PASSED! (Both 2D & 1D yield exact discrete optimum: $" << res_2d.max_value 
              << " | Selected Items: #2, #3)\n";
}

void test_matrix_chain_multiplication() {
    std::cout << "[TEST 2] Running Matrix Chain Multiplication (MCM) Test...";

    // 4 matrices: A1(10x20), A2(20x30), A3(30x40), A4(40x30)
    std::vector<int> p = {10, 20, 30, 40, 30};

    MCMResult res = MatrixChainWorkbench::solve(p);

    // Textbook optimal cost for this chain is 30,000 multiplications
    assert(res.min_multiplications == 30000);
    assert(!res.optimal_parenthesization.empty());

    std::cout << " PASSED! (Min scalar multiplications: " << res.min_multiplications 
              << " | Order: " << res.optimal_parenthesization << ")\n";
}

void test_longest_common_subsequence() {
    std::cout << "[TEST 3] Running Longest Common Subsequence (LCS) Test...";

    std::string X = "ABCBDAB";
    std::string Y = "BDCABA";

    LCSResult res = LCSWorkbench::solve(X, Y);

    // Length of LCS is 4 (e.g. "BCBA" or "BDAB")
    assert(res.length == 4);
    assert(res.lcs_string.length() == 4);
    assert(res.similarity_percentage > 0.0);

    std::cout << " PASSED! (LCS Length: " << res.length 
              << " | Subsequence: \"" << res.lcs_string 
              << "\" | Similarity: " << res.similarity_percentage << "%)\n";
}

void test_optimal_bst() {
    std::cout << "[TEST 4] Running Optimal Binary Search Tree (OBST) Test...";

    std::vector<std::string> keys = {"crash", "memory", "network", "security"};
    std::vector<double> p = {0.15, 0.10, 0.05, 0.10}; // Search probabilities
    std::vector<double> q = {0.05, 0.10, 0.05, 0.05, 0.10}; // Unsuccessful search probabilities

    OBSTResult res = OBSTWorkbench::solve(keys, p, q);

    assert(res.expected_cost > 0.0);
    assert(res.root_table.size() == 5);

    std::cout << " PASSED! (OBST Expected Cost: " << res.expected_cost 
              << " | Root Key Index: " << res.root_table[1][4] << ")\n";
}

void test_bellman_ford() {
    std::cout << "[TEST 5] Running Bellman-Ford Shortest Path & Negative Cycle Test...";

    int V = 5;
    // Graph without negative cycle
    std::vector<DirectedEdge> edges_valid = {
        {0, 1, -1.0},
        {0, 2, 4.0},
        {1, 2, 3.0},
        {1, 3, 2.0},
        {1, 4, 2.0},
        {3, 2, 5.0},
        {3, 1, 1.0},
        {4, 3, -3.0}
    };

    BellmanFordResult res_valid = BellmanFordWorkbench::shortest_path(V, edges_valid, 0);
    assert(!res_valid.has_negative_cycle);
    assert(res_valid.distances[0] == 0.0);
    assert(res_valid.distances[1] == -1.0);
    assert(res_valid.distances[2] == 2.0);
    assert(res_valid.distances[3] == -2.0);
    assert(res_valid.distances[4] == 1.0);

    // Graph WITH negative cycle: 1 -> 2 (w=1), 2 -> 3 (w=2), 3 -> 1 (w=-5) => sum = -2
    std::vector<DirectedEdge> edges_cycle = {
        {0, 1, 1.0},
        {1, 2, 1.0},
        {2, 3, 2.0},
        {3, 1, -5.0}
    };
    BellmanFordResult res_cycle = BellmanFordWorkbench::shortest_path(4, edges_cycle, 0);
    assert(res_cycle.has_negative_cycle);

    std::cout << " PASSED! (Distances correct and negative cycle correctly detected)\n";
}

void test_floyd_warshall() {
    std::cout << "[TEST 6] Running Floyd-Warshall All-Pairs & Blast Radius Test...";

    const double INF = 1e18;
    int V = 4;
    std::vector<std::vector<double>> cost = {
        {0.0, 3.0, INF, 7.0},
        {8.0, 0.0, 2.0, INF},
        {5.0, INF, 0.0, 1.0},
        {2.0, INF, INF, 0.0}
    };

    FloydWarshallResult res = FloydWarshallWorkbench::all_pairs_shortest_path(V, cost);

    assert(!res.has_negative_cycle);
    // Shortest path 0 -> 2: 0 -> 1 -> 2: cost = 3 + 2 = 5.0
    assert(res.dist[0][2] == 5.0);
    // Shortest path 0 -> 3: 0 -> 1 -> 2 -> 3: cost = 3 + 2 + 1 = 6.0 (beats direct 7.0)
    assert(res.dist[0][3] == 6.0);

    // Path verification
    auto path_0_to_3 = res.get_path(0, 3);
    assert(path_0_to_3.size() == 4);
    assert(path_0_to_3[0] == 0 && path_0_to_3[1] == 1 && path_0_to_3[2] == 2 && path_0_to_3[3] == 3);

    // Blast radius: module 0 can reach all other 3 modules
    assert(res.get_blast_radius(0) == 3);

    std::cout << " PASSED! (All-pairs verified. 0->3 shortest: " << res.dist[0][3] 
              << " via intermediate nodes | Blast radius: " << res.get_blast_radius(0) << ")\n";
}

void test_tsp_held_karp() {
    std::cout << "[TEST 7] Running TSP Held-Karp Bitmask DP Test...";

    // 4 microservices distance matrix
    std::vector<std::vector<double>> dist = {
        {0.0, 10.0, 15.0, 20.0},
        {10.0, 0.0, 35.0, 25.0},
        {15.0, 35.0, 0.0, 30.0},
        {20.0, 25.0, 30.0, 0.0}
    };

    TSPResult res = TSPHeldKarpWorkbench::solve(dist);

    // Optimal tour: 0 -> 1 -> 3 -> 2 -> 0 has cost: 10 + 25 + 30 + 15 = 80.0
    assert(std::fabs(res.min_tour_cost - 80.0) < 1e-4);
    assert(res.tour.size() == 5);
    assert(res.tour[0] == 0 && res.tour[4] == 0);

    std::cout << " PASSED! (Optimal Closed Tour Cost: " << res.min_tour_cost << " | Route: ";
    for (size_t i = 0; i < res.tour.size(); ++i) {
        std::cout << res.tour[i] << (i + 1 < res.tour.size() ? "->" : "");
    }
    std::cout << ")\n";
}

int main() {
    std::cout << "\n=================================================================\n";
    std::cout << "  RUNNING CHUNK 4 AUTOMATED TEST SUITE (Dynamic Programming)\n";
    std::cout << "=================================================================\n\n";

    test_knapsack_01();
    test_matrix_chain_multiplication();
    test_longest_common_subsequence();
    test_optimal_bst();
    test_bellman_ford();
    test_floyd_warshall();
    test_tsp_held_karp();

    std::cout << "\n=================================================================\n";
    std::cout << "  Test summary: 7/7 tests passed.\n";
    std::cout << "=================================================================\n\n";
    return 0;
}
