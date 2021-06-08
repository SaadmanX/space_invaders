# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 15:10:03 2021

@author: saadm
"""

import random
import pygame
from pygame import mixer


pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("spce_background.png")

icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Invaders Game")

# Player
player_image = pygame.image.load("player_spaceship.png")
player_x = 368
player_y = 500


enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 6
enemy_image = pygame.image.load("enemy_spaceship.png")
for i in range(number_of_enemies):
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(0, 250))
    enemy_x_change.append(random.uniform(0.1, 0.3))
    enemy_y_change.append(128)

bullet_image = pygame.image.load("normal_bullet.png")
bullet_state = "ready"
bullet_y = 450
bullet_change = 2

score_value = 0
display_font = pygame.font.Font("CARGO2.ttf", 32)
score_x = 10
score_y = 10

mixer.music.load("bg.wav")
mixer.music.play(-1)

game_over_font = pygame.font.Font("CARGO2.ttf", 128)

def show_score(x, y):
    score = display_font.render(
        "Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x, y))


def player(x, y):
    screen.blit(player_image, (x, y))


def enemy(x, y):
    screen.blit(enemy_image, (x, y))


def distance(b_x, b_y, e_x, e_y):
    x_dist = abs(b_x - e_x)**2
    y_dist = abs(b_y - e_y)**2
    dist = (x_dist + y_dist)**.5
    if dist < 30:
        return True
    else:
        return False

def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255,0,0))
    screen.blit(game_over_text, (72,250))
    game_over_sound = mixer.Sound("game_over_sound.wav")
    game_over_sound.play()
        

running = True

while running:

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and player_x >= 0:
                player_x -= 10

            if event.key == pygame.K_d and player_x <= 736:
                player_x += 10

            if event.key == pygame.K_s:
                if bullet_state == "ready":
                    bullet_x = player_x + 24
                    fire_bullet(bullet_x, bullet_y)
                    bullet_sound = mixer.Sound("pew_pew.wav")
                    bullet_sound.play()

    player(player_x, player_y)

    if bullet_y < 1:
        bullet_y = 550
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_change

    for x in range(number_of_enemies):
        if enemy_y[x] > 600:
            for y in range(number_of_enemies):
                enemy_y[y] = 2000
            game_over()
            break
        
                
        enemy_x[x] += enemy_x_change[x]

        if enemy_x[x] <= 0:
            enemy_x_change[x] = .2
            enemy_y[x] += enemy_y_change[x]
        if enemy_x[x] >= 736:
            enemy_x_change[x] = -.2
            enemy_y[x] += enemy_y_change[x]

        if enemy_y[x] <= 664:
            enemy(enemy_x[x], enemy_y[x])

        if bullet_state == "fire" and distance(bullet_x, bullet_y, enemy_x[x] + 32, enemy_y[x]):
            explosion = mixer.Sound("enemy_hit_scream.wav")
            explosion.play()
            bullet_y = 550
            bullet_state = "ready"
            score_value += 1
            enemy_x[x] = random.randint(0, 736)
            enemy_y[x] = random.randint(0, 250)

            print(score_value)

        show_score(score_x, score_y)

    pygame.display.update()
