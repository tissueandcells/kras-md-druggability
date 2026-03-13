#!/usr/bin/env python3
"""Clean PDB files: keep chain A, res 1-169, nucleotide + Mg, remove waters/GOL/buffer"""

import os

RAW = os.path.expanduser("~/kras_md/structures/pdb_raw")
CLEAN = os.path.expanduser("~/kras_md/structures/pdb_clean")

KEEP_HETATM = {"GDP", "GNP", "MG"}
REMOVE_HETATM = {"HOH", "GOL", "EDO", "PEG", "SO4", "ACT", "CL", "NA"}

systems = {
    "WT_GDP":   ("4OBE", "A", 1, 169),
    "G12C_GDP": ("4LDJ", "A", 1, 169),
    "G12D_GDP": ("5US4", "A", 1, 169),
    "G12V_GDP": ("4TQ9", "A", 1, 169),
    "WT_GTP":   ("6GOD", "A", 1, 169),
    "G12V_GTP": ("6GOE", "A", 1, 169),
}

for sysname, (pdb_id, chain, res_min, res_max) in systems.items():
    infile = os.path.join(RAW, f"{pdb_id}.pdb")
    outfile = os.path.join(CLEAN, f"{sysname}.pdb")
    
    kept = 0
    with open(infile) as fin, open(outfile, 'w') as fout:
        for line in fin:
            if line.startswith("ATOM"):
                ch = line[21]
                try:
                    resnum = int(line[22:26].strip())
                except ValueError:
                    continue
                if ch == chain and res_min <= resnum <= res_max:
                    fout.write(line)
                    kept += 1
            elif line.startswith("HETATM"):
                ch = line[21]
                resname = line[17:20].strip()
                if ch == chain and resname in KEEP_HETATM:
                    try:
                        resnum = int(line[22:26].strip())
                    except ValueError:
                        fout.write(line)
                        kept += 1
                        continue
                    fout.write(line)
                    kept += 1
            elif line.startswith("END"):
                fout.write("END\n")
                break
    
    print(f"{sysname} ({pdb_id}): {kept} atoms written -> {outfile}")

print("\nDone! Clean PDBs ready.")
