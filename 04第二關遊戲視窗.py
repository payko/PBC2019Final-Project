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
    pygame.draw.rect(screen, orange, (20, 220, width/2-40, 350), 2) # 玩家1題目框框
    pygame.draw.rect(screen, orange, (width/2+20, 220, width/2-40, 350), 2) # 玩家2題目框框

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