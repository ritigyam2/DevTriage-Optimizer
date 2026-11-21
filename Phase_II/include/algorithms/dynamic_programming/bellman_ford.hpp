#pragma once

#include <vector>
#include <chrono>
#include <limits>

struct DirectedEdge {
    int u;
    int v;
    double weight;
};

struct BellmanFordResult {
    int source_vertex = -1;
    bool has_negative_cycle = false;
    std::vector<double> distances;
    std::vector<int> parents;
    double elapsed_microseconds = 0.0;
};

class BellmanFordWorkbench {
public:
    // ------------------------------------------------------------------------
    // Bellman-Ford Algorithm: Theta(V * E) time, Theta(V) aux space
    // Finds shortest paths and detects negative architectural debt cycles
    // ------------------------------------------------------------------------
    static BellmanFordResult shortest_path(int V, const std::vector<DirectedEdge>& edges, int src) {
        BellmanFordResult result;
        if (V <= 0 || src < 0 || src >= V) return result;

        result.source_vertex = src;
        result.distances.assign(V, 1e18);
        result.parents.assign(V, -1);
        result.distances[src] = 0.0;

        auto start = std::chrono::high_resolution_clock::now();

        // Relax all edges V - 1 times
        for (int i = 1; i <= V - 1; ++i) {
            bool any_relaxed = false;
            for (const auto& e : edges) {
                if (result.distances[e.u] < 1e17) {
                    if (result.distances[e.u] + e.weight < result.distances[e.v]) {
                        result.distances[e.v] = result.distances[e.u] + e.weight;
                        result.parents[e.v] = e.u;
                        any_relaxed = true;
                    }
                }
            }
            if (!any_relaxed) break; // Early termination if converged
        }

        // Pass V: Check for negative weight cycles
        for (const auto& e : edges) {
            if (result.distances[e.u] < 1e17) {
                if (result.distances[e.u] + e.weight < result.distances[e.v]) {
                    result.has_negative_cycle = true;
                    break;
                }
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
