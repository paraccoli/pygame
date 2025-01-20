# FILE: episode1.py
import pygame
import sys

credit_music = pygame.mixer.Sound("music/BGM09credits.wav")

def episode1(screen, third_dialogue_music):
    # third_dialogue_musicをフェードアウト
    third_dialogue_music.fadeout(1000)  # 1秒かけてフェードアウト

    # フェードアウトが完了するまで待機
    pygame.time.wait(1000)
    credit_music.play(-1)  # ループ再生
    running = True
    font = pygame.font.Font(None, 74)
    sub_font = pygame.font.Font(None, 36)

    while running:
        screen.fill((0, 0, 0))

        # メッセージを描画
        text = font.render("Next episode coming soon!", True, (255, 255, 255))
        sub_text = sub_font.render("Thanks for playing!", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))
        screen.blit(sub_text, (screen.get_width() // 2 - sub_text.get_width() // 2, screen.get_height() // 2 + text.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # BGMをフェードアウト
                    credit_music.fadeout(1000)  # 1秒かけてフェードアウト
                    pygame.time.wait(1000)
                    #TODO: オープンワールドのマップに遷移
                    from open_world import open_world
                    open_world(screen)
                    running = False

        pygame.display.flip()