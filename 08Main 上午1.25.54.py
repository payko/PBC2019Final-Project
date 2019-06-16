import pygame, sys, os, csv, cv2, random
from PIL import Image
from pygame.locals import *

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'  # 將 Pygame 視窗呈現在桌面中央

# 時間紀錄
COUNT = pygame.USEREVENT+1
pygame.time.set_timer(COUNT, 1000)  # 每隔1秒發送一次自定義事件

class Beginning_window():

    def __init__(self):
        # 設定音效
        play_game = pygame.mixer.Sound('play game.wav')  # 奪魂鋸音效
        pygame.mixer.Sound.play(play_game)

        # 設定圖片
        bg = pygame.image.load('beginning_bg.png')
        enter = pygame.image.load('beginning_enter.png')

        counter = 0  # 時間紀錄
        running = True

        while running:
            screen.blit(bg, (0,0))

            if counter % 2 == 0:  # press enter字樣閃爍
                screen.blit(enter, (width/2 - 120, height - 120))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == COUNT:  # 每過一秒counter加一
                    counter += 1
                if event.type == KEYDOWN and event.key == K_RETURN:  # enter鍵
                    pygame.mixer.Sound.play(select)  # 按鍵音效
                    running = False

            pygame.display.update()

class Intro_window():

    def __init__(self):
        intro_background = pygame.image.load('intro_bg.png')  # 背景圖片
        running = True

        while running:
            screen.blit(intro_background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == KEYDOWN and event.key == K_RETURN:  # enter鍵
                    pygame.mixer.Sound.play(select)  # 按鍵音效
                    running = False

            pygame.display.update()

class Photo():

    def __init__(self):
        self.capture()
        self.croppic()

    def capture(self):
        take = True
        times = 2 # 拍兩次後自動關閉
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("webcam")
        img_counter = 0

        while take:
            ret, frame = cam.read()
            frame = self.rescale_frame(frame, percent=30)

            if times == 2:
                cv2.imshow("Player1!", frame)
            else:
                cv2.imshow("Player2!", frame)

            if not ret:
                take = False
            k = cv2.waitKey(1)

            if k % 256 == 27:
                # ESC pressed
                take = False
            elif k % 256 == 32:
                # SPACE pressed
                times -= 1
                img_name = "capture_{}.png".format(img_counter)
                cv2.imwrite(img_name, frame)
                img_counter += 1
            if times == 0:
                take = False

        cam.release()
        cv2.destroyAllWindows()

    def rescale_frame(self, frame, percent=75):
        '''調整鏡頭大小'''
        width = int(frame.shape[1] * percent/ 100)
        height = int(frame.shape[0] * percent/ 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    def croppic(self):
        img_player1 = Image.open('capture_0.png')
        img_player2 = Image.open('capture_1.png')
        white = Image.open('white.png')
        newimg_player1 = img_player1.crop((70, 0, 314, 200)) # 左上右下
        newimg_player2 = img_player2.crop((70, 0, 314, 200))
        white.paste(newimg_player1, (10, 10))
        white.save('player1.png')
        white.paste(newimg_player2, (10, 10))
        white.save('player2.png')
        '''image for gaming'''
        player1 = Image.open('player1.png')
        player2 = Image.open('player2.png')
        forgame_player1 = player1.resize((132, 110), Image.ANTIALIAS)
        forgame_player2 = player2.resize((132, 110), Image.ANTIALIAS)
        forgame_player1.save('forgame_player1.png')
        forgame_player2.save('forgame_player2.png')

        # 設定玩家頭像照片
        global player1_face
        global player2_face
        player1_face = pygame.image.load('player1.png')
        player2_face = pygame.image.load('player2.png')
        global player1_image
        global player2_image
        player1_image = pygame.image.load('forgame_player1.png')
        player2_image = pygame.image.load('forgame_player2.png')
        player1_face.convert()
        player2_face.convert()

class Prepare_window():

    def __init__(self):
        # 設定字型
        self.name_font = pygame.font.SysFont('comicsansmsttf', 25)
        self.txt_font = pygame.font.SysFont('comicsansmsttf', 20)

        # 設定名字
        self.name1, self.name2 = "", ""

        # 設定文字
        self.nametxt1_surf = self.txt_font.render('Player 1: __________', True, black)
        self.nametxt2_surf = self.txt_font.render('(Press s to enter name)', True, black)
        self.nametxt3_surf = self.txt_font.render('Player 2: __________', True, black)
        self.nametxt4_surf = self.txt_font.render('(Press k to enter name)', True, black)

        # 設定圖片
        self.vs = pygame.image.load('vs.png')
        self.ready_button = pygame.image.load('準備完成.png')

        self.operating()

        # 設定玩家資訊、頭像位置
        global name1
        global name2
        name1, name2 = self.name1, self.name2
        global player1_surface
        global player1_rect
        global player2_surface
        global player2_rect
        player1_surface, player1_rect = self.set_player(1)
        player2_surface, player2_rect = self.set_player(2)

    def operating(self):
        stay = True
        bad = False

        while stay:
            self.bg()

            if bad:
                txt6_surf = self.txt_font.render('Please enter your names!', True, red)
                txt6_rect = txt6_surf.get_rect()
                txt6_rect.center = (width / 2, height - 100)
                screen.blit(txt6_surf, txt6_rect)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:  # 輸入名字
                    if event.key == pygame.K_s and self.name1 == "":
                        self.name1 = self.ask_name(1)
                        if self.name1:
                            bad = False
                    elif event.key == pygame.K_k and self.name2 == "":
                        self.name2 = self.ask_name(2)
                        if self.name2:
                            bad = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 500 < mouse[0] < 630 and 515 < mouse[1] < 565:  # 給ready button設定的範圍
                        if self.name1 == "" or self.name2 == "":
                            bad = True
                        else:
                            pygame.mixer.Sound.play(select)  # 按鍵音效
                            stay = False

            pygame.display.flip()
            mouse = pygame.mouse.get_pos()

    def bg(self):
        screen.blit(image_background, (0, 0))
        screen.blit(self.ready_button, (button_x, button_y))
        screen.blit(player1_face, (30, 60))
        screen.blit(player2_face, (width - 300, 60))
        screen.blit(self.vs, (250, 0))
        screen.blit(self.nametxt1_surf, (35, 400))
        screen.blit(self.nametxt2_surf, (35, 420))
        screen.blit(self.nametxt3_surf, (width - 295, 400))
        screen.blit(self.nametxt4_surf, (width - 295, 420))
        self.already()

    def get_key(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return event.key
                else:
                    pass

    def ask_name(self, player):
        "ask(question) -> answer"
        current_string = ""  # 用來記輸入的字串
        while True:
            self.display(current_string.capitalize(), player)  # 每輸入(或刪除)一個字母就刷新一次頁面
            inkey = self.get_key()
            if inkey == pygame.K_BACKSPACE:
                current_string = current_string[:-1]
            elif inkey == pygame.K_RETURN or inkey == pygame.K_KP_ENTER:
                break
            elif inkey == pygame.K_ESCAPE:
                pygame.quit()
            else:
                current_string += chr(inkey)
        return current_string.capitalize()

    def display(self, message, player):  # 顯示正在輸入的名字
        self.bg()

        txt5_surf = self.txt_font.render('Press Enter when done', True, black)
        if player == 1:
            screen.blit(txt5_surf, (35, 450))
        else:
            screen.blit(txt5_surf, (width - 295, 450))

        # 顯示正在輸入的字串
        if len(message) != 0:
            if player == 1:
                screen.blit(self.name_font.render(message, True, black), (125, 397))
            else:
                screen.blit(self.name_font.render(message, True, black), (width - 205, 397))

        pygame.display.update()

    def already(self):  # 顯示已經輸入好的名字
        if self.name1:
            screen.blit(self.name_font.render(self.name1, True, black), (125, 397))
        if self.name2:
            screen.blit(self.name_font.render(self.name2, True, black), (width - 205, 397))

    def set_player(self, num):  # 設定玩家名稱
        global size
        size = 140  # 頭像寬
        player_font = pygame.font.Font(None, 32)  # 字體大小 = 32
        if num == 1:
            player_surface = player_font.render(self.name1, True, black)
            player_rect = player_surface.get_rect()
            player_rect.center = (20 + size/2, 150)
        else:
            player_surface = player_font.render(self.name2, True, black)
            player_rect = player_surface.get_rect()
            player_rect.center = (width - 20 - size/2, 150)
        return player_surface, player_rect

class Game_intro():

    def window(self, image_rule):
        # 顯示背景
        screen.blit(image_rule, (0, 0))
        start_button = pygame.image.load('遊戲開始.png')
        screen.blit(start_button, (button_x, button_y))

        stay = True

        while stay:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 500 < mouse[0] < 630 and 515 < mouse[1] < 565:  # 給button設定的範圍
                        pygame.mixer.Sound.play(select)  # 點選音效
                        stay = False

            pygame.display.flip()
            mouse = pygame.mouse.get_pos()

class Three_games():

    def same(self):
        screen.blit(image_background, (0, 0))
        self.show_scoretxt('Score1', 1)
        self.show_scoretxt('Score2', 2)
        self.show_player()
        self.show_score()

    def show_scoretxt(self, score, num):  # 顯示Score字樣
        score_font = pygame.font.Font(None, 32)  # 字體大小 = 32
        score_surface = score_font.render(str(score), True, black)
        score_rect = score_surface.get_rect()
        if num == 1:
            score_rect.center = (20 + size + 50, 50)
        else:
            score_rect.center = (width - 20 - size - 50, 50)
        screen.blit(score_surface, score_rect)

    def show_player(self):  # 顯示頭像、名稱
        screen.blit(player1_image, (20, 20))  # 玩家1頭像
        screen.blit(player1_surface, player1_rect)  # 玩家1名稱
        screen.blit(player2_image, (width/2 + 200, 20))  # 玩家2頭像
        screen.blit(player2_surface, player2_rect)  # 玩家2名稱

    def show_score(self):  # 顯示分數
        score_font = pygame.font.Font(None, 50)
        score1_surface = score_font.render(str(score1), True, black)
        score2_surface = score_font.render(str(score2), True, black)
        screen.blit(score1_surface, (195,80))
        screen.blit(score2_surface, (480,80))

    def show_end(self):  # 顯示時間到
        timeup = pygame.image.load('Time\'s up.png')
        timeup_rect = timeup.get_rect()
        timeup_rect.center = (width/2, height/2)
        screen.blit(timeup, timeup_rect)

    def show_time(self, text, countdown):  # 顯示時間倒數
        font = pygame.font.Font(None, 60)
        font_big = pygame.font.Font(None, 80)
        if countdown <= 3:  # 倒數3秒內變紅字
            clock_surface = font_big.render(text, True, red)
        else:
            clock_surface = font.render(text, True, black)
        clock_rect = clock_surface.get_rect()
        clock_rect.center = (width/2, 130)
        screen.blit(clock_surface, clock_rect)

class Game_1():
    def __init__(self):
        # 設定拍手
        self.clap = pygame.image.load('clap.png')
        self.show = 0  # 不顯示拍手 ## 換新題目show要重設為0

        self.operating()

    def operating(self):
        start = pygame.time.get_ticks() #開啟程式到按下開始鍵經過的時間 也就是閱讀遊戲規則的時間
        last = 0
        getpoints = False

        countdown = 63
        play = 0  # time_up音效播放
        game1 = True
        while game1:
            Three_games().same()
            time = pygame.time.get_ticks()  #開啟程式後經過的時間

            # 倒數計時器
            countstext = str(countdown)
            if countdown > 60:
                Three_games().show_time(str(countdown - 60), countdown - 60)
            elif countdown > 0:
                Three_games().show_time(countstext, countdown)
                if (((time - start)//1000) % 2) == 0 and ((time - start)//1000) != last:
                    pass
                else:
                    screen.blit(self.question_surface, self.question_rect)
            else:
                if countdown == 0 and play == 0:  # time_up音效
                    pygame.mixer.Sound.play(time_up)
                    play = 1
                Three_games().show_end()

            if (((time - start)//1000) % 2) == 0 and ((time - start)//1000) != last:  # 每2秒換一個數字
                last = (time - start) // 1000
                # 設定題目
                self.random_ = random.randint(0, 1000)
                self.question_font = pygame.font.Font(None, 60)  # 字體大小 = 60
                self.question_surface = self.question_font.render(str(self.random_), True, black)  # Question更改為隨機數字
                self.question_rect = self.question_surface.get_rect()
                self.question_rect.center = (width/2, height/2)
                if 0 < countdown <= 60:
                    screen.blit(self.question_surface, self.question_rect)
                pygame.display.flip()
                self.show = 0
                getpoints = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and countdown > 0 and countdown <= 60:  # player1按 s 鍵，player2按 k 鍵
                        if event.key == pygame.K_s and getpoints == False:
                            self.show = 1
                            self.effect()
                            getpoints = True
                        elif event.key == pygame.K_k and getpoints == False:
                            self.show = 2
                            self.effect()
                            getpoints = True
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == COUNT:
                        countdown -= 1
                        if countdown == -3:
                            game1 = False
                # 顯示拍手
                if self.show == 1:
                    screen.blit(self.clap, (50, 350))
                elif self.show == 2:
                    screen.blit(self.clap, (width - 50 - 260, 350))

            pygame.display.flip()

    def effect(self):
        global score1
        global score2
        if self.random_ % 3 == 0 or '3' in str(self.random_):
            if self.show == 1:
                score1 += 2
                pygame.mixer.Sound.play(correct)
            elif self.show == 2:
                score2 += 2
                pygame.mixer.Sound.play(correct)
        else:
            if self.show == 1:
                score1 -= 1
                pygame.mixer.Sound.play(wrong)
            elif self.show == 2:
                score2 -= 1
                pygame.mixer.Sound.play(wrong)

class Game_2:
    def __init__(self):
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
        self.image_cover = pygame.image.load('遮罩.png')
        self.imagelist = [image_up_before, image_down_before, image_left_before, image_right_before,
                     image_down_before_reverse, image_up_before_reverse, image_right_before_reverse,
                     image_left_before_reverse,
                     image_up_after, image_down_after, image_left_after, image_right_after,
                     image_down_after_reverse, image_up_after_reverse, image_right_after_reverse, image_left_after_reverse]

        # 設定題目難度
        self.number = 1 #總共幾排
        self.questionnum = 1 #第幾題了

        self.operating()

    def operating(self):
            global score1
            global score2

            countdown = 93
            play = 0  # time_up音效播放
            game2 = True

            while game2:
                self.new_question()  # 隨機產生0-7之亂數

                # 設定題目難度
                if self.questionnum < 10:
                    self.questionnum += 1
                if self.number < 5:
                    self.number += 1

                # 判斷是否為5-4圖示的index
                self.index1 = 0
                self.index2 = 0

                # 從1-1開始玩
                i, j, k, l = 0, 0, int(len(self.num)/2), 0

                # 圖片是否閃爍
                self.flash1 = 0
                self.flash2 = 0

                # 閃爍圖片位置
                self.not_show_i = -1
                self.not_show_j = -1
                self.not_show_k = -1
                self.not_show_l = -1

                while game2:
                    Three_games().same()
                    pygame.draw.rect(screen, orange, (20, 220, width/2 - 40, 350), 2)  # 玩家1題目框框 310*350
                    pygame.draw.rect(screen, orange, (width/2 + 20, 220, width/2 - 40, 350), 2)  # 玩家2題目框框 310*350

                    # 顯示圖示
                    if countdown <= 90:
                        self.show_icons()

                    # 顯示遮罩
                    self.show_cover(i+1, 1)
                    self.show_cover(k-int(len(self.num)/2)+1, 2)

                    # 倒數計時器
                    countstext = str(countdown)
                    if countdown > 90:
                        Three_games().show_time(str(countdown - 90), countdown - 90)
                    elif countdown > 0:
                        Three_games().show_time(countstext, countdown)
                    else:
                        if countdown == 0 and play == 0: # time_up音效
                            pygame.mixer.Sound.play(time_up)
                            play = 1
                        Three_games().show_end()
                    pygame.display.flip()

                    # 玩家得分
                    if self.index1 == 1:
                        score1 += 3
                        pygame.mixer.Sound.play(correct) #正確音效
                        break
                    if self.index2 == 1:
                        score2 += 3
                        pygame.mixer.Sound.play(correct) #正確音效
                        break

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and 0 < countdown <= 90:
                            #玩家1輸入時
                            if event.key == pygame.K_w:
                                if self.num[i][j] == 0 or self.num[i][j] == 4:
                                    self.num[i][j] += 8  # 變成after的圖示
                                    i, j= self.next_pos(i, j, player = 1)
                                elif self.num[i][j] != 0 or self.num[i][j] != 4:
                                    score1 -= 1  # 錯誤分數-1&音效
                                    self.flash1 = 1  # 圖示閃爍
                                    self.not_show_i, self.not_show_j = i, j  # 閃爍圖示的位置
                                    pygame.mixer.Sound.play(wrong)
                            if event.key == pygame.K_s:
                                if self.num[i][j] == 1 or self.num[i][j] == 5:
                                    self.num[i][j] += 8  # 變成after的圖示
                                    i, j= self.next_pos(i, j, player = 1)
                                elif self.num[i][j] != 1 or self.num[i][j] != 5:
                                    score1 -= 1    # 錯誤分數-1&音效
                                    self.flash1 = 1  # 圖示閃爍
                                    self.not_show_i, self.not_show_j = i, j  # 閃爍圖示的位置
                                    pygame.mixer.Sound.play(wrong)
                            if event.key == pygame.K_a:
                                if self.num[i][j] == 2 or self.num[i][j] == 6:
                                    self.num[i][j] += 8  # 變成after的圖示
                                    i, j= self.next_pos(i, j, player = 1)
                                elif self.num[i][j] != 2 or self.num[i][j] != 6:
                                    score1 -= 1   # 錯誤分數-1&音效
                                    self.flash1 = 1  # 圖示閃爍
                                    self.not_show_i, self.not_show_j = i, j  # 閃爍圖示的位置
                                    pygame.mixer.Sound.play(wrong)
                            if event.key == pygame.K_d:
                                if self.num[i][j] == 3 or self.num[i][j] == 7:
                                    self.num[i][j] += 8  # 變成after的圖示
                                    i, j= self.next_pos(i, j, player = 1)
                                elif self.num[i][j] != 3 or self.num[i][j] != 7:
                                    score1 -= 1  # 錯誤分數-1&音效
                                    self.flash1 = 1  # 圖示閃爍
                                    self.not_show_i, self.not_show_j = i, j  # 閃爍圖示的位置
                                    pygame.mixer.Sound.play(wrong)
                            #玩家2輸入時
                            if event.key == pygame.K_UP:
                                if self.num[k][l] == 0 or self.num[k][l] == 4:
                                    self.num[k][l] += 8  # 變成after的圖示
                                    k, l = self.next_pos(k, l, player = 2)
                                elif self.num[k][l] != 0 or self.num[k][l] != 4:
                                    score2 -= 1  # 錯誤分數-1&音效
                                    self.flash2 = 1  # 圖示閃爍
                                    self.not_show_k, self.not_show_l = k, l  # 閃爍圖示的位置
                                    pygame.mixer.Sound.play(wrong)
                            if event.key == pygame.K_DOWN:
                                if self.num[k][l] == 1 or self.num[k][l] == 5:
                                    self.num[k][l] += 8  # 變成after的圖示
                                    k, l = self.next_pos(k, l, player = 2)
                                elif self.num[k][l] != 1 or self.num[k][l] != 5:
                                    score2 -= 1  # 錯誤分數-1&音效
                                    self.flash2 = 1  # 圖示閃爍
                                    self.not_show_k, self.not_show_l = k, l  # 閃爍圖示的位置
                                    pygame.mixer.Sound.play(wrong)
                            if event.key == pygame.K_LEFT:
                                if self.num[k][l] == 2 or self.num[k][l] == 6:
                                    self.num[k][l] += 8  # 變成after的圖示
                                    k, l = self.next_pos(k, l, player = 2)
                                elif self.num[k][l] != 2 or self.num[k][l] != 6:
                                    score2 -= 1  # 錯誤分數-1&音效
                                    self.flash2 = 1  # 圖示閃爍
                                    self.not_show_k, self.not_show_l = k, l  # 閃爍圖示的位置
                                    pygame.mixer.Sound.play(wrong)
                            if event.key == pygame.K_RIGHT:
                                if self.num[k][l] == 3 or self.num[k][l] == 7:
                                    self.num[k][l] += 8  # 變成after的圖示
                                    k, l = self.next_pos(k, l, player = 2)
                                elif self.num[k][l] != 3 or self.num[k][l] != 7:
                                    score2 -= 1 #錯誤分數-1&音效
                                    self.flash2 = 1  # 圖示閃爍
                                    self.not_show_k, self.not_show_l = k, l  # 閃爍圖示的位置
                                    pygame.mixer.Sound.play(wrong)
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == COUNT:
                            countdown = countdown - 1
                            if countdown == -3:
                                game2 = False

    def new_question(self):
        self.num = []
        self.qlist = []
        for i in range (self.number * 4):
            self.reversenum = self.qlist.count(4) + self.qlist.count(5) + self.qlist.count(6) + self.qlist.count(7)  # 反向指示數量
            if self.questionnum < 10:
                if len(self.qlist) == 0:
                    q = random.randint(0,7)
                    self.qlist.append(q)
                elif self.reversenum / len(self.qlist) < self.questionnum/12:
                    q = random.randint(0,7)
                    self.qlist.append(q)
                elif self.reversenum / len(self.qlist) >= self.questionnum/12:  # 反向指示超過一定比例不再增加
                    q = random.randint(0,3)
                    self.qlist.append(q)
            else:  # 第十題開始皆為反向指式
                q = random.randint(4,7)
                self.qlist.append(q)

        random.shuffle(self.qlist)

        for i in range(self.number):
            self.num.append([])
            for j in range(4):
                self.num[-1].append(self.qlist[i*4 + j])

        for i in range(self.number):
            self.num.append([])
            for j in range(4):
                r = self.num[i][j]
                self.num[-1].append(r)

    def show_icons(self):
        for i in range(len(self.num)):
            for j in range(4):
                if self.flash1 == 0 and self.flash2 ==0:
                    if i < len(self.num)/2:
                        x = 30 + 75.3 * j
                        y = 223 + 70 * i
                    else:
                        x = 380 + 75.3 * j
                        y = 223 + 70 * (i - len(self.num)/2)
                    screen.blit(self.imagelist[self.num[i][j]], (x, y))
                else:
                    if not ((i == self.not_show_i and j == self.not_show_j) or (i == self.not_show_k and j == self.not_show_l)):  # 不是要閃爍的圖示
                        if i < len(self.num)/2:
                            x = 30 + 75.3 * j
                            y = 223 + 70 * i
                        else:
                            x = 380 + 75.3 * j
                            y = 223 + 70 * (i - len(self.num)/2)
                        screen.blit(self.imagelist[self.num[i][j]], (x, y))
                    else:
                        if i < len(self.num)/2:
                            self.flash1 = 0
                        else:
                            self.flash2 = 0

    def show_cover(self, active, player):
        for i in range(1, int(len(self.num)/2) + 1):
            if i == active:
                continue
            if player == 1:
                x = 20
                y = 150 + 70 * i
            else:
                x = 370
                y = 150 + 70 * i
            screen.blit(self.image_cover, (x, y))

    def next_pos(self, i, j, player):
        if player == 1:
            if j == 3:
                if i == len(self.num)/2 - 1:
                    self.index1 = 1
                else:
                    i += 1
                    j = 0
            else:
                j += 1
        else:
            if j == 3:
                if i == len(self.num) - 1:
                    self.index2 = 1
                else:
                    i += 1
                    j = 0
            else:
                j += 1
        return i, j

class Game_3():

    def __init__(self):
        # 設定拍手
        self.clap = pygame.image.load('clap.png')
        self.show = 0  # 不顯示拍手 ## 換新題目show要重設為0

        self.operating()

    def operating(self):
        start = pygame.time.get_ticks()  # 開啟程式到按下開始鍵經過的時間 也就是閱讀遊戲規則的時間
        last = 0
        getpoints = False

        countdown = 53
        play = 0  # time_up音效播放
        game3 = True
        while game3:
            Three_games().same()
            time = pygame.time.get_ticks()  # 開啟程式後經過的時間

            # 倒數計時器
            countstext = str(countdown)
            if countdown > 50:
                Three_games().show_time(str(countdown - 50), countdown - 50)
            elif countdown > 0:
                Three_games().show_time(countstext, countdown)
                if (((time - start)//1000) % 0.5) == 0 and ((time - start)//1000) != last:
                    pass
                else:
                    screen.blit(self.question_surface, self.question_rect)
            else:
                if countdown == 0 and play == 0:  # time_up音效
                    pygame.mixer.Sound.play(time_up)
                    play = 1
                Three_games().show_end()

            if (((time - start)//1000) % 0.5) == 0 and ((time - start)//1000) != last:  # 每半秒換一次題目
                last = (time - start) // 1000
                # 設定題目
                self.word = ['RED', 'BLACK', 'GREEN', 'BLUE', 'PURPLE', 'GRAY']
                self.color = [(255, 0, 0), (0, 0, 0), (0, 128, 0), (0, 0, 255), (128, 0, 128), (128, 128, 128)]
                self.random_word = random.choice(self.word)  # 隨機選一單字
                for i in range(5):  # 把隨機選到的單字的色號增加五個 提高正確色號配正確單字的機率
                    self.color.append(self.color[self.word.index(self.random_word)])
                self.random_color = random.choice(self.color)  # 隨機選一色號
                self.question_font = pygame.font.Font(None, 60)  # 字體大小 = 60
                self.question_surface = self.question_font.render(str(self.random_word), True, self.random_color)  # Question更改為隨機單字
                self.question_rect = self.question_surface.get_rect()
                self.question_rect.center = (width / 2, height / 2)
                if 0 < countdown <= 50:
                    screen.blit(self.question_surface, self.question_rect)
                pygame.display.flip()
                self.show = 0
                getpoints = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and countdown > 0 and countdown <= 50:  # player1按 s 鍵，player2按 k 鍵
                        if event.key == pygame.K_s and getpoints == False:
                            self.show = 1
                            self.effect3()
                            getpoints = True
                        elif event.key == pygame.K_k and getpoints == False:
                            self.show = 2
                            self.effect3()
                            getpoints = True
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == COUNT:
                        countdown = countdown - 1
                        if countdown == -3:
                            game3 = False
                # 顯示拍手
                if self.show == 1:
                    screen.blit(self.clap, (50, 350))
                elif self.show == 2:
                    screen.blit(self.clap, (width - 50 - 260, 350))

            pygame.display.flip()

    def effect3(self):
        global score1
        global score2
        if self.word.index(self.random_word) == self.color.index(self.random_color) or self.color.index(self.random_color) > 5 :
            if self.show == 1:
                score1 += 2
                pygame.mixer.Sound.play(correct)
            elif self.show == 2:
                score2 += 2
                pygame.mixer.Sound.play(correct)
        else:
            if self.show == 1:
                score1 -= 1
                pygame.mixer.Sound.play(wrong)
            elif self.show == 2:
                score2 -= 1
                pygame.mixer.Sound.play(wrong)

class Result_window():

    def __init__(self):
        # 設定音效
        applause = pygame.mixer.Sound('applause.wav')
        pygame.mixer.Sound.play(applause)

        # 設定玩家
        player_font = pygame.font.Font(None, 54)
        player1_surface = player_font.render(name1, True, black)
        player1_rect = player1_surface.get_rect()
        player1_rect.center = (155, 320)
        player2_surface = player_font.render(name2, True, black)
        player2_rect = player2_surface.get_rect()
        player2_rect.center = (545, 320)

        # 設定分數
        score_font = pygame.font.Font(None, 50)
        score1_surf = score_font.render(str(score1), True, black)
        score1_rect = score1_surf.get_rect()
        score1_rect.center = (155, 360)
        score2_surf = score_font.render(str(score2), True, black)
        score2_rect = score2_surf.get_rect()
        score2_rect.center = (545, 360)

        # 找贏家
        global winner
        if score1 > score2:
            winner = 1
        elif score1 < score2:
            winner = 2
        else:
            winner = 0

        # 贏家/平手字樣
        if winner != 0:
            win_font = pygame.font.SysFont('comicsansmsttf', 60)
            win_surface = win_font.render('WINNER', True, red)
            win_rect = win_surface.get_rect()
            if winner == 1:
                win_rect.center = (160, 440)
            elif winner == 2:
                win_rect.center = (540, 440)
        else:
            even_font = pygame.font.SysFont('comicsansmsttf', 60)
            even_surface = even_font.render('EVEN', True, red)
            even_rect = even_surface.get_rect()
            even_rect.center = (width/2, 440)

        stay = True
        while stay:
            # 顯示背景
            screen.blit(image_background, (0,0))

            # 顯示玩家
            screen.blit(player1_face, (30, 60))
            screen.blit(player2_face, (width - 300, 60))
            screen.blit(player1_surface, player1_rect)
            screen.blit(player2_surface, player2_rect)

            # 顯示分數
            screen.blit(score1_surf, score1_rect)
            screen.blit(score2_surf, score2_rect)

            # 顯示贏家字樣
            if winner != 0:
                screen.blit(win_surface, win_rect)
            else:
                screen.blit(even_surface, even_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 500 < mouse[0] < 630 and 515 < mouse[1] < 565:  # 給button設定的範圍
                        pygame.mixer.Sound.play(select)  # 點選音效
                        stay = False

            screen.blit(image_next_button, (button_x, button_y))
            pygame.display.flip()
            mouse = pygame.mouse.get_pos()

class Board_window():

    def __init__(self):
        # 顯示背景
        bg = pygame.image.load('排行榜.png')
        screen.blit(bg, (0, 0))
        screen.blit(image_next_button, (button_x, button_y))

        self.read_board()
        self.new_board(name1, score1)
        self.new_board(name2,score2)
        self.write_board()

        # 顯示排行榜
        output_font = pygame.font.Font(None, 48)
        for i in range(1, 7):
            player = str(self.Board[i][1])
            score = str(self.Board[i][2])
            if player:  # 如果排行榜的第 i 行有遊戲紀錄，則顯示
                player_surface = output_font.render('{}'.format(player), True, black)
                player_rect = player_surface.get_rect()
                player_rect.center = (300, 230 + 50 * i)
                screen.blit(player_surface, player_rect)
                score_surface = output_font.render('{}'.format(score), True, black)
                score_rect = score_surface.get_rect()
                score_rect.center = (450, 230 + 50 * i)
                screen.blit(score_surface, score_rect)

        stay = True
        while stay:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 500 < mouse[0] < 630 and 515 < mouse[1] < 565:  # 給button設定的範圍
                        pygame.mixer.Sound.play(select) # 點選音效
                        stay = False

            pygame.display.flip()
            mouse = pygame.mouse.get_pos()

    def read_board(self):  # 讀入舊的排行榜
        r_file = open('排行榜.csv', 'r', newline='', encoding='utf-8')
        board = csv.reader(r_file)
        self.Board = []
        for row in board:
            self.Board.append(row)
        self.Board[0] = ['Rank', 'Player', 'Score']
        r_file.close()

    def new_board(self, name, score):  # 製造新的排行榜
        # 把一位玩家的結果記入排行榜
        for i in range(1, len(self.Board)):
            if self.Board[i][1] == '':
                # 如果排行榜是空的
                self.Board[i][1] = name
                self.Board[i][2] = score
                break
            elif score >= int(self.Board[i][2]):
                # 如果此次遊戲分數比排行榜的某行高
                for k in range(1, len(self.Board) - i):
                    # 把該某行以後的排名往後移一名
                    self.Board[-k][1] = self.Board[-(k + 1)][1]
                    self.Board[-k][2] = self.Board[-(k + 1)][2]
                # 計入新加入的排名
                self.Board[i][1] = name
                self.Board[i][2] = score
                break

    def write_board(self):  # 寫入新的排行榜
        w_file = open('排行榜.csv', 'w', newline='', encoding='utf-8')
        board_writer = csv.writer(w_file)
        for row in self.Board:
            board_writer.writerow(row)
        w_file.close()

class Ending_window():
    def __init__(self):
        # 設定圖片
        bg = pygame.image.load('ending_bg.png')
        yes = pygame.image.load('Yes_button.png')
        no = pygame.image.load('No_button.png')
        screen.blit(bg, (0, 0))
        screen.blit(yes, (width/2 - 180, height/2 - 20))
        screen.blit(no, (width/2 + 40, height/2 - 20))

        global again
        stay = True
        while stay:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 170 < mouse[0] < 310 and 280 < mouse[1] < 350:  # 給yes button設定的範圍
                        pygame.mixer.Sound.play(select)
                        again = True
                        stay = False
                    elif 390 < mouse[0] < 530 and 280 < mouse[1] < 350:  # 給no button設定的範圍
                        pygame.mixer.Sound.play(select)
                        again = False
                        stay = False

            pygame.display.flip()
            mouse = pygame.mouse.get_pos()


# 建立視窗
width, height = 700, 600
button_x, button_y = 540, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('善挑')
red, black, orange = (255,0,0), (0,0,0), (255,147,0)

# 設定音效
select = pygame.mixer.Sound('select.wav')
correct = pygame.mixer.Sound('correct.wav')
wrong = pygame.mixer.Sound('wrong.wav')
time_up = pygame.mixer.Sound('time up.wav')

# 設定圖片
image_rule1 = pygame.image.load('第一關遊戲規則.png')
image_rule2 = pygame.image.load('第二關遊戲規則.png')
image_rule3 = pygame.image.load('第三關遊戲規則.png')
image_next_button = pygame.image.load('下一頁.png')
image_background = pygame.image.load('background.png')

# run
again = True
while again:
    score1, score2 = 0, 0  # 設定分數
    again = False

    beginning_window = Beginning_window()
    intro_window = Intro_window()
    photo = Photo()
    prepare_window = Prepare_window()

    game_intro1 = Game_intro().window(image_rule1)
    game_1 = Game_1()

    game_intro2 = Game_intro().window(image_rule2)
    game_2 = Game_2()

    game_intro3= Game_intro().window(image_rule3)
    game_3 = Game_3()

    result_window = Result_window()
    board_window = Board_window()
    ending_window = Ending_window()