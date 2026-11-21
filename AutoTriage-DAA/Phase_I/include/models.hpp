#pragma once

#include <string>
#include <vector>
#include <chrono>

// Core Issue Entity
struct Issue {
    int id;                             // Positive unique identifier
    std::string title;                  // Brief description
    int severity;                       // 1 (Trivial) to 5 (Critical Blocker)
    int estimated_hours;                // Required effort w_i
    double business_value;              // Priority value v_i
    int deadline_day;                   // Hard SLA deadline day
    std::vector<std::string> skills;    // Required technical skills S_i
    std::vector<int> prerequisites;     // Dependency blocker issue IDs

    bool has_skill(const std::string& skill) const {
        for (const auto& s : skills) {
            if (s == skill) return true;
        }
        return false;
    }
};

// Core Developer Entity
struct Developer {
    int id;                             // Positive unique identifier
    std::string name;                   // Developer handle/name
    int available_hours;                // Capacity C_j in hours
    int assigned_hours;                 // Currently allocated hours
    std::vector<std::string> skills;    // Verified skillset K_j
    std::vector<int> assigned_issue_ids;// List of assigned issue IDs

    bool has_all_skills(const std::vector<std::string>& required) const {
        for (const auto& req : required) {
            bool found = false;
            for (const auto& s : skills) {
                if (s == req) {
                    found = true;
                    break;
                }
            }
            if (!found) return false;
        }
        return true;
    }

    int remaining_capacity() const {
        return available_hours - assigned_hours;
    }
};

// Statistics container for Sorting Benchmarks
struct SortStats {
    long long comparisons = 0;
    long long element_moves = 0;
    double elapsed_microseconds = 0.0;
    bool is_stable = true;
};

// Statistics container for Developer Assignment Benchmarks
struct MatchingStats {
    int total_issues = 0;
    int assigned_issues = 0;
    int unassigned_issues = 0;
    double assignment_rate_percent = 0.0;
    double elapsed_microseconds = 0.0;
    int total_developer_hours_used = 0;
    int total_developer_hours_available = 0;
    double average_developer_utilization = 0.0;
};
