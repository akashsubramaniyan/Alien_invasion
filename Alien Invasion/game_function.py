import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep
def key_down_event(event,ai_settings,screen,stats,ship,bullets):
     sound = pygame.mixer.Sound("sound.mp3")
     if event.key == pygame.K_RIGHT:
          ship.moving_right=True
     elif event.key == pygame.K_LEFT:
          ship.moving_left=True
     elif event.key == pygame.K_SPACE:
          fire_bullets(ai_settings,screen,ship,bullets)
          if stats.game_active:
               pygame.mixer.Sound.play(sound)
           
 
def fire_bullets(ai_settings,screen,ship,bullets):
     if len(bullets) < ai_settings.bullet_limited:
          new_bullet=Bullet(ai_settings,screen,ship)
          bullets.add(new_bullet)


def key_up_event(ship,event):
     if event.key == pygame.K_RIGHT:
          ship.moving_right=False
     elif event.key ==pygame.K_LEFT:
          ship.moving_left=False

def check_event(ai_settings,screen,stats,button,ship,aliens,bullets):
     for event in pygame.event.get():
          if event.type == pygame.QUIT:
                sys.exit()
          elif event.type == pygame.KEYDOWN:
               key_down_event(event,ai_settings,screen,stats,ship,bullets)
               
          elif event.type == pygame.KEYUP:
               key_up_event(ship,event)

          elif event.type==pygame.MOUSEBUTTONDOWN:
               mouse_x,mouse_y=pygame.mouse.get_pos()
               check_button(ai_settings,screen,stats,button,ship,aliens,bullets,mouse_x,mouse_y)

def check_button(ai_settings,screen,stats,button,ship,aliens,bullets,mouse_x,mouse_y):
     button_clicked =button.rect.collidepoint(mouse_x,mouse_y)
     if button_clicked and not stats.game_active:
          ai_settings.initialize_dynamic_settings()
          pygame.mouse.set_visible(False)
          stats.reset_stats()
          stats.game_active=True
          aliens.empty()
          bullets.empty()

          create_fleet(ai_settings,screen,ship,aliens)
          ship.center_ship()

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,button):
     screen.fill(ai_settings.screen_color)
     sb.show_score()
     for bullet in bullets.sprites():
          bullet.draw_bullet()
    
     ship.blitme()
     aliens.draw(screen)
     if not stats.game_active:
          button.draw_button()
         
     pygame.display.flip()
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
     check_bullet_alien_collison(ai_settings,screen,stats,sb,ship,aliens,bullets)
     bullets.update()
     for bullet in bullets.copy():
            if bullet.rect.bottom <=0:
               bullets.remove(bullet)
               # print(len(bullets))
     collisions=pygame.sprite.groupcollide(bullets,aliens,False,True)
     if len(aliens) == 0:
          bullets.empty()
          ai_settings.increase_speed()
          create_fleet(ai_settings,screen,ship,aliens)

   

def  get_number_aliens_x(ai_settings,alien_width):
          numberof_avail_space=ai_settings.screen_width - alien_width
          numberof_aliens=int(numberof_avail_space/(2*alien_width))
          return numberof_aliens
def get_number_rows(ai_settings,ship_height,alien_height):
     avail_space_y=(ai_settings.screen_height-alien_height-ship_height)

     number_rows=int(avail_space_y/(2*alien_height))
     return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
     alien =Alien(ai_settings,screen)
     alien_width=alien.rect.width
     alien.x=alien_width+2*alien_width*alien_number
     alien.rect.x=alien.x
     alien.rect.y=alien.rect.height+alien.rect.height * row_number
     aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
     alien =Alien(ai_settings,screen)
     number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
     number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

     for row_number in range(number_rows):
          for alien_number in range(number_aliens_x):
               create_alien(ai_settings,screen,aliens,alien_number,row_number)
         
def check_fleet_edges(ai_settings,aliens):
     for alien in aliens.sprites():
          if alien.check_edges():
               change_fleet_direction(ai_settings,aliens)
               break

def change_fleet_direction(ai_settings,aliens):
     for alien in aliens.sprites():
          alien.rect.y +=ai_settings.fleet_drop_speed
     ai_settings.alien_fleet_direction*=-1

def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
     check_fleet_edges(ai_settings,aliens)
     aliens.update()
     check_bottom_hit(ai_settings,stats,screen,ship,aliens,bullets)
     if pygame.sprite.spritecollideany(ship,aliens):
          ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
        

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
     if stats.ship_left > 0:
          stats.ship_left -=1
          aliens.empty()
          bullets.empty()
          create_fleet(ai_settings, screen, ship, aliens)
          ship.center_ship()
          sleep(0.5)

     else:
          stats.game_active=False
          pygame.mouse.set_visible(True)


def check_bottom_hit(ai_settings,stats,screen,ship,aliens,bullets):
     screen_rect=screen.get_rect()
     for alien in aliens.sprites():
          if alien.rect.bottom >= screen_rect.bottom:
               ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
               #break


def check_bullet_alien_collison(ai_settings,screen,stats,sb,ship,aliens,bullets):
     collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
     if collisions:
          for aliens in collisions.values():
               stats.score +=ai_settings.aliens_points * len(aliens)
               sb.prep_score()
