// Author:
// Title:

#ifdef GL_ES
precision mediump float;
#endif

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
    vec2 pos = st - vec2(.5);
	
    float r = length(pos)*2.0;
    float a = atan(pos.y,pos.x);

    float f = smoothstep(-.5,1., cos(a*10. + u_time))*0.1+0.5;

    vec3 color = vec3( 1.-smoothstep(f,f+0.02,r) );

    gl_FragColor = vec4(color, 1.0);
}
