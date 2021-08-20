// Author:
// Title:

#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

float rectangle(in vec2 position, in vec2 size, in vec2 st) {
    vec2 t = step(position, st) * step(vec2(1.) - (position + size), vec2(1.) - st);
    return t.x * t.y;
}

void main() {
    vec2 st = gl_FragCoord.xy/u_resolution.xy;
    
    vec3 color = vec3(0.);
    
    vec3 red = vec3(0.75, 0.15, 0.2);
    vec3 white = vec3(0.975,0.900,0.780);
    vec3 yellow = vec3(0.970,0.645,0.118);
    vec3 blue = vec3(0., 0.34, 0.48);
    
    float y = 0.;
    
    color = max(color, red * rectangle(vec2(0., y), vec2(0.07, 0.15), st.xy));
    color = max(color, red * rectangle(vec2(0.09, y), vec2(0.09, 0.15), st.xy));
    color = max(color, white * rectangle(vec2(0.21, y), vec2(0.53, 0.15), st.xy));
    color = max(color, white * rectangle(vec2(0.77, y), vec2(0.14, 0.15), st.xy));
    color = max(color, yellow * rectangle(vec2(0.93, y), vec2(0.07, 0.15), st.xy));

    y = 0.18;
    
    color = max(color, red * rectangle(vec2(0., y), vec2(0.07, 0.15), st.xy));
    color = max(color, red * rectangle(vec2(0.09, y), vec2(0.09, 0.15), st.xy));
    color = max(color, white * rectangle(vec2(0.21, y), vec2(0.53, 0.15), st.xy));
    color = max(color, white * rectangle(vec2(0.77, y), vec2(0.14, 0.15), st.xy));
    color = max(color, yellow * rectangle(vec2(0.93, y), vec2(0.07, 0.15), st.xy));

    y = 0.36;
    color = max(color, white * rectangle(vec2(0., y), vec2(0.18, 1.-y), st.xy));
    color = max(color, white * rectangle(vec2(0.21, y), vec2(0.53, 0.56), st.xy));
    color = max(color, white * rectangle(vec2(0.77, y), vec2(0.14, 0.56), st.xy));
    color = max(color, white * rectangle(vec2(0.93, y), vec2(0.07, 0.56), st.xy));
    
    y = 0.94;
    color = max(color, white * rectangle(vec2(0.21, y), vec2(0.53, 0.06), st.xy));
    color = max(color, blue * rectangle(vec2(0.77, y), vec2(0.14, 0.06), st.xy));
    color = max(color, blue * rectangle(vec2(0.93, y), vec2(0.07, 0.06), st.xy));


    gl_FragColor = vec4(color,1.0);
}