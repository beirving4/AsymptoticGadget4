

AsymptoticGadget4
=================

AsymptoticGadget4 is a research fork of GADGET-4 developed for thesis work with
the LOSS simulations. It is an alteration of, and is not an official release
of, GADGET-4. This release line is based directly on official GADGET-4 commit
`2046797b578a3be27433a23a9ba912715a829626` and preserves the upstream
simulation and merger-tree algorithms.

The extensions add two FOF-group spherical-overdensity boundaries:

- `Group_M_Turnaround` / `Group_R_Turnaround`, using
  `Delta = (3 pi / 4)^2` relative to the mean matter density;
- `Group_M_TurnLambda` / `Group_R_TurnLambda`, using the
  cosmological-constant force-balance threshold
  `Delta = 2 OmegaLambda a^3 / Omega0`.

Standard and added FOF properties are also copied onto the main subhalo of
each group in merger-tree output. Satellite tree rows contain zero for these
group-only fields. Lagrangian radii are intentionally not stored because they
can be derived from each mass and the cosmology/unit attributes already in the
HDF5 `/Parameters` group.

The LOSS reference configuration and exact historical inputs are in
[`examples/LOSS`](examples/LOSS). It uses `FOF_LINKLENGTH=0.28`; changing the
setting to the upstream default of 0.2 is supported, but does not reproduce
the published LOSS halo population.

Primary LOSS reproduction path
==============================

The primary reproduction claim is that a user can download the exact archived
LOSS initial conditions from the associated data release, build this tagged
source, initialize the simulation from those files, and evolve it forward.
Regenerating the initial conditions is optional and is not required for this
path. The release data must therefore include the IC checksum and a
ready-to-run parameter file with `InitCondFile`, `ICFormat`, cosmology, units,
starting time, and output schedule set for the archived files.

Before release, this path will be validated by reading the complete archived
IC set, checking its header and particle inventory, advancing beyond
initialization to a short checkpoint, and confirming that the resulting
snapshot and catalogue can be read. The deposited group catalogues, merger
trees, and tree-link files serve both as reference products and as a way to use
the thesis data without rerunning the full simulation; they are not inputs
required merely to start evolving the ICs.

Users may also supply their own GADGET-compatible initial conditions and
configurations. Such runs use this fork's added catalogue and merger-tree
fields but are not LOSS reproductions unless they use the released LOSS inputs
and settings.

Build and validation
====================

AsymptoticGadget4 requires a C++11 compiler, MPI-3, HDF5, GSL, FFTW, zlib,
GNU Make, and Python for the generated build configuration. The repository
provides `Darwin-Homebrew` for native Apple Silicon or Intel macOS builds and
`Generic-system-gcc` for Unix installations whose headers and libraries are
on the compiler's normal search path.

On a Homebrew-equipped Mac, the reduced validation build is:

```sh
brew install open-mpi hdf5 gsl fftw python
make -j 4 SYSTYPE=Darwin-Homebrew DIR=examples/LOSS-smoke
```

The complete platform matrix, run commands, reproducibility expectations, and
current verification status are in
[`documentation/15_build_portability.md`](documentation/15_build_portability.md).
The generated-IC smoke test is an interface test, not a scientific LOSS
reproduction or a substitute for the archived-IC startup validation.

See [`MODIFICATIONS.md`](MODIFICATIONS.md) for the code-level change map and
[`documentation/12_asymptotic_extensions.md`](documentation/12_asymptotic_extensions.md)
for the output schema and compatibility notes. The deterministic code-graph
pass is recorded in
[`documentation/14_graphify_audit.md`](documentation/14_graphify_audit.md).
The graph can be regenerated locally with [`tools/run_graphify.sh`](tools/run_graphify.sh);
large generated graph files are deliberately excluded from release archives.

The remaining author approvals and data-dependent tests are tracked in the
[`publication release checklist`](documentation/16_release_checklist.md).

Cluster acceptance and Zenodo staging
=====================================

The exact archived-IC integration test is intentionally manual because the
simulation inputs are external to GitHub Actions. A pinned, copy-paste handoff
for a Linux/HPC job is in
[`documentation/17_cluster_validation_handoff.md`](documentation/17_cluster_validation_handoff.md).
It keeps the repository private during testing, treats the ICs as immutable,
requires a short checkpoint and FOF/SUBFIND validation before any production
run, and builds a verified Zenodo staging manifest without uploading it.

Citation and license
====================

This modified source is distributed under the retained GNU GPL version 3; see
[`LICENSE`](LICENSE). When using it, cite both the immutable AsymptoticGadget4
software release and the upstream GADGET-4 code paper. Draft machine-readable
metadata is in [`CITATION.cff`](CITATION.cff); the version, software DOI, LOSS
data DOI, thesis link, institution, and ORCID will be added only after author
approval. Attribution and upstream lineage are summarized in
[`AUTHORS.md`](AUTHORS.md).

Relationship to upstream GADGET-4
=================================

![](documentation/img/top.jpg)

GADGET-4 is a massively parallel code for N-body/hydrodynamical
cosmological simulations. It is a flexible code that can be applied to
a variety of different types of simulations, offering a number of
sophisticated simulation algorithms.  An account of the numerical
algorithms employed by the code is given in the original code paper,
subsequent publications, and this documentation.

GADGET-4 was written mainly by
[Volker Springel](mailto:vspringel@mpa-garching.mpg.de), with
important contributions and suggestions being made by numerous people,
including [Ruediger Pakmor](mailto:rpakmor@mpa-garching.mpg.de),
[Oliver Zier](mailto:ozier@mpa-garching.mpg.de), and
[Martin Reinecke](mailto:martin@mpa-garching.mpg.de).


Documentation
=============

For documentation of the code as well as the code paper, please refer
to the [code's web-site](https://wwwmpa.mpa-garching.mpg.de/gadget4).
