import pygame
import quiz_lib as qlib
import db_quiz
from datetime import datetime


FPS = 30


def draw_quiz_page(screen, state, quiz_set, user_data):

    cur_question = 0
    next_question = False
    # Установка начального времени таймера (в секундах)
    countdown_time = 30
    # Задание начального времени
    start_ticks = pygame.time.get_ticks()
    #   Находим уник идентификатор игры
    game_id = db_quiz.sql_get_next_game_id()
    cur_date = datetime.now()
    date_id = cur_date.strftime('%d-%m-%Y')

    #
    active1 = active2 = active3 = False
    fonts = qlib.create_fonts()
    clock = pygame.time.Clock()
    button_quiz = qlib.create_button('Следующий вопрос', 230, 500, 280, 40, qlib.TEXT_COLOR, font=fonts['font32'])
    background_image = pygame.image.load('img/fon1.png')

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            if state == 'quiz':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_quiz['bt_rect'].collidepoint(event.pos):
                        next_question = True

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

        # screen.fill(qlib.BG_COLOR)
        screen.blit(background_image, (0, 0))

        # Вычисление оставшегося времени
        seconds = countdown_time - (pygame.time.get_ticks() - start_ticks) // 1000
        if seconds <= 0:
            next_question = True

        # Создание текстовой поверхности для отображения времени
        timer_text = fonts['font24'].render("Оставшееся время: "+str(seconds), True, qlib.TEXT_COLOR)
        # Отображение таймера на экране
        screen.blit(timer_text, (450, 50))

        qlib.draw_text(screen, f"Вопрос {cur_question+1}", (150, 50), False, fonts['font32'])
        qlib.draw_button(screen, button_quiz)
        rect_question = qlib.draw_question(screen, quiz_set[cur_question]['question'], (50, 150), False, fonts['font24'])
        qbottom = rect_question.bottom
        rect_answer1 = qlib.draw_answer(screen, '1. ' + quiz_set[cur_question]['answers'][0], (50, qbottom+50), active1, fonts['font24'])
        rect_answer2 = qlib.draw_answer(screen, '2. ' + quiz_set[cur_question]['answers'][1], (50, qbottom+100), active2, fonts['font24'])
        rect_answer3 = qlib.draw_answer(screen, '3. ' + quiz_set[cur_question]['answers'][2], (50, qbottom+150), active3, fonts['font24'])
        pygame.display.flip()
        clock.tick(FPS)

        if next_question:
            #   Сохранение ответа в БД
            db_quiz.sql_save_game_ansver(
                date_id,
                user_data['id'],
                game_id,
                quiz_set[cur_question]['id_question'],
                1 if quiz_set[cur_question]['user_answer'] == quiz_set[cur_question]['correct'] else 0,
                quiz_set[cur_question]['ball'] if quiz_set[cur_question]['user_answer'] == quiz_set[cur_question][
                    'correct'] else 0
            )
            #
            if cur_question < len(quiz_set) - 1:
                cur_question += 1
                active1 = active2 = active3 = False

                # Задание начального времени
                start_ticks = pygame.time.get_ticks()
                next_question = False

            else:
                return 'quiz_result', quiz_set
