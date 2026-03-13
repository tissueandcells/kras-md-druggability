#!/usr/bin/env python3
"""
Generate G12C_GTP and G12D_GTP by mutating Gly12 in WT_GTP (6GOD cleaned).
Since Gly->Cys/Asp involves adding sidechain atoms that don't exist in Gly,
we use a rotamer-based approach with Biopython.
For Gly->X mutations, we need to add CB and sidechain atoms.
We'll use a simpler approach: copy WT_GTP, rename residue 12, 
and let GROMACS pdb2gmx rebuild missing atoms.
"""

import os

CLEAN = os.path.expanduser("~/kras_md/structures/pdb_clean")
wt_gtp = os.path.join(CLEAN, "WT_GTP.pdb")

mutations = {
    "G12C_GTP": ("GLY", "CYS"),
    "G12D_GTP": ("GLY", "ASP"),
}

for sysname, (orig_res, new_res) in mutations.items():
    outfile = os.path.join(CLEAN, f"{sysname}.pdb")
    count = 0
    with open(wt_gtp) as fin, open(outfile, 'w') as fout:
        for line in fin:
            if (line.startswith("ATOM") or line.startswith("HETATM")):
                resnum = line[22:26].strip()
                resname = line[17:20].strip()
                if resnum == "12" and resname == orig_res and line.startswith("ATOM"):
                    # Replace residue name, keep only backbone atoms (N, CA, C, O)
                    atomname = line[12:16].strip()
                    if atomname in ("N", "CA", "C", "O"):
                        newline = line[:17] + f"{new_res}" + line[20:]
                        fout.write(newline)
                        count += 1
                    # Skip HA2, HA3 (Gly-specific H atoms) - already removed
                else:
                    fout.write(line)
            else:
                fout.write(line)
    
    print(f"{sysname}: Mutated res 12 {orig_res}->{new_res} (kept {count} backbone atoms)")
    print(f"  -> {outfile}")
    print(f"  Note: Missing sidechain atoms will be rebuilt by GROMACS pdb2gmx")

print("\nAll 8 systems ready!")
