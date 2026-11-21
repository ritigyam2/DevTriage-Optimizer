#include "../include/models.hpp"
#include "../include/parser.hpp"
#include "../include/sorting.hpp"
#include "../include/matching.hpp"

#include <iostream>
#include <iomanip>
#include <vector>
#include <string>

void print_banner() {
    std::cout << "\n===============================================================================\n";
    std::cout << "  AutoTriage-DAA\n";
    std::cout << "  Open Source Issue Triage and Developer Assignment Tool\n\n";
    std::cout << "  Design and Analysis of Algorithms -- PBL (Project 50)\n";
    std::cout << "  Developed by: Ritigya Mishra | SAP ID: 590028115 | Batch: B-9 (AI/ML)\n";
    std::cout << "  Course: B.Tech-CSE\n";
    std::cout << "===============================================================================\n\n";
}

void print_issues_table(const std::vector<Issue>& issues) {
    std::cout << "\n--------------------------------------------------------------------------------------------------\n";
    std::cout << std::left 
              << std::setw(5)  << "ID"
              << std::setw(38) << "Issue Title"
              << std::setw(6)  << "Sev"
              << std::setw(8)  << "Hours"
              << std::setw(8)  << "Value"
              << std::setw(6)  << "SLA"
              << "Required Skills\n";
    std::cout << "--------------------------------------------------------------------------------------------------\n";
    for (const auto& it : issues) {
        std::string skill_str;
        for (size_t s = 0; s < it.skills.size(); ++s) {
            skill_str += it.skills[s] + (s + 1 < it.skills.size() ? "; " : "");
        }
        std::cout << std::left 
                  << std::setw(5)  << it.id
                  << std::setw(38) << (it.title.length() > 36 ? it.title.substr(0, 33) + "..." : it.title)
                  << std::setw(6)  << it.severity
                  << std::setw(8)  << it.estimated_hours
                  << std::setw(8)  << it.business_value
                  << std::setw(6)  << it.deadline_day
                  << skill_str << "\n";
    }
    std::cout << "--------------------------------------------------------------------------------------------------\n";
    std::cout << "Total Issues: " << issues.size() << "\n\n";
}

void print_developers_table(const std::vector<Developer>& devs) {
    std::cout << "\n--------------------------------------------------------------------------------------------------\n";
    std::cout << std::left 
              << std::setw(5)  << "ID"
              << std::setw(25) << "Developer Name"
              << std::setw(12) << "Avail Hours"
              << std::setw(12) << "Alloc Hours"
              << "Verified Skillset\n";
    std::cout << "--------------------------------------------------------------------------------------------------\n";
    for (const auto& d : devs) {
        std::string skill_str;
        for (size_t s = 0; s < d.skills.size(); ++s) {
            skill_str += d.skills[s] + (s + 1 < d.skills.size() ? "; " : "");
        }
        std::cout << std::left 
                  << std::setw(5)  << d.id
                  << std::setw(25) << d.name
                  << std::setw(12) << d.available_hours
                  << std::setw(12) << d.assigned_hours
                  << skill_str << "\n";
    }
    std::cout << "--------------------------------------------------------------------------------------------------\n\n";
}

int main() {
    print_banner();

    std::vector<Issue> current_issues;
    std::vector<Developer> current_devs;
    std::string err;

    std::string default_issues_path = "data/normal_issues.csv";
    std::string default_devs_path = "data/normal_developers.csv";

    // Auto-load default dataset
    if (DataParser::parse_issues(default_issues_path, current_issues, err) &&
        DataParser::parse_developers(default_devs_path, current_devs, err)) {
        std::cout << "[INIT] Successfully loaded default normal datasets: "
                  << current_issues.size() << " issues, " << current_devs.size() << " developers.\n";
    } else {
        std::cout << "[WARN] " << err << "\n";
    }

    int choice = 0;
    while (true) {
        std::cout << "\n============================== MAIN MENU ==============================\n";
        std::cout << " 1. Display Current Backlog & Developer Roster\n";
        std::cout << " 2. Benchmark Sorting: Merge Sort vs Quick Sort (Median-3 vs First)\n";
        std::cout << " 3. Benchmark Assignment: Maximum Bipartite Matching vs Greedy\n";
        std::cout << " 4. Fast Retrieval: Binary Search by Issue ID (Iterative vs Recursive)\n";
        std::cout << " 5. Load Alternate Dataset (Boundary / Invalid / Custom CSV)\n";
        std::cout << " 6. Live Invariant & Algorithm Step-by-Step Diagnostic Trace\n";
        std::cout << " 7. Exit\n";
        std::cout << "=======================================================================\n";
        std::cout << "Enter your choice (1-7): ";

        if (!(std::cin >> choice)) {
            std::cin.clear();
            std::string discard;
            std::cin >> discard;
            continue;
        }

        if (choice == 1) {
            print_issues_table(current_issues);
            print_developers_table(current_devs);
        } else if (choice == 2) {
            std::cout << "\n>>> BENCHMARKING MULTI-KEY SORTING ALGORITHMS <<<\n";
            std::cout << "Comparator: Severity (Desc) -> Deadline (Asc) -> ID (Asc)\n\n";

            std::vector<Issue> merge_data = current_issues;
            std::vector<Issue> quick_m3_data = current_issues;
            std::vector<Issue> quick_first_data = current_issues;

            SortStats merge_stats, quick_m3_stats, quick_first_stats;

            SortingWorkbench::merge_sort(merge_data, SortingWorkbench::priority_comparator, merge_stats);
            SortingWorkbench::quick_sort(quick_m3_data, PivotStrategy::MEDIAN_OF_THREE, SortingWorkbench::priority_comparator, quick_m3_stats);
            SortingWorkbench::quick_sort(quick_first_data, PivotStrategy::FIRST_ELEMENT, SortingWorkbench::priority_comparator, quick_first_stats);

            std::cout << "----------------------------------------------------------------------------------------------------\n";
            std::cout << std::left 
                      << std::setw(28) << "Sorting Algorithm"
                      << std::setw(16) << "Time (microsec)"
                      << std::setw(16) << "Comparisons"
                      << std::setw(16) << "Element Moves"
                      << "Stability\n";
            std::cout << "----------------------------------------------------------------------------------------------------\n";
            std::cout << std::left 
                      << std::setw(28) << "Merge Sort (Student)"
                      << std::setw(16) << merge_stats.elapsed_microseconds
                      << std::setw(16) << merge_stats.comparisons
                      << std::setw(16) << merge_stats.element_moves
                      << "STABLE (Guaranteed)\n";
            std::cout << std::left 
                      << std::setw(28) << "Quick Sort (Median-of-3)"
                      << std::setw(16) << quick_m3_stats.elapsed_microseconds
                      << std::setw(16) << quick_m3_stats.comparisons
                      << std::setw(16) << quick_m3_stats.element_moves
                      << "UNSTABLE (In-place)\n";
            std::cout << std::left 
                      << std::setw(28) << "Quick Sort (First Pivot)"
                      << std::setw(16) << quick_first_stats.elapsed_microseconds
                      << std::setw(16) << quick_first_stats.comparisons
                      << std::setw(16) << quick_first_stats.element_moves
                      << "UNSTABLE (In-place)\n";
            std::cout << "----------------------------------------------------------------------------------------------------\n\n";

            std::cout << "Top 5 Prioritized Issues Post Merge Sort:\n";
            for (size_t i = 0; i < std::min((size_t)5, merge_data.size()); ++i) {
                std::cout << "  #" << (i + 1) << " [ID " << merge_data[i].id << "] "
                          << "Sev=" << merge_data[i].severity 
                          << ", SLA=Day " << merge_data[i].deadline_day 
                          << " | " << merge_data[i].title << "\n";
            }
        } else if (choice == 3) {
            std::cout << "\n>>> BENCHMARKING DEVELOPER ASSIGNMENT ALGORITHMS <<<\n\n";

            // Prioritize first via Merge Sort
            std::vector<Issue> sorted_issues = current_issues;
            SortStats sort_stats;
            SortingWorkbench::merge_sort(sorted_issues, SortingWorkbench::priority_comparator, sort_stats);

            std::vector<Developer> devs_bipartite = current_devs;
            std::vector<Developer> devs_greedy = current_devs;

            MatchingStats bip_stats = AssignmentWorkbench::maximum_bipartite_matching(sorted_issues, devs_bipartite);
            MatchingStats greedy_stats = AssignmentWorkbench::greedy_skill_matching(sorted_issues, devs_greedy);

            std::cout << "----------------------------------------------------------------------------------------------------\n";
            std::cout << std::left 
                      << std::setw(30) << "Assignment Strategy"
                      << std::setw(14) << "Assigned"
                      << std::setw(14) << "Unassigned"
                      << std::setw(16) << "Match Rate (%)"
                      << std::setw(16) << "Hours Used"
                      << "Time (microsec)\n";
            std::cout << "----------------------------------------------------------------------------------------------------\n";
            std::cout << std::left 
                      << std::setw(30) << "Max Bipartite Matching"
                      << std::setw(14) << bip_stats.assigned_issues
                      << std::setw(14) << bip_stats.unassigned_issues
                      << std::setw(16) << bip_stats.assignment_rate_percent
                      << std::setw(16) << bip_stats.total_developer_hours_used
                      << bip_stats.elapsed_microseconds << "\n";
            std::cout << std::left 
                      << std::setw(30) << "Greedy Skill-First Matching"
                      << std::setw(14) << greedy_stats.assigned_issues
                      << std::setw(14) << greedy_stats.unassigned_issues
                      << std::setw(16) << greedy_stats.assignment_rate_percent
                      << std::setw(16) << greedy_stats.total_developer_hours_used
                      << greedy_stats.elapsed_microseconds << "\n";
            std::cout << "----------------------------------------------------------------------------------------------------\n\n";

            std::cout << "Detailed Developer Allocations (Max Bipartite Matching):\n";
            for (const auto& d : devs_bipartite) {
                std::cout << "  " << std::left << std::setw(25) << d.name 
                          << " [Capacity: " << d.assigned_hours << "/" << d.available_hours << " hrs] -> Assigned Issues: ";
                if (d.assigned_issue_ids.empty()) {
                    std::cout << "(None)\n";
                } else {
                    for (int iid : d.assigned_issue_ids) std::cout << "#" << iid << " ";
                    std::cout << "\n";
                }
            }
        } else if (choice == 4) {
            std::cout << "\n>>> BINARY SEARCH RETRIEVAL BENCHMARK <<<\n";
            // Sort by ID for binary search
            std::vector<Issue> id_sorted = current_issues;
            SortStats id_sort_stats;
            auto id_comp = [](const Issue& a, const Issue& b) { return a.id < b.id; };
            SortingWorkbench::merge_sort(id_sorted, id_comp, id_sort_stats);

            std::cout << "Backlog sorted by unique ID. Available IDs: ";
            for (const auto& it : id_sorted) std::cout << it.id << " ";
            std::cout << "\nEnter Target Issue ID to search: ";

            int target_id;
            if (std::cin >> target_id) {
                long long iter_comps = 0, rec_comps = 0;
                int idx_iter = SortingWorkbench::binary_search_iterative(id_sorted, target_id, iter_comps);
                int idx_rec = SortingWorkbench::binary_search_recursive(id_sorted, target_id, rec_comps);

                if (idx_iter >= 0 && idx_rec >= 0) {
                    std::cout << "\n[FOUND] Issue #" << target_id << " at index " << idx_iter << " (iterative) and " << idx_rec << " (recursive):\n"
                              << "  Title:    " << id_sorted[idx_iter].title << "\n"
                              << "  Severity: " << id_sorted[idx_iter].severity << " / 5\n"
                              << "  Effort:   " << id_sorted[idx_iter].estimated_hours << " hours\n"
                              << "  Value:    " << id_sorted[idx_iter].business_value << "\n";
                } else {
                    std::cout << "\n[NOT FOUND] Issue #" << target_id << " does not exist in the current backlog.\n";
                }
                std::cout << "Iterative Binary Search Comparisons: " << iter_comps << " (Aux Space: O(1))\n";
                std::cout << "Recursive Binary Search Comparisons: " << rec_comps << " (Aux Space: O(log n) stack)\n";
            }
        } else if (choice == 5) {
            std::cout << "\nSelect Dataset to Load:\n";
            std::cout << " 1. Normal Dataset (20 realistic issues, 8 devs)\n";
            std::cout << " 2. Boundary Dataset (Single issue, extreme capacity bounds)\n";
            std::cout << " 3. Invalid Dataset (Negative hours, out-of-range severities - Tests Defensive Validation)\n";
            std::cout << "Enter dataset choice: ";
            int ds_choice;
            if (std::cin >> ds_choice) {
                std::string path;
                if (ds_choice == 1) path = "data/normal_issues.csv";
                else if (ds_choice == 2) path = "data/boundary_issues.csv";
                else if (ds_choice == 3) path = "data/invalid_issues.csv";
                else path = "data/normal_issues.csv";

                std::vector<Issue> new_issues;
                std::string p_err;
                if (DataParser::parse_issues(path, new_issues, p_err)) {
                    current_issues = new_issues;
                    std::cout << "[SUCCESS] Loaded " << current_issues.size() << " issues from " << path << "\n";
                } else {
                    std::cout << "[REJECTED BY DEFENSIVE VALIDATION] " << p_err << "\n";
                }
            }
        } else if (choice == 6) {
            std::cout << "\n================= LIVE INVARIANT & ALGORITHM TRACE =================\n";
            std::cout << "Loop Invariant for Partition Step in Quick Sort:\n";
            std::cout << "  At the start of each iteration of loop with index j:\n";
            std::cout << "    1. For all k such that low <= k <= i:       arr[k] <= pivot\n";
            std::cout << "    2. For all k such that i + 1 <= k <= j - 1: arr[k] > pivot\n";
            std::cout << "    3. arr[high] == pivot\n\n";
            std::cout << "Augmenting Path Invariant for Maximum Bipartite Matching (Berge's Lemma):\n";
            std::cout << "  A matching M is maximum if and only if there is no augmenting path\n";
            std::cout << "  with respect to M in graph G.\n";
            std::cout << "====================================================================\n";
        } else if (choice == 7) {
            std::cout << "Exiting AutoTriage-DAA. Thank you.\n";
            break;
        }
    }

    return 0;
}
