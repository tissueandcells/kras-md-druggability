#!/usr/bin/env python3
import os, subprocess, shutil

SIMDIR = os.path.expanduser("~/kras_md/simulations")
SCRIPTS = os.path.expanduser("~/kras_md/scripts")

systems = {
    "WT_GDP": "GDP", "G12C_GDP": "GDP", "G12D_GDP": "GDP", "G12V_GDP": "GDP",
    "WT_GTP": "GNP", "G12C_GTP": "GNP", "G12D_GTP": "GNP", "G12V_GTP": "GNP",
}

for sysname, ligtype in systems.items():
    sysdir = os.path.join(SIMDIR, sysname)
    
    # Read template NVT mdp and adjust tc-grps
    for mdp_name in ["nvt.mdp", "npt.mdp"]:
        src = os.path.join(SCRIPTS, mdp_name)
        dst = os.path.join(sysdir, mdp_name)
        with open(src) as f:
            content = f.read()
        content = content.replace("Protein_GDP", f"Protein_{ligtype}")
        with open(dst, 'w') as f:
            f.write(content)
    
    # Create index file with proper groups using make_ndx
    # We need: Protein + ligand group, and everything else
    em_gro = os.path.join(sysdir, "em.gro")
    ndx_file = os.path.join(sysdir, "index.ndx")
    
    # Create index: merge Protein + ligand + MG into one group
    cmd = f'echo -e "1 | r {ligtype} | r MG\nq" | gmx make_ndx -f {em_gro} -o {ndx_file} 2>&1'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=sysdir)
    
    # Find the group number of the merged group
    lines = result.stdout.split('\n') + result.stderr.split('\n')
    new_group = None
    for line in lines:
        if f'Protein_{ligtype}_MG' in line or f'Protein_or' in line:
            new_group = line.strip().split()[0]
    
    print(f"{sysname}: {ligtype}, index created")

print("Done!")
