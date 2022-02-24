import pygame
from .paddles import Paddle
from .ball import Ball

# python version 3.10.2
# pygame version 2.1.2
# Neat version 0.92

pygame.init()


class GameInfo:
    def __init__(self, playerOneHits, playerOneScore, playerTwoHits, playerTwoScore):
        self.playerOneHits = playerOneHits
        self.playerOneScore = playerOneScore
        self.playerTwoHits = playerTwoHits
        self.playerTwoScore = playerTwoScore


class Game:

    # Screen information
    pygame.display.set_caption("AI Plays Pong")
    scoreFont = pygame.font.SysFont("Arial", 50)

    # Object colors
    playerOneColor = 255, 0, 0
    playerTwoColor = 0, 0, 255
    playerColors = [(playerOneColor), (playerTwoColor)]
    white = 255, 255, 255
    black = 0, 0, 0
    purple = 128, 0, 128

    # Initialize class
    def __init__(self, screen, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.playerOnePaddle = Paddle(
            10, self.screenHeight // 2 - Paddle.paddleHeight // 2)
        self.playerTwoPaddle = Paddle(
            self.screenWidth - 10 - Paddle.paddleWidth, self.screenHeight // 2 - Paddle.paddleHeight//2)
        self.ball = Ball(self.screenWidth // 2, self.screenHeight // 2)

        self.playerOneScore = 0
        self.playerTwoScore = 0

        self.playerOneHits = 0
        self.playerTwoHits = 0

        self.screen = screen

    def drawScore(self):
        playerOneScoreText = self.scoreFont.render(
            f"{self.playerOneScore}", 1, self.playerOneColor)
        playerTwoScoreText = self.scoreFont.render(
            f"{self.playerTwoScore}", 1, self.playerTwoColor)

        self.screen.blit(playerOneScoreText, (self.screenWidth //
                                          4 - playerOneScoreText.get_width()//2, 20))
        self.screen.blit(playerTwoScoreText, (self.screenWidth * (3/4) -
                                          playerTwoScoreText.get_width()//2, 20))

    def drawHits(self):
        hitsText = self.scoreFont.render(
            f"{self.playerOneHits + self.playerTwoHits}", 1, self.purple)
        self.screen.blit(hitsText, (self.screenWidth //
                         2 - hitsText.get_width()//2, 10))

    def halfCourt(self):
        for i in range(10, self.screenHeight, self.screenHeight//20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(
                self.screen, self.white, (self.screenWidth//2 - 5, i, 1, self.screenHeight//20))

    def paddleBallCollisionDirection(self, ball, paddle):
        self.ball = ball
        self.paddle = paddle
        middlePaddle = paddle.y + paddle.paddleHeight / 2
        ballPaddleDiff = middlePaddle - ball.y
        reductionFactor = (paddle.paddleHeight / 2) / ball.maxVelocity
        yVel = ballPaddleDiff / reductionFactor
        ball.yVelocity = -1 * yVel

    # Change direction of ball when hitting paddle or wall

    def handleBallCollision(self):
        ball = self.ball
        playerOnePaddle = self.playerOnePaddle
        playerTwoPaddle = self.playerTwoPaddle

        if ball.y + ball.ballRadius >= self.screenHeight or ball.y - ball.ballRadius <= 0:
            ball.yVelocity *= -1

        if ball.xVelocity < 0:
            if ball.y >= playerOnePaddle.y and ball.y <= playerOnePaddle.y + Paddle.paddleHeight or ball.x - ball.ballRadius <= playerOnePaddle.x + Paddle.paddleWidth:
                ball.xVelocity *= -1
                self.paddleBallCollisionDirection(ball, playerOnePaddle)
                self.playerOneHits += 1

        else:
           if ball.y >= playerTwoPaddle.y and ball.y <= playerTwoPaddle.y + Paddle.paddleHeight and ball.x + ball.ballRadius >= playerTwoPaddle.x:
                ball.xVelocity *= -1
                self.paddleBallCollisionDirection(ball, playerTwoPaddle)
                self.playerTwoHits += 1

    # draw screen

    def draw(self, drawScore=True, drawHits=False):
        self.screen.fill(self.black)

      #  self.halfCourt()

        if drawScore:
            self.drawScore()
        if drawHits:
            self.drawHits()

        for p, paddle in enumerate([self.playerOnePaddle, self.playerTwoPaddle]):
            paddle.draw(self.screen, self.playerColors[p])

        self.ball.draw(self.screen)

    # Allow paddles to move

    def handlePaddleMovement(self, left=True, up=True):
        if left:
            if up and self.playerOnePaddle.y - Paddle.velocity < 0:
                return False
            if not up and self.playerOnePaddle.y + Paddle.paddleHeight > self.screenHeight:
                return False

            self.playerOnePaddle.move(up)

        else:
            if up and self.playerTwoPaddle.y - Paddle.velocity < 0:
                return False
            if not up and self.playerTwoPaddle.y + Paddle.paddleHeight > self.screenHeight:
                return False
            self.playerTwoPaddle.move(up)

        return True

    # Create the gameplay loop
    def loop(self):
        self.ball.move()
        self.handleBallCollision()

        if self.ball.x < 0:
            self.ball.reset()
            self.playerOneScore += 1
        elif self.ball.x > self.screenWidth:
            self.ball.reset()
            self.playerTwoScore += 1

        gameInfo = GameInfo(self.playerOneHits, self.playerOneScore,
                            self.playerTwoHits, self.playerTwoScore)

        return gameInfo

    # Reset the game
    def reset(self):
        self.ball.reset()
        self.playerOnePaddle.reset()
        self.playerTwoPaddle.reset()
        self.playerOneScore = 0
        self.playerTwoScore = 0
        self.playerOneHits = 0
        self.playerTwoHits = 0
