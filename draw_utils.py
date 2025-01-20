# FILE: draw_utils.py
import pygame

def draw_image(screen, image, x, y, flip=False):
    if flip:
        image = pygame.transform.flip(image, True, False)
    screen.blit(image, (x, y))

def draw_animated_image(screen, images, index, x, y, flip=False):
    image = images[index]
    draw_image(screen, image, x, y, flip)