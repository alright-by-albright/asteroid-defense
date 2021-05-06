import pygame

class UserInterface():
    """The UserInterface class controls the elements found at the bottom of the
    game screen while during the main portion - that is, what follows the
    introduction. The battery (bottom right), tiny ship (to the left of the
    battery) and chat message (to be displayed on the bottom left) methods
    are controlled here. Additionally the example battery played during the
    introduction is found here."""
    def __init__(self, ad_game):
        "Initialize the UI, and necesarry resources."
        super().__init__()
        self.screen = ad_game.screen
        self.screen_rect = ad_game.screen.get_rect()
        self.chat_active = False
        #Similar to the explosions method, a dictionary is created with the
        #battery images being added to it.
        self.weapon_battery = {}
        self.weapon_battery['std'] = []
        self.weapon_battery['std'].append(pygame.image.load('images/weapon_battery_5.png'))
        self.weapon_battery['std'].append(pygame.image.load('images/weapon_battery_4.png'))
        self.weapon_battery['std'].append(pygame.image.load('images/weapon_battery_3.png'))
        self.weapon_battery['std'].append(pygame.image.load('images/weapon_battery_2.png'))
        self.weapon_battery['std'].append(pygame.image.load('images/weapon_battery_1.png'))
        self.weapon_battery['std'].append(pygame.image.load('images/weapon_battery_0.png'))
        #The following 3 variables are all associated with the game_over state that was never fully
        #implimented.
        self.ship_integrity = 0
        self.ship_damage = 0
        self._ship_integrity(ad_game)

    def battery_example(self, ad_game):
        """This method controls the logic for the battery shown during the introducion. Variables are
        established to serve as the current frame and a count to limit the loops repeating. After
        getting the image and rect, the image is assigned to the coordinates needed manually. A miniscreen
        is used again to only refresh the portion of the screen that the battery is being displayed on."""
        frame = 0
        frame_count = 0
        self.battery_image = self.weapon_battery['std'][frame]
        self.battery_image_rect = self.battery_image.get_rect()
        self.battery_image_rect.x, self.battery_image_rect.y = 830, 785
        self.miniscreen_width, self.miniscreen_height = self.battery_image.get_size()
        self.miniscreen = pygame.Surface((self.miniscreen_width, self.miniscreen_height))
        self.miniscreen_rect = self.miniscreen.get_rect()
        self.miniscreen.fill((0, 0, 0))
        self.miniscreen_rect.x, self.miniscreen_rect.y = 830, 785
        self.screen.blit(self.battery_image, self.battery_image_rect)
        pygame.display.flip()
        start_time = float(ad_game.time_elapsed)
        end_time = float(start_time + 5)
        #Here is the core logic loop for the graphic. Using a combination of if statements and timers, the
        #battery frames are incremented in ascending and descending order depending on which end the
        #frames are currently moving towards. We begin "descending" when we reach frame 0 (representing a
        #full battery) and "ascending" at frame 5 (a fully depleted battery). When the currently True
        #variable is changed, a break statement is used to return to logic choice that chose between them.
        while start_time < end_time:
            inner_start_time = float(ad_game.time_elapsed)
            inner_end_time = float(inner_start_time + 0.2)
            while frame_count < 11: 
                if frame == 0:
                    descending = True
                if frame == 5:
                    ascending = True
                while descending:
                    for i in range(0, 5):
                        if inner_end_time < ad_game.time_elapsed:
                            frame += 1
                            frame_count += 1
                            inner_end_time += 0.2
                            start_time += 0.2
                            self.screen.blit(self.miniscreen, self.miniscreen_rect)
                            self.battery_image = self.weapon_battery['std'][frame]
                            self.screen.blit(self.battery_image, self.battery_image_rect)
                            pygame.display.flip()
                        if frame == 5:
                            descending = False
                            ascending = True
                            break
                while ascending:
                    for i in range(0, 5):
                        if inner_end_time < ad_game.time_elapsed:
                            frame -= 1
                            frame_count += 1
                            inner_end_time += 0.2
                            start_time += 0.2
                            self.screen.blit(self.miniscreen, self.miniscreen_rect)
                            self.battery_image = self.weapon_battery['std'][frame]
                            self.screen.blit(self.battery_image, self.battery_image_rect)
                            pygame.display.flip()
                        if frame == 0:
                            ascending = False
                            descending = True
                            break
                if frame_count == 10:
                   start_time += 10
            

    def _battery_status(self, ad_game):
        """The battery_status method uses the bullet_count found in AsteroidDefense to shift between the
        different battery frames. This bullet_count variable is updated whenever the gun is fired."""
        bullet_count = ad_game.bullet_count
        self.battery_status_image = self.weapon_battery['std'][bullet_count]
        self.battery_status_rect = self.battery_status_image.get_rect()
        self.battery_status_rect.x = 830
        self.battery_status_rect.y = 785

    def _ship_integrity(self, ad_game):
        """Another of the methods planned to find game_over states. This one would use the number of times
        the ship has been struck by an asteroid - as well as on which side it was struck. Using the
        preloaded images, the non functinoal half of the ship could be displayed."""
        self.ship_structural_integrity = {}
        self.ship_structural_integrity['std'] = []
        self.ship_structural_integrity['std'].append(pygame.image.load('images/playerShip.png'))
        self.ship_structural_integrity['std'].append(pygame.image.load('images/playerShip_2.png'))
        self.ship_structural_integrity['std'].append(pygame.image.load('images/playerShip_3.png'))
        
        self.ship_integrity_image = self.ship_structural_integrity['std'][ad_game.ship.ship_integrity ]
        self.ship_integrity_image_rect = self.ship_integrity_image.get_rect()
        self.ship_integrity_image_rect.x, self.ship_integrity_image_rect.y = 716, 840

            

    def _chat_active(self, msg_image, msg_rect):
        """A method to control updateing the chat box when a message is available."""
        self.chat_active = True
        self.msg_image = msg_image
        self.msg_rect = msg_rect


            

    def _update(self, ad_game):
        """The userinterface class' update  method. The self.chat_active refers to an unused ai function
        and below that is the update method for the battery."""
        if self.chat_active:
            self.screen.blit(self.msg_image, self.msg_rect)
        self._battery_status(ad_game)
        self.screen.blit(self.battery_status_image, self.battery_status_rect)
        self.screen.blit(self.ship_integrity_image, self.ship_integrity_image_rect)

        

        
