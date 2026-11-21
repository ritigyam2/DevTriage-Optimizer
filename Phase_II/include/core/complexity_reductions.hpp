#pragma once

#include <vector>
#include <string>
#include <iostream>

struct ReductionProofResult {
    bool subset_sum_has_solution = false;
    bool knapsack_has_solution = false;
    bool reduction_holds = false;
    std::string reduction_proof_log;
};

class ComplexityReductionWorkbench {
public:
    // ------------------------------------------------------------------------
    // Formal Polynomial-Time Reduction: Subset-Sum <=_P 0/1 Knapsack
    // Proves that 0/1 Knapsack is NP-Complete by reducing known NP-Complete Subset-Sum
    // ------------------------------------------------------------------------
    static ReductionProofResult verify_subset_sum_to_knapsack_reduction(
        const std::vector<int>& S, int Target) {
        ReductionProofResult result;

        // Step 1: Polynomial-time transformation (takes O(n) time)
        // For each x_i in S: construct knapsack item with weight w_i = x_i and value v_i = x_i
        // Set capacity W = Target, value threshold K = Target
        int n = static_cast<int>(S.size());
        std::vector<int> weights = S;
        std::vector<double> values;
        for (int x : S) values.push_back(static_cast<double>(x));
        int capacity = Target;
        double threshold = static_cast<double>(Target);

        result.reduction_proof_log += "1. Transformation constructed in O(n) time:\n";
        result.reduction_proof_log += "   Constructed " + std::to_string(n) + " items with w_i = v_i = x_i. W = K = " + std::to_string(Target) + "\n";
        result.reduction_proof_log += "   [THEORETICAL NOTE] The reduction mapping itself is strictly O(n) polynomial time.\n";
        result.reduction_proof_log += "   The testbed below independently verifies equivalence using O(nW) DP and O(2^n) subset enumeration on small test instances.\n";

        // Step 2: Solve 0/1 Knapsack on transformed instance
        // dp[w] stores max value for capacity w
        std::vector<double> dp(capacity + 1, 0.0);
        for (int i = 0; i < n; ++i) {
            for (int w = capacity; w >= weights[i]; --w) {
                dp[w] = std::max(dp[w], dp[w - weights[i]] + values[i]);
            }
        }

        double max_val = dp[capacity];
        result.knapsack_has_solution = (max_val >= threshold);

        // Step 3: Solve Subset-Sum directly via brute-force verification to check bidirectional equivalence
        bool subset_sum_found = false;
        int total_subsets = 1 << n;
        for (int mask = 0; mask < total_subsets; ++mask) {
            int sum = 0;
            for (int i = 0; i < n; ++i) {
                if (mask & (1 << i)) {
                    sum += S[i];
                }
            }
            if (sum == Target) {
                subset_sum_found = true;
                break;
            }
        }
        result.subset_sum_has_solution = subset_sum_found;

        // Step 4: Verify Equivalence (YES iff YES, NO iff NO)
        result.reduction_holds = (result.subset_sum_has_solution == result.knapsack_has_solution);

        result.reduction_proof_log += "2. Bidirectional Equivalence Check:\n";
        result.reduction_proof_log += "   Subset-Sum instance YES? " + std::string(result.subset_sum_has_solution ? "YES" : "NO") + "\n";
        result.reduction_proof_log += "   Transformed Knapsack instance YES? " + std::string(result.knapsack_has_solution ? "YES" : "NO") + "\n";
        result.reduction_proof_log += "   Reduction Preserves Decision: " + std::string(result.reduction_holds ? "VALID" : "INVALID") + "\n";

        return result;
    }
};
