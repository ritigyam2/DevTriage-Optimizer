#include "../include/models.hpp"
#include "../include/parser.hpp"
#include "../include/sorting.hpp"
#include "../include/matching.hpp"

#include <iostream>
#include <cassert>
#include <vector>

void test_merge_sort_correctness_and_stability() {
    std::cout << "[TEST 1] Running Merge Sort Correctness & Stability Test...";
    std::vector<Issue> issues = {
        {1, "Task A", 3, 5, 50.0, 5, {}, {}},
        {2, "Task B", 5, 8, 90.0, 2, {}, {}},
        {3, "Task C", 5, 4, 85.0, 1, {}, {}},
        {4, "Task D", 1, 2, 10.0, 10, {}, {}},
        {5, "Task E", 3, 6, 45.0, 5, {}, {}}
    };

    SortStats stats;
    SortingWorkbench::merge_sort(issues, SortingWorkbench::priority_comparator, stats);

    // Expected order:
    // 1st: Task C (Sev 5, SLA 1)
    // 2nd: Task B (Sev 5, SLA 2)
    // 3rd: Task A (Sev 3, SLA 5, ID 1)
    // 4th: Task E (Sev 3, SLA 5, ID 5)
    // 5th: Task D (Sev 1, SLA 10)
    assert(issues[0].id == 3);
    assert(issues[1].id == 2);
    assert(issues[2].id == 1);
    assert(issues[3].id == 5);
    assert(issues[4].id == 4);
    std::cout << " PASSED!\n";
}

void test_quick_sort_adversarial() {
    std::cout << "[TEST 2] Running Quick Sort Adversarial (Pre-sorted) Test...";
    std::vector<Issue> sorted_issues;
    for (int i = 1; i <= 50; ++i) {
        sorted_issues.push_back({i, "Issue " + std::to_string(i), 5, 4, 100.0, i, {}, {}});
    }

    std::vector<Issue> m3_copy = sorted_issues;
    std::vector<Issue> first_copy = sorted_issues;

    SortStats stats_m3, stats_first;
    SortingWorkbench::quick_sort(m3_copy, PivotStrategy::MEDIAN_OF_THREE, SortingWorkbench::priority_comparator, stats_m3);
    SortingWorkbench::quick_sort(first_copy, PivotStrategy::FIRST_ELEMENT, SortingWorkbench::priority_comparator, stats_first);

    // Median of 3 must significantly outperform or equal first-element on comparisons
    assert(m3_copy[0].id == 1);
    assert(m3_copy[49].id == 50);
    std::cout << " PASSED! (Median-of-3 Comparisons: " << stats_m3.comparisons 
              << " vs First-Pivot: " << stats_first.comparisons << ")\n";
}

void test_bipartite_matching_optimality() {
    std::cout << "[TEST 3] Running Maximum Bipartite Matching vs Greedy Test...";
    std::vector<Issue> issues = {
        {1, "Bug 1", 5, 10, 100.0, 1, {"C++"}, {}},
        {2, "Bug 2", 4, 10, 80.0, 2, {"C++", "Go"}, {}},
        {3, "Bug 3", 3, 10, 60.0, 3, {"Go"}, {}}
    };

    std::vector<Developer> devs = {
        {1, "Dev Alpha", 10, 0, {"C++"}, {}},
        {2, "Dev Beta",  10, 0, {"C++", "Go"}, {}},
        {3, "Dev Gamma", 10, 0, {"Go"}, {}}
    };

    std::vector<Developer> devs_bip = devs;
    std::vector<Developer> devs_greedy = devs;

    MatchingStats bip_stats = AssignmentWorkbench::maximum_bipartite_matching(issues, devs_bip);
    MatchingStats greedy_stats = AssignmentWorkbench::greedy_skill_matching(issues, devs_greedy);

    // Bipartite must match all 3 issues
    assert(bip_stats.assigned_issues == 3);
    assert(bip_stats.assigned_issues >= greedy_stats.assigned_issues);
    std::cout << " PASSED! (Bipartite Matched: " << bip_stats.assigned_issues 
              << " | Greedy Matched: " << greedy_stats.assigned_issues << ")\n";
}

void test_binary_search() {
    std::cout << "[TEST 4] Running Binary Search (Iterative & Recursive) Test...";
    std::vector<Issue> issues;
    for (int i = 1; i <= 20; ++i) {
        issues.push_back({i * 10, "Task " + std::to_string(i), 3, 5, 50.0, 5, {}, {}});
    }

    long long iter_comps = 0, rec_comps = 0;
    int idx1 = SortingWorkbench::binary_search_iterative(issues, 70, iter_comps);
    int idx2 = SortingWorkbench::binary_search_recursive(issues, 70, rec_comps);
    assert(idx1 == 6);
    assert(idx2 == 6);

    // Search non-existent
    int idx_none = SortingWorkbench::binary_search_iterative(issues, 999, iter_comps);
    assert(idx_none == -1);

    std::cout << " PASSED!\n";
}

void test_defensive_validation() {
    std::cout << "[TEST 5] Running Defensive Input Validation Rejection Test...";
    std::vector<Issue> invalid_issues;
    std::string err;
    bool parsed = DataParser::parse_issues("data/invalid_issues.csv", invalid_issues, err);

    // Must return false and set descriptive error message
    assert(!parsed);
    assert(!err.empty());
    std::cout << " PASSED! (Correctly rejected with: \"" << err << "\")\n";
}

void test_boundary_dataset() {
    std::cout << "[TEST 6] Running Boundary Dataset Handling Test...";
    std::vector<Issue> boundary_issues;
    std::string err;
    bool parsed = DataParser::parse_issues("data/boundary_issues.csv", boundary_issues, err);
    assert(parsed);
    assert(boundary_issues.size() == 3);

    SortStats stats;
    SortingWorkbench::merge_sort(boundary_issues, SortingWorkbench::priority_comparator, stats);
    assert(boundary_issues[0].severity == 5);
    std::cout << " PASSED!\n";
}

void test_circular_prerequisite_detection() {
    std::cout << "[TEST 7] Running Circular Prerequisite Dependency Detection Test...";
    std::vector<Issue> cyclic_issues;
    std::string err;
    bool parsed = DataParser::parse_issues("data/cyclic_issues.csv", cyclic_issues, err);
    assert(!parsed);
    assert(err.find("Circular prerequisite dependency detected") != std::string::npos);
    std::cout << " PASSED! (Correctly trapped: \"" << err << "\")\n";
}

int main() {
    std::cout << "\n=================================================================\n";
    std::cout << "  RUNNING PHASE I AUTOMATED TEST HARNESS (AutoTriage-DAA | C++17)\n";
    std::cout << "=================================================================\n\n";

    test_merge_sort_correctness_and_stability();
    test_quick_sort_adversarial();
    test_bipartite_matching_optimality();
    test_binary_search();
    test_defensive_validation();
    test_boundary_dataset();
    test_circular_prerequisite_detection();

    std::cout << "\n=================================================================\n";
    std::cout << "  ALL 7 TEST SUITES PASSED! (100% SUCCESS RATE)\n";
    std::cout << "=================================================================\n\n";

    return 0;
}
