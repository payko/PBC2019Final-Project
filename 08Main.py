##needs:
#1 第一關的計分問題
#2 遊戲畫面頭像
#3 RESULT的背景(WINNER vs LOSER)
#4 音效
#5 


import pygame, sys, os 
os.environ['SDL_VIDEO_CENTERED'] = '1' # centers Pygame SCREEN on desktop 
import csv
from PIL import Image
import cv2
import random
from pygame.locals import *

pygame.init()
COUNT = pygame.USEREVENT + 1
pygame.time.set_timer(COUNT, 1000)  # 每隔1秒發送一次自定義事件


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
    timeup = pygame.image.load('Time\'s up.png')
    screen.blit(timeup, (0, 0))

# functions for enter names:
def get_key(): 
    while 1: 
     for event in pygame.event.get(): 
      if event.type == pygame.KEYDOWN: 
       return event.key
      else: 
       pass 

def ask_name(player, name1, name2): 
    "ask(question) -> answer" 
    current_string = "" 
    display(current_string, name1, name2, player) 
    while True: 
        inkey = get_key() 
        if inkey == pygame.K_BACKSPACE: 
            current_string = current_string[:-1]
        elif inkey == pygame.K_RETURN or inkey == pygame.K_KP_ENTER: 
            break 
        elif inkey == pygame.K_ESCAPE: 
            pygame.quit()
        else: 
            current_string += chr(inkey)
        display(current_string.capitalize(), name1, name2, player) 

    return current_string.capitalize() # this is the answer

def display(message, name1, name2, player): 
    orange = (255, 147, 0)
    player1_face = pygame.image.load('player1.png')
    player2_face = pygame.image.load('player2.png')
    vs = pygame.image.load('vs.png')
    player1_face.convert()
    player2_face.convert()

    # 設定文字
    name_font = pygame.font.Font(None, 32)
    txt_font = pygame.font.Font(None, 30)
    nametxt1_surf = txt_font.render('Player 1: ____________', True, orange)
    nametxt2_surf = txt_font.render('(Press s to enter name)', True, orange)
    nametxt3_surf = txt_font.render('Player 2: ____________', True, orange)
    nametxt4_surf = txt_font.render('(Press k to enter name)', True, orange)
    
    screen.fill(background)
    screen.blit(player1_face, (30, 60))
    screen.blit(player2_face, (width - 300, 60)) #照片位置
    screen.blit(vs, (250, 0))
    screen.blit(nametxt1_surf, (35, 355))
    screen.blit(nametxt2_surf, (35, 375))
    screen.blit(nametxt3_surf, (width - 295, 355))
    screen.blit(nametxt4_surf, (width - 295, 375))
    
    if name1:
        screen.blit(name_font.render(name1, True, black), (125, 355))
    if name2:
        screen.blit(name_font.render(name2, True, black), (width - 205, 355))
    
    txt5_surf = txt_font.render('Press Enter when done', True, (255,160,50))
    if player == 1:
        screen.blit(txt5_surf, (35, 405))
    else:
        screen.blit(txt5_surf, (width - 295, 405))
    if len(message) != 0: 
        if player == 1:
            screen.blit(name_font.render(message, True, black), (125, 355)) 
        else:
            screen.blit(name_font.render(message, True, black), (width - 205, 355))

    pygame.display.update()

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

# functions for game1
def effect(random_, show, score1, score2):
    if random_ % 3 == 0 or '3' in str(random_):
        if show == 1:
            score1 += 2 # 加分音效
        elif show == 2:
            score2 += 2 # 加分音效
    else:
        if show == 1:
            score1 -= 1 # 扣分音效
        elif show == 2:
            score2 -= 1 # 扣分音效
            
    return score1, score2

# functions for game2
def show_icons(num, imagelist):
    # input: a list
    for i in range(len(num)):
        for j in range(4):
            if i < len(num) / 2:
                x = 30 + 75.3 * j
                y = 223 + 70 * i
            else:
                x = 380 + 75.3 * j
                y = 223 + 70 * (i - len(num) / 2)
            screen.blit(imagelist[num[i][j]], (x, y))

def show_cover(num, image_cover, active, player):
    for i in range(1, int(len(num) / 2) + 1):
        if i == active:
            continue
        if player == 1:
            x = 20
            y = 150 + 70 * i
        else:
            x = 370
            y = 150 + 70 * i
        screen.blit(image_cover, (x, y))  # 第二行遮罩

def next_pos(num, i, j, index, player):
    if player == 1:
        if j == 3:
            if i == len(num) / 2 - 1:
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

def new_question(number, questionnum):
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

# functions for game3
def effect3(random_word, random_color, show, score1, score2):
    word = ['RED', 'BLACK', 'GREEN', 'BLUE', 'PURPLE', 'GRAY', 'RED', 'BLACK', 'GREEN', 'BLUE', 'PURPLE', 'GRAY', 'RED', 'BLACK', 'GREEN', 'BLUE', 'PURPLE', 'GRAY', 'RED', 'BLACK', 'GREEN', 'BLUE', 'PURPLE', 'GRAY']
    color = [(255, 0, 0), (0, 0, 0), (0, 128, 0), (0, 0, 255), (128, 0, 128), (128, 128, 128)]  
     
    if (word.index(random_word) % 6) == color.index(random_color):
        if show == 1:
            score1 += 2 # 加分音效
        elif show == 2:
            score2 += 2 # 加分音效
    else:
        if show == 1:
            score1 -= 1 # 扣分音效
        elif show == 2:
            score2 -= 1 # 扣分音效
                    
    return score1, score2

# functions for create windows
def blank_window(string, image_button, background_image):
    stay = True
    screen.fill(background)
    if background_image != None:
        screen.blit(background_image, (0, 0))

    if string != None:
        output_font = pygame.font.Font(None, 60)  # 字體大小 = 60
        output_surface = output_font.render(string, True, black)
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
                if 500 < mouse[0] < 630 and 515 < mouse[1] < 565:  # 給button設定的範圍
                    stay = False
        screen.blit(image_button, (button_x, button_y))
        pygame.display.flip()
        mouse = pygame.mouse.get_pos()

def beginning_window():
    
    counter = 0
    running = True
    
    while running:
        screen.fill((0, 0, 0))
        screen.blit(background_pic1, (0, 0))
        if counter % 2 == 0:
            screen.blit(beginning_enter, (width / 2 - 120, height - 120))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == KEYDOWN and event.key == K_RETURN: # enter鍵
                running = False
            if event.type == COUNT:
                counter += 1
        pygame.display.update()

def prepare_window():
    red = (255, 0, 0)
    orange = (255, 147, 0)
    player1_face = pygame.image.load('player1.png')
    player2_face = pygame.image.load('player2.png')
    vs = pygame.image.load('vs.png')
    player1_face.convert()
    player2_face.convert()
    name1 = ""
    name2 = ""

    # 設定文字
    name_font = pygame.font.Font(None, 32)
    txt_font = pygame.font.Font(None, 30)
    nametxt1_surf = txt_font.render('Player 1: __________', True, orange)
    nametxt2_surf = txt_font.render('(Press s to enter name)', True, orange)
    nametxt3_surf = txt_font.render('Player 2: __________', True, orange)
    nametxt4_surf = txt_font.render('(Press k to enter name)', True, orange)

    stay = True
    bad = False
    while stay:
        screen.fill(background)
        screen.blit(player1_face, (30, 60))
        screen.blit(player2_face, (width - 300, 60)) #照片位置
        screen.blit(vs, (250, 0))
        screen.blit(nametxt1_surf, (35, 355))
        screen.blit(nametxt2_surf, (35, 375))
        screen.blit(nametxt3_surf, (width - 295, 355))
        screen.blit(nametxt4_surf, (width - 295, 375))
        if name1:
            screen.blit(name_font.render(name1, True, black), (125, 355))
        if name2:
            screen.blit(name_font.render(name2, True, black), (width - 205, 355))
        if bad:
            txt6_surf = txt_font.render('Please enter your names!', True, red)
            txt6_rect = txt6_surf.get_rect()
            txt6_rect.center = (width / 2, height - 150)
            screen.blit(txt6_surf, txt6_rect)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_s and name1 == "": 
                    name1 = ask_name(1, name1, name2)
                    if name1:
                        bad = False
                elif event.key == pygame.K_k and name2 == "":
                    name2 = ask_name(2, name1, name2)
                    if name2:
                        bad = False
            # 關閉視窗
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 500 < mouse[0] < 630 and 515 < mouse[1] < 565:  # 給Again button設定的範圍
                    if name1 == "" or name2 == "":
                        bad = True
                    else:
                        stay = False
        screen.blit(image_done_button, (button_x, button_y))
        pygame.display.flip()
        mouse = pygame.mouse.get_pos()
    return name1, name2

def game_intro(image_rule):
    blank_window(None, image_start_button, image_rule)

def result_window(string):
    blank_window(string, image_next_button, None)

def board_window(wn, ws, ln, ls):
    # input: 贏家名字、得分、輸家名字、得分
    stay = True
    screen.fill(background)
    screen.blit(image_boardbg, (0, 0))
    # 之後補上

    # 讀入舊的排行榜
    r_file = open('排行榜.csv', 'r', newline='', encoding='utf-8')
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
    w_file = open('排行榜.csv', 'w', newline='', encoding='utf-8')
    board_writer = csv.writer(w_file)
    for row in Board:
        board_writer.writerow(row)
    w_file.close()

    output_font = pygame.font.Font(None, 48)  # 字體大小 = 60
    for i in range(1, 7):
        player = str(Board[i][1])
        score = str(Board[i][2])
        if player:
            player_surface = output_font.render('{}'.format(player), True, black)
            player_rect = player_surface.get_rect()
            player_rect.center = (300, 230 + 50 * i)
            screen.blit(player_surface, player_rect)
            score_surface = output_font.render('{}'.format(score), True, black)
            score_rect = score_surface.get_rect()
            score_rect.center = (450, 230 + 50 * i)
            screen.blit(score_surface, score_rect)
    while stay:
        for event in pygame.event.get():
            # 關閉視窗
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 500 < mouse[0] < 630 and 515 < mouse[1] < 565:  # 給button設定的範圍
                    stay = False
        screen.blit(image_next_button, (button_x, button_y))
        pygame.display.flip()
        mouse = pygame.mouse.get_pos()

def again_window(string):
    stay = True
    screen.fill(background)
    output_font = pygame.font.Font(None, 60)  # 字體大小 = 60
    output_surface = output_font.render(string, True, black)
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
                if 500 < mouse[0] < 630 and 515 < mouse[1] < 565:  # 給Again button設定的範圍
                    again = True
                    stay = False
                elif 280 < mouse[0] < 430 and 515 < mouse[1] < 565:  # 給End button設定的範圍
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
    player_surface = player_font.render(name, True, black)
    player_rect = player_surface.get_rect()
    if num == 1:
        player_rect.center = (20 + size / 2, 20 + size + 20 + 20)
    else:
        player_rect.center = (width - 20 - size / 2, 20 + size + 20 + 20)
    return player_surface, player_rect

def set_scoretxt(score, num):
    background, black, white = set_color()
    size = 140
    # 設定分數
    score_font = pygame.font.Font(None, 32)  # 字體大小 = 32
    score_surface = score_font.render(str(score), True, black)  # 玩家1分數
    score_rect = score_surface.get_rect()
    if num == 1:
        score_rect.center = (20 + size + 50, 50)
    else:
        score_rect.center = (width - 20 - size - 50, 50)
    return score_surface, score_rect

def set_score(score):
    score_font = pygame.font.Font(None, 50)
    score_surf = score_font.render(str(score), True, (0, 0, 0))
    return score_surf

# for game runnung
def game_1(score1, score2):
    game1 = True
    countdown = 60
    
    background, black, white = set_color()
    size = 140
    player_font = pygame.font.Font(None, 32)

    # 設定題目
    random_ = random.randint(0,1000)
    question_font = pygame.font.Font(None, 60)  # 字體大小 = 60
    question_surface = question_font.render(str(random_), True, black)  # Question更改為隨機數字
    question_rect = question_surface.get_rect()
    question_rect.center = (width / 2, height / 2)

    # 設定分數
    score1txt_surface, score1txt_rect = set_scoretxt('Score1', 1)
    score2txt_surface, score2txt_rect = set_scoretxt('Score2', 2)

    # 設定拍手
    clap = pygame.image.load('clap.png')
    show = 0  # 不顯示拍手 ## 換新題目show要重設為0
        
    start = pygame.time.get_ticks() #開啟程式到按下開始鍵經過的時間 也就是閱讀遊戲規則的時間
    last = 0
     
    while game1:
        screen.fill(background)
                
        # 顯示玩家
        pygame.draw.rect(screen, white, (20, 20, size, size + 20), 2)  # 玩家1頭像
        screen.blit(player1_surface, player1_rect)  # 玩家1名稱
        pygame.draw.rect(screen, white, (width - 20 - size, 20, size, 20 + size), 2)  # 玩家2頭像                screen.blit(player2_surface, player2_rect)  # 玩家2名稱
        screen.blit(player2_surface, player2_rect)  # 玩家2名稱

        time = pygame.time.get_ticks()  #開啟程式後經過的時間
        
        #顯示分數
        screen.blit(score1txt_surface, score1txt_rect)  # 玩家1分數
        screen.blit(score2txt_surface, score2txt_rect)  # 玩家2分數
        score1_surface = set_score(score1)
        screen.blit(score1_surface, (200,80))
        score2_surface = set_score(score2)
        screen.blit(score2_surface, (480,80))
            
        countstext = str(countdown)
        if countdown > 0:
            show_time(countstext, countdown)
        else:
            show_end()
        # 顯示題目
        if countdown > 0:
            screen.blit(question_surface, question_rect)
        if (((time - start)//1000) % 2) == 0 and ((time - start)//1000) != last: #每2秒換一個數字
            last = (time - start) // 1000
            random_ = random.randint(0,1000)
            question_surface = question_font.render('{}'.format(str(random_)), True, black)  # Question更改為隨機數字
            question_rect = question_surface.get_rect()
            question_rect.center = (width / 2, height / 2)
            if countdown > 0:
                screen.blit(question_surface, question_rect)
            pygame.display.flip()
            show = 0
            continue
        else:
            for event in pygame.event.get():
            # player1按 s 鍵，player2按 k 鍵
                if event.type == pygame.KEYDOWN and countdown > 0:
                    if event.key == pygame.K_s:
                        show = 1
                        score1, score2 = effect(random_, show, score1, score2)
                        score1_surface = player_font.render(str(score1), True, black)  # 玩家1分數
                    elif event.key == pygame.K_k:
                        show = 2
                        score1, score2 = effect(random_, show, score1, score2)
                        score2_surface = player_font.render(str(score2), True, black)  # 玩家2分數                        # 關閉視窗
                elif event.type == pygame.QUIT:
                    pygame.quit()
                # 倒數
                elif event.type == COUNT:
                    countdown = countdown - 1
                    countstext = str(countdown)
                    if countdown == -3:
                        game1 = False
            # 顯示拍手
            if show == 1:
                screen.blit(clap, (50, 350))
            elif show == 2:
                screen.blit(clap, (width - 50 - 260, 350))

        pygame.display.flip()

    return score1, score2

def game_2(score1, score2):
    game2 = True
    countdown = 90
    background, black, white = set_color()
    orange = (255, 147, 0)
    size = 140

    # 設定分數
    score1txt_surface, score1txt_rect = set_scoretxt('Score1', 1)
    score2txt_surface, score2txt_rect = set_scoretxt('Score2', 2)

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
                 image_down_before_reverse, image_up_before_reverse, image_right_before_reverse,
                 image_left_before_reverse,
                 image_up_after, image_down_after, image_left_after, image_right_after,
                 image_down_after_reverse, image_up_after_reverse, image_right_after_reverse, image_left_after_reverse]

    questionnum = 1 #第幾題了
    number = 1 #總共幾排
    while game2:
        # 隨機產生0-7之亂數
        num = new_question(number, questionnum)
        if questionnum < 10:
            questionnum += 1
        if number < 5:
            number += 1
        # 判斷是否為5-4圖示的index
        index1 = 0
        index2 = 0
        # 從1-1開始玩
        i, j, k, l = 0, 0, int(len(num) / 2), 0
        while game2:  # 遊戲迴圈
            screen.fill(background)
            # 顯示玩家
            pygame.draw.rect(screen, white, (20, 20, size, size + 20), 2)  # 玩家1頭像
            screen.blit(player1_surface, player1_rect)  # 玩家1名稱
            pygame.draw.rect(screen, white, (width - 20 - size, 20, size, 20 + size), 2)  # 玩家2頭像
            screen.blit(player2_surface, player2_rect)  # 玩家2名稱
            
            # 顯示分數
            screen.blit(score1txt_surface, score1txt_rect)  # 玩家1分數
            screen.blit(score2txt_surface, score2txt_rect)  # 玩家2分數

            # 顯示題目
            pygame.draw.rect(screen, orange, (20, 220, width / 2 - 40, 350), 2)  # 玩家1題目框框 310*350
            pygame.draw.rect(screen, orange, (width / 2 + 20, 220, width / 2 - 40, 350), 2)  # 玩家2題目框框 310*350

            # 顯示圖示
            show_icons(num, imagelist)

            # 顯示遮罩
            show_cover(num, image_cover, i + 1, player=1)
            show_cover(num, image_cover, k - int(len(num) / 2) + 1, player=2)

            #顯示分數
            score_surf = set_score(score1)
            screen.blit(score_surf, (200,80))
            score_surf = set_score(score2)
            screen.blit(score_surf, (480,80))

            countstext = str(countdown)
            if countdown > 0:
                show_time(countstext, countdown)
            else:
                show_end()

            pygame.display.flip()

            if index1 == 1:
                score1 += 3 #正確音效
                break
            if index2 == 1:
                score2 += 3 #正確音效
                break

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and countdown > 0: 
                    #玩家1輸入時
                    if event.key == pygame.K_w:
                        if num[i][j] == 0 or num[i][j] == 4:
                            num[i][j] += 8  # 變成after的圖示&簡易音效
                            i, j, index1 = next_pos(num, i, j, index1, player = 1)
                        elif num[i][j] != 0 or num[i][j] != 4:
                            score1 -= 1 #錯誤分數-1&音效
                    if event.key == pygame.K_s:
                        if num[i][j] == 1 or num[i][j] == 5:
                            num[i][j] += 8  # 變成after的圖示&簡易音效
                            i, j, index1 = next_pos(num, i, j, index1, player = 1)
                        elif num[i][j] != 1 or num[i][j] != 5:
                            score1 -= 1   #錯誤分數-1&音效
                    if event.key == pygame.K_a:
                        if num[i][j] == 2 or num[i][j] == 6:
                            num[i][j] += 8  # 變成after的圖示&簡易音效
                            i, j, index1 = next_pos(num, i, j, index1, player = 1)
                        elif num[i][j] != 2 or num[i][j] != 6:
                            score1 -= 1  #錯誤分數-1&音效
                    if event.key == pygame.K_d:
                        if num[i][j] == 3 or num[i][j] == 7:
                            num[i][j] += 8  # 變成after的圖示&簡易音效
                            i, j, index1 = next_pos(num, i, j, index1, player = 1)
                        elif num[i][j] != 3 or num[i][j] != 7:
                            score1 -= 1 #錯誤分數-1&音效
                    #玩家2輸入時
                    if event.key == pygame.K_UP:
                        if num[k][l] == 0 or num[k][l] == 4:
                            num[k][l] += 8  # 變成after的圖示&簡易音效
                            k, l, index2 = next_pos(num, k, l, index2, player = 2)
                        elif num[i][j] != 0 or num[i][j] != 4:
                            score2 -= 1 #錯誤分數-1&音效
                    if event.key == pygame.K_DOWN:
                        if num[k][l] == 1 or num[k][l] == 5:
                            num[k][l] += 8  # 變成after的圖示&簡易音效
                            k, l, index2 = next_pos(num, k, l, index2, player = 2)
                        elif num[i][j] != 1 or num[i][j] != 5:
                            score2 -= 1 #錯誤分數-1&音效
                    if event.key == pygame.K_LEFT:
                        if num[k][l] == 2 or num[k][l] == 6:
                            num[k][l] += 8  # 變成after的圖示&簡易音效
                            k, l, index2 = next_pos(num, k, l, index2, player = 2)
                        elif num[i][j] != 2 or num[i][j] != 6:
                            score2 -= 1 #錯誤分數-1&音效
                    if event.key == pygame.K_RIGHT:
                        if num[k][l] == 3 or num[k][l] == 7:
                            num[k][l] += 8  # 變成after的圖示&簡易音效
                            k, l, index2 = next_pos(num, k, l, index2, player = 2)
                        elif num[i][j] != 3 or num[i][j] != 7:
                            score2 -= 1 #錯誤分數-1&音效
                if event.type == pygame.QUIT:
                    pygame.quit()
                # 倒數
                if event.type == COUNT:
                    countdown = countdown - 1
                    countstext = str(countdown)
                    if countdown == -3:
                        game2 = False
    return score1, score2

def game_3(score1, score2):
    game3 = True
    countdown = 50
    background, black, white = set_color()
    size = 140
    player_font = pygame.font.Font(None, 32)

    # 設定分數
    score1txt_surface, score1txt_rect = set_scoretxt('Score1', 1)
    score2txt_surface, score2txt_rect = set_scoretxt('Score2', 2)

    # 設定題目
    random_word = random.choice(['RED', 'BLACK', 'GREEN', 'BLUE', 'PURPLE', 'GRAY', 'RED', 'BLACK', 'GREEN', 'BLUE', 'PURPLE', 'GRAY', 'RED', 'BLACK', 'GREEN', 'BLUE', 'PURPLE', 'GRAY', 'RED', 'BLACK', 'GREEN', 'BLUE', 'PURPLE', 'GRAY'])
    random_color = random.choice([(255, 0, 0), (0, 0, 0), (0, 128, 0), (0, 0, 255), (128, 0, 128), (128, 128, 128)])
    question_font = pygame.font.Font(None, 60)  # 字體大小 = 60
    question_surface = question_font.render(str(random_word), True, random_color)  # Question更改為隨機單字
    question_rect = question_surface.get_rect()
    question_rect.center = (width / 2, height / 2)
        
    # 設定拍手
    clap = pygame.image.load('clap.png')
    show = 0  # 不顯示拍手 ## 換新題目show要重設為0
    start = pygame.time.get_ticks() #開啟程式到按下開始鍵經過的時間 也就是閱讀遊戲規則的時間
    last = 0
    while game3:
        screen.fill(background)

        # 顯示玩家
        pygame.draw.rect(screen, white, (20, 20, size, size + 20), 2)  # 玩家1頭像
        screen.blit(player1_surface, player1_rect)  # 玩家1名稱
        pygame.draw.rect(screen, white, (width - 20 - size, 20, size, 20 + size), 2)  # 玩家2頭像
        screen.blit(player2_surface, player2_rect)  # 玩家2名稱
                
        time = pygame.time.get_ticks()  #開啟程式後經過的時間
        
        #顯示分數
        screen.blit(score1txt_surface, score1txt_rect)  # 玩家1分數
        screen.blit(score2txt_surface, score2txt_rect)  # 玩家2分數
        score1_surface = set_score(score1)
        screen.blit(score1_surface, (200,80))
        score2_surface = set_score(score2)
        screen.blit(score2_surface, (480,80))
        
        countstext = str(countdown)
        if countdown > 0:
            show_time(countstext, countdown)
            screen.blit(question_surface, question_rect)
        else:
            show_end()

        if (((time - start)//1000) % 0.5) == 0 and ((time - start)//1000) != last: #每半秒換一次題目
            last = (time - start) // 1000
            random_word = random.choice(['RED', 'BLACK', 'GREEN', 'BLUE', 'PURPLE', 'GRAY'])
            random_color = random.choice([(255, 0, 0), (0, 0, 0), (0, 128, 0), (0, 0, 255), (128, 0, 128), (128, 128, 128)])
            question_surface = question_font.render(str(random_word), True, random_color)  # Question更改為隨機單字
            question_rect = question_surface.get_rect()
            question_rect.center = (width / 2, height / 2)
            if countdown > 0:
                screen.blit(question_surface, question_rect)
            pygame.display.flip()
            show = 0
            continue
        else:
            for event in pygame.event.get():
            # player1按 s 鍵，player2按 k 鍵
                if event.type == pygame.KEYDOWN and countdown > 0:
                    if event.key == pygame.K_s:
                        show = 1
                        score1, score2 = effect3(random_word, random_color, show, score1, score2)
                        score1_surface = player_font.render(str(score1), True, black)  # 玩家1分數
                    elif event.key == pygame.K_k:
                        show = 2
                        score1, score2 = effect3(random_word, random_color, show, score1, score2)
                        score2_surface = player_font.render(str(score2), True, black)  # 玩家2分數    
                # 關閉視窗
                elif event.type == pygame.QUIT:
                    pygame.quit()
                # 倒數
                elif event.type == COUNT:
                    countdown = countdown - 1
                    countstext = str(countdown)
                    if countdown == -3:
                        game3 = False
            # 顯示拍手
            if show == 1:
                screen.blit(clap, (50, 350))
            elif show == 2:
                screen.blit(clap, (width - 50 - 260, 350))
    
        pygame.display.flip()
    
    return score1, score2

# functions for photos
def rescale_frame(frame, percent=75):
    '''調整鏡頭大小'''
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

def capture():
    take = True
    times = 2 # 拍兩次後自動關閉
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("webcam")
    img_counter = 0

    while take:
        ret, frame = cam.read()
        frame = rescale_frame(frame, percent=30)

        if times == 2:
            cv2.imshow("Player1!", frame)
        else:
            cv2.imshow("Player2!", frame)

        if not ret:
            take = False
        k = cv2.waitKey(1)

        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            take = False
        elif k % 256 == 32:
            # SPACE pressed
            times -= 1
            img_name = "capture_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
        if times == 0:
            take = False

    cam.release()
    cv2.destroyAllWindows()

def croppic():
    img_player1 = Image.open('capture_0.png')
    img_player2 = Image.open('capture_1.png')
    white = Image.open('white.png')
    newimg_player1 = img_player1.crop((70, 0, 314, 200)) # 左上右下
    newimg_player2 = img_player2.crop((70, 0, 314, 200))
    white.paste(newimg_player1, (10, 10))
    white.save('player1.png')
    white.paste(newimg_player2, (10, 10))
    white.save('player2.png')

def intro_0():
    screen.blit(intro_background, (0, 0))
    running = True


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_RETURN: # enter鍵
                running = False
        pygame.display.update()


# main funtions
# 建立視窗
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
image_boardbg = pygame.image.load('排行榜.png')
background_pic1 = pygame.image.load('background_pic1.png')
background_pic2 = pygame.image.load('background_pic2.jpg')
beginning_enter = pygame.image.load('beginingenter.png')
intro_background = pygame.image.load('introbg.png')


background, black, white = set_color()
size = 140
# 設定玩家
name1 = 'Name1'
name2 = 'Name2'

# 設定分數
score1 = 0
score2 = 0

# run
again = True
while again:
    again = False
    #blank_window('Beginning', image_start_button, None)  # for 遊戲開始畫面
    beginning_window()
    intro_0()
    # game_intro(image_rule0)
    capture()
    croppic()
    name1, name2 = prepare_window()  # for 輸入玩家資訊
    player1_surface, player1_rect = set_player(name1, 1)
    player2_surface, player2_rect = set_player(name2, 2)
    
    game_intro(image_rule1)
    score1, score2 = game_1(score1, score2)  # 按數字 1 鍵會跳下一頁
    
    game_intro(image_rule2)
    score1, score2 = game_2(score1, score2)  # 按數字 1 鍵會跳下一頁
    game_intro(image_rule3)
    score1, score2 = game_3(score1, score2)  # 按數字 1 鍵會跳下一頁
    
    # 判斷輸家贏家
    wname, wscore = compared(name1, score1, name2, score2, 'w')
    lname, lscore = compared(name1, score1, name2, score2, 'l')

    result_window('Result')  # for 最終輸贏畫面
    board_window(wname, wscore, lname, lscore)  # for 排行榜
    again = again_window('Again?')
