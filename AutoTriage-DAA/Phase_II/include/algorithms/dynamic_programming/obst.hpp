#pragma once

#include <vector>
#include <string>
#include <limits>
#include <chrono>

struct OBSTResult {
    double expected_cost = 0.0;
    std::vector<std::vector<int>> root_table;
    double elapsed_microseconds = 0.0;
};

class OBSTWorkbench {
public:
    // ------------------------------------------------------------------------
    // Optimal Binary Search Tree: Theta(n^3) time, Theta(n^2) aux space
    // Minimizes expected search cost for skewed triage tag access frequencies
    // ------------------------------------------------------------------------
    static OBSTResult solve(const std::vector<std::string>& keys,
                            const std::vector<double>& p,
                            const std::vector<double>& q) {
        OBSTResult result;
        int n = static_cast<int>(keys.size());
        if (n <= 0) return result;

        auto start = std::chrono::high_resolution_clock::now();

        // e[i][j]: expected cost of searching OBST with keys k_i..k_j (1-indexed)
        // w[i][j]: sum of probabilities for subtree
        // root[i][j]: index of optimal root
        std::vector<std::vector<double>> e(n + 2, std::vector<double>(n + 2, 0.0));
        std::vector<std::vector<double>> w(n + 2, std::vector<double>(n + 2, 0.0));
        std::vector<std::vector<int>> root(n + 1, std::vector<int>(n + 1, 0));

        // Base cases: empty subtrees with dummy keys
        for (int i = 1; i <= n + 1; ++i) {
            e[i][i - 1] = q[i - 1];
            w[i][i - 1] = q[i - 1];
        }

        // l is subtree size: 1 to n
        for (int l = 1; l <= n; ++l) {
            for (int i = 1; i <= n - l + 1; ++i) {
                int j = i + l - 1;
                e[i][j] = std::numeric_limits<double>::infinity();
                w[i][j] = w[i][j - 1] + p[j - 1] + q[j];

                for (int r = i; r <= j; ++r) {
                    double t = e[i][r - 1] + e[r + 1][j] + w[i][j];
                    if (t < e[i][j]) {
                        e[i][j] = t;
                        root[i][j] = r;
                    }
                }
            }
        }

        result.expected_cost = e[1][n];
        result.root_table = root;

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
