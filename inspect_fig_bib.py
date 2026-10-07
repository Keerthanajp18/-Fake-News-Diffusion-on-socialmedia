import re

with open("reconstructed_paper.tex", "r", encoding="utf-8") as f:
    text = f.read()

# Inspect Figure 3
fig3_match = re.search(r"(\\begin\{figure\*?\}[\s\S]*?Twitter16 Precision[\s\S]*?\\end\{figure\*?\})", text)
if fig3_match:
    print("=== EXACT FIGURE 3 IN RECONSTRUCTED PAPER ===")
    print(fig3_match.group(1))

# Inspect thebibilography
bib_match = re.search(r"\\begin\{thebibliography\}[\s\S]*?\\end\{thebibliography\}", text)
if bib_match:
    print("\n=== BIBLIOGRAPHY IN RECONSTRUCTED PAPER ===")
    bib_text = bib_match.group(0)
    items = re.findall(r"\\bibitem\{([^}]+)\}", bib_text)
    print("Total bibitems:", len(items))
    for i, it in enumerate(items):
        print(f"{i+1}. {it}")
