#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
import traceback
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor"
if str(VENDOR) not in sys.path:
    sys.path.insert(0, str(VENDOR))


@dataclass
class RunResult:
    dialect: str
    assembly: str
    output: str
    storage: dict[str, Any] = field(default_factory=dict)
    registers: Any = None


def normalise_simple_cpl(source: str) -> str:
    """The bundled simple compiler has greedy ; handling. Normalize final semicolons."""
    cleaned: list[str] = []
    for raw in source.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            cleaned.append(line)
            continue
        if stripped.endswith(";"):
            line = line[: line.rfind(";")]
        cleaned.append(line)
    return "\n".join(cleaned)


def detect_dialect(source: str) -> str:
    text = source.lower()
    markers = ["streng ", "skriv_voxel", "kanal ", "findeksponent", "strengtiltal", "potens "]
    if any(marker in text for marker in markers):
        return "danish-cpl"
    return "simple-cpl"


def compile_source(source: str, dialect: str | None = None) -> tuple[str, str]:
    dialect = dialect or detect_dialect(source)
    if dialect == "danish-cpl":
        from chromaplex.cpl_compiler import compile_cpl

        return compile_cpl(source), dialect

    from chromaplex_os.compiler import CPLCompiler

    compiler = CPLCompiler()
    return compiler.compile(normalise_simple_cpl(source)), "simple-cpl"


def _parse_reg(token: str) -> int:
    m = re.fullmatch(r"R(\d+)", token.strip().upper())
    if not m:
        raise SyntaxError(f"Ugyldigt register: {token}")
    idx = int(m.group(1))
    if idx < 0 or idx > 7:
        raise SyntaxError(f"Register udenfor R0-R7: {token}")
    return idx


def _value(token: str, regs: list[int]) -> int:
    token = token.strip()
    if token.upper().startswith("R"):
        return regs[_parse_reg(token)]
    return int(token, 0)


def run_simple_asm(asm: str) -> RunResult:
    from chromaplex_os.spec import COLOUR_NAMES
    from chromaplex_os.storage import CrystalStorage

    regs = [0] * 8
    storage = CrystalStorage()
    current_colour = COLOUR_NAMES["GREEN"]
    pos = (0, 0, 0)
    out: list[str] = []

    for lineno, raw in enumerate(asm.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith(";"):
            continue
        op, _, rest = line.partition(" ")
        op = op.upper()
        args = [a.strip() for a in rest.split(",") if a.strip()]

        if op == "HALT":
            break
        if op == "MOV":
            regs[_parse_reg(args[0])] = _value(args[1], regs)
        elif op == "ADD":
            regs[_parse_reg(args[0])] += _value(args[1], regs)
        elif op == "SUB":
            regs[_parse_reg(args[0])] -= _value(args[1], regs)
        elif op == "SET_COLOR":
            current_colour = COLOUR_NAMES[args[0].upper()]
        elif op == "POSITION":
            pos = (int(args[0]), int(args[1]), int(args[2]))
        elif op == "LASER_WRITE":
            storage.write_voxel(*pos, current_colour, regs[_parse_reg(args[0])])
        elif op == "LASER_READ":
            regs[_parse_reg(args[0])] = storage.read_voxel(*pos, current_colour)
        elif op == "PRINT":
            out.append(str(regs[_parse_reg(args[0])]))
        else:
            raise SyntaxError(f"Ikke-understøttet ASM-instruktion i editor-runtime på linje {lineno}: {line}")

    storage_dump = {
        f"{x},{y},{z}": {str(color): value for color, value in vox.items()}
        for (x, y, z), vox in storage.data.items()
    }
    output = "\n".join(out) if out else "Program kørte uden PRINT-output."
    output += "\nRegistre: " + repr(regs)
    output += "\nStorage: " + repr(storage_dump)
    return RunResult("simple-cpl", asm, output, storage_dump, regs)


def run_source(source: str) -> RunResult:
    asm, dialect = compile_source(source)
    if dialect == "danish-cpl":
        from chromaplex.cpa_assembler import assemble
        from chromaplex.crystal_simulator import CrystalSimulator

        instrs = assemble(asm)
        sim = CrystalSimulator()
        output_values = sim.execute_program(instrs)
        grid = {}
        for coords, voxel in getattr(sim, "_grid", {}).items():
            grid[str(coords)] = {color: pair for color, pair in voxel.channels.items()}
        output = "Output: " + repr(output_values)
        output += "\nRegistre: " + repr(getattr(sim, "registers", None))
        output += "\nStorage: " + repr(grid)
        return RunResult(dialect, asm, output, grid, getattr(sim, "registers", None))
    return run_simple_asm(asm)


def build_binary_without_print(source: str, output_path: str) -> tuple[str, str]:
    """Build et output-bundle fra CPL.

    simple-cpl:
        Bygger legacy bytecode via chromaplex_os.assembler.

    danish-cpl:
        Bygger et CPA instruction bundle som JSON-bytes med en tydelig magic-header.
        Det er ikke legacy VM-bytecode; det er et simulator-/editor-bundle for CPA-sporet.
    """
    asm, dialect = compile_source(source)

    out = Path(output_path)

    if dialect == "simple-cpl":
        from chromaplex_os.assembler import assemble

        asm_for_bin = "\n".join(
            line for line in asm.splitlines()
            if not line.strip().upper().startswith("PRINT")
        )
        bytecode = assemble(asm_for_bin)
        out.write_bytes(bytecode)
        return str(out), asm_for_bin

    if dialect == "danish-cpl":
        from chromaplex.cpa_assembler import assemble
        import json

        instructions = assemble(asm)
        bundle = {
            "format": "chromaplex-cpa-bundle",
            "version": 1,
            "dialect": dialect,
            "assembly": asm,
            "instructions": instructions,
        }
        payload = "CHROMAPLEX_CPA_BUNDLE_V1\n".encode("utf-8")
        payload += json.dumps(bundle, ensure_ascii=False, indent=2).encode("utf-8")
        out.write_bytes(payload)
        return str(out), asm

    raise ValueError(f"Ukendt dialect til build_binary: {dialect}")


def ok(**payload: Any) -> None:
    print(json.dumps({"ok": True, **payload}, ensure_ascii=False))


def fail(exc: BaseException) -> None:
    print(json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False))


def main() -> int:
    try:
        request = json.loads(sys.stdin.read() or "{}")
        action = request.get("action")
        source = request.get("source", "")
        if action == "compile":
            assembly, dialect = compile_source(source)
            ok(dialect=dialect, assembly=assembly, output="")
        elif action == "run":
            result = run_source(source)
            ok(**asdict(result))
        elif action == "build_binary":
            output_path = request.get("output_path")
            if not output_path:
                raise ValueError("output_path mangler")
            binary_path, asm = build_binary_without_print(source, output_path)
            ok(dialect="simple-cpl", assembly=asm, output=f"Binær fil skrevet: {binary_path}", binary_path=binary_path)
        else:
            raise ValueError(f"Ukendt action: {action}")
        return 0
    except Exception as exc:
        fail(exc)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
