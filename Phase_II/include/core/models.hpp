#pragma once

#include <string>
#include <vector>
#include <chrono>

struct Issue {
    int id;
    std::string title;
    int severity;          // 1 to 5
    int estimated_hours;   // w_i
    double business_value; // v_i
    int deadline_day;
    std::vector<std::string> skills;
    std::vector<int> prerequisites;

    bool has_skill(const std::string& skill) const {
        for (const auto& s : skills) {
            if (s == skill) return true;
        }
        return false;
    }
};

struct Developer {
    int id;
    std::string name;
    int available_hours;
    int assigned_hours = 0;
    std::vector<std::string> skills;
    std::vector<int> assigned_issue_ids;

    bool has_skill(const std::string& skill) const {
        for (const auto& s : skills) {
            if (s == skill) return true;
        }
        return false;
    }

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

struct SortStats {
    long long comparisons = 0;
    long long element_moves = 0;
    double elapsed_microseconds = 0.0;
    bool is_stable = false;
};

struct MatchingStats {
    int matches_count = 0;
    long long dfs_augmenting_calls = 0;
    double elapsed_microseconds = 0.0;
    std::vector<std::pair<int, int>> matched_pairs; // issue_id, dev_id
};
