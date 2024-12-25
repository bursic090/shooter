import pygame
import random

pygame.init()
font1 = pygame.font.SysFont('Arial', 36)  

window = pygame.display.set_mode((700, 500))
pygame.display.set_caption('Шутер')
background = pygame.transform.scale(pygame.image.load('galaxy.jpg'), (700, 500))

pygame.mixer.init()
pygame.mixer.music.load('space.ogg')
pygame.mixer.music.play(-1) 

lost = 0
score = 0
max_lost = 5
win_score = 10

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.rect.x < 595:
            self.rect.x += self.speed
        if keys[pygame.K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 5)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.rect.y = -50 

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -50
            self.rect.x = random.randint(10, 690)
            global lost
            lost += 1

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.rect.x = player_x
        self.rect.y = player_y
    def update(self):
        self.rect.y -= self.speed  
        if self.rect.bottom < 0:  
            self.kill()

rocket = Player('rocket.png', 5, 420, 4)

enemies = pygame.sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', random.randint(10, 690), -50, 2)
    enemies.add(enemy)




bullets = pygame.sprite.Group()

game = True
clock = pygame.time.Clock()
FPS = 60

while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                rocket.fire()

    window.blit(background, (0, 0))

    enemies.update()
    enemies.draw(window)

    bullets.update()
    bullets.draw(window)

    rocket.update()
    rocket.reset()


    collisions = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for collision in collisions:
        score += 1
        enemy = Enemy('ufo.png', random.randint(10, 690), -50, 2)
        enemies.add(enemy)

    if pygame.sprite.spritecollide(rocket, enemies, True):
      game= False
      window.fill((0, 0, 0))
      font2 = pygame.font.SysFont('Arial', 100) 
      text_over = font2.render("Game Over", True, (255, 0, 0))
      window.blit(text_over, (170, 200))
      pygame.display.update()
      pygame.time.wait(1500)
      
    if lost >= max_lost:
      game= False
      window.fill((0, 0, 0))
      font2 = pygame.font.SysFont('Arial', 100) 
      text_lose = font2.render("You Lost", True, (255, 0, 0))
      window.blit(text_lose, (170, 200))
      pygame.display.update()
      pygame.time.wait(1500)

    if score >= win_score:
       game = False
       window.fill((0, 0, 0))
       font2 = pygame.font.SysFont('Arial', 100) 
       text_win = font2.render("You Win", True, (0, 255, 0))
       window.blit(text_win, (170, 200))
       pygame.display.update()
       pygame.time.wait(1500)
      

    text_lose = font1.render('Пропущено: ' + str(lost), True, (255, 255, 255))
    text_score = font1.render("Счёт: " + str(score), True, (255, 255, 255))
    window.blit(text_lose, (10, 10)) 
    window.blit(text_score, (10, 40))
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()



