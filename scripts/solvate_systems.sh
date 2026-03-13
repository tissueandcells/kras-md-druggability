#!/bin/bash
source /home/kubra/kras_md/software/gromacs-2026.0-install/bin/GMXRC

SIMDIR=~/kras_md/simulations

for sys in WT_GDP WT_GTP G12C_GDP G12C_GTP G12D_GDP G12D_GTP G12V_GDP G12V_GTP; do
    echo "========== $sys =========="
    cd $SIMDIR/$sys
    
    # 1. Define dodecahedron box with 1.2 nm padding
    gmx editconf -f complex.gro -o box.gro -c -d 1.2 -bt dodecahedron 2>&1 | grep -E "box\|Volume\|atom"
    
    # 2. Solvate
    gmx solvate -cp box.gro -cs spc216.gro -o solv.gro -p topol.top 2>&1 | grep -E "Number\|Added\|atom"
    
    # 3. Create ions.mdp for genion
    cat > ions.mdp << 'MDP'
integrator  = steep
emtol       = 1000.0
emstep      = 0.01
nsteps      = 50000
nstlist     = 1
cutoff-scheme = Verlet
ns_type     = grid
coulombtype = PME
rcoulomb    = 1.0
rvdw        = 1.0
pbc         = xyz
MDP
    
    # 4. Prepare for genion
    gmx grompp -f ions.mdp -c solv.gro -p topol.top -o ions.tpr -maxwarn 10 2>&1 | grep -E "charge\|Warning\|Error\|Fatal" | head -5
    
    # 5. Add ions (replace SOL, neutralize + 0.15M NaCl)
    echo "SOL" | gmx genion -s ions.tpr -o solv_ions.gro -p topol.top -pname NA -nname CL -neutral -conc 0.15 2>&1 | grep -E "replaced\|Will\|Group"
    
    NATOM=$(sed -n '2p' solv_ions.gro | tr -d ' ')
    echo "$sys: DONE - $NATOM total atoms"
    echo ""
done
