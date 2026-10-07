with open("reconstructed_paper.tex", "r", encoding="utf-8") as f:
    rec = f.read()

with open("thesis_final_report.tex", "r", encoding="utf-8") as f:
    orig = f.read()

print("Reconstructed len:", len(rec))
print("Original len:", len(orig))

# Compare section headers
import re
print("\n--- RECONSTRUCTED SECTIONS ---")
for s in re.findall(r"\\(?:sub)*section\{[^}]+\}", rec):
    print(" ", s)

print("\n--- ORIGINAL SECTIONS ---")
for s in re.findall(r"\\(?:sub)*section\{[^}]+\}", orig):
    print(" ", s)
