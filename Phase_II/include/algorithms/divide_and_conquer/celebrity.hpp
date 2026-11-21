#pragma once

#include <vector>
#include <chrono>
#include <iostream>

struct CelebrityResult {
    int candidate_id = -1;
    bool exists = false;
    int comparisons = 0;
    double elapsed_microseconds = 0.0;
};

class CelebrityWorkbench {
public:
    using ReviewMatrix = std::vector<std::vector<int>>;

    // Query function: Does developer A request code review / PR approval from developer B?
    static bool requests_review(const ReviewMatrix& M, int a, int b, int& comps) {
        comps++;
        return M[a][b] == 1;
    }

    // ------------------------------------------------------------------------
    // 1. Two-Pointer Elimination Algorithm: O(n) Comparisons, O(1) Aux Space
    // ------------------------------------------------------------------------
    static CelebrityResult find_core_maintainer_linear(const ReviewMatrix& M) {
        CelebrityResult res;
        int n = static_cast<int>(M.size());
        if (n == 0) return res;

        int comps = 0;
        auto start = std::chrono::high_resolution_clock::now();

        // Step 1: Elimination phase (n - 1 comparisons)
        int i = 0;
        int j = n - 1;
        while (i < j) {
            if (requests_review(M, i, j, comps)) {
                // If i requests review from j, i cannot be the core maintainer (bottleneck)
                i++;
            } else {
                // If i does not request review from j, j cannot be the core maintainer
                j--;
            }
        }

        int candidate = i;

        // Step 2: Verification phase (2 * (n - 1) comparisons)
        bool is_celebrity = true;
        for (int k = 0; k < n; ++k) {
            if (k != candidate) {
                // Core maintainer must NOT request review from anyone (out-degree = 0)
                // Everyone else MUST request review from the core maintainer (in-degree = n-1)
                if (requests_review(M, candidate, k, comps) || !requests_review(M, k, candidate, comps)) {
                    is_celebrity = false;
                    break;
                }
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        res.candidate_id = is_celebrity ? candidate : -1;
        res.exists = is_celebrity;
        res.comparisons = comps;
        res.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return res;
    }

    // ------------------------------------------------------------------------
    // 2. Brute Force Comparison Algorithm: O(n^2) Comparisons
    // ------------------------------------------------------------------------
    static CelebrityResult find_core_maintainer_bruteforce(const ReviewMatrix& M) {
        CelebrityResult res;
        int n = static_cast<int>(M.size());
        if (n == 0) return res;

        int comps = 0;
        auto start = std::chrono::high_resolution_clock::now();

        int celebrity = -1;
        for (int i = 0; i < n; ++i) {
            bool valid = true;
            for (int j = 0; j < n; ++j) {
                if (i != j) {
                    if (requests_review(M, i, j, comps) || !requests_review(M, j, i, comps)) {
                        valid = false;
                        break;
                    }
                }
            }
            if (valid) {
                celebrity = i;
                break;
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        res.candidate_id = celebrity;
        res.exists = (celebrity != -1);
        res.comparisons = comps;
        res.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return res;
    }
};
