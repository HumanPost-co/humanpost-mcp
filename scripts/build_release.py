"""Build credential-free portable and OpenAI upload bundles deterministically."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FILES = sorted([
    ".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json",
    ".claude-plugin/plugin.json", ".cursor-plugin/plugin.json",
    ".grok-plugin/marketplace.json", ".grok-plugin/plugin.json", ".mcp.json",
    "LICENSE", "README.md", "SECURITY.md", "assets/icon-400.png", "assets/icon.svg",
    "config-cline.json", "config-muse.json", "llms-install.md", "mcp.json",
    "openai/mcp.json", "plugin.json", "scripts/build_release.py",
    "scripts/check_endpoint.py", "skills/humanpost-publishing/SKILL.md",
    "skills/humanpost-publishing/references/api.md",
])


def build(output: Path, version: str, openai: bool) -> Path:
    name = "humanpost-openai-plugin" if openai else "humanpost-plugin"
    archive = output / f"{name}-{version}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for relative in FILES:
            source = ROOT / ("openai/mcp.json" if openai and relative == "mcp.json" else relative)
            if source.is_symlink() or not source.is_file() or not source.resolve().is_relative_to(ROOT):
                raise ValueError(f"Unsafe or missing release file: {relative}")
            data = source.read_bytes()
            if relative.endswith(".json"):
                json.loads(data)
            info = zipfile.ZipInfo(relative, date_time=(2026, 10, 23, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, data)
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None:
            raise ValueError("Archive integrity check failed")
    return archive


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    options = parser.parse_args()
    options.output_dir.mkdir(parents=True, exist_ok=True)
    version = json.loads((ROOT / "plugin.json").read_text())["version"]
    lines = []
    for openai in (False, True):
        archive = build(options.output_dir, version, openai)
        lines.append(f"{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}")
    (options.output_dir / "SHA256SUMS").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
