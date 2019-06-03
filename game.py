import pygame

pygame.init()

# 建立第一關遊戲視窗
width = 700
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('第一關 3的世界')

# 設定顏色
background = (255, 246, 211)
black = (0, 0, 0)
white = (255, 255, 255)

# 設定玩家
size = 140 # 頭像寬
player_font = pygame.font.Font(None, 32) # 字體大小 = 32
player1_surface = player_font.render('Name1', False, black)
player1_rect = player1_surface.get_rect()
player1_rect.center = (20+size/2, 20+size+20+20)
player2_surface = player_font.render('Name2', False, black)
player2_rect = player2_surface.get_rect()
player2_rect.center = (width-20-size/2, 20+size+20+20)

# 設定題目
question_font = pygame.font.Font(None, 60) # 字體大小 = 60
question_surface = question_font.render('Question', False, black) ## Question更改為隨機數字
question_rect = question_surface.get_rect()
question_rect.center = (width/2, height/2)

# 設定拍手
clap = pygame.image.load('clap.png')

while True: # 遊戲迴圈
    screen.fill(background)

    # 顯示玩家
    pygame.draw.rect(screen, white, (20, 20, size, size+20), 2) # 玩家1頭像
    screen.blit(player1_surface, player1_rect) # 玩家1名稱
    pygame.draw.rect(screen, white, (width-20-size, 20, size, 20+size), 2) # 玩家2頭像
    screen.blit(player2_surface, player2_rect) # 玩家2名稱

    # 顯示題目
    screen.blit(question_surface, question_rect)

    for event in pygame.event.get():
        # 顯示拍手
        # player1按 s 鍵，player2按 k 鍵
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                screen.blit(clap, (50, 350))
            elif event.key == pygame.K_k:
                screen.blit(clap, (width-50-260, 350))
        # 關閉視窗
        elif event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.flip()
