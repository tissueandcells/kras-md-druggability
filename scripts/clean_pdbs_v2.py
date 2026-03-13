#!/usr/bin/env python3
"""Clean PDB v2: handle altloc (keep A or blank), remove H atoms, fix residue ranges"""

import os

RAW = os.path.expanduser("~/kras_md/structures/pdb_raw")
CLEAN = os.path.expanduser("~/kras_md/structures/pdb_clean")

KEEP_HETATM = {"GDP", "GNP", "MG"}

systems = {
    "WT_GDP":   ("4OBE", "A", 1, 169),
    "G12C_GDP": ("4LDJ", "A", 1, 169),
    "G12D_GDP": ("5US4", "A", 1, 169),
    "G12V_GDP": ("4TQ9", "A", 1, 169),  # ends at 168 in crystal
    "WT_GTP":   ("6GOD", "A", 1, 169),
    "G12V_GTP": ("6GOE", "A", 1, 169),
}

for sysname, (pdb_id, chain, res_min, res_max) in systems.items():
    infile = os.path.join(RAW, f"{pdb_id}.pdb")
    outfile = os.path.join(CLEAN, f"{sysname}.pdb")
    
    kept = 0
    with open(infile) as fin, open(outfile, 'w') as fout:
        for line in fin:
            rec = line[:6].strip()
            if rec not in ("ATOM", "HETATM"):
                if rec == "END":
                    fout.write("END\n")
                    break
                continue
            
            ch = line[21]
            if ch != chain:
                continue
            
            altloc = line[16]
            if altloc not in (' ', '', 'A'):
                continue
            
            # Remove hydrogen atoms
            element = line[76:78].strip() if len(line) >= 78 else ""
            if element == "H":
                continue
            
            resname = line[17:20].strip()
            try:
                resnum = int(line[22:26].strip())
            except ValueError:
                continue
            
            if rec == "ATOM":
                if res_min <= resnum <= res_max:
                    # Clear altloc indicator
                    line_clean = line[:16] + ' ' + line[17:]
                    fout.write(line_clean)
                    kept += 1
            elif rec == "HETATM":
                if resname in KEEP_HETATM:
                    line_clean = line[:16] + ' ' + line[17:]
                    fout.write(line_clean)
                    kept += 1
    
    # Verify
    max_res = 0
    with open(outfile) as f:
        for line in f:
            if line.startswith("ATOM"):
                try:
                    r = int(line[22:26].strip())
                    max_res = max(max_res, r)
                except:
                    pass
    
    print(f"{sysname:12s} ({pdb_id}): {kept:5d} atoms | res 1-{max_res}")

print("\nDone!")
