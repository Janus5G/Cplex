# Cplex

**Cplex** er en Linux-first, Windows-kompatibel desktop-kodeeditor til **ChromaPlex/CPL** — et eksperimentelt programmeringssprog bygget omkring farvekanaler, potenser, voxels, krystal-lagring og holografisk datatænkning.

Cplex er skabt som det første seriøse editor-miljø til ChromaPlex: ikke bare en tekstboks, men begyndelsen på en rigtig udviklingsplatform for et nyt sprog.

Editoren er bygget med **Rust + Slint** og kobler sig på den eksisterende Python-baserede ChromaPlex compiler/runtime gennem et smalt JSON bridge-lag. Det betyder, at den nuværende compiler, CPA assembler og CrystalSimulator kan bruges direkte, mens editoren gradvist kan vokse mod en mere komplet IDE.

Cplex er ikke den tidligere Python/Tkinter-prototype. Dette er den native editor-retning.

---

## Vision

ChromaPlex/CPL undersøger en anden måde at tænke kode og data på.

I stedet for kun klassiske variabler og hukommelse arbejder sproget med:

- farvekanaler
- potenser og restværdier
- voxels
- krystal-lagring
- CPA assembly
- hologram-rekonstruktion
- simulatorbaseret execution

**Cplex** er editoren, der skal gøre dette sprog praktisk at skrive, teste, forstå og videreudvikle.

Målet er ikke kun at lave endnu en kodeeditor. Målet er at bygge et arbejdsrum til et nyt programmeringssprog.

---

## Status

Cplex kan aktuelt:

- åbne og gemme `.cpl`-filer
- kompilere CPL til CPA assembly
- køre CPL gennem den eksisterende Python compiler/simulator-stack
- bygge legacy `.bin` for simple-CPL/bytecode-sporet
- bygge dansk CPL som `CHROMAPLEX_CPA_BUNDLE_V1`
- køre den fulde hologram-demo gennem compiler, CPA assembler og simulator
- skrive 100 voxels i `full_potential_demo.cpl`
- bruge lokal Python `.venv` via `CHROMAPLEX_PYTHON`
- bevare både legacy simple-CPL og dansk CPL i samme editor

Den fulde demo-pipeline er bekræftet:

```text
full_potential_demo.cpl
→ dansk CPL compiler
→ CPA assembly
→ CPA assembler
→ CrystalSimulator
→ 100 voxels skrevet
→ CPA bundle build
```

---

## Hvorfor Rust + Slint?

Rust + Slint er valgt, fordi Cplex skal være en rigtig native editor og ikke kun en hurtig prototype.

Fordele:

- native desktop-følelse på Linux
- Windows-kompatibel kildekode
- hurtig og kontrolleret runtime
- mindre og mere fokuseret end Electron i den tidlige fase
- god vej mod rigtig IDE-arkitektur
- mulighed for senere Rust-baseret parser, diagnostics og LSP
- mulighed for senere Tauri/Monaco, hvis editor-widget og plugin-økosystem bliver vigtigere

Rust holder fundamentet stærkt. Slint holder UI’et let og native.

---

## Understøttede CPL-spor

Cplex understøtter aktuelt to compiler-spor.

### 1. Simple-CPL / legacy bytecode

Dette spor kommer fra `chromaplex_os`.

Eksempel:

```cpl
var x = 1000;
store x at (10, 20, 30) colour GREEN;
load y from (10, 20, 30) colour GREEN;
print y;
```

Dette spor kan bygges som legacy `.bin`.

### 2. Dansk CPL / CPA-sporet

Dette spor kommer fra `chromaplex`.

Eksempel:

```cpl
streng navn = "ChromaPlex"
tal x = 100
potens p = findEksponent(x)

skriv_voxel(0, 0, 0) {
    kanal rød = p, rest = 0;
}
```

Cplex er også udvidet til at understøtte dele af den fulde hologram-demo:

```cpl
konstant BREDDE = 10
konstant HOEJDE = 10

for y = 0 to HOEJDE-1 {
    for x = 0 to BREDDE-1 {
        pixel pixeldata = hent_pixel(x, y)

        potens r_e, rest r_rest = komponent_til_potens(pixeldata.rød)
        potens g_e, rest g_rest = komponent_til_potens(pixeldata.grøn)
        potens b_e, rest b_rest = komponent_til_potens(pixeldata.blå)

        skriv_voxel(x, y, 0) {
            kanal rød = r_e, rest = r_rest;
            kanal grøn = g_e, rest = g_rest;
            kanal blå = b_e, rest = b_rest;
        }
    }
}
```

For dansk CPL bygges der ikke legacy bytecode. I stedet bygger Cplex et CPA bundle:

```text
CHROMAPLEX_CPA_BUNDLE_V1
```

Dette bundle indeholder CPA assembly og assemblerede instruktioner til simulator-/editor-sporet.

---

## Funktioner

- Rust + Slint desktop-GUI
- filåbning og filgemning
- CPL-kompilering
- CPL-kørsel
- build af simple-CPL legacy `.bin`
- build af dansk CPL som CPA bundle
- Python bridge via JSON
- vendored ChromaPlex compiler/runtime-komponenter
- Linux/WSL startscript
- Windows startscript
- udviklerdokumentation
- demo-program til holografisk voxel-pipeline

---

## Projektstruktur

```text
Cplex/
├── Cargo.toml
├── Cargo.lock
├── README.md
├── requirements.txt
├── run_linux.sh
├── run_windows.bat
├── test_bridge.sh
├── src/
│   └── main.rs
├── ui/
│   └── app.slint
├── python_bridge/
│   └── chromaplex_bridge.py
├── vendor/
│   ├── chromaplex/
│   ├── chromaplex_os/
│   └── full_potential_demo.cpl
└── docs/
```

---

## Arkitektur

```text
Rust/Slint GUI
  -> JSON request
    -> python_bridge/chromaplex_bridge.py
      -> vendor/chromaplex_os
         simple-CPL compiler/assembler/bytecode path
      -> vendor/chromaplex
         dansk CPL compiler/CPA assembler/CrystalSimulator path
  <- JSON response
```

Rust-appen holder GUI og brugerflow rent.

Python-bridgen håndterer:

- dialect-detektion
- compiler-kald
- simulator-kørsel
- legacy bytecode-build
- CPA bundle-build
- JSON-respons tilbage til editoren

Dette gør det muligt at videreudvikle editoren uden at omskrive hele compiler-stacken for tidligt.

---

## Linux/WSL setup

Installer systempakker:

```bash
sudo apt update
sudo apt install -y \
  build-essential \
  curl \
  pkg-config \
  python3-full \
  python3-venv \
  python3-pip \
  libxkbcommon-dev \
  libxkbcommon-x11-0 \
  libxkbcommon-x11-dev \
  libfontconfig1-dev \
  libgtk-3-dev
```

Installer Rust, hvis det ikke allerede er installeret:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
. "$HOME/.cargo/env"
```

Opret Python virtualenv:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start Cplex:

```bash
export CHROMAPLEX_PYTHON="$PWD/.venv/bin/python"
cargo run
```

Eller brug scripts:

```bash
chmod +x run_linux.sh test_bridge.sh
./test_bridge.sh
./run_linux.sh
```

---

## Ubuntu 24.04 og PEP 668

Ubuntu 24.04 blokerer normalt global `pip install`.

Brug derfor ikke:

```bash
python3 -m pip install numpy
```

Brug i stedet lokal `.venv`:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
export CHROMAPLEX_PYTHON="$PWD/.venv/bin/python"
cargo run
```

---

## Kendt WSL-fejl: libxkbcommon-x11.so

Hvis Cplex fejler med:

```text
Library libxkbcommon-x11.so could not be loaded
```

så installer:

```bash
sudo apt update
sudo apt install -y libxkbcommon-x11-0 libxkbcommon-dev libxkbcommon-x11-dev
```

Start derefter igen:

```bash
cargo run
```

---

## Windows setup

Installer:

- Rust via rustup
- Python 3
- Visual Studio Build Tools med C++ workload

Start derefter:

```bat
run_windows.bat
```

eller manuelt:

```bat
cargo run
```

---

## Test compiler-bridge uden GUI

Simple-CPL test:

```bash
python3 python_bridge/chromaplex_bridge.py <<'JSON'
{"action":"run","source":"var x = 1000;\nstore x at (10, 20, 30) colour GREEN;\nload y from (10, 20, 30) colour GREEN;\nprint y;"}
JSON
```

Dansk CPL/full demo test:

```bash
python - <<'PY'
import json
import subprocess
import sys
from pathlib import Path

src = Path("vendor/full_potential_demo.cpl").read_text(encoding="utf-8")
req = json.dumps({"action": "run", "source": src}, ensure_ascii=False)

p = subprocess.run(
    [sys.executable, "python_bridge/chromaplex_bridge.py"],
    input=req,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

print("STDERR:")
print(p.stderr)
print("STDOUT:")
print(p.stdout[:4000])
PY
```

Forventet resultat:

```text
"ok": true
"dialect": "danish-cpl"
```

---

## Byg dansk CPL som CPA bundle

Dansk CPL bygges som et CPA bundle med header:

```text
CHROMAPLEX_CPA_BUNDLE_V1
```

Eksempel:

```bash
python - <<'PY'
import json
import subprocess
import sys
from pathlib import Path

src = Path("vendor/full_potential_demo.cpl").read_text(encoding="utf-8")
req = json.dumps({
    "action": "build_binary",
    "source": src,
    "output_path": "vendor/full_potential_demo.bin",
}, ensure_ascii=False)

p = subprocess.run(
    [sys.executable, "python_bridge/chromaplex_bridge.py"],
    input=req,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

print(p.stderr)
print(p.stdout)
PY
```

Forventet resultat:

```text
"ok": true
"binary_path": "vendor/full_potential_demo.bin"
```

Headeren i filen bør starte med:

```text
CHROMAPLEX_CPA_BUNDLE_V1
```

---

## Hent projektet

Du kan hente Cplex direkte fra GitHub:

```bash
git clone https://github.com/Janus5G/Cplex.git
cd Cplex

chmod +x run_linux.sh test_bridge.sh
./test_bridge.sh
./run_linux.sh

python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
export CHROMAPLEX_PYTHON="$PWD/.venv/bin/python"
cargo run

## Kendte begrænsninger

Cplex er stadig en tidlig editor.

Aktuelle begrænsninger:

- teksteditoren er simpel og ikke en fuld IDE-editor endnu
- run-output kan stadig blive for langt ved store programmer
- diagnostics har ikke fuld linje/kolonne-visning endnu
- hologram-visning er endnu ikke en rigtig grafisk visualisering
- dele af hologram-demoen er compile-time demo-understøttelse
- dansk CPL og simple-CPL bruger forskellige outputmodeller
- CPA bundle er ikke det samme som legacy bytecode

---

## Næste milepæle

1. Gøre `Kør`-output kort og læsbart.
2. Beholde fuld CPA assembly i `Kompilér`.
3. Omdøbe `.bin`-flowet tydeligt til CPA bundle for dansk CPL.
4. Tilføje bedre fejlvisning med linjenummer og forslag.
5. Tilføje syntaksfremhævning.
6. Tilføje projekt-/filtræ.
7. Tilføje rigtig hologram-preview.
8. Tilføje `cplex-lsp`.
9. Flytte stabile compilerdele gradvist fra Python til Rust.
10. Tilføje Linux AppImage/deb og Windows installer.

---

## Udviklingsprincip

Cplex bygges kontrolleret.

Reglen er:

```text
Få én del til at virke.
Test den.
Lås den.
Byg næste lag.
```

ChromaPlex/CPL er stadig under udvikling, og editoren skal følge sproget uden at skjule fejl eller fake resultater.

Derfor skal Cplex:

- vise reelle compilerfejl
- ikke ignorere ukendt syntaks
- adskille legacy bytecode og CPA bundle tydeligt
- genbruge fungerende compilerdele
- gradvist flytte stabile dele til Rust, når sproget er klar

---

## Kort sagt

**Cplex er det første native udviklingsmiljø til ChromaPlex/CPL.**

Det er bygget til at hjælpe sproget videre fra eksperiment og compiler-demo til et reelt programmeringsmiljø, hvor kode kan skrives, køres, forstås og udvikles videre.

Dette repo er fundamentet.
