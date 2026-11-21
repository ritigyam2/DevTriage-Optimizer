import csv

# 16 Real-World Developers with diverse specialties
developers = [
    (1, "Linus_KernelLead", 40, "Kernel;C;Memory;Concurrency;Systems"),
    (2, "Sarah_SecArchitect", 35, "Security;Crypto;Auth;Audit;C"),
    (3, "David_SystemsLead", 40, "C++;Systems;Networking;Distributed;Storage"),
    (4, "Elena_DBAPrincipal", 40, "Database;Storage;SQL;Indexing;Concurrency"),
    (5, "Alex_FrontendLead", 40, "Frontend;TypeScript;React;Electron;UI"),
    (6, "Wei_CompilerStaff", 35, "Compiler;LLVM;Optimization;Assembly;C++"),
    (7, "Fatima_CloudDevOps", 40, "Kubernetes;Cloud;Docker;DevOps;CI"),
    (8, "Vikram_DistributedLead", 40, "Distributed;Raft;Consensus;Networking;Storage"),
    (9, "Chloe_RuntimeSenior", 35, "Runtime;Memory;GC;V8;C++"),
    (10, "Marcus_SystemsSenior", 40, "C;Systems;Debugging;POSIX;Kernel"),
    (11, "Aisha_SecEngineer", 35, "Security;Crypto;Vulnerability;Fuzzing;Audit"),
    (12, "James_NetEngineer", 40, "Networking;Sockets;HTTP;TLS;C++"),
    (13, "Priya_UIUXEngineer", 40, "Frontend;UI;Electron;Rendering;Performance"),
    (14, "Carlos_CoreJunior", 30, "C++;Systems;Debugging;Testing;POSIX"),
    (15, "Ananya_CloudJunior", 30, "Docker;DevOps;CI;Automation;Cloud"),
    (16, "Dmitri_SecJunior", 30, "Security;Audit;Fuzzing;Python;Testing"),
]

with open("c:/Users/user/OneDrive/Desktop/DAA PROJECT/Phase_II/data/real_world_developers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "name", "available_hours", "skills"])
    for d in developers:
        writer.writerow([d[0], d[1], d[2], d[3]])

# 120 Real-World Issues
# id,title,severity,estimated_hours,business_value,deadline_day,required_skills,prerequisites
seed_issues = [
    # Critical CVEs & Kernel Panics (Severity 5)
    (101, "CVE-2026-1044: Use-after-free in eBPF verifier kernel subsystem", 5, 16, 98.0, 2, "Kernel;C;Memory;Security", ""),
    (102, "CVE-2026-2189: Remote code execution in TLS 1.3 handshake state machine", 5, 24, 99.0, 1, "Security;Crypto;TLS;Networking", "101"),
    (103, "Silent data corruption on dirty cache flush in ext4 block journaling", 5, 20, 95.0, 3, "Database;Storage;C;Systems", ""),
    (104, "Deadlock in Raft leader election during network partition split-brain", 5, 18, 96.0, 2, "Distributed;Raft;Consensus;Networking", ""),
    (105, "CVE-2026-3390: Out-of-bounds heap write in V8 JIT compiler optimization", 5, 22, 97.0, 2, "Runtime;Memory;Compiler;V8", ""),
    (106, "Kernel panic in Pod sandbox CNI network bridge teardown", 5, 14, 94.0, 3, "Kubernetes;Cloud;Docker;Networking", ""),
    (107, "Zero-day vulnerability in OpenSSL ASN.1 decoder stack overflow", 5, 26, 100.0, 1, "Security;Crypto;C;Audit", ""),
    (108, "B-tree index page corruption on concurrent multithreaded split", 5, 16, 95.0, 3, "Database;Storage;SQL;Indexing", "103"),
    (109, "CPU core starvation in spinlock under NUMA memory node scheduling", 5, 12, 92.0, 4, "Kernel;C;Memory;Concurrency", ""),
    (110, "LLVM Backend crash generating AVX-512 vector register spills", 5, 16, 93.0, 3, "Compiler;LLVM;Optimization;Assembly", ""),

    # High Severity (Severity 4)
    (111, "Memory leak in TCP socket buffer pool under high connection churn", 4, 14, 82.0, 5, "Networking;Sockets;C++;Systems", ""),
    (112, "Double-free vulnerability in WebSocket connection upgrade teardown", 4, 10, 85.0, 4, "Networking;C++;Memory;Security", "102"),
    (113, "Lock contention in WAL write-ahead log commit transaction pipeline", 4, 16, 88.0, 5, "Database;Storage;SQL;Concurrency", "108"),
    (114, "Garbage collection stop-the-world pause exceeds 250ms SLA", 4, 20, 80.0, 6, "Runtime;Memory;GC;V8", "105"),
    (115, "OOM killer prematurely terminates healthy container worker daemon", 4, 12, 78.0, 5, "Kubernetes;Cloud;Docker;DevOps", "106"),
    (116, "Incorrect instruction reordering in Clang -O3 loop vectorizer", 4, 18, 86.0, 4, "Compiler;LLVM;Optimization;Assembly", "110"),
    (117, "Race condition in thread pool work-stealing queue dequeue", 4, 14, 84.0, 5, "C++;Systems;Concurrency;POSIX", "109"),
    (118, "Electron UI white screen flash during hardware acceleration fallback", 4, 12, 76.0, 7, "Frontend;Electron;Rendering;Performance", ""),
    (119, "Etcd key-value compaction blocks concurrent read transactions", 4, 16, 83.0, 6, "Distributed;Raft;Consensus;Database", "104"),
    (120, "Timing side-channel leak in ECDSA signature nonce generation", 4, 18, 89.0, 4, "Security;Crypto;Audit;Fuzzing", "107"),

    # Medium Severity (Severity 3)
    (121, "Add support for io_uring asynchronous disk I/O in worker engine", 3, 20, 68.0, 8, "Kernel;C;Storage;Systems", ""),
    (122, "Implement Brotli dynamic HTTP response compression filter", 3, 10, 60.0, 9, "Networking;HTTP;C++;Performance", ""),
    (123, "Optimize AST parser memory allocation using arena allocators", 3, 16, 65.0, 8, "Compiler;LLVM;Memory;Optimization", ""),
    (124, "Expose Prometheus latency metrics for DB connection pool", 3, 8, 55.0, 10, "Cloud;Docker;DevOps;CI", ""),
    (125, "Support multi-column composite index scan in query planner", 3, 18, 67.0, 9, "Database;SQL;Indexing;Storage", "113"),
    (126, "Add dark mode theme palette and CSS variable tokens", 3, 10, 50.0, 11, "Frontend;TypeScript;React;Electron", ""),
    (127, "Refactor session token storage to use secure HTTP-only cookies", 3, 12, 62.0, 8, "Security;Auth;Audit;HTTP", "120"),
    (128, "Add fuzz testing target for RPC protobuf deserializer", 3, 14, 64.0, 9, "Security;Fuzzing;Audit;C++", ""),
    (129, "Reduce virtual DOM reconciliation passes on issue grid scroll", 3, 12, 58.0, 10, "Frontend;React;Rendering;Performance", "118"),
    (130, "Implement adaptive backoff retry policy for downstream API client", 3, 8, 52.0, 11, "C++;Networking;Systems;Testing", ""),

    # Low Severity (Severity 2)
    (131, "Migrate build configuration from CMake 3.10 to CMake 3.25", 2, 8, 38.0, 12, "CI;DevOps;Automation;Docker", ""),
    (132, "Update bundled timezone database to IANA 2026a", 2, 4, 30.0, 14, "POSIX;Systems;C;Testing", ""),
    (133, "Add CLI flag --json-compact to suppress indentation in output", 2, 4, 32.0, 13, "POSIX;Debugging;C++;Systems", ""),
    (134, "Improve tooltip accessibility and keyboard navigation tabindex", 2, 6, 35.0, 14, "Frontend;TypeScript;React;Electron", "126"),
    (135, "Add benchmark suite for SIMD string search functions", 2, 10, 42.0, 12, "C++;Performance;Optimization;Testing", ""),
    (136, "Cache pre-compiled regular expressions in rule evaluation engine", 2, 6, 36.0, 13, "C++;Systems;Performance;POSIX", ""),
    (137, "Upgrade SQLite embedded fallback driver to version 3.48", 2, 6, 34.0, 14, "Database;SQL;C;Storage", ""),
    (138, "Add shell completion scripts for zsh and fish", 2, 4, 28.0, 15, "POSIX;DevOps;Automation;Testing", ""),
    (139, "Fix typo in diagnostic warning message for unaligned pointer access", 2, 2, 20.0, 15, "Compiler;LLVM;Testing;POSIX", ""),
    (140, "Support custom user avatar image upload cropping in settings modal", 2, 8, 39.0, 14, "Frontend;React;TypeScript;Rendering", ""),

    # Cosmetic / Documentation (Severity 1)
    (141, "Align copyright notice year in source headers to 2026", 1, 2, 12.0, 16, "Automation;CI;Testing;POSIX", ""),
    (142, "Remove deprecated legacy config parser stub functions", 1, 4, 15.0, 15, "C++;Debugging;POSIX;Testing", ""),
    (143, "Fix markdown formatting in CONTRIBUTING.md table of contents", 1, 2, 10.0, 16, "CI;Automation;Testing;Docs", ""),
    (144, "Standardize error log color codes in terminal runner", 1, 3, 14.0, 15, "POSIX;Debugging;C++;Testing", ""),
    (145, "Clean up unused SVG icons from asset bundle directory", 1, 2, 11.0, 16, "Frontend;React;Electron;Rendering", ""),
]

subsystems = [
    ("Kernel", ["Kernel;C;Memory;Concurrency", "Kernel;C;Systems;Debugging", "Kernel;Memory;POSIX;Concurrency"]),
    ("Security", ["Security;Crypto;Auth;Audit", "Security;Fuzzing;Audit;C++", "Security;Vulnerability;Audit;Testing"]),
    ("Database", ["Database;Storage;SQL;Indexing", "Database;SQL;Concurrency;Storage", "Database;Storage;C;Systems"]),
    ("Networking", ["Networking;Sockets;HTTP;TLS", "Networking;Distributed;C++;Systems", "Networking;Sockets;C++;Performance"]),
    ("Frontend", ["Frontend;TypeScript;React;Electron", "Frontend;React;Rendering;Performance", "Frontend;Electron;Rendering;Performance"]),
    ("Cloud", ["Kubernetes;Cloud;Docker;DevOps", "Docker;DevOps;CI;Automation", "Cloud;Kubernetes;Networking;DevOps"]),
    ("Compiler", ["Compiler;LLVM;Optimization;Assembly", "Compiler;LLVM;Memory;Optimization", "Compiler;Optimization;Assembly;C++"]),
    ("Distributed", ["Distributed;Raft;Consensus;Networking", "Distributed;Raft;Consensus;Database", "Distributed;Networking;Systems;C++"])
]

titles_template = [
    "Buffer allocation invariant violation during high-throughput streaming in {sub}",
    "Fix edge-case segfault when handling null pointer callback in {sub}",
    "Optimize lock-free ring buffer read throughput for {sub}",
    "Add regression test suite covering concurrent race conditions in {sub}",
    "Refactor legacy telemetry collector to reduce memory footprint in {sub}",
    "Fix socket leak on unexpected remote peer reset in {sub}",
    "Mitigate cross-tenant noisy neighbor CPU throttling in {sub}",
    "Audit cryptographic signature verification for replay attack protection in {sub}",
    "Implement zero-copy memory-mapped ring buffer in {sub}",
    "Resolve thread affinity thrashing on high-core server architectures in {sub}"
]

all_issues = list(seed_issues)
cur_id = 146
while len(all_issues) < 120:
    sub_name, skill_sets = subsystems[(cur_id % len(subsystems))]
    template = titles_template[(cur_id % len(titles_template))]
    title = template.format(sub=sub_name)
    severity = ((cur_id % 5) + 1)
    hours = ((cur_id * 3) % 24) + 4
    val = round(severity * 18.0 + ((cur_id * 5) % 15), 1)
    deadline = (6 - severity) * 3 + ((cur_id % 4) + 1)
    skills = skill_sets[(cur_id % len(skill_sets))]
    prereq = str(cur_id - 10) if (cur_id % 6 == 0) else ""
    
    all_issues.append((cur_id, title, severity, hours, val, deadline, skills, prereq))
    cur_id += 1

with open("c:/Users/user/OneDrive/Desktop/DAA PROJECT/Phase_II/data/real_world_issues.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "title", "severity", "estimated_hours", "business_value", "deadline_day", "required_skills", "prerequisites"])
    for row in all_issues:
        writer.writerow(row)

print(f"Generated {len(all_issues)} issues in real_world_issues.csv and {len(developers)} developers in real_world_developers.csv")
