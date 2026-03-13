#!/usr/bin/env python3
import os

SIMDIR = os.path.expanduser("~/kras_md/simulations")

for sysname in ["WT_GDP","WT_GTP","G12C_GDP","G12C_GTP","G12D_GDP","G12D_GTP","G12V_GDP","G12V_GTP"]:
    topol = os.path.join(SIMDIR, sysname, "topol.top")
    with open(topol) as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if '#include "mg.itp"' in line:
            new_lines.append('; Include ion parameters\n')
            new_lines.append('#include "amber99sb-ildn.ff/ions.itp"\n')
        else:
            new_lines.append(line)
    
    with open(topol, 'w') as f:
        f.writelines(new_lines)
    print(f"{sysname}: mg.itp -> ions.itp")

print("Done!")
