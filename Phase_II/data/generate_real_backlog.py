import csv

issues = [
    # Critical CVEs & Kernel Bugs (Severity 1)
    ("ISSUE-101", "CVE-2026-1044: Use-after-free in eBPF verifier kernel subsystem", "Kernel", 1, 16, 480, "kernel;c;memory;security"),
    ("ISSUE-102", "CVE-2026-2189: Remote code execution in TLS 1.3 handshake state machine", "Security", 1, 24, 500, "security;crypto;tls;networking"),
    ("ISSUE-103", "Data corruption on dirty cache flush in ext4 block journaling", "Storage", 1, 20, 460, "database;storage;c;systems"),
    ("ISSUE-104", "Deadlock in Raft leader election during network partition split-brain", "Distributed", 1, 18, 470, "distributed;raft;consensus;networking"),
    ("ISSUE-105", "CVE-2026-3390: Out-of-bounds heap write in V8 JIT compiler optimization", "Runtime", 1, 22, 490, "memory;compiler;v8;runtime"),
    ("ISSUE-106", "Panic in Kubernetes Pod sandbox CNI network teardown", "Cloud", 1, 14, 430, "kubernetes;cloud;docker;networking"),
    ("ISSUE-107", "Zero-day vulnerability in OpenSSL ASN.1 decoder stack overflow", "Security", 1, 26, 500, "security;crypto;c;audit"),
    ("ISSUE-108", "Silent integer overflow in PostgreSQL B-tree page index split", "Database", 1, 16, 450, "database;storage;sql;indexing"),
    ("ISSUE-109", "Infinite loop and CPU starvation in spinlock under NUMA scheduling", "Kernel", 1, 12, 420, "kernel;c;memory;concurrency"),
    ("ISSUE-110", "LLVM Backend crash generating AVX-512 vector register spills", "Compiler", 1, 16, 440, "llvm;compiler;optimization;assembly"),
    
    # High Priority Deficiencies (Severity 2)
    ("ISSUE-111", "Memory leak in TCP socket buffer pool under high connection churn", "Networking", 2, 14, 380, "networking;sockets;c++;systems"),
    ("ISSUE-112", "Double-free in WebSocket connection upgrade teardown", "Networking", 2, 10, 360, "networking;c++;memory;security"),
    ("ISSUE-113", "Lock contention in WAL write ahead log commit pipeline", "Database", 2, 16, 390, "database;storage;sql;concurrency"),
    ("ISSUE-114", "Garbage collection stop-the-world pause exceeds 250ms SLA", "Runtime", 2, 20, 370, "runtime;memory;gc;v8"),
    ("ISSUE-115", "OOM killer prematurely terminates healthy container worker daemon", "Cloud", 2, 12, 340, "kubernetes;cloud;docker;devops"),
    ("ISSUE-116", "Incorrect instruction reordering in Clang -O3 loop vectorizer", "Compiler", 2, 18, 380, "llvm;compiler;optimization;assembly"),
    ("ISSUE-117", "Race condition in thread pool work-stealing queue dequeue", "Core", 2, 14, 360, "c++;systems;concurrency;posix"),
    ("ISSUE-118", "Electron UI white screen flash during hardware acceleration fallback", "Frontend", 2, 12, 320, "gui;electron;rendering;performance"),
    ("ISSUE-119", "Etcd key-value compaction blocks concurrent read transactions", "Distributed", 2, 16, 370, "distributed;raft;consensus;database"),
    ("ISSUE-120", "Timing side-channel leak in ECDSA signature nonce generation", "Security", 2, 18, 390, "security;crypto;audit;fuzzing"),

    # Medium Priority Features & Fixes (Severity 3)
    ("ISSUE-121", "Add support for io_uring asynchronous disk I/O in worker engine", "Storage", 3, 20, 290, "kernel;c;storage;systems"),
    ("ISSUE-122", "Implement Brotli dynamic HTTP response compression filter", "Networking", 3, 10, 240, "networking;http;c++;performance"),
    ("ISSUE-123", "Optimize AST parser memory allocation using arena allocators", "Compiler", 3, 16, 280, "llvm;compiler;memory;optimization"),
    ("ISSUE-124", "Expose Prometheus Prometheus latency metrics for DB connection pool", "Cloud", 3, 8, 200, "cloud;docker;devops;ci"),
    ("ISSUE-125", "Support multi-column composite index scan in query planner", "Database", 3, 18, 270, "database;sql;indexing;storage"),
    ("ISSUE-126", "Add dark mode theme palette and CSS variable tokens", "Frontend", 3, 10, 210, "gui;typescript;react;electron"),
    ("ISSUE-127", "Refactor session token storage to use secure HTTP-only cookies", "Security", 3, 12, 260, "security;auth;audit;http"),
    ("ISSUE-128", "Add fuzz testing target for RPC protobuf deserializer", "Security", 3, 14, 250, "security;fuzzing;audit;c++"),
    ("ISSUE-129", "Reduce virtual DOM reconciliation passes on issue grid scroll", "Frontend", 3, 12, 230, "gui;react;rendering;performance"),
    ("ISSUE-130", "Implement adaptive backoff retry policy for downstream API client", "Core", 3, 8, 190, "c++;networking;systems;testing"),

    # Low Priority Enhancements (Severity 4)
    ("ISSUE-131", "Migrate build configuration from CMake 3.10 to CMake 3.25", "DevOps", 4, 8, 140, "ci;devops;automation;docker"),
    ("ISSUE-132", "Update bundled timezone database to IANA 2026a", "Core", 4, 4, 90, "posix;systems;c;testing"),
    ("ISSUE-133", "Add CLI flag --json-compact to suppress indentation in output", "Core", 4, 4, 100, "posix;debugging;c++;systems"),
    ("ISSUE-134", "Improve tooltip accessibility and keyboard navigation tabindex", "Frontend", 4, 6, 120, "gui;typescript;react;electron"),
    ("ISSUE-135", "Add benchmark suite for SIMD string search functions", "Core", 4, 10, 150, "c++;performance;optimization;testing"),
    ("ISSUE-136", "Cache pre-compiled regular expressions in rule evaluation engine", "Core", 4, 6, 110, "c++;systems;performance;regex"),
    ("ISSUE-137", "Upgrade SQLite embedded fallback driver to version 3.48", "Database", 4, 6, 130, "database;sql;c;storage"),
    ("ISSUE-138", "Add shell completion scripts for zsh and fish", "Core", 4, 4, 80, "posix;devops;automation;testing"),
    ("ISSUE-139", "Fix typo in diagnostic warning message for unaligned pointer access", "Compiler", 4, 2, 50, "llvm;compiler;testing;posix"),
    ("ISSUE-140", "Support custom user avatar image upload cropping in settings modal", "Frontend", 4, 8, 140, "gui;react;typescript;rendering"),

    # Trivial / Cosmetic (Severity 5)
    ("ISSUE-141", "Align copyright notice year in source headers to 2026", "Documentation", 5, 2, 30, "automation;ci;testing;posix"),
    ("ISSUE-142", "Remove deprecated legacy config parser stub functions", "Core", 5, 4, 40, "c++;debugging;posix;testing"),
    ("ISSUE-143", "Fix markdown formatting in CONTRIBUTING.md table of contents", "Documentation", 5, 2, 20, "documentation;ci;automation;testing"),
    ("ISSUE-144", "Standardize error log color codes in terminal runner", "Core", 5, 3, 35, "posix;debugging;c++;testing"),
    ("ISSUE-145", "Clean up unused SVG icons from asset bundle directory", "Frontend", 5, 2, 25, "gui;react;electron;rendering"),
]

# Generate remaining issues up to 120 procedurally with realistic variety
subsystems = [
    ("Kernel", ["kernel;c;memory;concurrency", "kernel;c;systems;debugging", "kernel;memory;posix;concurrency"]),
    ("Security", ["security;crypto;auth;audit", "security;fuzzing;audit;c++", "security;vulnerability;audit;python"]),
    ("Database", ["database;storage;sql;indexing", "database;sql;concurrency;storage", "database;storage;c;systems"]),
    ("Networking", ["networking;sockets;http;tls", "networking;distributed;c++;systems", "networking;sockets;c++;performance"]),
    ("Frontend", ["gui;typescript;react;electron", "gui;react;rendering;performance", "gui;electron;rendering;performance"]),
    ("Cloud", ["kubernetes;cloud;docker;devops", "docker;devops;ci;automation", "cloud;kubernetes;networking;devops"]),
    ("Compiler", ["llvm;compiler;optimization;assembly", "llvm;compiler;memory;optimization", "compiler;optimization;assembly;c++"]),
    ("Distributed", ["distributed;raft;consensus;networking", "distributed;raft;consensus;database", "distributed;networking;systems;c++"])
]

titles_template = [
    "Buffer allocation invariant violation during high throughput streaming in {sub}",
    "Fix edge-case segfault when handling null pointer callback in {sub}",
    "Optimize lock-free ring buffer read throughput for {sub}",
    "Add regression test suite covering concurrent race conditions in {sub}",
    "Refactor legacy telemetry collector to reduce memory footprint in {sub}",
    "Fix socket leak on unexpected remote peer reset in {sub}",
    "Mitigate cross-tenant noisy neighbor CPU throttling in {sub}",
    "Audit cryptographic signature verification for replay attack protection in {sub}",
    "Implement zero-copy memory mapped ring buffer in {sub}",
    "Resolve thread affinity thrashing on high-core server architectures in {sub}"
]

issue_id = 146
while len(issues) < 120:
    sub_name, skill_sets = subsystems[(issue_id % len(subsystems))]
    template = titles_template[(issue_id % len(titles_template))]
    title = template.format(sub=sub_name)
    severity = ((issue_id % 5) + 1)
    hours = ((issue_id * 3) % 28) + 4  # 4 to 32 hours
    priority = (6 - severity) * 80 + ((issue_id * 7) % 50)  # Value correlated with severity
    skills = skill_sets[(issue_id % len(skill_sets))]
    
    issues.append((f"ISSUE-{issue_id}", title, sub_name, severity, hours, priority, skills))
    issue_id += 1

with open("c:/Users/user/OneDrive/Desktop/DAA PROJECT/Phase_II/data/real_world_backlog.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "title", "component", "severity", "estimated_hours", "priority_score", "required_skills"])
    for row in issues:
        writer.writerow(row)

print(f"Successfully generated {len(issues)} real-world issues in real_world_backlog.csv")
