#!/usr/bin/env python3
import os

SIMDIR = os.path.expanduser("~/kras_md/simulations")

for sysname in ["WT_GDP","WT_GTP","G12C_GDP","G12C_GTP","G12D_GDP","G12D_GTP","G12V_GDP","G12V_GTP"]:
    sysdir = os.path.join(SIMDIR, sysname)
    for mdp in ["nvt.mdp", "npt.mdp"]:
        path = os.path.join(sysdir, mdp)
        with open(path) as f:
            content = f.read()
        # Replace any Protein_XXX Non-Protein with Protein Non-Protein
        content = content.replace("Protein_GDP", "Protein")
        content = content.replace("Protein_GNP", "Protein")
        with open(path, 'w') as f:
            f.write(content)
    print(f"{sysname}: tc-grps fixed to Protein / Non-Protein")

print("Done!")
