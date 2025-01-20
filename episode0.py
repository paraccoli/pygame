import pygame
import os
import json
import math
from dialogue_manager import DialogueManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_PATH, screen
from episode0_0 import episode0_0
from save_manager import load_save_data

# プレイヤー名を取得
with open('save/selected_save_slot.json', 'r') as file:
    selected_save_slot = json.load(file)["selected_slot"]

save_data = load_save_data(f'save/save_{selected_save_slot}.json')
player_name = save_data["player_name"]

BACKGROUND_IMAGE_PATHS = [
    os.path.join("images", "episode0-0.png"),
    os.path.join("images", "episode0-1.png"),
    os.path.join("images", "episode0-2.png")
]

DIALOGUES = [
    "古の時代から、この世界には一つの伝説が残されている。",
    "それは、すべての生命の力を秘めたという、一振りの剣の伝説。",
    "その剣を手にした者は、世界を支配できるという。",
    "しかし、その剣は、同時に持ち主を滅ぼす力も持っていた。",
    "そのため、その剣は封印され、その伝説は忘れ去られた。",
    "しかし、今、その封印が解かれようとしている。",
    "果たして、その剣を手にした者は、どのような運命を辿るのか。",
    f"小さな村に住む一人の若者、{player_name}の手に",
    "その剣が渡されたとき、世界の運命は大きく動き始める。",
    f"果たして、{player_name}はその剣を手にして、",
    "世界を救うことができるのだろうか。",
    "それとも、世界を滅ぼす運命に身を投じるのか。",
    "さあ、物語の幕が開く。",
    "Episode 0: The Legend of the Sword"
]

FPS = 60  # フレームレート
clock = pygame.time.Clock()

def fadein(surface, duration):
    """
    フェードイン処理

    Args:
        surface: 処理したいSurface
        duration: フェード時間(秒)
    """
    alpha = 0
    for i in range(duration * FPS):
        clock.tick(FPS)
        alpha += 255 / (duration * FPS)
        surface.set_alpha(alpha)
        screen.fill((0, 0, 0))  # 背景を黒にする
        screen.blit(surface, (0, 0))
        pygame.display.update()

def start_episode0(screen):
    pygame.init()
    backgrounds = [pygame.transform.scale(pygame.image.load(path), (SCREEN_WIDTH, SCREEN_HEIGHT)) for path in BACKGROUND_IMAGE_PATHS]
    dialogue_manager = DialogueManager(FONT_PATH, SCREEN_HEIGHT)
    episode0_music = pygame.mixer.Sound(os.path.join("music", "episode0.mp3"))
    episode0_music.play()

    for dialogue in DIALOGUES:
        dialogue_manager.add_dialogue(dialogue)

    skip_timer = 0
    skip_duration = 2000  # スペースキーを2秒間押し続けるとスキップ
    skip_circle_radius = 20
    skip_circle_position = (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)

    # 画面を黒にして2秒待つ
    screen.fill((0, 0, 0))
    pygame.display.update()
    pygame.time.wait(2000)

    # フェードイン処理
    fadein(backgrounds[0], 2)

    running = True
    current_background_index = 0
    last_switch_time = pygame.time.get_ticks()
    switch_interval = 15000  # 15秒ごとに背景を切り替える
    last_update_time = pygame.time.get_ticks()  # 現在の時間を取得

    while running:
        current_time = pygame.time.get_ticks()
        if current_time - last_update_time > 2500:  # 2.5秒経過したら次のセリフに進む
            dialogue_manager.next_dialogue()
            last_update_time = current_time
        if current_time - last_switch_time > switch_interval:
            current_background_index = (current_background_index + 1) % len(backgrounds)
            last_switch_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    skip_timer = pygame.time.get_ticks()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    skip_timer = 0

        screen.blit(backgrounds[current_background_index], (0, 0))  # 背景を描画

        # ダイアログボックスを描画
        dialogue_box_width = SCREEN_WIDTH * 0.8
        dialogue_box_height = SCREEN_HEIGHT * 0.3
        dialogue_box_x = (SCREEN_WIDTH - dialogue_box_width) // 2
        dialogue_box_y = SCREEN_HEIGHT - dialogue_box_height - 50  # 画面下に配置
        dialogue_box_rect = pygame.Rect(dialogue_box_x, dialogue_box_y, dialogue_box_width, dialogue_box_height)
        pygame.draw.rect(screen, (0, 0, 0), dialogue_box_rect)  # 黒い四角
        pygame.draw.rect(screen, (255, 255, 255), dialogue_box_rect, 3)  # 白い枠線
        pygame.draw.rect(screen, (0, 0, 0, 128), dialogue_box_rect)  # 中を薄くする

        dialogue_manager.draw(screen, dialogue_box_rect)  # ダイアログを描画

        # スペースキーが押されている間、円を描画
        if skip_timer:
            elapsed_time = pygame.time.get_ticks() - skip_timer
            if elapsed_time >= skip_duration:
                dialogue_manager.skip_to_end()
                skip_timer = 0
                episode0_music.fadeout(2000)
                pygame.time.wait(2000)
                running = False
            else:
                angle = (elapsed_time / skip_duration) * 360
                pygame.draw.arc(screen, (255, 255, 255), (skip_circle_position[0] - skip_circle_radius, skip_circle_position[1] - skip_circle_radius, skip_circle_radius * 2, skip_circle_radius * 2), 0, math.radians(angle), 5)

        pygame.display.flip()

        # セリフがすべて終わったかどうかを確認
        if dialogue_manager.is_finished() or dialogue_manager.skip_to_end():
            episode0_music.fadeout(2000)  # 2秒で音楽をフェードアウト
            pygame.time.wait(2000)  # フェードアウトが完了するまで待つ
            break  # ループを抜ける

    episode0_0()  # 次の関数に遷移