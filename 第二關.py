import pygame, random

pygame.init()

def show_icons(num, player):
    # input: a list, an int(1 or 2)
    for i in range(5):
        if player == 2:
            k = i + 5
        for j in range(4):
            if player == 1:
                x = 30 + 75.3*j
                y = 223 + 70*i
            else:
                x = 380 + 75.3*j
                y = 223 + 70*i
            screen.blit(imagelist[num[i if player == 1 else k][j]], (x, y))

def show_cover(active, player):
    for i in range(1,6):
        if i == active:
            continue
        if player == 1:
            x = 20
            y = 150 + 70*i
        else:
            x = 370
            y = 150 + 70*i
        screen.blit(image_cover, (x, y)) # 第二行遮罩

def next_pos(i, j):
    if j == 3:
        if i == 4:
            index = 1
        else:
            i += 1
            j = 0
    else:
        j += 1
    return i, j

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
imagelist = [image_up_before, image_down_before, image_left_before, image_right_before,
             image_down_before_reverse, image_up_before_reverse, image_right_before_reverse, image_left_before_reverse,
             image_up_after, image_down_after, image_left_after, image_right_after,
             image_down_after_reverse, image_up_after_reverse,image_right_after_reverse, image_left_after_reverse]


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

    for event in pygame.event.get():
        # 關閉視窗
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.flip()
    #隨機產生0-7之亂數
    num = []
    for i in range(5):
        num.append([])
        for j in range(4):
            r = random.randint(0,7)
            num[-1].append(r)
    for i in range(5):
        num.append(num[i])


    active1 = 1  # 玩家一按到第幾行
    active2 = 1  # 玩家二按到第幾行
    while True:
        # 顯示題目
        show_icons(num, player = 1)
        show_icons(num, player = 2)
        
        # 顯示遮罩
        show_cover(active1, player = 1)
        show_cover(active2, player = 2)
   
        for event in pygame.event.get():
            # 關閉視窗
            if event.type == pygame.QUIT:
                pygame.quit()
        
        pygame.display.flip()
        
        #判斷是否為5-4圖示的index
        index = 0
		
        #從1-1開始玩
        i, j, k, l = 0, 0, 5, 0
        while True:
            # 玩家按下相對按鍵，題目變色
            if index == 1:
               break
            #上或反下的時候
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_w and (num[i][j] == 0 or num[i][j] == 4))\
                        or (event.key == pygame.K_s and (num[i][j] == 1 or num[i][j] == 5))\
                        or (event.key == pygame.K_a and (num[i][j] == 2 or num[i][j] == 6))\
                        or (event.key == pygame.K_d and (num[i][j] == 3 or num[i][j] == 7)):
                        num[i][j] += 7  # 變成after的圖示
                        i, j = next_pos(i, j)
                    if (event.key == pygame.K_UP and (num[k][l] == 0 or num[k][l] == 4))\
                        or (event.key == pygame.K_DOWN and (num[k][l] == 1 or num[k][l] == 5))\
                        or (event.key == pygame.K_LEFT and (num[k][l] == 2 or num[k][l] == 6))\
                        or (event.key == pygame.K_RIGHT and (num[k][l] == 3 or num[k][l] == 7)):
                        num[k][l] += 7
                        k, l = next_pos(k, l)
                if event.type == pygame.QUIT:
                    pygame.quit()
