# Arkitektur

Cplex består af tre hovedlag:

1. Rust/Slint GUI
2. Python bridge
3. Vendored ChromaPlex compiler/runtime

Flowet er:

Rust/Slint GUI  
→ JSON request  
→ python_bridge/chromaplex_bridge.py  
→ vendor/chromaplex_os eller vendor/chromaplex  
→ JSON response tilbage til GUI

## Rust/Slint GUI

Rust/Slint håndterer:

- vindue
- editorfelter
- knapper
- filåbning
- filgemning
- visning af CPA assembly
- visning af output

## Python bridge

Bridge-filen ligger her:

python_bridge/chromaplex_bridge.py

Den håndterer:

- dialect-detektion
- compile
- run
- build binary/bundle
- JSON-output tilbage til Rust

## Compiler-spor

Cplex understøtter to compiler-spor:

- simple-CPL / legacy bytecode via vendor/chromaplex_os
- dansk CPL / CPA assembly via vendor/chromaplex
