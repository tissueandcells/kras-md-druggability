# KRAS G12C/G12D/G12V Comparative Molecular Dynamics Simulations

## Simulated Systems

Eight all-atom MD simulations (200 ns each, 1.6 μs aggregate) of KRAS4B wild-type and G12C, G12D, G12V mutants in GDP- and GTP-bound states.

| System   | PDB ID | Nucleotide | Total Atoms |
|----------|--------|------------|-------------|
| WT-GDP   | 4OBE   | GDP        | 25,243      |
| WT-GTP   | 6GOD   | GNP        | 23,263      |
| G12C-GDP | 4LDJ   | GDP        | 27,258      |
| G12C-GTP | 6GOD*  | GNP        | 23,267      |
| G12D-GDP | 5US4   | GDP        | 26,511      |
| G12D-GTP | 6GOD*  | GNP        | 23,251      |
| G12V-GDP | 4TQ9   | GDP        | 25,689      |
| G12V-GTP | 6GOE   | GNP        | 25,539      |

*\*In silico mutant from 6GOD via PDBFixer v1.12.*

## Simulation Details

GROMACS 2026.0, AMBER99SB-ILDN force field, TIP3P water, GAFF2 ligand parameters (ACPYPE), 0.15 M NaCl, rhombic dodecahedron box, 2 fs time step, PME electrostatics (1.2 nm cutoff), V-rescale thermostat (300 K), Parrinello-Rahman barostat (1.0 bar). NVT and NPT equilibration 100 ps each, production run 200 ns per system.

## Repository Contents

```
structures/            Starting PDB files (raw from RCSB + cleaned)
parameters/            GDP/GNP GAFF2 topologies, Mg2+ parameters, ACPYPE files
simulation_inputs/     Per-system GROMACS inputs (topol.top, .gro, .ndx, .itp)
  mdp/                 Shared parameter files (em, nvt, npt, md)
minimized_structures/  Energy-minimized structures for all 8 systems
scripts/               System setup and simulation pipeline scripts
```

## Quick Start

```bash
cd simulation_inputs/G12D_GTP/
gmx grompp -f ../mdp/em.mdp -c solv_ions.gro -p topol.top -o em.tpr
gmx mdrun -deffnm em -v
gmx grompp -f ../mdp/nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun -deffnm nvt -v
gmx grompp -f ../mdp/npt.mdp -c nvt.gro -r nvt.gro -p topol.top -t nvt.cpt -o npt.tpr
gmx mdrun -deffnm npt -v
gmx grompp -f ../mdp/md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr
gmx mdrun -deffnm md -v
```

## Requirements

GROMACS >= 2023, Python 3.10+, numpy, pandas, matplotlib, seaborn, scipy, MDAnalysis, scikit-learn. See `requirements.txt`.

## Data and Software Availability

All simulation input files, energy-minimized structures, force field parameters, and analysis scripts are provided in this repository.

