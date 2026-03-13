#!/bin/bash
source /home/kubra/kras_md/software/gromacs-2026.0-install/bin/GMXRC

CLEAN=~/kras_md/structures/pdb_clean
SIMDIR=~/kras_md/simulations

for sys in WT_GDP WT_GTP G12C_GDP G12C_GTP G12D_GDP G12D_GTP G12V_GDP G12V_GTP; do
    echo "========== $sys =========="
    DIR=$SIMDIR/$sys
    cd $DIR
    
    # Extract protein only from fixed PDB
    grep "^ATOM" $CLEAN/${sys}_fixed.pdb > protein_only.pdb
    echo "END" >> protein_only.pdb
    
    # Extract ligands
    grep "^HETATM.*GDP\|^HETATM.*GNP" $CLEAN/${sys}_fixed.pdb > ligand.pdb 2>/dev/null
    grep "^HETATM.*MG" $CLEAN/${sys}_fixed.pdb > mg.pdb 2>/dev/null
    
    # Run pdb2gmx
    gmx pdb2gmx -f protein_only.pdb -o protein_processed.gro -p topol.top \
        -water tip3p -ignh -ff amber99sb-ildn 2>&1 | tail -3
    
    if [ -s topol.top ]; then
        echo "$sys: SUCCESS"
    else
        echo "$sys: FAILED"
    fi
    echo ""
done
