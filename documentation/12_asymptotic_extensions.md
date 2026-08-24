# AsymptoticGadget4 extensions

## Catalogue data flow

SUBFIND evaluates spherical-overdensity masses and radii around the main
subhalo centre. The resulting values are stored once per FOF group in the
HDF5 `/Group` table. During restartflag 8, the merger-tree assembler reloads
the group catalogues and copies the group properties only onto the main
subhalo (`SubRankInGr == 0`). Satellite tree rows contain zero for these
group-level fields.

The extension changes the property payload, not the descendant/progenitor
algorithm or tree topology.

## Added definitions

| Name | Threshold relative to mean matter density | Scope |
|---|---:|---|
| Turnaround | `(3 pi / 4)^2` | EdS-exact constant approximation |
| TurnLambda | `2 OmegaLambda a^3 / Omega0` | cosmological constant only |

Search radii never exceed `0.45 * BoxSize`. A zero mass/radius means that no
valid resolved crossing was found inside the permitted range or that the
enclosed mass failed the standard minimum-particle criterion.

## Group catalogue schema

Added `/Group` datasets:

- `Group_M_Turnaround`
- `Group_R_Turnaround`
- `Group_M_TurnLambda`
- `Group_R_TurnLambda`

They use the same internal mass and coordinate units as the standard SO
fields. The generic HDF5 writer also records runtime inputs in `/Parameters`
and compile-time settings in `/Config`.

## Tree schema

The `/TreeHalos` table carries `GroupMass` and the mass/radius pairs for
Mean200, Crit200, Crit500, TopHat200, Turnaround, and TurnLambda. Values are
meaningful only on the main subhalo of an FOF group; satellite values are zero.
Merger-tree and `subhalo_treelink` files record `Git_commit` and `Git_date` in
their `/Header` attributes so every assembled product identifies its source
revision.

For a real multi-subhalo fixture, validate satellite zero-initialization,
provenance, FOF definition, and exact catalogue-to-tree transfer with:

```sh
python3 tools/validate_loss_tree_fields.py OUTPUT/treedata/trees.hdf5 \
  --catalogue-dir OUTPUT \
  --expected-commit "$(git rev-parse HEAD)" \
  --expected-fof-link-length 0.28
```

The validator accepts single- or multi-file catalogue and tree layouts. It
requires at least one satellite row, checks that no stored `R_Lag` dataset is
present, and compares every source catalogue field that exists exactly (not
with a floating-point tolerance).

## Derived Lagrangian radius

Lagrangian radii are not stored. For any catalogue mass definition `M`, the
comoving radius is

`R_Lag = [3 M / (4 pi rho_m,0)]^(1/3)`.

The required `Omega0`, `Hubble`, gravitational-constant setting, and unit
parameters are already present in `/Parameters`. Run:

```sh
python3 examples/LOSS/derive_lagrangian_radii.py \
  output/fof_subhalo_tab_000.hdf5 \
  --output lagrangian_radii_000.npz
```

The output radii use the catalogue's internal comoving length unit.
