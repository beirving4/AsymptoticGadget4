# Graphify code-graph audit

## Reproducible local pass

The current working tree was indexed with Graphify 0.9.44 using the tracked
`tools/run_graphify.sh` recipe. The script pins the expected Graphify version,
runs the local AST extractor, diagnoses edge-collapse risk, and produces a
hierarchical HTML inspector:

```sh
tools/run_graphify.sh
```

An optional first argument redirects the generated artifact root outside the
repository. No LLM backend, API key, remote model, document extraction,
community labeling, or network service is used. `.graphifyignore` removes
generated products, data, images, and the vendored `half` and `vectorclass`
implementations so project architecture is not dominated by third-party type
nodes.

The 2026-08-24 pass found 182 code files and produced 2,727 nodes and 7,007 raw
edges. It skipped 41 documentation files by request and 48 unclassified files
such as licenses, Makefile fragments, and text configuration/data inputs.
Fourteen macro-heavy C++ translation units produced parser warnings and may be
only partially represented; these warnings are Graphify limitations, not
compiler failures.

The committed release-candidate graph was regenerated with the working tree at
AsymptoticGadget4 commit `2c025f1e190c708e7f9760484b5abd3816fdc386`, based
on official GADGET-4 commit `2046797b578a3be27433a23a9ba912715a829626`.
The follow-up audit-record commit changes only this skipped Markdown file, so it
does not alter the extracted code graph. Regenerate once more after the final
release tag so the public audit can name the immutable tag and release DOI.

The multigraph diagnostic found 1,266 dangling edge endpoints, two directed
same-endpoint edge groups that lose one relation during the post-build
`DiGraph` conversion, and no exact duplicate edges or missing endpoint IDs.
The post-build graph contains 5,740 edges. Important conclusions must therefore
be confirmed in source or by a runtime test.

The generated `graphify-out` directory is about 8.0 MB, `graph.json` is about
2.9 MB, and `GRAPH_TREE.html` is about 160 KB. These reproducible products are
ignored by Git because they are tool-version-sensitive generated artifacts;
the pinned recipe, filters, and this audited summary are the release sources.
To publish generated graph files later, review their stability, usefulness,
and disclosure surface before removing the ignore rule.

## Evidence layers

The deterministic graph contains source code only. The
[official GADGET-4 site](https://wwwmpa.mpa-garching.mpg.de/gadget4/),
[official paper](https://arxiv.org/abs/2010.03567), and
[upstream manual](https://wwwmpa.mpa-garching.mpg.de/gadget4/gadget4_manual.pdf)
provide context for baseline algorithms, but are not silently merged into AST edges.
The release audit keeps these evidence layers distinct:

- `UPSTREAM_SOURCE_BASE`: official commit
  `2046797b578a3be27433a23a9ba912715a829626`;
- `OFFICIAL_PAPER_AND_MANUAL`: baseline algorithm and usage descriptions;
- `LOCAL_EXTENSION`: the reviewed working-tree changes listed in
  `MODIFICATIONS.md`;
- `INFERENCE`: Graphify edges marked inferred or ambiguous.

The official sources do not establish the scientific meaning of Turnaround or
TurnLambda fields, because those are local extensions. Their definitions are
supported by the local source, release documentation, and validation tests.

## Findings and verification

- **High confidence:** `mergertree` remains the highest-degree project node
  (degree 129), followed by the generic tree, I/O, domain, MPI communication,
  FOF, and N-GenIC classes. Excluding vendored numerical types makes this hub
  list substantially more useful for change-risk review.
- **High confidence:** Graphify locates
  `fof<partset>::subfind_overdensity()` in `src/subfind/subfind_so.cc` at its
  current source location. Direct source inspection and the one- and two-rank
  smoke runs verify that this is the producer of the standard and added SO
  values.
- **High confidence:** Graphify locates
  `mergertree::halotrees_assign_global_subhalonr_and_groupnr()` in
  `src/mergertree/halotrees.cc`. Direct inspection verifies the group-to-main-
  subhalo field transfer, and the runtime tree test verifies catalogue loading
  and serialization.
- **High confidence:** Graphify found both snapshot and light-cone functions
  named `io_func_accel`, correctly marking an unqualified query ambiguous.
  The changed snapshot implementation was verified directly in
  `src/io/snap_io.h` and with an HDF5 FOF read/write round trip.
- **Limited confidence:** Graphify does not model individual C++ structure
  fields as first-class nodes and its broad natural-language query for group
  field transfer returns a noisy neighborhood. The field-by-field lineage in
  `MODIFICATIONS.md` and `documentation/12_asymptotic_extensions.md` comes
  from source inspection and tests, not from an inferred graph edge.
- **Limited confidence:** fourteen partially parsed translation units and the
  dangling endpoints mean that graph reachability cannot establish that
  preprocessor-guarded or template-heavy code is dead.

Graph edges are never used alone to remove code or establish scientific
meaning. Git history establishes provenance; direct source inspection,
successful compilation, and end-to-end HDF5 tests are the authoritative
evidence for release claims.

## Useful local queries

```sh
graphify god-nodes --top 15 --graph graphify-out/graph.json
graphify explain subfind_overdensity --graph graphify-out/graph.json
graphify explain "mergertree::halotrees_assign_global_subhalonr_and_groupnr()" --graph graphify-out/graph.json
graphify query "Where are FOF group properties transferred into merger-tree records?" --graph graphify-out/graph.json
```

The query output should be treated as navigation assistance. Follow every
inferred or ambiguous edge to the cited source and verify runtime-sensitive
paths with an applicable test.
