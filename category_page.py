import pygame
import quiz_lib as qlib

FPS = 30


def draw_category_page(screen, state):

    fonts = qlib.create_fonts()
    clock = pygame.time.Clock()
    button_category = qlib.create_button('Начать Викторину', 200, 500, 370, 50, qlib.TEXT_COLOR, font=fonts['font32'])

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            if state == 'category':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_category['bt_rect'].collidepoint(event.pos):
                        return 'quiz'

        screen.fill(qlib.BG_COLOR)

        qlib.draw_text(screen, "Выбор категории", (250, 100), False, fonts['font32'])
        qlib.draw_button(screen, button_category)

        pygame.display.flip()
        clock.tick(FPS)
