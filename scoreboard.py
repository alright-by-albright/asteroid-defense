import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """A class to report scoring information."""
    """This is another class that's been made obsolete, but that I'm again
    afraid to remove in case of unforeseen problems arising. None of these
    methods are used at this stage."""
    def __init__(self, ad_game):
        """Initialize scorekeeping attributes."""
        self.ad_game = ad_game
        self.screen = ad_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ad_game.settings
        self.stats = ad_game.stats

        #Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        #Prepare ships
        self.prep_ships()

    def show_score(self):
        """Draw scores, level, and ships to the screen."""
        
        #self.ships.draw() 

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ad_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
        



