class Settings():
    def __init__(self):
        self.screen_width=1400
        self.screen_height=800
        self.screen_color=(255,255,255)

        self.score_color=(60,60,60)
        
        #ship speed factor
        self.ship_speed_factor = 2.5
        self.ship_limit=2

        #bullet
        self.bullet_speed_factor=3
        self.bullet_height=15
        self.bullet_width=3
        self.bullet_color=(60,60,60)
        self.bullet_limited=3

        #alien
        self.fleet_drop_speed=20
        self.alien_speed_factor=10
        self.alien_fleet_direction=1

        self.speedup_scale=1
        self.score_scale=1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor=1.5
        self.bullet_speed_factor=3
        self.alien_speed_factor=1
        self.alien_fleet_direction=1
        self.aliens_points=50



    def increase_speed(self):
        self.ship_speed_factor*=self.speedup_scale
        self.bullet_speed_factor*=self.speedup_scale
        self.alien_speed_factor*=self.speedup_scale

        self.aliens_points=int(self.aliens_points * self.score_scale)

