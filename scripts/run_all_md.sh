#!/bin/bash
unset LD_PRELOAD
source /home/kubra/kras_md/software/gromacs-2026.0-install/bin/GMXRC

LOG=~/kras_md/md_progress.log
echo "=== MD Production Started: $(date) ===" > $LOG

for sys in WT_GDP WT_GTP G12C_GDP G12C_GTP G12D_GDP G12D_GTP G12V_GDP G12V_GTP; do
    echo "=== $sys: Started $(date) ===" | tee -a $LOG
    cd ~/kras_md/simulations/$sys
    gmx mdrun -deffnm md -nb gpu -pme cpu -bonded gpu -update gpu -ntmpi 1 -ntomp 4 2>&1 | grep "Performance" | tee -a $LOG
    echo "=== $sys: Finished $(date) ===" | tee -a $LOG
    echo "" | tee -a $LOG
done

echo "=== ALL DONE: $(date) ===" | tee -a $LOG
