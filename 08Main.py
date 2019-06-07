import pygame
import csv
import random

pygame.init()
COUNT = pygame.USEREVENT + 1
pygame.time.set_timer(COUNT,1000)  # 每隔1秒發送一次自定義事件

# functions for countdown
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

# functions for leader board
def compared(n1, s1, n2, s2, want):
    # input: 玩家名稱、得分、回傳winner(want = 'w')、回傳loser(want = 'l')
    if (s1 >= s2 and want == 'w') or (s1 < s2 and want == 'l'):
        return n1, s1
    return n2, s2

def write_board(name, score, Board):
    # 把一位玩家的結果記入排行榜
    for i in range(1, len(Board)):
        if Board[i][1] == '':
            Board[i][1] = name
            Board[i][2] = score
            break
        elif score >= int(Board[i][2]):
            for k in range(1, len(Board) - i):
                Board[-k][1] = Board[-(k + 1)][1]
                Board[-k][2] = Board[-(k + 1)][2]
            Board[i][1] = name
            Board[i][2] = score
            break
    return Board

# functions for game2
def show_icons(num, imagelist):
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
            

def show_cover(num, image_cover, active, player):
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

def next_pos(num, i, j, index, player):
    if player == 1:
        if j == 3:
            if i == len(num)/2 - 1:
                index = 1
            else:
                i += 1
                j = 0
        else:
            j += 1
    else:
        if j == 3:
            if i == len(num) - 1:
                index = 1
            else:
                i += 1
                j = 0
        else:
            j += 1
    return i, j, index

def new_question(number):
    # input: a list
    num = []
    for i in range(number):
        num.append([])
        for j in range(4):
            r = random.randint(0,7)
            num[-1].append(r)
    for i in range(number):
        num.append([])
        for j in range(4):
            r = num[i][j]
            num[-1].append(r)
    return num

# functions for create windows
def blank_window(string, image_button, background_image):
    stay = True
    screen.fill(background)
    if background_image != None:
        screen.blit(background_image, (0, 0))
         
    if string != None:
        output_font = pygame.font.Font(None, 60)  # 字體大小 = 60
        output_surface = output_font.render(string, False, black)
        output_rect = output_surface.get_rect()
        output_rect.center = (width / 2, height / 2)
        screen.blit(output_surface, output_rect)   
    while stay:
        for event in pygame.event.get():
            # 關閉視窗
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 500 < mouse[0] < 630 and 515 < mouse[1] < 565: # 給button設定的範圍
                     stay = False
        screen.blit(image_button, (button_x, button_y))
        pygame.display.flip()
        mouse = pygame.mouse.get_pos()

def prepare_window(string):
    blank_window(string, image_done_button, None)

def game_intro(image_rule):
    blank_window(None, image_start_button, image_rule)

def result_window(string):
    blank_window(string, image_next_button, None)

def board_window(wn, ws, ln, ls):
    #input: 贏家名字、得分、輸家名字、得分
    stay = True
    screen.fill(background)
    # screen.blit(background_image, (0, 0))
    # 之後補上
    
    # 讀入舊的排行榜
    r_file = open('排行榜.csv', 'r', newline = '', encoding = 'utf-8') 
    board = csv.reader(r_file) 
    Board = []
    for row in board:
        Board.append(row)
    Board[0] = ['Rank', 'Player', 'Score']
    r_file.close()

    # 製造新的排行榜
    Board = write_board(wname, wscore, Board)
    Board = write_board(lname, lscore, Board)

    # 寫入新的排行榜
    w_file = open('排行榜.csv', 'w', newline = '', encoding = 'utf-8')
    board_writer = csv.writer(w_file)
    for row in Board:
        board_writer.writerow(row)
    w_file.close()

    output_font = pygame.font.Font(None, 48)  # 字體大小 = 60
    for i in range(6):
        rank = str(Board[i][0])
        player = str(Board[i][1])
        score = str(Board[i][2])
        output_surface = output_font.render('%s%15s%10s' % (rank, player, score), False, black)
        output_rect = output_surface.get_rect()
        output_rect.center = (width / 2, 100 + 50*i)
        screen.blit(output_surface, output_rect)   
    while stay:
        for event in pygame.event.get():
            # 關閉視窗
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 500 < mouse[0] < 630 and 515 < mouse[1] < 565: # 給button設定的範圍
                     stay = False
        screen.blit(image_next_button, (button_x, button_y))
        pygame.display.flip()
        mouse = pygame.mouse.get_pos()

def again_window(string):
    stay = True
    screen.fill(background)
    output_font = pygame.font.Font(None, 60)  # 字體大小 = 60
    output_surface = output_font.render(string, False, black)
    output_rect = output_surface.get_rect()
    output_rect.center = (width / 2, height / 2)
    screen.blit(output_surface, output_rect)
    while stay:
        for event in pygame.event.get():
            # 關閉視窗
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 500 < mouse[0] < 630 and 515 < mouse[1] < 565: # 給Again button設定的範圍
                    again = True
                    stay = False
                elif 280 < mouse[0] < 430 and 515 < mouse[1] < 565: # 給End button設定的範圍
                    again = False
                    stay = False
        screen.blit(image_again_button, (button_x, button_y))
        screen.blit(image_end_button, (width / 2 - 40, 507))
        pygame.display.flip()
        mouse = pygame.mouse.get_pos()
    return again

# for game windows setting
def set_color():
    background = (255, 246, 211)
    black = (0, 0, 0)
    white = (255, 255, 255)
    return background, black, white

def set_player(name, num):
    background, black, white = set_color()
    # 設定玩家
    size = 140  # 頭像寬
    player_font = pygame.font.Font(None, 32)  # 字體大小 = 32
    player_surface = player_font.render(name, False, black)
    player_rect = player_surface.get_rect()
    if num == 1:
        player_rect.center = (20 + size / 2, 20 + size + 20 + 20)
    else:
        player_rect.center = (width - 20 - size / 2, 20 + size + 20 + 20)
    return player_surface, player_rect

def set_score(score, num):
    background, black, white = set_color()
    size = 140
    # 設定分數
    score_font = pygame.font.Font(None, 32)  # 字體大小 = 32
    score_surface = score_font.render(str(score), False, black)  # 玩家1分數
    score_rect = score_surface.get_rect()
    if num == 1:
        score_rect.center = (20 + size + 50, 50)
    else:
        score_rect.center = (width - 20 - size - 50, 50)
    return score_surface, score_rect

# for game runnung
def game_1():
    game1 = True
    countdown = 60
    while game1:
        background, black, white = set_color()
        size = 140
        # 設定題目
        question_font = pygame.font.Font(None, 60)  # 字體大小 = 60
        question_surface = question_font.render('Question', False, black)  ## Question更改為隨機數字
        question_rect = question_surface.get_rect()
        question_rect.center = (width / 2, height / 2)
        # 設定拍手
        clap = pygame.image.load('clap.png')
        show = 0  # 不顯示拍手 ## 換新題目show要重設為0
        while game1:  # 遊戲迴圈
            screen.fill(background)
            # 顯示玩家
            pygame.draw.rect(screen, white, (20, 20, size, size + 20), 2)  # 玩家1頭像
            screen.blit(player1_surface, player1_rect)  # 玩家1名稱
            pygame.draw.rect(screen, white, (width - 20 - size, 20, size, 20 + size), 2)  # 玩家2頭像
            screen.blit(player2_surface, player2_rect)  # 玩家2名稱
            # 顯示分數
            screen.blit(score1_surface, score1_rect)  # 玩家1分數
            screen.blit(score2_surface, score2_rect)  # 玩家2分數
            # 顯示題目
            screen.blit(question_surface, question_rect)
            countstext = str(countdown)
            for event in pygame.event.get():
                # 顯示拍手
                # player1按 s 鍵，player2按 k 鍵
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        show = 1
                    elif event.key == pygame.K_k:
                        show = 2
                    elif event.key == pygame.K_1:
                        game1 = False
                # 關閉視窗
                if event.type == pygame.QUIT:
                   pygame.quit()
                if event.type == COUNT:
                    countdown = countdown - 1
                    countstext = str(countdown)
                    if countdown == -3:
                        game1 = False

            # 顯示拍手
            if show == 1:
                screen.blit(clap, (50, 350))
            elif show == 2:
                screen.blit(clap, (width - 50 - 260, 350))
            # 倒數
            if countdown > 0:
                show_time(countstext, countdown)
            else:
                show_end()
            pygame.display.update()

def game_2():
    game2 = True
    countdown = 100
    background, black, white = set_color()
    orange = (255, 147, 0)
    size = 140

    # 設定題目圖片
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
    
    number = 1
    while game2:
        #隨機產生0-7之亂數
        num = new_question(number)
        if number <= 5:
            number += 1
        #判斷是否為5-4圖示的index
        index = 0		
        #從1-1開始玩
        i, j, k, l = 0, 0, int(len(num)/2), 0
        while game2: # 遊戲迴圈
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
            show_icons(num, imagelist)
        
            # 顯示遮罩
            show_cover(num, image_cover, i + 1, player = 1)
            show_cover(num, image_cover, k - int(len(num)/2) + 1, player = 2)
            
            countstext = str(countdown)
            if countdown > 0:
                show_time(countstext, countdown)
            else:
                show_end()

            pygame.display.flip()

            if index == 1:  # if index == 0, 刷新題目
                break
            
            
            for event in pygame.event.get():
                # 玩家按下相對按鍵，題目變色
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_w and (num[i][j] == 0 or num[i][j] == 4))\
                        or (event.key == pygame.K_s and (num[i][j] == 1 or num[i][j] == 5))\
                        or (event.key == pygame.K_a and (num[i][j] == 2 or num[i][j] == 6))\
                        or (event.key == pygame.K_d and (num[i][j] == 3 or num[i][j] == 7)):
                        num[i][j] += 8  # 變成after的圖示
                        i, j, index = next_pos(num, i, j, index, player = 1)
                    elif (event.key == pygame.K_UP and (num[k][l] == 0 or num[k][l] == 4))\
                        or (event.key == pygame.K_DOWN and (num[k][l] == 1 or num[k][l] == 5))\
                        or (event.key == pygame.K_LEFT and (num[k][l] == 2 or num[k][l] == 6))\
                        or (event.key == pygame.K_RIGHT and (num[k][l] == 3 or num[k][l] == 7)):
                        num[k][l] += 8
                        k, l, index = next_pos(num, k, l, index, player = 2)
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == COUNT:
                    countdown = countdown - 1
                    countstext = str(countdown)
                    if countdown == -3:
                        game2 = False
            # 倒數


def game_3():
    game3 = True
    countdown = 30
    while game3:
        background, black, white = set_color()
        size = 140
        
        # 設定題目
        question_font = pygame.font.Font(None, 60)  # 字體大小 = 60
        question_surface = question_font.render('Question', False, black)  ## Question更改為隨機數字
        question_rect = question_surface.get_rect()
        question_rect.center = (width / 2, height / 2)
        # 設定拍手
        clap = pygame.image.load('clap.png')
        show = 0  # 不顯示拍手 ## 換新題目show要重設為0
        while game3:  # 遊戲迴圈
            screen.fill(background)
            # 顯示玩家
            pygame.draw.rect(screen, white, (20, 20, size, size + 20), 2)  # 玩家1頭像
            screen.blit(player1_surface, player1_rect)  # 玩家1名稱
            pygame.draw.rect(screen, white, (width - 20 - size, 20, size, 20 + size), 2)  # 玩家2頭像
            screen.blit(player2_surface, player2_rect)  # 玩家2名稱
            # 顯示分數
            screen.blit(score1_surface, score1_rect)  # 玩家1分數
            screen.blit(score2_surface, score2_rect)  # 玩家2分數
            # 顯示題目
            screen.blit(question_surface, question_rect)
            
            countstext = str(countdown)
            for event in pygame.event.get():
                # 顯示拍手
                # player1按 s 鍵，player2按 k 鍵
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        show = 1
                    elif event.key == pygame.K_k:
                        show = 2
                    elif event.key == pygame.K_1:
                        game3 = False
                # 關閉視窗
                if event.type == pygame.QUIT:
                     pygame.quit()
                if event.type == COUNT:
                    countdown = countdown - 1
                    countstext = str(countdown)
                    if countdown == -3:
                        game3 = False

            # 顯示拍手
            if show == 1:
                screen.blit(clap, (50, 350))
            elif show == 2:
                screen.blit(clap, (width - 50 - 260, 350))
                game3 = False
            # 倒數
            if countdown > 0:
                show_time(countstext, countdown)
            else:
                show_end()
            pygame.display.flip()


#main funtions
#建立視窗
width = 700
height = 600
button_x = 500
button_y = 500
screen = pygame.display.set_mode((width, height))
update_rect = pygame.Rect(0, 300, 700, 250)
pygame.display.set_caption('善挑')
# image_rule0 = pygame.image.load()
image_rule1 = pygame.image.load('第一關遊戲規則.png')
image_rule2 = pygame.image.load('第二關遊戲規則.png')
image_rule3 = pygame.image.load('第三關遊戲規則.png')
image_start_button = pygame.image.load('遊戲開始.png')
image_done_button = pygame.image.load('準備完成.png')
image_next_button = pygame.image.load('下一頁.png')
image_again_button = pygame.image.load('再來一次.png')
image_end_button = pygame.image.load('遊戲結束.png')

background, black, white = set_color()
size = 140
# 設定玩家
name1 = 'Name1'
name2 = 'Name2'
player1_surface, player1_rect = set_player(name1, 1)
player2_surface, player2_rect = set_player(name2, 2)
# 設定分數
score1 = 10
score2 = 20
score1_surface, score1_rect = set_score(score1, 1)
score2_surface, score2_rect = set_score(score2, 2)

#run
again = True
while again:
    again = False
    blank_window('Beginning', image_start_button, None)  # for 遊戲開始畫面
                                # game_intro(image_rule0)
    prepare_window('Information')  # for 輸入玩家資訊
    game_intro(image_rule1)
    game_1()  # 按數字 1 鍵會跳下一頁
    game_intro(image_rule2)
    game_2()  # 按數字 1 鍵會跳下一頁
    game_intro(image_rule3)
    game_3()  # 按數字 1 鍵會跳下一頁

    # 判斷輸家贏家
    wname, wscore = compared(name1, score1, name2, score2, 'w')
    lname, lscore = compared(name1, score1, name2, score2, 'l')
    
    result_window('Result')  # for 最終輸贏畫面
    board_window(wname, wscore, lname, lscore)  # for 排行榜
    again = again_window('Again?')
