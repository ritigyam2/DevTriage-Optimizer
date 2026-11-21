#include "../include/algorithms/greedy/fractional_knapsack.hpp"
#include "../include/algorithms/greedy/activity_selection.hpp"
#include "../include/algorithms/greedy/interval_partitioning.hpp"
#include "../include/algorithms/greedy/huffman.hpp"
#include "../include/algorithms/greedy/dijkstra.hpp"
#include "../include/algorithms/greedy/mst.hpp"

#include <iostream>
#include <cassert>
#include <vector>
#include <cmath>

void test_fractional_knapsack() {
    std::cout << "[TEST 1] Running Fractional Knapsack Test...";

    std::vector<FractionalItem> items = {
        {1, 10.0, 60.0},  // density = 6.0
        {2, 20.0, 100.0}, // density = 5.0
        {3, 30.0, 120.0}  // density = 4.0
    };

    double capacity = 50.0;
    FractionalResult res = FractionalKnapsackWorkbench::solve(items, capacity);

    // Greedily: Item 1 (10kg, $60) + Item 2 (20kg, $100) + 20/30 of Item 3 (20kg, $80) = $240.0
    assert(std::fabs(res.total_value - 240.0) < 1e-4);
    assert(std::fabs(res.total_weight_used - 50.0) < 1e-4);
    assert(res.selected_items.size() == 3);
    assert(std::fabs(res.selected_items[2].fraction_taken - (20.0 / 30.0)) < 1e-4);

    std::cout << " PASSED! (Total Value: $" << res.total_value << " for 50 hours capacity)\n";
}

void test_activity_selection() {
    std::cout << "[TEST 2] Running Activity Selection (Single Reviewer) Test...";

    std::vector<Activity> activities = {
        {1, 1, 4},
        {2, 3, 5},
        {3, 0, 6},
        {4, 5, 7},
        {5, 3, 9},
        {6, 5, 9},
        {7, 6, 10},
        {8, 8, 11},
        {9, 8, 12},
        {10, 2, 14},
        {11, 12, 16}
    };

    ActivityResult res = ActivitySelectionWorkbench::solve(activities);

    // Optimal non-overlapping schedule has 4 activities: e.g., (1,4), (5,7), (8,11), (12,16)
    assert(res.count == 4);
    for (size_t i = 1; i < res.scheduled_activities.size(); ++i) {
        assert(res.scheduled_activities[i].start_time >= res.scheduled_activities[i - 1].finish_time);
    }

    std::cout << " PASSED! (Scheduled " << res.count << " non-overlapping review sessions)\n";
}

void test_interval_partitioning() {
    std::cout << "[TEST 3] Running Interval Partitioning (CI Servers) Test...";

    // 5 intervals. Intervals 1, 2, 3 all overlap at time 4 => maximum depth d = 3
    std::vector<Interval> intervals = {
        {1, 1, 5},  // Overlaps at 4
        {2, 2, 6},  // Overlaps at 4
        {3, 3, 7},  // Overlaps at 4
        {4, 6, 9},
        {5, 8, 10}
    };

    PartitionResult res = IntervalPartitioningWorkbench::solve(intervals);

    // Maximum depth is 3, so exactly 3 servers are required
    assert(res.total_rooms_needed == 3);
    assert(res.assigned_intervals.size() == 5);

    std::cout << " PASSED! (Allocated all tasks across exactly " << res.total_rooms_needed << " servers)\n";
}

void test_huffman_encoding() {
    std::cout << "[TEST 4] Running Huffman Encoding (Lossless Compression) Test...";

    std::string text = "OPEN_SOURCE_ISSUE_TRIAGE_AND_DEVELOPER_ASSIGNMENT_TOOL_CRASH_DUMP_LOG";
    HuffmanResult res = HuffmanWorkbench::compress_and_decompress(text);

    // 1. Lossless decoding verification
    assert(res.decoded_text == text);

    // 2. Compression verification
    assert(res.compressed_bits < res.original_bits);
    assert(res.compression_ratio > 1.0);

    // 3. Prefix-free verification: no code is prefix of another
    for (const auto& p1 : res.codebook) {
        for (const auto& p2 : res.codebook) {
            if (p1.first != p2.first) {
                // p1's code cannot start with p2's code
                if (p1.second.length() >= p2.second.length()) {
                    assert(p1.second.substr(0, p2.second.length()) != p2.second);
                }
            }
        }
    }

    std::cout << " PASSED! (Lossless verified. Original: " << res.original_bits 
              << " bits -> Compressed: " << res.compressed_bits 
              << " bits | Ratio: " << res.compression_ratio << "x)\n";
}

void test_dijkstra() {
    std::cout << "[TEST 5] Running Dijkstra's Shortest Path Test...";

    // 5-vertex graph:
    // 0 -> 1 (w=4), 0 -> 2 (w=2)
    // 1 -> 2 (w=1), 1 -> 3 (w=5)
    // 2 -> 3 (w=8), 2 -> 4 (w=10)
    // 3 -> 4 (w=2)
    DijkstraWorkbench::WeightedGraph adj(5);
    adj[0].push_back({1, 4.0});
    adj[0].push_back({2, 2.0});
    adj[1].push_back({2, 1.0});
    adj[1].push_back({3, 5.0});
    adj[2].push_back({3, 8.0});
    adj[2].push_back({4, 10.0});
    adj[3].push_back({4, 2.0});

    DijkstraResult res = DijkstraWorkbench::shortest_path(adj, 0);

    // Shortest path 0 -> 4: 0 -> 1 -> 3 -> 4: cost = 4 + 5 + 2 = 11.0 (or 0->2->... = 12.0)
    // Wait: 0 -> 1 is 4, 1 -> 3 is 5 (total 9), 3 -> 4 is 2 (total 11.0)
    assert(res.distances[0] == 0.0);
    assert(res.distances[1] == 4.0);
    assert(res.distances[2] == 2.0);
    assert(res.distances[3] == 9.0);
    assert(res.distances[4] == 11.0);

    auto path_to_4 = res.get_path(4);
    assert(path_to_4.size() == 4);
    assert(path_to_4[0] == 0 && path_to_4[1] == 1 && path_to_4[2] == 3 && path_to_4[3] == 4);

    std::cout << " PASSED! (Shortest path 0->4 distance: " << res.distances[4] << " via 0->1->3->4)\n";
}

void test_kruskal_and_prim_mst() {
    std::cout << "[TEST 6] Running Kruskal vs Prim Minimum Spanning Tree Test...";

    int V = 5;
    std::vector<Edge> edges = {
        {0, 1, 2.0},
        {0, 3, 6.0},
        {1, 2, 3.0},
        {1, 3, 8.0},
        {1, 4, 5.0},
        {2, 4, 7.0},
        {3, 4, 9.0}
    };

    // Adjacency for Prim (undirected)
    std::vector<std::vector<std::pair<int, double>>> adj(V);
    for (const auto& e : edges) {
        adj[e.u].push_back({e.v, e.weight});
        adj[e.v].push_back({e.u, e.weight});
    }

    MSTResult res_kruskal = MSTWorkbench::kruskal_mst(V, edges);
    MSTResult res_prim = MSTWorkbench::prim_mst(V, adj);

    // Both Kruskal and Prim MUST compute the exact same MST total weight!
    // MST edges: (0,1: 2), (1,2: 3), (1,4: 5), (0,3: 6) => Total weight = 2 + 3 + 5 + 6 = 16.0
    assert(res_kruskal.total_weight == 16.0);
    assert(res_prim.total_weight == 16.0);
    assert(res_kruskal.mst_edges.size() == 4);
    assert(res_prim.mst_edges.size() == 4);

    std::cout << " PASSED! (Kruskal & Prim both yield exact MST cost: " << res_kruskal.total_weight << ")\n";
}

int main() {
    std::cout << "\n=================================================================\n";
    std::cout << "  RUNNING CHUNK 3 AUTOMATED TEST SUITE (Greedy Methods Workbench)\n";
    std::cout << "=================================================================\n\n";

    test_fractional_knapsack();
    test_activity_selection();
    test_interval_partitioning();
    test_huffman_encoding();
    test_dijkstra();
    test_kruskal_and_prim_mst();

    std::cout << "\n=================================================================\n";
    std::cout << "  Test summary: 6/6 tests passed.\n";
    std::cout << "=================================================================\n\n";
    return 0;
}
