import pygame
import os

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

ball_x, ball_y = locate_ball()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill('black')
    screen.blit(scaled_image, (0, 0))

    pygame.draw.circle(screen, 'blue', (ball_x, ball_y), 5)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
