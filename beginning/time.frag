// Author:
// Title:

#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

float r() {
    return abs(sin(u_time));
}

float g() {
	return abs(cos(u_time));
}

float b() {
	return abs(cos(3.*u_time));
}

float a() {
	return 1.;
}

void main() {
    gl_FragColor = vec4(r(), g(), b(), a());
}