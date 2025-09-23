########Task2########
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

B_width, B_height = 500, 500
point_size = 5
speed = 1.0
points = []
direction = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
directions = []
colors = []
frozen = False
blinking = False
blink_counting = 0  
duration = 30  
def convert_coordinate(x, y):
    global B_width, B_height
    a = x - (B_width / 2)
    b = (B_height / 2) - y
    return a, b

def movements():
    global points, directions, blinking, frozen, speed, blink_counting
    any_bounce = False
    updated_points = []
    if frozen==True :
        if not blinking or (blink_counting // duration) % 2 == 0:
            glPointSize(point_size)
            glBegin(GL_POINTS)
            for i in range(len(points)):
                r, g, b = colors[i]
                glColor3f(r, g, b)
                x, y = points[i]
                glVertex2f(x, y)
            glEnd()
        return

    for i in range(len(points)):
        x, y = points[i]
        dx, dy = directions[i]

        x += dx * speed
        y += dy * speed

                             
        if x >= B_width / 2: # Bounce X 
            x = B_width / 2
            dx = -abs(dx)
            any_bounce = True
        elif x <= -B_width / 2:
            x = -B_width / 2
            dx = abs(dx)
            any_bounce = True


        if y >= B_height / 2:         # Bounce  Y 
            y = B_height / 2
            dy = -abs(dy)
            any_bounce = True
        elif y <= -B_height / 2:
            y = -B_height / 2
            dy = abs(dy)
            any_bounce = True

        updated_points.append((x, y))
        directions[i] = (dx, dy)

    points[:] = updated_points
    blink_counting += 1  

    if not blinking or (blink_counting // duration) % 2 == 0:
        glPointSize(point_size)
        glBegin(GL_POINTS)
        for i in range(len(points)):
            r, g, b = colors[i]
            glColor3f(r, g, b)
            x, y = points[i]
            glVertex2f(x, y)
        glEnd()

def keyboardListener(key, x, y):
    global frozen
    if key == b' ':
        if not frozen:
            frozen = True
        else:
            frozen = False
    else:
        frozen = True
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global speed
    if key == GLUT_KEY_UP:
        speed *= 1.5
    elif key == GLUT_KEY_DOWN:
        speed = max(0.1, speed / 1.5)
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global points, colors, blinking, frozen, directions, direction, speed
    if frozen==False:
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            point_x, point_y = convert_coordinate(x, y)
            if -B_width / 2 < point_x < B_width / 2 and -B_height / 2 < point_y < B_height / 2:
                dir_x, dir_y = random.choice(direction)
                directions.append((dir_x * speed, dir_y * speed))
                colors.append((random.random(), random.random(), random.random()))
                points.append((point_x, point_y))
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        frozen = False
        blinking = not blinking
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    movements()
    glutSwapBuffers()

def animate():
    if frozen==False:
        glutPostRedisplay()

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

glutInit()
glutInitWindowSize(B_width, B_height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Amazing Box")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()

