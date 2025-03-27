import pygame, sys
from pygame.locals import *
import random, time
 
pygame.init()
 
FPS = 60
FramePerSec = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

COINS = 0


# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Screen information
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1200

# Entities
ENTITY_WIDTH = 120
ENTITY_HEIGHT = 240

PLAYER_SPEED = 10
ENEMY_SPEED = 10
COIN_SPEED = 15

COIN_WIDTH = 40
COIN_HEIGHT = 40
COIN_SPAWN_INTERVAL = 200
COIN_LIMIT_FOR_SPEED = 5

SPEEDED = False


DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("assets/Coin.png")
        self.image = pygame.transform.scale(self.image, (COIN_WIDTH, COIN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(COIN_WIDTH//2,SCREEN_WIDTH-COIN_WIDTH//2),0) 
    
    def move(self):
        self.rect.move_ip(0,COIN_SPEED)
        if (self.rect.bottom > SCREEN_HEIGHT+COIN_HEIGHT):
            self.rect.top = 0
            self.rect.center = (random.randint(COIN_WIDTH//2,SCREEN_WIDTH-COIN_WIDTH//2), -(COIN_SPEED * COIN_SPAWN_INTERVAL))

    def collide(self):
        self.rect.center = (random.randint(COIN_WIDTH//2,SCREEN_WIDTH-ENTITY_WIDTH//2), -(COIN_SPEED * COIN_SPAWN_INTERVAL))

    def draw(self, surface):
        surface.blit(self.image, self.rect) 
    
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("assets/Enemy.png")
        self.image = pygame.transform.scale(self.image, (ENTITY_WIDTH, ENTITY_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(ENTITY_WIDTH//2,SCREEN_WIDTH-ENTITY_WIDTH//2),0) 
 
      def move(self):
        self.rect.move_ip(0,ENEMY_SPEED)
        if (self.rect.bottom > SCREEN_HEIGHT+ENTITY_HEIGHT):
            self.rect.top = 0
            self.rect.center = (random.randint(ENTITY_WIDTH//2,SCREEN_WIDTH-ENTITY_WIDTH//2), -ENTITY_HEIGHT)
 
      def draw(self, surface):
        surface.blit(self.image, self.rect) 
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("assets/Player.png")
        self.image = pygame.transform.scale(self.image, (ENTITY_WIDTH, ENTITY_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (ENTITY_WIDTH//2, SCREEN_HEIGHT-ENTITY_HEIGHT//2)
 
    def update(self):
        pressed_keys = pygame.key.get_pressed()
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-PLAYER_SPEED, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(PLAYER_SPEED, 0)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)     
 
         
P1 = Player()
E1 = Enemy()
C1 = Coin()

coins = pygame.sprite.Group()
coins.add(C1)
enemies = pygame.sprite.Group()
enemies.add(E1)
 
while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    P1.update()
    E1.move()
    C1.move()
     
    DISPLAYSURF.fill(WHITE)
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)
    C1.draw(DISPLAYSURF)

    if pygame.sprite.spritecollideany(P1, enemies):
        DISPLAYSURF.fill(RED)
        pygame.display.update()
        P1.kill()
        E1.kill()
        C1.kill()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    if pygame.sprite.spritecollideany(P1, coins):
        COINS += 1
        C1.collide()

    if COINS == COIN_LIMIT_FOR_SPEED and not SPEEDED:
        ENEMY_SPEED += 5
        SPEEDED = True

    coin_count_text = font.render(f"Coins: {COINS}", True, BLACK)
    DISPLAYSURF.blit(coin_count_text, (10, 10))
        
    pygame.display.update()
    FramePerSec.tick(FPS)