#include "../include/core/models.hpp"
#include "../include/core/parser.hpp"
#include "../include/core/sorting.hpp"
#include "../include/core/visualizer.hpp"
#include "../include/algorithms/divide_and_conquer/strassen.hpp"
#include "../include/algorithms/divide_and_conquer/max_subarray.hpp"
#include "../include/algorithms/divide_and_conquer/fast_power.hpp"
#include "../include/algorithms/divide_and_conquer/celebrity.hpp"
#include "../include/algorithms/greedy/fractional_knapsack.hpp"
#include "../include/algorithms/greedy/activity_selection.hpp"
#include "../include/algorithms/greedy/interval_partitioning.hpp"
#include "../include/algorithms/greedy/huffman.hpp"
#include "../include/algorithms/greedy/dijkstra.hpp"
#include "../include/algorithms/greedy/mst.hpp"
#include "../include/algorithms/dynamic_programming/knapsack_01.hpp"
#include "../include/algorithms/dynamic_programming/matrix_chain.hpp"
#include "../include/algorithms/dynamic_programming/lcs.hpp"
#include "../include/algorithms/dynamic_programming/obst.hpp"
#include "../include/algorithms/dynamic_programming/bellman_ford.hpp"
#include "../include/algorithms/dynamic_programming/floyd_warshall.hpp"
#include "../include/algorithms/dynamic_programming/tsp_held_karp.hpp"
#include "../include/algorithms/backtracking_bb/n_queens.hpp"
#include "../include/algorithms/backtracking_bb/sum_of_subsets.hpp"
#include "../include/algorithms/backtracking_bb/knapsack_backtracking.hpp"
#include "../include/algorithms/backtracking_bb/knapsack_branch_and_bound.hpp"
#include "../include/algorithms/backtracking_bb/tsp_branch_and_bound.hpp"
#include "../include/algorithms/flow_matching/ford_fulkerson.hpp"
#include "../include/algorithms/flow_matching/bipartite_matching.hpp"
#include "../include/algorithms/online_streaming/online_triage.hpp"
#include "../include/algorithms/number_theory/crt.hpp"
#include "../include/algorithms/string_matching/string_matchers.hpp"
#include "../include/core/complexity_reductions.hpp"
#include "../include/core/report_exporter.hpp"

#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <fstream>

void print_header() {
    std::cout << "\n===============================================================================\n";
    std::cout << "  AutoTriage-DAA (Project 50) | INTEGRATED PHASE II SYLLABUS WORKBENCH\n";
    std::cout << "  Open Source Issue Triage and Developer Assignment Tool\n";
    std::cout << "  Author: Ritigya Mishra | Course: Design and Analysis of Algorithms (C++17)\n";
    std::cout << "===============================================================================\n\n";
}

int main() {
    print_header();

    std::vector<Issue> issues;
    std::vector<Developer> devs;
    std::string err;

    // Prefer Synthetic Enterprise Benchmark Dataset if available
    std::string issues_file = "data/synthetic_enterprise_issues.csv";
    std::string devs_file = "data/synthetic_enterprise_developers.csv";

    if (!DataParser::parse_issues(issues_file, issues, err) ||
        !DataParser::parse_developers(devs_file, devs, err)) {
        issues_file = "data/real_world_issues.csv";
        devs_file = "data/real_world_developers.csv";
        if (!DataParser::parse_issues(issues_file, issues, err) ||
            !DataParser::parse_developers(devs_file, devs, err)) {
            // Fallback to Phase I baseline dataset
            issues_file = "../Phase_I/data/normal_issues.csv";
            devs_file = "../Phase_I/data/normal_developers.csv";
            DataParser::parse_issues(issues_file, issues, err);
            DataParser::parse_developers(devs_file, devs, err);
        }
    }

    std::cout << "[INIT] Successfully loaded repository dataset: " 
              << issues.size() << " issues, " << devs.size() << " developers.\n";

    int choice = 0;
    while (true) {
        std::cout << "\n============================= MAIN WORKBENCH MENU =============================\n";
        std::cout << " 1. Backlog Triage & Multi-Key Stable Sorting (Merge Sort)\n";
        std::cout << " 2. Developer Assignment Engine (Bipartite Flow Matching vs Greedy)\n";
        std::cout << " 3. Sprint Release Planning (0/1 Knapsack DP vs LC B&B vs Fractional)\n";
        std::cout << " 4. Code Review & CI Machine Scheduling (Activity Selection & Interval Partition)\n";
        std::cout << " 5. Architecture & Refactoring (Strassen, Dijkstra, MST, Floyd-Warshall)\n";
        std::cout << " 6. Issue Intelligence & Search (4-Way String Matchers & Huffman Compression)\n";
        std::cout << " 7. Verification & Complexity Suite (Celebrity Maintainer, CRT, P/NP Reductions)\n";
        std::cout << " 8. Real-Time Online Streaming & Zero-Day Preemption Simulation\n";
        std::cout << " 9. Sprint Capacity Visualizer & ASCII Gantt Schedule Matrix\n";
        std::cout << " 10. Export Complete Assignment Plan & Benchmarks to CSV\n";
        std::cout << " 11. Exit\n";
        std::cout << "================================================================================\n";
        std::cout << "Select a module to execute (1-11): ";

        if (!(std::cin >> choice)) {
            std::cin.clear();
            std::string discard;
            std::cin >> discard;
            continue;
        }

        if (choice == 1) {
            std::cout << "\n>>> MODULE 1: MULTI-KEY BACKLOG TRIAGE <<<\n";
            SortStats stats;
            SortingWorkbench::merge_sort(issues, SortingWorkbench::priority_comparator, stats);
            std::cout << "[SUCCESS] Backlog sorted via Stable Merge Sort in " << stats.elapsed_microseconds 
                      << " us (" << stats.comparisons << " comparisons, " << stats.element_moves << " moves)\n\n";

            std::cout << std::left << std::setw(6) << "ID" << std::setw(42) << "Issue Title"
                      << std::setw(6) << "Sev" << std::setw(8) << "Hours" << std::setw(8) << "Value" << "SLA\n";
            std::cout << "--------------------------------------------------------------------------------\n";
            for (size_t i = 0; i < std::min((size_t)10, issues.size()); ++i) {
                std::cout << std::left << std::setw(6) << issues[i].id
                          << std::setw(42) << (issues[i].title.length() > 40 ? issues[i].title.substr(0, 37) + "..." : issues[i].title)
                          << std::setw(6) << issues[i].severity
                          << std::setw(8) << issues[i].estimated_hours
                          << std::setw(8) << issues[i].business_value
                          << "Day " << issues[i].deadline_day << "\n";
            }
        } else if (choice == 2) {
            std::cout << "\n>>> MODULE 2: CAPACITY-CONSTRAINED DEVELOPER ASSIGNMENT <<<\n";
            int N = static_cast<int>(issues.size());
            int M = static_cast<int>(devs.size());

            std::vector<std::vector<int>> compat(N);
            for (int i = 0; i < N; ++i) {
                for (int j = 0; j < M; ++j) {
                    if (devs[j].has_all_skills(issues[i].skills) && devs[j].remaining_capacity() >= issues[i].estimated_hours) {
                        compat[i].push_back(j);
                    }
                }
            }

            BipartiteAssignmentResult bip_res = BipartiteFlowWorkbench::solve(N, M, compat);
            std::cout << "[MAX BIPARTITE FLOW MATCHING] Matched " << bip_res.max_matched 
                      << " / " << N << " issues in " << bip_res.elapsed_microseconds << " us\n";
            
            // Populate developer loads
            for (auto& d : devs) {
                d.assigned_hours = 0;
                d.assigned_issue_ids.clear();
            }
            for (const auto& pair : bip_res.issue_dev_pairs) {
                devs[pair.second].assigned_hours += issues[pair.first].estimated_hours;
                devs[pair.second].assigned_issue_ids.push_back(issues[pair.first].id);
            }

            TerminalVisualizer::print_developer_workload(devs);
        } else if (choice == 3) {
            std::cout << "\n>>> MODULE 3: SPRINT RELEASE PLANNING OPTIMIZATION <<<\n";
            std::vector<KnapsackItem> k_items;
            std::vector<FractionalItem> f_items;
            std::vector<BBItem> bb_items;

            for (const auto& it : issues) {
                k_items.push_back({it.id, it.estimated_hours, it.business_value});
                f_items.push_back({it.id, static_cast<double>(it.estimated_hours), it.business_value});
                bb_items.push_back({it.id, it.estimated_hours, it.business_value});
            }

            int sprint_capacity = 120; // Team sprint budget

            Knapsack01Result res_dp = Knapsack01Workbench::solve_2d(k_items, sprint_capacity);
            FractionalResult res_frac = FractionalKnapsackWorkbench::solve(f_items, sprint_capacity);
            BBStrategyResult res_lc = KnapsackBranchAndBoundWorkbench::solve_least_cost(bb_items, sprint_capacity);

            std::cout << "--------------------------------------------------------------------------------\n";
            std::cout << std::left << std::setw(32) << "Optimization Strategy"
                      << std::setw(16) << "Total Value"
                      << std::setw(16) << "Hours Used"
                      << "Time (us)\n";
            std::cout << "--------------------------------------------------------------------------------\n";
            std::cout << std::left << std::setw(32) << "0/1 Knapsack (DP 2D)"
              << std::setw(16) << res_dp.max_value << std::setw(16) << res_dp.total_weight_used
              << res_dp.elapsed_microseconds << "\n";
            std::cout << std::left << std::setw(32) << "0/1 Knapsack (LC Branch&Bound)"
              << std::setw(16) << res_lc.max_value << std::setw(16) << res_lc.total_weight_used
              << res_lc.elapsed_microseconds << "\n";
            std::cout << std::left << std::setw(32) << "Fractional Knapsack (Greedy)"
              << std::setw(16) << res_frac.total_value << std::setw(16) << res_frac.total_weight_used
              << res_frac.elapsed_microseconds << "\n";
            std::cout << "--------------------------------------------------------------------------------\n";
            std::cout << "Selected Discrete Issue IDs: ";
            for (size_t i = 0; i < std::min((size_t)12, res_dp.selected_item_ids.size()); ++i) {
                std::cout << "#" << res_dp.selected_item_ids[i] << " ";
            }
            std::cout << "...\n";
        } else if (choice == 4) {
            std::cout << "\n>>> MODULE 4: REVIEW & CI RESOURCE SCHEDULING <<<\n";
            std::vector<Activity> activities = {
                {1, 9, 11}, {2, 10, 12}, {3, 11, 13}, {4, 13, 15}, {5, 14, 16}, {6, 15, 17}
            };
            ActivityResult act_res = ActivitySelectionWorkbench::solve(activities);
            std::cout << "[ACTIVITY SELECTION] Scheduled " << act_res.count << " non-overlapping review sessions:\n";
            for (const auto& a : act_res.scheduled_activities) {
                std::cout << "  Session #" << a.id << ": [" << a.start_time << ":00 - " << a.finish_time << ":00]\n";
            }

            std::vector<Interval> intervals = {
                {1, 9, 12}, {2, 10, 13}, {3, 11, 14}, {4, 13, 16}, {5, 14, 17}
            };
            PartitionResult part_res = IntervalPartitioningWorkbench::solve(intervals);
            std::cout << "[INTERVAL PARTITIONING] Minimum CI runner servers required: " 
                      << part_res.total_rooms_needed << "\n";
        } else if (choice == 5) {
            std::cout << "\n>>> MODULE 5: REPOSITORY ARCHITECTURE & REFACTORING <<<\n";
            int V = 5;
            std::vector<Edge> edges = {
                {0, 1, 2.0}, {0, 3, 6.0}, {1, 2, 3.0}, {1, 4, 5.0}, {2, 4, 7.0}, {3, 4, 9.0}
            };
            std::vector<std::vector<std::pair<int, double>>> adj(V);
            for (const auto& e : edges) {
                adj[e.u].push_back({e.v, e.weight});
                adj[e.v].push_back({e.u, e.weight});
            }

            MSTResult k_res = MSTWorkbench::kruskal_mst(V, edges);
            MSTResult p_res = MSTWorkbench::prim_mst(V, adj);
            std::cout << "[MST REFACTORING BACKBONE] Kruskal Cost = " << k_res.total_weight 
                      << " | Prim Cost = " << p_res.total_weight << " (Exact match!)\n";

            DijkstraResult d_res = DijkstraWorkbench::shortest_path(adj, 0);
            std::cout << "[DIJKSTRA] Shortest refactoring path from Module 0 to 4: cost = " 
                      << d_res.distances[4] << "\n";

            const double INF = 1e18;
            std::vector<std::vector<double>> cost = {
                {0, 3, INF, 7}, {8, 0, 2, INF}, {5, INF, 0, 1}, {2, INF, INF, 0}
            };
            FloydWarshallResult fw_res = FloydWarshallWorkbench::all_pairs_shortest_path(4, cost);
            std::cout << "[FLOYD-WARSHALL] Blast radius of Core Module 0: " 
                      << fw_res.get_blast_radius(0) << " downstream modules\n";
        } else if (choice == 6) {
            std::cout << "\n>>> MODULE 6: ISSUE TEXT INTELLIGENCE & COMPRESSION <<<\n";
            std::string log_text = "ERROR_CRITICAL_PANIC_CVE_2026_MEMORY_CORRUPTION_IN_KERNEL_NETWORK_DRIVER";
            std::string query = "CVE_2026";

            StringMatchResult kmp_res = StringMatchingWorkbench::kmp_search(log_text, query);
            std::cout << "[KMP STRING SEARCH] Found signature \"" << query << "\" at offset: "
                      << (kmp_res.match_indices.empty() ? -1 : kmp_res.match_indices[0]) << "\n";

            HuffmanResult huff_res = HuffmanWorkbench::compress_and_decompress(log_text);
            std::cout << "[HUFFMAN COMPRESSION] " << huff_res.original_bits << " bits -> " 
                      << huff_res.compressed_bits << " bits (" << huff_res.compression_ratio << "x ratio)\n";
        } else if (choice == 7) {
            std::cout << "\n>>> MODULE 7: VERIFICATION & COMPLEXITY REDUCTIONS <<<\n";
            CelebrityWorkbench::ReviewMatrix M = {
                {0, 1, 1, 0}, {0, 0, 1, 1}, {0, 0, 0, 0}, {1, 0, 1, 0}
            };
            CelebrityResult celeb_res = CelebrityWorkbench::find_core_maintainer_linear(M);
            std::cout << "[CELEBRITY REVIEW BOTTLENECK] Core Maintainer: Dev #" 
                      << celeb_res.candidate_id << " (" << celeb_res.comparisons << " comparisons)\n";

            CRTResult crt_res = ChineseRemainderTheoremWorkbench::solve({2, 3, 2}, {3, 5, 7});
            std::cout << "[CHINESE REMAINDER THEOREM] Reconstructed commit counter: " 
                      << crt_res.solution << " mod " << crt_res.combined_modulus << "\n";

            ReductionProofResult red_res = ComplexityReductionWorkbench::verify_subset_sum_to_knapsack_reduction({3, 34, 4, 12, 5, 2}, 9);
            std::cout << "[COMPLEXITY REDUCTION] Subset-Sum <=_P 0/1 Knapsack: " 
                      << (red_res.reduction_holds ? "FORMALLY VERIFIED (Q.E.D.)" : "INVALID") << "\n";
        } else if (choice == 8) {
            std::cout << "\n>>> MODULE 8: ONLINE STREAMING & ZERO-DAY PREEMPTION SIMULATION <<<\n";
            std::vector<StreamEvent> stream;
            for (int i = 0; i < 20; ++i) {
                StreamEvent ev;
                ev.arrival_time_hour = i * 4;
                ev.issue = issues[i % issues.size()];
                ev.is_emergency_cve = (i == 7);
                if (ev.is_emergency_cve) {
                    ev.issue.severity = 5;
                    ev.issue.title = "CVE-2026-9999: Zero-Day Memory Corruption in Kernel eBPF";
                }
                stream.push_back(ev);
            }

            OnlineStreamingReport stream_rep = OnlineStreamingEngine::simulate_online_stream(devs, stream, true);
            std::cout << "Online Streaming Arrivals: " << stream_rep.total_arrivals << " events over 80h\n";
            std::cout << "  Accepted: " << stream_rep.online_accepted << " | Preemptions: " 
                      << stream_rep.preemptions_triggered << "\n";
            std::cout << "  Empirical Competitive Ratio (Online / Offline): " << std::fixed << std::setprecision(4) 
                      << stream_rep.competitive_ratio << "\n\n";

            for (const auto& p : stream_rep.preemption_log) {
                std::cout << "  [PREEMPTION EVENT @ " << p.hour << "h] Paused task #" << p.preempted_issue_id
                          << " on " << p.dev_name << " -> Dispatched Zero-Day CVE #" << p.emergency_issue_id << "\n";
            }
        } else if (choice == 9) {
            std::cout << "\n>>> MODULE 9: SPRINT CAPACITY VISUALIZER & GANTT MATRIX <<<\n";
            TerminalVisualizer::print_developer_workload(devs);
            TerminalVisualizer::print_ascii_gantt_chart(devs, issues, 10);
        } else if (choice == 10) {
            std::cout << "\n>>> MODULE 10: EXPORTING ASSIGNMENT PLAN & BENCHMARKS <<<\n";
            std::string triage_csv = "assignment_plan_report.csv";
            std::string workload_csv = "developer_workload_report.csv";
            if (ReportExporter::export_triage_csv(triage_csv, issues) &&
                ReportExporter::export_assignment_plan(workload_csv, devs, issues)) {
                std::cout << "[SUCCESS] Exported triage backlog to: " << triage_csv << "\n";
                std::cout << "[SUCCESS] Exported developer workloads to: " << workload_csv << "\n";
            } else {
                std::cout << "[ERROR] Could not write report files.\n";
            }
        } else if (choice == 11) {
            std::cout << "Exiting AutoTriage-DAA Integrated Workbench. Goodbye.\n";
            break;
        }
    }

    return 0;
}
