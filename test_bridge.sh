#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 python_bridge/chromaplex_bridge.py <<'JSON'
{"action":"run","source":"var x = 1000;\nstore x at (10, 20, 30) colour GREEN;\nload y from (10, 20, 30) colour GREEN;\nprint y;"}
JSON
