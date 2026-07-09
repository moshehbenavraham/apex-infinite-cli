# Apex Hyperterminal Shader Provenance

Every shader source in this directory was authored from scratch for the
Apex Infinite Hyperterminal. No source, constants, formulas, or generated
artifacts were copied from the reference-only `EXAMPLE/` study tree or any
other project.

## Modules

| Module | Purpose |
| --- | --- |
| `surface_postprocess.frag` | Barrel curvature, edge vignette, and glass falloff for the presentation pass |
| `glow_composite.frag` | Accent-tinted additive glow composition over the command surface |
| `noise_field.frag` | Procedural hash-based static noise bounded by quality tier |
| `chroma_edge.frag` | Subtle RGB edge separation for the `subpixel` and `cinematic` modes |
| `persistence_buffer.frag` | Event-row phosphor persistence with explicit decay state |
| `signal_distortion.frag` | Horizontal sync offset and line jitter driven by workflow pulses |

## Rules

- Shader sources are written in Vulkan-style GLSL (`#version 440`) for the
  Qt 6 `qsb` pipeline.
- Generated `.qsb` artifacts are build outputs. They live in
  `shaders/compiled/`, are not tracked by git, and must be regenerated from
  these sources with `scripts/build-shaders.sh` and reviewed before any
  release that bundles them.
- Uniform interfaces are driven by the typed render state exposed by
  `render_caps.py` and the wrapper bridge; shaders never read workflow
  text or secrets.
- If compiled artifacts are absent, `render_caps.detect_capabilities()`
  reports `shaders_available=False` and the QML-only effect layer is used
  automatically.
