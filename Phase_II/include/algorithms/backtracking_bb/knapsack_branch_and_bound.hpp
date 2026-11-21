#pragma once

#include <vector>
#include <string>
#include <queue>
#include <stack>
#include <algorithm>
#include <chrono>

struct BBItem {
    int id;
    int weight;
    double value;

    double density() const {
        return weight > 0 ? (value / weight) : 0.0;
    }
};

struct BBNode {
    int level;                  // Index of decision item
    int current_weight;         // Accumulated weight
    double current_value;       // Accumulated value
    double upper_bound;         // Fractional knapsack upper bound
    std::vector<int> path_ids;  // IDs of included items

    // For LC Priority Queue (higher upper bound has higher priority)
    bool operator<(const BBNode& other) const {
        return upper_bound < other.upper_bound;
    }
};

struct BBStrategyResult {
    std::string strategy_name;
    double max_value = 0.0;
    int total_weight_used = 0;
    std::vector<int> selected_ids;
    long long nodes_generated = 0;
    long long nodes_expanded = 0;
    long long nodes_pruned = 0;
    double elapsed_microseconds = 0.0;
};

class KnapsackBranchAndBoundWorkbench {
private:
    static double compute_bound(int level, int current_weight, double current_value,
                                int capacity, const std::vector<BBItem>& items) {
        if (current_weight > capacity) return 0.0;

        double bound = current_value;
        int remaining_cap = capacity - current_weight;
        int n = static_cast<int>(items.size());

        for (int i = level; i < n; ++i) {
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

public:
    // ------------------------------------------------------------------------
    // 1. Least-Cost (LC) Branch & Bound (Priority Queue / Best-First Search)
    // ------------------------------------------------------------------------
    static BBStrategyResult solve_least_cost(std::vector<BBItem> items, int capacity) {
        BBStrategyResult result;
        result.strategy_name = "Least-Cost (LC) Branch & Bound";
        int n = static_cast<int>(items.size());
        if (n == 0 || capacity <= 0) return result;

        auto start = std::chrono::high_resolution_clock::now();

        std::sort(items.begin(), items.end(), [](const BBItem& a, const BBItem& b) {
            return a.density() > b.density();
        });

        std::priority_queue<BBNode> pq;

        BBNode root;
        root.level = 0;
        root.current_weight = 0;
        root.current_value = 0.0;
        root.upper_bound = compute_bound(0, 0, 0.0, capacity, items);
        pq.push(root);
        result.nodes_generated++;

        while (!pq.empty()) {
            BBNode curr = pq.top();
            pq.pop();
            result.nodes_expanded++;

            if (curr.upper_bound <= result.max_value) {
                result.nodes_pruned++;
                continue; // Prune node
            }

            if (curr.level == n) continue;

            // Child 1: Include item at curr.level
            if (curr.current_weight + items[curr.level].weight <= capacity) {
                BBNode left;
                left.level = curr.level + 1;
                left.current_weight = curr.current_weight + items[curr.level].weight;
                left.current_value = curr.current_value + items[curr.level].value;
                left.path_ids = curr.path_ids;
                left.path_ids.push_back(items[curr.level].id);
                left.upper_bound = compute_bound(left.level, left.current_weight, left.current_value, capacity, items);
                result.nodes_generated++;

                if (left.current_value > result.max_value) {
                    result.max_value = left.current_value;
                    result.total_weight_used = left.current_weight;
                    result.selected_ids = left.path_ids;
                }

                if (left.upper_bound > result.max_value) {
                    pq.push(left);
                } else {
                    result.nodes_pruned++;
                }
            }

            // Child 2: Exclude item at curr.level
            BBNode right;
            right.level = curr.level + 1;
            right.current_weight = curr.current_weight;
            right.current_value = curr.current_value;
            right.path_ids = curr.path_ids;
            right.upper_bound = compute_bound(right.level, right.current_weight, right.current_value, capacity, items);
            result.nodes_generated++;

            if (right.upper_bound > result.max_value) {
                pq.push(right);
            } else {
                result.nodes_pruned++;
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }

    // ------------------------------------------------------------------------
    // 2. FIFO Branch & Bound (Queue / Breadth-First Search)
    // ------------------------------------------------------------------------
    static BBStrategyResult solve_fifo(std::vector<BBItem> items, int capacity) {
        BBStrategyResult result;
        result.strategy_name = "FIFO Branch & Bound (Queue)";
        int n = static_cast<int>(items.size());
        if (n == 0 || capacity <= 0) return result;

        auto start = std::chrono::high_resolution_clock::now();

        std::sort(items.begin(), items.end(), [](const BBItem& a, const BBItem& b) {
            return a.density() > b.density();
        });

        std::queue<BBNode> q;

        BBNode root;
        root.level = 0;
        root.current_weight = 0;
        root.current_value = 0.0;
        root.upper_bound = compute_bound(0, 0, 0.0, capacity, items);
        q.push(root);
        result.nodes_generated++;

        while (!q.empty()) {
            BBNode curr = q.front();
            q.pop();
            result.nodes_expanded++;

            if (curr.upper_bound <= result.max_value) {
                result.nodes_pruned++;
                continue;
            }

            if (curr.level == n) continue;

            // Include
            if (curr.current_weight + items[curr.level].weight <= capacity) {
                BBNode left;
                left.level = curr.level + 1;
                left.current_weight = curr.current_weight + items[curr.level].weight;
                left.current_value = curr.current_value + items[curr.level].value;
                left.path_ids = curr.path_ids;
                left.path_ids.push_back(items[curr.level].id);
                left.upper_bound = compute_bound(left.level, left.current_weight, left.current_value, capacity, items);
                result.nodes_generated++;

                if (left.current_value > result.max_value) {
                    result.max_value = left.current_value;
                    result.total_weight_used = left.current_weight;
                    result.selected_ids = left.path_ids;
                }

                if (left.upper_bound > result.max_value) {
                    q.push(left);
                } else {
                    result.nodes_pruned++;
                }
            }

            // Exclude
            BBNode right;
            right.level = curr.level + 1;
            right.current_weight = curr.current_weight;
            right.current_value = curr.current_value;
            right.path_ids = curr.path_ids;
            right.upper_bound = compute_bound(right.level, right.current_weight, right.current_value, capacity, items);
            result.nodes_generated++;

            if (right.upper_bound > result.max_value) {
                q.push(right);
            } else {
                result.nodes_pruned++;
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }

    // ------------------------------------------------------------------------
    // 3. LIFO Branch & Bound (Stack / Depth-First Search)
    // ------------------------------------------------------------------------
    static BBStrategyResult solve_lifo(std::vector<BBItem> items, int capacity) {
        BBStrategyResult result;
        result.strategy_name = "LIFO Branch & Bound (Stack)";
        int n = static_cast<int>(items.size());
        if (n == 0 || capacity <= 0) return result;

        auto start = std::chrono::high_resolution_clock::now();

        std::sort(items.begin(), items.end(), [](const BBItem& a, const BBItem& b) {
            return a.density() > b.density();
        });

        std::stack<BBNode> st;

        BBNode root;
        root.level = 0;
        root.current_weight = 0;
        root.current_value = 0.0;
        root.upper_bound = compute_bound(0, 0, 0.0, capacity, items);
        st.push(root);
        result.nodes_generated++;

        while (!st.empty()) {
            BBNode curr = st.top();
            st.pop();
            result.nodes_expanded++;

            if (curr.upper_bound <= result.max_value) {
                result.nodes_pruned++;
                continue;
            }

            if (curr.level == n) continue;

            // Exclude first (so Include is processed first when popped from stack)
            BBNode right;
            right.level = curr.level + 1;
            right.current_weight = curr.current_weight;
            right.current_value = curr.current_value;
            right.path_ids = curr.path_ids;
            right.upper_bound = compute_bound(right.level, right.current_weight, right.current_value, capacity, items);
            result.nodes_generated++;

            if (right.upper_bound > result.max_value) {
                st.push(right);
            } else {
                result.nodes_pruned++;
            }

            // Include
            if (curr.current_weight + items[curr.level].weight <= capacity) {
                BBNode left;
                left.level = curr.level + 1;
                left.current_weight = curr.current_weight + items[curr.level].weight;
                left.current_value = curr.current_value + items[curr.level].value;
                left.path_ids = curr.path_ids;
                left.path_ids.push_back(items[curr.level].id);
                left.upper_bound = compute_bound(left.level, left.current_weight, left.current_value, capacity, items);
                result.nodes_generated++;

                if (left.current_value > result.max_value) {
                    result.max_value = left.current_value;
                    result.total_weight_used = left.current_weight;
                    result.selected_ids = left.path_ids;
                }

                if (left.upper_bound > result.max_value) {
                    st.push(left);
                } else {
                    result.nodes_pruned++;
                }
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
