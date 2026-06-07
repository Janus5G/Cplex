use anyhow::{anyhow, Context, Result};
use serde::{Deserialize, Serialize};
use slint::SharedString;
use std::fs;
use std::io::Write;
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};

slint::include_modules!();

#[derive(Debug, Serialize)]
struct BridgeRequest<'a> {
    action: &'a str,
    source: &'a str,
    output_path: Option<String>,
}

#[derive(Debug, Deserialize)]
struct BridgeResponse {
    ok: bool,
    dialect: Option<String>,
    assembly: Option<String>,
    output: Option<String>,
    error: Option<String>,
    binary_path: Option<String>,
}

fn app_root() -> PathBuf {
    if let Ok(root) = std::env::var("CHROMAPLEX_EDITOR_ROOT") {
        return PathBuf::from(root);
    }
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
}

fn python_cmd() -> &'static str {
    if cfg!(target_os = "windows") { "python" } else { "python3" }
}

fn call_bridge(action: &str, source: &str, output_path: Option<String>) -> Result<BridgeResponse> {
    let bridge = app_root().join("python_bridge").join("chromaplex_bridge.py");
    if !bridge.exists() {
        return Err(anyhow!("Python bridge mangler: {}", bridge.display()));
    }

    let request = BridgeRequest { action, source, output_path };
    let input = serde_json::to_vec(&request)?;

    let mut child = Command::new(python_cmd())
        .arg(&bridge)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .with_context(|| format!("Kunne ikke starte {}. Installer Python 3 og prøv igen.", python_cmd()))?;

    child.stdin.as_mut().unwrap().write_all(&input)?;
    let output = child.wait_with_output()?;

    if !output.status.success() {
        return Err(anyhow!(
            "Bridge fejlede:\n{}",
            String::from_utf8_lossy(&output.stderr)
        ));
    }

    let response: BridgeResponse = serde_json::from_slice(&output.stdout).with_context(|| {
        format!("Ugyldigt bridge-output: {}", String::from_utf8_lossy(&output.stdout))
    })?;

    if !response.ok {
        return Err(anyhow!(response.error.unwrap_or_else(|| "Ukendt compilerfejl".into())));
    }

    Ok(response)
}

fn set_error(ui: &MainWindow, message: impl AsRef<str>) {
    ui.set_status_text(SharedString::from("Fejl"));
    ui.set_output_text(SharedString::from(message.as_ref()));
}

fn save_to_path(path: &Path, text: &str) -> Result<()> {
    fs::write(path, text).with_context(|| format!("Kunne ikke gemme {}", path.display()))
}

fn main() -> Result<()> {
    let ui = MainWindow::new()?;

    {
        let ui_weak = ui.as_weak();
        ui.on_new_file(move || {
            if let Some(ui) = ui_weak.upgrade() {
                ui.set_file_path(SharedString::from(""));
                ui.set_source_text(SharedString::from("// ChromaPlex CPL\nvar x = 40;\nvar y = x + 2;\nprint y;\n"));
                ui.set_assembly_text(SharedString::from(""));
                ui.set_output_text(SharedString::from(""));
                ui.set_status_text(SharedString::from("Ny fil"));
            }
        });
    }

    {
        let ui_weak = ui.as_weak();
        ui.on_open_file(move || {
            if let Some(ui) = ui_weak.upgrade() {
                if let Some(path) = rfd::FileDialog::new()
                    .add_filter("ChromaPlex", &["cpl"])
                    .add_filter("Alle filer", &["*"])
                    .pick_file()
                {
                    match fs::read_to_string(&path) {
                        Ok(text) => {
                            ui.set_file_path(SharedString::from(path.display().to_string()));
                            ui.set_source_text(SharedString::from(text));
                            ui.set_status_text(SharedString::from("Fil åbnet"));
                        }
                        Err(err) => set_error(&ui, format!("Kunne ikke åbne fil:\n{err}")),
                    }
                }
            }
        });
    }

    {
        let ui_weak = ui.as_weak();
        ui.on_save_file(move || {
            if let Some(ui) = ui_weak.upgrade() {
                let existing = ui.get_file_path().to_string();
                let path = if existing.is_empty() {
                    rfd::FileDialog::new().add_filter("ChromaPlex", &["cpl"]).save_file()
                } else {
                    Some(PathBuf::from(existing))
                };
                if let Some(path) = path {
                    match save_to_path(&path, &ui.get_source_text().to_string()) {
                        Ok(_) => {
                            ui.set_file_path(SharedString::from(path.display().to_string()));
                            ui.set_status_text(SharedString::from("Fil gemt"));
                        }
                        Err(err) => set_error(&ui, format!("Kunne ikke gemme fil:\n{err:?}")),
                    }
                }
            }
        });
    }

    {
        let ui_weak = ui.as_weak();
        ui.on_save_file_as(move || {
            if let Some(ui) = ui_weak.upgrade() {
                if let Some(path) = rfd::FileDialog::new().add_filter("ChromaPlex", &["cpl"]).save_file() {
                    match save_to_path(&path, &ui.get_source_text().to_string()) {
                        Ok(_) => {
                            ui.set_file_path(SharedString::from(path.display().to_string()));
                            ui.set_status_text(SharedString::from("Fil gemt"));
                        }
                        Err(err) => set_error(&ui, format!("Kunne ikke gemme fil:\n{err:?}")),
                    }
                }
            }
        });
    }

    {
        let ui_weak = ui.as_weak();
        ui.on_compile_source(move || {
            if let Some(ui) = ui_weak.upgrade() {
                match call_bridge("compile", &ui.get_source_text().to_string(), None) {
                    Ok(response) => {
                        ui.set_assembly_text(SharedString::from(response.assembly.unwrap_or_default()));
                        let dialect = response.dialect.unwrap_or_else(|| "ukendt".into());
                        ui.set_status_text(SharedString::from(format!("Kompileret: {dialect}")));
                    }
                    Err(err) => set_error(&ui, format!("Compilerfejl:\n{err:?}")),
                }
            }
        });
    }

    {
        let ui_weak = ui.as_weak();
        ui.on_run_source(move || {
            if let Some(ui) = ui_weak.upgrade() {
                match call_bridge("run", &ui.get_source_text().to_string(), None) {
                    Ok(response) => {
                        ui.set_assembly_text(SharedString::from(response.assembly.unwrap_or_default()));
                        ui.set_output_text(SharedString::from(response.output.unwrap_or_default()));
                        let dialect = response.dialect.unwrap_or_else(|| "ukendt".into());
                        ui.set_status_text(SharedString::from(format!("Kørt: {dialect}")));
                    }
                    Err(err) => set_error(&ui, format!("Runtime/compilerfejl:\n{err:?}")),
                }
            }
        });
    }

    {
        let ui_weak = ui.as_weak();
        ui.on_build_binary(move || {
            if let Some(ui) = ui_weak.upgrade() {
                if let Some(path) = rfd::FileDialog::new().add_filter("ChromaPlex bytecode", &["bin"]).save_file() {
                    match call_bridge("build_binary", &ui.get_source_text().to_string(), Some(path.display().to_string())) {
                        Ok(response) => {
                            ui.set_assembly_text(SharedString::from(response.assembly.unwrap_or_default()));
                            ui.set_output_text(SharedString::from(format!(
                                "Binær fil skrevet: {}",
                                response.binary_path.unwrap_or_else(|| path.display().to_string())
                            )));
                            ui.set_status_text(SharedString::from(".bin bygget"));
                        }
                        Err(err) => set_error(&ui, format!("Kunne ikke bygge .bin:\n{err:?}")),
                    }
                }
            }
        });
    }

    ui.run()?;
    Ok(())
}
