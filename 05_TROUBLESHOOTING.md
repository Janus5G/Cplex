# Fejlfinding

## ModuleNotFoundError: No module named 'numpy'

Brug lokal Python virtualenv:

python3 -m venv .venv  
. .venv/bin/activate  
python -m pip install -r requirements.txt  
export CHROMAPLEX_PYTHON="$PWD/.venv/bin/python"  
cargo run

## Ubuntu 24.04 externally-managed-environment

Ubuntu 24.04 blokerer global pip-install.

Brug .venv i stedet for global pip.

Brug ikke --break-system-packages.

## Library libxkbcommon-x11.so could not be loaded

Installer:

sudo apt update  
sudo apt install -y libxkbcommon-x11-0 libxkbcommon-dev libxkbcommon-x11-dev

Start derefter igen:

cargo run

## xdg color schemes warning

I WSL kan denne advarsel forekomme:

Error watching for xdg color schemes

Den er normalt ufarlig og stopper ikke Cplex.

## Build .bin fejler på dansk CPL

Dansk CPL bygger ikke legacy bytecode.

Det skal bygges som CPA bundle med header:

CHROMAPLEX_CPA_BUNDLE_V1

Hvis UI stadig siger “Byg .bin”, bør teksten senere ændres til “Byg bundle”.
