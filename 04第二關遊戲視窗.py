import pygame

pygame.init()

# 建立第一關遊戲視窗
width = 700
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('第二關 上下左右')

# 設定顏色
background = (255, 246, 211)
black = (0, 0, 0)
white = (255, 255, 255)
orange = (255, 147, 0)

# 設定玩家
size = 140 # 頭像寬
player_font = pygame.font.Font(None, 32) # 字體大小 = 32
player1_surface = player_font.render('Name1', False, black)
player1_rect = player1_surface.get_rect()
player1_rect.center = (20+size/2, 20+size+20+20)
player2_surface = player_font.render('Name2', False, black)
player2_rect = player2_surface.get_rect()
player2_rect.center = (width-20-size/2, 20+size+20+20)

# 設定分數
score_font = pygame.font.Font(None, 32) # 字體大小 = 32
score1_surface = player_font.render('Score1', False, black) # 玩家1分數
score1_rect = score1_surface.get_rect()
score1_rect.center = (20+size+50, 50)
score2_surface = player_font.render('Score2', False, black) # 玩家2分數
score2_rect = score2_surface.get_rect()
score2_rect.center = (width-20-size-50, 50)

# 設定題目
image_up_before = pygame.image.load('上前.png')
image_up_after = pygame.image.load('上後.png')
image_down_before = pygame.image.load('下前.png')
image_down_after = pygame.image.load('下後.png')
image_left_before = pygame.image.load('左前.png')
image_left_after = pygame.image.load('左後.png')
image_right_before = pygame.image.load('右前.png')
image_right_after = pygame.image.load('右後.png')
image_up_before_reverse = pygame.image.load('上前反.png')
image_up_after_reverse = pygame.image.load('上後反.png')
image_down_before_reverse = pygame.image.load('下前反.png')
image_down_after_reverse = pygame.image.load('下後反.png')
image_left_before_reverse = pygame.image.load('左前反.png')
image_left_after_reverse = pygame.image.load('左後反.png')
image_right_before_reverse = pygame.image.load('右前反.png')
image_right_after_reverse = pygame.image.load('右後反.png')
image_cover = pygame.image.load('遮罩.png')
### 隨機出現上下左右的圖

while True: # 遊戲迴圈
    screen.fill(background)

    # 顯示玩家
    pygame.draw.rect(screen, white, (20, 20, size, size+20), 2) # 玩家1頭像
    screen.blit(player1_surface, player1_rect) # 玩家1名稱
    pygame.draw.rect(screen, white, (width-20-size, 20, size, 20+size), 2) # 玩家2頭像
    screen.blit(player2_surface, player2_rect) # 玩家2名稱

    # 顯示分數
    screen.blit(score1_surface, score1_rect) # 玩家1分數
    screen.blit(score2_surface, score2_rect) # 玩家2分數

    # 顯示題目
    pygame.draw.rect(screen, orange, (20, 220, width/2-40, 350), 2) # 玩家1題目框框 310*350
    pygame.draw.rect(screen, orange, (width/2+20, 220, width/2-40, 350), 2) # 玩家2題目框框 310*350
    # 玩家1的圖示
    screen.blit(image_up_before, (30, 223)) # 1-1
    screen.blit(image_up_before, (30 + 64 + 11.3, 223)) # 1-2
    screen.blit(image_up_before, (30 + 64 + 64 + 11.3 + 11.3, 223)) # 1-3
    screen.blit(image_up_before, (30 + 64 + 64 + 64 + 11.3 + 11.3 + 11.3, 223)) # 1-4
    screen.blit(image_cover, (20, 220)) # 第一行遮罩 #好像用不到哈哈哈
    screen.blit(image_up_before, (30, 220 + 70 + 3)) # 2-1
    screen.blit(image_up_before, (30 + 64 + 11.3, 220 + 70 + 3)) # 2-2
    screen.blit(image_up_before, (30 + 64 + 64 + 11.3 + 11.3, 220 + 70 + 3)) # 2-3
    screen.blit(image_up_before, (30 + 64 + 64 + 64 + 11.3 + 11.3 + 11.3, 220 + 70 + 3)) # 2-4
    screen.blit(image_cover, (20, 220+70)) # 第二行遮罩
    screen.blit(image_up_before, (30, 220 + 70 + 70 + 3)) # 3-1
    screen.blit(image_up_before, (30 + 64 + 11.3, 220 + 70 + 70 + 3)) # 3-2
    screen.blit(image_up_before, (30 + 64 + 64 + 11.3 + 11.3, 220 + 70 + 70 + 3)) # 3-3
    screen.blit(image_up_before, (30 + 64 + 64 + 64 + 11.3 + 11.3 + 11.3, 220 + 70 + 70 + 3)) # 3-4
    screen.blit(image_cover, (20, 220+70+70)) # 第三行遮罩
    screen.blit(image_up_before, (30, 220 + 70 + 70 + 70 + 3)) # 4-1
    screen.blit(image_up_before, (30 + 64 + 11.3, 220 + 70 + 70 + 70 + 3)) # 4-2
    screen.blit(image_up_before, (30 + 64 + 64 + 11.3 + 11.3, 220 + 70 + 70 + 70 + 3)) # 4-3
    screen.blit(image_up_before, (30 + 64 + 64 + 64 + 11.3 + 11.3 + 11.3, 220 + 70 + 70 + 70 + 3)) # 4-4
    screen.blit(image_cover, (20, 220+70+70+70)) # 第四行遮罩
    screen.blit(image_up_before, (30, 220 + 70 + 70 + 70 + 70 + 3)) # 5-1
    screen.blit(image_up_before, (30 + 64 + 11.3, 220 + 70 + 70 + 70 + 70 + 3)) # 5-2
    screen.blit(image_up_before, (30 + 64 + 64 + 11.3 + 11.3, 220 + 70 + 70 + 70 + 70 + 3)) # 5-3
    screen.blit(image_up_before, (30 + 64 + 64 + 64 + 11.3 + 11.3 + 11.3, 220 + 70 + 70 + 70 + 70 + 3)) # 5-4
    screen.blit(image_cover, (20, 220+70+70+70+70)) # 第五行遮罩
    # 玩家2的圖示
    screen.blit(image_up_before, (30 + 350, 223)) # 1-1
    screen.blit(image_up_before, (30 + 64 + 11.3 + 350, 223)) # 1-2
    screen.blit(image_up_before, (30 + 64 + 64 + 11.3 + 11.3 + 350, 223)) # 1-3
    screen.blit(image_up_before, (30 + 64 + 64 + 64 + 11.3 + 11.3 + 11.3 + 350, 223)) # 1-4
    screen.blit(image_cover, (20+350, 220)) # 第一行遮罩 #好像用不到哈哈哈
    screen.blit(image_up_before, (30 + 350, 220 + 70 + 3)) # 2-1
    screen.blit(image_up_before, (30 + 64 + 11.3 + 350, 220 + 70 + 3)) # 2-2
    screen.blit(image_up_before, (30 + 64 + 64 + 11.3 + 11.3 + 350, 220 + 70 + 3)) # 2-3
    screen.blit(image_up_before, (30 + 64 + 64 + 64 + 11.3 + 11.3 + 11.3 + 350, 220 + 70 + 3)) # 2-4
    screen.blit(image_cover, (20+350, 220+70)) # 第二行遮罩
    screen.blit(image_up_before, (30 + 350, 220 + 70 + 70 + 3)) # 3-1
    screen.blit(image_up_before, (30 + 64 + 11.3 + 350, 220 + 70 + 70 + 3)) # 3-2
    screen.blit(image_up_before, (30 + 64 + 64 + 11.3 + 11.3 + 350, 220 + 70 + 70 + 3)) # 3-3
    screen.blit(image_up_before, (30 + 64 + 64 + 64 + 11.3 + 11.3 + 11.3 + 350, 220 + 70 + 70 + 3)) # 3-4
    screen.blit(image_cover, (20+350, 220+70+70)) # 第三行遮罩
    screen.blit(image_up_before, (30 + 350, 220 + 70 + 70 + 70 + 3)) # 4-1
    screen.blit(image_up_before, (30 + 64 + 11.3 + 350, 220 + 70 + 70 + 70 + 3)) # 4-2
    screen.blit(image_up_before, (30 + 64 + 64 + 11.3 + 11.3 + 350, 220 + 70 + 70 + 70 + 3)) # 4-3
    screen.blit(image_up_before, (30 + 64 + 64 + 64 + 11.3 + 11.3 + 11.3 + 350, 220 + 70 + 70 + 70 + 3)) # 4-4
    screen.blit(image_cover, (20+350, 220+70+70+70)) # 第四行遮罩
    screen.blit(image_up_before, (30 + 350, 220 + 70 + 70 + 70 + 70 + 3)) # 5-1
    screen.blit(image_up_before, (30 + 64 + 11.3 + 350, 220 + 70 + 70 + 70 + 70 + 3)) # 5-2
    screen.blit(image_up_before, (30 + 64 + 64 + 11.3 + 11.3 + 350, 220 + 70 + 70 + 70 + 70 + 3)) # 5-3
    screen.blit(image_up_before, (30 + 64 + 64 + 64 + 11.3 + 11.3 + 11.3 + 350, 220 + 70 + 70 + 70 + 70 + 3)) # 5-4
    screen.blit(image_cover, (20+350, 220+70+70+70+70)) # 第五行遮罩


    for event in pygame.event.get():
        # 玩家按下相對按鍵，題目變色
        """if event.type == pygame.KEYDOWN:
            # 玩家 1
            if event.key == pygame.K_w:
                # 上 圖示變色
            elif event.key == pygame.K_s:
                # 下 圖示變色
            elif event.key == pygame.K_a:
                # 左 圖示變色
            elif event.key == pygame.K_d:
                # 右 圖示變色
            # 玩家 2
            if event.key == pygame.K_UP:
                # 上 圖示變色
            elif event.key == pygame.K_DOWN:
                # 下 圖示變色
            elif event.key == pygame.K_LEFT:
                # 左 圖示變色
            elif event.key == pygame.K_RIGHT:
                # 右 圖示變色"""
        # 關閉視窗
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.flip()