# FILE: variables.py
import pygame
import time

# 定数の定義
TILE_SIZE = 32
CHARACTER_SIZE = 64
ANIMATION_SPEED = 10  # アニメーション速度を制御するための変数（大きくすると遅くなる）
MOVE_SPEED = TILE_SIZE // 16  # 移動速度を制御するための変数（小さくすると遅くなる）
ORC_MOVE_SPEED = MOVE_SPEED // 2  # Orcの移動速度はプレイヤーの半分
ORC_ANIMATION_SPEED = ANIMATION_SPEED  # Orcのアニメーション速度はプレイヤーの半分
ORC_ATTACK_FREQUENCY = 2  # Orcの攻撃頻度はプレイヤーの半分
ORC_DETECTION_RADIUS = 200  # Orcがプレイヤーを検知する距離
ORC_ATTACK_RADIUS = 50  # Orcが攻撃を開始する距離
ATTACK_RANGE = 50  # 攻撃範囲を50ピクセルに設定
hearts = []  # ハートのドロップリスト
clock = pygame.time.Clock()  # クロックオブジェクトを作成

NUM_FIRE_BALL_IMAGES = 4  # ファイアボールの画像の数を定義
NUM_EXPLOSION_IMAGES = 4  # 爆発の画像の数を定義


# 初期体力の設定
health = 100
character_x = 200
character_y = 100

# プレイ時間を計測するための変数
start_time = time.time()

# その他の変数
idle_images = []
walk_images = []
attack_images1 = []
attack_images2 = []
hurt_images = []
death_images = []
orc_idle_images = []
orc_walk_images = []
orc_attack_images = []
orc_hurt_images = []
orc_death_images = []

# 全体マップの画像をロード
full_map_image = pygame.image.load("maps/country_of_lil_vale.png")

# 画像をロードする関数
def load_images(path, count, size):
    return [pygame.transform.scale(pygame.image.load(f'{path}-{i}.png'), size) for i in range(1, count + 1)]


# アイドル状態の画像をロード
idle_images = load_images('characters/Friends/Soldier/Soldier_Idle/Soldier-Idle', 6, (CHARACTER_SIZE, CHARACTER_SIZE))
# 歩行状態の画像をロード
walk_images = load_images('characters/Friends/Soldier/Soldier_Walk/Soldier-Walk', 8, (CHARACTER_SIZE, CHARACTER_SIZE))
# 攻撃状態の画像をロード
attack_images1 = load_images('characters/Friends/Soldier/Soldier_Attack_1/Soldier-Attack', 6, (CHARACTER_SIZE, CHARACTER_SIZE))
attack_images2 = load_images('characters/Friends/Soldier/Soldier_Attack_2/Soldier-Attack', 6, (CHARACTER_SIZE, CHARACTER_SIZE))
# 攻撃を受けた状態の画像をロード
hurt_images = load_images('characters/Friends/Soldier/Soldier_Hurt/Soldier-Hurt', 4, (CHARACTER_SIZE, CHARACTER_SIZE))
# 死亡状態の画像をロード
death_images = load_images('characters/Friends/Soldier/Soldier_Death/Soldier-Death', 4, (CHARACTER_SIZE, CHARACTER_SIZE))
# Orcの画像をロード
orc_idle_images = load_images('characters/Enemy/Orc/Orc_Idle/Orc-Idle', 6, (CHARACTER_SIZE, CHARACTER_SIZE))
orc_walk_images = load_images('characters/Enemy/Orc/Orc_Walk/Orc-Walk', 8, (CHARACTER_SIZE, CHARACTER_SIZE))
orc_attack_images = load_images('characters/Enemy/Orc/Orc_Attack/Orc-Attack', 6, (CHARACTER_SIZE, CHARACTER_SIZE))
orc_hurt_images = load_images('characters/Enemy/Orc/Orc_Hurt/Orc-Hurt', 4, (CHARACTER_SIZE, CHARACTER_SIZE))
orc_death_images = load_images('characters/Enemy/Orc/Orc_Death/Orc-Death', 4, (CHARACTER_SIZE, CHARACTER_SIZE))
# ハートのアニメーションをロード
heart_images = load_images('Texture/Heart/Heart-Pickup', 6, (12, 12))
# 体力バーの画像をロード
health_bar_bg = pygame.image.load("Texture/HealthMeter/health meter-09.png")
health_bar_fg = pygame.image.load("Texture/HealthMeter/health meter-12.png")
health_bar_bg = pygame.transform.scale(health_bar_bg, (333, 65))
health_bar_fg = pygame.transform.scale(health_bar_fg, (269, 21))
# OrcHPメーターの画像をロード
health_meter_full = pygame.image.load('Texture/HealthMeter/health meter-42.png')
health_meter_empty = pygame.image.load('Texture/HealthMeter/health meter-36.png')
health_meter_full = pygame.transform.scale(health_meter_full, (312, 33))
health_meter_empty = pygame.transform.scale(health_meter_empty, (393, 105))

# ファイアボールの画像をロード
fire_ball_images = load_images('magic/fire_ball/fire_ball', 3, (32, 32))
explosion_images = load_images('magic/fire_ball/explosion', 3, (32, 32))

tileset_filenames = [f"Texture/Grand/object{i}.png" for i in range(1, 15)]
tile_sizes = [
    (32, 32), (32, 32), (32, 32), (32, 32), (32, 32), (32, 32),
    (64, 97), (64, 97), (160, 224), (37, 32), (36, 49), (60, 38), (24, 44),(32, 32)
]

# タイルパレットの初期化
selected_tile = None
temp_tile = None
palette_scroll_y = 0
PALETTE_WIDTH = 200
PALETTE_HEIGHT = 400

# 都市名の表示フラグ
show_city_name_flag = False

# ミニマップの設定
minimap_radius = 50
minimap_position = (minimap_radius + 10, minimap_radius + 10)

# Orcの初期位置とHPをランダムに設定
orc_positions = [
(1700, 100),
(1670, 150)
]

orcs = []
for pos in orc_positions:
    orc_x, orc_y = pos
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