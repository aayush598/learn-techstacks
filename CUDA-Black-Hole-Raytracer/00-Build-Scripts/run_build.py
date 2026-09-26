"""Build runner: merges all curated content modules (keys are full relative
paths) and writes questions.md (100 flashcard-format Q&A) into every leaf.

Run from this directory:  python3 run_build.py
"""
import os
import engine
import c_cuda, c_ray, c_rel, c_grt, c_grmhd, c_rad, c_num, c_perf
import c_prod, c_astro, c_end

SOURCES = [
    c_cuda.CUDA, c_ray.RAY, c_rel.REL, c_grt.GRT, c_grmhd.GRMHD,
    c_rad.RAD, c_num.NUM, c_perf.PERF, c_prod.PROD, c_astro.ASTRO, c_end.END,
]

def build_pool():
    pool = {}
    for d in SOURCES:
        for key, qa in d.items():
            pool.setdefault(key, []).extend(qa)
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
    orphans = sorted(set(pool) - rels)
    if orphans:
        print("  ORPHAN KEYS ->", orphans)
    engine.build_all(pool)

if __name__ == "__main__":
    main()