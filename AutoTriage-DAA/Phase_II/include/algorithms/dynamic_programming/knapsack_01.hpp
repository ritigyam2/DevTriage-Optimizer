#pragma once

#include <vector>
#include <algorithm>
#include <chrono>

struct KnapsackItem {
    int id;
    int weight; // Estimated developer hours w_i
    double value; // Business priority value v_i
};

struct Knapsack01Result {
    double max_value = 0.0;
    int total_weight_used = 0;
    std::vector<int> selected_item_ids;
    double elapsed_microseconds = 0.0;
    long long dp_table_cell_computations = 0;
};

class Knapsack01Workbench {
public:
    // ------------------------------------------------------------------------
    // 1. Standard 2D Dynamic Programming with Item Backtracking: O(n * W)
    // ------------------------------------------------------------------------
    static Knapsack01Result solve_2d(const std::vector<KnapsackItem>& items, int capacity) {
        Knapsack01Result result;
        int n = static_cast<int>(items.size());
        if (n == 0 || capacity <= 0) return result;

        auto start = std::chrono::high_resolution_clock::now();

        // DP table: dp[i][w] is max value using a subset of first i items with capacity w
        std::vector<std::vector<double>> dp(n + 1, std::vector<double>(capacity + 1, 0.0));

        for (int i = 1; i <= n; ++i) {
            int wt = items[i - 1].weight;
            double val = items[i - 1].value;
            for (int w = 0; w <= capacity; ++w) {
                result.dp_table_cell_computations++;
                if (wt <= w) {
                    dp[i][w] = std::max(dp[i - 1][w], dp[i - 1][w - wt] + val);
                } else {
                    dp[i][w] = dp[i - 1][w];
                }
            }
        }

        result.max_value = dp[n][capacity];

        // Backtrack to recover selected item IDs
        int w = capacity;
        for (int i = n; i > 0 && result.max_value > 0; --i) {
            // If value differs from previous row, item i-1 was included
            if (dp[i][w] != dp[i - 1][w]) {
                result.selected_item_ids.push_back(items[i - 1].id);
                result.total_weight_used += items[i - 1].weight;
                w -= items[i - 1].weight;
            }
        }
        std::reverse(result.selected_item_ids.begin(), result.selected_item_ids.end());

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }

    // ------------------------------------------------------------------------
    // 2. Space-Optimized 1D Array DP: O(n * W) time, O(W) aux space
    // Iterating w backwards preserves the 0/1 invariant
    // ------------------------------------------------------------------------
    static Knapsack01Result solve_1d_space_optimized(const std::vector<KnapsackItem>& items, int capacity) {
        Knapsack01Result result;
        int n = static_cast<int>(items.size());
        if (n == 0 || capacity <= 0) return result;

        auto start = std::chrono::high_resolution_clock::now();

        std::vector<double> dp(capacity + 1, 0.0);

        for (int i = 0; i < n; ++i) {
            int wt = items[i].weight;
            double val = items[i].value;
            // Reverse loop: from capacity down to wt
            for (int w = capacity; w >= wt; --w) {
                result.dp_table_cell_computations++;
                dp[w] = std::max(dp[w], dp[w - wt] + val);
            }
        }

        result.max_value = dp[capacity];
        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
