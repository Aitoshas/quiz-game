import pygame
import quiz_lib as qlib

FPS = 30


def draw_quiz_page(screen, state, quiz_set):

    cur_question = 0
    active1 = active2 = active3 =  False
    fonts = qlib.create_fonts()
    clock = pygame.time.Clock()
    button_quiz = qlib.create_button('Следующий вопрос', 230, 500, 370, 50, qlib.TEXT_COLOR, font=fonts['font32'])

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            if state == 'quiz':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_quiz['bt_rect'].collidepoint(event.pos):
                        if cur_question < len(quiz_set) - 1:
                            cur_question += 1
                            active1 = active2 = active3 = False
                        else:
                             return 'quiz_result', quiz_set

                    if rect_answer1.collidepoint(event.pos):
                        quiz_set[cur_question]['user_answer'] = 0
                        active1 = True
                        active2 = active3 = False
                    if rect_answer2.collidepoint(event.pos):
                        quiz_set[cur_question]['user_answer'] = 1
                        active2 = True
                        active1 = active3 = False
                    if rect_answer3.collidepoint(event.pos):
                        quiz_set[cur_question]['user_answer'] = 2
                        active3 = True
                        active1 = active2 = False

        screen.fill(qlib.BG_COLOR)

        qlib.draw_text(screen, "Викторина", (300, 50), False, fonts['font32'])
        qlib.draw_button(screen, button_quiz)
        qlib.draw_question(screen, quiz_set[cur_question]['question'], (50, 150), False, fonts['font24'])
        rect_answer1 = qlib.draw_answer(screen, '1. ' + quiz_set[cur_question]['answers'][0], (50, 220), active1, fonts['font24'])
        rect_answer2 = qlib.draw_answer(screen, '2. ' + quiz_set[cur_question]['answers'][1], (50, 270), active2, fonts['font24'])
        rect_answer3 = qlib.draw_answer(screen, '3. ' + quiz_set[cur_question]['answers'][2], (50, 320), active3, fonts['font24'])
        pygame.display.flip()
        clock.tick(FPS)
