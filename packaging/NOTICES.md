# Apex Infinite Hyperterminal - Third-Party Notices

The Apex Infinite Hyperterminal binary distribution bundles the following
third-party components. The apex-infinite-cli source itself is MIT
licensed (see LICENSE).

## Bundled Runtime Components

| Component | License | Role |
| --- | --- | --- |
| Python (CPython) | PSF License | Bundled interpreter runtime |
| PySide6 / Shiboken6 | LGPL-3.0-only (Qt for Python) | Qt bindings for the visual wrapper |
| Qt 6 (via PySide6 wheels) | LGPL-3.0-only | GUI, QML, Quick runtime |
| click | BSD-3-Clause | Base CLI option parsing |
| rich | MIT | Base CLI terminal rendering |
| openai | Apache-2.0 | Manager/summarizer provider client |
| PyYAML | MIT | Config parsing |
| python-dotenv | BSD-3-Clause | Environment loading |
| structlog | MIT / Apache-2.0 | Diagnostic logging |

The generated `dependency-inventory.txt` produced by
`scripts/build-appimage.sh` records the exact bundled versions for each
release artifact.

## LGPL Compliance (Qt / PySide6)

- PySide6 and Qt are dynamically linked inside the bundled Python
  environment; no static linking is performed.
- The AppImage bundles unmodified PySide6 wheels from PyPI. Users can
  replace the bundled Qt/PySide6 libraries by editing the AppDir
  (extract with `--appimage-extract`, swap the wheels inside
  `usr/venv`, and repack), which satisfies the LGPL relinking
  requirement.
- No GPL-only Qt modules are bundled.
- Qt source code is available from https://download.qt.io/ and PySide6
  source from https://code.qt.io/cgit/pyside/pyside-setup.git/.

## Clean-Room Statement

The local `EXAMPLE/` study tree (cool-retro-term, GPL-3.0) is
reference-only. No source code, QML, shaders, generated shader blobs,
images, icons, fonts, profiles, manifests, or packaging scripts from that
tree are included in this repository or any release artifact. Shader
provenance is documented in `src/apex_infinite_visual/shaders/PROVENANCE.md`;
the icon and desktop metadata are original works created for this project.
