#pragma once

#include <vector>
#include <chrono>
#include <stdexcept>
#include <iostream>

class FastPowerWorkbench {
public:
    using Matrix = std::vector<std::vector<double>>;

    struct PowerStats {
        long long multiplications = 0;
        double elapsed_microseconds = 0.0;
    };

    // ------------------------------------------------------------------------
    // 1. Scalar Binary Exponentiation: a^n mod m in O(log n)
    // ------------------------------------------------------------------------
    static long long power_scalar(long long base, long long exp, long long mod, PowerStats& stats) {
        stats.multiplications = 0;
        auto start = std::chrono::high_resolution_clock::now();

        long long result = 1;
        base = base % mod;

        while (exp > 0) {
            if (exp % 2 == 1) {
                result = (result * base) % mod;
                stats.multiplications++;
            }
            base = (base * base) % mod;
            stats.multiplications++;
            exp /= 2;
        }

        auto end = std::chrono::high_resolution_clock::now();
        stats.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }

    // Helper: Matrix Multiplication for probabilities
    static Matrix multiply_matrices(const Matrix& A, const Matrix& B, PowerStats& stats) {
        int n = static_cast<int>(A.size());
        Matrix C(n, std::vector<double>(n, 0.0));
        for (int i = 0; i < n; ++i) {
            for (int k = 0; k < n; ++k) {
                for (int j = 0; j < n; ++j) {
                    C[i][j] += A[i][k] * B[k][j];
                    stats.multiplications++;
                }
            }
        }
        return C;
    }

    // ------------------------------------------------------------------------
    // 2. Fast Matrix Exponentiation: M^k in O(m^3 log k)
    // ------------------------------------------------------------------------
    static Matrix power_matrix(Matrix base, int exp, PowerStats& stats) {
        stats.multiplications = 0;
        int n = static_cast<int>(base.size());

        auto start = std::chrono::high_resolution_clock::now();

        // Initialize Identity Matrix I_n
        Matrix result(n, std::vector<double>(n, 0.0));
        for (int i = 0; i < n; ++i) result[i][i] = 1.0;

        while (exp > 0) {
            if (exp % 2 == 1) {
                result = multiply_matrices(result, base, stats);
            }
            base = multiply_matrices(base, base, stats);
            exp /= 2;
        }

        auto end = std::chrono::high_resolution_clock::now();
        stats.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }

    // ------------------------------------------------------------------------
    // Domain Role: Markov-Chain Issue Lifecycle Prediction
    // States: 0=TRIAGE, 1=DEVELOPMENT, 2=REVIEW, 3=RESOLVED
    // Multiplies initial issue distribution vector by P^k in O(log k)
    // ------------------------------------------------------------------------
    static std::vector<double> predict_issue_lifecycle(const Matrix& transition_matrix,
                                                      int sprint_cycles,
                                                      const std::vector<double>& initial_dist,
                                                      PowerStats& stats) {
        Matrix P_k = power_matrix(transition_matrix, sprint_cycles, stats);
        int n = static_cast<int>(initial_dist.size());

        std::vector<double> final_dist(n, 0.0);
        for (int j = 0; j < n; ++j) {
            for (int i = 0; i < n; ++i) {
                final_dist[j] += initial_dist[i] * P_k[i][j];
            }
        }
        return final_dist;
    }
};
