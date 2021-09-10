#version 120

attribute vec2 vPosition;
attribute vec2 vTexcoords;

void main()
{
    gl_Position = vec4(vPosition.x, vPosition.y, 0.0, 0.0);
}