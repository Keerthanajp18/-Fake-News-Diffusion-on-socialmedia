with open("reconstructed_paper.tex", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Check all environment begin and end tags
begins = re.findall(r"\\begin\{([^}]+)\}", text)
ends = re.findall(r"\\end\{([^}]+)\}", text)

print("Total begins:", len(begins))
print("Total ends:", len(ends))

from collections import Counter
b_cnt = Counter(begins)
e_cnt = Counter(ends)

for env in sorted(set(list(b_cnt.keys()) + list(e_cnt.keys()))):
    if b_cnt[env] != e_cnt[env]:
        print(f"ENV MISMATCH: {env} -> begin={b_cnt[env]}, end={e_cnt[env]}")
    else:
        print(f"ENV OK: {env} ({b_cnt[env]})")
