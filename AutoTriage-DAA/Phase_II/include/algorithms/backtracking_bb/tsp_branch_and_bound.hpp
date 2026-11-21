#pragma once

#include <vector>
#include <queue>
#include <limits>
#include <chrono>

struct TSPBBResult {
    double min_cost = 1e18;
    std::vector<int> tour;
    long long nodes_generated = 0;
    long long nodes_expanded = 0;
    long long nodes_pruned = 0;
    double elapsed_microseconds = 0.0;
};

class TSPBranchAndBoundWorkbench {
private:
    static constexpr double INF = 1e18;

    struct Node {
        std::vector<std::vector<double>> reduced_matrix;
        double cost; // Lower bound cost
        int vertex;  // Current vertex
        int level;   // Number of cities visited so far
        std::vector<int> path;

        // Min-heap: lowest lower bound cost has highest priority (Least-Cost Search)
        bool operator>(const Node& other) const {
            return cost > other.cost;
        }
    };

    // Reduces matrix by subtracting row and column minimums
    static double reduce_matrix(std::vector<std::vector<double>>& matrix, int n) {
        double reduction_sum = 0.0;

        // Row reduction
        for (int i = 0; i < n; ++i) {
            double row_min = INF;
            for (int j = 0; j < n; ++j) {
                if (matrix[i][j] < row_min) row_min = matrix[i][j];
            }
            if (row_min < INF && row_min > 0.0) {
                reduction_sum += row_min;
                for (int j = 0; j < n; ++j) {
                    if (matrix[i][j] < INF) matrix[i][j] -= row_min;
                }
            }
        }

        // Column reduction
        for (int j = 0; j < n; ++j) {
            double col_min = INF;
            for (int i = 0; i < n; ++i) {
                if (matrix[i][j] < col_min) col_min = matrix[i][j];
            }
            if (col_min < INF && col_min > 0.0) {
                reduction_sum += col_min;
                for (int i = 0; i < n; ++i) {
                    if (matrix[i][j] < INF) matrix[i][j] -= col_min;
                }
            }
        }

        return reduction_sum;
    }

public:
    // ------------------------------------------------------------------------
    // TSP Branch & Bound: Exact solver using Reduced Cost Matrices
    // Least-Cost Search with lower-bounding matrix reduction
    // ------------------------------------------------------------------------
    static TSPBBResult solve(const std::vector<std::vector<double>>& orig_matrix) {
        TSPBBResult result;
        int n = static_cast<int>(orig_matrix.size());
        if (n <= 1) return result;

        auto start = std::chrono::high_resolution_clock::now();

        std::vector<std::vector<double>> matrix = orig_matrix;
        // Ensure self-loops are INF
        for (int i = 0; i < n; ++i) matrix[i][i] = INF;

        std::priority_queue<Node, std::vector<Node>, std::greater<Node>> pq;

        // Initialize root node
        Node root;
        root.reduced_matrix = matrix;
        root.cost = reduce_matrix(root.reduced_matrix, n);
        root.vertex = 0;
        root.level = 1;
        root.path.push_back(0);

        pq.push(root);
        result.nodes_generated++;

        while (!pq.empty()) {
            Node curr = pq.top();
            pq.pop();
            result.nodes_expanded++;

            if (curr.cost >= result.min_cost) {
                result.nodes_pruned++;
                continue;
            }

            // All cities visited! Compute exact closed tour cost back to city 0
            if (curr.level == n) {
                double return_edge = orig_matrix[curr.vertex][0];
                if (return_edge < INF) {
                    double tour_cost = 0.0;
                    for (size_t i = 0; i + 1 < curr.path.size(); ++i) {
                        tour_cost += orig_matrix[curr.path[i]][curr.path[i + 1]];
                    }
                    tour_cost += return_edge;

                    if (tour_cost < result.min_cost) {
                        result.min_cost = tour_cost;
                        result.tour = curr.path;
                        result.tour.push_back(0); // Close tour
                    }
                }
                continue;
            }

            // Branch to all unvisited cities
            for (int v = 0; v < n; ++v) {
                if (curr.reduced_matrix[curr.vertex][v] < INF) {
                    Node child;
                    child.reduced_matrix = curr.reduced_matrix;
                    child.level = curr.level + 1;
                    child.vertex = v;
                    child.path = curr.path;
                    child.path.push_back(v);

                    double edge_cost = curr.reduced_matrix[curr.vertex][v];

                    // Set row of curr.vertex and col of v to INF
                    for (int k = 0; k < n; ++k) {
                        child.reduced_matrix[curr.vertex][k] = INF;
                        child.reduced_matrix[k][v] = INF;
                    }
                    // Prevent return to start if not yet at the last level
                    if (child.level < n) {
                        child.reduced_matrix[v][0] = INF;
                    }

                    double add_reduction = reduce_matrix(child.reduced_matrix, n);
                    child.cost = curr.cost + edge_cost + add_reduction;
                    result.nodes_generated++;

                    if (child.cost < result.min_cost) {
                        pq.push(child);
                    } else {
                        result.nodes_pruned++;
                    }
                }
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
