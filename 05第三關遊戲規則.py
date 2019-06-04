import pygame

pygame.init()

# 建立第一關遊戲視窗
width = 700
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('第三關 顏色辨別')

# 設定規則
image_rule = pygame.image.load('第三關遊戲規則.png')

# 設定遊戲開始按鈕
image_button = pygame.image.load('遊戲開始按鈕.png')

while True:
    # 顯示規則
    screen.blit(image_rule, (0, 0))

    # 顯示遊戲開始按鈕
    screen.blit(image_button, (0, 0))

    # 關閉視窗
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.flip()