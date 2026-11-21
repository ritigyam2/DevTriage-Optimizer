#include "../include/algorithms/backtracking_bb/n_queens.hpp"
#include "../include/algorithms/backtracking_bb/sum_of_subsets.hpp"
#include "../include/algorithms/backtracking_bb/knapsack_backtracking.hpp"
#include "../include/algorithms/backtracking_bb/knapsack_branch_and_bound.hpp"
#include "../include/algorithms/backtracking_bb/tsp_branch_and_bound.hpp"

#include <iostream>
#include <cassert>
#include <vector>
#include <cmath>

void test_n_queens() {
    std::cout << "[TEST 1] Running N-Queens Backtracking Test...";

    // N = 4 has exactly 2 solutions
    NQueensResult res4 = NQueensWorkbench::solve(4);
    assert(res4.total_solutions == 2);
    assert(res4.solutions.size() == 2);

    // Verify diagonal and column safety on solutions
    for (const auto& sol : res4.solutions) {
        for (int r1 = 0; r1 < 4; ++r1) {
            for (int r2 = r1 + 1; r2 < 4; ++r2) {
                assert(sol[r1] != sol[r2]); // Distinct columns
                assert(std::abs(r1 - r2) != std::abs(sol[r1] - sol[r2])); // Distinct diagonals
            }
        }
    }

    // N = 8 has exactly 92 solutions (classical textbook benchmark)
    NQueensResult res8 = NQueensWorkbench::solve(8);
    assert(res8.total_solutions == 92);

    std::cout << " PASSED! (N=4: " << res4.total_solutions << " solutions, N=8: " 
              << res8.total_solutions << " solutions)\n";
}

void test_sum_of_subsets() {
    std::cout << "[TEST 2] Running Sum of Subsets Backtracking Test...";

    std::vector<int> weights = {10, 7, 5, 18, 12, 20, 15};
    int target = 35;

    SubsetResult res = SumOfSubsetsWorkbench::solve(weights, target);

    assert(res.total_solutions > 0);
    // Verify each returned subset sums to exactly 35
    for (const auto& subset : res.valid_subsets) {
        int sum = 0;
        for (int w : subset) sum += w;
        assert(sum == target);
    }

    std::cout << " PASSED! (Found " << res.total_solutions 
              << " exact subset combinations summing to " << target 
              << " | Nodes Explored: " << res.state_space_nodes_explored << ")\n";
}

void test_knapsack_backtracking() {
    std::cout << "[TEST 3] Running 0/1 Knapsack Backtracking Test...";

    std::vector<BTKnapsackItem> items = {
        {1, 10, 60.0},
        {2, 20, 100.0},
        {3, 30, 120.0}
    };
    int capacity = 50;

    BTKnapsackResult res = KnapsackBacktrackingWorkbench::solve(items, capacity);

    // Matches DP result: Items 2 and 3 = $220.0
    assert(std::fabs(res.max_value - 220.0) < 1e-4);
    assert(res.total_weight_used == 50);
    assert(res.selected_ids.size() == 2);
    assert(res.nodes_pruned > 0);

    std::cout << " PASSED! (Max Value: $" << res.max_value 
              << " | Nodes Visited: " << res.nodes_visited 
              << " | Nodes Pruned: " << res.nodes_pruned << ")\n";
}

void test_knapsack_branch_and_bound_suite() {
    std::cout << "[TEST 4] Running Knapsack Branch & Bound (FIFO vs LIFO vs Least-Cost) Test...";

    std::vector<BBItem> items = {
        {1, 10, 60.0},
        {2, 20, 100.0},
        {3, 30, 120.0},
        {4, 15, 75.0},
        {5, 25, 90.0}
    };
    int capacity = 60;

    BBStrategyResult res_lc = KnapsackBranchAndBoundWorkbench::solve_least_cost(items, capacity);
    BBStrategyResult res_fifo = KnapsackBranchAndBoundWorkbench::solve_fifo(items, capacity);
    BBStrategyResult res_lifo = KnapsackBranchAndBoundWorkbench::solve_lifo(items, capacity);

    // All three strategies must converge to the exact same optimal value
    assert(std::fabs(res_lc.max_value - res_fifo.max_value) < 1e-4);
    assert(std::fabs(res_lc.max_value - res_lifo.max_value) < 1e-4);
    assert(res_lc.total_weight_used <= capacity);

    std::cout << " PASSED! (All 3 strategies yield identical optimal value: $" << res_lc.max_value << ")\n";
    std::cout << "         [LC B&B]   Nodes Generated: " << res_lc.nodes_generated 
              << ", Expanded: " << res_lc.nodes_expanded << ", Pruned: " << res_lc.nodes_pruned << "\n";
    std::cout << "         [FIFO B&B] Nodes Generated: " << res_fifo.nodes_generated 
              << ", Expanded: " << res_fifo.nodes_expanded << ", Pruned: " << res_fifo.nodes_pruned << "\n";
    std::cout << "         [LIFO B&B] Nodes Generated: " << res_lifo.nodes_generated 
              << ", Expanded: " << res_lifo.nodes_expanded << ", Pruned: " << res_lifo.nodes_pruned << "\n";
}

void test_tsp_branch_and_bound() {
    std::cout << "[TEST 5] Running TSP Branch & Bound (Reduced Cost Matrix) Test...";

    // 4-city cost matrix
    std::vector<std::vector<double>> matrix = {
        {0.0, 10.0, 15.0, 20.0},
        {10.0, 0.0, 35.0, 25.0},
        {15.0, 35.0, 0.0, 30.0},
        {20.0, 25.0, 30.0, 0.0}
    };

    TSPBBResult res = TSPBranchAndBoundWorkbench::solve(matrix);

    // Matches Held-Karp DP optimal cost: 80.0
    assert(std::fabs(res.min_cost - 80.0) < 1e-4);
    assert(res.tour.size() == 5);
    assert(res.tour[0] == 0 && res.tour[4] == 0);

    std::cout << " PASSED! (Tour Cost: " << res.min_cost 
              << " | Nodes Generated: " << res.nodes_generated 
              << " | Pruned: " << res.nodes_pruned << ")\n";
}

int main() {
    std::cout << "\n=================================================================\n";
    std::cout << "  RUNNING CHUNK 5 AUTOMATED TEST SUITE (Backtracking & B&B)\n";
    std::cout << "=================================================================\n\n";

    test_n_queens();
    test_sum_of_subsets();
    test_knapsack_backtracking();
    test_knapsack_branch_and_bound_suite();
    test_tsp_branch_and_bound();

    std::cout << "\n=================================================================\n";
    std::cout << "  Test summary: 5/5 tests passed.\n";
    std::cout << "=================================================================\n\n";
    return 0;
}
