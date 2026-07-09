#version 440
// Apex Hyperterminal event-row phosphor persistence with explicit decay.
// Clean-room original. See PROVENANCE.md.

layout(location = 0) in vec2 qt_TexCoord0;
layout(location = 0) out vec4 fragColor;

layout(std140, binding = 0) uniform buf {
    mat4 qt_Matrix;
    float qt_Opacity;
    float decayPerFrame;   // 0.0 - 1.0, derived from quality tier fps
    float trailStrength;   // 0.0 - 1.0
};

layout(binding = 1) uniform sampler2D currentFrame;
layout(binding = 2) uniform sampler2D previousAccumulation;

void main() {
    vec4 now = texture(currentFrame, qt_TexCoord0);
    vec4 past = texture(previousAccumulation, qt_TexCoord0);
    vec3 faded = past.rgb * (1.0 - decayPerFrame);
    vec3 accumulated = max(now.rgb, faded * trailStrength);
    fragColor = vec4(accumulated, 1.0) * qt_Opacity;
}
