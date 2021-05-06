import pygame
import os

class Settings:
    """A class to store all settings for Asteroid Defense."""
    """Despite being one of the more bare bones original classes, it's still
    heavily used. Some settings like spawn_timer and speech_cooldown have been
    added for us in the various new methods."""
    def __init__(self):
        """Initialize the games static settings."""
        #Screen settings.
        self.screen_width = 1200
        self.screen_height = 907
        
        #Ship settings
        self.ship_limit = 3

        #Bullet settings
        self.bullet_width = 6
        self.bullet_height = 20
        self.bullet_color = pygame.Color('blue')
        self.bullets_allowed = 5

        #Asteroid settings
        self.spawn_timer = 3

        #How quickly the game speeds up.
        self.timer_decrease = 1
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

        #ShipAI settings
        self.speech_cooldown = 3

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.75
        self.bullet_speed = 4
        self.asteroid_speed = 0.0007
        self.explosion_speed = 0.00035

        #Scoring
        self.asteroid_count = 30

    def increase_speed(self):
        """Increase speed settings and asteroid point values."""
        self.spawn_timer -= 1
        
        
