import pygame
import random
import math

class Ball:
    maxVelocity = 5
    color = purple = 128, 0, 128
    ballRadius = 7

    def __init__(self, x, y):
        self.x = self.originalX = x
        self.y = self.originalY = y

        angle = self.getRandomAngle(-30, 30, [0])
        pos = 1 if random.random() < 0.5 else -1

        self.xVelocity = pos * abs(math.cos(angle) * self.maxVelocity)
        self.yVelocity = math.sin(angle) * self.maxVelocity

    def getRandomAngle(self, minAngle, maxAngle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(minAngle, maxAngle))

        return angle

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.ballRadius)

    def move(self):
        self.x += self.xVelocity
        self.y += self.yVelocity

    def reset(self):
        self.x = self.originalX
        self.y = self.originalY
        
        angle = self.getRandomAngle(-30, 30, [0])
        xVelocity = abs(math.cos(angle) * self.maxVelocity)
        yVelocity = math.sin(angle) * self.maxVelocity

        self.xVelocity *= -1
        self.yVelocity = yVelocity


