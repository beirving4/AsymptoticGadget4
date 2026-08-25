

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

LOSS software validation and catalogue record
=============================================

The software and data releases have distinct provenance. The LOSS Zenodo data
record contains standard-SO halo catalogues produced by upstream GADGET-4
commit `1e171a4a679d30ac1e6accabe8a76a037ccbacac`, not by this fork. It ships
`fof_subhalo_tab`, `subhalo_desc`, and `subhalo_prog` through snapshot 074 so
users can analyze the catalogues directly and rebuild native merger trees. It
does not ship initial conditions, particle snapshots, assembled trees, or
tree-link outputs.

AsymptoticGadget4's compatibility with the exact archived LOSS initial
conditions was tested separately on Linux x86-64. The pinned candidate read all
16,777,216 particles in the 256-cubed IC, advanced beyond initialization,
wrote and reopened a finite checkpoint with exact ID-set equality, and left the
source IC checksum unchanged. The archived ICs remain preserved validation
inputs outside the current catalogue record; the record is therefore not a
complete from-IC reproduction package.

Users may supply their own GADGET-compatible initial conditions and
configurations to produce this fork's added catalogue and merger-tree fields.
The released standard catalogues do not contain Turnaround or TurnLambda and
cannot be used to derive those values without a new FOF/SUBFIND run from
particle data. The released HDF5 schema and link semantics are documented in
[`documentation/18_loss_catalogue_data_dictionary.md`](documentation/18_loss_catalogue_data_dictionary.md).

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
reproduction. The Linux exact-IC result and remaining macOS/large-box gates are
recorded separately in the portability guide.

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
simulation inputs are external to GitHub Actions. The Linux/HPC acceptance run
has passed, and its pinned, copy-paste procedure is retained in
[`documentation/17_cluster_validation_handoff.md`](documentation/17_cluster_validation_handoff.md).
It treats the ICs as immutable and requires a short checkpoint plus
FOF/SUBFIND validation. The separately scoped catalogue archives and release
manifest have also passed clean-extraction hash verification; transfer to an
unpublished Zenodo draft remains a cluster-side release step.

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
