# ChromaPlex Editor Rust + Slint v0.2

Linux-first, Windows-compatible desktop editor for ChromaPlex CPL.

This is the serious Rust/Slint track, not the earlier Python/Tkinter prototype. The UI shell is Rust + Slint, while the existing Python compiler/runtime is vendored and called through a narrow JSON bridge so the current compiler stack is reused instead of rewritten prematurely.

## Why Rust + Slint

- Native desktop feel on Linux.
- Cross-platform source code for Linux and Windows.
- Smaller and more controlled than Electron/Tauri for an early language tool.
- Good path to a real IDE architecture: compiler bridge today, native parser/LSP later.

Tauri is still a good option if you want a web-based UI and plugin ecosystem. For a language editor, Slint is cleaner for a native first version.

## Features in this package

- Open/save `.cpl` files.
- Compile CPL to CPA assembly.
- Run CPL through the existing Python compiler/simulator stack.
- Build `.bin` for the simple bytecode compiler path.
- Supports both included dialects:
  - simple `var/store/load/print` CPL from `chromaplex_os`
  - Danish CPL with `streng`, `tal`, `potens`, `skriv_voxel`, `kanal` from `chromaplex`
- Vendored compiler code from the uploaded projects.
- JSON-only Python bridge so the Rust GUI stays clean.

## Linux setup

Install Rust and system dependencies:

```bash
sudo apt update
sudo apt install -y build-essential python3 python3-pip curl libxkbcommon-dev libfontconfig1-dev libgtk-3-dev
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
. "$HOME/.cargo/env"
```

Run:

```bash
cd chromaplex_editor_rust_slint
cargo run
```

## Windows setup

Install:

- Rust from rustup.rs
- Python 3
- Visual Studio Build Tools with C++ workload

Then:

```bat
cd chromaplex_editor_rust_slint
cargo run
```

## Test the compiler bridge without GUI

```bash
python3 python_bridge/chromaplex_bridge.py <<'JSON'
{"action":"run","source":"var x = 1000;\nstore x at (10, 20, 30) colour GREEN;\nload y from (10, 20, 30) colour GREEN;\nprint y;"}
JSON
```

Expected output includes `"output": "1000...`.

## Architecture

```text
Rust/Slint GUI
  -> JSON request
    -> python_bridge/chromaplex_bridge.py
      -> vendor/chromaplex_os compiler/assembler/vm path
      -> vendor/chromaplex Danish CPL compiler/simulator path
  <- JSON response with dialect, assembly, output, storage/register state
```

## Next serious IDE milestones

1. Replace TextEdit with a code editor widget layer or Tauri/Monaco frontend if deep editor features are more important than native UI purity.
2. Add diagnostics: line/column errors from compiler bridge.
3. Add syntax highlighting and symbol outline.
4. Add file/project tree.
5. Add a real `chromaplex-lsp` process in Rust.
6. Move parser/compiler pieces from Python to Rust gradually after language grammar stabilizes.
7. Add packaging: AppImage/deb for Linux and MSI/NSIS for Windows.

## Known limitation

This package was assembled in an environment without Cargo installed, so the Rust GUI source could not be compiled here. The Python compiler bridge was tested directly with both compiler dialects.
