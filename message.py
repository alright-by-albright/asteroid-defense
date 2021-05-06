import pygame
import pygame.font
import time
import sys


from bullet import Bullet
from ship import Ship
from settings import Settings


class Message:
    """The message class was initially created to serve as a template for
    for messages. However, the addition of the blocks controlling the
    movement tutorials ended up making this one of the more difficult blocks.
    Another ship is initialized here, in a vain attempt to gain control over
    settings of the ship within the tutorials - to no avail."""
    def __init__(self, controller):
        pygame.sprite.Sprite.__init__(self)
        self.ship = Ship(controller)
        self.settings = Settings()
        self.screen = controller.screen
        self.screen_rect = self.screen.get_rect()
        pygame.mixer.set_reserved(10)
        self.message_sound = pygame.mixer.Sound('sounds/multimedia_alert_error_002_26393.mp3')

    def _intro_msg(self, msg, controller):
        #This is the template used for the mid screen messages that begin
        #constitute the majority of the introduction. After initializing
        #their settings, they're given images and associated rects.
        self.width, self.height = 300, 75
        self.message_color = pygame.Color('black')
        self.text_color = ('blue')
        self.font = pygame.font.SysFont('Perfect DOS VGA 437.ttf', 30)
        self.msg_image = self.font.render(msg, True, self.text_color, self.message_color)
        self.screen.fill((0, 0, 0))
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.screen_rect.center
        #The screen is filled to cover any previous messages, before the
        #new message and player ship are redrawn via blit commands.
        self.screen.fill(self.message_color, self.msg_image_rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        self.ship.blitme()
        pygame.display.flip()
        #The makeshift timer found in AsteroidDefense is used again here to
        #keep messages displayed for a few moments before moving on to the next.
        start_time = float(controller.time_elapsed)
        end_time = float(start_time + 1.5)
        pygame.mixer.find_channel().play(self.message_sound)
        while True:
            if end_time < float(controller.time_elapsed):
                break
            else:
                #While waiting the _check_events method in AsteroidDefense is
                #used to check to see if the player has attempted to quit
                #the game.
                controller._check_events()
                self.screen.blit(self.msg_image, self.msg_image_rect)
                pygame.display.flip()
        self.screen.fill((0, 0, 0))
        self.ship.blitme()
        pygame.display.flip()
        
    def show_right_strafe_key(self):
        """The first of the control explanation modules. This one tells the user
        that the D key is used to strafe right."""
        #self.ship = Ship(self)
        self.settings.ship_speed = 0.00025
        print(self.settings.ship_speed)
        test_passed = False
        self.width, self.height = 300, 75
        self.message_color = pygame.Color('black')
        self.text_color = ('blue')
        self.font = pygame.font.SysFont('Perfect DOS VGA 437.ttf', 30)
        self.screen.fill((0, 0, 0))
        right_msg = 'Press D to strafe right.'
        #The message is displayed in the bottomright corner of the screen
        #to reinforce the rightward movement of the key.
        self.msg_image = self.font.render(right_msg, True, self.text_color, self.message_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.bottomright = self.screen_rect.bottomright
        self.screen.blit(self.msg_image, self.msg_image_rect)
        pygame.display.flip()
        pygame.mixer.find_channel().play(self.message_sound)
        """At this point the scenario portion of the explanation is created.
        The variable test_passed is set to False in order to control the time
        spent. pygame's event.get() is primed, but only to accept key presses
        from the D key. One the player has pressed D, the ship will jet to
        the right until it passes an x value of at least 1050. At this point
        movement is manually ended, and the program shifts the ship back to
        it's center position."""
        while not test_passed:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.ship.moving_right = True
                    elif event.key == pygame.K_q:
                        pygame.mixer.stop()
                        pygame.display.quit()
                        sys.exit()
            self.ship.update()
            self.screen.fill((0, 0, 0))
            self.ship.blitme()
            self.screen.blit(self.msg_image, self.msg_image_rect)
            pygame.display.flip()
            if self.ship.x > 1050:
                self.ship.moving_right = False
                self.ship.update()
                self.screen.fill((0, 0, 0))
                self.ship.blitme()
                pygame.display.flip()
                #With the movement successfully completed, the test_passed
                #variable is given the True value.
                test_passed = True
        while self.ship.x != 600:
            self.ship.moving_left = True
            self.ship.update()
            self.screen.fill((0, 0, 0))
            self.ship.blitme()       
            pygame.display.flip()
            #This control function ensures that x will end it's movement once
            #passing the center point, even if the exact point of 600 is
            #missed.
            if self.ship.x == 600 or self.ship.x < 600:
                self.ship.moving_left = False
                self.ship.center_ship()
                self.ship.update()
                self.ship.blitme()
                break                

    def show_left_strafe_key(self):
        """The second of the movement tutorial methods. This one shows that the
        A key will shift the ship to the left, and the message is displayed
        in the bottom left. This method functions essentially identically
        to the previous."""
        self.settings.ship_speed = 0.25
        test_passed = False
        self.width, self.height = 300, 75
        self.message_color = pygame.Color('black')
        self.text_color = ('blue')
        self.font = pygame.font.SysFont('Perfect DOS VGA 437.ttf', 30)
        self.screen.fill((0, 0, 0))
        left_msg = 'Press A to strafe left.'
        self.msg_image = self.font.render(left_msg, True, self.text_color, self.message_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.bottomleft = self.screen_rect.bottomleft
        self.screen.blit(self.msg_image, self.msg_image_rect) 
        pygame.display.flip()
        pygame.mixer.find_channel().play(self.message_sound)
        while not test_passed:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.ship.moving_left = True
                    elif event.key == pygame.K_q:
                        pygame.mixer.stop()
                        pygame.display.quit()
                        sys.exit()
            self.ship.update()
            self.screen.fill((0, 0, 0))
            self.ship.blitme()
            self.screen.blit(self.msg_image, self.msg_image_rect)
            pygame.display.flip()
            if self.ship.x< 150:
                self.ship.moving_left = False
                self.screen.fill((0, 0, 0))
                self.ship.update()
                self.ship.blitme()
                pygame.display.flip()
                test_passed = True
        while self.ship.x != 600:
            self.ship.moving_right = True
            self.ship.update()
            self.screen.fill((0, 0, 0))
            self.ship.blitme()   
            pygame.display.flip()
            if self.ship.x == 600 or self.ship.x > 600:
                self.ship.moving_right = False
                self.ship.center_ship()
                self.ship.update()
                self.ship.blitme()
                break

    def show_fire_key(self, ad_game):
        """The show_fire_key method informs the player that pressing the
        spacebar will fire the ship's weaponry. The length of this method
        is due in large part to another instance of much needed refactoring
        that time did not permit. The tutorial test itself uses a long,
        winding algorithm to test for a certain number of shots being taken
        by the player. I only realized now that simply checking to see if
        the user had fired once."""
        self.ship = Ship(self)
        test_passed = False
        guns_hot = False
        self.settings.bullet_speed = 2
        self.width, self.height = 300, 75
        self.message_color = pygame.Color('black')
        self.text_color = ('blue')
        self.font = pygame.font.SysFont('Perfect DOS VGA 437.ttf', 30)
        self.screen.fill((0, 0, 0))
        space_msg = 'Press the spacebar to fire gauss cannons.'
        self.screen.fill((0, 0, 0))
        bullet_count = 0
        self.bullets = pygame.sprite.Group()
        self.bullet_fired = pygame.mixer.Sound('sounds/pm_sfg_vol1_weapon_1_1_gun_gunshot_futuristic_363.mp3')
        self.msg_image = self.font.render(space_msg, True, self.text_color, self.message_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.bottomright = self.screen_rect.midbottom
        self.screen.fill(self.message_color, self.msg_image_rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        self.ship.center_ship()
        self.ship.update()
        self.ship.blitme()
        pygame.display.flip()
        pygame.mixer.find_channel().play(self.message_sound)
        #When initially figuring out this sequence, I was working around a
        #requirement of the player having taken 3 shots. I was also attempting
        #to create a delay suitable for allowing any shots in air to travel off
        #screen before filling the screen again.
        while bullet_count < 1:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if len(self.bullets) < self.settings.bullets_allowed:
                            new_bullet = Bullet(self)
                            self.bullets.add(new_bullet)
                            pygame.mixer.find_channel().play(self.bullet_fired)
                            bullet_count += 1
                        elif event.key == pygame.K_q:
                            pygame.mixer.stop()
                            pygame.display.quit()
                            sys.exit()
            self.screen.fill((0, 0, 0))
            self.bullets.update()
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.update()
            self.screen.blit(self.msg_image, self.msg_image_rect)
            self.ship.blitme()
            pygame.display.flip()
            
        start_time = float(ad_game.time_elapsed)
        end_time = float(start_time + 0.5)
        while True:
            if end_time < ad_game.time_elapsed:
                break
            else:
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
                self.screen.fill((0, 0, 0))
                self.bullets.update()
                for bullet in self.bullets.sprites():
                    bullet.draw_bullet()
                for bullet in self.bullets.copy():
                    if bullet.rect.bottom <= 0:
                        self.bullets.remove(bullet)
                        pygame.display.flip()
                self.ship.blitme()
                pygame.display.flip()
            
       
        
    def _clean_screen(self):
        self.screen.fill((0, 0, 0)) 

    def _ship_ai_message(self, msg):
        """This is another piece of the planned AI features that there weren't
        time to impliment."""
        self.width, self.height = 340, 77
        #self.message_color = pygame.Color('dimgrey')
        self.text_color = ('blue')
        self.font = pygame.font.SysFont('Perfect DOS VGA 437.ttf', 30)
        self.msg_image =  self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.topleft = (177, 820)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        return self.msg_image, self.msg_image_rect
