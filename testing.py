import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode(
            (1200, 907))
    screen_rect = screen.get_rect()
    pygame.display.set_caption("Asteroid Defense")
    background = pygame.image.load('images/earthInCrisis.png').convert_alpha()
    screen.blit(background, [0,0])
    pygame.display.flip()
    click = 0
    
    for click in range(0, 20):
        #def _check_events(self):
            #"""Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            #if event.type == pygame.QUIT:
                #testing = False
                #sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                click += 1

if __name__ == '__main__':
    main()
    
