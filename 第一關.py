import pygame
import random

def button(x, y):
    screen.blit(image_button, (x, y))

button_x = 500
button_y = 500

def game_intro():
    intro = True
	
    # 顯示規則
    while intro:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # 關閉視窗
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 500 < mouse[0] <630 and 515 < mouse[1] < 565: # 給箭頭button設定的範圍
                    intro = False
        screen.blit(image_rule, (0, 0))        
        screen.blit(image_button, (0, 0))
        pygame.display.update()
        
class Game_1():

        # 設定顏色
        background = (255, 246, 211)
        black = (0, 0, 0)
        white = (255, 255, 255)

        # 設定玩家
        size = 140  # 頭像寬

        def __init__(self):
            self.player_font = pygame.font.Font(None, 32)  # 字體大小 = 32
            self.player1_surface = self.player_font.render('Name1', False, self.black)
            self.player1_rect = self.player1_surface.get_rect()
            self.player1_rect.center = (20 + self.size / 2, 20 + self.size + 20 + 20)
            self.player2_surface = self.player_font.render('Name2', False, self.black)
            self.player2_rect = self.player2_surface.get_rect()
            self.player2_rect.center = (width - 20 - self.size / 2, 20 + self.size + 20 + 20)

        # 設定分數
            self.score1 = 0
            self.score2 = 0
            self.score_font = pygame.font.Font(None, 32)  # 字體大小 = 32
            self.score1_surface = self.player_font.render(str(self.score1), False, self.black)  # 玩家1分數
            self.score1_rect = self.score1_surface.get_rect()
            self.score1_rect.center = (20 + self.size + 50, 50)
            self.score2_surface = self.player_font.render(str(self.score2), False, self.black)  # 玩家2分數
            self.score2_rect = self.score2_surface.get_rect()
            self.score2_rect.center = (width - 20 - self.size - 50, 50)

        # 設定題目
            self.random_ = random.randint(0,1000)
            self.question_font = pygame.font.Font(None, 60)  # 字體大小 = 60
            self.question_surface = self.question_font.render(str(self.random_), False, self.black)  # Question更改為隨機數字
            self.question_rect = self.question_surface.get_rect()
            self.question_rect.center = (width / 2, height / 2)

        # 設定拍手
            self.clap = pygame.image.load('clap.png')
            self.show = 0  # 不顯示拍手 ## 換新題目show要重設為0
            self.operating()

        def operating(self):
            self.start = pygame.time.get_ticks() #開啟程式到按下開始鍵經過的時間 也就是閱讀遊戲規則的時間
            self.last = 0
            self.getpoints = False
            while True:
                screen.fill(self.background)
				
            # 顯示玩家
                pygame.draw.rect(screen, self.white, (20, 20, self.size, self.size + 20), 2)  # 玩家1頭像
                screen.blit(self.player1_surface, self.player1_rect)  # 玩家1名稱
                pygame.draw.rect(screen, self.white, (width - 20 - self.size, 20, self.size, 20 + self.size), 2)  # 玩家2頭像
                screen.blit(self.player2_surface, self.player2_rect)  # 玩家2名稱
                
                self.time = pygame.time.get_ticks()  #開啟程式後經過的時間
                self.time_font = pygame.font.Font(None, 60)
                self.time_surface = self.time_font.render("Time:" + str(((61000 - self.time + self.start) // 1000)), True, (0, 0, 0))
                screen.blit(self.time_surface, [330, 70])

            # 顯示分數
                screen.blit(self.score1_surface, self.score1_rect)  # 玩家1分數
                screen.blit(self.score2_surface, self.score2_rect)  # 玩家2分數

            # 顯示題目
                screen.blit(self.question_surface, self.question_rect)
                if (((self.time - self.start)//1000) % 2) == 0 and ((self.time - self.start)//1000) != self.last: # 每2秒換一個數字
                    self.last = (self.time - self.start) // 1000
                    self.random_ = random.randint(0,1000)
                    self.question_surface = self.question_font.render(str(self.random_), False, self.black)  # Question更改為隨機數字
                    screen.blit(self.question_surface, self.question_rect)
                    pygame.display.flip()
                    self.show = 0
                    self.getpoints = False
                    continue
                else:
                    for event in pygame.event.get():
                    # player1按 s 鍵，player2按 k 鍵
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_s and self.getpoints == False:
                                self.show = 1
                                self.result = self.effect()
                                self.getpoints = True
                                self.score1_surface = self.player_font.render(str(self.result[0]), False, self.black)  # 玩家1分數
                            elif event.key == pygame.K_k and self.getpoints == False:
                                self.show = 2
                                self.result = self.effect()
                                self.getpoints = True
                                self.score2_surface = self.player_font.render(str(self.result[1]), False, self.black)  # 玩家2分數    
                    # 關閉視窗
                        elif event.type == pygame.QUIT:
                            pygame.quit()
            # 顯示拍手
                    if self.show == 1:
                        screen.blit(self.clap, (50, 350))
                    elif self.show == 2:
                        screen.blit(self.clap, (width - 50 - 260, 350))

                    pygame.display.flip()

        #遊戲規則
        def effect(self):
            #正確得2分
            if self.random_ % 3 == 0 or '3' in str(self.random_):
                if self.show == 1:
                    self.score1 += 2   
                elif self.show == 2:
                    self.score2 += 2
            #錯誤扣1分
            else:
                if self.show == 1:
                    self.score1 -= 1
                elif self.show == 2:
                    self.score2 -= 1
                else:
                    pass
					
            return [self.score1, self.score2]

pygame.init()

# 建立第一關遊戲視窗
width = 700
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('第一關 3的世界')

# 設定規則
image_rule = pygame.image.load('第一關遊戲規則.png')

# 設定遊戲開始按鈕
image_button = pygame.image.load('遊戲開始按鈕.png')
game_intro()
g1 = Game_1()
