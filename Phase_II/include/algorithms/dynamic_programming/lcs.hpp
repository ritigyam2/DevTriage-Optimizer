#pragma once

#include <string>
#include <vector>
#include <algorithm>
#include <chrono>

struct LCSResult {
    int length = 0;
    std::string lcs_string;
    double similarity_percentage = 0.0;
    double elapsed_microseconds = 0.0;
};

class LCSWorkbench {
public:
    // ------------------------------------------------------------------------
    // Longest Common Subsequence: Theta(m * n) time, Theta(m * n) aux space
    // Identifies duplicate bug reports, stack trace matches, and code diffs
    // ------------------------------------------------------------------------
    static LCSResult solve(const std::string& X, const std::string& Y) {
        LCSResult result;
        int m = static_cast<int>(X.size());
        int n = static_cast<int>(Y.size());
        if (m == 0 || n == 0) return result;

        auto start = std::chrono::high_resolution_clock::now();

        std::vector<std::vector<int>> c(m + 1, std::vector<int>(n + 1, 0));

        for (int i = 1; i <= m; ++i) {
            for (int j = 1; j <= n; ++j) {
                if (X[i - 1] == Y[j - 1]) {
                    c[i][j] = c[i - 1][j - 1] + 1;
                } else {
                    c[i][j] = std::max(c[i - 1][j], c[i][j - 1]);
                }
            }
        }

        result.length = c[m][n];

        // Backtrack to recover LCS string
        int i = m, j = n;
        std::string seq;
        while (i > 0 && j > 0) {
            if (X[i - 1] == Y[j - 1]) {
                seq.push_back(X[i - 1]);
                i--;
                j--;
            } else if (c[i - 1][j] >= c[i][j - 1]) {
                i--;
            } else {
                j--;
            }
        }
        std::reverse(seq.begin(), seq.end());
        result.lcs_string = seq;

        // Dice similarity coefficient: 2 * LCS / (|X| + |Y|)
        if (m + n > 0) {
            result.similarity_percentage = (200.0 * result.length) / (m + n);
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
