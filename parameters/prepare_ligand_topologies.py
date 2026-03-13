#!/usr/bin/env python3
"""
Prepare ligand GRO files and copy ITP files to each simulation directory.
Also create Mg2+ ITP and GRO entries.
"""
import os, shutil

SIMDIR = os.path.expanduser("~/kras_md/simulations")
PARAMDIR = os.path.expanduser("~/kras_md/parameters")
CLEAN = os.path.expanduser("~/kras_md/structures/pdb_clean")

# Systems and their ligand type
systems = {
    "WT_GDP": "GDP", "G12C_GDP": "GDP", "G12D_GDP": "GDP", "G12V_GDP": "GDP",
    "WT_GTP": "GNP", "G12C_GTP": "GNP", "G12D_GTP": "GNP", "G12V_GTP": "GNP",
}

# Create Mg2+ ITP (AMBER99SB-ILDN already has MG ion type)
mg_itp = """; MG2+ ion topology
[ moleculetype ]
; name  nrexcl
MG      1

[ atoms ]
;  nr  type  resnr  residu  atom  cgnr  charge  mass
   1   MG      1     MG      MG    1    2.000   24.305
"""

mg_itp_path = os.path.join(PARAMDIR, "mg.itp")
with open(mg_itp_path, 'w') as f:
    f.write(mg_itp)
print(f"Created {mg_itp_path}")

for sysname, ligtype in systems.items():
    sysdir = os.path.join(SIMDIR, sysname)
    
    # Copy ligand ITP
    src_itp = os.path.join(PARAMDIR, ligtype, f"{ligtype}.acpype", f"{ligtype}_GMX.itp")
    dst_itp = os.path.join(sysdir, f"{ligtype}.itp")
    shutil.copy2(src_itp, dst_itp)
    
    # Copy Mg ITP
    shutil.copy2(mg_itp_path, os.path.join(sysdir, "mg.itp"))
    
    # Create ligand GRO from fixed PDB using gmx editconf
    lig_pdb = os.path.join(sysdir, "ligand.pdb")
    mg_pdb = os.path.join(sysdir, "mg.pdb")
    
    print(f"{sysname}: {ligtype}.itp + mg.itp copied")

print("\nDone!")
