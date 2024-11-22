# FILE: player_data.py
def update_player_data(name, time, level, inventory, position, health):
    global player_name, play_time, player_level, player_inventory, player_position, player_health
    player_name = name
    play_time = time
    player_level = level
    player_inventory = inventory
    player_position = position
    player_health = health

# プレイヤーの情報を初期化
player_name = "Player"
play_time = "00:00:00"
player_level = 1
player_inventory = []
player_position = {"x": 350, "y": 100}
player_health = 100