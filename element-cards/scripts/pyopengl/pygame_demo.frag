#version 120

uniform vec2 u_resolution;
uniform sampler2D u_texTemplate;
uniform vec2 u_texTemplateResolution;

void main()
{
    vec2 st = gl_FragCoord.xy / u_resolution.xy;

    vec3 color = vec3(0.);
    // color = ;
    // gl_FragColor = vec4(color, 1.0);
    gl_FragColor = texture2D(u_texTemplate, st);
}