#pragma once

#include <vector>
#include <algorithm>
#include <chrono>

struct Activity {
    int id;
    int start_time;
    int finish_time;
};

struct ActivityResult {
    int count = 0;
    std::vector<Activity> scheduled_activities;
    double elapsed_microseconds = 0.0;
};

class ActivitySelectionWorkbench {
public:
    // ------------------------------------------------------------------------
    // Activity Selection: O(n log n) time, O(1) aux space
    // Greedily selects non-overlapping activities ordered by finish time ascending
    // ------------------------------------------------------------------------
    static ActivityResult solve(std::vector<Activity> activities) {
        ActivityResult result;
        if (activities.empty()) return result;

        auto start = std::chrono::high_resolution_clock::now();

        // Sort activities by finish time ascending
        std::sort(activities.begin(), activities.end(), [](const Activity& a, const Activity& b) {
            if (a.finish_time != b.finish_time) return a.finish_time < b.finish_time;
            return a.start_time < b.start_time;
        });

        // Greedily pick the first activity
        result.scheduled_activities.push_back(activities[0]);
        int last_finish = activities[0].finish_time;

        for (size_t i = 1; i < activities.size(); ++i) {
            // Next activity must start at or after previous finished
            if (activities[i].start_time >= last_finish) {
                result.scheduled_activities.push_back(activities[i]);
                last_finish = activities[i].finish_time;
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.count = static_cast<int>(result.scheduled_activities.size());
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
