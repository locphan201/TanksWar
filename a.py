import pygame, math
from server_map import Map
from tank import Tank
from shot import Shot

pygame.init()
screen = pygame.display.set_mode((800, 800))

index = 0

server = Map()
server.add_tank(Tank(400, 400, 0))

FULL_HP = 100
hp = FULL_HP
hp_rect = pygame.Rect(375, 355, 50, 10)

RELOAD_TIME = 1.5
reload_time = 0
reload_rect = pygame.Rect(375, 365, 50, 10)


BACKGROUND = pygame.image.load('Assets\\background.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (1600, 1600))
x, y = server.tank_pos(index)
bg_x = x - 400
bg_y = y - 400

# tank = Tank(100, 100)
left = False
right = False
up = False
down = False

bullet_img = pygame.image.load('Assets\\shot_blue.png')
bullet_img = pygame.transform.scale(bullet_img, (50, 50))

tank_img = pygame.image.load('Assets\\BlueTank.png')
tank_img = pygame.transform.scale(tank_img, (50, 50))
current_img = tank_img

turret_img = pygame.image.load('Assets\\BlueTurret.png')
turret_img = pygame.transform.scale(turret_img, (50, 50))

clock = pygame.time.Clock()

running = True

def movement():
    global current_img, bg_x, bg_y
    x, y = server.tank_pos(index)
    tank_rect = current_img.get_rect(center = current_img.get_rect(center = (400, 400)).center)
    move_x = 0
    move_y = 0
    if left:
        if x <= 25:
            move_x = 0
        elif up:
            if y <= 25:
                move_y = 0
            else:
                current_img = pygame.transform.rotate(tank_img, 45)
                move_x = -math.sqrt(2)
                move_y = -math.sqrt(2)
        elif down:  
            if y >= 1574:
                move_y = 0
            else:  
                current_img = pygame.transform.rotate(tank_img, 135)
                move_x = -math.sqrt(2)
                move_y = math.sqrt(2)
        else:
            current_img = pygame.transform.rotate(tank_img, 90)
            move_x = -2
            move_y = 0
    elif right:
        if x >= 1574:
            move_x = 0
        elif up:
            if y <= 25:
                move_y = 0
            else:
                current_img = pygame.transform.rotate(tank_img, -45)
                move_x = math.sqrt(2)
                move_y = -math.sqrt(2)
        elif down:  
            if y >= 1574:
                move_y = 0
            else:  
                current_img = pygame.transform.rotate(tank_img, -135)
                move_x = math.sqrt(2)
                move_y = math.sqrt(2)
        else:
            current_img = pygame.transform.rotate(tank_img, -90)
            move_x = 2
            move_y = 0           
    elif up:
        current_img = tank_img
        if y > 25:
            move_x = 0
            move_y = -2
    elif down:
        current_img = pygame.transform.rotate(tank_img, 180)
        if y < 1574:
            move_x = 0
            move_y = 2
    
    server.update_tank(index, move_x, move_y)
    bg_x += -move_x
    bg_y += -move_y
    screen.blit(current_img, tank_rect)

def turret_turn(pos_x, pos_y):
    global turret_img
    x = 375 - pos_x
    y = 375 - pos_y
    new_turret_img = pygame.transform.rotate(turret_img, math.degrees(math.atan2(x, y)))
    new_rect = new_turret_img.get_rect(center = turret_img.get_rect(center = (400, 400)).center)
    screen.blit(new_turret_img, new_rect)

def draw_shots():
    global server
    x, y = server.tank_pos(index)
    for shot in server.get_all_shots():
        temp_bullet_img = pygame.transform.rotate(bullet_img, shot.angle())
        new_rect = temp_bullet_img.get_rect(center = temp_bullet_img.get_rect(center = (shot.x+25+bg_x, shot.y+25+bg_y)).center)
        screen.blit(temp_bullet_img, new_rect)
        pygame.draw.rect(screen, (255, 0, 0), (shot.x+bg_x, shot.y+bg_y, 50, 50), 2)
    server.update_shots()
 
def draw_reload_bar():
    global reload_time, reload_rect
    temp = pygame.Rect(reload_rect.x, reload_rect.y, reload_rect.width*(1-reload_time/RELOAD_TIME), reload_rect.height)
    pygame.draw.rect(screen, (255, 255, 255), temp)
    pygame.draw.rect(screen, (0, 0, 0), reload_rect, 3) 

def draw_hp_bar():
    global hp, hp_rect
    temp = pygame.Rect(hp_rect.x, hp_rect.y, hp_rect.width*(hp/FULL_HP), hp_rect.height)
    pygame.draw.rect(screen, (225,6,0), temp)
    pygame.draw.rect(screen, (0, 0, 0), hp_rect, 3)
    
    
while running:
    screen.fill((0, 0, 0))
    screen.blit(BACKGROUND, (bg_x, bg_y))
    clock.tick(120)
    
    mouse_x, mouse_y = pygame.mouse.get_pos()

    movement()
    draw_shots()
    turret_turn(mouse_x, mouse_y)
    draw_hp_bar()
    draw_reload_bar()
    if reload_time <= 0.0:
        reload_time = 0.0
    else:
        reload_time -= 1/120
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_w:
                up = True
            if event.key == pygame.K_s:
                down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False
            if event.key == pygame.K_w:
                up = False
            if event.key == pygame.K_s:
                down = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and reload_time <= 0.0:
                x, y = server.tank_pos(index)
                server.add_shot(Shot(x-25, y-25, mouse_x-25-bg_x, mouse_y-25-bg_y))
                reload_time = RELOAD_TIME
        
    pygame.display.flip()