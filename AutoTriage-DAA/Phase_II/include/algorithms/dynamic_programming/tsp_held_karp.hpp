#pragma once

#include <vector>
#include <chrono>
#include <limits>
#include <algorithm>

struct TSPResult {
    double min_tour_cost = 1e18;
    std::vector<int> tour;
    double elapsed_microseconds = 0.0;
};

class TSPHeldKarpWorkbench {
public:
    // ------------------------------------------------------------------------
    // TSP Held-Karp Dynamic Programming: Theta(n^2 * 2^n) time, Theta(n * 2^n) space
    // Finds exact minimum cost tour across tightly coupled microservices
    // ------------------------------------------------------------------------
    static TSPResult solve(const std::vector<std::vector<double>>& dist) {
        TSPResult result;
        int n = static_cast<int>(dist.size());
        if (n <= 1) return result;

        auto start = std::chrono::high_resolution_clock::now();

        int num_subsets = 1 << n; // 2^n
        const double INF = 1e18;

        // dp[mask][u] = min cost to visit subset `mask` starting at 0 and ending at `u`
        std::vector<std::vector<double>> dp(num_subsets, std::vector<double>(n, INF));
        // parent[mask][u] = previous vertex on optimal path
        std::vector<std::vector<int>> parent(num_subsets, std::vector<int>(n, -1));

        // Base case: starting at vertex 0
        dp[1][0] = 0.0;

        // Iterate over all subset masks
        for (int mask = 1; mask < num_subsets; ++mask) {
            // Must contain starting vertex 0
            if (!(mask & 1)) continue;

            for (int u = 0; u < n; ++u) {
                if (!(mask & (1 << u))) continue;
                if (dp[mask][u] >= INF) continue;

                // Try transitioning to unvisited neighbor v
                for (int v = 0; v < n; ++v) {
                    if (!(mask & (1 << v))) {
                        int next_mask = mask | (1 << v);
                        double new_cost = dp[mask][u] + dist[u][v];
                        if (new_cost < dp[next_mask][v]) {
                            dp[next_mask][v] = new_cost;
                            parent[next_mask][v] = u;
                        }
                    }
                }
            }
        }

        // Return to starting vertex 0 from all full subsets
        int full_mask = (1 << n) - 1;
        int last_node = -1;
        for (int u = 1; u < n; ++u) {
            if (dp[full_mask][u] + dist[u][0] < result.min_tour_cost) {
                result.min_tour_cost = dp[full_mask][u] + dist[u][0];
                last_node = u;
            }
        }

        // Reconstruct optimal tour
        if (last_node != -1) {
            int curr_mask = full_mask;
            int curr_node = last_node;
            std::vector<int> rev_tour;
            rev_tour.push_back(0); // return to start

            while (curr_node != -1) {
                rev_tour.push_back(curr_node);
                int prev = parent[curr_mask][curr_node];
                curr_mask ^= (1 << curr_node);
                curr_node = prev;
            }
            std::reverse(rev_tour.begin(), rev_tour.end());
            result.tour = rev_tour;
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
