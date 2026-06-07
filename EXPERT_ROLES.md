# 18 GPT Expert Roles for ChromaPlex Editor

Use the 18 experts as separate review lanes, not as 18 people all changing code at once.

1. Product Architect - defines editor scope and release gates.
2. Language Designer - owns CPL syntax and grammar consistency.
3. Compiler Engineer - owns Python compiler compatibility and future Rust compiler plan.
4. Runtime/VM Engineer - owns CPA execution, bytecode, simulator and storage state.
5. Rust Desktop Engineer - owns Slint/Tauri shell, process model and native packaging.
6. UI/UX Designer - owns editor layout, command palette, panes and keyboard flow.
7. LSP Engineer - owns diagnostics, autocomplete, go-to-definition and formatting.
8. Parser/AST Engineer - designs stable AST and incremental parsing.
9. Security Engineer - reviews subprocess bridge, file access and sandboxing.
10. Linux Packaging Engineer - AppImage/deb/rpm, desktop file, icons, MIME type.
11. Windows Packaging Engineer - MSI/NSIS, PATH/Python detection, signing later.
12. Test Engineer - compiler fixture tests, GUI smoke tests and regression suite.
13. Documentation Engineer - user docs, language docs and developer docs.
14. Build/CI Engineer - GitHub Actions for Linux/Windows builds.
15. Performance Engineer - compiler latency, large files, async process calls.
16. Error Message Specialist - turns raw compiler exceptions into useful diagnostics.
17. Release Manager - versioning, changelog and stable release bundles.
18. Integration Lead - keeps all tracks aligned and rejects conflicting changes.

Recommended workflow:

- One expert proposes.
- One expert reviews.
- One expert tests.
- Integration Lead accepts or rejects.

Do not let all experts rewrite architecture at once. That creates drift.
