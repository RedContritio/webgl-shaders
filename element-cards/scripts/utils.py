#!/usr/bin/python
# -*- coding: UTF-8 -*-

from PIL import Image, ImageFont, ImageDraw
import numpy as np
import re
import functools


def foldl(func, acc, xs):
    return functools.reduce(func, xs, acc)


def InvertRGBA(image, mask):
    mask_array = np.array(mask)
    image_array = np.array(image)
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            if mask_array[i, j]:
                for c in range(3):
                    image_array[i, j][c] = 255 - image_array[i, j][c]
    return Image.fromarray(image_array)


def getMetaFromFrag(card_name, codelines):
    meta = {'id': card_name[1:3], 'name': card_name[4:], 'codes': []}

    READ_STATE = 0  # 0 normal, 1 global, 2 segment

    for codes in codelines:
        if codes.lstrip().startswith('//'):
            content = codes.lstrip()[2:].strip()
            if content.startswith('Title:'):
                meta['title'] = content[6:].strip()
            if content.startswith('Author:'):
                meta['author'] = content[7:].strip()
            if content.startswith('Number:'):
                meta['number'] = content[7:].strip()
            if content.startswith('Deps'):
                meta['predefined-deps'] = content[4:].strip().split()
            if content.startswith('GLOBAL_END'):
                assert READ_STATE == 1
                READ_STATE = 0
            if content.startswith('END'):
                assert READ_STATE == 2
                READ_STATE = 0
                meta['codes'] += ['...', '']

        if READ_STATE == 1 or READ_STATE == 2:
            meta['codes'].append(re.sub('\t', '    ', codes[:-1]))

        if codes.lstrip().startswith('//'):
            if content.startswith('GLOBAL_START'):
                assert READ_STATE == 0
                READ_STATE = 1
            if content.startswith('START'):
                assert READ_STATE == 0
                READ_STATE = 2
                meta['codes'] += [' ', ' ', '...']

    meta['deps'] = getCodeDeps(meta['codes'], meta['id'])
    return meta


def getCodeDeps(codes, current='00', use_deep=False):
    if not hasattr(getCodeDeps, 'history'):
        getCodeDeps.history = {}

    words = list(
        set(
            [
                word
                for code in codes
                for word in re.split('[^\w]', code)
                if word and len(word) > 0
            ]
        )
    )
    depend_dict = {
        'stroke': '04',
        'circleSDF': '08',
        'fill': '09',
        'rectSDF': '10',
        'crossSDF': '11',
        'flip': '12',
        'vesicaSDF': '14',
        'triSDF': '15',
        'rhombSDF': '17',
        'rotate': '19',
        'polySDF': '26',
        'hexSDF': '27',
        'starSDF': '28',
        'raysSDF': '30',
        'heartSDF': '34',
        'bridge': '35',
        'scale': '44',
        'ratio': '44',
        'flowerSDF': '46',
        'spiralSDF': '47',
    }
    deps = []

    for word in words:
        if word in depend_dict and depend_dict[word] != current:
            deps.append(depend_dict[word])

    if use_deep:
        expand_deps = [d for d1 in deps for d in getCodeDeps.history[d1]]
        deps = list(set(deps + expand_deps))

    getCodeDeps.history[current] = deps

    deps.sort()
    return deps


def isKeyWord(word):
    if not hasattr(isKeyWord, 'keywords'):
        keyword_source = (
            'sampler1D sampler2D sampler3D samplerCube '
            + 'sampler1DShadow sampler2DShadow '
            + 'const attribute uniform varying '
            + 'break continue discard return '
            + 'for while do if else struct '
            + 'in out inout '
        )

        keyword_source += (
            'float int bool void '
            + 'vec2 vec3 vec4 ivec2 ivec3 ivec4 bvec2 bvec3 bvec4 '
            + 'mat2 mat3 mat4 '
        )

        keyword_source += 'for while do if else struct '

        keyword_source += (
            'radians degrees sin cos tan asin acos atan '
            + 'pow exp log exp2 sqrt inversesqrt '
            + 'abs sign floor ceil fract mod min max clamp mix step smoothstep '
            + 'length distance dot cross normalize ftransform faceforward '
            + 'reflect refract matrixCompMult '
            + 'lessThan lessThanEqual greaterThan greaterThanEqual '
            + 'equal notEqual any all not '
            + 'texture1D texture1DProj texture1DLod texture1DProjLod '
            + 'texture2D texture2DProj texture2DLod texture2DProjLod '
            + 'texture3D texture3DProj texture3DLod texture3DProjLod '
            + 'textureCube textureCubeLod '
            + 'shadow1D shadow2D shadow1DProj shadow2DProj '
            + 'shadow1DLod shadow2DLod shadow1DProjLod shadow2DProjLod '
            + 'dFdx dFdy fwidth '
            + 'noise1 noise2 noise3 noise4 '
        )

        keyword_source += (
            'true false '
            + 'gl_FragColor gl_SecondaryColor gl_Normal gl_Vertex '
            + 'gl_MultiTexCoord0 gl_MultiTexCoord1 gl_MultiTexCoord2 gl_MultiTexCoord3 '
            + 'gl_MultiTexCoord4 gl_MultiTexCoord5 gl_MultiTexCoord6 gl_MultiTexCoord7 '
            + 'gl_FogCoord gl_PointCoord '
            + 'gl_Position gl_PointSize gl_ClipVertex '
            + 'gl_FrontColor gl_BackColor gl_FrontSecondaryColor gl_BackSecondaryColor '
            + 'gl_TexCoord gl_FogFragCoord '
            + 'gl_FragCoord gl_FrontFacing '
            + 'gl_FragData gl_FragDepth '
            + 'gl_ModelViewMatrix gl_ProjectionMatrix gl_ModelViewProjectionMatrix '
            + 'gl_TextureMatrix gl_NormalMatrix gl_ModelViewMatrixInverse '
            + 'gl_ProjectionMatrixInverse gl_ModelViewProjectionMatrixInverse '
            + 'gl_TexureMatrixTranspose gl_ModelViewMatrixInverseTranspose '
            + 'gl_ProjectionMatrixInverseTranspose '
            + 'gl_ModelViewProjectionMatrixInverseTranspose '
            + 'gl_TextureMatrixInverseTranspose '
            + 'gl_NormalScale gl_DepthRange gl_ClipPlane '
            + 'gl_Point gl_FrontMaterial gl_BackMaterial gl_LightSource gl_LightModel '
            + 'gl_FrontLightModelProduct gl_BackLightModelProduct '
            + 'gl_TextureColor gl_EyePlaneS gl_EyePlaneT gl_EyePlaneR gl_EyePlaneQ '
            + 'gl_FogParameters '
            + 'gl_MaxLights gl_MaxClipPlanes gl_MaxTextureUnits gl_MaxTextureCoords '
            + 'gl_MaxVertexAttribs gl_MaxVertexUniformComponents gl_MaxVaryingFloats '
            + 'gl_MaxVertexTextureImageUnits gl_MaxTextureImageUnits '
            + 'gl_MaxFragmentUniformComponents gl_MaxCombineTextureImageUnits '
            + 'gl_MaxDrawBuffers '
        )
        isKeyWord.keywords = set(keyword_source.split())

    return word in isKeyWord.keywords
