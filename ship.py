import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""
    """The last of the original classes that's been kept in use. Changes here
    would be the image used (a png instead of a bmp to allow for transparency)
    and some small changes to speed here and there. A ship_integrity variable
    was also added for use in reaching the game_over game state, but this was
    not completed."""
    def __init__(self, ad_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ad_game.screen
        self.settings = ad_game.settings
        self.screen_rect = ad_game.screen.get_rect()

        #Load the ship image and get its rect.
        self.image = pygame.image.load('images/playerShip.png').convert_alpha()
        self.rect = self.image.get_rect()

        #"Asteroid variable" for use when determining explosion size
        self.asteroid_var = 3
        self.ship_damaged_side = 0

        #Start each new ship at the bottom center of the screen.
        self.rect.center = (600, 760)

        #Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        #Movement flags
        self.moving_right = False
        self.moving_left = False

        #Structural Integrity
        self.ship_integrity = 0
        
    def update(self):
        """Update the ship's position based on the movement flag."""
        #Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        #Update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
        

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.center = (600, 760)
        self.x = float(self.rect.x)
