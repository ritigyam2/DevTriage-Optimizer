#pragma once

#include <string>
#include <vector>
#include <chrono>

struct StringMatchResult {
    std::string algorithm_name;
    std::vector<int> match_indices;
    long long comparisons = 0;
    double elapsed_microseconds = 0.0;
};

class StringMatchingWorkbench {
public:
    // ------------------------------------------------------------------------
    // 1. Naive String Matching (L42): O((n - m + 1) * m)
    // ------------------------------------------------------------------------
    static StringMatchResult naive_search(const std::string& text, const std::string& pattern) {
        StringMatchResult result;
        result.algorithm_name = "Naive String Matcher";
        int n = static_cast<int>(text.size());
        int m = static_cast<int>(pattern.size());
        if (m == 0 || n < m) return result;

        auto start = std::chrono::high_resolution_clock::now();

        for (int s = 0; s <= n - m; ++s) {
            bool match = true;
            for (int j = 0; j < m; ++j) {
                result.comparisons++;
                if (text[s + j] != pattern[j]) {
                    match = false;
                    break;
                }
            }
            if (match) {
                result.match_indices.push_back(s);
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }

    // ------------------------------------------------------------------------
    // 2. Rabin-Karp Algorithm (L43): Rolling Hash, Avg O(n + m), Worst O(n * m)
    // ------------------------------------------------------------------------
    static StringMatchResult rabin_karp_search(const std::string& text, const std::string& pattern,
                                               long long d = 256, long long q = 1000000007) {
        StringMatchResult result;
        result.algorithm_name = "Rabin-Karp Rolling Hash";
        int n = static_cast<int>(text.size());
        int m = static_cast<int>(pattern.size());
        if (m == 0 || n < m) return result;

        auto start = std::chrono::high_resolution_clock::now();

        long long h = 1;
        // h = d^(m-1) mod q
        for (int i = 0; i < m - 1; ++i) {
            h = (h * d) % q;
        }

        long long p = 0; // Hash of pattern
        long long t = 0; // Hash of text window

        for (int i = 0; i < m; ++i) {
            p = (d * p + static_cast<unsigned char>(pattern[i])) % q;
            t = (d * t + static_cast<unsigned char>(text[i])) % q;
        }

        for (int s = 0; s <= n - m; ++s) {
            if (p == t) {
                // Check for spurious hit
                bool match = true;
                for (int j = 0; j < m; ++j) {
                    result.comparisons++;
                    if (text[s + j] != pattern[j]) {
                        match = false;
                        break;
                    }
                }
                if (match) {
                    result.match_indices.push_back(s);
                }
            }

            if (s < n - m) {
                t = (d * (t - static_cast<unsigned char>(text[s]) * h) + static_cast<unsigned char>(text[s + m])) % q;
                if (t < 0) t = (t + q);
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }

    // ------------------------------------------------------------------------
    // 3. String Matching with Finite Automata (L44): Preprocessing O(m^3 |Sigma|), Match Theta(n)
    // ------------------------------------------------------------------------
    static StringMatchResult finite_automata_search(const std::string& text, const std::string& pattern) {
        StringMatchResult result;
        result.algorithm_name = "Finite Automaton (DFA)";
        int n = static_cast<int>(text.size());
        int m = static_cast<int>(pattern.size());
        if (m == 0 || n < m) return result;

        auto start = std::chrono::high_resolution_clock::now();

        // Alphabet size (ASCII 128)
        const int ALPHABET_SIZE = 128;
        std::vector<std::vector<int>> transition(m + 1, std::vector<int>(ALPHABET_SIZE, 0));

        // Build transition table delta(q, a)
        for (int q = 0; q <= m; ++q) {
            for (int a = 0; a < ALPHABET_SIZE; ++a) {
                char ch = static_cast<char>(a);
                if (q < m && ch == pattern[q]) {
                    transition[q][a] = q + 1;
                } else {
                    // Longest prefix of pattern that is a suffix of P[0..q-1] + ch
                    for (int k = q; k > 0; --k) {
                        if (pattern[k - 1] == ch) {
                            bool is_suffix = true;
                            for (int i = 0; i < k - 1; ++i) {
                                if (pattern[i] != pattern[q - (k - 1) + i]) {
                                    is_suffix = false;
                                    break;
                                }
                            }
                            if (is_suffix) {
                                transition[q][a] = k;
                                break;
                            }
                        }
                    }
                }
            }
        }

        // Match text in strictly linear time
        int q = 0;
        for (int i = 0; i < n; ++i) {
            unsigned char ch = static_cast<unsigned char>(text[i]);
            int idx = (ch < ALPHABET_SIZE) ? ch : 0;
            q = transition[q][idx];
            result.comparisons++;
            if (q == m) {
                result.match_indices.push_back(i - m + 1);
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }

    // ------------------------------------------------------------------------
    // 4. Knuth-Morris-Pratt (KMP) Algorithm (L45): Preprocessing Theta(m), Match Theta(n)
    // ------------------------------------------------------------------------
    static std::vector<int> compute_prefix_function(const std::string& pattern, long long& comps) {
        int m = static_cast<int>(pattern.size());
        std::vector<int> pi(m, 0);
        int k = 0;

        for (int q = 1; q < m; ++q) {
            while (k > 0 && pattern[k] != pattern[q]) {
                comps++;
                k = pi[k - 1];
            }
            comps++;
            if (pattern[k] == pattern[q]) {
                k++;
            }
            pi[q] = k;
        }
        return pi;
    }

    static StringMatchResult kmp_search(const std::string& text, const std::string& pattern) {
        StringMatchResult result;
        result.algorithm_name = "Knuth-Morris-Pratt (KMP)";
        int n = static_cast<int>(text.size());
        int m = static_cast<int>(pattern.size());
        if (m == 0 || n < m) return result;

        auto start = std::chrono::high_resolution_clock::now();

        std::vector<int> pi = compute_prefix_function(pattern, result.comparisons);
        int q = 0; // Number of characters matched

        for (int i = 0; i < n; ++i) {
            while (q > 0 && pattern[q] != text[i]) {
                result.comparisons++;
                q = pi[q - 1]; // Shift without backtracking text pointer i
            }
            result.comparisons++;
            if (pattern[q] == text[i]) {
                q++;
            }
            if (q == m) {
                result.match_indices.push_back(i - m + 1);
                q = pi[q - 1]; // Look for next match
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();
        return result;
    }
};
