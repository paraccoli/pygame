# +----------------------------------------------------+
#  This file was created by Paraccoli.
#  Contact:m.mirim1357@gmail.com
# +----------------------------------------------------+


class Episode:
    def __init__(self, title, description, episode_number):
        self.title = title
        self.description = description
        self.episode_number = episode_number
        self.current_stage = 0
        self.progress = 0

    def start(self):
        self.current_stage = 1
        self.progress = 0
        print(f"エピソード {self.title} が始まりました。")

    def end(self):
        self.current_stage = -1
        self.progress = 100
        print(f"エピソード {self.title} が終了しました。")

    def next_stage(self):
        if self.current_stage != -1:
            self.current_stage += 1
            self.progress += 10
            print(f"次のステージに進みました。現在のステージ: {self.current_stage}, 進行度: {self.progress}%")
        else:
            print("エピソードは既に終了しています。")