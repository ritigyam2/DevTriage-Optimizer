#pragma once

#include "models.hpp"
#include <vector>
#include <chrono>
#include <iostream>

class AssignmentWorkbench {
private:
    // DFS helper for finding augmenting paths in Bipartite Graph
    static bool dfs_augment(int issue_idx,
                            const std::vector<std::vector<int>>& adj,
                            std::vector<bool>& visited_dev,
                            std::vector<int>& match_dev_to_issue) {
        for (int dev_idx : adj[issue_idx]) {
            if (!visited_dev[dev_idx]) {
                visited_dev[dev_idx] = true;
                // If developer is unassigned or their current issue can be reassigned
                if (match_dev_to_issue[dev_idx] < 0 ||
                    dfs_augment(match_dev_to_issue[dev_idx], adj, visited_dev, match_dev_to_issue)) {
                    match_dev_to_issue[dev_idx] = issue_idx;
                    return true;
                }
            }
        }
        return false;
    }

public:
    // ------------------------------------------------------------------------
    // MAXIMUM BIPARTITE MATCHING (Augmenting Paths - Kuhn's Algorithm)
    // ------------------------------------------------------------------------
    static MatchingStats maximum_bipartite_matching(const std::vector<Issue>& issues,
                                                   std::vector<Developer>& devs) {
        MatchingStats stats;
        stats.total_issues = static_cast<int>(issues.size());

        auto start = std::chrono::high_resolution_clock::now();

        // Reset developer allocations
        for (auto& d : devs) {
            d.assigned_hours = 0;
            d.assigned_issue_ids.clear();
        }

        int N = static_cast<int>(issues.size());
        int M = static_cast<int>(devs.size());

        // Step 1: Construct Bipartite Adjacency List
        // An edge exists if developer has ALL required skills AND has enough capacity
        std::vector<std::vector<int>> adj(N);
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < M; ++j) {
                if (devs[j].has_all_skills(issues[i].skills) &&
                    devs[j].available_hours >= issues[i].estimated_hours) {
                    adj[i].push_back(j);
                }
            }
        }

        // match_dev_to_issue[j] stores index of issue assigned to developer j (-1 if free)
        std::vector<int> match_dev_to_issue(M, -1);
        int matched_count = 0;

        // Step 2: Find augmenting paths for each issue
        for (int i = 0; i < N; ++i) {
            std::vector<bool> visited_dev(M, false);
            if (dfs_augment(i, adj, visited_dev, match_dev_to_issue)) {
                matched_count++;
            }
        }

        // Step 3: Commit assignments back to Developer structs
        for (int j = 0; j < M; ++j) {
            if (match_dev_to_issue[j] >= 0) {
                int issue_idx = match_dev_to_issue[j];
                devs[j].assigned_issue_ids.push_back(issues[issue_idx].id);
                devs[j].assigned_hours += issues[issue_idx].estimated_hours;
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        stats.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();

        stats.assigned_issues = matched_count;
        stats.unassigned_issues = stats.total_issues - matched_count;
        stats.assignment_rate_percent = stats.total_issues > 0 ?
            (100.0 * stats.assigned_issues / stats.total_issues) : 0.0;

        int total_avail = 0, total_used = 0;
        for (const auto& d : devs) {
            total_avail += d.available_hours;
            total_used += d.assigned_hours;
        }
        stats.total_developer_hours_available = total_avail;
        stats.total_developer_hours_used = total_used;
        stats.average_developer_utilization = total_avail > 0 ?
            (100.0 * total_used / total_avail) : 0.0;

        return stats;
    }

    // ------------------------------------------------------------------------
    // GREEDY SKILL-FIRST MATCHING (Comparative Heuristic Algorithm)
    // ------------------------------------------------------------------------
    static MatchingStats greedy_skill_matching(const std::vector<Issue>& prioritized_issues,
                                              std::vector<Developer>& devs) {
        MatchingStats stats;
        stats.total_issues = static_cast<int>(prioritized_issues.size());

        auto start = std::chrono::high_resolution_clock::now();

        // Reset developer allocations
        for (auto& d : devs) {
            d.assigned_hours = 0;
            d.assigned_issue_ids.clear();
        }

        int assigned_count = 0;

        // Greedily iterate over prioritized issues
        for (const auto& issue : prioritized_issues) {
            // Find the first eligible developer with sufficient remaining hours
            for (auto& dev : devs) {
                if (dev.has_all_skills(issue.skills) &&
                    dev.remaining_capacity() >= issue.estimated_hours) {
                    dev.assigned_hours += issue.estimated_hours;
                    dev.assigned_issue_ids.push_back(issue.id);
                    assigned_count++;
                    break; // Greedily bind and do not backtrack
                }
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        stats.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();

        stats.assigned_issues = assigned_count;
        stats.unassigned_issues = stats.total_issues - assigned_count;
        stats.assignment_rate_percent = stats.total_issues > 0 ?
            (100.0 * stats.assigned_issues / stats.total_issues) : 0.0;

        int total_avail = 0, total_used = 0;
        for (const auto& d : devs) {
            total_avail += d.available_hours;
            total_used += d.assigned_hours;
        }
        stats.total_developer_hours_available = total_avail;
        stats.total_developer_hours_used = total_used;
        stats.average_developer_utilization = total_avail > 0 ?
            (100.0 * total_used / total_avail) : 0.0;

        return stats;
    }
};
