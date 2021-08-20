
#ifdef GL_ES
precision highp float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

uniform sampler2D u_texTemplate; // https://patriciogonzalezvivo.github.io/glslCards/html/imgs/tarot-merge.png
uniform vec2 u_texTemplateResolution;

// math.h
#define QTR_PI 0.78539816339
#define HALF_PI 1.5707963267948966192313216916398
#define PI 3.1415926535897932384626433832795
#define TWO_PI 6.2831853071795864769252867665590
#define TAU 6.2831853071795864769252867665590
#define PHI 1.618033988749894848204586834
#define EPSILON 0.0000001

#ifdef GL_OES_standard_derivatives
#extension GL_OES_standard_derivatives : enable
#endif
float aastep(float threshold, float value) {
  // The MIT License (MIT) Copyright (c) 2015 stackgl 
  #ifdef GL_OES_standard_derivatives
  float afwidth = 0.7 * length(vec2(dFdx(value), dFdy(value)));
  return smoothstep(threshold - afwidth, threshold + afwidth, value);
  #else
  return step(threshold, value);
  #endif
}

// PIXELSPIRITDECK - ELEMENTS
// Copyright (c) 2017 Patricio Gonzalez Vivo
// https://github.com/patriciogonzalezvivo/PixelSpiritDeck 

// Card 04
float stroke(float x, float size, float w) {
  float d = aastep(size, x + w * .5) - aastep(size, x - w * .5);
  return clamp(d, 0., 1.);
}

// Card 08
float circleSDF(vec2 st) {
  return length(st - .5) * 2.;
}

// Card 09
float fill(float x, float size) {
  return 1. - aastep(size, x);
}

// Card 10
float rectSDF(vec2 st, vec2 s) {
  st = st * 2. - 1.;
  return max(abs(st.x / s.x), abs(st.y / s.y));
}

// Card 11
float crossSDF(vec2 st, float s) {
  vec2 size = vec2(.25, s);
  return min(rectSDF(st.xy, size.xy), rectSDF(st.xy, size.yx));
}

// Card 12
float flip(float v, float pct) {
  return mix(v, 1. - v, pct);
}

// Card 14
float vesicaSDF(vec2 st, float w) {
  vec2 offset = vec2(w * .5, 0.);
  return max(circleSDF(st - offset), circleSDF(st + offset));
}

// Card 15
float triSDF(vec2 st) {
  st = (st * 2. - 1.) * 2.;
  return max(abs(st.x) * 0.866025 + st.y * 0.5, -st.y * 0.5);
}

// Card 17
float rhombSDF(vec2 st) {
  return max(triSDF(st), triSDF(vec2(st.x, 1. - st.y)));
}

// Card 19
vec2 rotate(vec2 st, float a) {
  st = mat2(cos(a), -sin(a), sin(a), cos(a)) * (st - .5);
  return st + .5;
}

// Card 26
float polySDF(vec2 st, int V) {
  st = st * 2. - 1.;
  float a = atan(st.x, st.y) + PI;
  float r = length(st);
  float v = TAU / float(V);
  return cos(floor(.5 + a / v) * v - a) * r;
}

// Card 27
float hexSDF(vec2 st) {
  st = abs(st * 2. - 1.);
  return max(abs(st.y), st.x * 0.866025 + st.y * 0.5);
}

// Card 28
float starSDF(vec2 st, int V, float s) {
  st = st * 4. - 2.;
  float a = atan(st.y, st.x) / TAU;
  float seg = a * float(V);
  a = ((floor(seg) + 0.5) / float(V) +
    mix(s, -s, step(.5, fract(seg)))) * TAU;
  return abs(dot(vec2(cos(a), sin(a)), st));
}

// Card 30
float raysSDF(vec2 st, int N) {
  st -= .5;
  return fract(atan(st.y, st.x) / TAU * float(N));
}

// Card 34
float heartSDF(vec2 st) {
  st -= vec2(.5, .8);
  float r = length(st) * 5.;
  st = normalize(st);
  return r -
    ((st.y * pow(abs(st.x), 0.67)) /
    (st.y + 1.5) - (2.) * st.y + 1.26);
}

// Card 35
vec3 bridge(vec3 c, float d, float s, float w) {
  c *= 1. - stroke(d, s, w * 2.);
  return c + stroke(d, s, w);
}

// Card 44
vec2 scale(vec2 st, vec2 s) {
  return (st - .5) * s + .5;
}

vec2 ratio(vec2 st, vec2 s) {
  return mix(vec2((st.x * s.x / s.y) - (s.x * .5 - s.y * .5) / s.y, st.y), vec2(st.x, st.y * (s.y / s.x) - (s.y * .5 - s.x * .5) / s.x), step(s.x, s.y));
}

// Card 46
float flowerSDF(vec2 st, int N) {
  st = st * 2. - 1.;
  float r = length(st) * 2.;
  float a = atan(st.y, st.x);
  float v = float(N) * .5;
  return 1. - (abs(cos(a * v)) * .5 + .5) / r;
}

// Card 47
float spiralSDF(vec2 st, float t) {
  st -= .5;
  float r = dot(st, st);
  float a = atan(st.y, st.x);
  return abs(sin(fract(log(r) * t + a * 0.159)));
}

// Title: Vision
// Author: Patricio Gonzalez Vivo

void main() {
  vec3 color = vec3(0.);
  vec2 st = gl_FragCoord.xy / u_resolution.xy;
  st = ratio(st, u_resolution);
  st = scale(st, vec2(1.1912));
  //START
  float v1 = vesicaSDF(st, .5);
  vec2 st2 = st.yx + vec2(.04, .0);
  float v2 = vesicaSDF(st2, .7);
  color += stroke(v2, 1., .05);
  color += fill(v2, 1.) *
           stroke(circleSDF(st), .3, .05);
  color += fill(raysSDF(st, 50), .2) *
           fill(v1, 1.25) *
           step(1., v2);
  //END
  // This just add the fake margins and deck decorations
  if(texture2D(u_texTemplate, vec2(.5)).a == .0) {
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;
    uv = ratio(uv, u_resolution);
    uv = scale(uv, vec2(1., u_texTemplateResolution.x / u_texTemplateResolution.y));
    vec4 colorTemplate = texture2D(u_texTemplate, uv);
    color = mix(color, colorTemplate.rgb, colorTemplate.a);
    color *= 1. - step(.99, uv.x);
    color *= 1. - step(.99, 1. - uv.y);
  }
  gl_FragColor = vec4(color, 1.);
}
