class GameStats:
    """Track statistics for Asteroid Defense."""
    #At this stage, this is 90% a depricated file fit for removal - but the
    #fear of errors stills my hand. A planned use for this file involed
    #populating a list of cities to be used to tabulate a final grade of
    #player performance. 
    def __init__(self, ad_game):
        """Initialize statistics."""
        self.settings = ad_game.settings
        self.cities = []
        self.reset_stats()
        ships_left = 1
        #Start Asteroid Defense in an inactive state.
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.cities.append('Shangai')
        self.cities.append('Beijing')
        self.cities.append('Istanbul')
        self.cities.append('Tokyo')
        self.cities.append('Moscow')
        self.cities.append('Singapore')
        self.cities.append('Rio De Janeiro')
        self.cities.append('Berlin')
        self.cities.append('Hong Kong')
        self.cities.append('Dubai')
        self.cities.append('Seoul')
        self.cities.append('Cairo')
        self.cities.append('New York')
        self.cities.append('DC')
        self.cities.append('London')
        self.cities.append('Paris')
        
