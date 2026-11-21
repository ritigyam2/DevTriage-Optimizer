#pragma once

#include <vector>
#include <algorithm>
#include <chrono>

struct FractionalItem {
    int id;
    double weight; // Estimated hours w_i
    double value;  // Priority value v_i
    double fraction_taken = 0.0; // In range [0.0, 1.0]

    double density() const {
        return weight > 0 ? (value / weight) : 0.0;
    }
};

struct FractionalResult {
    double total_value = 0.0;
    double total_weight_used = 0.0;
    std::vector<FractionalItem> selected_items;
    double elapsed_microseconds = 0.0;
};

class FractionalKnapsackWorkbench {
public:
    // ------------------------------------------------------------------------
    // Greedy Fractional Knapsack: O(n log n) time, O(1) aux space
    // Greedily selects items in descending order of value-density (v_i / w_i)
    // ------------------------------------------------------------------------
    static FractionalResult solve(std::vector<FractionalItem> items, double capacity) {
        FractionalResult result;
        auto start = std::chrono::high_resolution_clock::now();

        // Sort items by value density descending
        std::sort(items.begin(), items.end(), [](const FractionalItem& a, const FractionalItem& b) {
            return a.density() > b.density();
        });

        double current_capacity = capacity;
        for (auto& item : items) {
            if (current_capacity <= 0.0) break;

            if (item.weight <= current_capacity) {
                // Take whole item
                item.fraction_taken = 1.0;
                result.total_value += item.value;
                result.total_weight_used += item.weight;
                current_capacity -= item.weight;
                result.selected_items.push_back(item);
            } else {
                // Take fraction of item
                double fraction = current_capacity / item.weight;
                item.fraction_taken = fraction;
                result.total_value += item.value * fraction;
                result.total_weight_used += item.weight * fraction;
                current_capacity = 0.0;
                result.selected_items.push_back(item);
                break;
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
