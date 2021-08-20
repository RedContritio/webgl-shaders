
#ifdef GL_ES
precision mediump float;
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
    return smoothstep(threshold-afwidth, threshold+afwidth, value);
    #else
    return step(threshold, value);
    #endif
}

// PIXELSPIRITDECK - ELEMENTS
// Copyright (c) 2017 Patricio Gonzalez Vivo
// https://github.com/patriciogonzalezvivo/PixelSpiritDeck 

vec2 scale(vec2 st, vec2 s) {
    return (st-.5)*s+.5;
}

vec2 ratio(vec2 st, vec2 s) {
    return mix( vec2((st.x*s.x/s.y)-(s.x*.5-s.y*.5)/s.y,st.y), 
                vec2(st.x,st.y*(s.y/s.x)-(s.y*.5-s.x*.5)/s.x), 
                step(s.x,s.y));
}


// Title: The Wall
// Author: Patricio Gonzalez Vivo

#ifdef GL_ES
precision mediump float;
#endif

//GLOBAL_START
float stroke(float x, float s, float w){
    float d = step(s,x+w*.5) - 
              step(s,x-w*.5);
    return clamp(d, 0., 1.);
}
//GLOBAL_END

void main() {
    vec3 color = vec3(0.);
    vec2 st = gl_FragCoord.xy/u_resolution;
    
    st = ratio(st, u_resolution);
    st = scale(st, vec2(1.1912));
    
    //START
    color += stroke(st.x, .5, .15);
    //END
   
    // This just add the fake margins and deck decorations
    if (texture2D(u_texTemplate, vec2(.5)).a == .0) {
        vec2 uv = gl_FragCoord.xy/u_resolution.xy;
        uv = ratio(uv, u_resolution);
        uv = scale(uv, vec2(1.,u_texTemplateResolution.x/u_texTemplateResolution.y));
        vec4 colorTemplate = texture2D(u_texTemplate, uv);
        color = mix(color, colorTemplate.rgb, colorTemplate.a);
        color *= 1.-step(.99,uv.x);
        color *= 1.-step(.99,1.-uv.y);
    }
    gl_FragColor = vec4(color, 1.);
}

