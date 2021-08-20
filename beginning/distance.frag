// Author:
// Title:

#ifdef GL_ES
precision mediump float;
#endif

#define TWO_PI 6.28318530718

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

void main() {
    vec2 st = gl_FragCoord.xy / u_resolution;
    float pct = 0.0;

    float radius = 0.3;
    float alpha = 0.1 * TWO_PI * u_time;
    vec2 p = vec2(radius * cos(alpha), vec2(radius * sin(alpha)));

    pct = distance(st, vec2(0.5) + p) + distance(st, vec2(0.5));
    pct = distance(st, vec2(0.5) + p) * distance(st, vec2(0.5));
    pct = pow(distance(st, vec2(0.5) + p), distance(st, vec2(0.5)));
    pct = max(distance(st, vec2(0.5) + p), distance(st, vec2(0.5)));
    pct = min(distance(st, vec2(0.5) + p), distance(st, vec2(0.5)));

    pct = smoothstep(0.1, 1., pct);
    vec3 color = vec3(pct);

    gl_FragColor = vec4(color, 1.0);
}
