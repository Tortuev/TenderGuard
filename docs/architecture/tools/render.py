"""Render the architecture document's Mermaid blocks as portable SVG exports."""

import argparse
import os
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mmdc", help="Path to an already installed Mermaid CLI")
    parser.add_argument(
        "--browser", help="Chrome/Chromium executable, if using a local browser"
    )
    args = parser.parse_args()
    tools = Path(__file__).resolve().parent
    base = tools.parent
    document = (base / "architecture.md").read_text(encoding="utf-8")
    blocks = re.findall(
        r"<!-- diagram:([\w-]+) -->\s*```mermaid\n(.*?)\n```", document, re.DOTALL
    )
    diagrams = dict(blocks)
    required = {
        "context",
        "use-cases",
        "components",
        "data-model",
        "analysis-flow",
        "deployment",
    }
    if len(blocks) != len(diagrams) or diagrams.keys() != required:
        raise SystemExit("Expected six uniquely named architecture diagrams.")
    if args.mmdc:
        command = [args.mmdc]
    else:
        npx = shutil.which("npx.cmd" if os.name == "nt" else "npx")
        if not npx:
            raise SystemExit("Install Node.js with npm, or pass --mmdc.")
        command = [npx, "--yes", "--package", "@mermaid-js/mermaid-cli@12.0.0", "mmdc"]
    (base / "export").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="tenderguard-diagrams-") as temporary:
        browser_config = []
        if args.browser:
            import json

            config = Path(temporary) / "browser.json"
            config.write_text(
                json.dumps({"executablePath": str(Path(args.browser).resolve())}),
                encoding="utf-8",
            )
            browser_config = ["--puppeteerConfigFile", str(config)]
        for name, code in sorted(diagrams.items()):
            source = Path(temporary) / (name + ".mmd")
            source.write_text(code + "\n", encoding="utf-8")
            output = base / "export" / (name + ".svg")
            subprocess.run(
                command
                + [
                    "--input",
                    str(source),
                    "--output",
                    str(output),
                    "--configFile",
                    str(tools / "mermaid-config.json"),
                    "--svgId",
                    source.stem,
                    "--backgroundColor",
                    "white",
                    *browser_config,
                ],
                check=True,
            )
            # Preserve word spacing in non-browser SVG viewers and keep the
            # black labels readable when embedded on a dark page.
            svg = output.read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            if root.findall(".//{http://www.w3.org/2000/svg}foreignObject"):
                raise SystemExit(
                    f"HTML labels are not portable vector text: {source.name}"
                )
            x, y, width, height = root.attrib["viewBox"].split()
            background = (
                f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
                'fill="white" aria-hidden="true"/>'
            )
            svg = re.sub(
                r"(<svg\b[^>]*)(>)",
                r'\1 xml:space="preserve"\2' + background,
                svg,
                count=1,
            )
            output.write_text(svg, encoding="utf-8")
            print(output.relative_to(base))


if __name__ == "__main__":
    main()
