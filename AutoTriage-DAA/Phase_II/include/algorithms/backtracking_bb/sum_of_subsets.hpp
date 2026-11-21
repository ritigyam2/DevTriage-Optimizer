#pragma once

#include <vector>
#include <algorithm>
#include <chrono>

struct SubsetResult {
    int total_solutions = 0;
    std::vector<std::vector<int>> valid_subsets;
    long long state_space_nodes_explored = 0;
    double elapsed_microseconds = 0.0;
};

class SumOfSubsetsWorkbench {
private:
    static void solve_recursive(int idx, int current_sum, int remaining_sum, int target,
                                const std::vector<int>& weights, std::vector<int>& current_subset,
                                SubsetResult& res) {
        res.state_space_nodes_explored++;

        if (current_sum == target) {
            res.total_solutions++;
            res.valid_subsets.push_back(current_subset);
            return;
        }

        if (idx >= static_cast<int>(weights.size())) return;

        // Pruning Bounding Condition 1:
        // If current sum + current weight exceeds target, prune
        if (current_sum + weights[idx] <= target) {
            current_subset.push_back(weights[idx]);
            solve_recursive(idx + 1, current_sum + weights[idx], remaining_sum - weights[idx],
                            target, weights, current_subset, res);
            current_subset.pop_back(); // Backtrack
        }

        // Pruning Bounding Condition 2:
        // If current sum + remaining sum without current weight is less than target, prune
        if (current_sum + remaining_sum - weights[idx] >= target) {
            solve_recursive(idx + 1, current_sum, remaining_sum - weights[idx],
                            target, weights, current_subset, res);
        }
    }

public:
    // ------------------------------------------------------------------------
    // Sum of Subsets Backtracking: O(2^n) worst case, O(n) aux space
    // Finds exact combinations of issue story-points to fill remaining sprint capacity
    // ------------------------------------------------------------------------
    static SubsetResult solve(std::vector<int> weights, int target) {
        SubsetResult result;
        if (weights.empty() || target <= 0) return result;

        auto start = std::chrono::high_resolution_clock::now();

        // Sort weights ascending to enable aggressive pruning
        std::sort(weights.begin(), weights.end());

        int total_sum = 0;
        for (int w : weights) total_sum += w;

        std::vector<int> current_subset;
        solve_recursive(0, 0, total_sum, target, weights, current_subset, result);

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
