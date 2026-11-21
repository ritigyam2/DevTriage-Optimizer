#pragma once

#include "models.hpp"
#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <algorithm>

class TerminalVisualizer {
public:
    static std::string progress_bar(int current, int total, int width = 20) {
        if (total <= 0) total = 1;
        double ratio = std::max(0.0, std::min(1.0, static_cast<double>(current) / total));
        int filled = static_cast<int>(ratio * width);
        std::string bar = "[";
        for (int i = 0; i < filled; ++i) bar += "=";
        if (filled < width) bar += ">";
        for (int i = filled + 1; i < width; ++i) bar += " ";
        bar += "]";
        std::ostringstream ss;
        ss << bar << " " << std::setw(3) << static_cast<int>(ratio * 100) << "%";
        return ss.str();
    }

    static void print_developer_workload(const std::vector<Developer>& devs) {
        std::cout << "\n+-----------------------------------------------------------------------------------------+\n";
        std::cout << "|                          DEVELOPER SPRINT CAPACITY UTILIZATION                          |\n";
        std::cout << "+----+------------------------+----------+----------+--------------------+----------------+\n";
        std::cout << "| ID | Name                   | Capacity | Assigned | Utilization Bar    | Issues In-Flight|\n";
        std::cout << "+----+------------------------+----------+----------+--------------------+----------------+\n";

        for (const auto& dev : devs) {
            std::string pbar = progress_bar(dev.assigned_hours, dev.available_hours, 12);
            std::cout << "| " << std::setw(2) << dev.id << " | "
                      << std::left << std::setw(22) << dev.name.substr(0, 22) << " | "
                      << std::right << std::setw(6) << dev.available_hours << "h | "
                      << std::setw(6) << dev.assigned_hours << "h | "
                      << std::left << std::setw(18) << pbar << " | "
                      << std::setw(14) << (std::to_string(dev.assigned_issue_ids.size()) + " assigned") << " |\n";
        }
        std::cout << "+----+------------------------+----------+----------+--------------------+----------------+\n";
    }

    static void print_ascii_gantt_chart(const std::vector<Developer>& devs, 
                                        const std::vector<Issue>& /* issues */, 
                                        int total_days = 10) {
        std::cout << "\n=========================================================================================\n";
        std::cout << "                 SPRINT SCHEDULE GANTT TIMELINE MATRIX (10-DAY HORIZON)                  \n";
        std::cout << "=========================================================================================\n";
        std::cout << "Developer              ";
        for (int d = 1; d <= total_days; ++d) {
            std::cout << "| D" << std::setw(2) << d << " ";
        }
        std::cout << "|\n-----------------------";
        for (int d = 1; d <= total_days; ++d) {
            std::cout << "+-----";
        }
        std::cout << "+\n";

        for (const auto& dev : devs) {
            std::cout << std::left << std::setw(22) << dev.name.substr(0, 22) << " ";
            int remaining_work_hours = dev.assigned_hours;
            for (int d = 1; d <= total_days; ++d) {
                if (remaining_work_hours >= 4) {
                    std::cout << "| [X] ";
                    remaining_work_hours -= 4; // 4 hours per day slot
                } else if (remaining_work_hours > 0) {
                    std::cout << "| [/] ";
                    remaining_work_hours = 0;
                } else {
                    std::cout << "|  .  "; // Free / Idle
                }
            }
            std::cout << "|\n";
        }
        std::cout << "-----------------------------------------------------------------------------------------\n";
        std::cout << "Legend: [X] Full Day Slot (4h)  |  [/] Partial Slot  |  . Idle / Spare Capacity Available\n";
    }

    static void print_banner(const std::string& title) {
        int len = static_cast<int>(title.size()) + 4;
        std::string border(len, '=');
        std::cout << "\n" << border << "\n";
        std::cout << "= " << title << " =\n";
        std::cout << border << "\n";
    }
};
