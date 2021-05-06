import pygame
from pygame.sprite import Sprite
import random

class Asteroid(Sprite):
    """A class for controlling asteroid behaviour."""
    
    def __init__(self, ad_game):
        #Initialize a new instance of this class with each asteroid generation.
        #Get the settings and such from the ad_game class.
        super().__init__()
        self.screen = ad_game.screen
        self.settings = ad_game.settings
        self.asteroid_var = 0
        self.random_image = random.randint(1, 4)
        self._random_image()
        self.rect = self.image.get_rect()
        
        #Get a random x value to place our asteroid's spawn at.
        self.rect.x = random.randint(0, 1200)
        self.starting_x = self.rect.x
        self.rect.y = self.rect.height - 150
        self.starting_y = self.rect.y
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        #Now, another random x value to serve as the asteroid's target.
        #This will be our random trajectory.
        self.x_target = random.randint(0, 1200)
        self.y_target = 1000
        #The asteroids movement will be based off of the slope of the line
        #connecting those 2 coordinate pairs.
        self.run = float(self.x_target - self.rect.x)
        self.rise = float(self.y_target - self.rect.y)
        self.rect.topleft = (self.rect.x, self.rect.y)

    def _random_image(self):
        """This function will select one of four random asteroid images."""
        self.random_image = random.randint(1, 4)
        if self.random_image == 1:
            self.image = pygame.image.load('images/asteroid_1.png').convert_alpha()
            self.asteroid_var = 1
        if self.random_image == 2:
            self.image = pygame.image.load('images/asteroid_2.png').convert_alpha()
            self.asteroid_var = 2
        if self.random_image == 3:
            self.image = pygame.image.load('images/asteroid_3.png').convert_alpha()
            self.asteroid_var = 2
        if self.random_image == 4:
            self.image = pygame.image.load('images/asteroid_4.png').convert_alpha()
            self.asteroid_var = 2
            
    def update(self):
        """This update will apply the rise and run values to the asteroids
            current x and y values."""
        self.x+= (self.run * self.settings.asteroid_speed)
        self.curr_x = self.x
        self.rect.x = self.x
        self.y+= (self.rise * self.settings.asteroid_speed)
        self.curr_y = self.y
        self.rect.y = self.y

            
