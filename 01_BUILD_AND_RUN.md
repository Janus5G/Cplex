# Build og kørsel

## Linux/WSL

Installer afhængigheder:

sudo apt update  
sudo apt install -y build-essential curl pkg-config python3-full python3-venv python3-pip libxkbcommon-dev libxkbcommon-x11-0 libxkbcommon-x11-dev libfontconfig1-dev libgtk-3-dev

Opret Python-miljø:

python3 -m venv .venv  
. .venv/bin/activate  
python -m pip install -r requirements.txt

Start Cplex:

export CHROMAPLEX_PYTHON="$PWD/.venv/bin/python"  
cargo run

Eller brug scripts:

chmod +x run_linux.sh test_bridge.sh  
./test_bridge.sh  
./run_linux.sh

## Windows

Installer først:

- Rust via rustup
- Python 3
- Visual Studio Build Tools med C++ workload

Start derefter:

run_windows.bat

eller:

cargo run
