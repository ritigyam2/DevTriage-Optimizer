#include "../include/algorithms/divide_and_conquer/strassen.hpp"
#include "../include/algorithms/divide_and_conquer/max_subarray.hpp"
#include "../include/algorithms/divide_and_conquer/fast_power.hpp"
#include "../include/algorithms/divide_and_conquer/celebrity.hpp"

#include <iostream>
#include <cassert>
#include <vector>
#include <cmath>

void test_strassen_matrix_multiplication() {
    std::cout << "[TEST 1] Running Strassen vs Classical Matrix Multiplication Test...";

    // 4x4 Test Matrices
    StrassenWorkbench::Matrix A = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 1, 2, 3},
        {4, 5, 6, 7}
    };

    StrassenWorkbench::Matrix B = {
        {2, 0, 1, 2},
        {1, 3, 2, 1},
        {0, 1, 3, 2},
        {3, 2, 1, 0}
    };

    StrassenWorkbench::MatrixStats stats_classic, stats_strassen;
    auto C_classic = StrassenWorkbench::classical_multiply(A, B, stats_classic);
    auto C_strassen = StrassenWorkbench::strassen_multiply(A, B, stats_strassen, 2);

    // Verify mathematical equivalence
    for (size_t i = 0; i < A.size(); ++i) {
        for (size_t j = 0; j < A[0].size(); ++j) {
            assert(C_classic[i][j] == C_strassen[i][j]);
        }
    }

    // Verify developer co-maintenance calculation (3 developers x 4 modules)
    StrassenWorkbench::Matrix dev_modules = {
        {5, 2, 0, 1}, // Dev 0 commits
        {1, 0, 4, 3}, // Dev 1 commits
        {4, 2, 1, 0}  // Dev 2 commits
    };
    StrassenWorkbench::MatrixStats stats_co;
    auto co_maint = StrassenWorkbench::compute_developer_co_maintenance(dev_modules, stats_co, true);
    assert(co_maint.size() == 3);
    assert(co_maint[0][0] > 0); // Self-intensity

    std::cout << " PASSED! (Strassen matches Classical exactly)\n";
}

void test_maximum_subarray() {
    std::cout << "[TEST 2] Running Maximum Subarray (D&C vs Kadane) Test...";

    // Net daily issue churn: positive = bug surge, negative = bug resolution surplus
    std::vector<int> churn = {-2, 1, -3, 4, -1, 2, 1, -5, 4};

    SubarrayResult res_dnc = MaxSubarrayWorkbench::divide_and_conquer(churn);
    SubarrayResult res_kadane = MaxSubarrayWorkbench::kadane_linear(churn);

    // Max contiguous sum is 4 + (-1) + 2 + 1 = 6 from index 3 to 6
    assert(res_dnc.max_sum == 6);
    assert(res_kadane.max_sum == 6);
    assert(res_dnc.start_index == 3 && res_dnc.end_index == 6);
    assert(res_kadane.start_index == 3 && res_kadane.end_index == 6);

    // All negative case
    std::vector<int> all_neg = {-7, -3, -5, -2, -8};
    SubarrayResult res_neg_dnc = MaxSubarrayWorkbench::divide_and_conquer(all_neg);
    SubarrayResult res_neg_kad = MaxSubarrayWorkbench::kadane_linear(all_neg);
    assert(res_neg_dnc.max_sum == -2);
    assert(res_neg_kad.max_sum == -2);

    std::cout << " PASSED! (D&C and Kadane yield identical max sum: " << res_dnc.max_sum << ")\n";
}

void test_fast_power_and_markov() {
    std::cout << "[TEST 3] Running Fast Exponentiation & Markov Lifecycle Test...";

    FastPowerWorkbench::PowerStats stats_scalar, stats_matrix;

    // Scalar test: 3^13 mod 1000 = 1594323 mod 1000 = 323
    long long p_scalar = FastPowerWorkbench::power_scalar(3, 13, 1000, stats_scalar);
    assert(p_scalar == 323);
    // Number of multiplications should be <= 2 * log2(13) = 8
    assert(stats_scalar.multiplications <= 10);

    // Markov 4x4 State Transition Matrix:
    // States: 0=TRIAGE, 1=DEVELOPMENT, 2=REVIEW, 3=RESOLVED
    FastPowerWorkbench::Matrix P = {
        {0.2, 0.6, 0.1, 0.1}, // From Triage
        {0.0, 0.3, 0.5, 0.2}, // From Development
        {0.0, 0.1, 0.2, 0.7}, // From Review
        {0.0, 0.0, 0.0, 1.0}  // Resolved (Absorbing State)
    };

    std::vector<double> initial_issues = {100.0, 0.0, 0.0, 0.0}; // 100 fresh issues
    std::vector<double> predicted_sprint_4 = FastPowerWorkbench::predict_issue_lifecycle(P, 4, initial_issues, stats_matrix);

    // Total issues must remain 100.0 (probability conservation)
    double total = 0.0;
    for (double val : predicted_sprint_4) total += val;
    assert(std::fabs(total - 100.0) < 1e-4);
    assert(predicted_sprint_4[3] > 0.0); // Some issues resolved

    std::cout << " PASSED! (Conservation holds: " << total << " issues; " 
              << predicted_sprint_4[3] << " resolved by Sprint 4)\n";
}

void test_celebrity_problem() {
    std::cout << "[TEST 4] Running Celebrity Problem (Core Maintainer) Test...";

    // 5 engineers. Engineer #2 is the Core Maintainer (reviewed by everyone, reviews no one)
    CelebrityWorkbench::ReviewMatrix M = {
        {0, 1, 1, 0, 0}, // Dev 0 reviews Dev 1 and Dev 2
        {0, 0, 1, 1, 0}, // Dev 1 reviews Dev 2 and Dev 3
        {0, 0, 0, 0, 0}, // Dev 2 (Core Maintainer) requests review from NO ONE
        {1, 0, 1, 0, 1}, // Dev 3 reviews Dev 0, Dev 2, Dev 4
        {0, 1, 1, 0, 0}  // Dev 4 reviews Dev 1 and Dev 2
    };

    CelebrityResult res_linear = CelebrityWorkbench::find_core_maintainer_linear(M);
    CelebrityResult res_brute = CelebrityWorkbench::find_core_maintainer_bruteforce(M);

    assert(res_linear.exists && res_linear.candidate_id == 2);
    assert(res_brute.exists && res_brute.candidate_id == 2);

    // In a 5-person graph, linear algorithm must take at most 3*(5-1) = 12 comparisons
    assert(res_linear.comparisons <= 12);

    // Negative case: Modify M so Dev 2 reviews Dev 0 (no celebrity)
    M[2][0] = 1;
    CelebrityResult res_none = CelebrityWorkbench::find_core_maintainer_linear(M);
    assert(!res_none.exists);

    std::cout << " PASSED! (Core Maintainer identified as Dev #" << res_linear.candidate_id 
              << " in " << res_linear.comparisons << " comparisons)\n";
}

int main() {
    std::cout << "\n=================================================================\n";
    std::cout << "  RUNNING CHUNK 2 AUTOMATED TEST SUITE (Divide & Conquer Workbench)\n";
    std::cout << "=================================================================\n\n";

    test_strassen_matrix_multiplication();
    test_maximum_subarray();
    test_fast_power_and_markov();
    test_celebrity_problem();

    std::cout << "\n=================================================================\n";
    std::cout << "  ALL CHUNK 2 TESTS PASSED FLAWLESSLY! (100% SUCCESS RATE)\n";
    std::cout << "=================================================================\n\n";
    return 0;
}
