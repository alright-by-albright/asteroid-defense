import sys
import pygame
import random
import time
import threading
from multiprocessing import Process

from message import Message
from introduction import Intro
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from asteroid import Asteroid
from explosion import Explosion
from userinterface import UserInterface
from shipai import ShipAI

class AsteroidDefense:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        pygame.sprite.Sprite.__init__(self)
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Asteroid Defense")
        self.ship = Ship(self)
        self.ui = UserInterface(self)
        

        #Initialize pygame mixer with arguements
        pygame.mixer.init(48000, -16, 1, 1024)
        #Load sound files
        self.background_music = pygame.mixer.Sound('sounds/pioxonaq_static_scream.mp3')
        self.bullet_fired = pygame.mixer.Sound('sounds/pm_sfg_vol1_weapon_1_1_gun_gunshot_futuristic_363.mp3')
        self.message_sound = pygame.mixer.Sound('sounds/multimedia_alert_error_002_26393.mp3')
        #Adjust sound volumes
        self.background_music.set_volume(0.05)
        self.bullet_fired.set_volume(0.10)
        self.message_sound.set_volume(0.15)
        pygame.mixer.set_reserved(5)
        #Load background image
        self.background = pygame.image.load('images/earthInCrisis.png').convert_alpha()
        self.user_interface = pygame.image.load('images/user_interface_base.png').convert_alpha()     
        #Create an instance to store game statistics and create a scoreboard.
        self.stats = GameStats(self)
        self.sb =  Scoreboard(self)

        #Initialize sprite groups and variables
        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.ai_portraits = pygame.sprite.Group()
        self.ships = pygame.sprite.Group()
        self.asteroids_spawned = 0
        self.asteroids_destroyed = 0
        self.bullet_count = 0
        self.intro_ai = False
        self.introduction = True
        self.speech_ready = True
        self.woke_up = False
        self.game_over_explosion = False
        self.game_over = False
        pygame.display.flip()
        
        #Create process variables
        self.asteroid_thread_created = False
        self.asteroid_bool = False


        self._asteroid_spawn_thread_start()
        self.shipai = ShipAI(self)
            
    def _asteroid_spawn_thread_start(self):
        """"This function creates a thread to be used as a timer."""
        if not self.asteroid_thread_created:
            self.t1 = threading.Thread(target=self._asteroid_spawn_thread)
            self.t1.start()
            self.asteroid_thread_created = True
    
    def _asteroid_spawn_thread(self):
        """This thread will keep a timer for the purpose of spawning
        asteroids at set intervals."""
        self.timer = self.settings.spawn_timer + 1
        self.count = 1
        self.time_elapsed = 0
        while self.intro_ai:
            start_time = float(self.time_elapsed)
            if start_time < self.time_elapsed:
                start_time += 0.1 
                self.intro.ai.update()
        while self.asteroids_spawned < 30:
            if int(self.count) == self.timer or int(self.count) > self.timer:
                self.asteroid_bool = True
                self.count = 0
            else:
                time.sleep(0.1)
                self.time_elapsed += .1
                self.count+= .1
        
    def _create_asteroid(self):
        #Create an asteroid if self.asteroid_bool is True and place it on screen.
        if self.asteroid_bool:
            asteroid = Asteroid(self)
            self.this_asteroid = asteroid
            self.asteroid_width, self.asteroid_height = asteroid.rect.size
            asteroid.rect.x = asteroid.rect.x
            asteroid.rect.y = asteroid.rect.y
            ai_state = random.randint(1, 2)
            if ai_state == 2:
                self.shipai._ship_behaviour(self,  ai_state, self.this_asteroid)
            self.asteroids.add(asteroid)
            self.asteroids_spawned += 1
            self.asteroid_bool = False
        else:
            pass

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_d:
            #Move the ship to the right.
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            #Move the ship to the left.
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            #Fire a bullet from the ship.
            self._fire_bullet()
        elif event.key == pygame.K_q:
            #Exit the game.
            pygame.mixer.stop()
            pygame.display.quit()
            sys.exit()

    def _begin_game(self):
        """Start a new game when the player clicks Play"""
        #button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if self.intro.introduction_done and not self.stats.game_active:
            #Reset the game statistics.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.count = 1
            self.stats.game_active = True
            self.sb.prep_ships()
            #Get rid of any remaining aliens and bullets.
            self.asteroids.empty()
            self.bullets.empty()

            
    def _end_game(self):
        if self.asteroids_destroyed == 29:
            victory = True
            while victory:
                self._check_events()
                victory_screen = pygame.image.load('images/victory_screen.png')
                victory_screen_rect = victory_screen.get_rect()
                self.screen.blit(victory_screen, victory_screen_rect)
                pygame.display.flip()
                
            

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False


    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            pygame.mixer.find_channel().play(self.bullet_fired)
            self.bullet_count += 1
            self.ui._battery_status(self)

    def _ship_hit(self):
        #if self.ship.x
        if self.ui.ship_integrity < 3:
            #Decrement ships_left.
            if self.ship.ship_damaged_side == -1:
                self.ui.ship_structural_integrity += 1
                self.ship.ship_damaged_side = 100
            if self.ship.ship_damaged_side == 1:
                self.ui.ship_integrity += 2
                self.ship.ship_damaged_side = 100
        if self.ui.ship_integrity >= 3:
            self.stats.game_active = False
            self.game_over_explosion = True
            while self.game_over:
                self._check_events()
                game_over_screen = pygame.image.load('images\game_over.png')
                game_over_screen_rect = game_over_screen.get_rect()
                self.screen.blit(game_over_screen, game_over_screen_rect)
                pygame.display.flip()
                #pygame.mouse.set_visible(True)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        #Update bullet positions.
        self.bullets.update()
        #Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                self.bullet_count -= 1
                self.ui._battery_status(self)

        self._check_bullet_asteroid_collisions()

    def _check_bullet_asteroid_collisions(self):
        """Respond to bullet-asteroid collisions."""
        collisions = pygame.sprite.groupcollide(
            self.asteroids, self.bullets, False, False)
        for asteroid in collisions:
            self.this_asteroid = asteroid
            centerX, centerY = self.this_asteroid.rect.midtop
            self.center_x = centerX
            self.center_y = centerY
            self.this_asteroid_width, self.this_asteroid_height = self.this_asteroid.rect.size
            self.this_asteroid_x = self.this_asteroid.rect.x
            self.this_asteroid_y = self.this_asteroid.rect.y
            expl = Explosion(self, centerX, centerY)
            self.explosions.add(expl)
            self.bullet_count -= 1
            self.ui._battery_status(self)
        collisions = pygame.sprite.groupcollide(
            self.asteroids, self.bullets, True, True)
 
    def _check_asteroids_bottom(self):
        """Check if any asteroids have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for asteroid in self.asteroids.sprites():
            if asteroid.rect.top >= asteroid.y_target:
                self.asteroids.remove(asteroid)
                self.asteroids_destroyed += 1          

    def _update_asteroids(self):
        """Check for and manage collisions between asteroids and the player ship."""
        self.asteroids.update()
        self.ships.add(self.ship)
        #Look for asteroid-ship collisions. self.this_asteroid is created as an object with
        #matching rect information to the player ship. This allows the previously created
        #explosion functions (that only worked on asteroids) to now work on the player ship as well.
        if pygame.sprite.spritecollideany(self.ship, self.asteroids):
            #If an asteroid has previously struck the player twice,
            #this final explosion will be larger.
            self._ship_hit()
            if self.game_over_explosion == True:
                self.this_asteroid = self.ship
                self.centerX, self.centerY = self.this_asteroid.rect.midtop
                self.center_x = self.centerX
                self.center_y = self.centerY
                self.this_asteroid_width, self.this_asteroid_height = self.this_asteroid.rect.size
                self.this_asteroid_x = self.this_asteroid.rect.x
                self.this_asteroid_y = self.this_asteroid.rect.y
                self.this_asteroid.starting_x = self.ship.rect.x
                self.this_asteroid.starting_y = self.ship.rect.y
                self.this_asteroid.x_target = self.ship.rect.x + 1
                self.this_asteroid.y_target = self.ship.rect.y + 1
                expl = Explosion(self, self.centerX, self.centerY)
                self.explosions.add(expl)
                self.asteroids.asteroid.kill()
                self.asteroids_destroyed += 1
                #A "catch all". An explosion will occur even for the first strike.
            else:
                self.this_asteroid = self.ship
                self.centerX, self.centerY = self.this_asteroid.rect.midtop
                self.center_x = self.centerX
                self.center_y = self.centerY
                self.this_asteroid_width, self.this_asteroid_height = self.this_asteroid.rect.size
                self.this_asteroid_x = self.this_asteroid.rect.x
                self.this_asteroid_y = self.this_asteroid.rect.y
                self.this_asteroid.starting_x = self.ship.rect.x
                self.this_asteroid.starting_y = self.ship.rect.y
                self.this_asteroid.x_target = self.ship.rect.x + 1
                self.this_asteroid.y_target = self.ship.rect.y + 1
                expl = Explosion(self, self.centerX, self.centerY)
                self.explosions.add(expl)
                self.asteroids_destroyed += 1
            collisions= pygame.sprite.groupcollide(self.asteroids, self.ships, False, False)
            #An iterable group 'collisions' is created to examine positioning during the strike.
            #A planned feature (close to implimentation) was the player ship losing functionality
            #specifically on the struck side.
            for asteroid in collisions:
                this_asteroid_hit = asteroid
                this_asteroid_right_x, this_asteroid_right_y = this_asteroid_hit.rect.bottomright
                this_asteroid_left_x, this_asteroid_left_y = this_asteroid_hit.rect.bottomleft
                ship_center_x = self.ship.rect.centerx
                ship_x_distance_right = ship_center_x - this_asteroid_right_x
                ship_x_distance_left = ship_center_x - this_asteroid_left_x
                ship_x_sign = ship_center_x - this_asteroid_left_x
                print(self.ui.ship_integrity)
                if ship_x_sign > 0:
                    self.ship_damaged_side = -1
                if ship_x_sign < 0:
                    self.ship_damaged_side = 1
                if ship_x_sign == 0:
                    self.ship_damaged_side = 1
                else:
                    #If something goes wrong, print 'uh oh' in the terminal.
                    print('uh oh')
                #Clean up. Remove any asteroids that struck the player, as well as temp
                #ship sprites created for collision testing.
                collisions = pygame.sprite.groupcollide(self.asteroids, self.ships, True, True) 
                
        #Look for asteroids hitting the bottom of the screen.
        self._check_asteroids_bottom()
        #Check to see if the timer has indicated it's time to spawn an asteroid.
        self._create_asteroid()
        


    def _update_explosions(self):
        """Check the status of explosions, update current frame."""
        for explosion in self.explosions.sprites():
            explosion.update(self)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.blit(self.background, [0,0])
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.asteroids.draw(self.screen)
        self.explosions.draw(self.screen)
        self.screen.blit(self.user_interface, [149, 802])
        self.shipai.update()
        self.ui._update(self)
        self._end_game()
        pygame.display.flip()     

    def run_game(self):
        """Start the main loop for the game."""
        #Message is instantiated to perform it's role of displaying messages throughout the intro.
        #Next, the introduction is called which begins the game via dialogue.
        #Following completion of the introduction, _wake_up is checked for True before moving on.
        #Finally, begin playing background music.
        self.message = Message(self)
        self.intro = Intro()
        self.intro._wake_up(self)
        pygame.mixer.find_channel().play(self.background_music, -1)
        
        while self.intro.introduction_done:
            #Another check to ensure the introduction was completed, then to establish methods
            #that require constant refreshing.
            self._begin_game()
            self._check_events()
            if self.stats.game_active:
                #These are seperated from the above because _check_events will still need to be
                #ran during game over/ victory screens, regardless of game state.
                #Another call for updates.
                self.ship.update()
                self._update_bullets()
                self._update_asteroids()
                self._update_explosions()

            #_update_screen and bullet updates are both ran outside of game state, to ensure objects
            #leave the screen.
            self._update_screen()

            #Get rid of bullets that have disappeared.
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
                    self.ui._battery_status(self)

if __name__ == '__main__':
    #The main loop insantiates the primary controller of our game's pieces, AsteroidDefense.
    #The game is begun using the run_game method.
    ad = AsteroidDefense()
    ad.run_game()
