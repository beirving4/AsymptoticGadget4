# LOSS smoke test

This reduced 32^3 run is for interface and schema validation only. Its
deliberately late generated initial conditions are not a scientific
reproduction of LOSS.

Build from the repository root with an explicit system profile, for example
`make -j 4 SYSTYPE=Darwin-Homebrew DIR=examples/LOSS-smoke` on a Homebrew Mac
or `SYSTYPE=Generic-system-gcc` when Unix system libraries are on the default
search path. Then run from this directory. A normal start invokes the
compiled-in N-GenIC module and evolves through one quick catalogue checkpoint:

```sh
mpirun -np 2 ./Gadget4 param.txt
mpirun -np 2 ./Gadget4 param.txt 8 0
python validate_outputs.py output
```

The validation should confirm that each HDF5 group catalogue contains
`/Parameters`, `/Config`, the four added turnaround datasets, and no stored
`Group_R_Lag_*` fields. After restartflag 8, group-only tree fields must be
zero on satellite rows.

See the [build portability guide](../../documentation/15_build_portability.md)
for dependencies, the tested platform matrix, and why cross-platform results
should be compared with explicit numerical tolerances rather than bytewise
equality.
