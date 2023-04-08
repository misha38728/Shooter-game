from pygame import *
from random import randint
win_width = 1920
win_height = 768
score = 0
lost = 0
max_lost = 10
enemy1 = 10
hp = 100
boss_life = 100
make = 0
made = 0
score2 = 0

WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect() 
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed     
        if keys[K_d] and self.rect.x < win_width -80:
            self.rect.x += self.speed 

    def fire(self):
        bullet = Bullet("Bullet.png", self.rect.centerx - 50, self.rect.top, 100, 5, 20)
        bullets.add(bullet)


bullets = sprite.Group()
bullets_boss = sprite.Group()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Boss(GameSprite):
    def update(self):
        if self.rect.x > 1260:
            self.direction = 'left'
            #self.rect.x -= self.speed
        elif self.rect.x < 100 :
            self.direction = 'right'
            #self.rect.x += self.speed
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

        global hp
        if hp <= 0:
            self.kill()
        
    def fire(self):
        bullet = Bullet("Bullet.png", self.rect.centerx - 50, self.rect.bottom, 100, 5, -10)
        bullets_boss.add(bullet)
    
    def draw_boss(self, surf, pt):
        # global boss_life
        if pt < 0:
            pt = 0
        BAR_LENGTH_1 = 150
        BAR_HEIGHT_1 = 20
        fill_1 = (pt / 100) * BAR_LENGTH_1
        outline_rect_1 = Rect(self.rect.x-70/2, self.rect.y-25, BAR_LENGTH_1, BAR_HEIGHT_1)
        fill_rect_1 = Rect(self.rect.x-70/2, self.rect.y-25, fill_1, BAR_HEIGHT_1)
        draw.rect(surf, GREEN, fill_rect_1)
        draw.rect(surf, WHITE, outline_rect_1, 2)



class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0 or self.rect.y > 700:
            self.kill()
    def update_boss(self):
        self.rect.y -= self.speed
        if self.rect.y > 766:
            self.kill()

font.init()
font2 = font.SysFont('Arial', 36)
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
sound = mixer.Sound('fire.ogg')

background = transform.scale(image.load("galaxy.jpg"), (win_width,win_height))

ship = Player("rocket.png", 5, win_height -100, 80, 100, 20)
enemy_boss = Boss("asteroid.png", 1268, 100, 100, 100, 5)

monsters = sprite.Group()  
for i in range(enemy1):
    monster = Enemy("ufo.png", randint(80, win_width), -40, 80, 50, randint(1, 3))
    monsters.add(monster)

sprites_list = sprite.groupcollide(monsters, bullets, True, True )
#sprite_list = sprite_groupcollide(enemy_boss, bullets, True, True)

window = display.set_mode((0,0), FULLSCREEN)
display.set_caption("Шутер")


enemies = 0
finish = False
game = True
win = font2.render("You win!!!!" , 1, (0,255,0))
lose = font2.render("You lose!!!!" , 1, (255,0,0))
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                sound.play()
                ship.fire()
            elif e.key == K_ESCAPE:
                game = False
           
    if not finish:
        window.blit(background, ((0,0)))
        text = font2.render("Счет: " + str(score), 1, (225,255,255))
        window.blit(text, (10, 50))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 80))
        monsters.update()
        monsters.draw(window)
        sprites_list = sprite.groupcollide(monsters, bullets, True, True )
        for i in sprites_list:
            monster = Enemy("ufo.png", randint(80, win_width), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            score += 1
            enemies += 1
            score2 = score2 + 1 
            if score2 >= 15:
                make = True
                if make == True:
                    enemy_boss = Boss("asteroid.png", 1268, 100, 100, 100, 15)
                    make == False
                    made = 1
                    score2 = 0
                    for i in monsters:
                        i.kill()

        if score >= 60:
            finish = True
            window.blit(win, (win_width/2-50, win_height/2))

        if lost >= max_lost:
            finish = True
            window.blit(lose, (win_width/2-50, win_height/2))
            
        if enemies >= enemy1:
            monster = Enemy("ufo.png", randint(80, win_width), -40, 80, 50, 10)
            monsters.add(monster)
            enemies = 0

        ship.update()
        ship.reset()

        bullets.update()
        bullets.draw(window)
        if made == 1:
            enemy_boss.update()
            enemy_boss.reset()
            bullets_boss.draw(window)
            bullets_boss.update()
            enemy_boss.draw_boss(window, boss_life)
            if len(bullets_boss) < 6:
                enemy_boss.fire()
            if sprite.spritecollide(enemy_boss, bullets, True):
                hp -= 1
                boss_life -= 1
                if hp <= 0:
                    enemy_boss.kill()
                    made = 0
                print(hp)
            if sprite.spritecollide(ship, bullets_boss, False):
                finish = True
                aaa = font2.render('Вы проиграли!', True, GREEN)
                window.blit(aaa, (win_width/2-50, win_height/2))


                    

    # else:
    #     finish = True
    #     score = 0
    #     lost = 0 
    #     for b in bullets:
    #         b.kill()
    #     for m in monsters:
    #         m.kill()
    #     time.delay(300)
    #     for i in range(enemy1):
    #         monster = Enemy("ufo.png", randint(80, win_width), -40, 80, 50, randint(1, 3))
    #         monsters.add(monster)

        display.update()






























