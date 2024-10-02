from pygame import *
from random import randint
from time import time as timer


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_w, player_h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_w, player_h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        
        if keys_pressed[K_s] and self.rect.y < height - 70:
            self.rect.y += self.speed

        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        
        if keys_pressed[K_d] and self.rect.x < width - 70:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > height:
            self.rect.x = randint(50, 1200)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()




font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 127)




enemys1 = sprite.Group()
enemys2 = sprite.Group()
enemys3 = sprite.Group()
boss_enemy = sprite.Group()
bullets = sprite.Group()
meteors = sprite.Group()





player = Player('player.png', 500, 500, 65, 65, 25)



for _ in range(1):
    enemy_1 = Enemy('enemy1.png', randint(50, 1200), -40, 50, 50, randint(3, 5))
    enemys1.add(enemy_1)

    enemy_2 = Enemy('enemy2.png', randint(50, 1200), -40, 50, 70, randint(3, 5))
    enemys2.add(enemy_2)

    enemy_3 = Enemy('enemy3.png', randint(50, 1200), -40, 50, 70, randint(3, 5))
    enemys3.add(enemy_3)

for _ in range(1):
    boss = Enemy('boss.png', randint(50, 1200), -40, 100, 100, randint(2, 5)) 
    boss_enemy.add(boss)

for _ in range(1):
    meteor = Enemy('meteor.png', randint(50, 1200), -40, 70, 70, randint(2, 6))
    meteors.add(meteor)




        


width = 1250
height = 650

window = display.set_mode((width, height))

display.set_caption('Шутер')

backgraund = transform.scale(image.load('back.jpg'), (width, height))

mixer.init()
mixer.music.load('fonk.mp3')
#mixer.music.play()

score = 0

num_fire = 0
rel_time = False



shot = mixer.Sound('shot.ogg')

clock = time.Clock()
FPS = 60

live = 3

finish = False
game = True

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False


        if e.type == KEYDOWN:
            if e.key == K_SPACE:

                if num_fire < 5 and rel_time == False:
                    player.fire()
                    num_fire += 1

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                
                    
                    
                    


    if not finish:
        window.blit(backgraund,(0, 0))

        text_lose = font1.render('Пропущенно: ' + str(lost), 1, (5, 250, 54))

        text_kill = font1.render('Уничтоженно: ' + str(score), 1, (252, 194, 3))

        window.blit(text_lose,(25, 25))

        window.blit(text_kill,(25, 75))

        enemys1.draw(window)

        enemys2.draw(window)

        enemys3.draw(window)

        boss_enemy.draw(window)

        meteors.draw(window)

        meteor.update()

        bullets.draw(window)

        player.reset()

        enemys1.update()

        enemys2.update()

        enemys3.update()

        player.update()

        boss.update()

        bullets.update()


        if rel_time == True:
            new_time = timer()
            if new_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (245, 15, 15))
                window.blit(reload,(500, 275))
            else:
                num_fire = 0
                rel_time = False



        collides1 = sprite.groupcollide(bullets, enemys1, True, True)
        collides2 = sprite.groupcollide(bullets, enemys2, True, True)
        collides3 = sprite.groupcollide(bullets, enemys3, True, True)
        collides4 = sprite.groupcollide(bullets, boss_enemy, True, True)


        for _ in collides1:
            score += 1
            enemy_1 = Enemy('enemy1.png', randint(50, 1200), -40, 50, 50, randint(3, 6))
            enemys1.add(enemy_1)
        for _ in collides2:
            score += 1
            enemy_2 = Enemy('enemy2.png', randint(50, 1200), -40, 50, 70, randint(3, 8))
            enemys2.add(enemy_2)
        for _ in collides3:
            score += 1
            enemy_3 = Enemy('enemy3.png', randint(50, 1200), -40, 50, 70, randint(3, 8))
            enemys3.add(enemy_3)
        for _ in collides4:
            score += 1
            boss = Enemy('boss.png', randint(50, 1200), -40, 100, 100, randint(3, 6)) 
            boss_enemy.add(boss)

        if sprite.spritecollide(player, enemys1, False) or sprite.spritecollide(player, enemys2, False) or sprite.spritecollide(player, enemys3, False) or sprite.spritecollide(player, boss_enemy, False) or sprite.spritecollide(player, meteors, False):
            sprite.spritecollide(player, enemys1, True)
            sprite.spritecollide(player, enemys2, True)
            sprite.spritecollide(player, enemys3, True)
            sprite.spritecollide(player, boss_enemy, True)
            sprite.spritecollide(player, meteors, True)
            live -= 1

        if live == 0 or lost > 3:


            loos = font1.render('YOU LOOSER!', True, (255, 215, 0))
            finish = True

            window.blit(loos, (500, 275))
            
        if score >= 10:
            win = font1.render('YOU WIN!', True, (255, 215, 0))
            finish = True
            
            window.blit(win, (500, 275))

        if live == 3:
            heart = transform.scale(image.load('heart3.jpg'), (30, 30))
            window.blit(heart, (500, 275))
        if live == 2:
            heart = transform.scale(image.load('heart2.jpg'), (30, 30))
            window.blit(heart, (500, 275))
        if live == 1:
            heart = transform.scale(image.load('heart1.jpg'), (30, 30))
            window.blit(heart, (500, 275))
        
        display.update()
    else:
        finish = False
        lost = 0
        score = 0
        live = 3
        num_fire = 0
        for b in bullets:
            b.kill()
        for enemy_1 in enemys1:
            enemy_1.kill()
        for enemy_2 in enemys2:
            enemy_2.kill() 
        for enemy_3 in enemys3:
            enemy_3.kill() 
        for boss in boss_enemy:
            boss.kill()
        for meteor in meteors:
            meteor.kill()
        clock.tick(60) 

        for _ in range(1):
            enemy_1 = Enemy('enemy1.png', randint(50, 1200), -40, 50, 50, randint(3, 5))
            enemys1.add(enemy_1)

            enemy_2 = Enemy('enemy2.png', randint(50, 1200), -40, 50, 70, randint(3, 5))
            enemys2.add(enemy_2)

            enemy_3 = Enemy('enemy3.png', randint(50, 1200), -40, 50, 70, randint(3, 5))
            enemys3.add(enemy_3)

        for _ in range(1):
            boss = Enemy('boss.png', randint(50, 1200), -40, 100, 100, randint(2, 5)) 
            boss_enemy.add(boss)
            
        for _ in range(1):
            meteor = Enemy('meteor.png', randint(50, 1200), -40, 70, 70, randint(2, 6))
            meteors.add(meteor)


    
    clock.tick(FPS)
