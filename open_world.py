# FILE: open_world.py
import pygame
import math
import time
from config import SCREEN_WIDTH, SCREEN_HEIGHT, screen
from settings import show_menu, key_config
from save_manager import load_save_data, get_selected_save_slot
from episode0_0 import *
from variables import *
from player_data import *



# Pygameの初期化
pygame.init()
pygame.font.init()  # フォントモジュールの初期化トを作成

# 全体マップの画像をロード
full_map_image = pygame.image.load("maps/country_of_lil_vale.png")

# プレイ時間を計測するための変数
start_time = time.time()

def open_world(screen):
    global tiles, map_data, selected_tile, temp_tile, palette_scroll_y, PALETTE_WIDTH, PALETTE_HEIGHT,heart_images,orcs,health,show_city_name_flag, player_name, play_time, player_level, player_position, player_inventory, player_health, selected_save_slot, character_x, character_y
    # 画面を暗転させる
    screen.fill((0, 0, 0))
    pygame.display.flip()
    pygame.time.wait(1000)  # 1秒待つ

    # セーブデータを読み込む
    selected_save_slot = get_selected_save_slot()
    save_data = load_save_data(f'save/save_{selected_save_slot}.json')

    # タイルセットを読み込む
    tiles = load_tileset(tileset_filenames, tile_sizes)

    # フィールドデータを読み込む
    map_data = load_field_data("field_data_0-0.json")

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


    # プレイヤーの初期位置をセーブデータから取得
    if "position" in save_data:
        player_position = save_data["position"]
        character_x = player_position["x"]
        character_y = player_position["y"]
    else:
        character_x = 350
        player_position = {"x": character_x, "y": character_y}  # 初期位置を設定
    


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

        # プレイヤーデータを更新
        update_player_data(player_name, play_time, player_level, player_inventory, player_position, player_health)


        # 画面をクリア
        screen.fill((0, 0, 0))

        # フィールドを再描画
        draw_map(screen, map_data, tiles)

        # ハートの更新と描画
        update_hearts()

        # 都市名を表示
        if show_city_name_flag:
            draw_city_name(screen, "都市名：Suncrossham")

        if health <= 0:
            is_dead = True
            is_walking = False
            is_attacking = False
            is_hurt = False

        if is_dead:
            if flip_image:
                death_image = pygame.transform.flip(death_images[death_index], True, False)
            else:
                death_image = death_images[death_index]

            screen.blit(death_image, (character_x, character_y))
            if animation_counter % ANIMATION_SPEED == 0:
                death_index += 1
                if death_index >= len(death_images):
                    game_over()
        else:
            if is_walking and not is_attacking:  # 攻撃中でない場合のみ移動
                new_x = character_x + move_x_direction * MOVE_SPEED
                new_y = character_y + move_y_direction * MOVE_SPEED
                # マップ外に出ないように制御
                if 0 <= new_x <= SCREEN_WIDTH - CHARACTER_SIZE and 0 <= new_y <= SCREEN_HEIGHT - CHARACTER_SIZE:
                    # キャラクターの矩形を定義
                    character_rect = pygame.Rect(new_x, new_y, CHARACTER_SIZE, CHARACTER_SIZE)
                    # 衝突判定
                    collision = True  # デフォルトで衝突とする
                    for rect in passable_areas:
                        if character_rect.colliderect(rect):
                            collision = False  # 赤い部分に衝突した場合は移動可能
                            break
                    if not collision:
                        character_x = new_x
                        character_y = new_y

                if flip_image:
                    walk_image = pygame.transform.flip(walk_images[walk_index], True, False)
                else:
                    walk_image = walk_images[walk_index]

                screen.blit(walk_image, (character_x, character_y))
                if animation_counter % ANIMATION_SPEED == 0:
                    walk_index = (walk_index + 1) % len(walk_images)
            elif is_attacking:
                if flip_image:
                    attack_image = pygame.transform.flip(current_attack_images[attack_index], True, False)
                else:
                    attack_image = current_attack_images[attack_index]

                screen.blit(attack_image, (character_x, character_y))
                if animation_counter % ANIMATION_SPEED == 0:
                    attack_index += 1
                    if attack_index >= len(current_attack_images):
                        is_attacking = False
                        # プレイヤーの攻撃が当たったかどうかをチェック
                        for orc in orcs:
                            if is_attack_hit(character_x, character_y, orc['x'], orc['y'], attack_direction):
                                orc['hp'] -= 10  # HPを減らす
                                if orc['hp'] <= 0:
                                    orc['state'] = 'death'
                                    orc['death_index'] = 0
                                else:
                                    orc['state'] = 'hurt'
            elif is_hurt:
                if flip_image:
                    hurt_image = pygame.transform.flip(hurt_images[hurt_index], True, False)
                else:
                    hurt_image = hurt_images[hurt_index]

                screen.blit(hurt_image, (character_x, character_y))
                if animation_counter % ANIMATION_SPEED == 0:
                    hurt_index += 1
                    if hurt_index >= len(hurt_images):
                        is_hurt = False
            else:
                if flip_image:
                    idle_image = pygame.transform.flip(idle_images[idle_index], True, False)
                else:
                    idle_image = idle_images[idle_index]

                screen.blit(idle_image, (character_x, character_y))
                if animation_counter % ANIMATION_SPEED == 0:
                    idle_index = (idle_index + 1) % len(idle_images)

        # Orcの動作を更新
        for orc in orcs:
            orc_x, orc_y = orc['x'], orc['y']
            distance_to_player = math.hypot(character_x - orc_x, character_y - orc_y)

            if orc['state'] != 'attack' and orc['state'] != 'hurt' and orc['state'] != 'death':  # 攻撃中およびダメージ中でない場合のみ状態を変更
                if distance_to_player < ORC_ATTACK_RADIUS:
                    orc['state'] = 'attack'
                    orc['attack_index'] = 0  # 攻撃アニメーションの開始
                    orc['attack_direction'] = 'right' if character_x > orc_x else 'left'  # 攻撃方向を設定
                elif distance_to_player < ORC_DETECTION_RADIUS:
                    orc['state'] = 'walk'
                else:
                    orc['state'] = 'idle'

            if orc['state'] == 'walk':
                handle_orc_movement(orc, character_x, character_y, passable_areas)

                if orc['flip_image']:
                    orc_walk_image = pygame.transform.flip(orc_walk_images[orc['walk_index']], True, False)
                else:
                    orc_walk_image = orc_walk_images[orc['walk_index']]
                
                screen.blit(orc_walk_image, (orc['x'], orc['y']))
                if animation_counter % ORC_ANIMATION_SPEED == 0:
                    orc['walk_index'] = (orc['walk_index'] + 1) % len(orc_walk_images)
            elif orc['state'] == 'attack':
                if orc['flip_image']:
                    orc_attack_image = pygame.transform.flip(orc_attack_images[orc['attack_index']], True, False)
                else:
                    orc_attack_image = orc_attack_images[orc['attack_index']]
                
                screen.blit(orc_attack_image, (orc['x'], orc['y']))
                if animation_counter % (ORC_ANIMATION_SPEED * ORC_ATTACK_FREQUENCY) == 0:
                    orc['attack_index'] += 1
                    if orc['attack_index'] >= len(orc_attack_images):
                        orc['state'] = 'idle'  # 攻撃アニメーションが終了したら移動可能にする
                    else:
                        # 攻撃アニメーションの特定のフレームでのみダメージを与える
                        if orc['attack_index'] == 4:  # 攻撃アニメーションの4フレーム目でダメージを与える
                            if is_attack_hit(orc['x'], orc['y'], character_x, character_y, orc['attack_direction']):
                                if not is_hurt and not is_dead:  # プレイヤーが攻撃を受けていない場合のみダメージ処理
                                    is_hurt = True
                                    hurt_index = 0
                                    health -= 10  # HPを10減らす
                                    if health < 0:
                                        health = 0
            elif orc['state'] == 'hurt':
                if orc['flip_image']:
                    orc_hurt_image = pygame.transform.flip(orc_hurt_images[orc['hurt_index']], True, False)
                else:
                    orc_hurt_image = orc_hurt_images[orc['hurt_index']]

                screen.blit(orc_hurt_image, (orc['x'], orc['y']))
                if animation_counter % ORC_ANIMATION_SPEED == 0:
                    orc['hurt_index'] += 1
                    if orc['hurt_index'] >= len(orc_hurt_images):
                        orc['state'] = 'idle'
                        orc['hurt_index'] = 0
            elif orc['state'] == 'death':
                if orc['flip_image']:
                    orc_death_image = pygame.transform.flip(orc_death_images[orc['death_index']], True, False)
                else:
                    orc_death_image = orc_death_images[orc['death_index']]
                
                screen.blit(orc_death_image, (orc['x'], orc['y']))
                if animation_counter % ANIMATION_SPEED == 0:
                    orc['death_index'] += 1
                    if orc['death_index'] >= len(orc_death_images):
                        orcs.remove(orc)  # 死亡アニメーションが終了したらOrcを削除
                        drop_heart(orc['x'], orc['y'])  # ハートをドロップ

            else:
                if orc['flip_image']:
                    orc_idle_image = pygame.transform.flip(orc_idle_images[orc['idle_index']], True, False)
                else:
                    orc_idle_image = orc_idle_images[orc['idle_index']]
                
                screen.blit(orc_idle_image, (orc['x'], orc['y']))
                if animation_counter % ORC_ANIMATION_SPEED == 0:
                    orc['idle_index'] = (orc['idle_index'] + 1) % len(orc_idle_images)

        # プレイヤーから一番近いOrcを取得
        closest_orc = get_closest_orc(character_x, character_y, orcs)

        # 一番近いOrcのHPを表示
        if closest_orc:
            hp_percentage = closest_orc['hp'] / 100
            health_meter_width = health_meter_full.get_width()
            health_meter_height = health_meter_full.get_height()
            current_health_width = int(health_meter_width * hp_percentage)
            
            # 空のHPメーターを描画
            screen.blit(health_meter_empty, (SCREEN_WIDTH - health_meter_width - 100, 10))
            
            # 現在のHPを描画
            screen.blit(health_meter_full, (SCREEN_WIDTH - health_meter_width - 44, 23), (0, 0, current_health_width, health_meter_height))

        # 体力バーを描画
        screen.blit(health_bar_bg, (150, 10))
        current_health_width = int(health_bar_fg.get_width() * (health / 100))
        screen.blit(health_bar_fg, (192, 32), (0, 0, current_health_width, health_bar_fg.get_height()))

        # ミニマップを描画
        pygame.draw.circle(screen, (255, 0, 0), minimap_position, minimap_radius, 2)
        # ミニマップの内容を描画（ここでは仮にキャラクターの位置を示す点を描画）
        pygame.draw.circle(screen, (0, 255, 0), minimap_position, 5)

        animation_counter += 1
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    open_world(screen)