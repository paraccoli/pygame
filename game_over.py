# game_over.py

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_PATH, screen

def game_over(show_main_menu):
    # フェードアウト処理
    for alpha in range(0, 256, 5):
        fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.wait(50)  # フェードアウトの速度を調整
    # GAME OVERのテキストを表示
    try:
        font = pygame.font.Font(FONT_PATH, 100)  # 指定されたフォントを使用
    except FileNotFoundError:
        print(f"Font file not found: {FONT_PATH}")
        font = pygame.font.Font(None, 100)  # フォントが見つからない場合はデフォルトフォントを使用

    text = font.render("GAME OVER", True, (255, 0, 0))  # 赤い文字で描画
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    # 3秒待つ
    pygame.time.wait(3000)
    show_main_menu()  # 引数として渡されたshow_main_menu関数を呼び出す