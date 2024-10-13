import pygame

BLUE = (0, 0, 255)

class Food:
    def __init__(self,hp,x,y,foodSize):
        self.x = x
        self.y = y
        self.hp = hp
        self.foodSize = foodSize

    def draw(self,screen):
        pygame.draw.circle(screen, BLUE, (self.x, self.y), self.foodSize)