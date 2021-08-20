// Author:
// Title:

#ifdef GL_ES
precision mediump float;
#endif

#define PI 3.1415926535
#define TWO_PI 6.28318530718

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

vec2 squareCanvas() {
    float wh = u_resolution.x / u_resolution.y;
    vec2 r = max(vec2(1.), vec2(wh, 1. / wh));
    vec2 st = gl_FragCoord.xy / u_resolution * r;
    return st;
}

void main() {
    vec2 st = squareCanvas();
    vec2 pos = st * 2. - 1.; // x, y: [-1, 1]
    vec3 color = vec3(0.);

    int N = 3;

    float a = atan(pos.x, pos.y) + PI;
    float au = TWO_PI / float(N);
    float ad = floor(.5+a/au)*au-a; // 到最近顶点的角度差

    float r = cos(ad)*length(pos);

    color = vec3(1.0-smoothstep(.4, .41,r));

    gl_FragColor = vec4(color, 1.0);
}
