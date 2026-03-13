#!/usr/bin/env python3
import os

SIMDIR = os.path.expanduser("~/kras_md/simulations")

for sysname in ["WT_GDP","WT_GTP","G12C_GDP","G12C_GTP","G12D_GDP","G12D_GTP","G12V_GDP","G12V_GTP"]:
    topol = os.path.join(SIMDIR, sysname, "topol.top")
    with open(topol) as f:
        lines = f.readlines()
    
    # Remove our added ions.itp and its comment (keep the original one)
    new_lines = []
    seen_ions = False
    skip_next_ions = False
    for line in lines:
        if 'amber99sb-ildn.ff/ions.itp' in line:
            if not seen_ions:
                seen_ions = True
                new_lines.append(line)
            else:
                # Skip duplicate
                continue
        elif '; Include ion parameters' in line:
            # Skip our comment line too
            continue
        else:
            new_lines.append(line)
    
    with open(topol, 'w') as f:
        f.writelines(new_lines)
    print(f"{sysname}: duplicate ions.itp removed")

print("Done!")
