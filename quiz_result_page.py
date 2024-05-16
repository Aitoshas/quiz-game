import pygame
import quiz_lib as qlib

FPS = 30


def draw_quiz_result_page(screen, state, result=None):

    fonts = qlib.create_fonts()
    clock = pygame.time.Clock()
    button_result = qlib.create_button('Начать новую Викторину/Закончить', 120, 500, 470, 50, qlib.TEXT_COLOR, font=fonts['font32'])

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            elif state == 'quiz_result':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_result['bt_rect'].collidepoint(event.pos):
                        return 'category'

        screen.fill(qlib.BG_COLOR)

        qlib.draw_text(screen, "Ваш результат", (200, 100), False, fonts['font32'])
        qlib.draw_button(screen, button_result)

        pygame.display.flip()
        clock.tick(FPS)
