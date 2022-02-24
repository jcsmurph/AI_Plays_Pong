import pygame

class Paddle:
    velocity = 4
    paddleHeight = 70
    paddleWidth = 20

    def __init__(self, x, y):
        self.x = self.originalX = x
        self.y = self.originalY = y

    def draw(self, screen, color):
        pygame.draw.rect(
            screen, color, (self.x, self.y, self.paddleWidth, self.paddleHeight))

    def move(self, up=True):
        if up:
            self.y -= self.velocity
        else:
            self.y += self.velocity

    def reset(self):
        self.x = self.originalX
        self.y = self.originalY

