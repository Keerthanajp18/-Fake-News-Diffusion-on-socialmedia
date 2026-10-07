import os

with open("reconstructed_paper.tex", "r", encoding="utf-8") as f:
    text = f.read()

print("File length:", len(text))
print("Line count:", len(text.splitlines()))

# Find any ``` in text
import re
code_fences = [m.start() for m in re.finditer(r"```", text)]
print("Code fences found:", len(code_fences))
for pos in code_fences:
    print("Fence at pos:", pos, "context:", repr(text[max(0, pos-30):min(len(text), pos+30)]))
