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
import pygame, random, math

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


# class player defini
class Player(pygame.sprite.Sprite):
	def __init__(self):  # init
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(
			path.join(assets_dir, "player.png")).convert().convert_alpha()  # load the image of the player
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2  # on the start of the game center the player at the middle
		self.rect.bottom = HEIGHT - 10  # on the start of the game align the player at the bottom of the screen and give 10px of margin
		self.speedX = 0  # define the speed X to 0
		self.speedY = 0  # define the speed Y to 0

	def shoot(self):
		# on transmet la position du vaisseau au missile ainsi que sa vitesse
		# puis on crée l'instance et l'ajoute au groupe de sprites pour qu'il s'affiche
		positionX = self.rect.centerx  # get the X pos of the player
		positionY = self.rect.top  # same but Y
		missile = Missile(positionX, positionY,
		                  0)  # call the class missile and define it position at the same place of the player, the 0 define a player bullet.
		all_sprites.add(missile)  # add the bullet to the sprite
		all_player.add(missile)

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


# class ennemys / mobs
class ennemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(
			path.join(assets_dir, "enemy.png")).convert().convert_alpha()  # define the image of the mob
		self.rect = self.image.get_rect()
		self.positionx = random.randrange(0, WIDTH - self.rect.width)
		# On choisit une position x alÃ©atoire entre le cÃ´tÃ© gauche de l'Ã©cran et le cÃ´tÃ© droit - la largeur du vaisseau
		self.rect.x = self.positionx
		# On choisit une position y alÃ©atoire entre 100 pixels au dessus de l'Ã©cran et le haut de l'Ã©cran - la hauteur du vaisseau
		self.rect.y = random.randrange(-100, 0 - self.rect.height)
		# On donne une vitesse alÃ©atoire au vaisseau
		self.speedY = random.randrange(2, 5)

		self.randtimer = random.randint(100, 200)  # define the number of cycle to shot bullet on the player
		self.timer = 0  # define the timer to 0

		# Vague sinusoidale
		self.amplitude = 32
		self.frequence = 0.01

	def shoot(self):
		# on transmet la position du vaisseau au missile ainsi que sa vitesse
		# puis on crée l'instance et l'ajoute au groupe de sprites pour qu'il s'affiche
		positionX = self.rect.centerx
		positionY = self.rect.top
		missile = Missile(positionX, positionY, 1)
		all_sprites.add(missile)
		all_missile.add(missile)

	def update(self):
		pygame.sprite.Sprite.update(self)

		# On bouge le vaisseau en fonction de la vitesse
		self.rect.y += self.speedY
		self.rect.x = self.positionx + math.sin(self.rect.y * self.frequence) * self.amplitude
		# On empÃªche l'ennemy de sortir de l'Ã©cran
		if self.rect.bottom > HEIGHT:
			self.rect.top = 0  # remettre l'ennemy en haut

			self.speedY = random.randrange(1, 5)
			self.speedX = math.sin(player.rect.x)

			self.rect.right = random.randint(1, WIDTH)

		self.timer += 1  # at eache cycle add 1

		if self.randtimer < self.timer:  # at each cycle if rand timer < timer continue to shoot, else stop
			self.shoot()
			self.timer = 0


class Missile(pygame.sprite.Sprite):

	def __init__(self, posX, posY, type):
		pygame.sprite.Sprite.__init__(self)

		if type == 0:  # if the arguments type is equal to 0
			type_missile = "player"  # define player
		elif type == 1:  # else define ennemy
			type_missile = "enemy"

		self.image = pygame.image.load(
			path.join(assets_dir,
			          "missile_" + type_missile + ".png")).convert().convert_alpha()  # load the image of a bullet
		self.rect = self.image.get_rect()
		self.rect.centerx = posX  # define the pos of the bullet as the pos of the argument
		self.rect.y = posY  # same

		if type == 0:  # if type 0 define to go to the top
			self.speedY = -2
		elif type == 1:  # else go to the down (ennemies bullets)
			self.speedY = 2

	def update(self):
		pygame.sprite.Sprite.update(self)
		self.rect.y += self.speedY
		if self.rect.top < 0:  # if bullet is outside
			self.kill()  # kill the bullet


		if self.rect.bottom > HEIGHT:
			self.kill()

def AABBCollision(rectA, rectB):
	if rectA.rect.right > rectB.rect.left and rectA.rect.left < rectB.rect.right and rectA.rect.bottom > rectB.rect.top and rectA.rect.top < rectB.rect.bottom:
		return True
	else:
		return False

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # resolution of the screen
pygame.display.set_caption("PyGame")  # name of the program
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
all_missile = pygame.sprite.Group()
all_player = pygame.sprite.Group()

#  display 10 ennemies on the screen
for i in range(10):
	ennemy1 = ennemy()
	all_sprites.add(ennemy1)
	all_enemies.add(ennemy1)

# display the player (add into sprites)
player = Player()
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


	screen.fill(BLACK)
	all_sprites.draw(screen)

	# Une fois que tout est dessiné, on l'affiche à l'écran
	pygame.display.flip()

# Quand on sort de la boucle, on ferme le jeu
pygame.quit()
