from PIL import Image

def split_image(input_image_path, output_folder, start_index=91):
    # 画像を開く
    image = Image.open(input_image_path)
    image_width, image_height = image.size

    # 32x32の区画に分割
    tile_width = 32
    tile_height = 32

    index = start_index
    for y in range(0, image_height, tile_height):
        for x in range(0, image_width, tile_width):
            # 画像を切り取る
            box = (x, y, x + tile_width, y + tile_height)
            tile = image.crop(box)
            # ファイル名を作成して保存
            output_image_path = f"{output_folder}/weapon-{index}.png"
            tile.save(output_image_path)
            index += 1

if __name__ == "__main__":
    input_image_path = r"C:\\Users\\e2258\\python\\Pygame\\weapons\\Placton\\File 2024.png"  # 入力画像のパス
    output_folder = r"C:\\Users\\e2258\\python\\Pygame\\weapons\\Placton"  # 出力フォルダのパス
    split_image(input_image_path, output_folder)