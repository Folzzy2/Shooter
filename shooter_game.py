
from pygame import *
from random import randint
from time import time as timer
mixer.init()
#mixer.music.load("space.ogg")
#mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial',80)
win = font1.render('You Win',True,(255,255,255))
lose = font1.render('You Lose',True,(255,255,255))
font2 = font.SysFont('Arial',36)
time1 = font1.render('Время не прошло',True,(255,255,255))

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_ast = "asteroid.png"
score = 0
lost = 0 
max_lost = 3
max_score = 10
life = 10
rel_time = False
num_fire = False
post = 0
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < win_height - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx,self.rect.top,15,20,15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_windth - 80)
            self.rect.y =0


class Bullet(GameSprite):
    def update(self):
        self.rect.y-=self.speed
        if self.rect.y < 0:
            self.kill()


win_windth = 700
win_height = 650
display.set_caption("Shooter")
window = display.set_mode((win_windth,win_height))
background = transform.scale(image.load(img_back),(win_windth,win_height))
ship = Player(img_hero,5,win_height - 100,80,100,10)
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy ,randint(80, win_windth - 80),-40,80,50,randint(1,5))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(1,3):
    asteroid= Enemy(img_ast,randint(80, win_windth - 80),-40,80,50,randint(1,5))
    asteroids.add(asteroid)
bullets = sprite.Group()



finish = False

game = False


run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()

                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    

    if not finish:
        text = font2.render("Счет:"+str(score),1,(255,255,255))
        window.blit(text,(10,50))
        text_lose = font2.render('Пропущено:'+ str(lost),1,(255,255,255))
    
        window.blit(text_lose,(10,50))
        window.blit(background,(0,0))
        ship.update() 
        monsters.update()
        ship.reset()
        asteroids.update()
        asteroids.draw(window)
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload1 = font2.render('Wait,reload,,,',1,(150,0,0))
                window.blit(reload1,(260,460))
            else:
                num_fire = 0 
                rel_time = False
        sprites_list = sprite.groupcollide(monsters,bullets,True,True)
        
        for c in sprites_list:
            score += 1
            monster = Enemy(img_enemy ,randint(80, win_windth - 80),-40,80,50,randint(1,5))
            monsters.add(monster)
        if score >= 10:
            window.blit(win,(200,200))
            finish = True
        if lost >= 3 or  sprite.spritecollide(ship,monsters, False) or sprite.spritecollide(ship,asteroids, False):
            window.blit(lose,(200,200))

            finish = True
        display.update()
    time.delay(50)