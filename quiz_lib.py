import pygame


# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GRAY240 = (240, 240, 240)
GRAY200 = (200, 200, 200)
YELLOW = (255, 255, 0)
BG_COLOR = WHITE
TEXT_COLOR = BLACK


# Шрифты
def create_fonts():
    font48 = pygame.font.Font(None, 48)
    font40 = pygame.font.Font(None, 40)
    font32 = pygame.font.Font(None, 32)
    font24 = pygame.font.Font(None, 24)

    return {'font48': font48, 'font40': font40, 'font32': font32, 'font24': font24}


# Общие функции
def draw_text(screen, text, position, input_active, font):
    surface = font.render(text, True, GRAY if input_active else BLACK)
    screen.blit(surface, position)


def create_button(button_text, x, y, w, h, color, font):
    bt_text = font.render(button_text, True, color)
    bt_rect = bt_text.get_rect(x=x, y=y, width=w, height=h)
    return {'bt_text': bt_text, 'bt_rect': bt_rect}


def draw_button(screen, button):
    pygame.draw.rect(screen, GRAY, button['bt_rect'])
    screen.blit(button['bt_text'], (button['bt_rect'].x + 20, button['bt_rect'].y + 10))
