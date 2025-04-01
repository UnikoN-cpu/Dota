from pygame import*
from time import time as timer
import math
mixer.init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_x, player_y,w,h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    
    def reset(self):
        window.blit(self.image, self.rect)



class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 700 - 80:
            self.rect.y += self.speed

    def fire(self):
        mouse_x, mouse_y = mouse.get_pos()  
        bullet = Bullet(self.rect.centerx, self.rect.centery, mouse_x, mouse_y, 4)
        puli.add(bullet)


    
puli = sprite.Group()
            
font.init()
font2 = font.SysFont("Arial",30)
font1 = font.SysFont("Arial",70)
win = font1.render('YOU WIN', True, (0,255,0))
lose = font1.render('YOU LOSE', True, (255,0,0))
    
lost = 0
score = 0 
class Enemy(GameSprite):
    def update1(self):#M3
        if self.rect.x > 30:
            self.rect.x -= self.speed
        else:
            self.rect.y += self.speed
            global lost
        if self.rect.y > 550:
            self.rect.x = 550
            self.rect.y = 50
            lost = lost + 1


        
        

    def update2(self):#M2
        if self.rect.y < 550:
            self.rect.y += self.speed
        else:
            self.rect.x -= self.speed
            global lost
        if self.rect.x < 50:
            self.rect.x = 550
            self.rect.y = 50
            lost = lost + 1
        

    def update3(self):#m1
        self.rect.x -= self.speed
        self.rect.y += self.speed
        global lost
        if self.rect.y > 550:
            self.rect.x = 550
            self.rect.y = 50
            lost = lost + 1
    

class Bullet(GameSprite):
    def __init__(self, player_x, player_y, target_x, target_y, speed):
        super().__init__("паарп (1).png", player_x, player_y, 40, 40, speed)
        # Вычисление угла направления
        angle = math.atan2(target_y - player_y, target_x - player_x)
        # Разделение скорости на компоненты
        self.speed_x = math.cos(angle) * speed
        self.speed_y = math.sin(angle) * speed

    def update(self):
        # Движение пули
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Уничтожение пули, если она выходит за экран
        if self.rect.x < 0 or self.rect.x > 700 or self.rect.y < 0 or self.rect.y > 700:
            self.kill()
 


    
    





    



        





win_wight = 700
win_hight = 700
window = display.set_mode((win_wight,win_hight))

display.set_caption("maze")
svaga = transform.scale(image.load("TMvoRFU.png"),(win_wight,win_hight))
background = transform.scale(image.load("1032683.jpg"),(win_wight,win_hight))


player = Player("png-clipart-dota-2-invoker-dota-2-defense-of-the-ancients-invoker-the-international-youtube-dota-game-video-1121212.png", 5 , 550 ,110,90, 4)
monster1 = Enemy("images (1)оо.png", 550, 50 , 110,90,1)
monster2 = Enemy("pudge.png",560,50,110,90,1.5)
monster3 = Enemy("images (2).png", 550,50,90,70,2)

game = True
clock = time.Clock()

monsters = sprite.Group()
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)





num_fire = 0
rel_time = False


finish = False
start = timer()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1: 
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    
                    player.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time=True   
                

    if not finish:
        window.blit(background, (0, 0))
        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload..', True, (150,0,0))
                window.blit(reload, (250,400))
            else:
                num_fire = 0
                rel_time = False
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (0, 0))
        text_score = font2.render('Килов: ' + str(score), 1, (255, 255, 255))
        window.blit(text_score, (0, 30))

        
                





        monster1.reset()
        monster2.reset()
        monster3.reset()
        puli.update()  
        puli.draw(window)  
        player.reset()
        player.update()
        monster1.update3()
        monster2.update2()
        monster3.update1()

        



        if sprite.spritecollide(monster1, puli,True):
            score +=1
            monster1.kill
            monster1 = Enemy("images (1)оо.png", 550, 50 , 110,90,1)
            

        if sprite.spritecollide(monster2, puli,True):
            score +=1
            monster2.kill
            monster2 = Enemy("pudge.png",560,50,110,90,1.5)

        if sprite.spritecollide(monster3, puli, True):
            score +=1
            monster3.kill
            monster3 = Enemy("images (2).png", 550,50,90,70,2)


          

        if sprite.collide_rect(player, monster1) or sprite.collide_rect(player, monster2) or sprite.collide_rect(player, monster3):
            finish = True
            window.blit(lose,(200,300))
            
        if lost >= 5:
            finish = True
            window.blit(lose,(250,300))

        if score >= 10:
            finish = True
            window.blit(svaga, (10,10))

        

        


    display.update()
    clock.tick(60)























 

