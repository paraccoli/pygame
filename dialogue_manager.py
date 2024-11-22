# +----------------------------------------------------+
#  This file was created by Paraccoli.
#  Contact:m.mirim1357@gmail.com
# +----------------------------------------------------+


import pygame

class DialogueManager:
    def __init__(self, font_path, screen_height, font_size=48):  # フォントサイズを大きくする
        pygame.font.init()
        self.font = pygame.font.Font(font_path, font_size)
        self.screen_height = screen_height
        self.dialogues = []
        self.current_index = 0

    def add_dialogue(self, dialogue):
        self.dialogues.append(dialogue)

    def next_dialogue(self):
        if self.current_index < len(self.dialogues) - 1:
            self.current_index += 1

    def draw(self, screen, dialogue_box_rect):
        if self.dialogues:
            dialogue_surface = self.font.render(self.dialogues[self.current_index], True, (255, 255, 255))
            dialogue_rect = dialogue_surface.get_rect(center=dialogue_box_rect.center)
            screen.blit(dialogue_surface, dialogue_rect.topleft)  # セリフボックスの中央にセリフを描画

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.next_dialogue()

    def is_finished(self):
        return self.current_index >= len(self.dialogues) - 1

    def get_current_dialogue(self):
        if self.current_index < len(self.dialogues):
            return self.dialogues[self.current_index]
        return ""

    def skip_to_end(self):
        self.current_dialogue_index = len(self.dialogues) - 1