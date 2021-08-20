// Author:
// Title:

#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform float u_time;

float plot(vec2 st) {
    return smoothstep(0.005, 0., abs(st.y - st.x));
}

void main() {
    vec2 st = gl_FragCoord.xy / u_resolution.xy;

    vec3 color = vec3(st.x);
    
    float pct = plot(st);
    color = (1. - pct) * color + pct * vec3(0., 1., 0.);

    gl_FragColor = vec4(color, 1.0);
}