from OpenGL.GL import *
from OpenGL.GLUT import*
from OpenGL.GLU import *

import time
import random

W_Width, W_Height = 500, 500
play = True
pause = False
game_over = False
speed = 70
score = 0
End_Time = time.time()
catcher_bowl_info = None
diamond_position_x = None
diamond_y = 445
diamond_color = (random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0))

def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y
    return a, b

def draw_points(x, y, color):
    glColor3f(*color)
    glPointSize(1)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def zone_detection(starting_point, ending_point):
    x1, y1 = starting_point
    x2, y2 = ending_point

    dx = x2 - x1
    dy = y2 - y1

    if dx >= 0 and dy >= 0:
        if abs(dx) > abs(dy):
            zone = 0
        else:
            zone = 1
    elif dx < 0 and dy >= 0:
        if abs(dx) < abs(dy):
            zone = 2
        else:
            zone = 3
    elif dx < 0 and dy < 0:
        if abs(dx) > abs(dy):
            zone = 4
        else:
            zone = 5
    elif dx >= 0 and dy < 0:
        if abs(dx) < abs(dy):
            zone = 6
        else:
            zone = 7
    return zone

def detect_zone_to_zone0(point, zone):
    x_prime = point[0]
    y_prime = point[1]
    if zone == 0:
        return x_prime, y_prime
    elif zone == 1:
        return y_prime, x_prime
    elif zone == 2:
        return y_prime, -x_prime
    elif zone == 3:
        return -x_prime, y_prime
    elif zone == 4:
        return -x_prime, -y_prime
    elif zone == 5:
        return -y_prime, -x_prime
    elif zone == 6:
        return -y_prime, x_prime
    elif zone == 7:
        return x_prime, -y_prime

def midpoint_line_algo(starting_point, ending_point, zone, color):
    x1, y1 = starting_point
    x2, y2 = ending_point

    dx = x2 - x1
    dy = y2 - y1
    
    a = 2 * dy
    b = -2 * dx
    d_in = a + 0.5 * b
    d_NE = a + b
    d_E = a

    while x1 <= x2:
        x, y = zone0_to_actual_zone(x1, y1, zone)
        draw_points(x, y, color)
        if d_in > 0:
            y1 += 1
            d_in += d_NE
        else:
            d_in += d_E
        x1 += 1

def zone0_to_actual_zone(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def draw_cross():
    zone = zone_detection((450, 450), (490, 490))
    x1, y1 = detect_zone_to_zone0((450, 450), zone)
    x2, y2 = detect_zone_to_zone0((490, 490), zone)
    midpoint_line_algo((x1, y1), (x2, y2), zone, (1, 0, 0))

    zone = zone_detection((450, 490), (490, 450))
    x1, y1 = detect_zone_to_zone0((450, 490), zone)
    x2, y2 = detect_zone_to_zone0((490, 450), zone)
    midpoint_line_algo((x1, y1), (x2, y2), zone, (1, 0, 0))

def draw_arrow():
    zone = zone_detection((10, 470), (50, 470))
    x1, y1 = detect_zone_to_zone0((10, 470), zone)
    x2, y2 = detect_zone_to_zone0((50, 470), zone)
    midpoint_line_algo((x1, y1), (x2, y2), zone, (0, 0.5, 0.5))

    zone = zone_detection((10, 470), (30, 490))
    x1, y1 = detect_zone_to_zone0((10, 470), zone)
    x2, y2 = detect_zone_to_zone0((30, 490), zone)
    midpoint_line_algo((x1, y1), (x2, y2), zone, (0, 0.5, 0.5))

    zone = zone_detection((10, 470), (30, 450))
    x1, y1 = detect_zone_to_zone0((10, 470), zone)
    x2, y2 = detect_zone_to_zone0((30, 450), zone)
    midpoint_line_algo((x1, y1), (x2, y2), zone, (0, 0.5, 0.5))

def draw_PlayOrPause():
    global play, pause
    if play:
        zone = zone_detection((230, 450), (230, 490))
        x1, y1 = detect_zone_to_zone0((230, 450), zone)
        x2, y2 = detect_zone_to_zone0((230, 490), zone)
        midpoint_line_algo((x1, y1), (x2, y2), zone, (1, 1, 0))

        zone = zone_detection((250, 450), (250, 490))
        x1, y1 = detect_zone_to_zone0((250, 450), zone)
        x2, y2 = detect_zone_to_zone0((250, 490), zone)
        midpoint_line_algo((x1, y1), (x2, y2), zone, (1, 1, 0))
    else:
        zone = zone_detection((225, 450), (225, 490))
        x1, y1 = detect_zone_to_zone0((225, 450), zone)
        x2, y2 = detect_zone_to_zone0((225, 490), zone)
        midpoint_line_algo((x1, y1), (x2, y2), zone, (1, 1, 0))

        zone = zone_detection((225, 450), (255, 470))
        x1, y1 = detect_zone_to_zone0((225, 450), zone)
        x2, y2 = detect_zone_to_zone0((255, 470), zone)
        midpoint_line_algo((x1, y1), (x2, y2), zone, (1, 1, 0))

        zone = zone_detection((225, 490), (255, 470))
        x1, y1 = detect_zone_to_zone0((225, 490), zone)
        x2, y2 = detect_zone_to_zone0((255, 470), zone)
        midpoint_line_algo((x1, y1), (x2, y2), zone, (1, 1, 0))

def draw_catcher_bowl(a, b, c, d):
    catcher_info = {
        "line1": (a, b),
        "line2": (b, c),
        "line3": (c, d),
        "line4": (d, a)}
    if game_over:
        color = (1, 0, 0)
    else:
        color = (1, 1, 1)
    for key in catcher_info:
        zone = zone_detection(catcher_info[key][0], catcher_info[key][1])
        x1, y1 = detect_zone_to_zone0(catcher_info[key][0], zone)
        x2, y2 = detect_zone_to_zone0(catcher_info[key][1], zone)
        midpoint_line_algo((x1, y1), (x2, y2), zone, color)
    return catcher_info

def draw_diamond(diamond_position_x, diamond_y):
    global diamond_color
    lst = [
        (diamond_position_x, diamond_y),
        (diamond_position_x + 15, diamond_y - 20),
        (diamond_position_x, diamond_y),
        (diamond_position_x - 15, diamond_y - 20),
        (diamond_position_x + 15, diamond_y - 20),
        (diamond_position_x, diamond_y - 40),
        (diamond_position_x - 15, diamond_y - 20),
        (diamond_position_x, diamond_y - 40)
    ]
    for i in range(0, len(lst), 2):
        zone = zone_detection(lst[i], lst[i + 1])
        x1, y1 = detect_zone_to_zone0(lst[i], zone)
        x2, y2 = detect_zone_to_zone0(lst[i + 1], zone)
        midpoint_line_algo((x1, y1), (x2, y2), zone, diamond_color)

def hasCollided(box_1, box_2):
    return (box_1['x'] < box_2['x'] + box_2['width'] and
            box_1['x'] + box_1['width'] > box_2['x'] and
            box_1['y'] < box_2['y'] + box_2['height'] and
            box_1['y'] + box_1['height'] > box_2['y'])

def animate():
    global game_over, play, pause, speed, score, catcher_bowl_info, diamond_position_x, diamond_y, End_Time, diamond_color
    if not game_over and play and not pause:
        Current_Time = time.time()
        deltaTime = min(Current_Time - End_Time, 0.1)  
        End_Time = Current_Time
        diamond_y -= speed * deltaTime

        diamond_box_bounds = {
            "x": diamond_position_x - 15,
            "y": diamond_y - 40,
            "width": 30,
            "height": 40}

        catcher_bowl_bounds = {
            "x": catcher_bowl_info["line1"][0][0],
            "y": catcher_bowl_info["line1"][0][1],
            "width": 140,
            "height": 30}

        if hasCollided(diamond_box_bounds, catcher_bowl_bounds):
            score += 1
            print("Score:", score)
            diamond_position_x = random.randint(25, 475)
            diamond_y = 445
            diamond_color = (random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0))
            speed += 10 

        elif diamond_y - 40 < 0:
            print("Game Over! Final Score:", score)
            game_over = True

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global play, pause, game_over, catcher_bowl_info
    if key == GLUT_KEY_RIGHT:
        if not game_over and play and not pause:
            if catcher_bowl_info["line2"][1][0] + 10 <= 500:
                for key_name in catcher_bowl_info:
                    catcher_bowl_info[key_name] = (
                        (catcher_bowl_info[key_name][0][0] + 10, catcher_bowl_info[key_name][0][1]),
                        (catcher_bowl_info[key_name][1][0] + 10, catcher_bowl_info[key_name][1][1])
                    )
    elif key == GLUT_KEY_LEFT:
        if not game_over and play and not pause:
            if catcher_bowl_info["line4"][0][0] - 10 >= 0:  
                for key_name in catcher_bowl_info:
                    catcher_bowl_info[key_name] = (
                        (catcher_bowl_info[key_name][0][0] - 10, catcher_bowl_info[key_name][0][1]),
                        (catcher_bowl_info[key_name][1][0] - 10, catcher_bowl_info[key_name][1][1])
                    )
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global play, pause, game_over, speed, score, diamond_position_x, diamond_y, catcher_bowl_info, diamond_color
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        conv_x = x
        conv_y = W_Height - y
        if 10 <= conv_x <= 50 and 450 <= conv_y <= 490:
            print("Starting Over!")
            score = 0
            speed = 70
            diamond_position_x = random.randint(25, 475)
            diamond_y = 445
            diamond_color = (random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0))
            catcher_bowl_info = draw_catcher_bowl((200, 10), (280, 10), (310, 40), (170, 40))
            play = True
            pause = False
            game_over = False
            End_Time = time.time()  
            #print("Game Restarted")
        elif 230 <= conv_x <= 250 and 450 <= conv_y <= 490 and play:
            pause = True
            play = False
            #print("Game Paused")
        elif 225 <= conv_x <= 255 and 450 <= conv_y <= 490 and pause:
            play = True
            pause = False
            End_Time = time.time()  
            #print("Game Resumed")
        elif 450 <= conv_x <= 490 and 450 <= conv_y <= 490:
            print(f"Goodbye! Final Score: {score}")
            game_over = True
            glutLeaveMainLoop()
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, W_Width, W_Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W_Width, 0, W_Height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_catcher_bowl(
        catcher_bowl_info["line1"][0],
        catcher_bowl_info["line1"][1],
        catcher_bowl_info["line3"][0],
        catcher_bowl_info["line3"][1],
    )
    draw_diamond(diamond_position_x, diamond_y)
    draw_arrow()
    draw_cross()
    draw_PlayOrPause()
    glutSwapBuffers()

def init():
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    global catcher_bowl_info, diamond_position_x
    catcher_bowl_info = draw_catcher_bowl((200, 10), (280, 10), (310, 40), (170, 40))
    diamond_position_x = random.randint(25, 475)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Midpoint Line Algorithm with OpenGL")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()