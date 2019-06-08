import pygame, random

pygame.init()
COUNT = pygame.USEREVENT + 1
pygame.time.set_timer(COUNT, 1000) 

def show_icons(num):
    # input: a list
    for i in range(len(num)):
        for j in range(4):
            if i < len(num)/2:
                x = 30 + 75.3*j
                y = 223 + 70*i
            else:
                x = 380 + 75.3*j
                y = 223 + 70*(i - len(num)/2)
            screen.blit(imagelist[num[i][j]], (x, y))
            

def show_cover(active, player):
    for i in range(1, int(len(num)/2) + 1):
        if i == active:
            continue
        if player == 1:
            x = 20
            y = 150 + 70*i
        else:
            x = 370
            y = 150 + 70*i
        screen.blit(image_cover, (x, y)) # 第二行遮罩

def next_pos(num, i, j, index1, player):
    if player == 1:
        if j == 3:
            if i == len(num)/2 - 1:
                index1 = 1
            else:
                i += 1
                j = 0
        else:
            j += 1
    else:
        if j == 3:
            if i == len(num) - 1:
                index1 = 1
            else:
                i += 1
                j = 0
        else:
            j += 1
    return i, j, index1

def next_pos2(num, k, l, index2, player):
    if player == 1:
        if l == 3:
            if k == len(num)/2 - 1:
                index2 = 1
            else:
                k += 1
                l = 0
        else:
            l += 1
    else:
        if l == 3:
            if k == len(num) - 1:
                index2 = 1
            else:
                k += 1
                l = 0
        else:
            l += 1
    return k, l, index2

def show_time(text, countdown):
    font = pygame.font.Font(None, 60)
    font_big = pygame.font.Font(None, 80)
    red = (255, 0, 0)
    if countdown <= 3:
        clock_surface = font_big.render(text, True, red)
    else:
        clock_surface = font.render(text, True, black)
    clock_rect = clock_surface.get_rect()
    clock_rect.center = (width / 2, 160)
    screen.blit(clock_surface, clock_rect)

def show_end():
    font_big = pygame.font.Font(None, 150)
    red = (255, 0, 0)
    output_surface = font_big.render("Time's Up!!", True, red)
    output_rect = output_surface.get_rect()
    output_rect.center = (width / 2, height / 2)
    screen.blit(output_surface, output_rect)

def new_question(number):
    # input: a list
    num = []
    qlist = []
    reversenum = qlist.count(4) + qlist.count(5) + qlist.count(6) + qlist.count(7) 
    for i in range (number*4):
        
        reversenum = qlist.count(4) + qlist.count(5) + qlist.count(6) + qlist.count(7) 
        if questionnum < 8:
            if len(qlist) == 0:
                q = random.randint(0,7)
                qlist.append(q)
            elif reversenum / len(qlist) < questionnum /10 : 
                q = random.randint(0,7)
                qlist.append(q)
            elif  reversenum / len(qlist) >= questionnum/10 :
                q = random.randint(0,3)
                qlist.append(q)
        if questionnum >= 8:
            q = random.randint(4,7)
            qlist.append(q)
 
    random.shuffle(qlist)  
    
    for i in range(number):
        num.append([])
        for j in range(4):
            
            num[-1].append(qlist[i*4 + j])
            
    for i in range(number):
        num.append([])
        for j in range(4):
            r = num[i][j]
            num[-1].append(r)
    qlist =[] 
    return num
countdown = 100
score1 = 0
score2 = 0 
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


#設定圖示
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


questionnum = 1 #第幾題了
number = 1 #總共幾排
while True:
    #隨機產生0-7之亂數
    num = new_question(number)
    if questionnum < 10:
        questionnum += 1
    if number < 5:
	    number += 1
    #判斷是否為5-4圖示的index
    index1 = 0
    index2 = 0	
    #從1-1開始玩
    i, j, k, l = 0, 0, int(len(num)/2), 0
    while True:
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

        # 顯示圖示
        show_icons(num)
        
        # 顯示遮罩
        show_cover(i + 1, player = 1)
        show_cover(k - int(len(num)/2) + 1, player = 2)
        
        #顯示分數
        score_font = pygame.font.Font(None, 50)
        score_surf = score_font.render(str(score1), 1, (0, 0, 0))
        screen.blit(score_surf, (200,80))
        score_font = pygame.font.Font(None, 50)
        score_surf = score_font.render(str(score2), 1, (0, 0, 0))
        screen.blit(score_surf, (480,80))
		
        #倒數計時
        countstext = str(countdown)
        if countdown > 0:
            show_time(countstext, countdown)
        else:
            show_end()

        pygame.display.flip()

        # 玩家按下相對按鍵，題目變色
        if index1 == 1:
           score1 += 3
           break
        if index2 == 1:
           score2 += 3
           break
        #上或反下的時候
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_w:
                    if num[i][j] == 0 or num[i][j] == 4:
                         num[i][j] += 8  # 變成after的圖示
                         i, j, index1 = next_pos(num, i, j, index1, player = 1)
                    elif num[i][j] != 0 or num[i][j] != 4:
                         score1 -= 1
                         
                if event.key == pygame.K_s:
                    if num[i][j] == 1 or num[i][j] == 5:
                         num[i][j] += 8  # 變成after的圖示
                         i, j, index1 = next_pos(num, i, j, index1, player = 1)
                    elif num[i][j] != 1 or num[i][j] != 5:
                         score1 -= 1
                if event.key == pygame.K_a:
                    if num[i][j] == 2 or num[i][j] == 6:
                         num[i][j] += 8  # 變成after的圖示
                         i, j, index1 = next_pos(num, i, j, index1, player = 1)
                    elif num[i][j] != 2 or num[i][j] != 6:
                         score1 -= 1
                if event.key == pygame.K_d:
                    if num[i][j] == 3 or num[i][j] == 7:
                         num[i][j] += 8  # 變成after的圖示
                         i, j, index1 = next_pos(num, i, j, index1, player = 1)
                    elif num[i][j] != 3 or num[i][j] != 7:
                         score1 -= 1
                if event.key == pygame.K_UP:
                    if num[k][l] == 0 or num[k][l] == 4:
                         num[k][l] += 8  # 變成after的圖示
                         k, l, index2 = next_pos2(num, k, l, index2, player = 2)
                    elif num[i][j] != 0 or num[i][j] != 4:
                         score2 -= 1
                         
                if event.key == pygame.K_DOWN:
                    if num[k][l] == 1 or num[k][l] == 5:
                         num[k][l] += 8  # 變成after的圖示
                         k, l, index2 = next_pos2(num, k, l, index2, player = 2)
                    elif num[i][j] != 1 or num[i][j] != 5:
                         score2 -= 1
                if event.key == pygame.K_LEFT:
                    if num[k][l] == 2 or num[k][l] == 6:
                         num[k][l] += 8  # 變成after的圖示
                         k, l, index2 = next_pos2(num, k, l, index2, player = 2)
                    elif num[i][j] != 2 or num[i][j] != 6:
                         score2 -= 1
                if event.key == pygame.K_RIGHT:
                    if num[k][l] == 3 or num[k][l] == 7:
                         num[k][l] += 8  # 變成after的圖示
                         k, l, index2 = next_pos2(num, k, l, index2, player = 2)
                    elif num[i][j] != 3 or num[i][j] != 7:
                         score2 -= 1
                        
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == COUNT:
                countdown = countdown - 1
                countstext = str(countdown)
                if countdown == -3:
                    game2 = False