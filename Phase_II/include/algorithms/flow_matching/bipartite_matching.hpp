#pragma once

#include "ford_fulkerson.hpp"
#include <vector>
#include <chrono>

struct BipartiteAssignmentResult {
    int max_matched = 0;
    std::vector<std::pair<int, int>> issue_dev_pairs; // (issue_id, dev_id)
    double elapsed_microseconds = 0.0;
};

class BipartiteFlowWorkbench {
public:
    // ------------------------------------------------------------------------
    // Maximum Bipartite Matching via Reduction to Max Flow: O(V * E)
    // Converts two-sided assignment into a directed unit network with source & sink
    // ------------------------------------------------------------------------
    static BipartiteAssignmentResult solve(int N_issues, int M_devs,
                                          const std::vector<std::vector<int>>& compatibility_adj) {
        BipartiteAssignmentResult result;
        auto start = std::chrono::high_resolution_clock::now();

        // Total vertices = 1 (source) + N_issues + M_devs + 1 (sink)
        int source = 0;
        int sink = 1 + N_issues + M_devs;
        int V = sink + 1;

        std::vector<std::pair<std::pair<int, int>, int>> edges;

        // 1. Source -> Issues (capacity 1)
        for (int i = 0; i < N_issues; ++i) {
            int issue_node = 1 + i;
            edges.push_back({{source, issue_node}, 1});
        }

        // 2. Issues -> Compatible Developers (capacity 1)
        for (int i = 0; i < N_issues; ++i) {
            int issue_node = 1 + i;
            for (int dev_idx : compatibility_adj[i]) {
                int dev_node = 1 + N_issues + dev_idx;
                edges.push_back({{issue_node, dev_node}, 1});
            }
        }

        // 3. Developers -> Sink (capacity 1)
        for (int j = 0; j < M_devs; ++j) {
            int dev_node = 1 + N_issues + j;
            edges.push_back({{dev_node, sink}, 1});
        }

        FlowResult flow_res = EdmondsKarpWorkbench::compute_max_flow(V, source, sink, edges);
        result.max_matched = flow_res.max_flow;

        // Recover matched pairs where flow == 1 between issues and developers
        for (const auto& e : flow_res.residual_edges) {
            if (e.flow == 1 && e.u >= 1 && e.u <= N_issues &&
                e.v >= 1 + N_issues && e.v < sink) {
                int issue_idx = e.u - 1;
                int dev_idx = e.v - (1 + N_issues);
                result.issue_dev_pairs.push_back({issue_idx, dev_idx});
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
