from pygame import *
import math
init()

class GameSprite(sprite.Sprite):
    def __init__(self, image1, x, y, speed, width, height):
        super().__init__()

        self.image = transform.scale(image.load(image1), (width, height))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 160:
            self.rect.y += self.speed
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 160:
            self.rect.y += self.speed

back = (200, 255, 255)
win_width = 1000
win_height = 700
win = display.set_mode((win_width, win_height))
win.fill(back)

game = True
finish = False
clock = time.Clock()
FPS = 60

score_1 = 1
score_2 = 1

background = transform.scale(image.load("картинки/fon.png"), (win_width, win_height))

racket1 = Player("картинки/player_1.png", win_width - 40, 0, 10, 40, 170)
racket2 = Player("картинки/player_2.png", 0, 0, 10, 40, 170)

ball = GameSprite("картинки/ball.png", win_width / 2, win_height / 2, 2, 50, 50)

font = font.Font(None, 60)
lose1 = font.render("PLAYER 1 LOSE!", True, (255, 255, 255))
lose2 = font.render("PLAYER 2 LOSE!", True, (255, 255, 255))

speed = 3
speedxy = [0, 0]
ang = 23
speedxy[0] = math.cos(math.radians(ang)) * speed
speedxy[1] = math.sin(math.radians(ang)) * speed


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        win.blit(background, (0, 0))
        racket1.update_l()
        racket2.update_r()

        ball.rect.x += speedxy[0]
        ball.rect.y += speedxy[1]

        if sprite.collide_rect(ball, racket1) or sprite.collide_rect(ball, racket2):
            speedxy[0] *= -1
            if speedxy[0] > 0 and speedxy[0] < 10:
                speedxy[0] += 1
            elif speedxy[0] < 0 and speedxy[0] > -10:
                speedxy[0] -= 1

        if ball.rect.y > win_height - 50 or  ball.rect.y < 0:
            speedxy[1] *= -1
            if speedxy[1] > 0 and speedxy[1] < 10:
                speedxy[1] += 1
            elif speedxy[1] < 0 and speedxy[1] > -10:
                speedxy[1] -= 1

        if score_1 >= 10:
            win.blit(lose2, (350, 330))
            finish = True
        elif score_2 >= 10:
            win.blit(lose1, (350, 330))
            finish = True
        else:
            ball.reset()

        if ball.rect.x < 0:
            ball.rect.y = 330 
            ball.rect.x = 480
            speedxy[0] = 3
            speedxy[1] = 3
            score_1 += 1

        if ball.rect.x > win_width:
            ball.rect.y = 330 
            ball.rect.x = 480
            speedxy[0] = 3
            speedxy[1] = 3
            score_2 += 1

        racket1.reset()
        racket2.reset()

        score1 = font.render(str(score_1), True, (255, 255, 255))
        score2 = font.render(str(score_2), True, (255, 255, 255))

        win.blit(score2, (250, 10))
        win.blit(score1, (750, 10))

    display.update()
    clock.tick(FPS)