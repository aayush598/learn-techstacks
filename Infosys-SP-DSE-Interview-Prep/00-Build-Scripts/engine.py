import os, sys, importlib

BASE = "/home/aayush/aayush/projects/learn-techstacks/Infosys-SP-DSE-Interview-Prep"

def leaf_dirs(base):
    out = []
    for root, dirs, files in os.walk(base):
        dirs.sort()
        dirs[:] = [d for d in dirs if d not in ("00-Build-Scripts", "__pycache__")]
        if not dirs:
            out.append(root)
    return sorted(out)

def human(name):
    parts = [p for p in name.replace("-", " ").title().split() if not p.isdigit()]
    return " ".join(parts)

def write_file(rel, title, qa):
    path = os.path.join(BASE, rel, "questions.md")
    lines = []
    lines.append("# %s Interview Questions and Answers" % title)
    lines.append("")
    for i, (q, a) in enumerate(qa, 1):
        lines.append("## Q%d: %s" % (i, q))
        lines.append("**A:** %s" % a)
        lines.append("")
    with open(path, "w") as f:
        f.write("\n".join(lines))
    return len(qa)

def build_all(pool):
    """pool: dict rel_path -> list[(q,a)]"""
    dirs = leaf_dirs(BASE)
    total = 0
    for d in dirs:
        rel = os.path.relpath(d, BASE)
        parent = human(os.path.basename(os.path.dirname(d)))
        leaf = human(os.path.basename(d))
        title = (parent + " — " + leaf).strip(" —")
        qa = pool.get(rel, [])
        if len(qa) < 100:
            qa = qa + pad(rel, 100 - len(qa))
        n = write_file(rel, title, qa[:100])
        total += n
    print("Files written:", len(dirs), "Total questions:", total)

def pad(rel, n):
    """Generate n additional meaningful questions for a leaf based on generic CS interview meta-questions."""
    from pad import generic_pad
    return generic_pad(rel, n)