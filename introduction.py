import pygame
import time

from settings import Settings
from message import Message
from userinterface import UserInterface
from shipai import ShipAI

class Intro:
    """This class controls the entirety of the introduction scenario. The
        majority of this section of the game is dialogue driven in order to
        provide both a reason for the situation, as well as a slightly more
        organic way of  displaying the controls to the player."""
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Asteroid Defense")
        #This introduction_done variable serves the control variable for this sequence.
        #Once it has been set to true, the next section of the game will occur via the
        #AsteroidDefender class.
        self.introduction_done = False
        self.message = Message(self)
        

    def _wake_up(self, ad_game):
        """This is the extremely long dialogue sequence composing the introduction. msg
        variables are assigned strings to display to the character, one after another.
        This could have been accomplished much more elegantly, but time didn't allow."""
        self.user_interface = UserInterface(ad_game)
        #An instance of the player ship is created on screen to give the otherwise pure
        #black void a bit of an anchor for the user. This ship will also be used when
        #the controls are shown later.
        self.ai = ShipAI(ad_game)
        msg = 'Hey.'
        #Each message is ran through the Message classes '_intro_msg' method. The command
        #is passed as AsteroidDefender so that Message can access the classes already
        #loaded in that primary controller.
        ad_game.message._intro_msg(msg, ad_game)
        #Another example of a planned feature that wasn't implimented in time.
        self.ai._intro(ad_game)
        ad_game.intro_ai = True
        msg = 'We\'ve got launch clearance.'
        ad_game.message._intro_msg(msg, ad_game)
        msg = 'They did it. Apophis in pieces.'
        ad_game.message._intro_msg(msg, ad_game)
        msg = 'I guess now it\'s A-pieces.'
        ad_game.message._intro_msg(msg, ad_game)
        msg = '. . .'
        ad_game.message._intro_msg(msg, ad_game)
        msg = 'You\'ve got to learn to smile more.'
        ad_game.message._intro_msg(msg, ad_game)
        msg = 'Relax. We\'ll stop the fragments.'
        ad_game.message._intro_msg(msg, ad_game)
        msg = 'The plan\'s good. A wall of pilots... shame we don\'t have more.'
        ad_game.message._intro_msg(msg, ad_game)
        msg = 'Besides, I\'ll be with you.'
        ad_game.message._intro_msg(msg, ad_game)
        msg = 'Come to think of it, more of us sparks would be better than more pilots...'
        ad_game.message._intro_msg(msg, ad_game)
        msg = 'Then again... I don\'t have hands...'
        ad_game.message._intro_msg(msg, ad_game)
        msg = 'How about a quick review simulation as I get us into orbit?'
        ad_game.message._intro_msg(msg, ad_game)
        msg = 'First up: strafing left.'
        ad_game.message._intro_msg(msg, ad_game)
        #Here the first tutorial method is called. The controls for the left strafe, right
        #strafe, and firing the ship's guns, are called one at a time so the keybind
        #assoicated with that action can be displayed on screen.
        ad_game.message.show_left_strafe_key()
        msg = 'Nice! Now strafing right.'
        ad_game.message._intro_msg(msg, ad_game)
        ad_game.message.show_right_strafe_key()
        msg = 'Easy. Not sure why you were so worried.'
        ad_game.message._intro_msg(msg, ad_game)
        msg = 'Finally, the fun part.'
        ad_game.message._intro_msg(msg, ad_game)
        ad_game.message.show_fire_key(ad_game)
        msg = 'Keep in mind, I can only handle firing 5 shots at a time.'
        ad_game.message._intro_msg(msg, ad_game)
        self.user_interface.battery_example(ad_game)
        msg = '''And a reminder, if anything larger than a baseball hits us up there, we're going to feel it.'''
        ad_game.message._intro_msg(msg, ad_game)
        msg = 'Not that I think it will come up.'
        ad_game.message._intro_msg(msg, ad_game)
        msg = 'Anyway, I\'m glad we could get your confidence back up...'
        ad_game.message._intro_msg(msg, ad_game)
        msg = '... and just in time. We\'re here.'
        ad_game.message._intro_msg(msg, ad_game)
        while ad_game.message.ship.rect.y > -40:
            ad_game.message.ship.settings.ship_speed = 0.43
            ad_game.message.ship.rect.y -= 1
            ad_game.message.ship.update()
            ad_game.message.screen.fill((0, 0, 0))
            ad_game.message.ship.blitme()
            pygame.display.flip()
        pygame.mixer.stop()
        self.introduction_done = True
        

    #def _remember(self, ad_game):
        
    def mission_start(self):
        msg = "Okay, we're here."
        
        

