import pygame
import random
import os
import sys

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WIDTH = 600
HEIGHT = 400
game_over = False

pygame.init()  # 初始化pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 定義畫面長寬高
pygame.display.set_caption("86-不存在的戰區")  # 遊戲標頭檔
clock = pygame.time.Clock()  # 確保在每一台電腦都成正常運作，控制偵數

background = pygame.image.load(os.path.join("bg.jpg")).convert()  # 載入圖片路徑
undertaker = pygame.image.load(os.path.join(
    "undertaker.png")).convert()  # 載入圖片路徑
bullet_image = pygame.image.load(
    os.path.join("bullet.jpg")).convert()  # 載入圖片路徑
army_image = pygame.image.load(os.path.join("army.png")).convert()  # 載入圖片路徑
font_name = os.path.join("微軟正黑體-1.ttf")


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


def draw_life(surf, life, x, y):
    if life < 0:
        life = 0
    life__LENGTH = 100
    life_WIDTH = 20
    fill = (life/100)*life__LENGTH
    outline_rect = pygame.Rect(x, y, life__LENGTH, life_WIDTH)
    fill_rect = pygame.Rect(x, y, fill, life_WIDTH)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_screen():
    screen.blit(background, (0, 0))
    draw_text(screen, '86不存在的戰區', 64, WIDTH / 2, HEIGHT/4)
    draw_text(screen, '左右鍵移動送葬者，上鍵發射子彈', 25, WIDTH / 2, HEIGHT/2)
    draw_text(screen, '按一下滑鼠開始遊戲', 20, WIDTH / 2, HEIGHT*3/4)
    pygame.display.update()
    wait = True
    while wait:
        clock.tick(FPS)  # 固定迴圈偵數
        for event in pygame.event.get():  # 取得輸入
            if event.type == pygame.QUIT:  # 當畫面又上的框框被按下
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 當鍵盤按鍵被按下的時候
                wait = False


class Plane(pygame.sprite.Sprite):  # 用plane繼承sprite類別
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call內建的sprite初始函式
        self.image = pygame.transform.scale(
            undertaker, (90, 165))  # 死神機甲圖片，改規格大小
        self.rect = self.image.get_rect()  # 用來定位圖片有x,y(框起來)
        self.radius = 30
        self.image.set_colorkey(BLACK)
        self.rect.centerx = WIDTH / 2  # 中間x座標
        self.rect.centery = HEIGHT - 50  # 底部座標
        self.speedx = 8
        self.life = 100

    def update(self):
        # pygame.key.get_pressed()會回傳布林值，判斷鍵盤上有沒有按鍵被按下去
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:  # 如果右鍵被按下就回傳True
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:  # 如果左鍵被按下就回傳True
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)  # 回傳飛機現在的x中心座標位置和頂部
        all_sprite.add(bullet)
        bullets.add(bullet)  # 建立子彈的sprite


class Army(pygame.sprite.Sprite):  # 用rock繼承sprite類別
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call內建的sprite初始函式
        self.image = pygame.transform.scale(army_image, (60, 117))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()  # 用來定位圖片有x,y(框起來)
        self.radius = 25
        self.rect.x = random.randrange(
            0, WIDTH - self.rect.width)  # 隨機在不同x座標生成
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 10)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:  # 超過底部，超過右邊，超過左邊
            self.rect.x = random.randrange(
                0, WIDTH - self.rect.width)  # 隨機在不同x座標生成
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 10)


class Bullet(pygame.sprite.Sprite):  # 用rock繼承sprite類別
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # call內建的sprite初始函式
        self.image = pygame.transform.scale(bullet_image, (10, 20))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()  # 用來定位圖片有x,y(框起來)
        self.rect.centerx = x  # 子彈
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()  # sprite 中的函式，會一個一個檢查sprite中的群組，如果裡面有Bullet就刪掉


all_sprite = pygame.sprite.Group()  # 用來放sprite物件的群組

show_screen = True
run = True
reset = False
while run:
    if show_screen:
        draw_screen()
        show_screen = False
        armys = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        plane = Plane()
        if not reset:
            all_sprite.add(plane)  # 把plane加到sprite的群組中
        for i in range(8):
            army = Army()
            all_sprite.add(army)  # 把rock加到sprite的群組中
            armys.add(army)  # 建立rock的sprite群組
        score = 0

    clock.tick(FPS)  # 固定迴圈偵數
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if not game_over and event.key == pygame.K_UP:
                plane.shoot()
            elif game_over and event.type == pygame.MOUSEBUTTONDOWN:
                show_screen = False  # 00000000
                reset = True
                game_over = False

    all_sprite.update()
    # 判斷敵人跟子彈有沒有撞到一起，第三個是判斷敵人碰撞後要不要刪掉
    hits = pygame.sprite.groupcollide(armys, bullets, True, True)
    for hit in hits:  # 此時hit是字典，用來紀錄被刪掉的子彈跟敵人
        r = Army()  # 當有敵人被刪掉時，就新增一個敵人
        all_sprite.add(r)  # 在加到all_sprite裡面
        armys.add(r)  # 加回敵人的群組，才能繼續判斷有沒有被子彈打到
        score += 10

    hits = pygame.sprite.spritecollide(
        plane, armys, True, pygame.sprite.collide_circle)  # 判斷死神跟子彈有沒有撞到一起
    for hit in hits:  # 如果死神和敵人撞到，就扣生命值
        r = Army()  # 當有敵人被刪掉時，就新增一個敵人
        all_sprite.add(r)  # 在加到all_sprite裡面
        armys.add(r)
        plane.life -= 10
        if plane.life <= 0:
            game_over = True
            reset = True

    screen.fill(WHITE)
    screen.blit(background, (0, 0))
    all_sprite.draw(screen)  # 把群組中的sprite都畫在畫面上
    draw_text(screen, str(score), 36, WIDTH / 2, 10)
    draw_life(screen, plane.life, 5, 10)
    while game_over:
        screen.blit(background, (0, 0))
        draw_text(screen, '86不存在的戰區', 64, WIDTH / 2, HEIGHT/4)
        draw_text(screen, "Game Over", 64, WIDTH/2, HEIGHT/2 - 30)
        draw_text(screen, "按下滑鼠回主畫面", 32, WIDTH/2, HEIGHT/2 + 50)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_over = False
                show_screen = True
        pygame.display.update()  # 更新畫面
        pygame.time.wait(200)

    pygame.display.update()  # 更新畫面

pygame.quit()  # 結束整個程式
