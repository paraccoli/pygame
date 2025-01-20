import pygame
import json
from config import FONT_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, screen
from dialogue_manager import DialogueManager
from save_manager import load_save_data, save_game

background_image = pygame.image.load("images/shop.png")  # 背景画像のロード
background_image = pygame.transform.scale(background_image, (1920, 1080))  # 背景画像を1920x1080に変換

def dialogue_model(screen, dialogue_manager, background_image):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    dialogue_manager.next_dialogue()

        screen.blit(background_image, (0, 0))  # 背景画像を描画

        # ダイアログボックスの大きさを設定
        dialogue_box_width = SCREEN_WIDTH
        dialogue_box_height = 200
        dialogue_box_x = 0
        dialogue_box_y = SCREEN_HEIGHT - dialogue_box_height

        # ダイアログボックスの背景を描画
        dialogue_box_rect = pygame.Rect(dialogue_box_x, dialogue_box_y, dialogue_box_width, dialogue_box_height)
        dialogue_box_surface = pygame.Surface((dialogue_box_width, dialogue_box_height))
        dialogue_box_surface.set_alpha(100)  # 透過度を設定（0-255）
        dialogue_box_surface.fill((0, 0, 0))  # 黒い四角
        screen.blit(dialogue_box_surface, (dialogue_box_x, dialogue_box_y))
        pygame.draw.rect(screen, (255, 255, 255), dialogue_box_rect, 3)  # 白い枠線

        # セリフの内容を取得
        current_dialogue = dialogue_manager.get_current_dialogue()

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

def dialogue(screen, background_image):
    dialogue_texts = ["こんにちは！", "私は武器屋の店主だよ。", "何かお探しですか？"]
    dialogue_manager = DialogueManager(FONT_PATH, SCREEN_HEIGHT)
    for dialogue in dialogue_texts:
        dialogue_manager.add_dialogue(dialogue)
    dialogue_model(screen, dialogue_manager, background_image)

def load_weapons():
    with open('weapons/Qrepus/weapons.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    weapons = data["weapons"]
    weapon_images = []
    for weapon in weapons:
        image = pygame.image.load(f'weapons/Qrepus/weapon-{weapon["id"]}.png')
        weapon_images.append({"image": image, "name": weapon["name"], "description": weapon["description"], "price": weapon["price"], "sell": weapon["sell"]})
    return weapons, weapon_images

def load_player_data():
    with open('save/selected_save_slot.json', 'r') as file:
        selected_save_slot = json.load(file)["selected_slot"]
    save_data = load_save_data(f'save/save_{selected_save_slot}.json')
    return save_data.get("zenny", 0), save_data.get("inventory", []), selected_save_slot

def save_player_data(selected_save_slot, player_money, inventory):
    save_data = load_save_data(f'save/save_{selected_save_slot}.json')
    save_data["zenny"] = player_money
    save_data["inventory"] = inventory
    save_game(f'save/save_{selected_save_slot}.json', save_data)

def buy_weapon(weapon, player_money, selected_save_slot):
    save_data = load_save_data(f'save/save_{selected_save_slot}.json')
    inventory = save_data.get("inventory", [])
    if player_money >= weapon["price"]:
        player_money -= weapon["price"]
        inventory.append(f"weapon-{weapon['id']}")
        save_data["inventory"] = inventory
        save_data["zenny"] = player_money
        save_game(f'save/save_{selected_save_slot}.json', save_data)
        return player_money
    else:
        print("お金が足りません")
        return player_money

def sell_weapon(weapon_id, player_money, selected_save_slot, weapons):
    save_data = load_save_data(f'save/save_{selected_save_slot}.json')
    inventory = save_data.get("inventory", [])
    weapon_index = int(weapon_id.split('-')[1]) - 1
    weapon = weapons[weapon_index]
    player_money += weapon["sell"]
    inventory.remove(weapon_id)
    save_player_data(selected_save_slot, player_money, inventory)
    return player_money, inventory

def weapon_shop():
    running = True
    selected_option = 0
    selected_weapon = 0
    selected_detail_option = 0  # 初期化
    options = ["武器を買う", "武器を売る"]
    player_money, inventory, selected_save_slot = load_player_data()  # プレイヤーの所持金とインベントリをロード
    insufficient_funds = False  # 所持金不足フラグ
    purchase_message = ""  # 購入メッセージ
    show_purchase_message = False  # 購入メッセージ表示フラグ
    sell_message = ""  # 売却メッセージ
    show_sell_message = False  # 売却メッセージ表示フラグ
    no_items_message = False  # 売るものがないメッセージ表示フラグ

    dialogue(screen, background_image)

    weapons, weapon_images = load_weapons()
    show_weapons = False
    show_weapon_details = False
    show_inventory = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if show_weapon_details:
                        show_weapon_details = False
                    elif show_weapons:
                        show_weapons = False
                    elif show_inventory:
                        show_inventory = False
                    else:
                        running = False  # 武器屋を終了して元の画面に戻る
                elif not show_weapons and not show_inventory:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:
                            show_weapons = True
                        elif selected_option == 1:
                            if len(inventory) == 0:
                                no_items_message = True
                            else:
                                show_inventory = True
                elif show_weapons and not show_weapon_details:
                    if event.key == pygame.K_UP:
                        selected_weapon = (selected_weapon - 6) % len(weapons)
                    elif event.key == pygame.K_DOWN:
                        selected_weapon = (selected_weapon + 6) % len(weapons)
                    elif event.key == pygame.K_LEFT:
                        selected_weapon = (selected_weapon - 1) % len(weapons)
                    elif event.key == pygame.K_RIGHT:
                        selected_weapon = (selected_weapon + 1) % len(weapons)
                    elif event.key == pygame.K_RETURN:
                        show_weapon_details = True
                elif show_weapon_details:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        selected_detail_option = (selected_detail_option + 1) % 2
                    elif event.key == pygame.K_RETURN:
                        if selected_detail_option == 0:
                            if player_money < weapons[selected_weapon]["price"]:
                                insufficient_funds = True
                            else:
                                player_money = buy_weapon(weapons[selected_weapon], player_money, selected_save_slot)
                                purchase_message = f"{weapons[selected_weapon]['name']}を購入しました"
                                show_purchase_message = True
                                show_weapon_details = False
                                # インベントリを再ロード
                                player_money, inventory, selected_save_slot = load_player_data()
                        elif selected_detail_option == 1:
                            show_weapon_details = False
                elif show_inventory:
                    if len(inventory) > 0:
                        if event.key == pygame.K_UP:
                            selected_weapon = (selected_weapon - 6) % len(inventory)
                        elif event.key == pygame.K_DOWN:
                            selected_weapon = (selected_weapon + 6) % len(inventory)
                        elif event.key == pygame.K_LEFT:
                            selected_weapon = (selected_weapon - 1) % len(inventory)
                        elif event.key == pygame.K_RIGHT:
                            selected_weapon = (selected_weapon + 1) % len(inventory)
                        elif event.key == pygame.K_RETURN:
                            sell_message = f"{weapons[int(inventory[selected_weapon].split('-')[1]) - 1]['name']}を売却しました"
                            player_money, inventory = sell_weapon(inventory[selected_weapon], player_money, selected_save_slot, weapons)
                            show_sell_message = True
                            selected_weapon = 0  # インベントリを更新した後、選択された武器のインデックスをリセット
                            # インベントリを再ロード
                            player_money, inventory, selected_save_slot = load_player_data()

        screen.blit(background_image, (0, 0))  # 背景画像を描画

        if not show_weapons and not show_inventory:
            # オプションの描画
            option_font = pygame.font.Font(FONT_PATH, 36)
            for i, option in enumerate(options):
                color = (255, 255, 255) if i == selected_option else (100, 100, 100)
                option_text = option_font.render(option, True, color)
                text_rect = option_text.get_rect(topleft=(50, 150 + i * 50))
                # 半透明の背景を描画
                pygame.draw.rect(screen, (0, 0, 0, 128), text_rect.inflate(20, 10))
                screen.blit(option_text, text_rect.topleft)
        elif show_weapons and not show_weapon_details:
            # 武器一覧の描画
            weapon_font = pygame.font.Font(FONT_PATH, 24)
            for i, weapon in enumerate(weapons):
                row = i // 6
                col = i % 6
                x = 50 + col * 250  # 横の間隔を広げる
                y = 250 + row * 150  # 縦の間隔を広げる
                weapon_image = pygame.transform.scale(weapon_images[i]["image"], (100, 100))  # 画像サイズを大きくする
                # 背景の描画
                if player_money >= weapon["price"]:
                    background_color = (50, 255, 50)  # 緑色
                else:
                    background_color = (255, 50, 50)  # 赤色
                if i == selected_weapon:
                    pygame.draw.rect(screen, (255, 215, 0), (x + 50, y - 10, 120, 140), 0)  # 選択された武器の背景を強調表示
                else:
                    pygame.draw.rect(screen, background_color, (x + 50, y - 10, 120, 140), 0)  # 通常の背景
                pygame.draw.rect(screen, (255, 255, 255), (x + 50, y - 10, 120, 140), 3)  # 枠線
                screen.blit(weapon_image, (x + 60, y + 10))  # 画像を中央に配置
        elif show_weapon_details:
            # 武器詳細の描画
            weapon = weapons[selected_weapon]
            weapon_image = pygame.transform.scale(weapon_images[selected_weapon]["image"], (200, 200))
            # 画像の背景に半透明の矩形を描画
            image_rect = pygame.Rect(50, 150, 200, 200)
            pygame.draw.rect(screen, (0, 0, 0, 128), image_rect)
            screen.blit(weapon_image, (50, 150))
            weapon_font = pygame.font.Font(FONT_PATH, 36)
            weapon_name = weapon_font.render(weapon["name"], True, (255, 255, 255))
            weapon_description = weapon_font.render(weapon["description"], True, (255, 255, 255))
            weapon_price = weapon_font.render(f"価格: {weapon['price']}ゼニー", True, (255, 255, 255))
            # テキストの背景に半透明の矩形を描画
            name_rect = weapon_name.get_rect(topleft=(300, 150))
            description_rect = weapon_description.get_rect(topleft=(300, 200))
            price_rect = weapon_price.get_rect(topleft=(300, 250))
            pygame.draw.rect(screen, (0, 0, 0, 128), name_rect.inflate(20, 10))
            pygame.draw.rect(screen, (0, 0, 0, 128), description_rect.inflate(20, 10))
            pygame.draw.rect(screen, (0, 0, 0, 128), price_rect.inflate(20, 10))
            screen.blit(weapon_name, (300, 150))
            screen.blit(weapon_description, (300, 200))
            screen.blit(weapon_price, (300, 250))
            # 購入オプションの描画
            detail_options = ["購入する", "やめる"]
            for i, option in enumerate(detail_options):
                color = (255, 255, 255) if i == selected_detail_option else (100, 100, 100)
                option_text = weapon_font.render(option, True, color)
                option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, 400 + i * 50))
                # オプションテキストの背景に半透明の矩形を描画
                pygame.draw.rect(screen, (0, 0, 0, 128), option_rect.inflate(20, 10))
                screen.blit(option_text, option_rect.topleft)
        elif show_inventory:
            # インベントリの描画
            weapon_font = pygame.font.Font(FONT_PATH, 24)
            weapon_count = {}
            for weapon_id in inventory:
                if weapon_id in weapon_count:
                    weapon_count[weapon_id] += 1
                else:
                    weapon_count[weapon_id] = 1

            unique_inventory = list(weapon_count.keys())

            for i, weapon_id in enumerate(unique_inventory):
                weapon_index = int(weapon_id.split('-')[1]) - 1
                weapon = weapons[weapon_index]
                row = i // 6
                col = i % 6
                x = 50 + col * 250  # 横の間隔を広げる
                y = 250 + row * 150  # 縦の間隔を広げる
                weapon_image = pygame.transform.scale(weapon_images[weapon_index]["image"], (100, 100))  # 画像サイズを大きくする
                # 背景の描画
                pygame.draw.rect(screen, (0, 0, 0, 128), (x - 10, y - 10, 120, 140))  # 半透明の背景
                pygame.draw.rect(screen, (255, 255, 255), (x - 10, y - 10, 120, 140), 3)  # 枠線
                screen.blit(weapon_image, (x, y + 10))  # 画像を中央に配置
                weapon_text = weapon_font.render(weapon["name"], True, (255, 255, 255))
                screen.blit(weapon_text, (x, y + 150))  # 武器名を枠の下に表示
                if weapon_count[weapon_id] > 1:
                    count_text = weapon_font.render(f"×{weapon_count[weapon_id]}", True, (255, 255, 255))
                    screen.blit(count_text, (x + 130, y + 70))
                if i == selected_weapon:
                    pygame.draw.rect(screen, (255, 255, 0), (x - 5, y - 5, 110, 140), 3)  # 選択された武器を強調表示

        # プレイヤーの所持金を表示
        money_font = pygame.font.Font(FONT_PATH, 36)
        money_text = money_font.render(f"所持金: {player_money}ゼニー", True, (255, 255, 255))
        money_rect = money_text.get_rect(topright=(SCREEN_WIDTH - 50, 50))

        # 所持金の背景に半透明の矩形を描画
        pygame.draw.rect(screen, (0, 0, 0, 128), money_rect.inflate(20, 10))

        screen.blit(money_text, money_rect.topleft)

        # 所持金不足メッセージの表示
        if insufficient_funds:
            insufficient_funds_font = pygame.font.Font(FONT_PATH, 48)
            insufficient_funds_text = insufficient_funds_font.render("購入できません", True, (255, 0, 0))
            screen.blit(insufficient_funds_text, (SCREEN_WIDTH // 2 - insufficient_funds_text.get_width() // 2, SCREEN_HEIGHT // 2 - insufficient_funds_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)  # 2秒間表示
            insufficient_funds = False

        # 購入メッセージの表示
        if show_purchase_message:
            purchase_message_font = pygame.font.Font(FONT_PATH, 48)
            purchase_message_text = purchase_message_font.render(purchase_message, True, (0, 255, 0))
            purchase_message_rect = purchase_message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            # 購入メッセージの背景に半透明の矩形を描画
            pygame.draw.rect(screen, (0, 0, 0, 128), purchase_message_rect.inflate(20, 10))
            screen.blit(purchase_message_text, purchase_message_rect.topleft)
            pygame.display.flip()
            pygame.time.wait(2000)  # 2秒間表示
            show_purchase_message = False

        # 売却メッセージの表示
        if show_sell_message:
            sell_message_font = pygame.font.Font(FONT_PATH, 48)
            sell_message_text = sell_message_font.render(sell_message, True, (0, 255, 0))
            sell_message_rect = sell_message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            # 売却メッセージの背景に半透明の矩形を描画
            pygame.draw.rect(screen, (0, 0, 0, 128), sell_message_rect.inflate(20, 10))
            screen.blit(sell_message_text, sell_message_rect.topleft)
            pygame.display.flip()
            pygame.time.wait(2000)  # 2秒間表示
            show_sell_message = False

        # 売るものがないメッセージの表示
        if no_items_message:
            no_items_font = pygame.font.Font(FONT_PATH, 48)
            no_items_text = no_items_font.render("何もありません", True, (255, 0, 0))
            screen.blit(no_items_text, (SCREEN_WIDTH // 2 - no_items_text.get_width() // 2, SCREEN_HEIGHT // 2 - no_items_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)  # 2秒間表示
            no_items_message = False

        pygame.display.flip()

if __name__ == "__main__":
    weapon_shop()