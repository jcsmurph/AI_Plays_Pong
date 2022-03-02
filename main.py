import pygame
from pong_game import Game
import neat
import os
import time
import pickle

# python version 3.10.2
# pygame version 2.1.2
# Neat version 0.92

class PongGame:
    def __init__(self, screen, width, height):
        self.game = Game(screen, width, height)
        self.ball = self.game.ball
        self.playerOnePaddle = self.game.playerOnePaddle
        self.playerTwoPaddle = self.game.playerTwoPaddle

    def testAi(self, net):
        clock = pygame.time.Clock()
        run = True

        while run:
            clock.tick(60)
            gameInfo = self.game.loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            output = net.activate((self.playerTwoPaddle.y, abs(
                self.playerTwoPaddle.x - self.ball.x), self.ball.y))
            decision = output.index(max(output))

            if decision == 1:
                self.game.handlePaddleMovement(left=False, up=True)
            elif decision == 2:
                self.game.handlePaddleMovement(left=False, up=False)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.handlePaddleMovement(left=True, up=True)
            elif keys[pygame.K_s]:
                self.game.handlePaddleMovement(left=True, up=False)

            self.game.draw(drawScore=True)
            pygame.display.update()

    def trainAi(self, genomeOne, genomeTwo, config, draw=False):
        run = True
        startTime = time.time()

        netOne = neat.nn.FeedForwardNetwork.create(genomeOne, config)
        self.genomeOne = genomeOne
        
        netTwo = neat.nn.FeedForwardNetwork.create(genomeTwo, config)
        self.genomeTwo = genomeTwo

        maxAllowedHits = 100

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            gameInfo = self.game.loop()

            self.aiMovePaddles(netOne, netTwo)

            if draw:
                self.game.draw(drawScore=False, drawHits=True)

            pygame.display.update()

            duration = time.time() - startTime

            if gameInfo.playerOneScore == 1 or gameInfo.playerTwoScore == 1 or gameInfo.playerOneHits >= maxAllowedHits:
                self.calculateFitness(gameInfo, duration)
                break

            return False

    # Allow for AI to move paddles
    def aiMovePaddles(self, netOne, netTwo):
        players = [(self.genomeOne, netOne, self.playerOnePaddle, True),
                   (self.genomeTwo, netTwo, self.playerTwoPaddle, False)]

        for (genome, net, paddle, left) in players:
            output = net.activate(
                (paddle.y, abs(paddle.x - self.ball.x), self.ball.y))
            decision = output.index(max(output))

            validMovement = True
            if decision == 0:
                genome.fitness -= 0.01
            elif decision == 1:
                validMovement = self.game.handlePaddleMovement(left=left, up=True)
            else:
                validMovement = self.game.handlePaddleMovement(left=left, up=False)

            if not validMovement:
                genome.fitness -= 1

    # Calculate AI fitness
    def calculateFitness(self, gameInfo, duration):
        self.genomeOne.fitness += gameInfo.playerOneHits + duration
        self.genomeTwo.fitness += gameInfo.playerTwoHits + duration

# Define the Genomes
def evaluateGenomes(genomes, config):
    width, height = 700, 500
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("AI Plays Pong")

    for g, (_, genomeOne) in enumerate(genomes):
        print(round(g/len(genomes) * 100), end=" ")
        genomeOne.fitness = 0
        for _, genomeTwo in genomes[min(g+1, len(genomes) - 1):]:
            genomeTwo.fitness = 0 if genomeTwo.fitness == None else genomeTwo.fitness
            pong = PongGame(screen, width, height)

            forceQuit = pong.trainAi(genomeOne, genomeTwo, config, draw=True)
            if forceQuit:
                quit()

    # Neat configuration


def runNeat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(evaluateGenomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def smartestAi(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winnerNet = neat.nn.FeedForwardNetwork.create(winner, config)

    width, height = 700, 500
    screen = pygame.display.set_mode(width,height)
    pygame.display.set_caption("AI Plays Pong")
    pong = PongGame(screen, width, height)
    pong.testAi(winnerNet)


if __name__ == "__main__":
    localDir = os.path.dirname(__file__)
    config_path = os.path.join(localDir, "neat-config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    runNeat(config)
    smartestAi(config)
