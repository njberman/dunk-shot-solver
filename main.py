import pygame
import os
import math
import random
import pygetwindow as gw
import pyautogui
from PIL import Image


def get_screenshot():
    window_title = 'Bluestacks App Player'

    window, = gw.getWindowsWithTitle(window_title)
    window.activate()
    pyautogui.sleep(0.5)

    screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
    cropped_screenshot = screenshot.crop((window.width / 2.7, 35, window.width - 35, window.height - 50))
    cropped_screenshot.save('screenshot.png')

get_screenshot()

SCALE = 1

pygame.init()

image = pygame.image.load(os.path.join('screenshot.png'))
orig_width, orig_height = image.get_size()
width, height = (orig_width * SCALE, orig_height * SCALE)

scaled_image = pygame.transform.smoothscale(image, (width, height))

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

def transform_point(x, y):
    return (x, height - y)

def locate_ball():
    for y in range(orig_height):
        for x in range(orig_width):
            r, g, b, a = image.get_at((x, y))
            if (r == 255 and g == 139 and b == 0) or (r == g and g == b and b == 170 and y > height / 2):
                return transform_point(x * SCALE, y * SCALE)
    return 0, 0

def locate_hoop():
    for y in range(orig_height):
        for x in range(orig_width):
            #216,78,43,
            r, g, b, a = image.get_at((x, y))
            if r == 216 and g == 79 and b == 44:
                return transform_point(x * SCALE + 5, y * SCALE + 4)
    return 0, 0

def calculate_u_and_alpha(ball_x, ball_y, hoop_x, hoop_y):
    a, b = ball_x, ball_y
    c, d = hoop_x, hoop_y

    minimum_alpha = math.atan((d - b)/(c - a))
    alpha = float(input(f'Please enter the angle you would like between {round(minimum_alpha, 2)} and {round(math.pi / 2, 2)}: '))
    # alpha = minimum_alpha + 0.1
    u = math.sqrt(4.9) * abs((c - a) / math.cos(alpha)) / math.sqrt(b - d + (c - a) * math.tan(alpha))

    return u, alpha

def basketball_pos(t, u, alpha, initial, hoop):
    initial_x, initial_y = initial
    orig_hoop_x, hoop_x, hoop_y = hoop

    sign = abs(orig_hoop_x - initial_x) / (orig_hoop_x - initial_x)

    t = min(t, (hoop_x - initial_x) / (u * math.cos(alpha)))

    return transform_point(initial_x + u * math.cos(alpha) * sign * t, initial_y + (u * math.sin(alpha) * t - 4.9 * t ** 2))

ball_x, ball_y = locate_ball()
orig_hoop_x, hoop_y = locate_hoop()
hoop_x = max(orig_hoop_x, ball_x + abs(orig_hoop_x - ball_x))
u, alpha = calculate_u_and_alpha(ball_x, ball_y, hoop_x, hoop_y)

print(ball_x, ball_y)
print(hoop_x, hoop_y)
print(u, alpha)


time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            time = 0

    screen.fill('black')
    screen.blit(scaled_image, (0, 0))

    pygame.draw.circle(screen, 'blue', transform_point(ball_x, ball_y), 5)
    pygame.draw.circle(screen, 'purple', transform_point(orig_hoop_x, hoop_y), 5)

    b_x, b_y = basketball_pos(time, u, alpha, (ball_x, ball_y), (orig_hoop_x, hoop_x, hoop_y))
    pygame.draw.circle(screen, 'orange', (b_x, b_y), 10)

    pygame.display.flip()

    time += 0.05


    clock.tick(60)

pygame.quit()
