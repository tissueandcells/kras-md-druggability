#!/bin/bash
source /home/kubra/kras_md/software/gromacs-2026.0-install/bin/GMXRC

SIMDIR=~/kras_md/simulations

declare -A LIGTYPE
LIGTYPE=( [WT_GDP]=GDP [G12C_GDP]=GDP [G12D_GDP]=GDP [G12V_GDP]=GDP \
          [WT_GTP]=GNP [G12C_GTP]=GNP [G12D_GTP]=GNP [G12V_GTP]=GNP )

for sys in WT_GDP WT_GTP G12C_GDP G12C_GTP G12D_GDP G12D_GTP G12V_GDP G12V_GTP; do
    echo "========== $sys =========="
    DIR=$SIMDIR/$sys
    cd $DIR
    LIG=${LIGTYPE[$sys]}
    
    # Convert ligand PDB to GRO
    gmx editconf -f ligand.pdb -o ligand.gro 2>/dev/null
    # Convert Mg PDB to GRO  
    gmx editconf -f mg.pdb -o mg.gro 2>/dev/null
    
    # Read box size from protein GRO (last line)
    BOXLINE=$(tail -1 protein_processed.gro)
    
    # Get atom counts
    PROT_NATOM=$(sed -n '2p' protein_processed.gro | tr -d ' ')
    LIG_NATOM=$(sed -n '2p' ligand.gro | tr -d ' ')
    MG_NATOM=$(sed -n '2p' mg.gro | tr -d ' ')
    TOTAL=$((PROT_NATOM + LIG_NATOM + MG_NATOM))
    
    # Build complex GRO
    TITLE=$(head -1 protein_processed.gro)
    echo "$TITLE + $LIG + MG" > complex.gro
    echo "$TOTAL" >> complex.gro
    # Protein atoms (skip first 2 lines, skip last line)
    head -n -1 protein_processed.gro | tail -n +3 >> complex.gro
    # Ligand atoms
    head -n -1 ligand.gro | tail -n +3 >> complex.gro
    # Mg atoms
    head -n -1 mg.gro | tail -n +3 >> complex.gro
    # Box
    echo "$BOXLINE" >> complex.gro
    
    # Update topology: add ligand and MG includes and molecules
    # Insert includes after forcefield include
    sed -i "/^#include \"amber99sb-ildn.ff\/forcefield.itp\"/a\\
#include \"${LIG}.itp\"\\
#include \"mg.itp\"" topol.top
    
    # Add molecules at end
    echo "${LIG}     1" >> topol.top
    echo "MG          1" >> topol.top
    
    echo "$sys: complex.gro ($TOTAL atoms), topol.top updated with $LIG + MG"
    echo ""
done
