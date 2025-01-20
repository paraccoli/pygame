# +----------------------------------------------------+
#  This file was created by Paraccoli.
#  Contact:m.mirim1357@gmail.com
# +----------------------------------------------------+


import pygame
from config import FONT_PATH, SCREEN_WIDTH, SCREEN_HEIGHT


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

def dialogue(screen, text):
    dialogue_manager = DialogueManager(FONT_PATH, SCREEN_HEIGHT, font_size=24)
    dialogue_manager.add_dialogue(text)

    dialogue_box_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)
    dialogue_box = pygame.Surface((SCREEN_WIDTH, 100))
    dialogue_box.fill((0, 0, 0))
    dialogue_box.set_alpha(200)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            dialogue_manager.handle_event(event)

        screen.blit(dialogue_box, dialogue_box_rect.topleft)
        dialogue_manager.draw(screen, dialogue_box_rect)
        pygame.display.flip()

        if dialogue_manager.is_finished():
            running = False

    pygame.time.wait(2000)  # 2秒間表示