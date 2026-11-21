import subprocess

original = subprocess.check_output(['git', 'show', 'HEAD:Phase_II/src/scenario_benchmarks.cpp'], text=True)

clean_main = r'''int main() {
    std::cout << "\n===============================================================================\n";
    std::cout << "  AutoTriage-DAA\n";
    std::cout << "  Open Source Issue Triage and Developer Assignment Tool\n\n";
    std::cout << "  Design and Analysis of Algorithms -- PBL (Project 50)\n";
    std::cout << "  Developed by: Ritigya Mishra | SAP ID: 590028115 | Batch: B-9 (AI/ML)\n";
    std::cout << "  Course: B.Tech-CSE\n";
    std::cout << "===============================================================================\n";

    Scenario1Evidence ev1 = run_scenario_1_normal();
    Scenario2Evidence ev2 = run_scenario_2_capacity_shock();
    Scenario3Evidence ev3 = run_scenario_3_large_scale_adversarial();
    Scenario4Evidence ev4 = run_scenario_4_real_world_and_online_streaming();

    // Export Reproducible Benchmark Evidence to CSV (strictly from measured runtime objects)
    std::string csv_path = "scenario_benchmark_results.csv";
    std::ofstream out(csv_path);
    if (out.is_open()) {
        out << "Scenario,Algorithm,Metric_Name,Metric_Value,Unit\n";
        out << "Scenario_1_Normal,Max_Bipartite_Matching,Matched_Issues," << ev1.max_matched << ",count\n";
        out << "Scenario_1_Normal,Max_Bipartite_Matching,Developer_Utilization_Rate," << ev1.dev_utilization_percent << ",percent\n";
        out << "Scenario_1_Normal,Max_Bipartite_Matching,Issue_Backlog_Assigned_Rate," << ev1.issue_assignment_percent << ",percent\n";
        out << "Scenario_1_Normal,0/1_Knapsack_DP,Total_Value," << ev1.knapsack_dp_value << ",points\n";
        out << "Scenario_1_Normal,Fractional_Knapsack,Theoretical_Bound_Value," << ev1.frac_knapsack_value << ",points\n";
        out << "Scenario_2_Shock,LC_Branch_And_Bound,Pruned_Nodes," << ev2.lc_bb_pruned_nodes << ",nodes\n";
        out << "Scenario_2_Shock,LC_Branch_And_Bound,Value_Achieved," << ev2.lc_bb_value << ",points\n";
        out << "Scenario_2_Shock,Dijkstra_Rerouting,Path_Cost," << ev2.reroute_path_cost << ",cost\n";
        out << "Scenario_3_Adversarial,Quick_Sort_Med3,Comparisons," << ev3.quick_med3_comparisons << ",ops\n";
        out << "Scenario_3_Adversarial,Merge_Sort_Stable,Comparisons," << ev3.merge_comparisons << ",ops\n";
        out << "Scenario_3_Adversarial,KMP_String_Search,Comparisons," << ev3.kmp_comparisons << ",ops\n";
        out << "Scenario_3_Adversarial,Naive_String_Search,Comparisons," << ev3.naive_comparisons << ",ops\n";
        out << "Scenario_4_Synthetic_Enterprise,Dataset_Size,Total_Issues," << ev4.dataset_issues_count << ",issues\n";
        out << "Scenario_4_Synthetic_Enterprise,Dataset_Size,Total_Developers," << ev4.dataset_devs_count << ",maintainers\n";
        out << "Scenario_4_Synthetic_Enterprise,Online_Streaming,Empirical_Competitive_Ratio," << ev4.empirical_competitive_ratio << ",ratio\n";
        out << "Scenario_4_Synthetic_Enterprise,Preemption_Engine,Preemptions_Triggered," << ev4.preemptions_triggered << ",count\n";
        out.close();
        std::cout << "\n[SUCCESS] Measured scenario benchmark evidence exported to: " << csv_path << "\n";
    }

    std::cout << "===============================================================================\n";
    std::cout << "  Benchmark summary: 4/4 demonstration scenarios completed successfully.\n";
    std::cout << "===============================================================================\n\n";
    return 0;
}'''

idx = original.find('int main() {')
clean_content = original[:idx] + clean_main

for target in ['Phase_II/src/scenario_benchmarks.cpp', 'AutoTriage-DAA/Phase_II/src/scenario_benchmarks.cpp']:
    with open(target, 'w', encoding='utf-8') as f:
        f.write(clean_content)

print('Cleanly updated scenario_benchmarks.cpp in both locations!')
