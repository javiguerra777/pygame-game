import pygame
from config import *
import math
import random

class Player(pygame.sprite.Sprite):
  def __init__(self, game, x, y, hp, moves):
    self.game = game
    self._layer = PLAYER_LAYER
    self.groups = self.game.all_sprites
    pygame.sprite.Sprite.__init__(self, self.groups)

    self.x = x * TILE_SIZE
    self.y = y * TILE_SIZE
    self.width = TILE_SIZE
    self.height = TILE_SIZE
    self.hp = hp
    self.moves = moves

    self.x_change = 0
    self.y_change = 0
    self.facing = 'down'

    self.image = pygame.Surface([self.width, self.height])
    self.image.fill(RED)

    self.rect = self.image.get_rect()
    self.rect.x = self.x
    self.rect.y = self.y
  
  def update(self):
    self.movement()
    self.collide_enemy()

    self.rect.x += self.x_change
    self.collide_blocks('x')
    self.rect.y += self.y_change
    self.collide_blocks('y')

    self.x_change = 0
    self.y_change = 0

  def movement(self):
    keys = pygame.key.get_pressed()
    if(keys[pygame.K_LEFT] and self.game.state == "overworld"):
      self.x_change -= PLAYER_SPEED
      self.facing = 'left'
    if(keys[pygame.K_RIGHT] and self.game.state == "overworld"):
      self.x_change += PLAYER_SPEED
      self.facing = 'right'
    if(keys[pygame.K_UP] and self.game.state == "overworld"):
      self.y_change -= PLAYER_SPEED
      self.facing = 'up'
    if(keys[pygame.K_DOWN] and self.game.state == "overworld"):
      self.y_change += PLAYER_SPEED
      self.facing = 'down'

  def collide_enemy(self):
    hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
    if hits:
      self.game.playing = False
      # self.hp -= 5
      # print(self.hp)
      if self.hp <= 0:
        self.kill
        self.game.playing = False
      
     
  def collide_blocks(self, direction):
    if direction == "x":
      hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
      if hits:
        if self.x_change > 0:
          self.rect.x = hits[0].rect.left - self.rect.width
        if self.x_change < 0:
          self.rect.x = hits[0].rect.right
    if direction == "y":
      hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
      if hits:
        if self.y_change > 0:
          self.rect.y = hits[0].rect.top - self.rect.height
        if self.y_change < 0:
          self.rect.y = hits[0].rect.bottom

class Enemy(pygame.sprite.Sprite):
  def __init__(self, game, x, y, hp, attacks):
    self.game = game
    self._layer = ENEMY_LAYER
    self.groups = self.game.all_sprites, self.game.enemies
    pygame.sprite.Sprite.__init__(self, self.groups)

    self.x = x * TILE_SIZE
    self.y = y * TILE_SIZE
    self.width = TILE_SIZE
    self.height = TILE_SIZE
    self.hp = hp
    self.attacks = attacks

    self.x_change = 0
    self.y_change = 0

    self.facing = random.choice(['left', 'right'])
    self.animation_loop = 1
    self.movement_loop = 0
    self.max_travel = random.randint(7,30)

    self.image = pygame.Surface([self.width, self.height])
    self.image.fill(ORANGE)

    self.rect = self.image.get_rect()
    self.rect.x = self.x
    self.rect.y = self.y

  def update(self):
    self.movement()
    self.rect.x += self.x_change
    self.rect.y += self.y_change

    self.x_change = 0
    self.y_change = 0

  def movement(self):
    if self.facing == 'left':
      self.x_change -= ENEMY_SPEED
      self.movement_loop -= 1
      if self.movement_loop <= -self.max_travel:
        self.facing = 'right'
    if self.facing == 'right':
      self.x_change += ENEMY_SPEED
      self.movement_loop += 1
      if self.movement_loop >= self.max_travel:
        self.facing = 'left'

class Block(pygame.sprite.Sprite):
  def __init__(self, game, x, y):
    self.game = game
    self._layer = BLOCK_LAYER
    self.groups = self.game.all_sprites, self.game.blocks
    pygame.sprite.Sprite.__init__(self, self.groups)

    self.x = x * TILE_SIZE
    self.y = y * TILE_SIZE
    self.width = TILE_SIZE
    self.height = TILE_SIZE

    self.image = pygame.Surface([self.width, self.height])
    self.image.fill(BLUE)

    self.rect = self.image.get_rect()
    self.rect.x = self.x
    self.rect.y = self.y
class Button:
  def __init__(self, x, y, width, height, fg, bg, content, fontsize):
    self.font = pygame.font.Font(None, fontsize)
    self.content = content

    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.fg = fg
    self.bg = bg

    self.image = pygame.Surface((self.width, self.height))
    self.image.fill(self.bg)
    self.rect = self.image.get_rect()

    self.rect.x = self.x
    self.rect.y = self.y

    self.text = self.font.render(self.content, True, self.fg)
    self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
    self.image.blit(self.text, self.text_rect)


  def is_pressed(self, pos, pressed):
    if self.rect.collidepoint(pos):
      if pressed[0]:
        return True
      return False
    return False