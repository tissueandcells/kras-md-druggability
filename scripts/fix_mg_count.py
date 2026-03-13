#!/usr/bin/env python3
import os

SIMDIR = os.path.expanduser("~/kras_md/simulations")

for sysname in ["WT_GDP","WT_GTP","G12C_GDP","G12C_GTP","G12D_GDP","G12D_GTP","G12V_GDP","G12V_GTP"]:
    sysdir = os.path.join(SIMDIR, sysname)
    
    # Count MG in complex.gro
    mg_count = 0
    with open(os.path.join(sysdir, "complex.gro")) as f:
        for line in f:
            if " MG " in line and "MG" in line[5:10]:
                mg_count += 1
    
    # Fix topol.top
    topol = os.path.join(sysdir, "topol.top")
    with open(topol) as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if line.strip().startswith("MG"):
            new_lines.append(f"MG          {mg_count}\n")
        else:
            new_lines.append(line)
    
    with open(topol, 'w') as f:
        f.writelines(new_lines)
    
    print(f"{sysname}: MG = {mg_count}")

print("Done!")
