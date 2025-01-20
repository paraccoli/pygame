import pygame
import json
from config import FONT_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, screen
from save_manager import load_save_data, save_game

def load_player_data():
    with open('save/selected_save_slot.json', 'r') as file:
        selected_save_slot = json.load(file)["selected_slot"]
    save_data = load_save_data(f'save/save_{selected_save_slot}.json')
    return save_data.get("inventory", []), selected_save_slot

def save_player_data(selected_save_slot, inventory):
    save_data = load_save_data(f'save/save_{selected_save_slot}.json')
    save_data["inventory"] = inventory
    save_game(f'save/save_{selected_save_slot}.json', save_data)

def load_weapons():
    with open('weapons/Qrepus/weapons.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    weapons = data["weapons"]
    weapon_images = []
    for weapon in weapons:
        image = pygame.image.load(f'weapons/Qrepus/weapon-{weapon["id"]}.png')
        weapon_images.append({"image": image, "name": weapon["name"], "description": weapon["description"], "price": weapon["price"], "sell": weapon["sell"]})
    return weapons, weapon_images

def inventory_screen(screen):
    pygame.font.init()  # フォントモジュールを初期化
    running = True
    selected_item = 0
    selected_option = 0
    show_options = False
    confirm_discard = False
    inventory, selected_save_slot = load_player_data()
    weapons, weapon_images = load_weapons()
    font = pygame.font.Font(FONT_PATH, 24)
    large_font = pygame.font.Font(FONT_PATH, 36)  # 大きなフォントを追加

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if confirm_discard:
                        confirm_discard = False
                        selected_option = 0  # リセット
                    elif show_options:
                        show_options = False
                    else:
                        running = False
                elif event.key == pygame.K_UP:
                    if confirm_discard:
                        selected_option = (selected_option - 1) % 2
                    elif show_options:
                        selected_option = (selected_option - 1) % 2
                    else:
                        selected_item = (selected_item - 5) % len(inventory) if inventory else 0
                elif event.key == pygame.K_DOWN:
                    if confirm_discard:
                        selected_option = (selected_option + 1) % 2
                    elif show_options:
                        selected_option = (selected_option + 1) % 2
                    else:
                        selected_item = (selected_item + 5) % len(inventory) if inventory else 0
                elif event.key == pygame.K_LEFT:
                    if not show_options and not confirm_discard:
                        selected_item = (selected_item - 1) % len(inventory) if inventory else 0
                elif event.key == pygame.K_RIGHT:
                    if not show_options and not confirm_discard:
                        selected_item = (selected_item + 1) % len(inventory) if inventory else 0
                elif event.key == pygame.K_RETURN:
                    if confirm_discard:
                        if selected_option == 0:
                            # アイテムを廃棄
                            if inventory:
                                del inventory[selected_item]
                                save_player_data(selected_save_slot, inventory)
                                selected_item = 0  # インベントリを更新した後、選択されたアイテムのインデックスをリセット
                        confirm_discard = False
                        selected_option = 0  # リセット
                    elif show_options:
                        if selected_option == 0:
                            # 武器を使う処理（ここに実装）
                            pass
                        elif selected_option == 1:
                            # アイテムを廃棄確認
                            confirm_discard = True
                        show_options = False
                    else:
                        show_options = True

        # インベントリの描画
        weapon_count = {}
        for weapon_id in inventory:
            if weapon_id in weapon_count:
                weapon_count[weapon_id] += 1
            else:
                weapon_count[weapon_id] = 1

        unique_inventory = list(weapon_count.keys())

        if not unique_inventory:
            # インベントリが空の場合の表示
            empty_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25, 300, 50)
            pygame.draw.rect(screen, (0, 0, 0, 128), empty_rect)  # 半透明の背景
            empty_text = large_font.render("何もありません", True, (255, 255, 255))
            screen.blit(empty_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 15))
        else:
            for i, weapon_id in enumerate(unique_inventory):
                weapon_index = int(weapon_id.split('-')[1]) - 1
                weapon = weapons[weapon_index]
                row = i // 5
                col = i % 5
                x = 50 + col * 150  # 横の間隔を広げる
                y = 50 + row * 150  # 縦の間隔を広げる
                weapon_image = pygame.transform.scale(weapon_images[weapon_index]["image"], (140, 140))  # 画像サイズを大きくする

                # 背景の描画
                pygame.draw.rect(screen, (139, 69, 19), (x - 10, y - 10, 150, 150))  # 背景
                pygame.draw.rect(screen, (255, 255, 255), (x - 10, y - 10, 150, 150), 3)  # 枠線

                screen.blit(weapon_image, (x, y))  # 画像を中央に配置

                if weapon_count[weapon_id] > 1:
                    count_text = font.render(f"×{weapon_count[weapon_id]}", True, (255, 255, 255))
                    screen.blit(count_text, (x + 100, y + 100))

                if i == selected_item:
                    pygame.draw.rect(screen, (255, 255, 0), (x - 5, y - 5, 140, 140), 3)  # 選択された武器を強調表示

        # 選択肢の描画
        if show_options:
            options_rect = pygame.Rect(SCREEN_WIDTH // 2 + 40, 490, 300, 120)
            pygame.draw.rect(screen, (0, 0, 0, 128), options_rect)  # 半透明の背景
            options = ["武器を使う", "武器を捨てる"]
            for i, option in enumerate(options):
                color = (255, 255, 255) if i == selected_option else (100, 100, 100)
                option_text = large_font.render(option, True, color)
                screen.blit(option_text, (SCREEN_WIDTH // 2 + 50, 500 + i * 50))

        # 廃棄確認の描画
        if confirm_discard:
            confirm_rect = pygame.Rect(SCREEN_WIDTH // 2 + 40, 490, 300, 150)
            pygame.draw.rect(screen, (0, 0, 0, 128), confirm_rect)  # 半透明の背景
            confirm_options = ["はい", "いいえ"]
            confirm_text = large_font.render("本当に捨てますか？", True, (255, 255, 255))
            screen.blit(confirm_text, (SCREEN_WIDTH // 2 + 50, 500))
            for i, option in enumerate(confirm_options):
                color = (255, 255, 255) if i == selected_option else (100, 100, 100)
                option_text = large_font.render(option, True, color)
                screen.blit(option_text, (SCREEN_WIDTH // 2 + 50, 550 + i * 50))

        pygame.display.flip()

if __name__ == "__main__":
    inventory_screen()