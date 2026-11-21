#pragma once

#include <vector>
#include <chrono>
#include <numeric>
#include <stdexcept>

struct CRTResult {
    long long solution = 0;
    long long combined_modulus = 0;
    bool is_valid = false;
    double elapsed_microseconds = 0.0;
};

class ChineseRemainderTheoremWorkbench {
public:
    // Extended Euclidean Algorithm: finds g = gcd(a, b) and x, y such that a*x + b*y = g
    static long long extended_gcd(long long a, long long b, long long& x, long long& y) {
        if (b == 0) {
            x = 1;
            y = 0;
            return a;
        }
        long long x1, y1;
        long long gcd = extended_gcd(b, a % b, x1, y1);
        x = y1;
        y = x1 - (a / b) * y1;
        return gcd;
    }

    // Modular inverse: a^(-1) mod m
    static long long mod_inverse(long long a, long long m) {
        long long x, y;
        long long g = extended_gcd(a, m, x, y);
        if (g != 1) {
            return -1; // Inverse does not exist (not coprime)
        }
        return (x % m + m) % m;
    }

    // ------------------------------------------------------------------------
    // Chinese Remainder Theorem: O(k log M)
    // Solves system x = a_i (mod m_i) where gcd(m_i, m_j) = 1
    // Used for distributed issue event counters and modular verification
    // ------------------------------------------------------------------------
    static CRTResult solve(const std::vector<long long>& remainders,
                           const std::vector<long long>& moduli) {
        CRTResult result;
        int k = static_cast<int>(remainders.size());
        if (k == 0 || k != static_cast<int>(moduli.size())) return result;

        auto start = std::chrono::high_resolution_clock::now();

        // 1. Verify pairwise coprimality and compute combined modulus M = prod m_i
        long long M = 1;
        for (int i = 0; i < k; ++i) {
            for (int j = i + 1; j < k; ++j) {
                long long x, y;
                if (extended_gcd(moduli[i], moduli[j], x, y) != 1) {
                    result.is_valid = false;
                    return result; // Not pairwise coprime
                }
            }
            M *= moduli[i];
        }

        // 2. Solve: x = sum (a_i * M_i * y_i) mod M
        long long x_total = 0;
        for (int i = 0; i < k; ++i) {
            long long M_i = M / moduli[i];
            long long y_i = mod_inverse(M_i, moduli[i]);
            if (y_i == -1) {
                result.is_valid = false;
                return result;
            }

            long long term = ((remainders[i] % M) * (M_i % M)) % M;
            term = (term * (y_i % M)) % M;
            x_total = (x_total + term) % M;
        }

        result.solution = (x_total % M + M) % M;
        result.combined_modulus = M;
        result.is_valid = true;

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
