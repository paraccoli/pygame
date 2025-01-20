import pygame
import json
import os
from tkinter import filedialog
import tkinter as tk
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class TileInfo:
    image: pygame.Surface
    width: int
    height: int
    filename: str

class MapEditor:
    def __init__(self):
        pygame.init()
        self.WINDOW_WIDTH = 1024
        self.WINDOW_HEIGHT = 768
        self.BASE_TILE_SIZE = 32  # グリッドの基本サイズ
        
        # ウィンドウの作成
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("RPG Map Editor")
        
        # 各パネルのサイズと位置
        self.PALETTE_WIDTH = 200
        self.PALETTE_HEIGHT = 400
        self.MAP_LIST_HEIGHT = 300
        
        # タイルセットの定義
        self.tileset_filenames = [f"Texture/Grand/object{i}.png" for i in range(1, 14)]
        self.tile_sizes = [
            (32, 32), (32, 32), (32, 32), (32, 32), (32, 32), (32, 32),
            (64, 97), (64, 97), (160, 224), (37, 32), (36, 49), (60, 38), (24, 44)
        ]
        
        # マップデータの初期化
        self.map_data = []
        self.current_layer = 0
        self.layers = 3
        
        # マップのサイズを1920×1080に設定
        self.map_width = 1920 // self.BASE_TILE_SIZE  # グリッド単位でのマップサイズ
        self.map_height = 1080 // self.BASE_TILE_SIZE
        
        # 選択中のタイル
        self.selected_tile = 0
        
        # タイル画像の読み込み
        self.tiles: List[TileInfo] = self.load_tiles()
        
        # 初期マップデータの作成とobject1での初期化
        self.initialize_map_data()
        
        # スクロール位置
        self.scroll_x = 0
        self.scroll_y = 0
        
        # パレットスクロール
        self.palette_scroll_y = 0
        
        # カーソル位置
        self.cursor_x = 0
        self.cursor_y = 0
        
        # 仮配置のタイル
        self.temp_tile = None
        
        # 操作履歴
        self.undo_stack = []
        
        # フルスクリーンフラグ
        self.fullscreen = False

    def load_tiles(self) -> List[TileInfo]:
        tiles = []
        for filename, size in zip(self.tileset_filenames, self.tile_sizes):
            try:
                image = pygame.image.load(filename)
                # オリジナルサイズを保持
                tiles.append(TileInfo(
                    image=image,
                    width=size[0],
                    height=size[1],
                    filename=filename
                ))
            except Exception as e:
                print(f"Failed to load {filename}: {e}")
        return tiles

    def initialize_map_data(self):
        # マップデータは [レイヤー][y座標][x座標] = (タイルID, x_offset, y_offset)
        self.map_data = [
            [[None for _ in range(self.map_width)]
             for _ in range(self.map_height)]
            for _ in range(self.layers)
        ]
        
        # 最下層（レイヤー0）にobject1を敷き詰める
        for y in range(self.map_height):
            for x in range(self.map_width):
                # object1は0番目のタイル、x_offsetとy_offsetは0
                self.map_data[0][y][x] = (0, 0, 0)

    def draw_tile_palette(self):
        # タイルパレットの背景
        pygame.draw.rect(self.screen, (200, 200, 200),
                        (0, 0, self.PALETTE_WIDTH, self.PALETTE_HEIGHT))
        
        # タイルの描画
        y_pos = -self.palette_scroll_y
        for i, tile in enumerate(self.tiles):
            # タイルのサムネイルサイズを計算（パレット幅に合わせる）
            scale = min(1.0, (self.PALETTE_WIDTH - 20) / tile.width)
            thumb_width = int(tile.width * scale)
            thumb_height = int(tile.height * scale)
            
            # サムネイルの作成
            thumbnail = pygame.transform.scale(tile.image, (thumb_width, thumb_height))
            
            # タイルの表示位置
            x = (self.PALETTE_WIDTH - thumb_width) // 2
            
            # 表示範囲内のタイルのみ描画
            if 0 <= y_pos <= self.PALETTE_HEIGHT - thumb_height:
                self.screen.blit(thumbnail, (x, y_pos))
                
                # 選択中のタイルを強調表示
                if i == self.selected_tile:
                    pygame.draw.rect(self.screen, (255, 0, 0),
                                   (x, y_pos, thumb_width, thumb_height), 2)
            
            y_pos += thumb_height + 10

    def draw_map_view(self, surface=None):
        if surface is None:
            surface = self.screen
        
        # マップビューの描画領域
        view_rect = pygame.Rect(self.PALETTE_WIDTH, 0,
                              self.WINDOW_WIDTH - self.PALETTE_WIDTH,
                              self.WINDOW_HEIGHT)
        
        # グリッドの描画
        for x in range(self.map_width):
            grid_x = self.PALETTE_WIDTH + x * self.BASE_TILE_SIZE - self.scroll_x
            pygame.draw.line(surface, (50, 50, 50),
                           (grid_x, 0), (grid_x, self.WINDOW_HEIGHT))
        
        for y in range(self.map_height):
            grid_y = y * self.BASE_TILE_SIZE - self.scroll_y
            pygame.draw.line(surface, (50, 50, 50),
                           (self.PALETTE_WIDTH, grid_y),
                           (self.WINDOW_WIDTH, grid_y))
        
        # マップの描画（レイヤー順）
        for layer in range(self.layers):
            for y in range(self.map_height):
                for x in range(self.map_width):
                    tile_data = self.map_data[layer][y][x]
                    if tile_data is not None:
                        tile_id, x_offset, y_offset = tile_data
                        tile = self.tiles[tile_id]
                        screen_x = (self.PALETTE_WIDTH + 
                                  x * self.BASE_TILE_SIZE + 
                                  x_offset - 
                                  self.scroll_x)
                        screen_y = y * self.BASE_TILE_SIZE + y_offset - self.scroll_y
                        
                        if view_rect.colliderect(pygame.Rect(
                            screen_x, screen_y, tile.width, tile.height)):
                            surface.blit(tile.image, (screen_x, screen_y))
        
        # 仮配置のタイルを描画
        if self.temp_tile is not None:
            tile_id, x, y = self.temp_tile
            tile = self.tiles[tile_id]
            surface.blit(tile.image, (x, y))
        
        # カーソル位置の強調表示
        cursor_screen_x = self.PALETTE_WIDTH + self.cursor_x * self.BASE_TILE_SIZE - self.scroll_x
        cursor_screen_y = self.cursor_y * self.BASE_TILE_SIZE - self.scroll_y
        pygame.draw.rect(surface, (255, 0, 0), 
                         (cursor_screen_x, cursor_screen_y, self.BASE_TILE_SIZE, self.BASE_TILE_SIZE), 2)

    def get_grid_position(self, mouse_pos):
        """マウス座標からグリッド位置を計算"""
        map_x = (mouse_pos[0] - self.PALETTE_WIDTH + self.scroll_x) // self.BASE_TILE_SIZE
        map_y = (mouse_pos[1] + self.scroll_y) // self.BASE_TILE_SIZE
        return map_x, map_y

    def handle_tile_placement(self, mouse_pos, is_left_click):
        """タイルの配置/削除を処理"""
        if mouse_pos[0] <= self.PALETTE_WIDTH:
            return  # パレット領域では何もしない

        map_x, map_y = self.get_grid_position(mouse_pos)
        
        if not (0 <= map_x < self.map_width and 0 <= map_y < self.map_height):
            return  # マップ範囲外
        
        if self.current_layer == 0:
            return  # レイヤー0（地面）は編集不可
            
        if is_left_click:
            # 左クリック: タイル配置
            selected_tile_info = self.tiles[self.selected_tile]
            if selected_tile_info.width == 32 and selected_tile_info.height == 32:
                # 32×32のタイルはグリッドに合わせて配置
                x_offset = 0
                y_offset = 0
            else:
                # それ以外のサイズのタイルは自由に配置
                x_offset = (mouse_pos[0] - self.PALETTE_WIDTH + self.scroll_x) % self.BASE_TILE_SIZE
                y_offset = (mouse_pos[1] + self.scroll_y) % self.BASE_TILE_SIZE
            
            # 操作履歴に追加
            self.undo_stack.append((self.current_layer, map_x, map_y, self.map_data[self.current_layer][map_y][map_x]))
            
            self.map_data[self.current_layer][map_y][map_x] = (
                self.selected_tile, x_offset, y_offset)
        else:
            # 右クリック: タイル削除
            # 操作履歴に追加
            self.undo_stack.append((self.current_layer, map_x, map_y, self.map_data[self.current_layer][map_y][map_x]))
            
            self.map_data[self.current_layer][map_y][map_x] = None

    def handle_input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        
        # タイルパレットでの選択
        if mouse_pos[0] < self.PALETTE_WIDTH and mouse_pos[1] < self.PALETTE_HEIGHT:
            y_pos = -self.palette_scroll_y
            for i, tile in enumerate(self.tiles):
                scale = min(1.0, (self.PALETTE_WIDTH - 20) / tile.width)
                thumb_height = int(tile.height * scale)
                
                if (y_pos <= mouse_pos[1] + self.palette_scroll_y < 
                    y_pos + thumb_height):
                    if mouse_buttons[0]:  # 左クリック
                        self.selected_tile = i
                        break
                y_pos += thumb_height + 10
        else:
            # タイル配置/削除
            if mouse_buttons[0]:  # 左クリック
                if self.temp_tile is None:
                    # 仮配置のタイルを設定
                    self.temp_tile = (self.selected_tile, mouse_pos[0], mouse_pos[1])
                else:
                    # 仮配置のタイルを移動
                    self.temp_tile = (self.selected_tile, mouse_pos[0], mouse_pos[1])
            elif mouse_buttons[2]:  # 右クリック
                self.handle_tile_placement(mouse_pos, False)
            else:
                if self.temp_tile is not None:
                    # 左クリックを離したときにタイルを確定して配置
                    self.handle_tile_placement((self.temp_tile[1], self.temp_tile[2]), True)
                    self.temp_tile = None

    def undo(self):
        """最後の操作を元に戻す"""
        if self.undo_stack:
            layer, x, y, previous_tile = self.undo_stack.pop()
            self.map_data[layer][y][x] = previous_tile

    def save_map(self):
        """マップデータを保存"""
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(self.map_data, f)
            print(f"Map saved to {file_path}")

    def load_map(self):
        """マップデータを読み込み"""
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                self.map_data = json.load(f)
            print(f"Map loaded from {file_path}")

    def toggle_fullscreen(self):
        """フルスクリーンモードの切り替え"""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

    def show_map_in_new_window(self):
        """新しいウィンドウにマップを表示"""
        new_window = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    running = False
            
            new_window.fill((0, 0, 0))
            self.draw_map_view(new_window)
            pygame.display.flip()
        
        pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("RPG Map Editor")

    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL:
                        self.save_map()
                    elif event.key == pygame.K_o and event.mod & pygame.KMOD_CTRL:
                        self.load_map()
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        self.current_layer = event.key - pygame.K_1
                    elif event.key == pygame.K_RETURN:
                        # エンターキーでタイルを配置
                        self.handle_tile_placement(
                            (self.PALETTE_WIDTH + self.cursor_x * self.BASE_TILE_SIZE, 
                             self.cursor_y * self.BASE_TILE_SIZE), True)
                    elif event.key == pygame.K_z and event.mod & pygame.KMOD_CTRL:
                        # CTRL+Zで元に戻す
                        self.undo()
                    elif event.key == pygame.K_m:
                        # Mキーで新しいウィンドウにマップを表示
                        self.show_map_in_new_window()
                elif event.type == pygame.MOUSEWHEEL:
                    if pygame.mouse.get_pos()[0] < self.PALETTE_WIDTH:
                        self.palette_scroll_y = max(0, self.palette_scroll_y - event.y * 30)
            
            # キー入力によるスクロールとカーソル移動
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.scroll_x = max(0, self.scroll_x - 5)
            if keys[pygame.K_RIGHT]:
                self.scroll_x += 5
            if keys[pygame.K_UP]:
                self.scroll_y = max(0, self.scroll_y - 5)
            if keys[pygame.K_DOWN]:
                self.scroll_y += 5
            if keys[pygame.K_a]:
                self.cursor_x = max(0, self.cursor_x - 1)
            if keys[pygame.K_d]:
                self.cursor_x = min(self.map_width - 1, self.cursor_x + 1)
            if keys[pygame.K_w]:
                self.cursor_y = max(0, self.cursor_y - 1)
            if keys[pygame.K_s]:
                self.cursor_y = min(self.map_height - 1, self.cursor_y + 1)
            
            # 入力の処理
            self.handle_input()
            
            # 画面の描画
            self.screen.fill((100, 100, 100))
            self.draw_tile_palette()
            self.draw_map_view()
            
            # 現在のレイヤー表示
            font = pygame.font.Font(None, 36)
            layer_text = f"Layer: {self.current_layer + 1}"
            text_surface = font.render(layer_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, self.WINDOW_HEIGHT - 30))
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    editor = MapEditor()
    editor.run()