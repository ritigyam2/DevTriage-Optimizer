#pragma once

#include <string>
#include <vector>
#include <queue>
#include <unordered_map>
#include <chrono>

struct HuffmanNode {
    char ch;
    int freq;
    HuffmanNode* left = nullptr;
    HuffmanNode* right = nullptr;

    HuffmanNode(char c, int f) : ch(c), freq(f), left(nullptr), right(nullptr) {}
    HuffmanNode(int f, HuffmanNode* l, HuffmanNode* r) : ch('\0'), freq(f), left(l), right(r) {}

    ~HuffmanNode() {
        delete left;
        delete right;
    }
};

struct CompareNode {
    bool operator()(const HuffmanNode* a, const HuffmanNode* b) const {
        return a->freq > b->freq; // Min-heap by frequency
    }
};

struct HuffmanResult {
    std::string encoded_bits;
    std::string decoded_text;
    std::unordered_map<char, std::string> codebook;
    size_t original_bits = 0;
    size_t compressed_bits = 0;
    double compression_ratio = 0.0;
    double elapsed_microseconds = 0.0;
};

class HuffmanWorkbench {
private:
    static void generate_codes(const HuffmanNode* root, const std::string& current_code,
                               std::unordered_map<char, std::string>& codebook) {
        if (!root) return;
        // Leaf node contains character
        if (!root->left && !root->right) {
            codebook[root->ch] = current_code.empty() ? "0" : current_code;
            return;
        }
        generate_codes(root->left, current_code + "0", codebook);
        generate_codes(root->right, current_code + "1", codebook);
    }

public:
    // ------------------------------------------------------------------------
    // Huffman Encoding: O(n log Sigma) time, O(Sigma) aux space
    // Lossless compression for offline git diffs, logs, and stack traces
    // ------------------------------------------------------------------------
    static HuffmanResult compress_and_decompress(const std::string& text) {
        HuffmanResult result;
        if (text.empty()) return result;

        auto start = std::chrono::high_resolution_clock::now();

        // 1. Compute character frequency table
        std::unordered_map<char, int> freq_map;
        for (char c : text) {
            freq_map[c]++;
        }

        // 2. Build Min-Heap of leaf nodes
        std::priority_queue<HuffmanNode*, std::vector<HuffmanNode*>, CompareNode> min_heap;
        for (const auto& pair : freq_map) {
            min_heap.push(new HuffmanNode(pair.first, pair.second));
        }

        // 3. Repeatedly merge two lowest-frequency nodes
        while (min_heap.size() > 1) {
            HuffmanNode* left = min_heap.top(); min_heap.pop();
            HuffmanNode* right = min_heap.top(); min_heap.pop();

            HuffmanNode* parent = new HuffmanNode(left->freq + right->freq, left, right);
            min_heap.push(parent);
        }

        HuffmanNode* root = min_heap.top();

        // 4. Generate prefix-free codes
        generate_codes(root, "", result.codebook);

        // 5. Encode original text to bitstring
        for (char c : text) {
            result.encoded_bits += result.codebook[c];
        }

        // 6. Decode bitstring back to text to verify lossless reconstruction
        std::string decoded;
        const HuffmanNode* curr = root;
        for (char bit : result.encoded_bits) {
            if (bit == '0') {
                curr = curr->left ? curr->left : curr;
            } else {
                curr = curr->right ? curr->right : curr;
            }
            if (!curr->left && !curr->right) {
                decoded += curr->ch;
                curr = root;
            }
        }
        result.decoded_text = decoded;

        // Cleanup tree
        delete root;

        auto end = std::chrono::high_resolution_clock::now();
        result.original_bits = text.size() * 8;
        result.compressed_bits = result.encoded_bits.size();
        result.compression_ratio = result.compressed_bits > 0 ?
            (static_cast<double>(result.original_bits) / result.compressed_bits) : 0.0;
        result.elapsed_microseconds = std::chrono::duration<double, std::micro>(end - start).count();

        return result;
    }
};
