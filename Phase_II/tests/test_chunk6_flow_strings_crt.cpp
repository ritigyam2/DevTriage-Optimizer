#include "../include/algorithms/flow_matching/ford_fulkerson.hpp"
#include "../include/algorithms/flow_matching/bipartite_matching.hpp"
#include "../include/algorithms/number_theory/crt.hpp"
#include "../include/algorithms/string_matching/string_matchers.hpp"
#include "../include/core/complexity_reductions.hpp"

#include <iostream>
#include <cassert>
#include <vector>
#include <string>

void test_edmonds_karp_max_flow() {
    std::cout << "[TEST 1] Running Edmonds-Karp Max Flow Test...";

    // 4-node flow network: source = 0, sink = 3
    int V = 4;
    std::vector<std::pair<std::pair<int, int>, int>> edges = {
        {{0, 1}, 10},
        {{0, 2}, 10},
        {{1, 2}, 1},
        {{1, 3}, 9},
        {{2, 3}, 10}
    };

    FlowResult res = EdmondsKarpWorkbench::compute_max_flow(V, 0, 3, edges);

    // Max flow: 0->1 sends 9 (to 3) + 1 (to 2->3), 0->2 sends 9 (to 3) => Total = 19
    assert(res.max_flow == 19);
    assert(res.augmenting_paths_found > 0);

    std::cout << " PASSED! (Max Flow: " << res.max_flow 
              << " | Augmenting Paths: " << res.augmenting_paths_found << ")\n";
}

void test_bipartite_matching_via_flow() {
    std::cout << "[TEST 2] Running Maximum Bipartite Matching via Flow Test...";

    // 3 issues, 3 developers
    int N_issues = 3;
    int M_devs = 3;
    std::vector<std::vector<int>> compat = {
        {0, 1},    // Issue 0 compatible with Dev 0, Dev 1
        {0, 1, 2}, // Issue 1 compatible with Dev 0, Dev 1, Dev 2
        {1, 2}     // Issue 2 compatible with Dev 1, Dev 2
    };

    BipartiteAssignmentResult res = BipartiteFlowWorkbench::solve(N_issues, M_devs, compat);

    // Max matching is 3
    assert(res.max_matched == 3);
    assert(res.issue_dev_pairs.size() == 3);

    std::cout << " PASSED! (Matched " << res.max_matched << " / " << N_issues << " issues via flow)\n";
}

void test_chinese_remainder_theorem() {
    std::cout << "[TEST 3] Running Chinese Remainder Theorem (CRT) Test...";

    // System:
    // x = 2 (mod 3)
    // x = 3 (mod 5)
    // x = 2 (mod 7)
    std::vector<long long> remainders = {2, 3, 2};
    std::vector<long long> moduli = {3, 5, 7};

    CRTResult res = ChineseRemainderTheoremWorkbench::solve(remainders, moduli);

    assert(res.is_valid);
    assert(res.combined_modulus == 105);
    assert(res.solution == 23);

    // Verify congruence
    assert(res.solution % 3 == 2);
    assert(res.solution % 5 == 3);
    assert(res.solution % 7 == 2);

    std::cout << " PASSED! (x = " << res.solution 
              << " mod " << res.combined_modulus << " solves system perfectly)\n";
}

void test_four_way_string_matching() {
    std::cout << "[TEST 4] Running 4-Way String Matchers Benchmark (Naive, RK, FA, KMP)...";

    std::string text = "CVE-2026-1049 CRITICAL_BUFFER_OVERFLOW IN KERNEL MEMORY DRIVER CVE-2026-1049";
    std::string pattern = "CVE-2026-1049";

    StringMatchResult res_naive = StringMatchingWorkbench::naive_search(text, pattern);
    StringMatchResult res_rk    = StringMatchingWorkbench::rabin_karp_search(text, pattern);
    StringMatchResult res_fa    = StringMatchingWorkbench::finite_automata_search(text, pattern);
    StringMatchResult res_kmp   = StringMatchingWorkbench::kmp_search(text, pattern);

    // Matches at index 0 and index 63
    assert(res_naive.match_indices.size() == 2);
    assert(res_naive.match_indices[0] == 0 && res_naive.match_indices[1] == 63);

    // All 4 algorithms MUST find the identical matches!
    assert(res_rk.match_indices == res_naive.match_indices);
    assert(res_fa.match_indices == res_naive.match_indices);
    assert(res_kmp.match_indices == res_naive.match_indices);

    std::cout << " PASSED! (All 4 algorithms found identical matches at indices 0 and 63)\n";
    std::cout << "         [Naive] Comparisons: " << res_naive.comparisons << "\n";
    std::cout << "         [KMP]   Comparisons: " << res_kmp.comparisons << "\n";
}

void test_complexity_reductions() {
    std::cout << "[TEST 5] Running Complexity Reduction Verifier (Subset-Sum <=_P 0/1 Knapsack)...";

    // YES Instance: S = {3, 34, 4, 12, 5, 2}, Target = 9 (4 + 5 = 9)
    std::vector<int> S_yes = {3, 34, 4, 12, 5, 2};
    ReductionProofResult res_yes = ComplexityReductionWorkbench::verify_subset_sum_to_knapsack_reduction(S_yes, 9);
    assert(res_yes.subset_sum_has_solution == true);
    assert(res_yes.knapsack_has_solution == true);
    assert(res_yes.reduction_holds == true);

    // NO Instance: S = {3, 34, 4, 12, 5, 2}, Target = 100 (Total sum is 60, so 100 is impossible)
    ReductionProofResult res_no = ComplexityReductionWorkbench::verify_subset_sum_to_knapsack_reduction(S_yes, 100);
    assert(res_no.subset_sum_has_solution == false);
    assert(res_no.knapsack_has_solution == false);
    assert(res_no.reduction_holds == true);

    std::cout << " PASSED! (Reduction verified bidirectionally for YES and NO instances)\n";
}

int main() {
    std::cout << "\n=================================================================\n";
    std::cout << "  RUNNING CHUNK 6 AUTOMATED TEST SUITE (Flow, Strings, CRT, Reductions)\n";
    std::cout << "=================================================================\n\n";

    test_edmonds_karp_max_flow();
    test_bipartite_matching_via_flow();
    test_chinese_remainder_theorem();
    test_four_way_string_matching();
    test_complexity_reductions();

    std::cout << "\n=================================================================\n";
    std::cout << "  ALL CHUNK 6 TESTS PASSED FLAWLESSLY! (100% SUCCESS RATE)\n";
    std::cout << "=================================================================\n\n";
    return 0;
}
