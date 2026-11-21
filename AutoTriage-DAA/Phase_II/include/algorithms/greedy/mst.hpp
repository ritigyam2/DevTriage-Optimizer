#pragma once

#include <vector>
#include <queue>
#include <algorithm>
#include <chrono>

struct Edge {
    int u;
    int v;
    double weight;
};

struct MSTResult {
    double total_weight = 0.0;
    std::vector<Edge> mst_edges;
    double elapsed_microseconds = 0.0;
};

// ------------------------------------------------------------------------
// Disjoint Set Union (DSU) with Path Compression & Union by Rank
// ------------------------------------------------------------------------
class DisjointSetUnion {
private:
    std::vector<int> parent;
    std::vector<int> rank;

public:
    DisjointSetUnion(int n) : parent(n), rank(n, 0) {
        for (int i = 0; i < n; ++i) parent[i] = i;
    }

    int find_set(int v) {
        if (v == parent[v]) return v;
        // Path compression
        return parent[v] = find_set(parent[v]);
    }

    bool union_sets(int a, int b) {
        a = find_set(a);
        b = find_set(b);
        if (a == b) return false; // Cycle detected

        // Union by rank
        if (rank[a] < rank[b]) {
            std::swap(a, b);
        }
        parent[b] = a;
        if (rank[a] == rank[b]) {
            rank[a]++;
        }
        return true;
    }
};

class MSTWorkbench {
public:
    // ------------------------------------------------------------------------
    // 1. Kruskal's MST: O(E log E) time, O(V) aux space
    // Greedily adds minimum weight edges using DSU
    // ------------------------------------------------------------------------
    static MSTResult kruskal_mst(int V, std::vector<Edge> edges) {
        MSTResult result;
        auto start = std::chrono::high_resolution_clock::now();

        // Sort all edges by weight ascending
        std::sort(edges.begin(), edges.end(), [](const Edge& a, const Edge& b) {
            return a.weight < b.weight;
        });

        DisjointSetUnion dsu(V);
        for (const auto& edge : edges) {
            if (dsu.union_sets(edge.u, edge.v)) {
                result.total_weight += edge.weight;
                result.mst_edges.push_back(edge);
                if (static_cast<int>(result.mst_edges.size()) == V - 1) {
                    break;
                }
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }

    // ------------------------------------------------------------------------
    // 2. Prim's MST: O((V + E) log V) time, O(V) aux space
    // Greedily grows tree from source node 0 via Min-Heap
    // ------------------------------------------------------------------------
    static MSTResult prim_mst(int V, const std::vector<std::vector<std::pair<int, double>>>& adj) {
        MSTResult result;
        if (V <= 0) return result;

        auto start = std::chrono::high_resolution_clock::now();

        std::vector<bool> in_mst(V, false);
        // Min-heap storing: (weight, target_vertex, source_vertex)
        using PrimEdge = std::pair<double, std::pair<int, int>>;
        std::priority_queue<PrimEdge, std::vector<PrimEdge>, std::greater<PrimEdge>> pq;

        // Start with vertex 0
        in_mst[0] = true;
        for (const auto& edge : adj[0]) {
            pq.push({edge.second, {edge.first, 0}});
        }

        while (!pq.empty() && static_cast<int>(result.mst_edges.size()) < V - 1) {
            auto top = pq.top();
            pq.pop();

            double weight = top.first;
            int u = top.second.first;
            int src = top.second.second;

            if (in_mst[u]) continue;

            in_mst[u] = true;
            result.total_weight += weight;
            result.mst_edges.push_back({src, u, weight});

            for (const auto& edge : adj[u]) {
                int v = edge.first;
                double w = edge.second;
                if (!in_mst[v]) {
                    pq.push({w, {v, u}});
                }
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
