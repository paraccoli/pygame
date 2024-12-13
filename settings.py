# FILE: settings.py
import pygame
import sys
from config import FONT_PATH, screen, SCREEN_WIDTH, SCREEN_HEIGHT
# グローバル変数の初期化
bgm_volume = 0.5
se_volume = 0.5
brightness = 0.5
selected_slider = 0

# キー設定の初期化
key_config = {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "pickup": pygame.K_e,
    "map": pygame.K_m,
    "attack": pygame.K_SPACE,
    "back": pygame.K_ESCAPE,
    "save": pygame.K_s,
    "magic": pygame.K_g,
    "inventory": pygame.K_i
}

def draw_slider(label, value, position):
    font = pygame.font.Font(FONT_PATH, 24)
    text = font.render(f"{label}: {int(value * 100)}%", True, (255, 255, 255))
    screen.blit(text, (position[0], position[1] - 30))
    pygame.draw.rect(screen, (255, 255, 255), (*position, 200, 10))
    pygame.draw.rect(screen, (0, 255, 0), (*position, int(value * 200), 10))

def draw_arrow(screen, position, visible=True):
    if visible:
        font = pygame.font.Font(FONT_PATH, 48)
        arrow = font.render("→", True, (255, 255, 255))
        screen.blit(arrow, (position[0] - 60, position[1] - 20))

def draw_key_icon(screen, key_name, position, width=50):
    font = pygame.font.Font(FONT_PATH, 24)
    key_rect = pygame.Rect(position[0], position[1], width, 50)
    pygame.draw.rect(screen, (255, 255, 255), key_rect, border_radius=5)
    key_text = font.render(key_name, True, (0, 0, 0))
    screen.blit(key_text, (position[0] + (width - key_text.get_width()) // 2, position[1] + (50 - key_text.get_height()) // 2))

def show_menu(screen):
    menu_options = ["オプション", "ゲームを続ける", "ゲームを終了する"]
    font = pygame.font.Font(FONT_PATH, 48)
    selected_option = 0
    running = True
    while running:
        screen.fill((0, 0, 0))

        option_positions = [
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        ]

        for i, option in enumerate(menu_options):
            option_text = font.render(option, True, (255, 255, 255))
            screen.blit(option_text, option_positions[i])

        # 現在選択しているオプションの左に矢印を表示
        draw_arrow(screen, option_positions[selected_option])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # オプション
                        show_options(screen)
                    elif selected_option == 1:  # ゲームを続ける
                        running = False
                    elif selected_option == 2:  # ゲームを終了する
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()


def show_options(screen):
    global bgm_volume, se_volume, brightness, selected_slider, key_config
    options = ["BGM 音量", "SE 音量", "明るさ", "キーコンフィグ", "戻る"]
    font = pygame.font.Font(FONT_PATH, 48)
    selected_option = 0
    running = True
    while running:
        screen.fill((0, 0, 0))

        option_positions = [
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 75),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 75),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
        ]

        for i, option in enumerate(options):
            option_text = font.render(option, True, (255, 255, 255))
            screen.blit(option_text, option_positions[i])

        # 現在選択しているオプションの左に矢印を表示
        draw_arrow(screen, option_positions[selected_option])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # BGM 音量
                        adjust_volume(screen, "BGM 音量", bgm_volume)
                    elif selected_option == 1:  # SE 音量
                        adjust_volume(screen, "SE 音量", se_volume)
                    elif selected_option == 2:  # 明るさ
                        adjust_brightness(screen)
                    elif selected_option == 3:  # キーコンフィグ
                        configure_keys(screen)
                    elif selected_option == 4:  # 戻る
                        running = False

        pygame.display.flip()

def adjust_volume(screen, label, volume):
    global bgm_volume, se_volume
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_slider(label, volume, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    volume = max(0, volume - 0.05)
                elif event.key == pygame.K_RIGHT:
                    volume = min(1, volume + 0.05)

        if label == "BGM 音量":
            bgm_volume = volume
        elif label == "SE 音量":
            se_volume = volume

        pygame.display.update()

def adjust_brightness(screen):
    global brightness
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_slider("明るさ", brightness, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    brightness = max(0, brightness - 0.05)
                elif event.key == pygame.K_RIGHT:
                    brightness = min(1, brightness + 0.05)

        # 明るさの調整は画面全体の色を変更することでシミュレート
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(int((1 - brightness) * 255))
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        pygame.display.update()

def configure_keys(screen):
    global key_config
    keys = ["up", "down", "left", "right", "pickup", "map", "attack", "magic", "inventory","save", "back"]
    key_labels = ["上", "下", "左", "右", "取得", "マップ", "攻撃", "魔法", "持ち物","保存", "戻る"]
    font = pygame.font.Font(FONT_PATH, 48)
    selected_key = 0
    waiting_for_key = False
    blink = False
    blink_timer = 0
    running = True
    while running:
        screen.fill((0, 0, 0))

        for i, key in enumerate(keys):
            key_text = f"{key_labels[i]}: {pygame.key.name(key_config[key])}"
            if key_config[key] in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                key_icon = {pygame.K_UP: "↑", pygame.K_DOWN: "↓", pygame.K_LEFT: "←", pygame.K_RIGHT: "→"}[key_config[key]]
            elif key_config[key] == pygame.K_ESCAPE:
                key_icon = "ESC"
            elif key_config[key] == pygame.K_SPACE:
                key_icon = "SPACE"
            else:
                key_icon = pygame.key.name(key_config[key]).upper()
            text = font.render(key_text, True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 200 + i * 50))
            icon_width = 100 if key_config[key] == pygame.K_SPACE else 50
            draw_key_icon(screen, key_icon, (SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2 - 200 + i * 50), icon_width)

        # 矢印を点滅させる
        if waiting_for_key:
            blink_timer += 1
            if blink_timer % 30 == 0:
                blink = not blink
            draw_arrow(screen, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 200 + selected_key * 50), blink)
        else:
            draw_arrow(screen, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 200 + selected_key * 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if waiting_for_key:
                    key_config[keys[selected_key]] = event.key
                    waiting_for_key = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    selected_key = (selected_key - 1) % len(keys)
                elif event.key == pygame.K_DOWN:
                    selected_key = (selected_key + 1) % len(keys)
                elif event.key == pygame.K_RETURN:
                    waiting_for_key = True

        pygame.display.flip()