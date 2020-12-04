import pygame
from pygame.locals import *
import sys
from math import pow, sqrt
from time import sleep
from random import choice

# TODO You're up to 16:23
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.mag = self.set_mag()

    def set_mag(self):
        return sqrt(pow(self.x, 2) + pow(self.y, 2))


class Snake:
    def __init__(self, pygame_display_surface, resolution):
        self.body = []
        self.body.append(Point(0, 0))

        self.x_dir = 1
        self.y_dir = 0

        self.surface = pygame_display_surface
        self.res = resolution

    def set_dir(self, x, y):
        self.x_dir = x
        self.y_dir = y

    def update(self):
        self.body[0].x += self.x_dir * self.res
        self.body[0].y += self.y_dir * self.res

    def show(self):
        pygame.draw.rect(self.surface, (0, 255, 0),
                         (self.body[0].x, self.body[0].y, self.res, self.res))


class Food:
    def __init__(self, w, h, pygame_display_surface, resolution):
        self.x = 100
        self.y = 100

        self.board_w = w
        self.board_h = h

        self.surface = pygame_display_surface
        self.res = resolution

        self.possible_x_locations = [x for x in range(0, w, w // resolution)]
        self.possible_y_locations = [x for x in range(0, h, h // resolution)]

        self.location()

    def location(self):
        self.x = choice(self.possible_x_locations)
        self.y = choice(self.possible_y_locations)

    def show(self):
        pygame.draw.rect(self.surface, (255, 0, 0), (self.x, self.y, self.res, self.res))


def stop():
    pygame.quit()
    sys.exit()


pygame.init()
display_surface = pygame.display.set_mode((400, 400))

resolution = 10

snake = Snake(display_surface, resolution)

w, h = pygame.display.get_surface().get_size()
w, h = w // resolution, h // resolution

food = Food(w, h, display_surface, resolution)

while True:
    display_surface.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            stop()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                snake.set_dir(-1, 0)
            elif event.key == K_RIGHT:
                snake.set_dir(1, 0)
            elif event.key == K_DOWN:
                snake.set_dir(0, 1)
            elif event.key == K_UP:
                snake.set_dir(0, -1)

            elif event.key == K_q or event.key == K_ESCAPE:
                stop()

    snake.update()
    snake.show()

    food.show()

    pygame.display.update()
    sleep(0.2)
