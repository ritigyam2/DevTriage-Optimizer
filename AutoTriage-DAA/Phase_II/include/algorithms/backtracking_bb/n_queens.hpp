#pragma once

#include <vector>
#include <chrono>
#include <cmath>
#include <cstdlib>

struct NQueensResult {
    int total_solutions = 0;
    std::vector<std::vector<int>> solutions; // Each solution is vector of column indices for rows 0..N-1
    long long state_space_nodes_visited = 0;
    double elapsed_microseconds = 0.0;
};

class NQueensWorkbench {
private:
    static bool is_safe(int row, int col, const std::vector<int>& board) {
        for (int i = 0; i < row; ++i) {
            int other_col = board[i];
            // Same column
            if (other_col == col) return false;
            // Diagonals: |row1 - row2| == |col1 - col2|
            if (std::abs(row - i) == std::abs(col - other_col)) return false;
        }
        return true;
    }

    static void solve_recursive(int row, int N, std::vector<int>& board, NQueensResult& res) {
        res.state_space_nodes_visited++;
        if (row == N) {
            res.total_solutions++;
            res.solutions.push_back(board);
            return;
        }

        for (int col = 0; col < N; ++col) {
            if (is_safe(row, col, board)) {
                board[row] = col;
                solve_recursive(row + 1, N, board, res);
                board[row] = -1; // Backtrack
            }
        }
    }

public:
    // ------------------------------------------------------------------------
    // N-Queens Backtracking: O(N!) worst case, O(N) recursion stack
    // Constraint satisfaction validator for non-conflicting reviewer allocations
    // ------------------------------------------------------------------------
    static NQueensResult solve(int N) {
        NQueensResult result;
        if (N <= 0) return result;

        auto start = std::chrono::high_resolution_clock::now();

        std::vector<int> board(N, -1);
        solve_recursive(0, N, board, result);

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
