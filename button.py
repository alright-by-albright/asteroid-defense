import pygame.font

class Button:
    """This class has been 100% depricated.However, I'm afraid to remove it
        due to unforeseen problems that may arise."""
    def __init__(self, ad_game, msg):
        """Initialize button attributes."""
        self.screen = ad_game.screen
        self.screen_rect = self.screen.get_rect()

        #Set the dimensions and properties of the button.
        self.width, self.height = 300, 200
        self.button_color = ('red')
        self.text_color = ('black')
        self.font = pygame.font.SysFont(None, 100)

        #Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.midtop

        #The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.midbottom = self.rect.midbottom

    def draw_button(self):
        #Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
