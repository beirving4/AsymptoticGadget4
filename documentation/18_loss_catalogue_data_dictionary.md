# LOSS halo-catalogue data dictionary

## Record identity and provenance

The LOSS data record contains FOF/SUBFIND halo catalogues and the descendant
and progenitor link files needed to rebuild merger trees. These files were
produced by upstream GADGET-4 with the LOSS configuration embedded in each
HDF5 file. They were **not** produced by AsymptoticGadget4.

The released catalogues contain only the four standard spherical-overdensity
definitions: Mean200, Crit200, Crit500, and TopHat200. They contain no
Turnaround, TurnLambda, or Lagrangian-radius datasets. AsymptoticGadget4 is a
separate software record that can produce the added fields in a new
FOF/SUBFIND run from particle data; the released catalogues alone cannot be
used to infer those values.

Every catalogue carries `/Header`, `/Parameters`, and `/Config` metadata.
Catalogue `/Header/Git_commit` identifies the producing source revision, while
`/Config/FOF_LINKLENGTH` records the value `0.28`. The embedded metadata is the
authoritative source for per-catalogue configuration differences.

## Fixed archive scope

Each catalogue archive contains:

- `fof_subhalo_tab_000` through `fof_subhalo_tab_074`;
- `subhalo_desc_000` through `subhalo_desc_073`;
- `subhalo_prog_001` through `subhalo_prog_074`.

The record contains no particle snapshots, initial-condition files, assembled
trees, `subhalo_treelink` outputs, derived analysis products, over-cap
snapshots, or `bak-*` files. The `bak-*` link files are intentionally excluded
because they are incompatible with the live catalogue sequence, not merely to
save space.

Products may use a flat one-file layout, for example,
`fof_subhalo_tab_074.hdf5`. Sixteen-piece products are stored as
`groups_074/fof_subhalo_tab_074.P.hdf5`, where `P` runs numerically from 0
through 15. Descendant and progenitor files follow the same layout.

## Indexing and multifile rules

Within one snapshot, concatenate pieces in numeric piece order to recover the
global `/Group` or `/Subhalo` table. Global group, subhalo, and link indices are
zero-based indices into those concatenated tables; they are not piece-local.

For every 16-piece file set:

- `*_ThisFile` is the number of rows physically stored in that piece;
- `*_Total` is the global snapshot count repeated identically in every piece;
- sum `*_ThisFile` across pieces to verify a file set;
- read `*_Total` once—never sum it across pieces.

The type-vector width is `NTYPES=2`. Column 0 is GADGET particle type 0 and
column 1 is type 1. These collisionless LOSS catalogues use type 1; the type-0
entries are zero.

## Units and scale-factor conventions

The embedded parameters define:

- `UnitLength_in_cm = 3.085678e24`: one internal length unit, conventionally
  `1 Mpc/h`;
- `UnitMass_in_g = 1.989e43`: one internal mass unit, conventionally
  `10^10 Msun/h`;
- `UnitVelocity_in_cm_per_s = 1.0e5`: one internal velocity unit, `1 km/s`;
- `HubbleParam = h = 0.68`;
- `/Header/Time = a`, the cosmological scale factor;
- `/Header/Redshift = 1/a - 1`.

For a stored mass `m`, physical solar masses are `m * 10^10 / h`. For a
comoving stored length `x`, comoving Mpc are `x / h` and proper physical Mpc
are `a * x / h`. Length fields explicitly marked physical below already
include the factor of `a`, so convert them to Mpc with `x / h` and do not
multiply by `a` again.

`GroupVel` and `SubhaloVel` have different conventions. `GroupVel` is the
mass-weighted internal canonical velocity `p = a^2 dx/dt`; for a synchronized
group, peculiar velocity is `GroupVel / a`. `GroupAscale` records the
mass-weighted particle scale factor for interpreting that value. `SubhaloVel`
is already converted to physical peculiar `km/s` by SUBFIND.

## HDF5 metadata groups

| Group | Contents |
| --- | --- |
| `/Header` | Snapshot time/redshift, box size, local/global object counts, file count, and catalogue Git provenance. Link-file headers contain their local/global subhalo counts and file count. |
| `/Parameters` | Complete runtime parameter attributes, including cosmology, units, output settings, and IC-generation metadata. |
| `/Config` | Compile-time configuration attributes, including `FOF_LINKLENGTH=0.28`, `NTYPES=2`, `FOF`, `SUBFIND`, `SUBFIND_HBT`, and `MERGERTREE`. |
| `/Group` | One row per FOF group in `fof_subhalo_tab`. |
| `/Subhalo` | One row per resolved SUBFIND subhalo in `fof_subhalo_tab`, or one link row per subhalo in descendant/progenitor files. |
| `/IDs` | Present but empty in these catalogues; member-particle ID lists are not part of this release. |

### `fof_subhalo_tab` header attributes

| Attribute | Type | Meaning |
| --- | --- | --- |
| `BoxSize` | float64 | Periodic comoving box size in internal length units. |
| `Git_commit` | 40-character string | Upstream GADGET-4 source commit that wrote the catalogue. |
| `Git_date` | string | Git date embedded at build time. |
| `Ngroups_ThisFile` | uint64 | Group rows in this piece. |
| `Ngroups_Total` | uint64 | Global group rows in the snapshot, repeated in every piece. |
| `Nids_ThisFile` | uint64 | FOF-member particle count assigned to this piece; the ID dataset itself is not shipped. |
| `Nids_Total` | uint64 | Global FOF-member particle count, repeated in every piece. |
| `Nsubhalos_ThisFile` | uint64 | Subhalo rows in this piece. |
| `Nsubhalos_Total` | uint64 | Global subhalo rows in the snapshot, repeated in every piece. |
| `NumFiles` | int32 | Number of HDF5 pieces for this product/snapshot: 1 or 16. |
| `Time` | float64 | Scale factor `a`. |
| `Redshift` | float64 | `1/a - 1`. |

Descendant and progenitor `/Header` groups contain `Nsubhalos_ThisFile`
(uint64), `Nsubhalos_Total` (uint64), and `NumFiles` (int32), with the same
local/global interpretation.

## FOF group datasets

Shapes below omit the leading `Ngroups_ThisFile` dimension.

| Dataset | Type; row shape | Units/scaling | Meaning and sentinel |
| --- | --- | --- | --- |
| `GroupAscale` | float32; scalar | dimensionless | Mass-weighted scale factor of the member particles. |
| `GroupFirstSub` | int64; scalar | index | Global index of the first subhalo in this group; `-1` when no resolved subhalo exists. |
| `GroupLen` | int32; scalar | count | Total number of FOF-member particles. |
| `GroupLenType` | int32; `[2]` | count | Member-particle count by GADGET type. |
| `GroupMass` | float32; scalar | `10^10 Msun/h` | Sum of all FOF-member particle masses. |
| `GroupMassType` | float32; `[2]` | `10^10 Msun/h` | FOF mass by particle type. |
| `GroupNsubs` | int32; scalar | count | Number of resolved subhalos belonging to this group. |
| `GroupOffsetType` | int64; `[2]` | global particle offset | Number of same-type FOF particles belonging to earlier groups in global catalogue order. Particle lists are not shipped. |
| `GroupPos` | float32; `[3]` | comoving `Mpc/h` | Potential-minimum position of the rank-0 subhalo when one exists; otherwise the periodic FOF centre of mass. |
| `GroupVel` | float32; `[3]` | canonical internal velocity | Mass-weighted `p=a^2 dx/dt`; divide by the applicable scale factor for physical peculiar `km/s`. |
| `Group_M_Mean200` | float32; scalar | `10^10 Msun/h` | Mass inside the radius with mean enclosed density 200 times the cosmic mean matter density. `0` means no accepted resolved crossing. |
| `Group_R_Mean200` | float32; scalar | comoving `Mpc/h` | Radius paired with `Group_M_Mean200`; physical radius is `a R`. `0` follows the mass sentinel. |
| `Group_M_Crit200` | float32; scalar | `10^10 Msun/h` | Mass inside the radius with mean enclosed density 200 times the critical density. `0` means no accepted resolved crossing. |
| `Group_R_Crit200` | float32; scalar | comoving `Mpc/h` | Radius paired with `Group_M_Crit200`; physical radius is `a R`. |
| `Group_M_Crit500` | float32; scalar | `10^10 Msun/h` | Mass inside the radius with mean enclosed density 500 times the critical density. `0` means no accepted resolved crossing. |
| `Group_R_Crit500` | float32; scalar | comoving `Mpc/h` | Radius paired with `Group_M_Crit500`; physical radius is `a R`. |
| `Group_M_TopHat200` | float32; scalar | `10^10 Msun/h` | Generalized spherical-collapse mass. The critical-density threshold is `18 pi^2 + 82 x - 39 x^2`, where `x = Omega_m(a)-1`. `0` means no accepted resolved crossing. |
| `Group_R_TopHat200` | float32; scalar | comoving `Mpc/h` | Radius paired with `Group_M_TopHat200`; physical radius is `a R`. |

The SO centre is the rank-0 subhalo potential minimum. The zero sentinel must
not be interpreted as a physical zero-radius halo.

## SUBFIND subhalo datasets

Shapes below omit the leading `Nsubhalos_ThisFile` dimension.

| Dataset | Type; row shape | Units/scaling | Meaning and sentinel |
| --- | --- | --- | --- |
| `SubhaloCM` | float32; `[3]` | comoving `Mpc/h` | Periodic centre of mass of all bound member particles. |
| `SubhaloGroupNr` | int64; scalar | global group index | Parent FOF-group row in the concatenated `/Group` table. |
| `SubhaloHalfmassRad` | float32; scalar | physical `Mpc/h` | Radius containing half the total bound subhalo mass. |
| `SubhaloHalfmassRadType` | float32; `[2]` | physical `Mpc/h` | Half-mass radius for each particle type; `0` when a type has no defined radius. |
| `SubhaloIDMostbound` | uint32; scalar | particle ID | ID of the most-bound particle. This is the only particle-ID field shipped. |
| `SubhaloLen` | int32; scalar | count | Total number of gravitationally bound member particles. |
| `SubhaloLenType` | int32; `[2]` | count | Bound member-particle count by type. |
| `SubhaloMass` | float32; scalar | `10^10 Msun/h` | Total bound mass. |
| `SubhaloMassType` | float32; `[2]` | `10^10 Msun/h` | Bound mass by particle type. |
| `SubhaloOffsetType` | int64; `[2]` | global particle offset | Same-type FOF-particle offset of the first member of this subhalo in group/subhalo particle ordering. Particle lists are not shipped. |
| `SubhaloParentRank` | int32; scalar | rank | Rank of the parent candidate in the nested SUBFIND hierarchy; ordinary descendants use the rank-0 main subhalo as the root. |
| `SubhaloPos` | float32; `[3]` | comoving `Mpc/h` | Position of the minimum-potential particle. |
| `SubhaloRankInGr` | int32; scalar | rank | Zero-based subhalo rank within the parent FOF group; rank 0 is the main subhalo. |
| `SubhaloSpin` | float32; `[3]` | physical `(Mpc/h) km/s` | Specific angular momentum from physical relative positions and velocities. |
| `SubhaloVel` | float32; `[3]` | physical `km/s` | Mass-weighted peculiar velocity of bound particles; already converted from the canonical integration variable. |
| `SubhaloVelDisp` | float32; scalar | physical `km/s` | One-dimensional bound-particle velocity dispersion, including the local Hubble-flow term used by SUBFIND. |
| `SubhaloVmax` | float32; scalar | physical `km/s` | Maximum of the circular-velocity curve `sqrt(G M(<r)/r)`. |
| `SubhaloVmaxRad` | float32; scalar | physical `Mpc/h` | Physical radius at which `SubhaloVmax` occurs. |

No Turnaround, TurnLambda, `R_Lag`, gas/star-formation, orphan-treatment, or
extended-property datasets occur in the released tables.

## Descendant and progenitor link datasets

All link datasets are signed little-endian int64. `SubhaloNr` is an identity
index and is never a missing-link sentinel. Every other link field uses `-1`
when no link exists; the released files contain no serialized internal
`HALONR_MAX`-style large sentinel.

For transition `s -> s+1`, `subhalo_desc_s` has one row per subhalo at `s`,
while `subhalo_prog_(s+1)` has one row per subhalo at `s+1`.

### `subhalo_desc_s`

| Dataset | Meaning |
| --- | --- |
| `SubhaloNr` | Global zero-based subhalo index at snapshot `s`. |
| `DescSubhaloNr` | Primary, maximum-score descendant index at snapshot `s+1`; `-1` if absent. |
| `FirstDescSubhaloNr` | Head at `s+1` of the linked list of descendants that select this subhalo as progenitor; `-1` if the list is empty. Follow `NextDescSubhaloNr` in `subhalo_prog_(s+1)`. |
| `NextProgSubhaloNr` | Next subhalo at `s` in the linked list sharing the same descendant; `-1` at the end. A list begins at `FirstProgSubhaloNr` in `subhalo_prog_(s+1)`. |

### `subhalo_prog_(s+1)`

| Dataset | Meaning |
| --- | --- |
| `SubhaloNr` | Global zero-based subhalo index at snapshot `s+1`. |
| `ProgSubhaloNr` | Primary, maximum-score progenitor index at snapshot `s`; `-1` if absent. |
| `FirstProgSubhaloNr` | Head at `s` of the linked list of progenitors whose primary descendant is this subhalo; `-1` if the list is empty. Follow `NextProgSubhaloNr` in `subhalo_desc_s`. |
| `NextDescSubhaloNr` | Next subhalo at `s+1` in the linked list sharing the same primary progenitor; `-1` at the end. A list begins at `FirstDescSubhaloNr` in `subhalo_desc_s`. |

The primary descendant and primary progenitor relations are selected
independently from the merger-matching scores and need not be mutual for every
row. Use the explicit chain fields rather than assuming a one-to-one mapping.

## Merger-tree rebuild contract

GADGET-4 restart flag 8 reads exactly `fof_subhalo_tab`, `subhalo_desc`, and
`subhalo_prog`. Particle snapshots and particle IDs are not needed. Assemble
through the release cap with `LAST_SNAPSHOT_NUMBER=74` and an output directory
containing the preserved hierarchy:

```sh
mpirun -np NUMBER_OF_RANKS ./Gadget4 PARAMETER_FILE 8 74
```

The native GADGET-4 tree basename is `trees`; `full_tree*` is a post-hoc rename,
not a native output name. `subhalo_treelink` files are also flag-8 outputs and
are therefore not shipped.

The release invariant is:

`trees/Header/Nhalos_Total == sum over snapshots 000–074 of catalogue Header/Nsubhalos_Total`.

For a multifile snapshot, read `Nsubhalos_Total` once, not once per piece.

When AsymptoticGadget4 reads these legacy catalogues, the nine available
standard group/SO payload fields transfer exactly. Its four optional
Turnaround/TurnLambda tree fields remain zero because the source catalogue
datasets do not exist; zero is not a reconstructed scientific measurement.

## Manifest and integrity

The data deposit supplies a machine-readable manifest containing its scope,
upstream provenance, archive inventory, byte sizes, and per-file checksums.
Use the manifest distributed with the data record to verify a download before
analysis or tree reconstruction.
