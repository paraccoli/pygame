# +----------------------------------------------------+
#  This file was created by Paraccoli.
#  Contact:m.mirim1357@gmail.com
#  This file contains the code for the main game loop.
# +----------------------------------------------------+


"""The main game loop."""
# -*- coding: utf-8 -*-
# ライブラリの読み込み
import pygame
import sys
import os
import time
import json
from config import SCREEN_WIDTH, SCREEN_HEIGHT, SLOT_INFO_MARGIN, FONT_PATH, screen
from episode0 import start_episode0
from save_manager import load_save_data
from open_world import open_world
from variables import *

# 選択中のスロット番号
selected_slot = 0

# パス
BACKGROUND_IMAGE_PATH = os.path.join("images", "background.png")
ICON_IMAGE_PATH = os.path.join("images", "icon.png")
GAME_ICON_IMAGE_PATH = os.path.join("images", "icon2.png")
GAME_TITLE_IMAGE_PATH = os.path.join("images", "title.png")
icon_image = pygame.image.load(ICON_IMAGE_PATH)
icon_image = pygame.transform.scale(icon_image, (700, 200))
icon_rect = icon_image.get_rect()
icon_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

# 定数の設定
FPS = 15
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(FONT_PATH, 50)
text = font.render('日本語', True, (0, 0, 0))
# スライダーの初期値
bgm_volume = 0.5
se_volume = 0.5
brightness = 1.0
# 選択中のスライダー
selected_slider = 0
# 音楽の読み込み
try:
    opening_music = pygame.mixer.Sound("music/BGM00hero.wav")
    # 音楽のループ再生
    opening_music.play(loops=-1)
except pygame.error as e:
    print(f"音楽ファイルの読み込みに失敗しました: {e}")

# 効果音の読み込み
try:
    click_sound = pygame.mixer.Sound("sounds/click.mp3")
except pygame.error as e:
    print(f"効果音ファイルの読み込みに失敗しました: {e}")


# アイコン設定
pygame.display.set_icon(pygame.image.load(GAME_ICON_IMAGE_PATH).convert())
pygame.display.set_caption("TEST GAME")

# ボタン設定
button_width = 150
button_height = 50
button_rect = pygame.Rect(SCREEN_WIDTH - button_width - SLOT_INFO_MARGIN,
                            SCREEN_HEIGHT - button_height - SLOT_INFO_MARGIN,
                            button_width, button_height)

# テロップ設定
message_font = pygame.font.Font(FONT_PATH, 30)
message_text = message_font.render("名前を記入してください", True, (0, 0, 0))
message_text_rect = message_text.get_rect()
message_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)

# 入力欄設定
input_width = 400
input_height = 50
input_rect = pygame.Rect(SCREEN_WIDTH / 2 - input_width / 2,
                            SCREEN_HEIGHT / 2 - input_height / 2,
                            input_width, input_height)
input_text = ""

# ゲームの状態
STATE_GAME = 0
STATE_CONFIRM = 1

# 状態
state = STATE_GAME

# ゲーム終了オプション
QUIT_OPTIONS = {
    "はい": "quit_game",
    "いいえ": "return_to_title",
}

# オプション
OPTIONS = {
    "はじめから": "start_game",
    "つづきから": "continue_game",
    "オプション": "show_options",
    "終了する": "show_confirm",
}

# スロット数
NUM_SLOTS = 3

# スロット枠の大きさ
SLOT_WIDTH = 600
SLOT_HEIGHT = 150

# スロット間隔
SLOT_MARGIN = 20
SLOT_INFO_MARGIN = 0

# 選択中のスロット番号
selected_slot = 0

# 各選択肢のテキストを描画する前に、Rectオブジェクトを作成
option_rects1 = []
for i, option in enumerate(OPTIONS.keys()):
    text_surface1 = font.render(option, True, (255, 255, 255))
    text_rect1 = text_surface1.get_rect()
    text_rect1.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + i * 50)
    option_rects1.append(text_rect1)

# 各選択肢のテキストを描画する前に、Rectオブジェクトを作成
option_rects2 = []
for i, option in enumerate(QUIT_OPTIONS.keys()):
    text_surface2 = font.render(option, True, (255, 255, 255))
    text_rect2 = text_surface2.get_rect()
    text_rect2.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + i * 50)
    option_rects2.append(text_rect2)

# データ保存関数
def save_game_data(selected_slot, player_name, play_time="0000:00:00", level=1):
    file_path = os.path.join("save", f"save_{selected_slot}.json")
    save_data = {
        "player_name": player_name,
        "play_time": play_time,
        "level": level,
        "position":{
            "x": 350,
            "y": 350,
        },
        "inventory": [
        ],
        "health": 100,
        "zenny": 1000
    }
    with open(file_path, "w", encoding='utf-8') as f:
        json.dump(save_data, f)
    # 選択されたセーブスロットを保存
    with open('save/selected_save_slot.json', 'w') as f:
        json.dump({"selected_slot": selected_slot}, f)

# フェードイン処理
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
        icon_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        screen.blit(surface, icon_rect)
        pygame.display.update()
""
# フェードアウト処理
def fadeout(surface, duration):
    """
    フェードアウト処理

    Args:
        surface: 処理したいSurface
        duration: フェード時間(秒)
    """
    alpha = 255
    for i in range(duration * FPS):
        clock.tick(FPS)
        alpha -= 255 / (duration * FPS)
        surface.set_alpha(alpha)
        icon_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        screen.blit(surface, icon_rect)
        pygame.display.update()


# オープニング画面表示
def opening():
    # 暗転処理
    screen.fill((0, 0, 0))
    pygame.display.update()

    # アイコン表示
    fadein(icon_image,3)
    # 暗転処理
    fadeout(icon_image,3)
    # メイン画面表示
    show_main_menu()

def show_main_menu():
    screen.fill((0, 0, 0))
    selected_option = 0  # 選択されているオプションのインデックス
    options = list(OPTIONS.keys())  # オプションリスト

    while True:
        # イベント処理
        for event in pygame.event.get():
            # 暗転処理
            screen.fill((0, 0, 0))
            # 背景画像設定
            background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
            background_image.set_alpha(128)
            scaled_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scaled_image, (0, 0))

            # オプション表示
            for i, option in enumerate(OPTIONS.keys()):
                # 文字色と背景色のコントラストを調整
                if i == selected_option:
                    text_color = (100, 50, 0)  # 茶色
                    background_color = (150, 200, 150)  # 薄い緑色
                else:
                    text_color = (255, 255, 255)  # 白色
                    background_color = (0, 0, 0)  # 黒色

                # 文字サイズを調整
                text_surface = font.render(option, True, text_color, background_color)
                text_surface = pygame.transform.scale(text_surface, (200, 50))
                text_rect = text_surface.get_rect()
                text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + i * 50)

                # 影をつける
                shadow_surface = pygame.Surface((text_surface.get_width() + 2, text_surface.get_height() + 2))
                shadow_surface.fill((0, 0, 0))
                shadow_surface.blit(text_surface, (1, 1))
                screen.blit(shadow_surface, text_rect)
                screen.blit(text_surface, text_rect)

            # 矢印キーによる選択処理
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = max(0, selected_option - 1)
                elif event.key == pygame.K_DOWN:
                    selected_option = min(len(options) - 1, selected_option + 1)

            # Enterキーを押された場合、選択されたオプションを実行
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                click_sound.play()
                selected_option_name = options[selected_option]
                selected_option_function = OPTIONS[selected_option_name]
                # 選択されたオプションの関数を呼び出す
                globals()[selected_option_function]()

            # ✕印を押された場合
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # 確認画面表示
                show_confirm()


        # 画面更新
        pygame.display.update()

# ゲーム終了画面表示
def show_confirm():
    screen.fill((0, 0, 0))
    selected_option = 0  # 選択されているオプションのインデックス
    options = list(QUIT_OPTIONS.keys())  # オプションリスト
    state = STATE_CONFIRM

    while True:
        # イベント処理
        for event in pygame.event.get():
            # 暗転処理
            screen.fill((0, 0, 0))

            # 確認メッセージ表示
            confirm_message = font.render("ゲームを終了しますか？", True, (255, 255, 255))
            confirm_message_rect = confirm_message.get_rect()
            confirm_message_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)
            screen.blit(confirm_message, confirm_message_rect)

            # オプション表示
            for i, option in enumerate(options):
                text_color = (0, 0, 0)  # デフォルトの文字色
                if i == selected_option:
                    text_color = (255, 255, 255)  # 選択されている項目の文字色
                text_surface = font.render(option, True, text_color)
                text_rect = text_surface.get_rect()
                text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + i * 50)
                screen.blit(text_surface, text_rect)

            # 画面更新
            pygame.display.update()

            # 矢印キーによる選択処理
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_option = max(0, selected_option - 1)
                elif event.key == pygame.K_RIGHT:
                    selected_option = min(len(options) - 1, selected_option + 1)

            # Enterキーを押された場合、選択されたオプションを実行
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                click_sound.play()
                selected_option_name = options[selected_option]
                selected_option_function = QUIT_OPTIONS[selected_option_name]
                # 選択されたオプションの関数を呼び出す
                globals()[selected_option_function]()


# 新規セーブデータ作成
def create_save_data():
    global selected_slot

    # パス
    BACKGROUND_IMAGE_PATH = os.path.join("images", "background.png")
    ICON_IMAGE_PATH = os.path.join("images", "icon2.png")
    icon_image = pygame.image.load(ICON_IMAGE_PATH)
    icon_image = pygame.transform.scale(icon_image, (700, 200))
    icon_rect = icon_image.get_rect()
    icon_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    font = pygame.font.Font('font/Nosutaru-dotMPlusH-10-Regular.ttf', 20)

    # 選択状態 (0: スロット, 1: ボタン)
    slot_state = 0

    # 選択状態 (0: スロット, 1: 入力欄, 2: 決定ボタン, 3: 戻るボタン)
    selection_state = 0

    # 入力欄設定
    input_width = 400
    input_height = 50
    input_rect = pygame.Rect(SCREEN_WIDTH / 2 - input_width / 2,
                              SCREEN_HEIGHT / 2 - input_height / 2,
                              input_width, input_height)
    input_text = ""
    show_input_box = False

    while True:
        # イベント処理
        for event in pygame.event.get():
            # 暗転処理
            screen.fill((0, 0, 0))
            # 背景画像設定
            background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
            background_image.set_alpha(128)
            scaled_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scaled_image, (0, 0))

            # スロット情報リスト
            slot_infos = []
            # 画面中央にスロット枠を作成
            slot_rects = []
            for i in range(NUM_SLOTS):
                slot_rect = pygame.Rect(0, 0, SLOT_WIDTH, SLOT_HEIGHT)
                # スロット間の余白を考慮して、Y座標を計算
                slot_rect.top = (SCREEN_HEIGHT - (SLOT_HEIGHT + SLOT_MARGIN) * NUM_SLOTS) / 2 + (SLOT_HEIGHT + SLOT_MARGIN) * i
                slot_rect.centerx = SCREEN_WIDTH / 2
                slot_rects.append(slot_rect)
            # スロット情報表示
            for i, slot_rect in enumerate(slot_rects):
                file_path = os.path.join("save", "save_{}.json".format(i + 1))
                save_data = {}
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding='utf-8') as f:
                        save_data = json.load(f)

                slot_infos.append({
                    "player_name": save_data.get("player_name", ""),
                    "play_time": save_data.get("play_time", "0000:00:00"),
                    "level": save_data.get("level", 1),
                })

                # スロット番号テキスト
                slot_number_text = font.render("スロット{}".format(i + 1), True, (0, 0, 0))
                slot_number_text_rect = slot_number_text.get_rect()
                slot_number_text_rect.topleft = (
                    slot_rect.left + SLOT_INFO_MARGIN,
                    slot_rect.top + SLOT_INFO_MARGIN,
                )

                # プレイヤー名テキスト
                player_name_text = font.render(save_data.get("player_name", ""), True, (0, 0, 0))
                player_name_text_rect = player_name_text.get_rect()
                player_name_text_rect.topleft = (
                    slot_rect.left + SLOT_INFO_MARGIN,
                    slot_rect.top + SLOT_HEIGHT // 2 + SLOT_INFO_MARGIN,
                )

                # プレイ時間テキスト
                play_time_text = font.render(save_data.get("play_time", "0000:00:00"), True, (0, 0, 0))
                play_time_text_rect = play_time_text.get_rect()
                play_time_text_rect.topleft = (
                    slot_rect.left + SLOT_INFO_MARGIN,
                    slot_rect.bottom - SLOT_INFO_MARGIN - play_time_text_rect.height,
                )

                # レベルテキスト
                level_text = font.render("レベル: {}".format(save_data.get("level", 1)), True, (0, 0, 0))
                level_text_rect = level_text.get_rect()
                level_text_rect.topright = (
                    slot_rect.right - SLOT_INFO_MARGIN,
                    slot_rect.bottom - SLOT_INFO_MARGIN - level_text_rect.height,
                )

                # 各要素を描画
                pygame.draw.rect(screen, (255, 255, 255), slot_rect)
                screen.blit(slot_number_text, slot_number_text_rect)
                screen.blit(player_name_text, player_name_text_rect)
                screen.blit(play_time_text, play_time_text_rect)
                screen.blit(level_text, level_text_rect)

            # 選択中のスロットを強調表示
            if slot_state == 0:
                pygame.draw.rect(screen, (255, 0, 0), slot_rects[selected_slot], 2)  # 赤い枠線を描画

            # ボタン設定
            button_width = 150
            button_height = 50
            button_rect = pygame.Rect(SCREEN_WIDTH - button_width - SLOT_INFO_MARGIN,
                                      SCREEN_HEIGHT - button_height - SLOT_INFO_MARGIN,
                                      button_width, button_height)

            # ボタンの描画
            if slot_state == 1:
                pygame.draw.rect(screen, (255, 0, 0), button_rect, 2)  # 赤い枠線を描画
            else:
                pygame.draw.rect(screen, (255, 255, 255), button_rect)
            button_text = font.render("戻る", True, (0, 0, 0))
            button_text_rect = button_text.get_rect()
            button_text_rect.center = button_rect.center
            screen.blit(button_text, button_text_rect)

            # 入力欄の描画
            if show_input_box:
                pygame.draw.rect(screen, (200, 200, 200), input_rect)  # 入力欄の背景色を灰色に変更
                pygame.draw.rect(screen, (0, 0, 0), input_rect, 2)  # 入力欄の枠線を黒色に設定
                input_text_surface = font.render(input_text, True, (0, 0, 0))
                input_text_rect = input_text_surface.get_rect()
                input_text_rect.midleft = input_rect.midleft
                input_text_rect.x += 10  # 入力テキストを少し右に移動
                screen.blit(input_text_surface, input_text_rect)

                # 決定ボタン
                decide_button_width = 100
                decide_button_height = 50
                decide_button_rect = pygame.Rect(input_rect.right + 20, input_rect.centery - decide_button_height // 2,
                                                decide_button_width, decide_button_height)
                if selection_state == 2:
                    pygame.draw.rect(screen, (0, 255, 0), decide_button_rect)  # 緑色の決定ボタン
                    pygame.draw.rect(screen, (255, 0, 0), decide_button_rect, 2)  # 赤色の枠線を追加
                else:
                    pygame.draw.rect(screen, (0, 255, 0), decide_button_rect)  # 緑色の決定ボタン
                    pygame.draw.rect(screen, (0, 0, 0), decide_button_rect, 2)  # 黒色の枠線を追加
                decide_button_text = font.render("決定", True, (0, 0, 0))
                decide_button_text_rect = decide_button_text.get_rect()
                decide_button_text_rect.center = decide_button_rect.center
                screen.blit(decide_button_text, decide_button_text_rect)

                # 戻るボタン
                back_button_width = 100
                back_button_height = 50
                back_button_rect = pygame.Rect(decide_button_rect.left - back_button_width - 20, decide_button_rect.centery - back_button_height // 2,
                                            back_button_width, back_button_height)
                if selection_state == 3:
                    pygame.draw.rect(screen, (255, 0, 0), back_button_rect)  # 赤色の戻るボタン
                    pygame.draw.rect(screen, (255, 0, 0), back_button_rect, 2)  # 赤色の枠線を追加
                else:
                    pygame.draw.rect(screen, (255, 0, 0), back_button_rect)  # 赤色の戻るボタン
                    pygame.draw.rect(screen, (0, 0, 0), back_button_rect, 2)  # 黒色の枠線を追加
                back_button_text = font.render("戻る", True, (0, 0, 0))
                back_button_text_rect = back_button_text.get_rect()
                back_button_text_rect.center = back_button_rect.center
                screen.blit(back_button_text, back_button_text_rect)

                # ボタンが押されたかどうかの判定
                mouse_pos = pygame.mouse.get_pos()
                if decide_button_rect.collidepoint(mouse_pos):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        click_sound.play()
                        # 入力された名前でセーブデータを作成/上書き
                        file_path = os.path.join("save", "save_{}.json".format(selected_slot + 1))
                        if os.path.exists(file_path):
                            # すでにデータが保存されている場合は上書き保存の確認
                            confirm_overwrite = show_overwrite_confirm()
                            if confirm_overwrite == True:
                                opening_music.fadeout(2500)  # 音楽をフェードアウト
                                save_game_data(selected_slot + 1, input_text)
                                start_episode0(screen) # エピソード0を開始
                        else:
                            save_game_data(selected_slot + 1, input_text)
                        show_input_box = False
                elif back_button_rect.collidepoint(mouse_pos):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        show_input_box = False

            # 選択処理
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    slot_state = 1 - slot_state  # 選択状態を切り替え
                elif event.key == pygame.K_LEFT:
                    if slot_state == 0:
                        selected_slot = (selected_slot - 1) % NUM_SLOTS
                elif event.key == pygame.K_RIGHT:
                    if slot_state == 0:
                        selected_slot = (selected_slot + 1) % NUM_SLOTS
                elif event.key == pygame.K_RETURN:
                    if slot_state == 0:
                        # 名前入力欄を表示
                        show_input_box = True
                        input_text = slot_infos[selected_slot]["player_name"]
                    else:
                        # show_main_menu関数に遷移
                        show_main_menu()

            # 入力欄のテキスト更新
            if show_input_box:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode.isprintable():
                        input_text += event.unicode

            # 画面更新
            pygame.display.update()


def show_overwrite_confirm():
    # 上書き保存確認画面の表示
    screen.fill((0, 0, 0))
    font = pygame.font.Font('font/Nosutaru-dotMPlusH-10-Regular.ttf', 20)
    selected_state = 0  # 0 -> いいえ、1 -> はい

    # 確認メッセージ表示
    confirm_message = font.render("セーブデータを上書きしますか？", True, (255, 255, 255))
    confirm_message_rect = confirm_message.get_rect()
    confirm_message_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)
    screen.blit(confirm_message, confirm_message_rect)

    # はい/いいえボタン
    button_width = 100
    button_height = 50
    yes_button_rect = pygame.Rect(SCREEN_WIDTH / 2 - button_width - 20, SCREEN_HEIGHT / 2 + 20, button_width, button_height)
    no_button_rect = pygame.Rect(SCREEN_WIDTH / 2 + 20, SCREEN_HEIGHT / 2 + 20, button_width, button_height)

    def draw_buttons():
        # ボタンの描画
        pygame.draw.rect(screen, (0, 255, 0) if selected_state == 1 else (0, 100, 0), yes_button_rect)  # 緑色のはいボタン
        yes_button_text = font.render("はい", True, (0, 0, 0))
        yes_button_text_rect = yes_button_text.get_rect()
        yes_button_text_rect.center = yes_button_rect.center
        screen.blit(yes_button_text, yes_button_text_rect)

        pygame.draw.rect(screen, (255, 0, 0) if selected_state == 0 else (100, 0, 0), no_button_rect)  # 赤色のいいえボタン
        no_button_text = font.render("いいえ", True, (0, 0, 0))
        no_button_text_rect = no_button_text.get_rect()
        no_button_text_rect.center = no_button_rect.center
        screen.blit(no_button_text, no_button_text_rect)

    # ボタンが押されるまで待機
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    selected_state = 1 - selected_state  # 0と1を切り替える
                elif event.key == pygame.K_RETURN:
                    if selected_state == 1:
                        click_sound.play()
                        return True  # はいが選択された場合はTrueを返す
                    else:
                        click_sound.play()
                        return False  # いいえが選択された場合はFalseを返す

        draw_buttons()
        pygame.display.update()


# ゲーム開始
def start_game():
    # 暗転処理
    screen.fill((0, 0, 0))
    create_save_data()


# ゲーム続行
def continue_game():
    font = pygame.font.Font(FONT_PATH, 48)
    selected_slot = 0
    running = True

    while running:
        screen.fill((0, 0, 0))

        # スロット情報を表示
        for i in range(NUM_SLOTS):
            slot_rect = pygame.Rect(
                (SCREEN_WIDTH - SLOT_WIDTH) // 2,
                (SCREEN_HEIGHT - (NUM_SLOTS * SLOT_HEIGHT + (NUM_SLOTS - 1) * SLOT_MARGIN)) // 2 + i * (SLOT_HEIGHT + SLOT_MARGIN),
                SLOT_WIDTH,
                SLOT_HEIGHT
            )
            pygame.draw.rect(screen, (255, 255, 255), slot_rect)
            pygame.draw.rect(screen, (0, 0, 0), slot_rect, 3)

            # スロット情報を読み込む
            file_path = f'save/save_{i + 1}.json'
            if os.path.exists(file_path):
                save_data = load_save_data(file_path)
                player_name = save_data.get("player_name", "空きスロット")
                play_time = save_data.get("play_time", "00:00:00")
                level = save_data.get("level", 1)
            else:
                player_name = "空きスロット"
                play_time = "00:00:00"
                level = 1

            # スロット情報を描画
            slot_text = font.render(f"スロット {i + 1}: {player_name}", True, (0, 0, 0))
            play_time_text = font.render(f"プレイ時間: {play_time}", True, (0, 0, 0))
            level_text = font.render(f"レベル: {level}", True, (0, 0, 0))
            screen.blit(slot_text, (slot_rect.x + SLOT_INFO_MARGIN, slot_rect.y + SLOT_INFO_MARGIN))
            screen.blit(play_time_text, (slot_rect.x + SLOT_INFO_MARGIN, slot_rect.y + SLOT_INFO_MARGIN + 50))
            screen.blit(level_text, (slot_rect.x + SLOT_INFO_MARGIN, slot_rect.y + SLOT_INFO_MARGIN + 100))

        # 選択中のスロットを強調表示
        selected_slot_rect = pygame.Rect(
            (SCREEN_WIDTH - SLOT_WIDTH) // 2,
            (SCREEN_HEIGHT - (NUM_SLOTS * SLOT_HEIGHT + (NUM_SLOTS - 1) * SLOT_MARGIN)) // 2 + selected_slot * (SLOT_HEIGHT + SLOT_MARGIN),
            SLOT_WIDTH,
            SLOT_HEIGHT
        )
        pygame.draw.rect(screen, (255, 0, 0), selected_slot_rect, 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_slot = (selected_slot - 1) % NUM_SLOTS
                elif event.key == pygame.K_DOWN:
                    selected_slot = (selected_slot + 1) % NUM_SLOTS
                elif event.key == pygame.K_RETURN:
                    file_path = f'save/save_{selected_slot + 1}.json'
                    if os.path.exists(file_path):
                        save_data = load_save_data(file_path)
                        # セーブスロットを選択
                        with open('save/selected_save_slot.json', 'w') as f:
                            json.dump({"selected_slot": selected_slot + 1}, f)
                        # ゲームを続ける
                        opening_music.fadeout(2500)  # 音楽をフェードアウト
                        open_world(screen)
                        running = False

        pygame.display.flip()

# スライダーの描画
def draw_slider(label, value, position):
    text = font.render(f"{label}: {int(value * 100)}%", True, (255, 255, 255))
    screen.blit(text, (position[0], position[1] - 30))
    pygame.draw.rect(screen, (255, 255, 255), (*position, 200, 10))
    pygame.draw.rect(screen, (0, 255, 0), (*position, int(value * 200), 10))

# 矢印の描画
def draw_arrow(position):
    arrow = font.render("→", True, (255, 255, 255))
    screen.blit(arrow, (position[0] - 60, position[1] - 20))

def show_options():
    global bgm_volume, se_volume, brightness, selected_slider
    running = True
    while running:
        screen.fill((0, 0, 0))
        
        slider_positions = [
            (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100),
            (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2),
            (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100)
        ]
        
        draw_slider("BGM 音量", bgm_volume, slider_positions[0])
        draw_slider("SE 音量", se_volume, slider_positions[1])
        draw_slider("明るさ", brightness, slider_positions[2])
        
        # 現在選択しているスライダーの左に矢印を表示
        draw_arrow(slider_positions[selected_slider])
        
        # 戻るボタン
        back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 100, 150, 50)
        pygame.draw.rect(screen, (255, 255, 255), back_button_rect)
        back_text = font.render("戻る", True, (0, 0, 0))
        screen.blit(back_text, (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 90))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    running = False
                for i, pos in enumerate(slider_positions):
                    if pos[0] <= event.pos[0] <= pos[0] + 200 and pos[1] <= event.pos[1] <= pos[1] + 10:
                        if i == 0:
                            bgm_volume = (event.pos[0] - pos[0]) / 200
                        elif i == 1:
                            se_volume = (event.pos[0] - pos[0]) / 200
                        elif i == 2:
                            brightness = (event.pos[0] - pos[0]) / 200
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    selected_slider = (selected_slider - 1) % 3
                elif event.key == pygame.K_DOWN:
                    selected_slider = (selected_slider + 1) % 3
                elif event.key == pygame.K_LEFT:
                    if selected_slider == 0:
                        bgm_volume = max(0, bgm_volume - 0.05)
                    elif selected_slider == 1:
                        se_volume = max(0, se_volume - 0.05)
                    elif selected_slider == 2:
                        brightness = max(0, brightness - 0.05)
                elif event.key == pygame.K_RIGHT:
                    if selected_slider == 0:
                        bgm_volume = min(1, bgm_volume + 0.05)
                    elif selected_slider == 1:
                        se_volume = min(1, se_volume + 0.05)
                    elif selected_slider == 2:
                        brightness = min(1, brightness + 0.05)
        
        # 音量と明るさの適用（仮の処理）
        opening_music.set_volume(bgm_volume)

        # SEの音量調整は個別に行う必要があります
        click_sound.set_volume(se_volume)
        # 明るさの調整は画面全体の色を変更することでシミュレート
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(int((1 - brightness) * 255))
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        pygame.display.update()


# ゲーム終了
def quit_game():
    pygame.quit()
    sys.exit()

# タイトル画面に戻る
def return_to_title():
    global state
    state = STATE_GAME
    screen.fill((0, 0, 0))
    time.sleep(1)
    show_main_menu()

# メインループ処理
def main():
    # メイン画面表示
    opening()


if __name__ == '__main__':
    opening()
    while True:
        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # 画面更新
        pygame.display.update()
        clock.tick(FPS)