#pragma once

#include <vector>
#include <chrono>
#include <climits>
#include <algorithm>

struct SubarrayResult {
    int start_index = -1;
    int end_index = -1;
    long long max_sum = 0;
    long long operations = 0;
    double elapsed_microseconds = 0.0;
};

class MaxSubarrayWorkbench {
private:
    // Helper: Find max crossing subarray crossing the midpoint mid in O(n)
    static SubarrayResult find_max_crossing_subarray(const std::vector<int>& arr, int low, int mid, int high, long long& ops) {
        long long left_sum = LLONG_MIN;
        long long sum = 0;
        int max_left = mid;

        for (int i = mid; i >= low; --i) {
            sum += arr[i];
            ops++;
            if (sum > left_sum) {
                left_sum = sum;
                max_left = i;
            }
        }

        long long right_sum = LLONG_MIN;
        sum = 0;
        int max_right = mid + 1;

        for (int j = mid + 1; j <= high; ++j) {
            sum += arr[j];
            ops++;
            if (sum > right_sum) {
                right_sum = sum;
                max_right = j;
            }
        }

        SubarrayResult res;
        res.start_index = max_left;
        res.end_index = max_right;
        res.max_sum = left_sum + right_sum;
        res.operations = ops;
        return res;
    }

    // Recursive Divide & Conquer: T(n) = 2T(n/2) + Theta(n) => Theta(n log n)
    static SubarrayResult find_max_subarray_recursive(const std::vector<int>& arr, int low, int high, long long& ops) {
        ops++;
        if (low == high) {
            SubarrayResult base;
            base.start_index = low;
            base.end_index = high;
            base.max_sum = arr[low];
            base.operations = ops;
            return base;
        }

        int mid = low + (high - low) / 2;
        SubarrayResult left_res = find_max_subarray_recursive(arr, low, mid, ops);
        SubarrayResult right_res = find_max_subarray_recursive(arr, mid + 1, high, ops);
        SubarrayResult cross_res = find_max_crossing_subarray(arr, low, mid, high, ops);

        if (left_res.max_sum >= right_res.max_sum && left_res.max_sum >= cross_res.max_sum) {
            return left_res;
        } else if (right_res.max_sum >= left_res.max_sum && right_res.max_sum >= cross_res.max_sum) {
            return right_res;
        } else {
            return cross_res;
        }
    }

public:
    // ------------------------------------------------------------------------
    // 1. Divide and Conquer: Theta(n log n)
    // ------------------------------------------------------------------------
    static SubarrayResult divide_and_conquer(const std::vector<int>& arr) {
        SubarrayResult res;
        if (arr.empty()) return res;

        long long ops = 0;
        auto start = std::chrono::high_resolution_clock::now();
        res = find_max_subarray_recursive(arr, 0, static_cast<int>(arr.size()) - 1, ops);
        auto end = std::chrono::high_resolution_clock::now();

        res.operations = ops;
        res.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return res;
    }

    // ------------------------------------------------------------------------
    // 2. Kadane's Linear Scan Algorithm: Theta(n) time, O(1) space
    // ------------------------------------------------------------------------
    static SubarrayResult kadane_linear(const std::vector<int>& arr) {
        SubarrayResult res;
        if (arr.empty()) return res;

        auto start = std::chrono::high_resolution_clock::now();
        long long max_so_far = arr[0];
        long long current_max = arr[0];
        int start_idx = 0;
        int end_idx = 0;
        int temp_start = 0;
        long long ops = 0;

        for (size_t i = 1; i < arr.size(); ++i) {
            ops++;
            if (arr[i] > current_max + arr[i]) {
                current_max = arr[i];
                temp_start = static_cast<int>(i);
            } else {
                current_max += arr[i];
            }

            if (current_max > max_so_far) {
                max_so_far = current_max;
                start_idx = temp_start;
                end_idx = static_cast<int>(i);
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        res.start_index = start_idx;
        res.end_index = end_idx;
        res.max_sum = max_so_far;
        res.operations = ops;
        res.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return res;
    }

    // ------------------------------------------------------------------------
    // Domain Role: Sprint Bug Surge / Churn Window Detection
    // Analyzes daily net issue influx (issues_opened - issues_closed)
    // ------------------------------------------------------------------------
    static SubarrayResult detect_peak_bug_surge_window(const std::vector<int>& daily_net_churn, bool use_dnc = true) {
        if (use_dnc) {
            return divide_and_conquer(daily_net_churn);
        } else {
            return kadane_linear(daily_net_churn);
        }
    }
};
