# Dataset Provenance, Schemas, and Licensing Statement
**Project Title:** Project 50: Open Source Issue Triage and Developer Assignment Tool (AutoTriage)  
**Academic Course:** Design and Analysis of Algorithms (DAA)  
**Offline Data Policy:** 100% Self-Contained, Local Storage, Open-Source Permissive Licensing  

---

## 1. Dataset Provenance & Data Engineering

AutoTriage utilizes two distinct tiers of dataset files to validate both baseline correctness and enterprise-scale robustness:

### Tier 1: Phase I Baseline Datasets (`Phase_I/data/`)
* **Purpose:** Academic correctness verification, boundary condition checks, and input rejection testing.
* **Files:**
  * `normal_issues.csv` (19 issues): Representative sample of common repository issues with varying severities ($1 \dots 5$), deadlines (Days $1 \dots 15$), estimated hours ($1 \dots 16\text{h}$), and business values (\$10.0 to \$98.0).
  * `normal_developers.csv` (8 developers): Maintainers with realistic weekly working capacities ($25 \dots 40\text{h}$) and multi-skill tags.
  * `boundary_issues.csv` (4 records): Tests boundary conditions including single-item backlogs, zero-capacity developers, single-hour tasks, and high-integer values.
  * `invalid_issues.csv` (3 records): Corrupted test inputs containing invalid severity levels ($s=9$), negative estimated hours ($-5\text{h}$), and malformed comma structures to verify defensive parser rejection.

### Tier 2: Phase II Synthetic Enterprise Benchmark Datasets (`Phase_II/data/`)
* **Purpose:** Realistic enterprise-scale stress testing, dynamic online streaming simulations, and developer capacity scheduling.
* **Dataset Type:** **Synthetic Benchmark Dataset.** Generated locally for reproducible academic benchmarking, inspired by realistic open-source defect taxonomies. No claim is made that the issue IDs or CVE strings correspond to active live security vulnerabilities.
* **Files:**
  * `synthetic_enterprise_issues.csv` (120 issues): Synthetic defect tickets, security vulnerability simulations, kernel panics, and compiler optimization bugs modeled after historical public issue trackers of tier-1 open-source systems:
    * **Linux Kernel Subsystem:** eBPF verifier use-after-free, NUMA spinlock starvation, ext4 journal data corruption.
    * **OpenSSL Security:** ASN.1 decoder stack overflows, TLS 1.3 handshake state machine RCEs, ECDSA side-channel timing leaks.
    * **Chromium / V8 Engine:** JIT optimization heap write vulnerabilities, GC stop-the-world pauses exceeding 250ms SLA.
    * **Kubernetes / Cloud Infrastructure:** Pod sandbox CNI network bridge panics, Etcd key-value compaction deadlocks.
    * **PostgreSQL Storage Engine:** B-tree page index corruption, WAL write-ahead log lock contentions.
    * **LLVM Compiler Backend:** Clang -O3 instruction reordering violations, AVX-512 register spill crashes.
  * `synthetic_enterprise_developers.csv` (16 maintainers): Synthetic engineering personas ranging from Lead Kernel Architects (`Linus_KernelLead`) and Principal Security Architects (`Sarah_SecArchitect`) to Junior DevOps Engineers.

---

## 2. Standard Input Schemas

### Issue Record Schema
```csv
id,title,severity,estimated_hours,business_value,deadline_day,required_skills,prerequisites
101,"CVE-2026-1044: Use-after-free in eBPF verifier kernel subsystem",5,16,98.0,2,Kernel;C;Memory;Security,
```
* `id` (Integer): Unique positive identifier.
* `title` (String): Descriptive defect or feature summary (quote-escaped to allow internal commas).
* `severity` (Integer $\in [1, 5]$): 5 = Critical / Blocker, 4 = High, 3 = Medium, 2 = Low, 1 = Cosmetic / Trivial.
* `estimated_hours` (Integer $> 0$): Estimated story point effort in hours ($w_i$).
* `business_value` (Double $> 0$): Priority business impact / value ($v_i$).
* `deadline_day` (Integer $> 0$): Sprint SLA delivery horizon.
* `required_skills` (Semicolon-separated string): Skill vector tags required for assignment.
* `prerequisites` (Semicolon-separated integers): Dependency issue IDs required before this issue can commence.

### Developer Record Schema
```csv
id,name,available_hours,skills
1,Linus_KernelLead,40,Kernel;C;Memory;Concurrency;Systems
```
* `id` (Integer): Unique developer identifier.
* `name` (String): Alphanumeric maintainer handle / identifier.
* `available_hours` (Integer $\ge 0$): Total sprint working capacity in hours.
* `skills` (Semicolon-separated string): Skill capabilities mastered by the developer.

---

## 3. Licensing & Permissive Use Statement

All synthetic and derived defect descriptions contained in these datasets are released under the **MIT License** and **Apache License 2.0 Open Source Data Declarations**. They contain zero proprietary, classified, or copyrighted commercial code and are entirely safe for academic evaluation, reproducibility, and publication.
