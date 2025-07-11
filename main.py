import pygame
import os
import math
import random

SCALE = 0.4

pygame.init()

image = pygame.image.load(os.path.join('image.jpg'))
orig_width, orig_height = image.get_size()
width, height = (orig_width * SCALE, orig_height * SCALE)

scaled_image = pygame.transform.smoothscale(image, (width, height))

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

def locate_ball():
    for y in range(orig_height):
        for x in range(orig_width):
            r, g, b, a = image.get_at((x, y))
            if r == 255 and g == 138 and b == 0:
                return x * SCALE, y * SCALE
    return 0, 0

def locate_hoop():
    for y in range(orig_height):
        for x in range(orig_width):
            #216,78,43,
            r, g, b, a = image.get_at((x, y))
            if r == 216 and g == 78:
                return x * SCALE + 40, y * SCALE + 4
    return 0, 0

def calculate_u_and_alpha(ball_x, ball_y, hoop_x, hoop_y):
    a = hoop_x - ball_x
    b = ball_y - hoop_y

    minimum_alpha = math.atan(b/a)
    alpha = minimum_alpha + 0.1
    u = math.sqrt(4.9) * abs(a / math.cos(alpha)) / math.sqrt(a * math.tan(alpha) - b)

    return u, alpha

def basketball_pos(t, u, alpha, inital_x, initial_y):
    return inital_x + u * math.cos(alpha) * t, initial_y - u * math.sin(alpha) * t - 4.9 * t ** 2

ball_x, ball_y = locate_ball()
hoop_x, hoop_y = locate_hoop()
u, alpha = calculate_u_and_alpha(ball_x, ball_y, hoop_x, hoop_y)

time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill('black')
    screen.blit(scaled_image, (0, 0))

    pygame.draw.circle(screen, 'blue', (ball_x, ball_y), 5)
    pygame.draw.circle(screen, 'purple', (hoop_x, hoop_y), 5)

    b_x, b_y = basketball_pos(time, u, alpha, ball_x, ball_y)
    pygame.draw.circle(screen, 'orange', (b_x, b_y), 10)

    pygame.display.flip()

    time += 0.05

    clock.tick(60)

pygame.quit()
