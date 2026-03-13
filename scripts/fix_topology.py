#!/usr/bin/env python3
"""
Fix topology files for all 8 systems:
1. Split GDP/GNP .itp into atomtypes and moleculetype sections
2. Rebuild topol.top with correct ordering
"""
import os, re

SIMDIR = os.path.expanduser("~/kras_md/simulations")

systems = {
    "WT_GDP": "GDP", "G12C_GDP": "GDP", "G12D_GDP": "GDP", "G12V_GDP": "GDP",
    "WT_GTP": "GNP", "G12C_GTP": "GNP", "G12D_GTP": "GNP", "G12V_GTP": "GNP",
}

for sysname, ligtype in systems.items():
    sysdir = os.path.join(SIMDIR, sysname)
    itp_file = os.path.join(sysdir, f"{ligtype}.itp")
    topol_file = os.path.join(sysdir, "topol.top")
    
    # 1. Read ligand ITP, split atomtypes from rest
    with open(itp_file) as f:
        itp_content = f.read()
    
    # Extract atomtypes section
    atomtypes_lines = []
    mol_lines = []
    in_atomtypes = False
    for line in itp_content.split('\n'):
        if '[ atomtypes ]' in line:
            in_atomtypes = True
            atomtypes_lines.append(line)
            continue
        if in_atomtypes:
            if line.strip().startswith('[') and 'atomtypes' not in line:
                in_atomtypes = False
                mol_lines.append(line)
            else:
                atomtypes_lines.append(line)
        else:
            mol_lines.append(line)
    
    # Write separate files
    at_file = os.path.join(sysdir, f"{ligtype}_atomtypes.itp")
    mol_file = os.path.join(sysdir, f"{ligtype}_mol.itp")
    
    with open(at_file, 'w') as f:
        f.write('\n'.join(atomtypes_lines) + '\n')
    with open(mol_file, 'w') as f:
        f.write('\n'.join(mol_lines) + '\n')
    
    # 2. Read topol.top and rebuild
    with open(topol_file) as f:
        top_lines = f.readlines()
    
    new_top = []
    added_ligand_includes = False
    molecules_section = False
    sol_written = False
    
    for line in top_lines:
        # Skip old ligand/mg includes
        if f'#include "{ligtype}.itp"' in line:
            continue
        if '#include "mg.itp"' in line:
            continue
        
        # After forcefield include, add atomtypes
        if '#include "amber99sb-ildn.ff/forcefield.itp"' in line and not added_ligand_includes:
            new_top.append(line)
            new_top.append(f'\n; Ligand atom types\n')
            new_top.append(f'#include "{ligtype}_atomtypes.itp"\n')
            added_ligand_includes = True
            continue
        
        # Before [ system ], add ligand and mg moleculetype includes
        if '[ system ]' in line:
            new_top.append(f'\n; Ligand topology\n')
            new_top.append(f'#include "{ligtype}_mol.itp"\n')
            new_top.append(f'#include "mg.itp"\n\n')
            new_top.append(line)
            continue
        
        new_top.append(line)
    
    with open(topol_file, 'w') as f:
        f.writelines(new_top)
    
    print(f"{sysname}: topol.top fixed ({ligtype}_atomtypes.itp + {ligtype}_mol.itp + mg.itp)")

print("\nDone!")
