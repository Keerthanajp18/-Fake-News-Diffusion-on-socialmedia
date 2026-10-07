import re

with open("reconstructed_paper.tex", "r", encoding="utf-8") as f:
    text = f.read()

# Let's inspect all places with ~[ in the text to see what needs replacing
all_matches = re.findall(r"~\[([0-9,\s]+)\]", text)
print("Bracket matches:", set(all_matches))
