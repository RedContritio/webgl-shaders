import sys
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

# define shader code
vertex_code='''
uniform float scale;
attribute vec2 position;
attribute vec4 color;
varying vec4 v_color;
attribute vec2 TexCoordIn; 
varying vec2 TexCoordOut;

void main()
{

    gl_Position = vec4(position*scale, 0.0, 1.0);
    v_color = color;
    TexCoordOut = TexCoordIn;

}'''

fragment_code='''
varying vec4 v_color;
varying vec2 TexCoordOut; 
uniform sampler2D Texture; 
uniform vec2 originPosition;
uniform vec2 targetPosition;
vec2 curveWarp(vec2 textureCoord, vec2 originPosition, vec2 targetPosition, float radius)
{
    vec2 offset = vec2(0.0);
    vec2 result = vec2(0.0);

    vec2 direction = targetPosition - originPosition;

    float infect = distance(textureCoord, originPosition)/radius;

    infect = 1.0 - infect;
    infect = clamp(infect, 0.0, 1.0);
    offset = direction * infect;

    result = textureCoord - offset;
    return result;
}

void main()
{
    vec2 coordinate = vec2(0.0);
    float radius = 0.5;
    coordinate = curveWarp(TexCoordOut,originPosition,targetPosition,radius);
    gl_FragColor = v_color*0.000000000001 + texture2D(Texture, coordinate);

}'''

#define vertex and color array
data = np.zeros(4, dtype = [ ("position", np.float32, 2), ("color", np.float32, 4),("textureCoord",np.float32,2)] )
data['color']    = [ (1,1,0,1), (1,1,0,1), (1,1,0,1), (1,1,0,1) ]
data['position'] = [ (-1,-1),   (-1,+1),   (+1,-1),   (+1,+1)  ]
data['textureCoord']= [ (0,0),   (0,1),   (1,0),   (1,1) ]

#define debug function
def showTextureInGLTexture2D():
    im = glGetTexImage( GL_TEXTURE_2D, 0, GL_RGBA,  GL_UNSIGNED_BYTE )
    image=Image.frombuffer("RGBA",(512,512),im, 'raw', 'RGBA', 0, 1)
    image.show()

#define useful function
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    glutSwapBuffers()

def reshape(width,height):
    glViewport(0, 0, width, height)



#step1 init the context
def  init(img_path):
    image = Image.open(img_path)
    image = image.resize((image.size[0] * 4, image.size[1] * 4))
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutCreateWindow('Hello world!')
    glutReshapeWindow(image.width,image.height)
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    return image

#step 2 
def initShaderProgram():
    program  = glCreateProgram()
    vertex   = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)

    # Set shaders source
    glShaderSource(vertex, vertex_code)
    glShaderSource(fragment, fragment_code)

    # Compile shaders
    glCompileShader(vertex)
    glCompileShader(fragment)

    fragSuccess=glGetShaderiv(fragment, GL_COMPILE_STATUS)
    vertSuccess=glGetShaderiv(vertex, GL_COMPILE_STATUS)
    print("vertext shader compile  success  [%s]" %(vertSuccess,))
    print( "fragment shader compile  success  [%s]" %(fragSuccess,))

    if vertSuccess==0:
        print (glGetShaderInfoLog(vertex))
        sys.exit(0)

    if fragSuccess==0:
        print (glGetShaderInfoLog(fragment))
        sys.exit(0)


    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
    glLinkProgram(program)
    linksucc=glGetProgramiv(program,GL_LINK_STATUS);
    print( "link  program success [%s]" %(linksucc,))
    glUseProgram(program)

    return program

#step 3.1 optional setup texture 
def getTextureFromFile(image_file):
    #convert file to bytes
    image = image_file.transpose(Image.FLIP_TOP_BOTTOM)
    image = image.convert("RGBA")
    byteImage =np.array(list(image.getdata()), np.uint8)

    #setup texture 
    texIndex=glGenTextures(1)
    glEnable( GL_TEXTURE_2D )
    glBindTexture(GL_TEXTURE_2D,texIndex)  

    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
     #make the texture the default
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texIndex, 0)
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image.width,image.height,0,GL_RGBA,GL_UNSIGNED_BYTE,byteImage)

    return texIndex




#step 4.1 optional get the image from BufferFrame 
def saveImageFromFBO(image):
    glReadBuffer(GL_COLOR_ATTACHMENT0)
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels (0, 0, image.width, image.height, GL_RGB,  GL_UNSIGNED_BYTE)
    image = Image.new ("RGB", (image.width, image.height), (0, 0, 0))
    image.frombytes (data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save ('9_result.jpg')


#step 4 optional if need to OSR generate a BufferFrame
def setupSelfDefineFBO(program,image):

    # Setup framebuffer
    framebuffer = glGenFramebuffers (1)
    glBindFramebuffer(GL_FRAMEBUFFER, framebuffer)

    # Setup depthbuffer
    # depthbuffer = glGenRenderbuffers (1)
    # glBindRenderbuffer (GL_RENDERBUFFER,depthbuffer)
    # glRenderbufferStorage (GL_RENDERBUFFER, GL_DEPTH_COMPONENT, image.width, image.height)
    # glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depthbuffer)

    #first init VBO, then other parameters
    buffer = glGenBuffers(1)     # Request a buffer slot from GPU
    glBindBuffer(GL_ARRAY_BUFFER, buffer)     # Make this buffer the default one
    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)    # Upload data    

    # Create texture to render to
    # glBufferData(GL_FRAMEBUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)
    loc = glGetAttribLocation(program, "position")   #get the index of  the attribute in program
    glEnableVertexAttribArray(loc)  #allow this attribute decide by index can be use 
    stride = data.strides[0]   #define how to read buffer
    offset = ctypes.c_void_p(0) #define the offset where the data begin in buffer
    glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)
    offset = ctypes.c_void_p(data.dtype["position"].itemsize)
    loc = glGetAttribLocation(program, "color")
    glEnableVertexAttribArray(loc)
    glVertexAttribPointer(loc, 4, GL_FLOAT, False, stride, offset)

    #setup other parameters
    loc = glGetUniformLocation(program, "scale")
    glUniform1f(loc, 1.0)


    originPosition = glGetUniformLocation(program, "originPosition")
    glUniform2f(originPosition, 0.5, 0.5 )

    targetPosition = glGetUniformLocation(program, "targetPosition")
    glUniform2f(targetPosition, 0.47, 0.47 )

    # following code to bind uniform texture if needed
    aTexture=getTextureFromFile(image)

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D,aTexture)
    loc=glGetUniformLocation(program,"Texture")
    textureId=glGetIntegerv(GL_TEXTURE_BINDING_2D)  #find out the id of the current texture bind to GL_TEXTURE_2D
    glUniform1i(loc,textureId)    

    loc= glGetAttribLocation(program, "TexCoordIn")
    glEnableVertexAttribArray(loc)
    offset=ctypes.c_void_p(data.dtype["color"].itemsize+8)
    glVertexAttribPointer(loc,2,GL_FLOAT,False,stride,offset)

    status = glCheckFramebufferStatus (GL_FRAMEBUFFER)
    if status != GL_FRAMEBUFFER_COMPLETE:
        print( "Error in framebuffer activation")

    saveImageFromFBO(image)


    glBindFramebuffer(GL_FRAMEBUFFER, GL_NONE)
    glDeleteTextures ([aTexture])
    glDeleteFramebuffers (1,[framebuffer])

    print( 'save image from FBO success')

def keyboard( keycode, x, y ):
    # print(keycode)
    # if (keycode == 'b'+'q'):
    #     sys.exit()
    # elif (keycode == 'b'+' '):
    saveImageFromFBO(image)



if (__name__ == '__main__'):
   image = init('tarot-merge.png')
   program = initShaderProgram()
   setupSelfDefineFBO(program,image)