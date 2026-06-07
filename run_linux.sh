#!/usr/bin/env bash
set -euo pipefail
export CHROMAPLEX_EDITOR_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$CHROMAPLEX_EDITOR_ROOT"
cargo run
