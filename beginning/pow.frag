// Author:
// Title:

#ifdef GL_ES
precision mediump float;
#endif

#define PI 3.1415926

uniform vec2 u_resolution;
uniform float u_time;

float plot(vec2 st, float pct) {
    return smoothstep(pct - 0.02, pct, st.y) - smoothstep(pct, pct + 0.02, st.y);
}

void main() {
    vec2 st = gl_FragCoord.xy / u_resolution.xy;
    float y = pow(st.x, 5.);
	// float y = 0.5 + 0.5 * sin(st.x * 2. * PI);

    vec3 color = vec3(y);

    float pct = plot(st, y);
    color = (1. - pct) * color + pct * vec3(0., 1., 0.);

    gl_FragColor = vec4(color, 1.0);
}