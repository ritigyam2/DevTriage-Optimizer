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
    // Multi-key priority comparator:
    // Primary: Severity (descending - higher severity first)
    // Secondary: Deadline (ascending - earlier deadline first)
    // Tertiary: ID (ascending - stable tie-break)
    static bool priority_comparator(const Issue& a, const Issue& b) {
        if (a.severity != b.severity) {
            return a.severity > b.severity;
        }
        if (a.deadline_day != b.deadline_day) {
            return a.deadline_day < b.deadline_day;
        }
        return a.id < b.id;
    }

    // ------------------------------------------------------------------------
    // MERGE SORT (Student Author Implementation - Stable, Theta(n log n))
    // ------------------------------------------------------------------------
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
            // Use <= logic to preserve stability when keys are equal
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

    static void merge_sort_recursive(std::vector<Issue>& arr, int left, int right,
                                     bool (*comp)(const Issue&, const Issue&), SortStats& stats) {
        if (left < right) {
            int mid = left + (right - left) / 2;
            merge_sort_recursive(arr, left, mid, comp, stats);
            merge_sort_recursive(arr, mid + 1, right, comp, stats);
            merge(arr, left, mid, right, comp, stats);
        }
    }

public:
    static void merge_sort(std::vector<Issue>& arr, bool (*comp)(const Issue&, const Issue&), SortStats& stats) {
        stats.comparisons = 0;
        stats.element_moves = 0;
        stats.is_stable = true;

        auto start = std::chrono::high_resolution_clock::now();
        if (!arr.empty()) {
            merge_sort_recursive(arr, 0, static_cast<int>(arr.size()) - 1, comp, stats);
        }
        auto end = std::chrono::high_resolution_clock::now();
        stats.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
    }

    // ------------------------------------------------------------------------
    // QUICK SORT (Student Author Implementation - In-Place Partitioning)
    // ------------------------------------------------------------------------
private:
    static void swap_issues(Issue& a, Issue& b, SortStats& stats) {
        Issue temp = a;
        a = b;
        b = temp;
        stats.element_moves += 3;
    }

    static int choose_pivot(std::vector<Issue>& arr, int low, int high,
                            PivotStrategy strategy, bool (*comp)(const Issue&, const Issue&), SortStats& stats) {
        if (strategy == PivotStrategy::FIRST_ELEMENT) {
            return low;
        } else if (strategy == PivotStrategy::RANDOM_ELEMENT) {
            int range = high - low + 1;
            return low + (std::rand() % range);
        } else {
            // Median-of-Three: low, mid, high
            int mid = low + (high - low) / 2;
            // Sort low, mid, high relative to comparator
            stats.comparisons++;
            if (comp(arr[mid], arr[low])) swap_issues(arr[low], arr[mid], stats);
            stats.comparisons++;
            if (comp(arr[high], arr[low])) swap_issues(arr[low], arr[high], stats);
            stats.comparisons++;
            if (comp(arr[high], arr[mid])) swap_issues(arr[mid], arr[high], stats);
            return mid;
        }
    }

    static int partition(std::vector<Issue>& arr, int low, int high,
                         PivotStrategy strategy, bool (*comp)(const Issue&, const Issue&), SortStats& stats) {
        int pivot_idx = choose_pivot(arr, low, high, strategy, comp, stats);
        swap_issues(arr[pivot_idx], arr[high], stats);
        Issue pivot = arr[high];

        int i = low - 1;
        for (int j = low; j < high; ++j) {
            stats.comparisons++;
            if (comp(arr[j], pivot)) {
                i++;
                swap_issues(arr[i], arr[j], stats);
            }
        }
        swap_issues(arr[i + 1], arr[high], stats);
        return i + 1;
    }

    static void quick_sort_recursive(std::vector<Issue>& arr, int low, int high,
                                     PivotStrategy strategy, bool (*comp)(const Issue&, const Issue&), SortStats& stats) {
        if (low < high) {
            int pi = partition(arr, low, high, strategy, comp, stats);
            quick_sort_recursive(arr, low, pi - 1, strategy, comp, stats);
            quick_sort_recursive(arr, pi + 1, high, strategy, comp, stats);
        }
    }

public:
    static void quick_sort(std::vector<Issue>& arr, PivotStrategy strategy,
                           bool (*comp)(const Issue&, const Issue&), SortStats& stats) {
        stats.comparisons = 0;
        stats.element_moves = 0;
        stats.is_stable = false;

        auto start = std::chrono::high_resolution_clock::now();
        if (!arr.empty()) {
            quick_sort_recursive(arr, 0, static_cast<int>(arr.size()) - 1, strategy, comp, stats);
        }
        auto end = std::chrono::high_resolution_clock::now();
        stats.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
    }

    // ------------------------------------------------------------------------
    // BINARY SEARCH (Iterative and Recursive Implementations)
    // ------------------------------------------------------------------------
    static int binary_search_iterative(const std::vector<Issue>& sorted_by_id, int target_id, long long& comparisons) {
        int low = 0;
        int high = static_cast<int>(sorted_by_id.size()) - 1;
        comparisons = 0;

        while (low <= high) {
            int mid = low + (high - low) / 2;
            comparisons++;
            if (sorted_by_id[mid].id == target_id) {
                return mid;
            }
            comparisons++;
            if (sorted_by_id[mid].id < target_id) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return -1; // Not found
    }

    static int binary_search_recursive_helper(const std::vector<Issue>& sorted_by_id, int target_id,
                                             int low, int high, long long& comparisons) {
        if (low > high) return -1;
        int mid = low + (high - low) / 2;
        comparisons++;
        if (sorted_by_id[mid].id == target_id) return mid;
        comparisons++;
        if (sorted_by_id[mid].id < target_id) {
            return binary_search_recursive_helper(sorted_by_id, target_id, mid + 1, high, comparisons);
        } else {
            return binary_search_recursive_helper(sorted_by_id, target_id, low, mid - 1, comparisons);
        }
    }

    static int binary_search_recursive(const std::vector<Issue>& sorted_by_id, int target_id, long long& comparisons) {
        comparisons = 0;
        return binary_search_recursive_helper(sorted_by_id, target_id, 0, static_cast<int>(sorted_by_id.size()) - 1, comparisons);
    }
};
