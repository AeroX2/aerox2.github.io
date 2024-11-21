#version 300 es
in vec2 iScreenPosition;
out vec2 v_uv;
void main() {
    v_uv = iScreenPosition * 0.5 + 0.5;
    gl_Position = vec4(iScreenPosition, 0.0, 1.0);
}
