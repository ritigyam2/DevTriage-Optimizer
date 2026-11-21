#pragma once

#include <vector>
#include <chrono>
#include <limits>
#include <algorithm>

struct FloydWarshallResult {
    int V = 0;
    std::vector<std::vector<double>> dist;
    std::vector<std::vector<int>> next_node;
    bool has_negative_cycle = false;
    double elapsed_microseconds = 0.0;

    std::vector<int> get_path(int u, int v) const {
        std::vector<int> path;
        if (u < 0 || u >= V || v < 0 || v >= V || dist[u][v] >= 1e17) {
            return path;
        }
        if (next_node[u][v] == -1) return path;

        path.push_back(u);
        while (u != v) {
            u = next_node[u][v];
            path.push_back(u);
        }
        return path;
    }

    // Blast Radius: number of downstream modules reachable from module u
    int get_blast_radius(int u) const {
        if (u < 0 || u >= V) return 0;
        int count = 0;
        for (int v = 0; v < V; ++v) {
            if (u != v && dist[u][v] < 1e17) {
                count++;
            }
        }
        return count;
    }
};

class FloydWarshallWorkbench {
public:
    // ------------------------------------------------------------------------
    // Floyd-Warshall All-Pairs Shortest Path: Theta(V^3) time, Theta(V^2) space
    // Evaluates repository-wide blast radius and reachability for every module
    // ------------------------------------------------------------------------
    static FloydWarshallResult all_pairs_shortest_path(int V, const std::vector<std::vector<double>>& cost_matrix) {
        FloydWarshallResult result;
        result.V = V;
        if (V <= 0) return result;

        auto start = std::chrono::high_resolution_clock::now();

        result.dist = cost_matrix;
        result.next_node.assign(V, std::vector<int>(V, -1));

        for (int i = 0; i < V; ++i) {
            for (int j = 0; j < V; ++j) {
                if (i != j && result.dist[i][j] < 1e17) {
                    result.next_node[i][j] = j;
                }
            }
        }

        // Triply nested DP loop: k is intermediate vertex
        for (int k = 0; k < V; ++k) {
            for (int i = 0; i < V; ++i) {
                for (int j = 0; j < V; ++j) {
                    if (result.dist[i][k] < 1e17 && result.dist[k][j] < 1e17) {
                        if (result.dist[i][k] + result.dist[k][j] < result.dist[i][j]) {
                            result.dist[i][j] = result.dist[i][k] + result.dist[k][j];
                            result.next_node[i][j] = result.next_node[i][k];
                        }
                    }
                }
            }
        }

        // Check for negative diagonal (negative cycle)
        for (int i = 0; i < V; ++i) {
            if (result.dist[i][i] < 0.0) {
                result.has_negative_cycle = true;
                break;
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
