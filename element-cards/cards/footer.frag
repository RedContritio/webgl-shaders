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

