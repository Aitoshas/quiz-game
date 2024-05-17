import pygame
import quiz_lib as qlib

FPS = 30


def draw_quiz_page(screen, state):

    fonts = qlib.create_fonts()
    clock = pygame.time.Clock()
    button_quiz = qlib.create_button('Завершить Викторину', 230, 500, 370, 50, qlib.TEXT_COLOR, font=fonts['font32'])

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            if state == 'quiz':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_quiz['bt_rect'].collidepoint(event.pos):
                        result = None
                        return 'quiz_result', result

        screen.fill(qlib.BG_COLOR)

        qlib.draw_text(screen, "Викторина", (300, 100), False, fonts['font32'])
        qlib.draw_button(screen, button_quiz)

        pygame.display.flip()
        clock.tick(FPS)
