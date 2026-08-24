# Reference compile-time configuration for the LOSS L=256 Mpc/h,
# 256^3-particle experiment. This keeps the scientific settings of the
# historical production configuration while omitting cluster-specific tuning.

# Basic operation
PERIODIC
NTYPES=2
RANDOMIZE_DOMAINCENTER
LEAN
SELFGRAVITY
EVALPOTENTIAL

# TreePM gravity
PMGRID=256
ASMTH=1.25
NSOFTCLASSES=1

# Snapshot products
OUTPUT_POTENTIAL
OUTPUT_ACCELERATION
POWERSPEC_ON_OUTPUT

# Haloes, subhaloes, and merger trees
FOF
# LOSS catalogues use b=0.28. Changing this to 0.2 is supported but produces
# a scientifically distinct halo population and does not reproduce LOSS.
FOF_LINKLENGTH=0.28
SUBFIND
SUBFIND_HBT
SUBFIND_STORE_LOCAL_DENSITY
MERGERTREE

# Built-in initial-condition generation. The historical source configuration
# used a 1024^3 displacement FFT while limiting physical modes and particles
# to NSample=GridSize=256 in the runtime parameter file.
NGENIC=1024
NGENIC_2LPT
CREATE_GRID
NGENIC_FIX_MODE_AMPLITUDES
