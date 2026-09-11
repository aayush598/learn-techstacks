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

def write_file(rel, title, qa):
    path = os.path.join(BASE, rel, "questions.md")
    lines = []
    lines.append("# %s" % title)
    lines.append("")
    lines.append("**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**")
    lines.append("")
    lines.append("<details open>")
    lines.append("<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>")
    lines.append("")
    for i, (q, a) in enumerate(qa, 1):
        lines.append("%d. **%s**" % (i, q))
        lines.append("   - %s" % a)
        lines.append("")
    lines.append("</details>")
    with open(path, "w") as f:
        f.write("\n".join(lines))
    return len(qa)

def build_all(pool):
    """pool: dict rel_path -> list[(q,a)]"""
    dirs = leaf_dirs(BASE)
    total = 0
    for d in dirs:
        rel = os.path.relpath(d, BASE)
        title = os.path.basename(d).replace("-", " ").title() + " — " + " / ".join(os.path.basename(os.path.dirname(d)).split("-")[1:]).title()
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