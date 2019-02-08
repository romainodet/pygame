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

# PyGame LDLC
import pygame
import random

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


class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((32, 64))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.speedX = 0

	def update(self):
		pygame.sprite.Sprite.update(self)

		# On rÃ©cupÃ¨re toutes les touches pressÃ©es Ã  cette frame
		keys_pressed = pygame.key.get_pressed()

		# La vitesse est remise Ã  0 Ã  chaque frame, sauf si on appuie sur la flÃ¨che gauche ou la flÃ¨che droite
		self.speedX = 0
		if keys_pressed[pygame.K_LEFT]:
			self.speedX = -5
		if keys_pressed[pygame.K_RIGHT]:
			self.speedX = 5

		# On bouge le vaisseau en fonction de la vitesse
		self.rect.x += self.speedX

		# On empÃªche le vaisseau de sortir de l'Ã©cran
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

		# La vitesse est remise Ã  0 Ã  chaque frame, sauf si on appuie sur la flÃ¨che gauche ou la flÃ¨che droite
		self.speedY = 0
		if keys_pressed[pygame.K_UP]:
			self.speedY = -5
		if keys_pressed[pygame.K_DOWN]:
			self.speedY = 5

		# On bouge le vaisseau en fonction de la vitesse
		self.rect.y += self.speedY

		# On empÃªche le vaisseau de sortir de l'Ã©cran
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT
		if self.rect.top < 0:
			self.rect.top = 0


# On initialise pygame et on crÃ©e la fenÃªtre grÃ¢ce aux variables WIDTH et HEIGHT
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hello World")
clock = pygame.time.Clock()

# On crÃ©e un groupe pour les sprites
all_sprites = pygame.sprite.Group()

# On crÃ©e une instance de la classe Player
player = Player()
# ... et on l'ajoute au groupe de sprites
all_sprites.add(player)

# Tant que le jeu tourne
running = True
while running:
	# On fixe le jeu Ã  60 FPS
	clock.tick(FPS)

	# RÃ©cupÃ©ration des inputes
	for event in pygame.event.get():
		# Pour fermer la fenÃªtre, on arrÃªte la boucle while
		if event.type == pygame.QUIT:
			running = False

	# Tous les sprites sont updatÃ©s
	all_sprites.update()

	# Tous les sprites sont dessinÃ©s
	screen.fill(BLACK)
	all_sprites.draw(screen)

	# Une fois que tout est dessinÃ©, on l'affiche Ã  l'Ã©cran
	pygame.display.flip()

# Quand on sort de la boucle, on ferme le jeu
pygame.quit()
