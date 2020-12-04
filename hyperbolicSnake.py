# PYTHON2, DO NOT USE
import sys, pygame
import math
#import pygame.gfxdraw
import random

SIZE = WIDTH, HEIGHT = 800, 800
SPEED = 0.10
#Please make these equal
BLACK = 0,0,0
WHITE = 255,255,255
RED = 255, 0, 0
#highscore_file = open('highscores', 'r+')

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)

class Point:
    def __init__(self, r, theta):
        #Of course, this could just be a tuple.
        self.theta = theta
        self.r = r
        self.direction = None
        self.rad_mod = 1.0
    def plot(self):
        eucl_r = math.tanh(self.r / 2)
        '''Fun stuff about circle radius'''
        circ_r = round(abs(eucl_r - math.tanh(self.r / 2 - SPEED / 4)) * WIDTH / 2)
        if circ_r < 1:
           circ_r = 1
        x = round(eucl_r * math.cos(self.theta) * WIDTH / 2)
        y = round(eucl_r * math.sin(self.theta) * HEIGHT / 2)
        pygame.draw.circle(screen, BLACK, (int(WIDTH / 2 + x), int(HEIGHT / 2 - y)), int(circ_r), 1)

class Blocker:
    def __init__(self, snake):
        #Not implemented
        while 1:
            self.r = random.uniform
            break


class Snake:
    def __init__(self, points):
        self.points = points
        self.length = len(points)
        self.add = 0
        self.goal = None
        self.dead = False
    def move(self):
        copypoint = self.points[0]
        newpoint = Point(copypoint.r, copypoint.theta)
        newpoint.direction = copypoint.direction
        move_point(newpoint, SPEED, newpoint.direction)
        self.points = [newpoint] + self.points
#        eucl_rs = math.tanh(self.points[0].r / 2)
#        xs = eucl_rs * math.cos(self.points[0].theta)
#        ys = eucl_rs * math.sin(self.points[0].theta)
#        circ_rs = abs(eucl_rs - math.tanh(self.points[0].r / 2 - SPEED / 4))
####        print "*", circ_rs
#        eucl_ra = math.tanh(self.goal.r / 2)
#        xa = eucl_ra * math.cos(self.goal.theta)
#        ya = eucl_ra * math.sin(self.goal.theta)
#        circ_ra = 2 * abs(eucl_ra - math.tanh(self.goal.r / 2 - SPEED / 4))
#        dist = (xs - xa)**2 + (ya - ys)**2
####        print "*", dist, (circ_rs + circ_ra)**2
####        if dist < (circ_rs + circ_ra)**2:
        if intersect(self.points[0], self.goal):
            self.eat()
        if self.add == 0:
            gone = self.points.pop()
        self.add -= 1
        if self.add < 0:
            self.add = 0
        if len(self.points) > 3:
            for segment in self.points[3:]:
                if intersect(segment, self.points[0]):
                    self.die()
    def plot(self):
        for point in self.points:
            point.plot()
    def eat(self):
        global SPEED
        SPEED += 0.00
        self.add += 2
        self.goal.replace()
        self.goal.max_dist += 0.1
        self.goal.rad_mod *= 0.96
        self.length += 2
    def left_turn(self):
        self.points[0].direction -= math.pi / 2
    def right_turn(self):
        self.points[0].direction += math.pi / 2
    def die(self):
        self.dead = True

class Apple:
    def __init__(self):
        self.max_dist = 2.0
        self.rad_mod = 2.0
        self.replace()
    def replace(self):
        self.r = random.uniform(0.1, self.max_dist)
        self.theta = random.uniform(0.0, math.pi * 2)
        self.plot()
    def plot(self):
        eucl_r = math.tanh(self.r / 2)
        '''Fun stuff about circle radius'''
        self.circ_r = round(self.rad_mod * abs(eucl_r - math.tanh(self.r / 2 - SPEED / 4)) * WIDTH / 2)
        x = round(WIDTH / 2 + eucl_r * math.cos(self.theta) * WIDTH / 2)
        y = round(HEIGHT / 2 - eucl_r * math.sin(self.theta) * HEIGHT / 2)
        pygame.draw.circle(screen, RED, (int(x), int(y)), int(self.circ_r))
        
def move_point(p, d, angle):
    sign4 = d / abs(d)
    if angle < -1 * math.pi:
        angle += math.pi * 2
    if angle > math.pi:
        angle -= math.pi * 2
#    print "angle: ", angle
    sign1 = abs(angle) / angle
    new_r = math.acosh((math.cosh(p.r) * math.cosh(d)) - (math.sinh(p.r) * math.sinh(d) * math.cos(angle)))
    test = (math.cosh(p.r) * math.cosh(new_r) - math.cosh(d)) / (math.sinh(p.r) * math.sinh(new_r))
#    print test
    if test < 1.0:
        p.theta += sign1 * sign4 * math.acos(test)
    else:
        p.theta += 0
    new_angle = sign1 * math.acos((math.cosh(p.r) - (math.cosh(new_r) * math.cosh(d))) / (math.sinh(new_r) * math.sinh(d)))
    p.r = new_r
    p.direction = new_angle

def intersect(circle1, circle2):
    eucl_r1 = math.tanh(circle1.r / 2)
    x1 = eucl_r1 * math.cos(circle1.theta)
    y1 = eucl_r1 * math.sin(circle1.theta)
    circ_r1 = circle1.rad_mod * abs(eucl_r1 - math.tanh(circle1.r / 2 - SPEED / 4))
#    print circ_r1
    eucl_r2 = math.tanh(circle2.r / 2)
    x2 = eucl_r2 * math.cos(circle2.theta)
    y2 = eucl_r2 * math.sin(circle2.theta)
    circ_r2 = circle2.rad_mod * abs(eucl_r2 - math.tanh(circle2.r / 2 - SPEED / 4))
    dist = (x1 - x2)**2 + (y1 - y2)**2
#    print dist, (circ_r1 + circ_r2)**2
    if dist < (circ_r1 + circ_r2)**2:
        return True
    return False

test_point = Point(0.86, 0.2223)
test_point.direction = math.pi/2
x = math.cos(0.2223)
y = math.sin(0.2223)

screen.fill(WHITE)

pygame.draw.circle(screen, BLACK, (WIDTH/2, HEIGHT/2), WIDTH / 2, 1)

pygame.draw.line(screen, BLACK, (WIDTH/2, HEIGHT/2), (x * WIDTH / 2 + WIDTH / 2, -1 * y * HEIGHT / 2 + HEIGHT / 2))
leave = False

snake = Snake([test_point])
apple = Apple()
snake.goal = apple

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            leave = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            leave = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            snake.left_turn()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            snake.right_turn()
#        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
#            snake.add = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            apple.replace()
#        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
#            SPEED += 0.01
#        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
#            SPEED -= 0.01
    if leave:
        break
    time_passed = clock.tick(15)
    pygame.display.flip()
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLACK, (WIDTH/2, HEIGHT/2), WIDTH / 2, 1)
    snake.move()
    snake.plot()
    apple.plot()
    if snake.dead:
        break
#    move_point(test_point, SPEED, test_point.direction)
#    test_point.plot()
print "Score: ", snake.length
sys.exit()
