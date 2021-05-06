import random
import pygame
from pygame.sprite import Sprite

from message import Message

class ShipAI(Sprite):
    """The ShipAI is the flagship class associated with the sadly never
    completed ship ai feature. This was the character that intitially speaks
    during the Introduction section, and would go on to play a role in the
    main portion of the game as well."""

    def __init__(self, ad_game):
        """A class for handling the actions of the ship ai character."""
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.screen = ad_game.screen
        self.settings = ad_game.settings
        self.stats = ad_game.stats
        self.ai_message = Message(self)
        self.ui = ad_game.ui
        #After instantiating the class, several variabels related to idle
        #movement and current temperament are established.
        self.state =''
        self.frame = 1
        self.swap = 1
        self.rising = True
        self.count = 0
        #The cities list is created fresh here for use in each game.
        self.cities = []
        for city in ad_game.stats.cities:
            self.cities.append(city)
        self.speech_cooldown = True
        self.chat_is_active = True
        self.message = ''
        self.start_time = float(ad_game.time_elapsed)
        #At one stage of development using a dictionary to control the ai's
        #movements in the same way that the explosion animations are played.
        self.ai_portrait = {}
        self.ai_portrait['active'] = []
        self.ai_portrait['active'].append(pygame.image.load('images/inactive_ai.png'))
        self.ai_portrait['active'].append(pygame.image.load('images/active_ai.png'))
        #A call to a never completed _quip function that would have prompted
        #the ai to speak, using the chat box on the bottom left of the game
        #screen.
        self._quip(ad_game)
        self.image = self.ai_portrait['active'][self.frame]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (555, 800)

    def _intro(self, ad_game):
        """A method for creating an ai image during the introduction and having
        move across the screen to stand beside the player's ship. This made no
        sense."""
        self.frame = 0
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 555, 203
        #In order to facilitate the need to refill the screen as the ai moved
        #across it, while maintaing any text and the player's ship, a mini
        #surface is created that instead matches the previous rectangle of the
        #ai sprite. It's then filled before the sprite moves to it's new
        #location.
        miniscreen_width, miniscreen_height = self.image.get_size()
        miniscreen = pygame.Surface((miniscreen_width, miniscreen_height))
        miniscreen_rect = miniscreen.get_rect()
        miniscreen.fill('grey')
        self.screen.blit(miniscreen, miniscreen_rect)
        self.screen.blit(self.image, self.rect)
        pygame.display.flip()
        

    def _ship_behaviour(self, ad_game, state, this_asteroid):
        """This function was planned to establish mental states for the ai,
        and easily switch between them using the passed values."""
        self.state = state
        if self.state == 'idle':
            self._ship_ai_idle(ad_game, this_asteroid)
    
    def _ship_ai_idle(self):
        """An attempt to create a simple animation loop of the ai drifting up
        slightly and then down."""
        if self.count < 10 and self.count > 0:
            self.y = self.rect.y
            self.y -= 20
            self.rect.y = self.y
            self.count += 1
        if self.count >= 10 and self.count < 20:
            self.y = self.recy.y
            self.y += 20
            self.rect.y = self.y
            self.count += 1
        if self.count == 20:
            self.count = 0
        

    def _quip(self, ad_game):
        """Attempt to have the ship's ai remark to the player."""
        if self.speech_cooldown == False:
            #This function would have prompted the AI to speak if a timer
            #hadn't been passed. Earlier iterations that did have the
            #speaking AI ran into situations with non stop chat messages
            #and sound alerts.
            print('Quip is active.')
            self.speech_cooldown = True

    def _get_destroyed_city(self):
        """Randomly choose a city to be destroyed."""
        #Here the purpose of the cities list is shown. As asteroids slipped past
        #the player, random numbers would be selected and used as an index. The
        #city associated with that index would be destroyed with the ai
        #remarking upon it. This gives a semi 'fail-state' to the player, in
        #spite of no true game over being achievable by letting asteroids
        #pass by.
        num_of_cities = len(self.cities) - 1
        city_destroyed = random.randint(0, num_of_cities)
        city_destroyed = self.cities[city_destroyed]
        self.cities.remove(city_destroyed)
        message = ('There goes %s ...' % city_destroyed)
        return message
            
    def update(self):
        """Update message to keep them on screen."""
        #The update method for this class calls the _ship_ai_idle method to
        #allow it to increase or decrease it's y value before drawing it to
        #the screen.
        self._ship_ai_idle()
        self.screen.blit(self.image, self.rect)
        
