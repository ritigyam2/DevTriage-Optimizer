#pragma once

#include "../../core/models.hpp"
#include "../../core/visualizer.hpp"
#include "../flow_matching/bipartite_matching.hpp"
#include <vector>
#include <string>
#include <iostream>
#include <iomanip>
#include <algorithm>

struct StreamEvent {
    int arrival_time_hour;
    Issue issue;
    bool is_emergency_cve;
};

struct PreemptionRecord {
    int hour;
    int dev_id;
    std::string dev_name;
    int preempted_issue_id;
    int preempted_severity;
    int emergency_issue_id;
};

struct OnlineStreamingReport {
    int total_arrivals = 0;
    int online_accepted = 0;
    int online_rejected = 0;
    int preemptions_triggered = 0;
    int offline_optimal_matches = 0;
    double competitive_ratio = 0.0;
    std::vector<PreemptionRecord> preemption_log;
};

class OnlineStreamingEngine {
public:
    static OnlineStreamingReport simulate_online_stream(
        std::vector<Developer> devs,
        const std::vector<StreamEvent>& stream,
        bool enable_preemption = true) {

        OnlineStreamingReport report;
        report.total_arrivals = static_cast<int>(stream.size());

        for (const auto& event : stream) {
            const Issue& incoming = event.issue;
            bool matched = false;
            int chosen_dev_idx = -1;

            for (size_t d = 0; d < devs.size(); ++d) {
                if (devs[d].has_skill(incoming.skills.empty() ? "" : incoming.skills[0])) {
                    if (devs[d].remaining_capacity() >= incoming.estimated_hours) {
                        chosen_dev_idx = static_cast<int>(d);
                        break;
                    }
                }
            }

            if (chosen_dev_idx != -1) {
                devs[chosen_dev_idx].assigned_hours += incoming.estimated_hours;
                devs[chosen_dev_idx].assigned_issue_ids.push_back(incoming.id);
                report.online_accepted++;
                matched = true;
            } else if (enable_preemption && (event.is_emergency_cve || incoming.severity == 5)) {
                int best_dev_idx = -1;
                int target_preempt_issue_id = -1;

                for (size_t d = 0; d < devs.size(); ++d) {
                    if (devs[d].has_skill(incoming.skills.empty() ? "" : incoming.skills[0])) {
                        for (int in_flight_id : devs[d].assigned_issue_ids) {
                            if (in_flight_id > 0) {
                                best_dev_idx = static_cast<int>(d);
                                target_preempt_issue_id = in_flight_id;
                                break;
                            }
                        }
                    }
                    if (best_dev_idx != -1) break;
                }

                if (best_dev_idx != -1) {
                    auto& dev_issues = devs[best_dev_idx].assigned_issue_ids;
                    dev_issues.erase(std::remove(dev_issues.begin(), dev_issues.end(), target_preempt_issue_id), dev_issues.end());
                    dev_issues.push_back(incoming.id);

                    PreemptionRecord rec;
                    rec.hour = event.arrival_time_hour;
                    rec.dev_id = devs[best_dev_idx].id;
                    rec.dev_name = devs[best_dev_idx].name;
                    rec.preempted_issue_id = target_preempt_issue_id;
                    rec.preempted_severity = 2;
                    rec.emergency_issue_id = incoming.id;
                    report.preemption_log.push_back(rec);

                    report.preemptions_triggered++;
                    report.online_accepted++;
                    matched = true;
                }
            }

            if (!matched) {
                report.online_rejected++;
            }
        }

        int n_issues = static_cast<int>(stream.size());
        int n_devs = static_cast<int>(devs.size());
        std::vector<std::vector<int>> compat(n_issues);
        for (int i = 0; i < n_issues; ++i) {
            for (int d = 0; d < n_devs; ++d) {
                if (devs[d].has_skill(stream[i].issue.skills.empty() ? "" : stream[i].issue.skills[0])) {
                    compat[i].push_back(d);
                }
            }
        }

        BipartiteAssignmentResult offline_stats = BipartiteFlowWorkbench::solve(n_issues, n_devs, compat);
        report.offline_optimal_matches = std::max(report.online_accepted, offline_stats.max_matched);

        if (report.offline_optimal_matches > 0) {
            report.competitive_ratio = static_cast<double>(report.online_accepted) / report.offline_optimal_matches;
        } else {
            report.competitive_ratio = 1.0;
        }

        return report;
    }
};
