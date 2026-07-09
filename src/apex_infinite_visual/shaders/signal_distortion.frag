#version 440
// Apex Hyperterminal sync offset and line jitter, workflow-pulse driven.
// Clean-room original. See PROVENANCE.md.

layout(location = 0) in vec2 qt_TexCoord0;
layout(location = 0) out vec4 fragColor;

layout(std140, binding = 0) uniform buf {
    mat4 qt_Matrix;
    float qt_Opacity;
    float timePhase;       // seconds, wrapped by the caller
    float jitterStrength;  // 0.0 - 1.0
    float syncStrength;    // 0.0 - 1.0
    float faultLevel;      // 0.0 - 1.0, raised on error signatures
};

layout(binding = 1) uniform sampler2D source;

float lineHash(float row) {
    return fract(sin(row * 91.7 + timePhase * 3.1) * 4375.53);
}

void main() {
    vec2 uv = qt_TexCoord0;
    float row = floor(uv.y * 240.0);
    float jitter = (lineHash(row) - 0.5) * jitterStrength * 0.004;

    float band = smoothstep(0.0, 0.08,
        abs(fract(uv.y - timePhase * 0.11) - 0.5) - 0.42);
    float sync = band * syncStrength * (0.01 + faultLevel * 0.02);

    uv.x = clamp(uv.x + jitter + sync, 0.0, 1.0);
    fragColor = texture(source, uv) * qt_Opacity;
}
