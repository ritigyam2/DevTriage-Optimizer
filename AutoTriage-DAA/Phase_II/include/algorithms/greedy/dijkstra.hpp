#pragma once

#include <vector>
#include <queue>
#include <chrono>
#include <limits>
#include <algorithm>

struct DijkstraResult {
    int source_vertex = -1;
    std::vector<double> distances;
    std::vector<int> parents;
    long long relaxations = 0;
    double elapsed_microseconds = 0.0;

    std::vector<int> get_path(int target) const {
        std::vector<int> path;
        if (target < 0 || target >= static_cast<int>(distances.size()) || distances[target] >= 1e17) {
            return path; // Unreachable
        }
        for (int curr = target; curr != -1; curr = parents[curr]) {
            path.push_back(curr);
        }
        std::reverse(path.begin(), path.end());
        return path;
    }
};

class DijkstraWorkbench {
public:
    using WeightedGraph = std::vector<std::vector<std::pair<int, double>>>; // (target_vertex, weight)

    // ------------------------------------------------------------------------
    // Dijkstra's Shortest Path: O((V + E) log V) time, O(V) aux space
    // Finds minimum refactoring risk path through module dependency graph
    // ------------------------------------------------------------------------
    static DijkstraResult shortest_path(const WeightedGraph& adj, int src) {
        DijkstraResult result;
        int V = static_cast<int>(adj.size());
        if (src < 0 || src >= V) return result;

        result.source_vertex = src;
        result.distances.assign(V, 1e18);
        result.parents.assign(V, -1);

        auto start = std::chrono::high_resolution_clock::now();

        // Min-heap storing pairs: (dist, vertex)
        using HeapElem = std::pair<double, int>;
        std::priority_queue<HeapElem, std::vector<HeapElem>, std::greater<HeapElem>> pq;

        result.distances[src] = 0.0;
        pq.push({0.0, src});

        while (!pq.empty()) {
            auto top = pq.top();
            pq.pop();
            double d = top.first;
            int u = top.second;

            // Skip if obsolete path
            if (d > result.distances[u]) continue;

            for (const auto& edge : adj[u]) {
                int v = edge.first;
                double weight = edge.second;

                if (weight < 0.0) {
                    // Dijkstra fails on negative weights; defensive guard
                    continue;
                }

                if (result.distances[u] + weight < result.distances[v]) {
                    result.distances[v] = result.distances[u] + weight;
                    result.parents[v] = u;
                    result.relaxations++;
                    pq.push({result.distances[v], v});
                }
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
