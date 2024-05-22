import pygame


# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GRAY240 = (240, 240, 240)
GRAY200 = (200, 200, 200)
YELLOW = (255, 255, 0)
PINK = (255, 200, 200)
YELLOW200 = (200, 200, 0)
BG_COLOR = WHITE
TEXT_COLOR = BLACK
ORANGE = (255, 165, 0)
BUTTON_COLOR = (200, 130, 200)

# Шрифты
def create_fonts():
    font48 = pygame.font.SysFont("Segoe script", 72)
    font40 = pygame.font.SysFont("Liberation Sans", 40)
    font32 = pygame.font.SysFont("Liberation Sans", 26)
    font24 = pygame.font.SysFont("Liberation Sans", 20)
    # font24 = pygame.font.Font(None, 24)

    return {'font48': font48, 'font40': font40, 'font32': font32, 'font24': font24}


# Общие функции
def draw_text(screen, text, position, input_active, font):
    #surface = font.render(text, True, GRAY if input_active else BLACK)
    surface = font.render(text, True, GRAY if input_active else (150, 75, 0))
    screen.blit(surface, position)


def create_button(button_text, x, y, w, h, color, font):
    bt_text = font.render(button_text, True, color)
    bt_rect = bt_text.get_rect(x=x, y=y, width=w, height=h)
    return {'bt_text': bt_text, 'bt_rect': bt_rect}


def draw_button(screen, button):
    pygame.draw.rect(screen, BUTTON_COLOR, button['bt_rect'])
    screen.blit(button['bt_text'], (button['bt_rect'].x + 20, button['bt_rect'].y + 5))


def wrap_text(text, font, max_width):
    """Разбивает текст на строки, которые помещаются в заданную ширину."""
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        # Добавляем слово в текущую строку и проверяем ее ширину
        current_line.append(word)
        width, _ = font.size(' '.join(current_line))
        if width > max_width:
            # Если ширина превышает максимум, удаляем последнее слово и добавляем текущую строку в список
            current_line.pop()
            lines.append(' '.join(current_line))
            # Начинаем новую строку с текущего слова
            current_line = [word]

    # Добавляем последнюю строку
    lines.append(' '.join(current_line))
    return lines


# Функция для рисования прямоугольника с закругленными углами
def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_question(screen, text, position, input_active, font):
    # Максимальная ширина текста
    max_text_width = screen.get_width() - 80  # 40 - это отступы от краев экрана

    # Разбиваем текст на строки
    lines = wrap_text(text, font, max_text_width)

    # Размеры и координаты прямоугольника
    padding = 10
    total_height = sum(font.size(line)[1] for line in lines) + padding * (len(lines) + 1)
    max_line_width = max(font.size(line)[0] for line in lines)
    rect_width = max_line_width + padding * 2
    rect_height = total_height
    rect_position = (position[0] - padding, position[1] - padding)
    rect = pygame.Rect(rect_position, (rect_width, rect_height))

    # Рисование прямоугольника с закругленными углами
    draw_rounded_rect(screen, GRAY200, rect, 10)

    # Рисование каждой строки текста поверх прямоугольника
    y_offset = position[1]
    for line in lines:
        text_surface = font.render(line, True, GRAY if input_active else BLACK)
        screen.blit(text_surface, (position[0], y_offset))
        y_offset += font.size(line)[1] + padding

    return rect


def draw_answer(screen, text, position, input_active, font):
    # Рендер текста
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(topleft=position)

    # Размеры и координаты прямоугольника
    padding = 10
    rect_width = text_rect.width + padding * 2
    rect_height = text_rect.height + padding * 2
    rect_position = (position[0] - padding, position[1] - padding)
    rect = pygame.Rect(rect_position, (rect_width, rect_height))

    # Рисование прямоугольника с закругленными углами
    draw_rounded_rect(screen,  YELLOW200 if input_active else PINK, rect, 10)

    # Рисование текста поверх прямоугольника
    screen.blit(text_surface, position)

    return rect


def draw_grid(screen, position, grid_width, grid_height):

    OFFSET_Y = 30
    CELL_SIZE = 30
    #for x in range(OFFSET_X, grid_width - OFFSET_X+1, CELL_SIZE):
    #    pygame.draw.line(screen, BLACK, (position[0], OFFSET_Y), (position[0], grid_height-OFFSET_Y))
    pygame.draw.line(screen, BLACK, (position[0], position[1]), (position[0], position[1]+grid_height-OFFSET_Y))
    pygame.draw.line(screen, BLACK, (position[0]+140, position[1]), (position[0]+140, position[1] + grid_height-OFFSET_Y))
    pygame.draw.line(screen, BLACK, (position[0]+300, position[1]), (position[0]+300, position[1] + grid_height-OFFSET_Y))
    pygame.draw.line(screen, BLACK, (position[0]+grid_width, position[1]), (position[0]+grid_width, position[1]+grid_height-OFFSET_Y))
    for y in range(position[1], grid_height+position[1], CELL_SIZE):
        pygame.draw.line(screen, BLACK, (position[0], y), (position[0]+grid_width, y))
