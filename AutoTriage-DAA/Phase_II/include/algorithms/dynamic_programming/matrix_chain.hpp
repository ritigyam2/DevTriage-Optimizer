#pragma once

#include <vector>
#include <string>
#include <climits>
#include <chrono>

struct MCMResult {
    long long min_multiplications = 0;
    std::string optimal_parenthesization;
    double elapsed_microseconds = 0.0;
};

class MatrixChainWorkbench {
private:
    static void print_optimal_parens(int i, int j, const std::vector<std::vector<int>>& s, std::string& out) {
        if (i == j) {
            out += "A" + std::to_string(i);
        } else {
            out += "(";
            print_optimal_parens(i, s[i][j], s, out);
            print_optimal_parens(s[i][j] + 1, j, s, out);
            out += ")";
        }
    }

public:
    // ------------------------------------------------------------------------
    // Matrix Chain Multiplication: Theta(n^3) time, Theta(n^2) aux space
    // Finds optimal parenthesization minimizing total scalar multiplications
    // ------------------------------------------------------------------------
    static MCMResult solve(const std::vector<int>& p) {
        MCMResult result;
        int n = static_cast<int>(p.size()) - 1; // Number of matrices
        if (n <= 0) return result;

        auto start = std::chrono::high_resolution_clock::now();

        // m[i][j] stores minimum multiplications for A_i..A_j (1-indexed)
        std::vector<std::vector<long long>> m(n + 1, std::vector<long long>(n + 1, 0));
        // s[i][j] stores split point k
        std::vector<std::vector<int>> s(n + 1, std::vector<int>(n + 1, 0));

        // l is chain length: from 2 to n
        for (int l = 2; l <= n; ++l) {
            for (int i = 1; i <= n - l + 1; ++i) {
                int j = i + l - 1;
                m[i][j] = LLONG_MAX;
                for (int k = i; k <= j - 1; ++k) {
                    long long cost = m[i][k] + m[k + 1][j] + static_cast<long long>(p[i - 1]) * p[k] * p[j];
                    if (cost < m[i][j]) {
                        m[i][j] = cost;
                        s[i][j] = k;
                    }
                }
            }
        }

        result.min_multiplications = m[1][n];
        std::string parens;
        print_optimal_parens(1, n, s, parens);
        result.optimal_parenthesization = parens;

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
