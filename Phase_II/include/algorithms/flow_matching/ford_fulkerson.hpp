#pragma once

#include <vector>
#include <queue>
#include <algorithm>
#include <chrono>

struct FlowEdge {
    int u;
    int v;
    int capacity;
    int flow;
    int rev_index; // Index of reverse edge in adj[v]
};

struct FlowResult {
    int max_flow = 0;
    std::vector<FlowEdge> residual_edges;
    int augmenting_paths_found = 0;
    double elapsed_microseconds = 0.0;
};

class EdmondsKarpWorkbench {
private:
    // BFS to find shortest augmenting path from s to t in residual graph
    static bool bfs_find_path(int s, int t, int V,
                             const std::vector<std::vector<FlowEdge>>& adj,
                             std::vector<int>& parent_edge_idx,
                             std::vector<int>& parent_node) {
        std::vector<bool> visited(V, false);
        std::queue<int> q;

        q.push(s);
        visited[s] = true;
        parent_node[s] = -1;

        while (!q.empty()) {
            int u = q.front();
            q.pop();

            if (u == t) return true;

            for (size_t i = 0; i < adj[u].size(); ++i) {
                const auto& edge = adj[u][i];
                int residual_cap = edge.capacity - edge.flow;
                if (!visited[edge.v] && residual_cap > 0) {
                    visited[edge.v] = true;
                    parent_node[edge.v] = u;
                    parent_edge_idx[edge.v] = static_cast<int>(i);
                    q.push(edge.v);
                }
            }
        }
        return false;
    }

public:
    // ------------------------------------------------------------------------
    // Edmonds-Karp Max Flow: O(V * E^2) time, O(V + E) aux space
    // Computes maximum throughput from skill categories to developer capacity
    // ------------------------------------------------------------------------
    static FlowResult compute_max_flow(int V, int source, int sink,
                                       const std::vector<std::pair<std::pair<int, int>, int>>& raw_edges) {
        FlowResult result;
        if (V <= 0 || source < 0 || sink < 0 || source >= V || sink >= V) return result;

        auto start = std::chrono::high_resolution_clock::now();

        std::vector<std::vector<FlowEdge>> adj(V);

        // Add forward and reverse residual edges
        for (const auto& re : raw_edges) {
            int u = re.first.first;
            int v = re.first.second;
            int cap = re.second;

            FlowEdge a{u, v, cap, 0, static_cast<int>(adj[v].size())};
            FlowEdge b{v, u, 0, 0, static_cast<int>(adj[u].size())};
            adj[u].push_back(a);
            adj[v].push_back(b);
        }

        std::vector<int> parent_edge_idx(V, -1);
        std::vector<int> parent_node(V, -1);

        while (bfs_find_path(source, sink, V, adj, parent_edge_idx, parent_node)) {
            // Find bottleneck capacity along augmenting path
            int path_flow = 1e9;
            for (int curr = sink; curr != source; curr = parent_node[curr]) {
                int p = parent_node[curr];
                int edge_idx = parent_edge_idx[curr];
                path_flow = std::min(path_flow, adj[p][edge_idx].capacity - adj[p][edge_idx].flow);
            }

            // Update residual flows
            for (int curr = sink; curr != source; curr = parent_node[curr]) {
                int p = parent_node[curr];
                int edge_idx = parent_edge_idx[curr];
                adj[p][edge_idx].flow += path_flow;
                int rev_idx = adj[p][edge_idx].rev_index;
                adj[curr][rev_idx].flow -= path_flow;
            }

            result.max_flow += path_flow;
            result.augmenting_paths_found++;
        }

        // Export non-zero flow edges
        for (int u = 0; u < V; ++u) {
            for (const auto& e : adj[u]) {
                if (e.capacity > 0) {
                    result.residual_edges.push_back(e);
                }
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
