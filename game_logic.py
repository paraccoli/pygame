# +----------------------------------------------------+
#  This file was created by Paraccoli.
#  Contact:m.mirim1357@gmail.com
# +----------------------------------------------------+


from enum import Enum
import sqlite3
import pygame
from pygame.locals import *
from config import NUM_SLOTS

class Game:
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background
        self.selected_slot = 0

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.selected_slot = (self.selected_slot - 1) % NUM_SLOTS
            elif event.key == K_RIGHT:
                self.selected_slot = (self.selected_slot + 1) % NUM_SLOTS

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        # スロットの描画処理を追加

class BuildingType(Enum):
    HQ = 1
    BRANCH = 2


class Game:
    def __init__(self):
        self.players = []  # プレイヤーリスト
        self.field = Field()  # フィールド
        self.turn = 1  # ターン番号

    def start_game(self):
        # プレイヤーの人数設定
        num_players = int(input("プレイヤーの人数を入力してください (2-4): "))
        for i in range(num_players):
            player_name = input(f"{i+1}番目のプレイヤーの名前を入力: ")
            self.players.append(Player(player_name))

        # HQの場所設定
        for i, player in enumerate(self.players):
            while True:
                row = int(input(f"{player.name}のHQの行を入力 (0-29): "))
                col = int(input(f"{player.name}のHQの列を入力 (0-29): "))
                if self.field.is_valid_hq_location(row, col):
                    player.hq = Building(row, col, BuildingType.HQ, player)
                    self.field.place_building(player.hq)
                    break
                else:
                    print("無効な場所です。もう一度入力してください。")

        # ゲームループ
        while True:
            self.print_game_state()
            current_player = self.players[(self.turn - 1) % len(self.players)]
            print(f"{current_player.name} のターンです。")

            # プレイヤーの行動
            action = input("行動を選択してください (place_branch, pass): ")
            if action == "place_branch":
                while True:
                    row = int(input("支部の行を入力 (0-29): "))
                    col = int(input("支部の列を入力 (0-29): "))
                    if self.field.is_valid_branch_location(row, col, current_player):
                        new_branch = Building(row, col, BuildingType.BRANCH, current_player)
                        self.field.place_building(new_branch)
                        current_player.branches.append(new_branch)
                        break
                    else:
                        print("無効な場所です。もう一度入力してください。")
            elif action == "pass":
                pass
            else:
                print("無効なコマンドです。")

            # 戦闘処理
            self.resolve_battles()

            # ターン終了処理
            self.turn += 1

    def print_game_state(self):
        # フィールドの表示
        for row in range(30):
            for col in range(30):
                building = self.field.get_building(row, col)
                if building:
                    if building.type == BuildingType.HQ:
                        print("H", end="")
                    elif building.type == BuildingType.BRANCH:
                        print(building.owner.name[0], end="")
                else:
                    print("-", end="")
            print()

        # プレイヤー情報の表示
        for player in self.players:
            print(f"{player.name}: 強さ={player.strength}, 支部数={len(player.branches)}")

    def resolve_battles(self):
        # すべての建物に対して
        for row in range(30):
            for col in range(30):
                building = self.field.get_building(row, col)
                if building and building.type == BuildingType.BRANCH:
                    # 隣接する敵対支部を探す
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        neighbor_row = row + dx
                        neighbor_col = col + dy
                        if 0 <= neighbor_row < 30 and 0 <= neighbor_col < 30:
                            neighbor_building = self.field.get_building(neighbor_row, neighbor_col)
                            if neighbor_building and neighbor_building.type == BuildingType.BRANCH and neighbor_building.owner != building.owner:
                                # 戦闘処理
                                self.fight(building, neighbor_building)

    def fight(self, branch1, branch2):
        # 強さを比較
        strength1 = branch1.strength
        strength2 = branch2.strength

        # 勝敗判定
        if strength1 > strength2:
            winner = branch1
            loser = branch2
        elif strength1 < strength2:
            winner = branch2
            loser = branch1
        else:
            # 引き分け
            return

        # 強さ調整
        winner.strength += int(loser.strength / 2)
        loser.strength = int(loser.strength / 2)

        # 支部乗っ取り
        if loser.strength == 0:
            loser.owner = winner
            loser.strength = int(winner.strength / 2)
            winner.strength -= int(loser.strength / 2)


class Player:
    def __init__(self, name):
        self.name = name
        self.hq = None  # HQ建物
        self.branches = []  # 支部建物のリスト
        self.strength = 100  # 強さ

    def place_branch(self, row, col):
        new_branch = Building(row, col, BuildingType.BRANCH, self)
        self.branches.append(new_branch)
        self.field.place_building(new_branch)

    def receive_strength(self, amount):
        self.strength += amount

    def lose_strength(self, amount):
        self.strength -= amount

class Field:
    def __init__(self):
        self.grid = [[None for _ in range(30)] for _ in range(30)]

    def is_valid_hq_location(self, row, col):
        # HQ配置のルール: 端の行にのみ配置可能
        if row in (0, 29):
            return True
        else:
            return False

    def is_valid_branch_location(self, row, col, player):
        # 支部配置のルール:
        # 1. 空いているマス
        # 2. 自分のHQの隣接マス
        # 3. 敵のHQの隣接マス
        if self.grid[row][col] is None:
            hq_row, hq_col = player.hq.row, player.hq.col
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor_row = row + dx
                neighbor_col = col + dy
                if 0 <= neighbor_row < 30 and 0 <= neighbor_col < 30:
                    neighbor_building = self.grid[neighbor_row][neighbor_col]
                    if neighbor_building:
                        if neighbor_building.type == BuildingType.HQ and neighbor_building.owner == player:
                            return True
                        elif neighbor_building.type == BuildingType.HQ and neighbor_building.owner != player:
                            return True
            return False
        else:
            return False

    def place_building(self, building):
        self.grid[building.row][building.col] = building

    def get_building(self, row, col):
        return self.grid[row][col]

    def get_adjacent_buildings(self, row, col):
        adjacent_buildings = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor_row = row + dx
            neighbor_col = col + dy
            if 0 <= neighbor_row < 30 and 0 <= neighbor_col < 30:
                neighbor_building = self.get_building(neighbor_row, neighbor_col)
                if neighbor_building:
                    adjacent_buildings.append(neighbor_building)
        return adjacent_buildings

    def get_strength_from_adjacent_branches(self, building):
        total_strength = 0
        for adjacent_building in self.get_adjacent_buildings(building.row, building.col):
            if adjacent_building.type == BuildingType.BRANCH and adjacent_building.owner == building.owner:
                total_strength += adjacent_building.strength
        return total_strength

    def update_building_strength(self):
        for row in range(30):
            for col in range(30):
                building = self.get_building(row, col)
                if building and building.type == BuildingType.HQ:
                    # HQの強さは、隣接する支部の強さを毎ターン1ずつ移す
                    adjacent_strength = self.get_strength_from_adjacent_branches(building)
                    building.strength = max(0, building.strength - adjacent_strength)
                elif building and building.type == BuildingType.BRANCH:
                    # 支部の強さは、毎ターン隣接する支部からの強さを1ずつ受け取る
                    adjacent_strength = self.get_strength_from_adjacent_branches(building)
                    building.strength += adjacent_strength

class Building:
    def __init__(self, row, col, building_type, owner):
        self.row = row
        self.col = col
        self.type = building_type  # HQ or BRANCH
        self.owner = owner  # Player instance
        self.strength = 100

    def is_hq(self):
        return self.type == BuildingType.HQ

    def is_branch(self):
        return self.type == BuildingType.BRANCH

    def get_strength(self):
        return self.strength

    def receive_strength(self, amount):
        self.strength += amount

    def lose_strength(self, amount):
        self.strength -= amount

    def change_owner(self, new_owner):
        self.owner = new_owner


def create_database():
    connection = sqlite3.connect('game_data.db')
    cursor = connection.cursor()

    # ゲーム情報のテーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_1_name TEXT,
            player_2_name TEXT,
            field_size INTEGER,
            turn INTEGER,
            winner TEXT
        )
    ''')

    # プレイヤー情報のテーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            name TEXT,
            hq_row INTEGER,
            hq_col INTEGER,
            strength INTEGER,
            FOREIGN KEY (game_id) REFERENCES game_info(id)
        )
    ''')

    # 建物のテーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buildings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            row INTEGER,
            col INTEGER,
            type INTEGER,
            owner_id INTEGER,
            strength INTEGER,
            FOREIGN KEY (game_id) REFERENCES game_info(id),
            FOREIGN KEY (owner_id) REFERENCES players(id)
        )
    ''')

    connection.commit()
    connection.close()

def save_game_info(game):
    connection = sqlite3.connect('game_data.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO game_info (player_1_name, player_2_name, field_size, turn, winner) VALUES (?, ?, ?, ?, ?)',
                   (game.player1.name, game.player2.name, game.field.size, game.turn, game.winner))

    game_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return game_id

def save_player_info(game, player):
    connection = sqlite3.connect('game_data.db')
    cursor = connection.cursor()

    game_id = save_game_info(game)

    cursor.execute('INSERT INTO players (game_id, name, hq_row, hq_col, strength) VALUES (?, ?, ?, ?, ?)',
                   (game_id, player.name, player.hq.row, player.hq.col, player.strength))

    player_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return player_id

def save_building_info(game, building):
    connection = sqlite3.connect('game_data.db')
    cursor = connection.cursor()

    game_id = save_game_info(game)
    player_id = save_player_info(game, building.owner)

    cursor.execute('INSERT INTO buildings (game_id, row, col, type, owner_id, strength) VALUES (?, ?, ?, ?, ?, ?)',
                   (game_id, building.row, building.col, building.type, player_id, building.strength))

    connection.commit()
    connection.close()

def load_game_info(game_id):
    connection = sqlite3.connect('game_data.db')
    cursor = connection.cursor()

    cursor.execute('SELECT player_1_name, player_2_name, field_size, turn, winner FROM game_info WHERE id = ?', (game_id,))
    result = cursor.fetchone()

    if result:
        player1_name, player2_name, field_size, turn, winner = result

        game = Game(player1_name, player2_name, field_size)
        game.turn = turn
        game.winner = winner

        return game
    else:
        return None

def load_player_info(game_id, player_name):
    connection = sqlite3.connect('game_data.db')
    cursor = connection.cursor()

    cursor.execute('SELECT hq_row, hq_col, strength FROM players WHERE game_id = ? AND name = ?', (game_id, player_name))
    result = cursor.fetchone()

    if result:
        hq_row, hq_col, strength = result

        player = Player(player_name)
        player.hq.row = hq_row
        player.hq.col = hq_col
        player.strength = strength

        return player
    else:
        return None

def load_building_info(game_id):
    connection = sqlite3.connect('game_data.db')
    cursor = connection.cursor()

    cursor.execute('SELECT row, col, type, owner_id, strength FROM buildings WHERE game_id = ?', (game_id,))
    results = cursor.fetchall()

    buildings = []
    for row, col, building_type, owner_id, strength in results:
        building = Building(row, col, BuildingType(building_type), None)
        building.strength = strength

        buildings.append(building)

    return buildings

def load_game(game_id):
    game_info = load_game_info(game_id)
    if game_info:
        player1 = load_player_info(game_id, game_info.player1_name)
        player2 = load_player_info(game_id, game_info.player2_name)
        buildings = load_building_info(game_id)

        game = Game(player1, player2, game_info.field_size)
        game.turn = game_info.turn
        game.winner = game_info.winner

        game.field.set_buildings(buildings)

        return game
    else:
        return None
