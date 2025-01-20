import pygame
import random
import json
import math
import time
import random
from dialogue_manager import DialogueManager
from config import FONT_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, screen
from settings import show_menu, key_config
from game_over import game_over
from save_manager import load_save_data, get_selected_save_slot
from variables import *
from draw_utils import draw_image, draw_animated_image


# Pygameの初期化
pygame.init()
pygame.font.init()  # フォントモジュールの初期化
# BGMのロード
first_dialogue_music = pygame.mixer.Sound("music/BGM01worldmap.wav")
battle_music = pygame.mixer.Sound("music/BGM07battle1.wav")
third_dialogue_music = pygame.mixer.Sound("music/BGM16jungle.wav")


# タイルセットの読み込み関数
def load_tileset(filenames, tile_sizes):
    tiles = []
    for filename, size in zip(filenames, tile_sizes):
        tileset_image = pygame.image.load(filename).convert_alpha()
        image_width, image_height = tileset_image.get_size()
        tile_width, tile_height = size
        # print(f"Loading {filename} with size {image_width}x{image_height}")  # デバッグ用出力
        for y in range(0, image_height, tile_height):
            for x in range(0, image_width, tile_width):
                rect = pygame.Rect(x, y, tile_width, tile_height)
                if rect.right <= image_width and rect.bottom <= image_height:
                    tile = tileset_image.subsurface(rect)
                    tiles.append(tile)
                else:
                    raise ValueError(f"Rectangle {rect} is outside the surface area of {filename}")
    return tiles

# フィールドデータを読み込む関数
def load_field_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        return data

# プレイヤー名を取得
selected_save_slot = get_selected_save_slot()
save_data = load_save_data(f'save/save_{selected_save_slot}.json')
player_name = save_data["player_name"]

# マップを描画する関数
def draw_map(screen, map_data, tiles):
    for layer_index, layer in enumerate(map_data):
        if layer_index == 3:  # レイヤー4を非表示にする
            continue
        for y, row in enumerate(layer):
            for x, tile_info in enumerate(row):
                if isinstance(tile_info, list) and len(tile_info) == 3:
                    tile_index, x_offset, y_offset = tile_info
                    tile = tiles[tile_index]
                    screen.blit(tile, (x * TILE_SIZE + x_offset, y * TILE_SIZE + y_offset))

# 移動可能なエリアを取得する関数
def get_passable_areas(map_data):
    passable_areas = []
    for layer_index, layer in enumerate(map_data):
        if layer_index == 3:  # レイヤー4の情報を使用
            for y, row in enumerate(layer):
                for x, tile_info in enumerate(row):
                    if tile_info == [255, 0, 0]:  # 赤く塗られた部分
                        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        passable_areas.append(rect)
    return passable_areas

# Orcの矩形を定義し、オブジェクトとの衝突判定を行う関数
def handle_orc_movement(orc, player_x, player_y, passable_areas):
    if player_x > orc['x']:
        orc['move_x_direction'] = 1
        orc['flip_image'] = False
    elif player_x < orc['x']:
        orc['move_x_direction'] = -1
        orc['flip_image'] = True
    else:
        orc['move_x_direction'] = 0

    if player_y > orc['y']:
        orc['move_y_direction'] = 1
    elif player_y < orc['y']:
        orc['move_y_direction'] = -1
    else:
        orc['move_y_direction'] = 0

    new_x = orc['x'] + orc['move_x_direction'] * ORC_MOVE_SPEED
    new_y = orc['y'] + orc['move_y_direction'] * ORC_MOVE_SPEED
    orc_rect = pygame.Rect(new_x, new_y, CHARACTER_SIZE, CHARACTER_SIZE)
    collision = True  # デフォルトで衝突とする
    for rect in passable_areas:
        if orc_rect.colliderect(rect):
            collision = False  # 赤い部分に衝突した場合は移動可能
            break
    if not collision:
        orc['x'] = new_x
        orc['y'] = new_y


# マップ表示関数
def show_full_map(screen, full_map_image):
    running = True
    map_scale = 1.0
    map_position = [0, 0]
    map_dragging = False
    drag_start_pos = [0, 0]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左クリックでドラッグ開始
                    map_dragging = True
                    drag_start_pos = event.pos
                elif event.button == 4:  # スクロールアップで拡大
                    map_scale = min(map_scale + 0.1, 3.0)
                elif event.button == 5:  # スクロールダウンで縮小
                    map_scale = max(map_scale - 0.1, 0.5)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 左クリックでドラッグ終了
                    map_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if map_dragging:
                    dx = event.pos[0] - drag_start_pos[0]
                    dy = event.pos[1] - drag_start_pos[1]
                    map_position[0] += dx
                    map_position[1] += dy
                    drag_start_pos = event.pos

        # マップの表示位置を制限
        map_width = full_map_image.get_width() * map_scale
        map_height = full_map_image.get_height() * map_scale
        map_position[0] = min(0, max(map_position[0], SCREEN_WIDTH - map_width))
        map_position[1] = min(0, max(map_position[1], SCREEN_HEIGHT - map_height))

        screen.fill((0, 0, 0))
        scaled_map = pygame.transform.scale(full_map_image, (int(full_map_image.get_width() * map_scale), int(full_map_image.get_height() * map_scale)))
        screen.blit(scaled_map, map_position)
        pygame.display.flip()
        pygame.time.wait(100)  # 100ミリ秒待つ

# 攻撃が当たったかどうかを判定する関数
def is_attack_hit(attacker_x, attacker_y, target_x, target_y, direction):
    if direction == 'right':
        return attacker_x < target_x < attacker_x + ATTACK_RANGE and abs(attacker_y - target_y) < CHARACTER_SIZE
    elif direction == 'left':
        return attacker_x - ATTACK_RANGE < target_x < attacker_x and abs(attacker_y - target_y) < CHARACTER_SIZE
    elif direction == 'up':
        return attacker_y - ATTACK_RANGE < target_y < attacker_y and abs(attacker_x - target_x) < CHARACTER_SIZE
    elif direction == 'down':
        return attacker_y < target_y < attacker_y + ATTACK_RANGE and abs(attacker_x - target_x) < CHARACTER_SIZE
    return False

# オークの攻撃が当たったかどうかを判定する関数
def is_orc_attack_hit(orc_x, orc_y, player_x, player_y, direction):
    if direction == 'right':
        return orc_x + 5 * TILE_SIZE >= player_x and orc_x < player_x and orc_y == player_y
    elif direction == 'left':
        return orc_x - 5 * TILE_SIZE <= player_x and orc_x > player_x and orc_y == player_y
    return False

# オークの攻撃を処理する関数
def get_closest_orc(player_x, player_y, orcs):
    closest_orc = None
    min_distance = float('inf')
    for orc in orcs:
        distance = math.hypot(player_x - orc['x'], player_y - orc['y'])
        if distance < min_distance:
            min_distance = distance
            closest_orc = orc
    return closest_orc

# ハートをドロップする関数
def drop_heart(x, y):
    # if random.random() < :  # 50%の確率でハートをドロップ
    hearts.append({'x': x, 'y': y, 'animation_index': 0})

# ハートを更新する関数
def update_hearts():
    for heart in hearts:
        heart['animation_index'] = (heart['animation_index'] + 1) % len(heart_images)
        screen.blit(heart_images[heart['animation_index']], (heart['x'], heart['y']))

# ハートを描画する関数
def check_heart_pickup(player_x, player_y):
    global health
    pickup_range = 50  # 拾える範囲を50に設定
    for heart in hearts:
        if abs(player_x - heart['x']) < pickup_range and abs(player_y - heart['y']) < pickup_range:
            return heart
    return None

# ハートを取得したときの処理
def handle_heart_pickup(player_x, player_y):
    global health
    heart = check_heart_pickup(player_x, player_y)
    if heart:
        hearts.remove(heart)
        health = min(100, health + 20)  # 体力を20回復

# ダイアログモデル関数
def dialogue_model(screen, map_data, tiles, dialogue_manager):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    dialogue_manager.next_dialogue()

        screen.fill((0, 0, 0))
        draw_map(screen, map_data, tiles)  # フィールドを描画

        # ダイアログボックスの大きさを設定
        dialogue_box_width = SCREEN_WIDTH
        dialogue_box_height = 200
        dialogue_box_x = 0
        dialogue_box_y = SCREEN_HEIGHT - dialogue_box_height

        # 選択されたセーブスロットを読み込む
        with open('save/selected_save_slot.json', 'r') as file:
            selected_save_slot = json.load(file)["selected_slot"]

        # プレイヤー名を取得
        save_data = load_save_data(f'save/save_{selected_save_slot}.json')
        player_name = save_data["player_name"]

        # ダイアログボックスの背景を描画
        dialogue_box_rect = pygame.Rect(dialogue_box_x, dialogue_box_y, dialogue_box_width, dialogue_box_height)
        dialogue_box_surface = pygame.Surface((dialogue_box_width, dialogue_box_height))
        dialogue_box_surface.set_alpha(100)  # 透過度を設定（0-255）
        dialogue_box_surface.fill((0, 0, 0))  # 黒い四角
        screen.blit(dialogue_box_surface, (dialogue_box_x, dialogue_box_y))
        pygame.draw.rect(screen, (255, 255, 255), dialogue_box_rect, 3)  # 白い枠線

        # セリフの内容に応じて適切な画像を表示
        current_dialogue = dialogue_manager.get_current_dialogue()
        current_dialogue = current_dialogue.replace("レイアン", player_name)  # プレイヤー名に置き換え

        if current_dialogue.startswith(f"{player_name}："):
            photo_image = pygame.image.load('characters/icons/00002.png')
            photo_image = pygame.transform.scale(photo_image, (180, 180))
            screen.blit(photo_image, (dialogue_box_x + 10, dialogue_box_y + 10))
        elif current_dialogue.startswith(f"{player_name}の父："):
            photo_image = pygame.image.load('characters/icons/00010.png')
            photo_image = pygame.transform.scale(photo_image, (180, 180))
            screen.blit(photo_image, (dialogue_box_x + 10, dialogue_box_y + 10))
        elif current_dialogue.startswith("オーク："):
            photo_image = pygame.image.load('characters/icons/00009.png')
            photo_image = pygame.transform.scale(photo_image, (180, 180))
            screen.blit(photo_image, (dialogue_box_x + 10, dialogue_box_y + 10))

        # テキストを一度に表示
        font = pygame.font.Font(FONT_PATH, 36)
        rendered_text = font.render(current_dialogue, True, (255, 255, 255))
        # テキストを中央に配置
        text_rect = rendered_text.get_rect(center=(dialogue_box_x + dialogue_box_width // 2, dialogue_box_y + dialogue_box_height // 2))
        screen.blit(rendered_text, text_rect)

        pygame.display.flip()
        # セリフがすべて終わったかどうかを確認
        if dialogue_manager.is_finished():
            running = False

# 1番目のダイアログ
def first_dialogue(screen, map_data, tiles):
    # BGMを再生
    first_dialogue_music.play(-1)

    dialogue_texts = [
        "炉の火が燃え、金槌を打つ音が響いている。",
        "窓からは朝日が差し込み、部屋を照らしている。",
        "レイアン：よし、今日も一日鍛錬だ！",
        "レイアンは、磨き上げた剣を手に取り、試しに振るう。",
        "レイアンの父：レイアン、もうそんな時間か。朝食は済ませたのか？",
        "レイアン：はい、もう済ませました。",
        "レイアン：今日は森に行って、父上から貰った新しい剣を試したいのです。",
        "レイアンの父：そうか。気を付けて行ってこい。",
        "レイアンの父：そして、くれぐれも無理はするなよ。",
        "レイアン：はい、分かりました！",
        "レイアンは、父親に頭を下げ、家を出る。",
        "レイアン：（この剣、父さんにもらった宝物だ。）",
        "レイアン：（いつか、この剣で伝説の剣士になるんだ。）",
        "レイアンは、村の外れの森へ向かう。",
        "移動は矢印キーで行います。",
        "ESCキーでメニューを開くことができます。"
        "まずは森の奥へ進もう！"
    ]
    dialogue_manager = DialogueManager(FONT_PATH, SCREEN_HEIGHT)
    for dialogue in dialogue_texts:
        dialogue_manager.add_dialogue(dialogue)

    dialogue_model(screen, map_data, tiles, dialogue_manager)

# 2番目のダイアログ
def second_dialogue(screen, map_data, tiles):
    dialogue_texts = [
        "森は日陰が多く、薄暗い。木々の葉がざわめき、鳥の鳴き声が聞こえる。",
        "レイアン：（よし、ここで新しい技を試してみよう。）",
        "すると少し遠くからかすかに光るものが見える。",
        "レイアン：（あれは…？）",
        "レイアンは、ゆっくりと光るものへと近づいていく。",
        "と、その時！レイアンの前にオークが現れた！",
        "オーク：グルルル…美味そうな人間が来たな！",
        "オーク：お前を食ってやる！"
        "オークが現れました！",
        "スペースキーで攻撃しましょう！"
    ]
    dialogue_manager = DialogueManager(FONT_PATH, SCREEN_HEIGHT)
    for dialogue in dialogue_texts:
        dialogue_manager.add_dialogue(dialogue)

    dialogue_model(screen, map_data, tiles, dialogue_manager)

    # 現在流れている楽曲をフェードアウト
    first_dialogue_music.fadeout(1000)  # 1秒かけてフェードアウト
    # フェードアウトが完了するまで待機
    pygame.time.wait(1000)
    # battle_musicを再生
    battle_music.play(-1)

# 3番目のダイアログ
def third_dialogue(screen, map_data, tiles):
    battle_music.fadeout(1000)  # 1秒かけてフェードアウト
    # フェードアウトが完了するまで待機
    pygame.time.wait(1000)
    third_dialogue_music.play(-1)
    dialogue_texts = [
        "レイアン：あれは…？",
        "レイアンは、ゆっくりと光るものへと近づいていく。",
        "光るものは、宝箱に入っていた剣だった。剣からは、神秘的な光が放たれていた。",
        "レイアン：（これは…！）",
        "レイアン：（この剣、父上に見せてみよう！)",
        "レイアン：（きっと喜んでくれるだろう。）",
        "レイアンは、剣を手に取り、光を浴びる。",
        "その瞬間、彼の体中に力がみなぎる。",
        "レイアン：（この剣、何か特別な力を持っている…！）",
        ""
        "レイアン：父上に報告しよう！"
    ]
    dialogue_manager = DialogueManager(FONT_PATH, SCREEN_HEIGHT)
    for dialogue in dialogue_texts:
        dialogue_manager.add_dialogue(dialogue)

    dialogue_model(screen, map_data, tiles, dialogue_manager)

# 4番目のダイアログ
def fourth_dialogue(screen, map_data, tiles):
    dialogue_texts = [
        "夕焼け空の下、レイアンは村に戻ってくる。",
        "レイアンの父：レイアン、どうしたんだ？ 随分と顔色が悪いぞ。",
        "レイアン：父上、これを見てください！",
        "レイアンは、慎重に背中から剣を取り出した",
        "レイアンの父：これは…一体どこで？",
        "レイアン：森の奥深くで、岩に突き刺さっていたんです。",
        "レイアン：この剣には、何か特別な力があるような気がして…。",
        "レイアンの父は、剣をじっと見つめる",
        "レイアンの父：これは…ただの剣ではないな。",
        "レイアンの父：どこかの遺跡から出てきたものかもしれない。",
        "レイアン：遺跡…？",
        "レイアンの父：そうだ。遺跡には、古代の文明が残されていることがある。",
        "レイアンの父：その剣は、きっと何かしらの力を持っているだろう。",
        "レイアン：父上、僕、この剣を持って旅に出たいんです。",
        "レイアン：この剣の秘密を解き明かしたいし、もっと強くなりたい！",
        "レイアンの父：旅か…危険がつきものだ。",
        "レイアン：でも、僕は…！",
        "レイアンの父：分かった。君の決意を尊重しよう。",
        "レイアン：本当ですか！？",
        "レイアンの父：この村を出るのも自由だ。",
        "レイアンの父：だが、くれぐれも気を付けてくれ。",
        "レイアン：はい！",
        "レイアンの父は、レイアンの頭を優しく撫でた。",
        "レイアン：（父上、ありがとう…！）",
        "レイアンは、父親と抱き合い、家を出た。",
    ]
    dialogue_manager = DialogueManager(FONT_PATH, SCREEN_HEIGHT)
    for dialogue in dialogue_texts:
        dialogue_manager.add_dialogue(dialogue)

    dialogue_model(screen, map_data, tiles, dialogue_manager)

# デバック用のキャラクター座標を描画する関数
def draw_character_coordinates(screen, x, y):
    font = pygame.font.Font(FONT_PATH, 24)
    coordinates_text = f"X: {x}, Y: {y}"
    rendered_text = font.render(coordinates_text, True, (255, 255, 255))
    screen.blit(rendered_text, (10, SCREEN_HEIGHT - 30))

# 街の名前を描画する関数
def draw_city_name(screen, city_name):
    font = pygame.font.Font(FONT_PATH, 24)
    city_name_text = font.render(city_name, True, (255, 255, 255))
    screen.blit(city_name_text, (10, SCREEN_HEIGHT - 30))

# エピソード0-0の関数
def episode0_0():
    global tiles, map_data, selected_tile, temp_tile, palette_scroll_y, PALETTE_WIDTH, PALETTE_HEIGHT,heart_images,orcs,health,show_city_name_flag, player_name, play_time, player_level, player_position, player_inventory, player_health, selected_save_slot, character_x, character_y
    # 画面を暗転させる
    screen.fill((0, 0, 0))
    pygame.display.flip()
    pygame.time.wait(1000)  # 1秒待つ

    # タイルセットを読み込む
    tiles = load_tileset(tileset_filenames, tile_sizes)

    # フィールドデータを読み込む
    map_data = load_field_data("field_data.json")

    # ダイアログの実行フラグ
    second_dialogue_executed = False
    third_dialogue_executed = False
    fourth_dialogue_executed = False


    # フェードイン処理
    for alpha in range(0, 256, 5):
        screen.fill((0, 0, 0))
        draw_map(screen, map_data, tiles)  # フィールドを描画
        fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(255 - alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.wait(50)  # フェードインの速度を調整

    # ダイアログを表示
    first_dialogue(screen, map_data, tiles)


    # メインループ
    running = True
    idle_index = 0
    walk_index = 0
    attack_index = 0
    hurt_index = 0
    death_index = 0
    is_walking = False
    is_attacking = False
    is_hurt = False
    is_dead = False
    move_x_direction = 0
    move_y_direction = 0
    flip_image = False
    animation_counter = 0  # アニメーション速度を制御するためのカウンター
    current_attack_images = attack_images1  # 現在の攻撃アニメーション
    attack_direction = 'right'  # プレイヤーの攻撃方向を追加
    passable_areas = get_passable_areas(map_data)  # 移動可能なエリアを取得

    # プレイヤーの初期位置とステータス
    character_x = 200
    character_y = 100
    player_position = {"x": character_x, "y": character_y}  # 初期位置を設定
    player_inventory = []
    player_health = 100
    player_level = 1

    # キー入力の状態を管理する変数
    key_pressed = {
        "up": False,
        "down": False,
        "left": False,
        "right": False
    }

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not is_attacking and not is_dead:  # 攻撃中および死亡中でない場合のみ移動を許可
                    if event.key == key_config["right"]:
                        key_pressed["right"] = True
                        move_x_direction = 1  # 右方向
                        move_y_direction = 0
                        flip_image = False
                        attack_direction = 'right'  # 攻撃方向を右に設定
                    elif event.key == key_config["left"]:
                        key_pressed["left"] = True
                        move_x_direction = -1  # 左方向
                        move_y_direction = 0
                        flip_image = True
                        attack_direction = 'left'  # 攻撃方向を左に設定
                    elif event.key == key_config["up"]:
                        key_pressed["up"] = True
                        move_x_direction = 0
                        move_y_direction = -1  # 上方向
                    elif event.key == key_config["down"]:
                        key_pressed["down"] = True
                        move_x_direction = 0
                        move_y_direction = 1  # 下方向
                if event.key == key_config["attack"] and not is_dead and not is_attacking:
                    is_attacking = True
                    attack_index = 0
                    current_attack_images = random.choice([attack_images1, attack_images2])  # ランダムに攻撃アニメーションを選択
                    animation_counter = 0  # アニメーションカウンターをリセット
                elif event.key == key_config["map"]:
                    show_full_map(screen, full_map_image)
                elif event.key == key_config["back"]:
                    show_menu(screen)
                elif event.key == key_config["pickup"]:
                    handle_heart_pickup(character_x, character_y)
                elif event.key == pygame.K_z:
                    show_city_name_flag = True
            elif event.type == pygame.KEYUP:
                if event.key == key_config["right"]:
                    key_pressed["right"] = False
                elif event.key == key_config["left"]:
                    key_pressed["left"] = False
                elif event.key == key_config["up"]:
                    key_pressed["up"] = False
                elif event.key == key_config["down"]:
                    key_pressed["down"] = False

        # 移動処理
        if key_pressed["right"]:
            is_walking = True
            move_x_direction = 1
            move_y_direction = 0
            flip_image = False
            attack_direction = 'right'
        elif key_pressed["left"]:
            is_walking = True
            move_x_direction = -1
            move_y_direction = 0
            flip_image = True
            attack_direction = 'left'
        elif key_pressed["up"]:
            is_walking = True
            move_x_direction = 0
            move_y_direction = -1
        elif key_pressed["down"]:
            is_walking = True
            move_x_direction = 0
            move_y_direction = 1
        else:
            is_walking = False

        # キャラクターの位置を更新
        player_position["x"] += move_x_direction
        player_position["y"] += move_y_direction

        # プレイ時間を更新
        elapsed_time = time.time() - start_time
        play_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

        # 画面をクリア
        screen.fill((0, 0, 0))

        # フィールドを再描画
        draw_map(screen, map_data, tiles)

        # ハートの更新と描画
        update_hearts()

        # 都市名を表示
        if show_city_name_flag:
            draw_city_name(screen, "都市名：Suncrossham")

        # プレイヤーの座標をチェックしてsecond_dialogue関数に遷移
        if not second_dialogue_executed and 1500 <= character_x <= 1600 and 200 <= character_y <= 500:
            second_dialogue(screen, map_data, tiles)
            second_dialogue_executed = True

        # プレイヤーの座標をチェックしてthird_dialogue関数に遷移
        if not third_dialogue_executed and 1600 <= character_x <= 1620 and 34 <= character_y <= 35:
            third_dialogue(screen, map_data, tiles)
            third_dialogue_executed = True

        # third_dialogueが終了した後、キャラクターが指定された座標範囲に来たらfourth_dialogueに遷移
        if third_dialogue_executed and not fourth_dialogue_executed and 1530 <= character_x <= 1650 and character_y >= 750:
            fourth_dialogue(screen, map_data, tiles)
            fourth_dialogue_executed = True

        # fourth_dialogueが終了した後、キャラクターが指定された座標範囲に来たらマップを暗くしてepisode1に遷移
        if fourth_dialogue_executed and 1570 <= character_x <= 1662 and character_y >= 1000:
            # マップを暗くする処理
            for alpha in range(0, 256, 5):
                screen.fill((0, 0, 0))
                draw_map(screen, map_data, tiles)  # フィールドを描画
                fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                fade_surface.fill((0, 0, 0))
                fade_surface.set_alpha(alpha)
                screen.blit(fade_surface, (0, 0))
                pygame.display.flip()
                pygame.time.wait(50)  # フェードインの速度を調整
            # episode1に遷移
            from episode1 import episode1  # 遅延インポート
            episode1(screen, third_dialogue_music)
            running = False


        if health <= 0:
            is_dead = True
            is_walking = False
            is_attacking = False
            is_hurt = False

        if is_dead:
            draw_animated_image(screen, death_images, death_index, character_x, character_y, flip_image)
            if animation_counter % ANIMATION_SPEED == 0:
                death_index += 1
                if death_index >= len(death_images):
                    game_over()
        else:
            if is_walking and not is_attacking:
                new_x = character_x + move_x_direction * MOVE_SPEED
                new_y = character_y + move_y_direction * MOVE_SPEED
                if 0 <= new_x <= SCREEN_WIDTH - CHARACTER_SIZE and 0 <= new_y <= SCREEN_HEIGHT - CHARACTER_SIZE:
                    character_rect = pygame.Rect(new_x, new_y, CHARACTER_SIZE, CHARACTER_SIZE)
                    collision = True
                    for rect in passable_areas:
                        if character_rect.colliderect(rect):
                            collision = False
                            break
                    if not collision:
                        character_x = new_x
                        character_y = new_y
                draw_animated_image(screen, walk_images, walk_index, character_x, character_y, flip_image)
                if animation_counter % ANIMATION_SPEED == 0:
                    walk_index = (walk_index + 1) % len(walk_images)
            elif is_attacking:
                draw_animated_image(screen, current_attack_images, attack_index, character_x, character_y, flip_image)
                if animation_counter % ANIMATION_SPEED == 0:
                    attack_index += 1
                    if attack_index >= len(current_attack_images):
                        is_attacking = False
                        for orc in orcs:
                            if is_attack_hit(character_x, character_y, orc['x'], orc['y'], attack_direction):
                                orc['hp'] -= 10
                                if orc['hp'] <= 0:
                                    orc['state'] = 'death'
                                    orc['death_index'] = 0
                                else:
                                    orc['state'] = 'hurt'
            elif is_hurt:
                draw_animated_image(screen, hurt_images, hurt_index, character_x, character_y, flip_image)
                if animation_counter % ANIMATION_SPEED == 0:
                    hurt_index += 1
                    if hurt_index >= len(hurt_images):
                        is_hurt = False
            else:
                draw_animated_image(screen, idle_images, idle_index, character_x, character_y, flip_image)
                if animation_counter % ANIMATION_SPEED == 0:
                    idle_index = (idle_index + 1) % len(idle_images)

        for orc in orcs:
            orc_x, orc_y = orc['x'], orc['y']
            distance_to_player = math.hypot(character_x - orc_x, character_y - orc_y)
            if orc['state'] != 'attack' and orc['state'] != 'hurt' and orc['state'] != 'death':
                if distance_to_player < ORC_ATTACK_RADIUS:
                    orc['state'] = 'attack'
                    orc['attack_index'] = 0
                    orc['attack_direction'] = 'right' if character_x > orc_x else 'left'
                elif distance_to_player < ORC_DETECTION_RADIUS:
                    orc['state'] = 'walk'
                else:
                    orc['state'] = 'idle'

            if orc['state'] == 'walk':
                handle_orc_movement(orc, character_x, character_y, passable_areas)
                draw_animated_image(screen, orc_walk_images, orc['walk_index'], orc['x'], orc['y'], orc['flip_image'])
                if animation_counter % ORC_ANIMATION_SPEED == 0:
                    orc['walk_index'] = (orc['walk_index'] + 1) % len(orc_walk_images)
            elif orc['state'] == 'attack':
                draw_animated_image(screen, orc_attack_images, orc['attack_index'], orc['x'], orc['y'], orc['flip_image'])
                if animation_counter % (ORC_ANIMATION_SPEED * ORC_ATTACK_FREQUENCY) == 0:
                    orc['attack_index'] += 1
                    if orc['attack_index'] >= len(orc_attack_images):
                        orc['state'] = 'idle'
                    else:
                        if orc['attack_index'] == 4:
                            if is_attack_hit(orc['x'], orc['y'], character_x, character_y, orc['attack_direction']):
                                if not is_hurt and not is_dead:
                                    is_hurt = True
                                    hurt_index = 0
                                    health -= 10
                                    if health < 0:
                                        health = 0
            elif orc['state'] == 'hurt':
                draw_animated_image(screen, orc_hurt_images, orc['hurt_index'], orc['x'], orc['y'], orc['flip_image'])
                if animation_counter % ORC_ANIMATION_SPEED == 0:
                    orc['hurt_index'] += 1
                    if orc['hurt_index'] >= len(orc_hurt_images):
                        orc['state'] = 'idle'
                        orc['hurt_index'] = 0
            elif orc['state'] == 'death':
                draw_animated_image(screen, orc_death_images, orc['death_index'], orc['x'], orc['y'], orc['flip_image'])
                if animation_counter % ANIMATION_SPEED == 0:
                    orc['death_index'] += 1
                    if orc['death_index'] >= len(orc_death_images):
                        orcs.remove(orc)
                        drop_heart(orc['x'], orc['y'])
            else:
                draw_animated_image(screen, orc_idle_images, orc['idle_index'], orc['x'], orc['y'], orc['flip_image'])
                if animation_counter % ORC_ANIMATION_SPEED == 0:
                    orc['idle_index'] = (orc['idle_index'] + 1) % len(orc_idle_images)

        closest_orc = get_closest_orc(character_x, character_y, orcs)
        if closest_orc:
            hp_percentage = closest_orc['hp'] / 100
            health_meter_width = health_meter_full.get_width()
            health_meter_height = health_meter_full.get_height()
            current_health_width = int(health_meter_width * hp_percentage)
            screen.blit(health_meter_empty, (SCREEN_WIDTH - health_meter_width - 100, 10))
            screen.blit(health_meter_full, (SCREEN_WIDTH - health_meter_width - 44, 23), (0, 0, current_health_width, health_meter_height))

        screen.blit(health_bar_bg, (150, 10))
        current_health_width = int(health_bar_fg.get_width() * (health / 100))
        screen.blit(health_bar_fg, (192, 32), (0, 0, current_health_width, health_bar_fg.get_height()))

        pygame.draw.circle(screen, (255, 0, 0), minimap_position, minimap_radius, 2)
        pygame.draw.circle(screen, (0, 255, 0), minimap_position, 5)

        animation_counter += 1
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    episode0_0()