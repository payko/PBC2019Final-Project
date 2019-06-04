import pygame

pygame.init()

# 建立第一關遊戲視窗
width = 700
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('輸入玩家資訊')

# 設定顏色
background = (255, 246, 211)

while True: # 遊戲迴圈
    screen.fill(background)

    # 關閉視窗
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.flip()