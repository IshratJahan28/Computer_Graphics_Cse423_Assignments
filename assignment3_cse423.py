from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

camera_pos = (0,500,500)

fovY = 120  
GRID_LENGTH = 100  
rand_var = 423
GRID_SIZE=15

Player_Position = [0, 0, 0]
Player_Angle = 0
Game_Over = False
cam_mode = "third"  

Bullet=[]

num_of_enemies=5
enemies=[]

life = 5
missed_bullets = 0
score = 0
left_bound = -GRID_SIZE * GRID_LENGTH // 2
right_bound = GRID_SIZE * GRID_LENGTH // 2

cheat = False
gun = False
can_fire = True
cheat_move_angle = 0
cheat_camera_view = [-90, 0, 60]
cheat_rotation = 0

cheatCamOffset=[0,0,0]

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_grid(GRID_LENGTH,GRID_SIZE):
    half_size =  GRID_SIZE// 2
    glBegin(GL_QUADS)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            CHECK_POS=(i+j)%2
            if CHECK_POS==0:
                glColor3f(1,1,1)
            else:
                glColor3f(0.7, 0.5, 0.95)
            bottom_left_x= (i-half_size)*GRID_LENGTH
            bottom_left_y= (j-half_size)*GRID_LENGTH
            glVertex3f(bottom_left_x, bottom_left_y, 0) 
            glVertex3f(bottom_left_x + GRID_LENGTH, bottom_left_y, 0) 
            glVertex3f(bottom_left_x + GRID_LENGTH, bottom_left_y + GRID_LENGTH, 0) 
            glVertex3f(bottom_left_x, bottom_left_y + GRID_LENGTH, 0) 
    glEnd()
    
def draw_walls():
    HalfSize = (GRID_LENGTH * GRID_SIZE) // 2
    Wall_Height = 110
    Wall_Colors = [(0.012,1.0,0.996),(0.0,0.0,1.0),(1.0,1.0,1.0),(0.0, 1.0, 0.0)]
    Wall_Edges = [[(-HalfSize,-HalfSize),(HalfSize,-HalfSize)],[(HalfSize,-HalfSize),(HalfSize,HalfSize)],[(HalfSize,HalfSize),(-HalfSize,HalfSize)],[(-HalfSize,HalfSize),(-HalfSize,-HalfSize)]]
    for i in range(len(Wall_Edges)):
        x1, y1 = Wall_Edges[i][0]
        x2, y2 = Wall_Edges[i][1]
        glBegin(GL_QUADS)
        glColor3f(* Wall_Colors[i])
        glVertex3f(x1, y1, 0)
        glVertex3f(x2, y2, 0)
        glVertex3f(x2, y2,  Wall_Height)
        glVertex3f(x1, y1,  Wall_Height)
        glEnd()

def draw_player():
    glPushMatrix()
    px, py, pz = Player_Position
    glTranslatef(px, py, pz)
    glRotatef(Player_Angle, 0, 0, 1)
    if Game_Over:
        glRotatef(90, 0, 1, 0)
    glTranslatef(0,0,170)
    # Left foot
    glColor3f(0, 0, 1)
    glTranslatef(0,-20,-100)
    glRotatef(90, 0, 1, 0)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 16, 8, 100, 10, 10)

    # Right foot
    glTranslatef(0,-80,0)
    gluCylinder(gluNewQuadric(), 16, 8, 100, 10, 10)

    # Body
    glColor3f(0.095, 0.350, 0.095)
    glTranslatef(0, 40, -30)
    glutSolidCube(80)

    # Gun
    glColor3f(0.6, 0.6, 0.6)
    glTranslatef(0, 0, 40)
    glTranslatef(30, 0, -90) 
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 20, 5, 120, 10, 10)

    # Left Hand
    glColor3f(1.0, 0.88, 0.65)
    glTranslatef(0, -25, 0)
    gluCylinder(gluNewQuadric(), 15, 6, 60, 10, 10)

    # Right Hand
    glTranslatef(0, 50, 0)
    gluCylinder(gluNewQuadric(), 15, 6, 60, 10, 10)

    # Head
    glColor3f(0, 0, 0)
    glTranslatef(40,-25, -25)
    gluSphere(gluNewQuadric(), 30, 10, 10)
    glPopMatrix()


def draw_enemy(enemy):
    glPushMatrix()
    pos_x, pos_y, pos_z = enemy["enemy_position"]
    glTranslatef(pos_x, pos_y, pos_z)
    size = enemy["scale"]
    glScalef(size, size, size)
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, 40)
    gluSphere(gluNewQuadric(), 40, 20, 20)
    glPopMatrix()
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, 80)
    gluSphere(gluNewQuadric(), 30, 20, 20)
    glPopMatrix()
    glPopMatrix()

def spawn_enemy():
    while True:
        x = random.randint(-650, 550)
        y = random.randint(-650, 550)
        if abs(x) > 200 or abs(y) > 200:
            break
    return {'enemy_position': [x, y, 0],
            'scale': 1.0,
            'scale_dir': 0.005,
            'collide': False}

for i in range(num_of_enemies):
    enemies.append(spawn_enemy())   

def draw_bullets():
    if not Bullet:
        return
    glColor3f(1, 0, 0)
    for b in Bullet:
        pos = b.get('bullet_pos') or b.get('BulletPosition') or b.get('bulletPosition')
        if not pos: 
            continue
        x, y, z = pos
        glPushMatrix()
        glTranslatef(x, y, z)
        glutSolidCube(10)
        glPopMatrix()

def activate_cheat_mode():
    global Player_Position, Player_Angle, enemies, cheat_rotation, can_fire, score, Bullet, missed_bullets

    if not cheat or Game_Over:
        return

    rotation_speed = 1.5

    # ALWAYS rotate the player
    Player_Angle = (Player_Angle + rotation_speed) % 360

    
    if not gun:
        cheat_rotation += rotation_speed
        if cheat_rotation >= 30:
            cheat_rotation = 0
            can_fire = True

    
    rad = math.radians(Player_Angle)
    gun_length = 140
    gun_offset_right = 50
    gun_offset_up = 10
    gun_tip = [
        Player_Position[0] + gun_offset_right * math.sin(rad) - math.cos(rad) * gun_length,
        Player_Position[1] - gun_offset_right * math.cos(rad) - math.sin(rad) * gun_length,
        Player_Position[2] + gun_offset_up
    ]

    if can_fire:
        for enemy in enemies:
            ex, ey, ez = enemy["enemy_position"]
            dx, dy = ex - gun_tip[0], ey - gun_tip[1]
            dist_xy = math.sqrt(dx**2 + dy**2)
            if dist_xy == 0:
                continue
            dir_x = -math.cos(rad)
            dir_y = -math.sin(rad)
            dot_product = (dx * dir_x + dy * dir_y) / dist_xy
            if dot_product > 0.998:
                dz = ez - gun_tip[2]
                total_dist = math.sqrt(dx**2 + dy**2 + dz**2)
                bullet_dir = [dx / total_dist, dy / total_dist, dz / total_dist]
                Bullet.append({
                    "bullet_pos": gun_tip.copy(),
                    "dir": bullet_dir,
                    "cheat": True
                })
                can_fire = False
                break

    glutPostRedisplay()


def restart_game():
    global Player_Position,Player_Angle, life, score, missed_bullets, Bullet, enemies, Game_Over, cheat, cam_mode
    Bullet.clear()
    enemies.clear()
    for _ in range(num_of_enemies):
        enemies.append(spawn_enemy())
    Player_Position[:] = [0, 0, 0]
    Player_Angle = 0
    life = 5
    score = 0
    missed_bullets = 0
    Game_Over = False
    cheat = False
    cam_mode = "third"
    print("Game has been restarted!")
    glutPostRedisplay()

def keyboard_listener(key, x, y):
    
    global Player_Position, Player_Angle, cam_mode, cheat_camera_view, life, missed_bullets, score, cheat, gun
    speed = 50 if cheat else 20
    angle_step = 5

    if not Game_Over:
        angle_rad = math.radians(Player_Angle)

        dx = dy = 0
        if key == b'w':
            dx, dy = -math.cos(angle_rad) * speed, -math.sin(angle_rad) * speed
        elif key == b's':
            dx, dy =  math.cos(angle_rad) * speed,  math.sin(angle_rad) * speed

        if dx != 0 or dy != 0:
            new_x = Player_Position[0] + dx
            new_y = Player_Position[1] + dy
            if left_bound <= new_x <= right_bound and left_bound <= new_y <= right_bound:
                Player_Position[0] = new_x
                Player_Position[1] = new_y
                if cam_mode == "first" and cheat and not gun:
                    cheat_camera_view[0] += dx
                    cheat_camera_view[1] += dy

        if key == b'a' and not cheat:
            Player_Angle = (Player_Angle + angle_step) % 360
        elif key == b'd' and not cheat:
            Player_Angle = (Player_Angle - angle_step) % 360

        if key == b'c':
            cheat = not cheat
            if cheat:
                activate_cheat_mode()
            else:
                gun = False

        if key == b'v':
            if cam_mode == "first" and cheat:
                gun = not gun
            elif not cheat:
                gun = False

    if key == b'r' and Game_Over:
        restart_game()
   
def specialKeyListener(key, x, y):
    
    global camera_pos
    cx, cy, cz = camera_pos
    if not Game_Over:
        if key == GLUT_KEY_UP:
            cz += 2
        if key == GLUT_KEY_DOWN:
            cz -= 2
        if key == GLUT_KEY_LEFT:
            cx -= 2
        if key == GLUT_KEY_RIGHT:
            cx += 2
    camera_pos = (cx, cy, cz)

def mouseListener(button, state, x, y):
    
    global cam_mode, Bullet, Player_Position, Player_Angle
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if not Game_Over:
            fire_bullet()
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not Game_Over:
        cam_mode = "first" if cam_mode == "third" else "third"
        print(f"Camera changed to {cam_mode}-person view")
        glutPostRedisplay()
        
def fire_bullet():
    global Bullet, Player_Position, Player_Angle, can_fire
    angle_rad = math.radians(Player_Angle)
    direction_x = -math.cos(angle_rad)
    direction_y = -math.sin(angle_rad)
    gun_forward = 170
    gun_side = 30
    gun_up = 120
    bullet_origin = [
        Player_Position[0] + gun_side * math.sin(angle_rad) + direction_x * gun_forward,
        Player_Position[1] - gun_side * math.cos(angle_rad) + direction_y * gun_forward,
        Player_Position[2] + gun_up
    ]
    Bullet.append({'BulletPosition': bullet_origin, 'direction': (direction_x, direction_y, 0)})
    print("Bullet has been fired!")

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if cam_mode == "third":
        x, y, z = camera_pos
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)

    elif cam_mode == "first" and cheat:
        if not gun:
            # Camera rotates with player
            angle_rad = math.radians(Player_Angle)
            base_cam = [
                Player_Position[0],
                Player_Position[1],
                Player_Position[2] + 150
            ]
            look_point = [
                base_cam[0] + math.cos(angle_rad) * 100,
                base_cam[1] - math.sin(angle_rad) * 100,
                base_cam[2]
            ]
        else:
            # Camera fixed, player rotates independently
            base_cam = [
                Player_Position[0],
                Player_Position[1],
                Player_Position[2] + 150
            ]
            
            look_point = [
                base_cam[0] + 1,
                base_cam[1],
                base_cam[2]
            ]

        gluLookAt(
            base_cam[0], base_cam[1], base_cam[2],
            look_point[0], look_point[1], look_point[2],
            0, 0, 1
        )

    elif cam_mode == "first" and not cheat:
        
        angle_rad = math.radians(Player_Angle)
        base_cam = [
            Player_Position[0] + 35 * math.sin(angle_rad) - math.cos(angle_rad) * 65,
            Player_Position[1] - 35 * math.cos(angle_rad) - math.sin(angle_rad) * 65,
            Player_Position[2] + 45
        ]
        look_point = [
            base_cam[0] - math.cos(angle_rad) * 95,
            base_cam[1] - math.sin(angle_rad) * 95,
            base_cam[2]
        ]
        gluLookAt(
            base_cam[0], base_cam[1], base_cam[2],
            look_point[0], look_point[1], look_point[2],
            0, 0, 1
        )




def move_enemies_towards_player():
    global missed_bullets, life, Game_Over
    for enemy in enemies:
        px, py = Player_Position[0], Player_Position[1]
        ex, ey = enemy['enemy_position'][0], enemy['enemy_position'][1]
        dx, dy = px - ex, py - ey
        distance = math.hypot(dx, dy)
        if distance > 1:
            enemy['enemy_position'][0] += (dx / distance) * 0.05
            enemy['enemy_position'][1] += (dy / distance) * 0.05
        enemy['scale'] += enemy['scale_dir']
        if not (0.8 <= enemy['scale'] <= 1.2):
            enemy['scale_dir'] *= -1

        if abs(Player_Position[0] - ex) < 100 and abs(Player_Position[1] - ey) < 100:
            if life > 0:
                life -= 1
                print(f"Lifes remaining: {life}")
                enemies.remove(enemy)
                enemies.append(spawn_enemy())
            else:
                Game_Over = True
                enemies.clear()
            break

def update_bullet_position():
    global missed_bullets, Game_Over, life

    for e in Bullet:
        pos_key = 'bullet_pos' if 'bullet_pos' in e else ('BulletPosition' if 'BulletPosition' in e else ('bulletPosition' if 'bulletPosition' in e else None))
        dir_key = 'dir' if 'dir' in e else ('direction' if 'direction' in e else None)
        if pos_key is None or dir_key is None:
            continue
        e[pos_key][0] += e[dir_key][0] * 10
        e[pos_key][1] += e[dir_key][1] * 10
        if len(e[dir_key]) >= 3:
            e[pos_key][2] += e[dir_key][2] * 10

    i = 0
    while i < len(Bullet):
        pos = Bullet[i].get('bullet_pos') or Bullet[i].get('BulletPosition') or Bullet[i].get('bulletPosition')
        if not pos:
            i += 1
            continue
        bx, by, bz = pos
        if abs(bx) > 600 or abs(by) > 600:
            missed_bullets += 1
            print(f"Missed bullets count: {missed_bullets}")
            Bullet.pop(i)
        else:
            i += 1

    if missed_bullets >= 10 or life <= 0:
        print("Game over!")
        Game_Over = True
        enemies.clear()

def check_enemy_hits():
    global Bullet, score, enemies

    updated_enemies = []
    bullets_to_remove = []

    HIT_RADIUS = 40.0 

    for enemy in enemies:
        enemy_hit = False
        ex, ey, ez = enemy['enemy_position']

        for x in Bullet:
            pos = x.get('bullet_pos') or x.get('BulletPosition') or x.get('bulletPosition')
            if not pos:
                continue
            bx, by, bz = pos

           
            if math.hypot(bx - ex, by - ey) <= HIT_RADIUS:
                enemy_hit = True
                score += 1
                bullets_to_remove.append(x)
                break

        if enemy_hit:
            updated_enemies.append(spawn_enemy())
        else:
            updated_enemies.append(enemy)

    for x in bullets_to_remove:
        if x in Bullet:
            Bullet.remove(x)

    enemies[:] = updated_enemies



def idle():
    update_bullet_position()
    check_enemy_hits()
    move_enemies_towards_player()
    activate_cheat_mode()
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
    draw_grid(GRID_LENGTH,GRID_SIZE)
    draw_walls()
    
    if not Game_Over:
        draw_text(10, 460, f"Player Life Remaining: {life} ")
        draw_text(10, 440, f"Game Score: {score}")
        draw_text(10, 420, f"Player Bullet Missed: {missed_bullets}")
    else:
        draw_text(10, 460, f"Game is Over. Your score is {score}.")
        draw_text(10, 440, f'Press "R" to RESTART the Game.')

    draw_player()
    draw_bullets()
    for y in enemies:
        draw_enemy(y)

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(250, 0)
    wind = glutCreateWindow(b"3D OpenGL Intro")

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.12, 1.0)

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()
