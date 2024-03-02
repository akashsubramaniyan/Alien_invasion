import pygame
from pygame.sprite import Group
from settings import Settings
from game_states import GameStats
from ship import Ship
import game_function as gf
from alien import Alien 
from button import Button
from score_board import ScoreBoard
def run_game():
    pygame.init()
    ai_settings=Settings()  
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("ALIEN INVASION")
   
    screen_color=(ai_settings.screen_color)
   
    ship=Ship(ai_settings,screen)
    stats=GameStats(ai_settings)
     
    sb=ScoreBoard(ai_settings,screen,stats)
    button = Button(ai_settings,screen,"Start")
    bullets=Group()
    aliens=Group() 
    gf.create_fleet(ai_settings,screen,ship,aliens)
    while True:
        gf.check_event(ai_settings,screen,stats,button,ship,aliens,bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets)
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,button)
        
        
run_game()