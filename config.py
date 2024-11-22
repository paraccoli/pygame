# +----------------------------------------------------+
#  This file was created by Paraccoli.
#  Contact:m.mirim1357@gmail.com
# +----------------------------------------------------+


import os
import pygame

# 画面サイズ
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

TILE_SIZE = 32
FIELD_WIDTH = 200  # フィールドの幅（タイル数）
FIELD_HEIGHT = 150  # フィールドの高さ（タイル数）

# スロット数
NUM_SLOTS = 3

# スロット枠の大きさ
SLOT_WIDTH = 1000
SLOT_HEIGHT = 300

# スロット間隔
SLOT_MARGIN = 20
SLOT_INFO_MARGIN = 0


# 選択中のスロット番号
selected_slot = 0

# パス
ICON_IMAGE_PATH = os.path.join("assets", "images", "icon.png")
FONT_PATH = os.path.join("font", "Nosutaru-dotMPlusH-10-Regular.ttf")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))