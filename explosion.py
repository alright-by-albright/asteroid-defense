import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    """A class for managing the explosion animations."""
    
    def __init__(self, ad_game, center_x, center_y):
        """Each instance of explosion is passed the center x and y values of
            the associated sprite."""
        #Initializing variables. start_time and time_elapsed will make use of
        #the pseudo timer created with the thread running alongside the program,
        #created in the asteroid defense class.
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.start_time = float(ad_game.time_elapsed)
        self.explosion_var = 0
        #A dictionary of imagesd is created, based upon the size of the object
        #that is exploding found in the asteroid_var.
        self.explosion_anim = {}
        if ad_game.this_asteroid.asteroid_var == 1:
            self.explosion_var = 1
            self.explosion_anim['sm'] = []
            self.explosion_anim['sm'].append(pygame.image.load('images/small_explosion_0.png'))
            self.explosion_anim['sm'].append(pygame.image.load('images/small_explosion_1.png'))
            self.explosion_anim['sm'].append(pygame.image.load('images/small_explosion_2.png'))
            self.explosion_anim['sm'].append(pygame.image.load('images/small_explosion_3.png'))
            self.explosion_anim['sm'].append(pygame.image.load('images/small_explosion_4.png'))
            self.explosion_anim['sm'].append(pygame.image.load('images/small_explosion_5.png'))
            self.explosion_anim['sm'].append(pygame.image.load('images/small_explosion_6.png'))
            self.image = self.explosion_anim['sm'][self.frame]            
            self.rect = self.image.get_rect()

        if ad_game.this_asteroid.asteroid_var == 2:
            self.explosion_var = 2
            self.explosion_anim['lg'] = []
            self.explosion_anim['lg'].append(pygame.image.load('images/large_explosion_0.png'))
            self.explosion_anim['lg'].append(pygame.image.load('images/large_explosion_1.png'))
            self.explosion_anim['lg'].append(pygame.image.load('images/large_explosion_2.png'))
            self.explosion_anim['lg'].append(pygame.image.load('images/large_explosion_3.png'))
            self.explosion_anim['lg'].append(pygame.image.load('images/large_explosion_4.png'))
            self.explosion_anim['lg'].append(pygame.image.load('images/large_explosion_5.png'))
            self.explosion_anim['lg'].append(pygame.image.load('images/large_explosion_6.png'))
            self.image = self.explosion_anim['lg'][self.frame]
            self.rect = self.image.get_rect()

        if ad_game.this_asteroid.asteroid_var == 3:
            self.explosion_var = 3
            self.explosion_anim['lg'] = []
            self.explosion_anim['lg'].append(pygame.image.load('images/large_explosion_0.png'))
            self.explosion_anim['lg'].append(pygame.image.load('images/large_explosion_1.png'))
            self.explosion_anim['lg'].append(pygame.image.load('images/large_explosion_2.png'))
            self.image = self.explosion_anim['lg'][self.frame]
            self.rect = self.image.get_rect()

        #The explosion takes the starting x and y coordinates of the object
        #it was called for, combined with that objects target points, and
        #recreates the path the object was following. This creates a smoother
        #animation that drifts along the established course.
        self.starting_x = ad_game.this_asteroid.starting_x
        self.starting_y = ad_game.this_asteroid.starting_y
        self.rect.center = (center_x, center_y)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.x_target = ad_game.this_asteroid.x_target
        self.y_target = ad_game.this_asteroid.y_target
        self.run = float(self.x_target - self.starting_x)
        self.rise = float(self.y_target - self.starting_y)

    def update(self, ad_game):
        """The explosion sprites is updated based up on time passing. This
            prevents the animation frames from being called simultanesouly
            one after another."""
        #Explosion_var's continue to be used to ensure the text of the
        #dictionary's outside of variables isn't called to the wrong object.
        if self.start_time < float(ad_game.time_elapsed):
            self.frame += 1
            if self.explosion_var == 1:
                if self.frame == len(self.explosion_anim['sm']):
                    #If the current frame matches the length of the animation
                    #the sprite is destroyed before it can cause an out of index
                    #range error.
                    self.kill()
                else:
                    self.x+= (self.run * ad_game.settings.explosion_speed)
                    self.rect.x = self.x
                    self.y+= (self.rise * ad_game.settings.explosion_speed)
                    self.rect.y = self.y
                    self.image = self.explosion_anim['sm'][self.frame]
                    self.start_time += 0.25
            if self.explosion_var == 2:
                #Explosion_var 2 had a 2nd planned purpose, operating as the
                #final switch before displaying a game over screen. This would
                #hopefully allow for the full animation of the player's
                #ship exploding to play, before ending the game.
                if self.frame == len(self.explosion_anim['lg']):
                    self.kill()
                    ad_game.asteroids_destroyed += 1
                    if ad_game.game_over_explosion == True:
                        ad_game.game_over = True
                        ad_game._end_game()
                else:
                    self.x+= (self.run * ad_game.settings.explosion_speed)
                    self.rect.x = self.x
                    self.y+= (self.rise * ad_game.settings.explosion_speed)
                    self.rect.y = self.y
                    self.image = self.explosion_anim['lg'][self.frame]
                    self.start_time += 0.25
            if self.explosion_var == 3:
                if self.frame == len(self.explosion_anim['lg']):
                    self.kill()
                else:
                    self.image = self.explosion_anim['lg'][self.frame]
                    self.start_time += 0.25
        else:
            #If it isn't time to update the frame, the explosion is instead
            #moved along it's trajectory, although at a slower pace than
            #the original object.
            self.x+= (self.run * ad_game.settings.explosion_speed)
            self.rect.x = self.x
            self.y+= (self.rise * ad_game.settings.explosion_speed)
            self.rect.y = self.y
            
    
            
            
        
