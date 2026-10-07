with open("reconstructed_paper.tex", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Split by sections
sections = re.split(r"(?=\\section\{)", text)
print(f"Total sections: {len(sections)}")
for i, s in enumerate(sections):
    m = re.search(r"\\section\{([^}]+)\}", s)
    title = m.group(1) if m else "Preamble/Abstract"
    print(f"Section {i}: {title} (len={len(s)})")
