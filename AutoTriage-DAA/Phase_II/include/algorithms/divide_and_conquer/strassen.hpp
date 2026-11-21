#pragma once

#include <vector>
#include <iostream>
#include <chrono>
#include <stdexcept>
#include <cmath>

class StrassenWorkbench {
public:
    using Matrix = std::vector<std::vector<long long>>;

    struct MatrixStats {
        long long scalar_multiplications = 0;
        long long scalar_additions = 0;
        double elapsed_microseconds = 0.0;
    };

    // Helper: Matrix Addition
    static Matrix add(const Matrix& A, const Matrix& B, MatrixStats& stats) {
        int n = static_cast<int>(A.size());
        Matrix C(n, std::vector<long long>(n, 0));
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                C[i][j] = A[i][j] + B[i][j];
                stats.scalar_additions++;
            }
        }
        return C;
    }

    // Helper: Matrix Subtraction
    static Matrix subtract(const Matrix& A, const Matrix& B, MatrixStats& stats) {
        int n = static_cast<int>(A.size());
        Matrix C(n, std::vector<long long>(n, 0));
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                C[i][j] = A[i][j] - B[i][j];
                stats.scalar_additions++; // Subtraction counted as additive operation
            }
        }
        return C;
    }

    // ------------------------------------------------------------------------
    // 1. Classical Matrix Multiplication: O(n^3)
    // ------------------------------------------------------------------------
    static Matrix classical_multiply(const Matrix& A, const Matrix& B, MatrixStats& stats) {
        int n = static_cast<int>(A.size());
        int m = static_cast<int>(A[0].size());
        int p = static_cast<int>(B[0].size());

        stats.scalar_multiplications = 0;
        stats.scalar_additions = 0;

        auto start = std::chrono::high_resolution_clock::now();

        Matrix C(n, std::vector<long long>(p, 0));
        for (int i = 0; i < n; ++i) {
            for (int k = 0; k < m; ++k) {
                for (int j = 0; j < p; ++j) {
                    C[i][j] += A[i][k] * B[k][j];
                    stats.scalar_multiplications++;
                    stats.scalar_additions++;
                }
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        stats.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return C;
    }

    // ------------------------------------------------------------------------
    // 2. Strassen's Matrix Multiplication: O(n^log2(7)) ~= O(n^2.807)
    // ------------------------------------------------------------------------
private:
    static Matrix strassen_recursive(const Matrix& A, const Matrix& B, MatrixStats& stats, int threshold) {
        int n = static_cast<int>(A.size());

        // Base case: switch to classical for small submatrices
        if (n <= threshold) {
            Matrix C(n, std::vector<long long>(n, 0));
            for (int i = 0; i < n; ++i) {
                for (int k = 0; k < n; ++k) {
                    for (int j = 0; j < n; ++j) {
                        C[i][j] += A[i][k] * B[k][j];
                        stats.scalar_multiplications++;
                        stats.scalar_additions++;
                    }
                }
            }
            return C;
        }

        int half = n / 2;
        Matrix A11(half, std::vector<long long>(half)), A12(half, std::vector<long long>(half)),
               A21(half, std::vector<long long>(half)), A22(half, std::vector<long long>(half)),
               B11(half, std::vector<long long>(half)), B12(half, std::vector<long long>(half)),
               B21(half, std::vector<long long>(half)), B22(half, std::vector<long long>(half));

        // Partition into 4 submatrices
        for (int i = 0; i < half; ++i) {
            for (int j = 0; j < half; ++j) {
                A11[i][j] = A[i][j];
                A12[i][j] = A[i][j + half];
                A21[i][j] = A[i + half][j];
                A22[i][j] = A[i + half][j + half];

                B11[i][j] = B[i][j];
                B12[i][j] = B[i][j + half];
                B21[i][j] = B[i + half][j];
                B22[i][j] = B[i + half][j + half];
            }
        }

        // Strassen's 7 submatrix products:
        // M1 = (A11 + A22) * (B11 + B22)
        Matrix M1 = strassen_recursive(add(A11, A22, stats), add(B11, B22, stats), stats, threshold);
        // M2 = (A21 + A22) * B11
        Matrix M2 = strassen_recursive(add(A21, A22, stats), B11, stats, threshold);
        // M3 = A11 * (B12 - B22)
        Matrix M3 = strassen_recursive(A11, subtract(B12, B22, stats), stats, threshold);
        // M4 = A22 * (B21 - B11)
        Matrix M4 = strassen_recursive(A22, subtract(B21, B11, stats), stats, threshold);
        // M5 = (A11 + A12) * B22
        Matrix M5 = strassen_recursive(add(A11, A12, stats), B22, stats, threshold);
        // M6 = (A21 - A11) * (B11 + B12)
        Matrix M6 = strassen_recursive(subtract(A21, A11, stats), add(B11, B12, stats), stats, threshold);
        // M7 = (A12 - A22) * (B21 + B22)
        Matrix M7 = strassen_recursive(subtract(A12, A22, stats), add(B21, B22, stats), stats, threshold);

        // Submatrix assembly:
        // C11 = M1 + M4 - M5 + M7
        Matrix C11 = add(subtract(add(M1, M4, stats), M5, stats), M7, stats);
        // C12 = M3 + M5
        Matrix C12 = add(M3, M5, stats);
        // C21 = M2 + M4
        Matrix C21 = add(M2, M4, stats);
        // C22 = M1 - M2 + M3 + M6
        Matrix C22 = add(add(subtract(M1, M2, stats), M3, stats), M6, stats);

        // Recombine into C
        Matrix C(n, std::vector<long long>(n, 0));
        for (int i = 0; i < half; ++i) {
            for (int j = 0; j < half; ++j) {
                C[i][j] = C11[i][j];
                C[i][j + half] = C12[i][j];
                C[i + half][j] = C21[i][j];
                C[i + half][j + half] = C22[i][j];
            }
        }
        return C;
    }

public:
    static Matrix strassen_multiply(const Matrix& A, const Matrix& B, MatrixStats& stats, int threshold = 2) {
        stats.scalar_multiplications = 0;
        stats.scalar_additions = 0;

        int orig_n = static_cast<int>(A.size());
        // Pad to next power of 2 for clean divide-and-conquer
        int p = 1;
        while (p < orig_n) p *= 2;

        Matrix A_pad(p, std::vector<long long>(p, 0));
        Matrix B_pad(p, std::vector<long long>(p, 0));
        for (int i = 0; i < orig_n; ++i) {
            for (int j = 0; j < orig_n; ++j) {
                A_pad[i][j] = A[i][j];
                B_pad[i][j] = B[i][j];
            }
        }

        auto start = std::chrono::high_resolution_clock::now();
        Matrix C_pad = strassen_recursive(A_pad, B_pad, stats, threshold);
        auto end = std::chrono::high_resolution_clock::now();
        stats.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();

        // Extract original submatrix
        Matrix C(orig_n, std::vector<long long>(orig_n, 0));
        for (int i = 0; i < orig_n; ++i) {
            for (int j = 0; j < orig_n; ++j) {
                C[i][j] = C_pad[i][j];
            }
        }
        return C;
    }

    // ------------------------------------------------------------------------
    // Domain Role: Developer Co-Maintenance Intensity Matrix
    // Computes M = C * C^T where C is Developer-Module contribution matrix
    // ------------------------------------------------------------------------
    static Matrix compute_developer_co_maintenance(const Matrix& dev_module_matrix, MatrixStats& stats, bool use_strassen = true) {
        int devs = static_cast<int>(dev_module_matrix.size());
        int modules = static_cast<int>(dev_module_matrix[0].size());

        // Transpose C -> C^T (modules x devs)
        Matrix C_T(modules, std::vector<long long>(devs, 0));
        for (int i = 0; i < devs; ++i) {
            for (int j = 0; j < modules; ++j) {
                C_T[j][i] = dev_module_matrix[i][j];
            }
        }

        // To use square Strassen: pad C and C_T to max(devs, modules) square
        int dim = std::max(devs, modules);
        Matrix A_sq(dim, std::vector<long long>(dim, 0));
        Matrix B_sq(dim, std::vector<long long>(dim, 0));
        for (int i = 0; i < devs; ++i) {
            for (int j = 0; j < modules; ++j) {
                A_sq[i][j] = dev_module_matrix[i][j];
                B_sq[j][i] = C_T[j][i];
            }
        }

        Matrix res_sq;
        if (use_strassen) {
            res_sq = strassen_multiply(A_sq, B_sq, stats);
        } else {
            res_sq = classical_multiply(A_sq, B_sq, stats);
        }

        Matrix result(devs, std::vector<long long>(devs, 0));
        for (int i = 0; i < devs; ++i) {
            for (int j = 0; j < devs; ++j) {
                result[i][j] = res_sq[i][j];
            }
        }
        return result;
    }
};
