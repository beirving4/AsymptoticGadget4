#!/usr/bin/env bash
set -euo pipefail

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
output_root="${1:-${repository_root}}"
expected_version="graphify 0.9.44"
installed_version="$(graphify --version)"

if [[ "${installed_version}" != "${expected_version}" ]]; then
  echo "expected ${expected_version}, found ${installed_version}" >&2
  echo "review Graphify release changes before updating the pinned version" >&2
  exit 2
fi

mkdir -p "${output_root}"
export GRAPHIFY_QUERY_LOG_DISABLE=1

graphify extract "${repository_root}" --code-only --no-cluster --out "${output_root}"

graph_json="${output_root}/graphify-out/graph.json"
graph_tree="${output_root}/graphify-out/GRAPH_TREE.html"

graphify diagnose multigraph --graph "${graph_json}"
graphify tree --graph "${graph_json}" --output "${graph_tree}" --root . --label AsymptoticGadget4

echo "Graphify artifacts: ${output_root}/graphify-out"
