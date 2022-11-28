import pygame, sys
from pygame.locals import *
import random

pygame.init()

FPS = 3
FramePerSec = pygame.time.Clock()

# Predefined some colors
BLUE = (85, 144, 206)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen information
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Game")

font = pygame.font.Font('freesansbold.ttf', 32)


class Snake(pygame.sprite.Sprite):
    score = 0
    direction = 0  #up 1, down -1, left -2, right 2
    body = []

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("snake_art/Snake.png")
        self.rect = self.image.get_rect()
        self.rect.center = (25, 25)
        #self.rect = pygame.Rect(0, 0, 50, 50)
        #self.rect.center = (75, 75)
        self.body.append(self.rect.center)

    def update(self, food):
        #print(self.score)
        if self.body[0][0] + 50 == food.rect.center[
                0] and self.body[0][1] + 50 == food.rect.center[1]:
            food.eaten()
            self.score += 1
            self.body.append(self.body[-1])

        for i in range(len(self.body) - 1, -1, -1):
            if i > 0:
                self.body[i] = (self.body[i - 1][0], self.body[i - 1][1])
            if i == 0:
                if self.detectCollision():
                    pygame.quit()
                    sys.exit()
                if self.direction == -1:
                    self.image = pygame.transform.rotate(
                        pygame.image.load("snake_art/Snake.png"), 180)
                    self.body[0] = (self.body[0][0], self.body[0][1] + 50)
                if self.direction == -2:
                    self.image = pygame.transform.rotate(
                        pygame.image.load("snake_art/Snake.png"), 90)
                    self.body[0] = (self.body[0][0] - 50, self.body[0][1])
                if self.direction == 1:
                    self.image = pygame.transform.rotate(
                        pygame.image.load("snake_art/Snake.png"), 0)
                    self.body[0] = (self.body[0][0], self.body[0][1] - 50)
                if self.direction == 2:
                    self.image = pygame.transform.rotate(
                        pygame.image.load("snake_art/Snake.png"), 270)
                    self.body[0] = (self.body[0][0] + 50, self.body[0][1])

    def draw(self, surface):
        adjacent = []
        tempImage = self.image
        for i in range(len(self.body)):
            tempRect = pygame.Rect(self.body[i][0] + 25, self.body[i][1] + 25,
                                   50, 50)
            if i == 0 and len(self.body) > 1:
                surface.blit(self.image, tempRect)
            elif i == 0:
                surface.blit(pygame.image.load("snake_art/Snake0.png"),
                             tempRect)
            elif i == len(self.body) - 1 and len(self.body) - 1 != 0:
                if self.body[i - 1][1] + 50 == self.body[i][1]:  # up
                    tempImage = pygame.transform.rotate(
                        pygame.image.load("snake_art/Snake3.png"), 0)
                    surface.blit(tempImage, tempRect)
                elif self.body[i - 1][1] - 50 == self.body[i][1]:  # down
                    tempImage = pygame.transform.rotate(
                        pygame.image.load("snake_art/Snake3.png"), 180)
                    surface.blit(tempImage, tempRect)
                elif self.body[i - 1][0] - 50 == self.body[i][0]:  # right
                    tempImage = pygame.transform.rotate(
                        pygame.image.load("snake_art/Snake3.png"), 270)
                    surface.blit(tempImage, tempRect)
                else:  # left
                    tempImage = pygame.transform.rotate(
                        pygame.image.load("snake_art/Snake3.png"), 90)
                    surface.blit(tempImage, tempRect)
            else:
                if not adjacent:
                    adjacent.append(self.body[i - 1])
                    adjacent.append(self.body[i])
                    adjacent.append(self.body[i + 1])
                else:
                    adjacent[0] = self.body[i - 1]
                    adjacent[1] = self.body[i]
                    adjacent[2] = self.body[i + 1]

                if adjacent[0][1] == adjacent[1][1] and adjacent[2][
                        1] == adjacent[1][1]:  # vertially adjacent
                    tempImage = pygame.transform.rotate(
                        pygame.image.load("snake_art/Snake2.png"), 90)
                    surface.blit(tempImage, tempRect)
                elif adjacent[0][0] == adjacent[1][0] and adjacent[2][
                        0] == adjacent[1][0]:  # horizontally adjacent
                    tempImage = pygame.transform.rotate(
                        pygame.image.load("snake_art/Snake2.png"), 0)
                    surface.blit(tempImage, tempRect)
                elif adjacent[0][0] == adjacent[1][0] and adjacent[2][
                        1] == adjacent[1][1]:  #first LR second AB
                    if adjacent[0][1] + 50 == adjacent[1][1]:  # first below
                        if adjacent[2][0] + 50 == adjacent[1][
                                0]:  # second right
                            tempImage = pygame.transform.rotate(
                                pygame.image.load("snake_art/Snake4.png"), 180)
                            surface.blit(tempImage, tempRect)

                        else:  # second left
                            tempImage = pygame.transform.rotate(
                                pygame.image.load("snake_art/Snake4.png"), 90)
                            surface.blit(tempImage, tempRect)

                    else:  # first above
                        if adjacent[2][0] + 50 == adjacent[1][
                                0]:  # second right
                            tempImage = pygame.transform.rotate(
                                pygame.image.load("snake_art/Snake4.png"), 270)
                            surface.blit(tempImage, tempRect)
                        else:  # second left
                            tempImage = pygame.transform.rotate(
                                pygame.image.load("snake_art/Snake4.png"), 0)
                            surface.blit(tempImage, tempRect)
                elif adjacent[0][1] == adjacent[1][1] and adjacent[2][
                        0] == adjacent[1][0]:  #first AB second LR
                    if adjacent[0][0] + 50 == adjacent[1][0]:  # first right
                        if adjacent[2][1] + 50 == adjacent[1][
                                1]:  # second below
                            tempImage = pygame.transform.rotate(
                                pygame.image.load("snake_art/Snake4.png"), 180)
                            surface.blit(tempImage, tempRect)
                        else:  # second above
                            tempImage = pygame.transform.rotate(
                                pygame.image.load("snake_art/Snake4.png"), 270)
                            surface.blit(tempImage, tempRect)
                    else:  # first left
                        if adjacent[2][1] + 50 == adjacent[1][
                                1]:  # second below
                            tempImage = pygame.transform.rotate(
                                pygame.image.load("snake_art/Snake4.png"), 90)
                            surface.blit(tempImage, tempRect)
                        else:  # second above
                            tempImage = pygame.transform.rotate(
                                pygame.image.load("snake_art/Snake4.png"), 0)
                            surface.blit(tempImage, tempRect)
            #pygame.draw.rect(surface, BLUE, tempRect)

    def detectCollision(self):
        for i in range(len(self.body) - 1, -1, -1):
            if self.direction == -1 and self.body[i] == (self.body[0][0],
                                                         self.body[0][1] + 50):
                return True
            if self.direction == -2 and self.body[i] == (self.body[0][0] - 50,
                                                         self.body[0][1]):
                return True
            if self.direction == 1 and self.body[i] == (self.body[0][0],
                                                        self.body[0][1] - 50):
                return True
            if self.direction == 2 and self.body[i] == (self.body[0][0] + 50,
                                                        self.body[0][1]):
                return True
        return False


class Food(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.rect.center = (225, 125)

    def eaten(self):
        randx = random.randrange(25, SCREEN_WIDTH - 25, 50)
        randy = random.randrange(25, SCREEN_HEIGHT - 25, 50)
        self.rect.center = (randx, randy)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect, 0, 12)


player = Snake()
text = font.render(str(player.score), True, WHITE)
textRect = text.get_rect()
textRect.center = (SCREEN_WIDTH // 2, 100)
apple = Food()

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.direction = 1
            if event.key == pygame.K_DOWN:
                player.direction = -1
            if event.key == pygame.K_LEFT:
                player.direction = -2
            if event.key == pygame.K_RIGHT:
                player.direction = 2
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.fill(BLACK)

    player.update(apple)

    apple.draw(DISPLAYSURF)
    player.draw(DISPLAYSURF)

    text = font.render(str(player.score), True, WHITE)
    DISPLAYSURF.blit(text, textRect)

    pygame.display.update()
    FramePerSec.tick(FPS)
