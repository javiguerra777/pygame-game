import pygame
from sprites import *
from config import *
import sys
"""
photo reference credits go to:
 https://www.bing.com/images/search?view=detailV2&ccid=bqugMG19&id=5A6A5F8A10E14BFB4DE59F07090ED1A578DBE8F0&thid=OIP.bqugMG197guOGd75vDBXhAHaHa&mediaurl=https%3a%2f%2fwallpapercave.com%2fwp%2fwp2561090.png&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.6eaba0306d7dee0b8e19def9bc305784%3frik%3d8OjbeKXRDgkHnw%26pid%3dImgRaw%26r%3d0&exph=1080&expw=1080&q=Simple+Background&simid=608006338285549238&FORM=IRPRST&ck=B228693C8C4DDAF08A065642D96F65BD&selectedIndex=5&ajaxhist=0&ajaxserp=0 
 for their background photo in the title page 
 https://wallpapercave.com/dwp1x/X1EOqAY.png for their background photo in the game over screen
 """

class Game:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    self.clock = pygame.time.Clock()
    self.running = True
    self.font = pygame.font.Font(None, 32)
    self.intro_background = pygame.image.load('./img/bckimg.png')
    self.go_background = pygame.image.load('./img/goimg.png')
    self.state = "overworld"


  def createTilemap(self):
      for i, row in enumerate(tilemap):
        for j, column in enumerate(row):
          if column == "B":
            Block(self, j, i)
          if column == "P":
            Player(self, j, i, 100,["jump", "hammer", "heal", "run"])
          if column == "E":
            Enemy(self, j, i, 30, ["attack", "defend"])
      
  def new(self):
    # a new game starts
    self.playing = True
    self.all_sprites = pygame.sprite.LayeredUpdates()
    self.blocks = pygame.sprite.LayeredUpdates()
    self.enemies = pygame.sprite.LayeredUpdates()
    self.attacks = pygame.sprite.LayeredUpdates()
    self.createTilemap()
    

  def events(self):
    # game loop events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.playing = False
        self.running = False

  def update(self):
    self.all_sprites.update()

  def draw(self):
    self.screen.fill(BLACK)
    self.all_sprites.draw(self.screen)
    self.clock.tick(FPS)
    pygame.display.update()

  def main(self):
    # game loop
    while self.playing:
      self.events()
      self.update()
      self.draw()
  def fight(self):
    print('fight')
    continue_button = Button(10, WIN_HEIGHT -60, 120, 50, BLACK, WHITE, 'Continue Game', 32)
    for sprite in self.all_sprites:
      sprite.kill()
    while self.running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
      mouse_pos = pygame.mouse.get_pos()
      mouse_pressed = pygame.mouse.get_pressed()

      if continue_button.is_pressed(mouse_pos, mouse_pressed):
        self.new()
        self.main()
      self.screen.fill(BLACK)
      self.screen.blit(continue_button.image, continue_button.rect)
      self.clock.tick(FPS)
      pygame.display.update()

  def game_over(self):
    restart_button = Button(10, WIN_HEIGHT -60, 120, 50, BLACK, WHITE, 'Start Over', 32)
    for sprite in self.all_sprites:
      sprite.kill()
    while self.running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
      mouse_pos = pygame.mouse.get_pos()
      mouse_pressed = pygame.mouse.get_pressed()

      if restart_button.is_pressed(mouse_pos, mouse_pressed):
        self.new()
        self.main()
      self.screen.blit(self.go_background, (0,0))
      self.screen.blit(restart_button.image, restart_button.rect)
      self.clock.tick(FPS)
      pygame.display.update()

  def intro_screen(self):
    intro = True
    title = self.font.render('JRPG Game', True, BLACK)
    title_rect = title.get_rect(x=10,y=10)

    play_button = Button(10,50,100,50, WHITE, BLACK, 'Play', 32)

    while intro:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          intro = False
          self.running = False
      mouse_pos = pygame.mouse.get_pos()
      mouse_pressed = pygame.mouse.get_pressed()

      if play_button.is_pressed(mouse_pos, mouse_pressed):
        intro = False

      self.screen.blit(self.intro_background, (0,0))
      self.screen.blit(title, title_rect)
      self.screen.blit(play_button.image, play_button.rect)
      self.clock.tick(FPS)
      pygame.display.update()

g = Game()
g.intro_screen()
g.new()
while g.running:
  g.main()
  g.fight()
  g.game_over()

pygame.quit()
sys.exit()