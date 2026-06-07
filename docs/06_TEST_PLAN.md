# Testplan

## 1. Test bridge

Kør:

./test_bridge.sh

Forventet:

- simple-CPL virker
- dansk CPL virker
- bridge returnerer ok true

## 2. Start GUI

Kør:

export CHROMAPLEX_PYTHON="$PWD/.venv/bin/python"  
cargo run

Forventet:

- Cplex-vinduet åbner
- ingen kritisk runtime-fejl

## 3. Test simple-CPL

Åbn eller indsæt et simple-CPL program.

Test:

- Kompilér
- Kør
- Byg legacy .bin

Forventet:

- compile uden fejl
- run-output vises
- legacy .bin bygges

## 4. Test dansk CPL

Åbn:

vendor/full_potential_demo.cpl

Test:

- Kompilér
- Kør
- Byg bundle

Forventet:

- compile uden fejl
- run uden compilerfejl
- 100 voxels i simulator-flow
- CPA bundle med header CHROMAPLEX_CPA_BUNDLE_V1

## 5. Regression

Efter ændringer må følgende stadig virke:

- simple-CPL compile
- simple-CPL run
- dansk CPL compile
- dansk CPL run
- CPA bundle build
- GUI startup
