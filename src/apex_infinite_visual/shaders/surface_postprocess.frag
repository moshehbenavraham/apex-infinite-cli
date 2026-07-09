#version 440
// Apex Hyperterminal presentation pass: curvature, vignette, glass falloff.
// Clean-room original. See PROVENANCE.md.

layout(location = 0) in vec2 qt_TexCoord0;
layout(location = 0) out vec4 fragColor;

layout(std140, binding = 0) uniform buf {
    mat4 qt_Matrix;
    float qt_Opacity;
    float curvatureStrength;   // 0.0 - 1.0
    float vignetteStrength;    // 0.0 - 1.0
    float glassStrength;       // 0.0 - 1.0
};

layout(binding = 1) uniform sampler2D source;

vec2 curve(vec2 uv, float strength) {
    vec2 centered = uv * 2.0 - 1.0;
    float bulge = 1.0 + strength * 0.12 * dot(centered, centered);
    return (centered * bulge) * 0.5 + 0.5;
}

void main() {
    vec2 uv = curve(qt_TexCoord0, curvatureStrength);
    if (uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0) {
        fragColor = vec4(0.0, 0.0, 0.0, qt_Opacity);
        return;
    }
    vec4 color = texture(source, uv);

    vec2 offset = uv * 2.0 - 1.0;
    float edge = dot(offset, offset);
    float vignette = 1.0 - vignetteStrength * 0.35 * edge;
    color.rgb *= clamp(vignette, 0.55, 1.0);

    float sheen = glassStrength * 0.05 * (1.0 - uv.y) * (1.0 - edge * 0.5);
    color.rgb += vec3(sheen);

    fragColor = color * qt_Opacity;
}
