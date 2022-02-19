import pygame
from tank import Tank
import math
from bullet import Bullet

pygame.init()
screen = pygame.display.set_mode((800, 800))

BACKGROUND = pygame.image.load('Assets\\background.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (1600, 1600))
bg_x = 0
bg_y = 0


# tank = Tank(100, 100)

left = False
right = False
up = False
down = False

bullet_img = pygame.image.load('Assets\\shot_blue.png')
bullet_img = pygame.transform.scale(bullet_img, (50, 50))
bullets = []

tank_img = pygame.image.load('Assets\\BlueTank.png')
tank_img = pygame.transform.scale(tank_img, (50, 50))
current_img = tank_img

turret_img = pygame.image.load('Assets\\BlueTurret.png')
turret_img = pygame.transform.scale(turret_img, (50, 50))

clock = pygame.time.Clock()

running = True

def movement():
    global current_img, bg_x, bg_y
    if left:
        current_img = pygame.transform.rotate(tank_img, 90)
        bg_x += 2
    elif right:
        current_img = pygame.transform.rotate(tank_img, -90)
        bg_x -= 2
    elif up:
        current_img = tank_img
        bg_y += 2
    elif down:
        current_img = pygame.transform.rotate(tank_img, 180)
        bg_y -= 2
    
    pygame.draw.rect(screen, (255, 0, 0), (375, 375, 50, 50), 2)
    screen.blit(current_img, (375, 375, 100, 100))

def turret_turn(pos_x, pos_y):
    global turret_img
    x = 375 - pos_x
    y = 375 - pos_y
    new_turret_img = pygame.transform.rotate(turret_img, math.degrees(math.atan2(x, y)))
    new_rect = new_turret_img.get_rect(center = turret_img.get_rect(center = (400, 400)).center)
    screen.blit(new_turret_img, new_rect)

def draw_bullet():
    global bullets
    for bullet in bullets:
        temp_bullet_img = pygame.transform.rotate(bullet_img, bullet.angle())
        new_rect = temp_bullet_img.get_rect(center = temp_bullet_img.get_rect(center = (bullet.x+25, bullet.y+25)).center)
        screen.blit(temp_bullet_img, new_rect)
        pygame.draw.rect(screen, (255, 0, 0), (bullet.x, bullet.y, 50, 50), 2)
        bullet.move()
        
while running:
    screen.fill((0, 0, 0))
    screen.blit(BACKGROUND, (bg_x, bg_y))
    clock.tick(120)
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    movement()
    turret_turn(mouse_x, mouse_y)
    draw_bullet()
    
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
            if event.button == 1:
                bullets.append(Bullet(375, 375, mouse_x-25, mouse_y-25)) 
        
    pygame.display.flip()