#version 440
// Apex Hyperterminal glow composition: accent-tinted additive bloom mix.
// Clean-room original. See PROVENANCE.md.

layout(location = 0) in vec2 qt_TexCoord0;
layout(location = 0) out vec4 fragColor;

layout(std140, binding = 0) uniform buf {
    mat4 qt_Matrix;
    float qt_Opacity;
    vec4 accentColor;
    float glowStrength;    // 0.0 - 1.0
    float chargeLevel;     // event-reactive pulse charge 0.0 - 1.0
};

layout(binding = 1) uniform sampler2D source;
layout(binding = 2) uniform sampler2D blurredSource;

void main() {
    vec4 base = texture(source, qt_TexCoord0);
    vec4 halo = texture(blurredSource, qt_TexCoord0);
    float mixLevel = glowStrength * (0.35 + 0.65 * chargeLevel);
    vec3 tinted = halo.rgb * accentColor.rgb;
    vec3 outColor = base.rgb + tinted * mixLevel;
    fragColor = vec4(outColor, base.a) * qt_Opacity;
}
