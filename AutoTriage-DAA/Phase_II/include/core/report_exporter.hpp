#pragma once

#include "models.hpp"
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

class ReportExporter {
public:
    static bool export_triage_csv(const std::string& filepath, const std::vector<Issue>& issues) {
        std::ofstream out(filepath);
        if (!out.is_open()) return false;

        out << "Issue_ID,Title,Severity,Estimated_Hours,Business_Value,Deadline_Day\n";
        for (const auto& it : issues) {
            out << it.id << ",\"" << it.title << "\"," << it.severity << "," 
                << it.estimated_hours << "," << it.business_value << "," << it.deadline_day << "\n";
        }
        out.close();
        return true;
    }

    static bool export_assignment_plan(const std::string& filepath, 
                                       const std::vector<Developer>& devs, 
                                       const std::vector<Issue>& issues) {
        std::ofstream out(filepath);
        if (!out.is_open()) return false;

        out << "Developer_ID,Developer_Name,Capacity_Hours,Assigned_Hours,Utilization_Percent,Assigned_Issue_Count\n";
        for (const auto& dev : devs) {
            double util = dev.available_hours > 0 ? (100.0 * dev.assigned_hours / dev.available_hours) : 0.0;
            out << dev.id << ",\"" << dev.name << "\"," << dev.available_hours << ","
                << dev.assigned_hours << "," << util << "," << dev.assigned_issue_ids.size() << "\n";
        }
        (void)issues;
        out.close();
        return true;
    }
};
