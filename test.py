#                 /
#    |      /  |////:  o////  ./////    s`      y////-
#    |         |       /      s-    s.  h`      h
#    |         |////.  /      s-    s-  h`      d////`
#    |         |       /      s-    s.  h`      h
#    |////     |////:  o/::/  -o/::/o   y////.  d////-
#
#        -mmmmm.   ymmmmmmmmmy-   ymmmm-       -ymmmmmm
#        -mmmmm.   ymmmm+ohmmmm-  ymmmm-     :mmmmdo/+s
#        -mmmmm.   ymmm     hmmmo ymmmm-    hmmmm:
#        -mmmmm:   hmmm     mmmm/ ymmmm/    ymmmmy:
#        -mmmmmmmmmmmmmmmmmmmms   ymmmmmmmm  dommmmmmmm
#        -hhhhhhhhhhhhhhhhys+/    shhhhhhhhy  ./shddhh/
#
#       Name of the file : test ~ Name of the project : Pygame
#       Created By : rodet the 08/02/2019 - 09:36
#       Email : romain.odet@lecole-ldlc.com
#
#       Last edit by : rodet the 08/02/19 at 09:36
import pygame
import math
import random
from os import path

# On dÃ©finit les variables concernant notre jeu
WIDTH = 400
HEIGHT = 600
FPS = 60

# On dÃ©finit des couleurs Ã  utiliser plus tard
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

diff = False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        assets_dir = path.join(path.dirname(__file__), 'assets')
        self.image = pygame.image.load(path.join(assets_dir, "player.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedX = 0
        self.speedY = 0




    def Shoot(self):
        posX = self.rect.centerx
        posY = self.rect.top-15
        missile = Missile(posX, posY, True)
        all_sprites.add(missile)
        all_player.add(missile)

    def update(self):
        pygame.sprite.Sprite.update(self)

        # On rÃ©cupÃ¨re toutes les touches pressÃ©es Ã  cette frame
        keys_pressed = pygame.key.get_pressed()

        # La vitesse est remise Ã  0 Ã  chaque frame, sauf si on appuie sur la flÃ¨che gauche ou la flÃ¨che droite
        self.speedX = 0
        self.speedY = 0
        if keys_pressed[pygame.K_LEFT]:
            self.speedX = -5
        if keys_pressed[pygame.K_RIGHT]:
            self.speedX = 5
        if keys_pressed[pygame.K_UP]:
            self.speedY = -5
        if keys_pressed[pygame.K_DOWN]:
            self.speedY = 5



        # On bouge le vaisseau en fonction de la vitesse
        self.rect.x += self.speedX
        self.rect.y += self.speedY
        # On empÃªche le vaisseau de sortir de l'Ã©cran
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect()
        self.posiX = random.randrange(0, WIDTH - self.rect.width)
        self.rect.x = self.posiX
        self.rect.bottom = 0
        self.speedX = 0
        self.speedY = random.randrange(1, 4)
        assets_dir = path.join(path.dirname(__file__), 'assets')
        self.image = pygame.image.load(path.join(assets_dir, "enemy.png")).convert()
        self.image.set_colorkey(BLACK)
        self.timer = 0
        self.randomTimer = random.randrange (50, 300)

        # Vague sinusoidale
        self.amplitude = 32
        self.frequence = 0.01


    def Shoot(self):
        posX = self.rect.centerx+4
        posY = self.rect.top+15
        missile = Missile(posX, posY, False)
        all_sprites.add(missile)
        all_missile.add(missile)


    def update(self):
        pygame.sprite.Sprite.update(self)
        # On bouge le vaisseau en fonction de la vitesse

        self.rect.y += self.speedY

        self.rect.x = self.posiX + math.sin(self.rect.y * self.frequence) * self.amplitude



        # On empÃªche le vaisseau de sortir de l'Ã©cran
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0

        self.timer +=1
        if self.timer > self.randomTimer:
            diff = False
            self.Shoot()
            self.timer = 0

        # Respawn

        if self.rect.bottom > HEIGHT +100 :
            self.rect.y = random.randrange(-100, 0 - self.rect.height)
            self.speedY = random.randrange(1, 4)
            self.posiX = random.randrange(0, WIDTH - self.rect.width)
            self.rect.x = self.posiX

class Missile(pygame.sprite.Sprite):
    def __init__(self, positionX, positionY, IsPlayer):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((4, 8))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = positionX
        self.rect.top = positionY
        assets_dir = path.join(path.dirname(__file__), 'assets')
        self.image = pygame.image.load(path.join(assets_dir, "missile_player.png")).convert()
        self.image.set_colorkey(BLACK)
        if IsPlayer == True:
            self.speedY = -8
            assets_dir = path.join(path.dirname(__file__), 'assets')
            self.image = pygame.image.load(path.join(assets_dir, "missile_player.png")).convert()

        if IsPlayer == False:
            self.speedY = 5
            assets_dir = path.join(path.dirname(__file__), 'assets')
            self.image = pygame.image.load(path.join(assets_dir, "missile_enemy.png")).convert()

    def update(self):
        pygame.sprite.Sprite.update(self)
        # On bouge le missile en fonction de la vitesse
        self.rect.y += self.speedY
        # On laisse le missile de sortir de l'Ã©cran et on le dÃ©truit
        if self.rect.top < 0:
            self.kill()

        if self.rect.bottom > HEIGHT:
            self.kill()


def AABBCollision(rectA, rectB):
    if rectA.rect.right > rectB.rect.left and rectA.rect.left < rectB.rect.right and rectA.rect.bottom > rectB.rect.top and rectA.rect.top < rectB.rect.bottom:
        return True
    else:
        return False

# On initialise pygame et on crÃ©e la fenÃªtre grÃ¢ce aux variables WIDTH et HEIGHT
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGame")
clock = pygame.time.Clock()

# On crÃ©e un groupe pour les sprites
all_sprites = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
all_missile = pygame.sprite.Group()
all_player = pygame.sprite.Group()

# On crÃ©e une instance de la classe Player
player = Player()


# ... et on l'ajoute au groupe de sprites
all_sprites.add(player)

for loop in range(10):
    ennemy = Enemy()
    all_sprites.add(ennemy)
    all_enemies.add(ennemy)
# Tant que le jeu tourne
running = True
while running:
    # On fixe le jeu Ã  60 FPS
    clock.tick(FPS)
    diff = False
    # RÃ©cupÃ©ration des inputes
    for event in pygame.event.get():
        # Pour fermer la fenÃªtre, on arrÃªte la boucle while
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                diff = True
                player.Shoot()


    # Tous les sprites sont updatÃ©s
    all_sprites.update()

    for ennemy in all_enemies:
        if AABBCollision(player, ennemy) == True:
            player.kill()
            running = False

    for missile in all_missile:
        if AABBCollision(player, missile) == True:
            player.kill()
            running = False

    for missile in all_player:
        for ennemy in all_enemies:
            if AABBCollision(missile, ennemy) == True:
                ennemy.kill()

    # Tous les sprites sont dessinÃ©s
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Une fois que tout est dessinÃ©, on l'affiche Ã  l'Ã©cran
    pygame.display.flip()

# Quand on sort de la boucle, on ferme le jeu
pygame.quit()