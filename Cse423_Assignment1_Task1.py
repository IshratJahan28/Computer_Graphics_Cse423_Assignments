#####task1########
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

D_Width, D_Height = 700,700
raindrops = []
rain_angle = 0.0
brightness = 0.0


def drawHouse():
    glBegin(GL_TRIANGLES)
    glColor3f(1,1, 0.5)
    glVertex2d(0,200)
    glVertex2d(-100,100)
    glVertex2d(100,100)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.2, 0.5, 0.3)
    glVertex2d(-100, 100)
    glVertex2d(100, 100)
    glVertex2d(100, 0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2d(100, 0)
    glVertex2d(-100, 0)
    glVertex2d(-100, 100)
    glEnd()

def drawing_window():
    glColor3f(0.6, 0.8, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(-80, 40)
    glVertex2f(-20, 40)
    glVertex2f(-20, 80)

    glVertex2f(-80, 40)
    glVertex2f(-20, 80)
    glVertex2f(-80, 80)
    glEnd()

def drawing_door():
    glColor3f(0.1, 0.1, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(40, 0)
    glVertex2f(80, 0)
    glVertex2f(80, 60)
    glVertex2f(40, 0)
    glVertex2f(80, 60)
    glVertex2f(40, 60)
    glEnd()

def drawRaindrops():
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0)
    global raindrops,rain_angle
    for raindrop_x, raindrop_y in raindrops:
        glVertex2f(raindrop_x,raindrop_y)
        glVertex2f(raindrop_x+rain_angle,raindrop_y-10)

    glEnd()

def animate():
    global raindrops, rain_angle
    for i in range(len(raindrops)):
        x, y = raindrops[i]
        x += rain_angle
        y -= 10

        if x < -D_Width/2:
            x += D_Width
        elif x > D_Width/2:
            x -= D_Width

        if y < -D_Height/2:
            x = random.uniform(-D_Width/2, D_Width/2)
            y = D_Height/2

        raindrops[i] = (x, y)
    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global rain_angle
    if key==GLUT_KEY_LEFT  :
        rain_angle -= 0.5
    if key== GLUT_KEY_RIGHT:		#// up arrow key
        rain_angle += 0.5
    glutPostRedisplay()


def keyboardListener(key, x, y):

    global brightness
    if key==b'w':
        brightness=min(1.0,brightness+0.1)
    elif key==b's':
        brightness=max(0.0,brightness-0.1)

    glutPostRedisplay()


def display():
    #//clear the display
    global brightness
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,1)
    glLoadIdentity()
    glBegin(GL_TRIANGLES) ##top er jnnw
    glColor3f(brightness, brightness, brightness)
    glVertex2f(-D_Width / 2, 100)
    glVertex2f(D_Width / 2, 100)
    glVertex2f(D_Width / 2, D_Height / 2)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(brightness, brightness, brightness)
    glVertex2f(-D_Width / 2, 100)
    glVertex2f(D_Width / 2, D_Height / 2)
    glVertex2f(-D_Width / 2, D_Height / 2)
    glEnd()

    glBegin(GL_TRIANGLES) ##bottom er jnnw
    glColor3f(0.3, 0.2, 0.0)
    glVertex2f(-D_Width / 2, -D_Height / 2)
    glVertex2f(D_Width / 2, -D_Height / 2)
    glVertex2f(D_Width / 2, 100)
    glEnd()

    glBegin(GL_TRIANGLES)
    #glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-D_Width / 2, -D_Height / 2)
    glVertex2f(D_Width / 2, 100)
    glVertex2f(-D_Width / 2,100)
    glEnd()
    
    drawHouse()
    drawing_window()
    drawing_door()
    drawRaindrops()
    glutSwapBuffers()

def init():
    #//clear the screen
    global raindrops
    glClearColor(0,0,0,0)
    #//load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    #//initialize the matrix
    glLoadIdentity()
    gluOrtho2D(-D_Width / 2, D_Width / 2, -D_Height / 2, D_Height / 2)  # Center origin
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    for i in range(200):
        x = random.randint(0, D_Width)
        y = random.randint(0, D_Height)
        raindrops.append((x, y))

glutInit()
glutInitWindowSize(D_Width, D_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color

# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"OpenGL rain fall simulation") # Create a window with a title
init()

glutDisplayFunc(display)	#display callback function
glutIdleFunc(animate)	#what you want to do in the idle time (when no drawing is occuring)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)

glutMainLoop()		#The main loop of OpenGL