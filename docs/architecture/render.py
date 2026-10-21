"""Render architecture sources with a pinned Mermaid CLI; run from any directory."""

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
    base = Path(__file__).resolve().parent
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
        for source in sorted((base / "src").glob("*.mmd")):
            output = base / "export" / (source.stem + ".svg")
            subprocess.run(
                command
                + [
                    "--input",
                    str(source),
                    "--output",
                    str(output),
                    "--configFile",
                    str(base / "mermaid-config.json"),
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
