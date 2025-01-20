# FILE: open_world.py
import pygame
import math
import time
from config import SCREEN_WIDTH, SCREEN_HEIGHT, screen
from settings import show_menu, key_config
from save_manager import *
from episode0_0 import *
from variables import *
from player_data import *
from dialogue_manager import *
from config import FONT_PATH
from draw_utils import draw_animated_image
from game_over import game_over

# Pygameの初期化
pygame.init()
pygame.font.init()

# 武器屋の位置を定義
weapon_shop_positions = [
    {"x": 505, "y": 194}
]

# 武器屋のアイコンをロード
weapon_shop_icon = pygame.image.load("images/weapon_shop_icon.png")

# 全体マップの画像をロード
full_map_image = pygame.image.load("maps/country_of_lil_vale.png")

# プレイ時間を計測するための変数
start_time = time.time()

# # プレイヤーの現在位置を表示する関数
# def draw_player_position(screen, font, x, y):
#     position_text = font.render(f"X: {x}, Y: {y}", True, (255, 255, 255))
#     screen.blit(position_text, (10, SCREEN_HEIGHT - 30))

# 武器屋のアイコンを描画する関数
def draw_weapon_shops(screen, weapon_shop_positions, weapon_shop_icon):
    for position in weapon_shop_positions:
        screen.blit(weapon_shop_icon, (position["x"], position["y"]))

# マップ遷移の処理
def check_map_transition(character_x, character_y, current_map):
    if current_map == "field_data_0-0.json":
        if character_x == 1856 and 930 <= character_y <= 1016:  # 右端に到達
            return "field_data_0-1.json", 30, 968  # 0-1に遷移
        elif character_y > SCREEN_HEIGHT - TILE_SIZE:  # 下端に到達
            return "field_data_1-0.json", character_x, 0  # 1-0に遷移
    elif current_map == "field_data_0-1.json":
        if character_x < 0 and 898 <= character_y <= 1016:  # 左端に到達
            return "field_data_0-0.json", 1856, 968  # 0-0に遷移
    elif current_map == "field_data_1-0.json":
        if character_y < 0:  # 上端に到達
            return "field_data_0-0.json", character_x, SCREEN_HEIGHT - TILE_SIZE  # 0-0に遷移
    elif current_map == "field_data_0-1.json":
        if character_x < 0 and 898 <= character_y <= 1016:
            return "field_data_0-0.json", 1856, 968  # 0-0に遷移
        elif character_y > SCREEN_HEIGHT - TILE_SIZE:  # 下端に到達
            return "field_data_1-0.json", character_x, 0  # 1-0に遷移
    elif character_x >= 1856 and 1010 <= character_y <= 1050:
        return "field_data_1-0.json", 0, 45  # 1-0に遷移
    return current_map, character_x, character_y

# オープンワールドのダイアログ
def open_world_dialogue(screen, map_data, tiles):
    dialogue_texts = [
        "ここからオープンワールドの世界です。",
        "自由に移動して、冒険を楽しんでください。",
        "スペースキーで攻撃ができます。",
        "Eキーでアイテムを拾うことができます。",
        "Mキーでフルマップを表示します。",
        "Iキーでインベントリを表示します。",
        "Zキーで都市名を表示します。",
        "Sキーでセーブします。",
        "武器屋に入るにはEキーを押してください。",
        "オークを倒すとゼニーを手に入れることができます。",
        "ゼニーは武器屋で武器を購入する際に使用します。",
        "ゼニーを手に入れたらセーブしておきましょう。",
        "オークを倒すとハートが出現します。",
        "ハートを拾うと体力が回復します。",
        "体力が0になるとゲームオーバーです。",
        "オークを倒してゼニーを稼ぎ、レベルを上げましょう。",
        "それでは、冒険を楽しんでください！"
    ]
    dialogue_manager = DialogueManager(FONT_PATH, SCREEN_HEIGHT)
    for dialogue in dialogue_texts:
        dialogue_manager.add_dialogue(dialogue)

    dialogue_model(screen, map_data, tiles, dialogue_manager)

def open_world(screen):
    global tiles, map_data, selected_tile, temp_tile, palette_scroll_y, PALETTE_WIDTH, PALETTE_HEIGHT,heart_images,orcs,health,show_city_name_flag, player_name, play_time, player_level, player_position, player_inventory, player_health, selected_save_slot, character_x, character_y
    # 画面を暗転させる
    screen.fill((0, 0, 0))
    pygame.display.flip()
    pygame.time.wait(1000)

    # セーブデータを読み込む
    selected_save_slot = get_selected_save_slot()
    save_data = load_save_data(f'save/save_{selected_save_slot}.json')

    # フォントの初期化
    font = pygame.font.Font(FONT_PATH, 24)

    # タイルセットを読み込む
    tiles = load_tileset(tileset_filenames, tile_sizes)

    # フィールドデータを読み込む
    current_map = "field_data_0-0.json"
    map_data = load_field_data(current_map)

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

    # オープンワールドのダイアログを表示
    open_world_dialogue(screen, map_data, tiles)


    # プレイヤーの初期位置をセーブデータから取得
    if "position" in save_data:
        player_position = save_data["position"]
        character_x = player_position["x"]
        character_y = player_position["y"]
    else:
        character_x = 350
        character_y = 350
        player_position = {"x": character_x, "y": character_y}

    # 移動可能なエリアを取得
    passable_areas = get_passable_areas(map_data)

    # プレイヤーの初期位置が通行可能なエリア内にあるか確認
    if not any(area.collidepoint(character_x, character_y) for area in passable_areas):
        # 近くの移動可能なエリアを探す
        closest_passable_area = min(passable_areas, key=lambda area: math.hypot(area.x - character_x, area.y - character_y))
        character_x, character_y = closest_passable_area.x, closest_passable_area.y
        player_position = {"x": character_x, "y": character_y}


    orc_x, orc_y = 1600, 300 # オークの初期位置

    # プレイヤー名をセーブデータから取得
    if "player_name" in save_data:
        player_name = save_data["player_name"]
    # プレイヤーレベルをセーブデータから取得
    if "level" in save_data:
        player_level = save_data["level"]
    # プレイヤーインベントリをセーブデータから取得
    if "inventory" in save_data:
        player_inventory = save_data["inventory"]
    # プレイヤーヘルスをセーブデータから取得
    if "health" in save_data:
        player_health = save_data["health"]
    # ゼニーをセーブデータから取得
    if "zenny" in save_data:
        zenny = save_data["zenny"]
    else:
        zenny = 0



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
    attack_direction = 'right'  # プレイ5の攻撃方向を追加
    # キー入力の状態を管理する変数
    key_pressed = {
        "up": False,
        "down": False,
        "left": False,
        "right": False
    }

    fire_balls = []  # ファイアボールのリスト
    explosions = []  # 爆発のリスト
    zenny_messages = []  # ゼニー取得メッセージのリスト

    # オークのリスポーンタイマーを設定
    orc_respawn_time = 5000  # 5秒ごとにリスポーン
    last_orc_respawn = pygame.time.get_ticks()
    orc_kill_count = 0  # オークを倒した回数
    orc_kill_reset_time = 20000  # 20秒でリセット
    last_kill_time = pygame.time.get_ticks()

    while running:
        current_time = pygame.time.get_ticks()
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
                    print(character_x, character_y)
                elif event.key == pygame.K_x:
                    print(f"キャラクターの座標: ({character_x}, {character_y})")
                    print(in_weapon_shop_area)
                elif event.key == key_config["magic"]:  # 魔法キーでファイアボールを発動
                    fire_balls.append({
                        "x": character_x,
                        "y": character_y + 20,
                        "direction": attack_direction,
                        "index": 0,
                        "start_x": character_x,
                        "start_y": character_y + 20
                    })
                elif event.key == key_config["inventory"]:
                    import inventory #遅延インポート
                    inventory.inventory_screen(screen)
                elif event.key == key_config["save"]:
                    selected_save_slot = get_selected_save_slot()
                    save_data = {
                        "player_name": player_name,
                        "play_time": play_time,
                        "level": player_level,
                        "position": player_position,
                        "inventory": player_inventory,
                        "health": player_health,
                        "zenny": zenny
                    }
                    save_game(f'save/save_{selected_save_slot}.json', save_data)
                    # 画面を黒にして保存完了メッセージを表示
                    screen.fill((0, 0, 0))
                    font = pygame.font.Font(FONT_PATH, 48)
                    save_text = font.render("保存しました", True, (255, 255, 255))
                    save_text_rect = save_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    screen.blit(save_text, save_text_rect)
                    pygame.display.flip()
                    pygame.time.wait(2000)  # 2秒待つ
                elif event.key == pygame.K_RETURN and in_weapon_shop_area:
                    # 武器屋のプログラムに移行
                    from shop import weapon_shop #遅延インポート
                    weapon_shop()
            elif event.type == pygame.KEYUP:
                if event.key == key_config["right"]:
                    key_pressed["right"] = False
                elif event.key == key_config["left"]:
                    key_pressed["left"] = False
                elif event.key == key_config["up"]:
                    key_pressed["up"] = False
                elif event.key == key_config["down"]:
                    key_pressed["down"] = False

        # マップ遷移のチェック
        new_map, new_x, new_y = check_map_transition(character_x, character_y, current_map)
        if new_map != current_map:
            current_map = new_map
            character_x = new_x
            character_y = new_y
            move_x_direction = 0
            move_y_direction = 0
            map_data = load_field_data(current_map)
            passable_areas = get_passable_areas(map_data)

        # オークのリスポーン処理
        if current_time - last_orc_respawn > orc_respawn_time and len(orcs) < 5:  # Orcの数を制限
            orc_x = random.randint(1548, 1656)
            orc_y = random.randint(0, 252)
            orcs.append({
                'x': orc_x,
                'y': orc_y,
                'state': 'idle',
                'idle_index': 0,
                'walk_index': 0,
                'attack_index': 0,
                'hurt_index': 0,
                'death_index': 0,
                'flip_image': False,
                'hp': 100,
                'move_x_direction': 0,
                'move_y_direction': 0
            })
            last_orc_respawn = current_time

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
            move_x_direction = 0
            move_y_direction = 0

        # 都市名を表示
        if show_city_name_flag:
            draw_city_name(screen, "都市名：Qrepus")

        # キャラクターの位置を更新
        new_character_x = character_x + move_x_direction
        new_character_y = character_y + move_y_direction

        # 移動先が通行可能か確認
        if any(area.collidepoint(new_character_x, new_character_y) for area in passable_areas):
            character_x = new_character_x
            character_y = new_character_y

        # プレイ時間を更新
        elapsed_time = time.time() - start_time
        play_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

        # プレイヤーデータを更新
        update_player_data(player_name, play_time, player_level, player_inventory, player_position, player_health)

        # 武器屋のアイコンを描画
        draw_weapon_shops(screen, weapon_shop_positions, weapon_shop_icon)

        # 画面をクリア
        screen.fill((0, 0, 0))

        # フィールドを再描画
        draw_map(screen, map_data, tiles)

        # キャラクターが指定された座標内にいるかどうかをチェック
        in_weapon_shop_area = 485 <= character_x <= 520 and 190 <= character_y <= 194
        # キャラクターが指定された座標内にいる場合、「E」を表示
        if in_weapon_shop_area:
            font = pygame.font.Font(FONT_PATH, 24)
            e_text = font.render("武器屋に入る", True, (255, 255, 255))
            screen.blit(e_text, (character_x + CHARACTER_SIZE // 2, character_y - 20))

        if health <= 0:
            is_dead = True
            is_walking = False
            is_attacking = False
            is_hurt = False

        # ファイアボールの更新と描画
        fire_balls_to_remove = []
        for fire_ball in fire_balls[:]:
            if fire_ball["direction"] == "right":
                fire_ball["x"] += 10
            elif fire_ball["direction"] == "left":
                fire_ball["x"] -= 10

            fire_ball_image = fire_ball_images[fire_ball["index"]]
            if fire_ball["direction"] == "left":
                fire_ball_image = pygame.transform.flip(fire_ball_image, True, False)
            screen.blit(fire_ball_image, (fire_ball["x"], fire_ball["y"]))

            if animation_counter % ANIMATION_SPEED == 0:
                fire_ball["index"] = (fire_ball["index"] + 1) % len(fire_ball_images)

            # ファイアボールがタイル3枚分の距離を超えたら削除
            if abs(fire_ball["x"] - fire_ball["start_x"]) > TILE_SIZE * 3:
                fire_balls_to_remove.append(fire_ball)

            # ファイアボールがオークに当たったら削除して爆発を表示
            for orc in orcs:
                if abs(fire_ball["x"] - orc["x"]) < TILE_SIZE and abs(fire_ball["y"] - orc["y"]) < TILE_SIZE:
                    fire_balls_to_remove.append(fire_ball)
                    orc["hp"] -= 20  # オークのHPを減らす
                    explosions.append({
                        "x": fire_ball["x"],
                        "y": fire_ball["y"],
                        "index": 0
                    })
                    if orc['hp'] <= 0:
                        orc['state'] = 'death'
                        orc['death_index'] = 0
                        # ゼニーを取得
                        zenny_amount = random.randint(1, 10)
                        zenny += zenny_amount
                        zenny_messages.append({
                            "amount": zenny_amount,
                            "x": orc["x"],
                            "y": orc["y"],
                            "start_time": time.time()
                        })
                        # セーブデータの更新
                        save_data = load_save_data(f'save/save_{selected_save_slot}.json')
                        save_data["zenny"] = zenny
                        save_game(f'save/save_{selected_save_slot}.json', save_data)

        for fire_ball in fire_balls_to_remove:
            if fire_ball in fire_balls:
                fire_balls.remove(fire_ball)

        # 爆発の更新と描画
        for explosion in explosions[:]:
            explosion_image = explosion_images[explosion["index"]]
            screen.blit(explosion_image, (explosion["x"], explosion["y"]))

            if animation_counter % ANIMATION_SPEED == 0:
                explosion["index"] += 1
                if explosion["index"] >= len(explosion_images):
                    explosions.remove(explosion)

        # ゼニー取得メッセージの描画
        for message in zenny_messages[:]:
            if time.time() - message["start_time"] < 2:  # 2秒間表示
                zenny_text = font.render(f"+{message['amount']} ゼニーを取得", True, (255, 255, 0))
                screen.blit(zenny_text, (message["x"], message["y"] - 20))
            else:
                zenny_messages.remove(message)


        if is_dead:
            draw_animated_image(screen, death_images, death_index, character_x, character_y, flip_image)
            if animation_counter % ANIMATION_SPEED == 0:
                death_index += 1
                if death_index >= len(death_images):
                    from main import show_main_menu
                    game_over(show_main_menu)
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
                                    # ゼニーを取得
                                    zenny_amount = random.randint(1, 10)
                                    zenny += zenny_amount
                                    zenny_messages.append({
                                        "amount": zenny_amount,
                                        "x": orc["x"],
                                        "y": orc["y"],
                                        "start_time": time.time()
                                    })
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

        # オークを倒した際の処理
        if closest_orc and closest_orc['hp'] <= 0:
            orcs.remove(closest_orc)
            orc_kill_count += 1
            last_kill_time = pygame.time.get_ticks()
            if orc_kill_count % 2 == 0:
                last_orc_respawn = pygame.time.get_ticks()  # リスポーンタイマーをリセット

        # オークキルカウントのリセット処理
        if current_time - last_kill_time > orc_kill_reset_time:
            orc_kill_count = 0

        # ハートの更新と描画
        update_hearts()

        # プレイヤーの現在位置を表示
        # draw_player_position(screen, font, character_x, character_y)

        animation_counter += 1
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    open_world(screen)