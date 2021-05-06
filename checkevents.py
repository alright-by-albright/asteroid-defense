import pygame

class CheckEvents:

    def __init__(self):
        pygame.init()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                

    def _check_keydown_events(self,event):
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

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
