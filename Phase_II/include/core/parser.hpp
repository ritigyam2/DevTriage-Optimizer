#pragma once

#include "models.hpp"
#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <cctype>
#include <unordered_map>
#include <functional>

class DataParser {
private:
    static std::vector<std::string> parse_csv_line(const std::string& line) {
        std::vector<std::string> fields;
        std::string field;
        bool in_quotes = false;
        for (size_t i = 0; i < line.size(); ++i) {
            char c = line[i];
            if (c == '"') {
                in_quotes = !in_quotes;
            } else if (c == ',' && !in_quotes) {
                fields.push_back(field);
                field.clear();
            } else {
                field += c;
            }
        }
        fields.push_back(field);
        return fields;
    }

    static int parse_id_field(const std::string& str) {
        std::string digits;
        for (char c : str) {
            if (isdigit(static_cast<unsigned char>(c))) digits += c;
        }
        return digits.empty() ? 0 : std::stoi(digits);
    }

    static std::vector<std::string> split_skills(const std::string& str) {
        std::vector<std::string> result;
        std::string current;
        for (char ch : str) {
            if (ch == ';' || ch == ',') {
                if (!current.empty()) {
                    result.push_back(current);
                    current.clear();
                }
            } else if (ch != ' ' && ch != '\t' && ch != '\r' && ch != '"') {
                current += ch;
            }
        }
        if (!current.empty()) result.push_back(current);
        return result;
    }

    static bool check_circular_prerequisites(const std::vector<Issue>& issues, std::string& error_msg) {
        std::unordered_map<int, int> id_to_idx;
        for (size_t i = 0; i < issues.size(); ++i) {
            id_to_idx[issues[i].id] = static_cast<int>(i);
        }

        int n = static_cast<int>(issues.size());
        std::vector<int> state(n, 0);

        std::function<bool(int)> dfs = [&](int u) -> bool {
            state[u] = 1;
            for (int prereq_id : issues[u].prerequisites) {
                auto it = id_to_idx.find(prereq_id);
                if (it == id_to_idx.end()) continue;
                int v = it->second;
                if (state[v] == 1) {
                    error_msg = "Circular prerequisite dependency detected between Issue #" + 
                                std::to_string(issues[u].id) + " and Issue #" + std::to_string(issues[v].id);
                    return true;
                }
                if (state[v] == 0) {
                    if (dfs(v)) return true;
                }
            }
            state[u] = 2;
            return false;
        };

        for (int i = 0; i < n; ++i) {
            if (state[i] == 0) {
                if (dfs(i)) return true;
            }
        }
        return false;
    }

public:
    static bool parse_issues(const std::string& filepath, std::vector<Issue>& issues, std::string& error_msg) {
        issues.clear();
        std::ifstream file(filepath);
        if (!file.is_open()) {
            error_msg = "Error: Unable to open file: " + filepath;
            return false;
        }

        std::string line;
        int line_num = 0;
        bool header_skipped = false;

        while (std::getline(file, line)) {
            line_num++;
            if (line.empty() || line[0] == '#') continue;

            if (!header_skipped) {
                header_skipped = true;
                if (line.find("id") != std::string::npos || line.find("severity") != std::string::npos) {
                    continue;
                }
            }

            std::vector<std::string> cols = parse_csv_line(line);
            if (cols.size() < 7) {
                error_msg = "Line " + std::to_string(line_num) + ": Missing required comma-separated columns.";
                return false;
            }

            Issue issue;
            try {
                issue.id = parse_id_field(cols[0]);
                issue.title = cols[1];
                issue.severity = std::stoi(cols[2]);
                issue.estimated_hours = std::stoi(cols[3]);
                issue.business_value = std::stod(cols[4]);
                issue.deadline_day = std::stoi(cols[5]);
            } catch (...) {
                error_msg = "Line " + std::to_string(line_num) + ": Numeric conversion failure.";
                return false;
            }

            if (issue.id <= 0 || issue.severity < 1 || issue.severity > 5 || issue.estimated_hours <= 0) {
                error_msg = "Line " + std::to_string(line_num) + ": Severity must be in range [1, 5]. Found: " + std::to_string(issue.severity);
                return false;
            }

            issue.skills = split_skills(cols[6]);

            if (cols.size() >= 8 && !cols[7].empty()) {
                std::stringstream pss(cols[7]);
                std::string pid_token;
                while (std::getline(pss, pid_token, ';')) {
                    if (!pid_token.empty()) {
                        int pid = parse_id_field(pid_token);
                        if (pid > 0) issue.prerequisites.push_back(pid);
                    }
                }
            }

            issues.push_back(issue);
        }

        if (check_circular_prerequisites(issues, error_msg)) {
            return false;
        }

        return true;
    }

    static bool parse_developers(const std::string& filepath, std::vector<Developer>& devs, std::string& error_msg) {
        devs.clear();
        std::ifstream file(filepath);
        if (!file.is_open()) {
            error_msg = "Error: Unable to open file: " + filepath;
            return false;
        }

        std::string line;
        int line_num = 0;
        bool header_skipped = false;

        while (std::getline(file, line)) {
            line_num++;
            if (line.empty() || line[0] == '#') continue;

            if (!header_skipped) {
                header_skipped = true;
                if (line.find("id") != std::string::npos || line.find("name") != std::string::npos) {
                    continue;
                }
            }

            std::vector<std::string> cols = parse_csv_line(line);
            if (cols.size() < 4) {
                error_msg = "Line " + std::to_string(line_num) + ": Developer record format invalid.";
                return false;
            }

            Developer dev;
            try {
                dev.id = parse_id_field(cols[0]);
                dev.name = cols[1];
                dev.available_hours = std::stoi(cols[2]);
                dev.assigned_hours = 0;
            } catch (...) {
                error_msg = "Line " + std::to_string(line_num) + ": Developer numeric conversion failure.";
                return false;
            }

            if (dev.id <= 0 || dev.available_hours < 0) {
                error_msg = "Line " + std::to_string(line_num) + ": Invalid developer attributes.";
                return false;
            }

            dev.skills = split_skills(cols[3]);
            devs.push_back(dev);
        }
        return true;
    }
};
