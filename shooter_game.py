from pygame import *
from random import randint
#импортируем функцию для засекания времени, 
#чтобы интерпретатор не искал эту функцию в pygame модуле time, даём ей другое название сами
from time import time as timer 
pygame.init()
#фоновая музыка

pygame.mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
#шрифты и надписи
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)
 
#нам нужны такие картинки:
img_back = "galaxy.jpg" #фон игры
img_hero = "rocket.png" #герой
img_bullet = "bullet.png" #пуля
img_enemy = "ufo.png" #враг
img_ast = "asteroid.png" #астероид
 
score = 0 #сбито кораблей
lost = 0 #пропущено кораблей
max_lost = 10 #проиграли, если пропустили столько
goal = 7 #выиграли, если сбито столько
rel_time = False #флаг, отвечающий за перезарядку
num_fire = 0  #переменная для подсчёта выстрелов 
life = 3  #очки жизни
 
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #вызываем конструктор класса (Sprite):
       GameSprite.sprite.Sprite.__init__(self)
 
       #каждый спрайт должен хранить свойство image - изображение
       self.image = GameSprite.transform.scale(GameSprite.image.load(player_image), (size_x, size_y))
       self.speed = player_speed
 
       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
   def update(self):
       keys = GameSprite.key.get_pressed()
       if keys[GameSprite.K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[GameSprite.K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
       bullets.add(bullet)
 
#класс спрайта-врага  
class Enemy(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдет до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1
 
#класс спрайта-пули  
class Bullet(GameSprite):
   #движение пули
   def update(self):
       self.rect.y -= self.speed
       #исчезает, если дойдет до края экрана
       if self.rect.y < 0:
           self.kill()
 
#создаем окошко
win_width = 700
win_height = 500
GameSprite.display.set_caption("Shooter")
window = GameSprite.display.set_mode((win_width, win_height))
background = GameSprite.transform.scale(GameSprite.image.load(img_back), (win_width, win_height))
 
#создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
monsters = GameSprite.sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

asteroids = GameSprite.sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)
 
bullets = GameSprite.sprite.Group()
 
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
while run:
   #событие нажатия на кнопку Закрыть
    for e in GameSprite.event.get():
        if e.type ==GameSprite.QUIT:
            run = False
        #событие нажатия на пробел - спрайт стреляет
        elif e.type == GameSprite.KEYDOWN:
            if e.key == GameSprite.K_SPACE:
                #проверяем, сколько выстрелов сделано и не происходит ли перезарядка
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                if num_fire  >= 5 and rel_time == False : #если игрок сделал 5 выстрелов
                    last_time = timer() #засекаем время, когда это произошло
                    rel_time = True #ставим флаг перезарядки
    
    if not finish:
        #обновляем фон
        window.blit(background,(0,0))

        #производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
    
        #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        #перезарядка
        if rel_time == True:
            now_time = timer() #считываем время

            if now_time - last_time < 3: #пока не прошло 3 секунды выводим информацию о перезарядке
                reload = font2.render('Внимание, перезарядка...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0   #обнуляем счётчик пуль
                rel_time = False #сбрасываем флаг перезарядки

        #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        #и монстры снова добавляются 
        collides = sprite.groupcollide(monsters, bullets, True, True)
        #print(collides)
        for c in collides:
            #этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        #если спрайт коснулся врага, уменьшает жизнь
        if GameSprite.sprite.spritecollide(ship, monsters, False) or GameSprite.sprite.spritecollide(ship, asteroids, False):
            GameSprite.sprite.spritecollide(ship, monsters, True)
            GameSprite.sprite.spritecollide(ship, asteroids, True)
            life = life -1
            print(life)

        #проигрыш
        if life == 0 or lost >= max_lost:
            finish = True #проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))  

        #проверка выигрыша: сколько очков набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
    
        #пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
    
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
    
        #задаём разный цвет в зависимости от количества жизней
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
    
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        GameSprite.display.update()

           
    #бонус: автоматический перезапуск игры
    else:
        finish = False
        score = 0
        lost = 0
        num_fire=0
        life=3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()   
    
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        for i in range(1, 3):
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)
        num_fire = 0
    #цикл срабатывает каждую 0.05 секунд
    time.delay(50)