#pragma once

#include <vector>
#include <queue>
#include <algorithm>
#include <chrono>

struct Interval {
    int id;
    int start_time;
    int finish_time;
    int assigned_room = -1; // Partition / Server / Room ID
};

struct PartitionResult {
    int total_rooms_needed = 0;
    std::vector<Interval> assigned_intervals;
    double elapsed_microseconds = 0.0;
};

class IntervalPartitioningWorkbench {
public:
    // ------------------------------------------------------------------------
    // Interval Partitioning: O(n log n) time, O(d) aux space (d = max overlap)
    // Minimizes total resources (CI servers / review tracks) needed for all tasks
    // ------------------------------------------------------------------------
    static PartitionResult solve(std::vector<Interval> intervals) {
        PartitionResult result;
        if (intervals.empty()) return result;

        auto start = std::chrono::high_resolution_clock::now();

        // Sort intervals by start time ascending
        std::sort(intervals.begin(), intervals.end(), [](const Interval& a, const Interval& b) {
            if (a.start_time != b.start_time) return a.start_time < b.start_time;
            return a.finish_time < b.finish_time;
        });

        // Min-heap storing pairs: (room_free_time, room_id)
        // using std::greater for min-heap
        using HeapElem = std::pair<int, int>;
        std::priority_queue<HeapElem, std::vector<HeapElem>, std::greater<HeapElem>> min_heap;

        int rooms_allocated = 0;

        for (auto& iv : intervals) {
            if (!min_heap.empty() && min_heap.top().first <= iv.start_time) {
                // Room is free! Reuse existing room
                auto top_elem = min_heap.top();
                min_heap.pop();

                iv.assigned_room = top_elem.second;
                min_heap.push({iv.finish_time, iv.assigned_room});
            } else {
                // All active rooms are busy. Allocate new room
                rooms_allocated++;
                iv.assigned_room = rooms_allocated;
                min_heap.push({iv.finish_time, iv.assigned_room});
            }
            result.assigned_intervals.push_back(iv);
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.total_rooms_needed = rooms_allocated;
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
