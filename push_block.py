# not used
import pygame
class PushBlock():
    def __init__(self, x, y, size, colour):
        self.x = x
        self.y = y
        self.size = size
        self.colour = colour
        self.cur_frame = 0
        self.falling = False

    def get_area(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def get_feet_area(self):
        return pygame.Rect(self.x, self.y+self.size, self.size, 1)