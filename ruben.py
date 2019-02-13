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
#       Name of the file : ruben ~ Name of the project : pygame
#       Created By : rodet the 13/02/2019 - 15:48
#       Email : romain.odet@lecole-ldlc.com
#
#       Last edit by : rodet the 13/02/19 at 15:48

from os import path
import pygame, random

assets_dir = path.join(path.dirname(__file__), 'assets')

WIDTH = 400
HEIGHT = 600
FPS = 60

# On définit des couleurs à utiliser plus tard
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(assets_dir, "player.png")).convert().convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedX = 0
        self.speedY = 0

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def shoot(self):
        # on transmet la position du vaisseau au missile ainsi que sa vitesse
        # puis on crée l'instance et l'ajoute au groupe de sprites pour qu'il s'affiche
        positionX = self.rect.centerx
        positionY = self.rect.top
        missile = Missile(positionX, positionY)
        all_sprites.add(missile)

    def update(self):
        pygame.sprite.Sprite.update(self)

        # On récupère toutes les touches pressées à cette frame
        keys_pressed = pygame.key.get_pressed()

        # La vitesse est remise à 0 à chaque frame, sauf si on appuie sur la flèche gauche ou la flèche droite
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

        # On empêche le vaisseau de sortir de l'écran
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

class ennemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(path.join(assets_dir, "enemy.png")).convert().convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.right = random.randrange(1,10)
		self.rect.top = 0
		self.speedY = random.randrange(3,5)

	def update(self):
		pygame.sprite.Sprite.update(self)

		# On bouge le vaisseau en fonction de la vitesse
		self.rect.y += self.speedY

		# On empÃªche l'ennemy de sortir de l'Ã©cran
		if self.rect.bottom > HEIGHT:
			self.rect.top = 0 # remettre l'ennemy en haut

			self.speedY = random.randrange(1, 5)

			self.rect.right = random.randint(1, WIDTH)

class Missile(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        type_missile = "player"
        self.image = pygame.image.load(path.join(assets_dir, "missile_" + type_missile + ".png")).convert().convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = posX
        self.rect.y = posY + 10
        self.speedY = -2
    def update(self):
        pygame.sprite.Sprite.update(self)
        self.rect.y += self.speedY



pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGame")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
# On crée une instance de la classe Player
player = Player()
# ... et on l'ajoute au groupe de sprites
for i in range (10):
	ennemy1 = ennemy()

	all_sprites.add(ennemy1)
all_sprites.add(player)

running = True
while running:
    # On fixe le jeu à 60 FPS
    clock.tick(FPS)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Tous les sprites sont updatés
    all_sprites.update()
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Une fois que tout est dessiné, on l'affiche à l'écran
    pygame.display.flip()

# Quand on sort de la boucle, on ferme le jeu
pygame.quit()