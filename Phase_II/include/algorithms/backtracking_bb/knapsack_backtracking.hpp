#pragma once

#include <vector>
#include <algorithm>
#include <chrono>

struct BTKnapsackItem {
    int id;
    int weight;
    double value;

    double density() const {
        return weight > 0 ? (value / weight) : 0.0;
    }
};

struct BTKnapsackResult {
    double max_value = 0.0;
    int total_weight_used = 0;
    std::vector<int> selected_ids;
    long long nodes_visited = 0;
    long long nodes_pruned = 0;
    double elapsed_microseconds = 0.0;
};

class KnapsackBacktrackingWorkbench {
private:
    // Computes upper bound using Fractional Knapsack from index idx onwards
    static double calculate_upper_bound(int idx, int current_weight, double current_value,
                                        int capacity, const std::vector<BTKnapsackItem>& items) {
        double bound = current_value;
        int remaining_cap = capacity - current_weight;
        int n = static_cast<int>(items.size());

        for (int i = idx; i < n; ++i) {
            if (items[i].weight <= remaining_cap) {
                remaining_cap -= items[i].weight;
                bound += items[i].value;
            } else {
                bound += items[i].value * (static_cast<double>(remaining_cap) / items[i].weight);
                break;
            }
        }
        return bound;
    }

    static void solve_recursive(int idx, int current_weight, double current_value, int capacity,
                                const std::vector<BTKnapsackItem>& items,
                                std::vector<int>& current_selection,
                                BTKnapsackResult& res, std::vector<int>& best_selection) {
        res.nodes_visited++;

        // Update best feasible solution found so far
        if (current_value > res.max_value) {
            res.max_value = current_value;
            res.total_weight_used = current_weight;
            best_selection = current_selection;
        }

        if (idx >= static_cast<int>(items.size())) return;

        // Bounding check: can this subtree beat the current best value?
        double bound = calculate_upper_bound(idx, current_weight, current_value, capacity, items);
        if (bound <= res.max_value) {
            res.nodes_pruned++;
            return; // Prune non-promising branch
        }

        // Branch 1: Include item idx (if feasible)
        if (current_weight + items[idx].weight <= capacity) {
            current_selection.push_back(items[idx].id);
            solve_recursive(idx + 1, current_weight + items[idx].weight, current_value + items[idx].value,
                            capacity, items, current_selection, res, best_selection);
            current_selection.pop_back(); // Backtrack
        }

        // Branch 2: Exclude item idx
        solve_recursive(idx + 1, current_weight, current_value,
                        capacity, items, current_selection, res, best_selection);
    }

public:
    // ------------------------------------------------------------------------
    // 0/1 Knapsack Backtracking: O(2^n) worst case, O(n) space
    // State-space tree with Fractional Knapsack upper-bounding pruning
    // ------------------------------------------------------------------------
    static BTKnapsackResult solve(std::vector<BTKnapsackItem> items, int capacity) {
        BTKnapsackResult result;
        if (items.empty() || capacity <= 0) return result;

        auto start = std::chrono::high_resolution_clock::now();

        // Sort items by value density descending to maximize bounding sharpness
        std::sort(items.begin(), items.end(), [](const BTKnapsackItem& a, const BTKnapsackItem& b) {
            return a.density() > b.density();
        });

        std::vector<int> current_selection;
        std::vector<int> best_selection;

        solve_recursive(0, 0, 0.0, capacity, items, current_selection, result, best_selection);

        result.selected_ids = best_selection;
        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
