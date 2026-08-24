# Contributing

AsymptoticGadget4 is a focused research fork. Contributions should preserve a
clear distinction between upstream GADGET-4 behavior, LOSS-specific behavior,
and new experiments.

## Before opening a change

1. Base work on a topic branch and identify whether the change is inherited
   from upstream, a bug fix in this fork, or a new scientific feature.
2. Do not commit initial conditions, simulation outputs, build products,
   credentials, private paths, allocation names, or machine-local settings.
3. Preserve GADGET-4 copyright and license notices.
4. Document any new compile-time option, runtime parameter, HDF5 field,
   sentinel, unit convention, or restart-compatibility effect.

## Validation

Install the validation-only Python dependencies with:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --requirement requirements-validation.txt
```

Run the lightweight tests:

```sh
python tools/test_build_release_manifest.py
python examples/LOSS/test_derive_lagrangian_radii.py
python tools/check_local_markdown_links.py
bash -n tools/run_graphify.sh
```

Build and execute `examples/LOSS-smoke` using the platform instructions in
`documentation/15_build_portability.md`. Changes to numerical definitions,
catalogue layouts, tree semantics, defaults, or production compatibility also
require a focused regression and author review. Do not respond to a mismatch by
loosening a numerical tolerance without diagnosing the difference.

## Documentation and provenance

Update `MODIFICATIONS.md`, `CHANGELOG.md`, and the relevant schema/build guide
with user-visible changes. Graphify is a navigation aid; direct source review,
Git history, compilation, and runtime tests remain the release evidence.

Report ordinary bugs through the repository issue tracker. Potentially
sensitive reports should use GitHub private vulnerability reporting if it is
enabled rather than placing credentials, private data, or cluster details in a
public issue.
