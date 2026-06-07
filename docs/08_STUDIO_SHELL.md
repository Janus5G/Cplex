# Cplex Studio Shell

Cplex Studio Shell er den planlagte visuelle arbejdsflade for Cplex.

Retningen bygger på tre ting:

1. Den fungerende Cplex engine
2. Det gamle ChromaPlex Developer Studio layout
3. index.html-simulatorens terminal/krystal-look

## Mål

Cplex skal ikke kun være en teksteditor.

Målet er et visuelt udviklingsmiljø til ChromaPlex/CPL med:

- editor
- generated CPA
- bytecode/bundle status
- VM summary
- terminal
- storage events
- simulatorpanel
- skins

## Foreslået layout

Topbar:

- Cplex
- Open Project
- Simulation Mode
- Hardware Locked
- Compile
- Run Sim
- Build Bundle
- Status

Venstre panel:

- Project
- åbne filer
- demoer
- status

Midterpanel:

- Source
- Generated CPA
- Bytecode / Bundle

Højre panel:

- VM Summary
- Storage
- Bytecode Meta
- Mode
- Hardware
- Status

Bundpanel:

- Terminal
- JSONL Events
- Storage Events

## Første skin

Første skin bør hedde:

Chroma Terminal

Farver:

- baggrund: næsten sort
- paneler: mørk blå/sort
- primary: cyan
- accent: neon grøn
- warning/locked: pink/rød
- font: monospace

## Simulator-retning

Simulatoren skal senere kunne vise:

- voxel-grid
- farvekanaler
- aktive CPA-instruktioner
- storage writes
- storage reads
- registerstatus
- hologram-preview
