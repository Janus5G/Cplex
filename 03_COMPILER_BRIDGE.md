# Compiler bridge

Compiler-bridgen forbinder Rust/Slint-editoren med Python compiler/runtime.

Fil:

python_bridge/chromaplex_bridge.py

## Actions

Bridge-filen understøtter tre primære actions:

compile  
run  
build_binary

## Compile

Input:

{"action": "compile", "source": "..."}

Output indeholder typisk:

- ok
- dialect
- assembly
- output

## Run

Input:

{"action": "run", "source": "..."}

Output indeholder typisk:

- ok
- dialect
- assembly
- output
- storage
- registers

## Build binary / bundle

Input:

{"action": "build_binary", "source": "...", "output_path": "..."}

For simple-CPL bygges legacy bytecode.

For dansk CPL bygges CPA bundle med header:

CHROMAPLEX_CPA_BUNDLE_V1

CPA bundle er ikke det samme som legacy bytecode. Det er et simulator-/editor-bundle til CPA-sporet.
