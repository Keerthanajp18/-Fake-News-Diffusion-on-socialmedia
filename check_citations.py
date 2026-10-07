import re

with open("reconstructed_paper.tex", "r", encoding="utf-8") as f:
    text = f.read()

# Find all citations in text
cites = re.findall(r"~\[([^\]]+)\]", text)
print("Explicit bracket citations found:", len(cites))
all_cites = set()
for c in cites:
    for item in c.split(","):
        all_cites.add(item.strip())
print("Unique citation markers:", sorted(list(all_cites)))

# Find \cite{...} if any
latex_cites = re.findall(r"\\cite\{([^}]+)\}", text)
print("LaTeX \\cite found:", len(latex_cites))
