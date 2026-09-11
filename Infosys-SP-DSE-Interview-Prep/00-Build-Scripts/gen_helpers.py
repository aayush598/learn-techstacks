import os, json

def leaf_dirs(base):
    out = []
    for root, dirs, files in os.walk(base):
        if not dirs:
            out.append(root)
    return sorted(out)

def write_file(path, title, qa):
    lines = []
    lines.append("# " + title)
    lines.append("")
    lines.append("> Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE) - Interview Preparation")
    lines.append("> 100 Questions & Answers")
    lines.append("")
    for i, (q, a) in enumerate(qa, 1):
        lines.append(f"**Q{i}. {q}**")
        lines.append("")
        lines.append(f"A{i}. {a}")
        lines.append("")
    with open(path, "w") as f:
        f.write("\n".join(lines))
    return len(qa)
