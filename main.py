import pygame
from math import sin
from time import sleep
from random import randint
from sys import exit


pygame.init()
icon = pygame.image.load('icon.png')
win = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Pong")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.Font("font.ttf", 40)
paddle_sound = pygame.mixer.Sound("Pong_paddle_sound.mp3")
wall_sound = pygame.mixer.Sound("Pong_wall_sound.mp3")
score_sound = pygame.mixer.Sound("Pong_score_sound.mp3")

vx, vy = -5, randint(-5, 5)

pad1score = pad2score = 0

ball = pygame.Rect(350, 240, 10, 10)
pad1 = pygame.Rect(25, 200, 20, 100)
pad2 = pygame.Rect(656, 200, 20, 100)


def hitFactor(by, py, ph):
    relativeIntersectY = (py + (ph / 2)) - by
    normalizedRelativeIntersectionY = (relativeIntersectY / (ph / 2))
    bounceAngle = normalizedRelativeIntersectionY
    return 5 * -sin(bounceAngle)


def renderFont(score1, score2):
    score1_surf = font.render(score1, True, (255, 255, 255))
    score1_rect = score1_surf.get_rect(center=(250, 75))
    win.blit(score1_surf, score1_rect)
    score1_surf = font.render(score2, True, (255, 255, 255))
    score1_rect = score1_surf.get_rect(center=(500, 75))
    win.blit(score1_surf, score1_rect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    win.fill((0, 0, 0))
    for i in range(26):
        pygame.draw.rect(win, (255, 255, 255), (347, 21.1 * (i - 1), 6, 14))
    pygame.draw.rect(win, (255, 255, 255), (ball.x, ball.y, ball.w, ball.h))
    pygame.draw.rect(win, (255, 255, 255), (pad1.x, pad1.y, pad1.w, pad1.h))
    pygame.draw.rect(win, (255, 255, 255), (pad2.x, pad2.y, pad2.w, pad2.h))
    renderFont(str(pad1score), str(pad2score))

    ball.x += vx
    ball.y += vy

    if ball.y < 0:
        wall_sound.play()
        ball.y = 5
        vy *= -1
    elif ball.y > 495:
        wall_sound.play()
        ball.y = 495
        vy *= -1

    if ball.x <= -10:
        score_sound.play()
        pad1score += 1
        ball.x, ball.y = 350, 250
        vx, vy = vx * -1, randint(-5, 5)
        sleep(1)
    elif ball.x >= 710:
        score_sound.play()
        pad2score += 1
        ball.x, ball.y = 350, 250
        vx, vy = vx * -1, randint(-5, 5)
        sleep(1)

    if ball.colliderect(pad1):
        paddle_sound.play()
        vy = hitFactor(ball.y, pad1.y, pad1.h)
        vx *= -1
        ballx = 45 + 10
    elif ball.colliderect(pad2):
        paddle_sound.play()
        vy = hitFactor(ball.y, pad2.y, pad2.h)
        vx *= -1
        ballx = 656 - 10

    if pygame.key.get_pressed()[pygame.K_w]:
        pad1.y -= 5
    elif pygame.key.get_pressed()[pygame.K_s]:
        pad1.y += 5
    if pygame.key.get_pressed()[pygame.K_UP]:
        pad2.y -= 5
    elif pygame.key.get_pressed()[pygame.K_DOWN]:
        pad2.y += 5

    if pad1.y >= 400:
        pad1.y = 400
    elif pad1.y <= 0:
        pad1.y = 0
    if pad2.y >= 400:
        pad2.y = 400
    elif pad2.y <= 0:
        pad2.y = 0

    pygame.display.update()
    clock.tick(60)
