#!/usr/bin/env python3
import os

SIMDIR = os.path.expanduser("~/kras_md/simulations")

for sysname in ["WT_GDP","WT_GTP","G12C_GDP","G12C_GTP","G12D_GDP","G12D_GTP","G12V_GDP","G12V_GTP"]:
    topol = os.path.join(SIMDIR, sysname, "topol.top")
    with open(topol) as f:
        lines = f.readlines()
    
    new_lines = []
    seen_sol = False
    for line in lines:
        if line.strip().startswith("SOL"):
            if not seen_sol:
                seen_sol = True
                new_lines.append(line)
            # skip duplicates
        else:
            new_lines.append(line)
    
    with open(topol, 'w') as f:
        f.writelines(new_lines)
    
    # Verify
    with open(topol) as f:
        mols = [l.strip() for l in f if l.strip().startswith("SOL")]
    print(f"{sysname}: {len(mols)} SOL line(s)")

print("Done!")
