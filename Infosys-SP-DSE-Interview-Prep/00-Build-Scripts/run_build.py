"""Build runner: merges all curated content modules (with top-level domain prefixes)
and writes questions.md (100 Q&A) into every leaf directory of the tree.

Run from this directory:  python3 run_build.py
"""
import os
import sys

import engine
import c_arrays, c_strings, c_ll, c_trees, c_graphs, c_dp, c_rec, c_greedy2p
import c_oop, c_dbms, c_cs
import c_python, c_aiml, c_sysdesign, c_devops, c_hr
import c_patterns, c_aptitude

# (module_dict, top_level_prefix)
SOURCES = [
    (c_arrays.ARRAYS,    "01-DSA"),
    (c_strings.STRINGS,  "01-DSA"),
    (c_ll.LL,            "01-DSA"),
    (c_trees.TREES,      "01-DSA"),
    (c_graphs.GRAPHS,    "01-DSA"),
    (c_dp.DP,            "01-DSA"),
    (c_rec.REC,          "01-DSA"),
    (c_greedy2p.GREEDY,  "01-DSA"),
    (c_oop.OOP,          "02-CS-Fundamentals"),
    (c_dbms.DBMS,        "02-CS-Fundamentals"),
    (c_cs.CS,            "02-CS-Fundamentals"),
    (c_python.PYTHON,    "03-Python"),
    (c_aiml.AIML,        "04-AI-ML"),
    (c_sysdesign.SYS,    "05-System-Design"),
    (c_devops.DEVOPS,    "06-DevOps"),
    (c_hr.HR,            "07-HR-Preparation"),
    (c_patterns.PATTERNS,"08-Coding-Patterns"),
    (c_aptitude.APTITUDE,"09-Aptitude"),
]

def build_pool():
    pool = {}
    for d, prefix in SOURCES:
        for key, qa in d.items():
            rel = os.path.join(prefix, key)
            pool.setdefault(rel, []).extend(qa)
    return pool

def main():
    pool = build_pool()
    dirs = engine.leaf_dirs(engine.BASE)
    rels = {os.path.relpath(d, engine.BASE) for d in dirs}
    matched = [rel for rel in pool if rel in rels]
    unmatched = sorted(rels - set(pool))
    print(f"Content keys: {len(pool)} | Matched leaves: {len(matched)} | Unmatched leaves: {len(unmatched)}")
    for u in unmatched:
        print("  NO CONTENT ->", u)
    engine.build_all(pool)

if __name__ == "__main__":
    main()