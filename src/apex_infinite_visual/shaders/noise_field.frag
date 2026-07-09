#version 440
// Apex Hyperterminal procedural static noise field.
// Clean-room original hash noise. See PROVENANCE.md.

layout(location = 0) in vec2 qt_TexCoord0;
layout(location = 0) out vec4 fragColor;

layout(std140, binding = 0) uniform buf {
    mat4 qt_Matrix;
    float qt_Opacity;
    float timePhase;       // seconds, wrapped by the caller
    float noiseStrength;   // 0.0 - 1.0
    vec2 gridResolution;   // virtual noise cell resolution
};

float hash21(vec2 point) {
    point = fract(point * vec2(157.31, 113.97));
    point += dot(point, point + 41.53);
    return fract(point.x * point.y);
}

void main() {
    vec2 cell = floor(qt_TexCoord0 * gridResolution);
    float sample1 = hash21(cell + fract(timePhase) * 61.7);
    float level = (sample1 - 0.5) * noiseStrength * 0.12;
    fragColor = vec4(vec3(level), 0.0) * qt_Opacity;
}
