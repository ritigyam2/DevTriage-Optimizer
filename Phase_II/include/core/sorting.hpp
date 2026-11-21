#pragma once

#include "models.hpp"
#include <vector>
#include <chrono>
#include <cstdlib>

enum class PivotStrategy {
    FIRST_ELEMENT,      // Vulnerable to sorted / reverse sorted adversarial attacks: O(n^2)
    MEDIAN_OF_THREE,    // Chooses median of low, mid, high: defeats sorted adversarial inputs
    RANDOM_ELEMENT      // Expected O(n log n) across all permutations
};

class SortingWorkbench {
public:
    static bool priority_comparator(const Issue& a, const Issue& b) {
        if (a.severity != b.severity) {
            return a.severity > b.severity;
        }
        if (a.deadline_day != b.deadline_day) {
            return a.deadline_day < b.deadline_day;
        }
        return a.id < b.id;
    }

private:
    static void merge(std::vector<Issue>& arr, int left, int mid, int right,
                      bool (*comp)(const Issue&, const Issue&), SortStats& stats) {
        int n1 = mid - left + 1;
        int n2 = right - mid;

        std::vector<Issue> L(n1);
        std::vector<Issue> R(n2);

        for (int i = 0; i < n1; ++i) {
            L[i] = arr[left + i];
            stats.element_moves++;
        }
        for (int j = 0; j < n2; ++j) {
            R[j] = arr[mid + 1 + j];
            stats.element_moves++;
        }

        int i = 0, j = 0, k = left;
        while (i < n1 && j < n2) {
            stats.comparisons++;
            if (comp(L[i], R[j]) || (!comp(R[j], L[i]))) {
                arr[k] = L[i];
                i++;
            } else {
                arr[k] = R[j];
                j++;
            }
            stats.element_moves++;
            k++;
        }

        while (i < n1) {
            arr[k] = L[i];
            i++;
            k++;
            stats.element_moves++;
        }
        while (j < n2) {
            arr[k] = R[j];
            j++;
            k++;
            stats.element_moves++;
        }
    }

    static void merge_sort_rec(std::vector<Issue>& arr, int left, int right,
                               bool (*comp)(const Issue&, const Issue&), SortStats& stats) {
        if (left < right) {
            int mid = left + (right - left) / 2;
            merge_sort_rec(arr, left, mid, comp, stats);
            merge_sort_rec(arr, mid + 1, right, comp, stats);
            merge(arr, left, mid, right, comp, stats);
        }
    }

    static int select_pivot_index(std::vector<Issue>& arr, int low, int high,
                                  PivotStrategy strategy, bool (*comp)(const Issue&, const Issue&),
                                  SortStats& stats) {
        if (strategy == PivotStrategy::FIRST_ELEMENT) {
            return low;
        } else if (strategy == PivotStrategy::RANDOM_ELEMENT) {
            int range = high - low + 1;
            return low + (std::rand() % range);
        } else {
            int mid = low + (high - low) / 2;
            stats.comparisons += 3;
            bool lm = comp(arr[low], arr[mid]);
            bool mh = comp(arr[mid], arr[high]);
            bool lh = comp(arr[low], arr[high]);

            if ((lm && mh) || (!lm && !mh)) return mid;
            if ((lh && !mh) || (!lh && mh)) return high;
            return low;
        }
    }

    static int partition(std::vector<Issue>& arr, int low, int high,
                         PivotStrategy strategy, bool (*comp)(const Issue&, const Issue&),
                         SortStats& stats) {
        int pivot_idx = select_pivot_index(arr, low, high, strategy, comp, stats);
        if (pivot_idx != high) {
            std::swap(arr[pivot_idx], arr[high]);
            stats.element_moves += 3;
        }

        Issue pivot = arr[high];
        int i = low - 1;

        for (int j = low; j < high; ++j) {
            stats.comparisons++;
            if (comp(arr[j], pivot) || (!comp(pivot, arr[j]))) {
                i++;
                if (i != j) {
                    std::swap(arr[i], arr[j]);
                    stats.element_moves += 3;
                }
            }
        }
        std::swap(arr[i + 1], arr[high]);
        stats.element_moves += 3;
        return i + 1;
    }

    static void quick_sort_rec(std::vector<Issue>& arr, int low, int high,
                               PivotStrategy strategy, bool (*comp)(const Issue&, const Issue&),
                               SortStats& stats) {
        if (low < high) {
            int pi = partition(arr, low, high, strategy, comp, stats);
            quick_sort_rec(arr, low, pi - 1, strategy, comp, stats);
            quick_sort_rec(arr, pi + 1, high, strategy, comp, stats);
        }
    }

public:
    static void merge_sort(std::vector<Issue>& arr, bool (*comp)(const Issue&, const Issue&), SortStats& stats) {
        stats.comparisons = 0;
        stats.element_moves = 0;
        stats.is_stable = true;
        auto start = std::chrono::high_resolution_clock::now();
        if (!arr.empty()) {
            merge_sort_rec(arr, 0, static_cast<int>(arr.size()) - 1, comp, stats);
        }
        auto end = std::chrono::high_resolution_clock::now();
        stats.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
    }

    static void quick_sort(std::vector<Issue>& arr, bool (*comp)(const Issue&, const Issue&),
                           PivotStrategy strategy, SortStats& stats) {
        stats.comparisons = 0;
        stats.element_moves = 0;
        stats.is_stable = false;
        auto start = std::chrono::high_resolution_clock::now();
        if (!arr.empty()) {
            quick_sort_rec(arr, 0, static_cast<int>(arr.size()) - 1, strategy, comp, stats);
        }
        auto end = std::chrono::high_resolution_clock::now();
        stats.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
    }
};
