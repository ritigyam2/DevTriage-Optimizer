import docx

doc_paths = [
    'PROJECT_50_FINAL_EVALUATION_DOSSIER_AND_ARCHITECTURE_GUIDE.docx',
    'PROJECT_50_TOPPER_PROJECT_PLAN_AND_ARCHITECTURE_GUIDE.docx',
    'AutoTriage-DAA/docs/PROJECT_50_FINAL_EVALUATION_DOSSIER_AND_ARCHITECTURE_GUIDE.docx'
]

replacements = [
    ('CSV/JSON parser', 'CSV parser'),
    ('CSV/JSON', 'CSV'),
    ('completely eliminating the O(n^2) quadratic degradation on pre-sorted or reverse-sorted backlogs',
     'mitigating common poor-pivot degradation on pre-sorted or reverse-sorted backlogs (worst case remains O(n^2))'),
    ('eliminating the O(n^2)', 'mitigating poor-pivot degradation (worst case remains O(n^2))'),
    ('eliminates anti-quicksort attacks', 'mitigates common poor-pivot cases (worst case remains O(n^2))'),
    ('eliminates O(n^2)', 'mitigates common poor-pivot cases (worst case remains O(n^2))'),
    ('Real-world 120-issue dataset', 'Synthetic enterprise-style benchmark dataset'),
    ('real-world 120-issue', 'synthetic enterprise 120-issue'),
    ('real-world issues', 'synthetic enterprise issues'),
    ('real-world CVEs', 'synthetic CVE-style security issues'),
    ('real CVEs', 'synthetic CVE-style security issues'),
    ('Reduction verifier O(n)', 'Reduction construction O(n); demonstration verification is exponential'),
    ('reduction verifier is O(n)', 'reduction construction is O(n); demonstration verification is exponential'),
    ('capacity-constrained bipartite matching', 'one-to-one maximum bipartite matching'),
]

for dp in doc_paths:
    d = docx.Document(dp)
    for p in d.paragraphs:
        for old_s, new_s in replacements:
            if old_s in p.text:
                p.text = p.text.replace(old_s, new_s)
    for t in d.tables:
        for r in t.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    for old_s, new_s in replacements:
                        if old_s in p.text:
                            p.text = p.text.replace(old_s, new_s)
    d.save(dp)
    print(f'Truth-table sanitized {dp}')
