#version 440
// Apex Hyperterminal chroma edge separation for subpixel/cinematic modes.
// Clean-room original. See PROVENANCE.md.

layout(location = 0) in vec2 qt_TexCoord0;
layout(location = 0) out vec4 fragColor;

layout(std140, binding = 0) uniform buf {
    mat4 qt_Matrix;
    float qt_Opacity;
    float chromaStrength;  // 0.0 - 1.0
    vec2 texelSize;        // 1.0 / texture resolution
};

layout(binding = 1) uniform sampler2D source;

void main() {
    vec2 shift = texelSize * chromaStrength * 1.4;
    float red = texture(source, qt_TexCoord0 - vec2(shift.x, 0.0)).r;
    float green = texture(source, qt_TexCoord0).g;
    float blue = texture(source, qt_TexCoord0 + vec2(shift.x, 0.0)).b;
    float alpha = texture(source, qt_TexCoord0).a;
    fragColor = vec4(red, green, blue, alpha) * qt_Opacity;
}
