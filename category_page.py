import pygame
import quiz_lib as qlib
import random
import db_quiz

FPS = 30

def create_quiz_set(quiz_category):
    quiz_set  = []
    #   Заполнение вопросов
    for t_one in quiz_category:
        if t_one['active']:
            quiz_set_t_one = db_quiz.sql_get_quiz(t_one['category'])
            for quiz_one in quiz_set_t_one:
                quiz_set_one = {
                    'question': quiz_one[1],
                    'id_question': quiz_one[0],
                    'answers': [quiz_one[2], quiz_one[3], quiz_one[4]],
                    'correct': -1,
                    'ball': quiz_one[7],
                    'user_answer': 99
                }
                random.shuffle(quiz_set_one['answers'])     #   Перетасовать ответы
                i_ans = 0
                for ans_one in quiz_set_one['answers']:
                    if ans_one == quiz_one[2]:
                        quiz_set_one['correct'] = i_ans
                        break
                    i_ans += 1

                quiz_set.append(quiz_set_one)
                ##id, quest, ans1, ans2, ans3, theme_name, category_name, points
                '''
    quiz_set = [
        {'question': 'Какая планета является красной?',
         'id_question': 23,
         'answers': ['Меркурий', 'Венера', 'Марс'],
         'correct': 2,
         'ball': 10,
         'user_answer': 99},
        {'question': 'Какая планета является самой маленькой?',
         'id_question': 17,
         'answers': ['Меркурий', 'Венера', 'Марс'],
         'correct': 0,
         'ball': 20,
         'user_answer': 99},
    ]
    '''
    random.shuffle(quiz_set)
    quiz_set = quiz_set[:10]            # Оставляем первые 10 элементов [:10]
    return quiz_set

def create_quiz_category():
    quiz_category = []
    # Загрузка списка категорий
    themes = db_quiz.sql_get_all_theme()

    for t_one in themes:
        quiz_cat_one = {'id': t_one[0], 'category': t_one[1], 'active': False}
        quiz_category.append(quiz_cat_one)
        '''
     quiz_category = [{'id': 0, 'category': 'Наука', 'active': False},
                    {'id': 1, 'category': 'История', 'active': False},
                    {'id': 2, 'category': 'Культура', 'active': False},
                    {'id': 3, 'category': 'Спорт', 'active': False}]
                    '''

    return quiz_category

def draw_category_page(screen, state):

    fonts = qlib.create_fonts()
    clock = pygame.time.Clock()
    quiz_category = create_quiz_category()
    button_category = qlib.create_button('Начать Викторину', 200, 500, 370, 50, qlib.TEXT_COLOR, font=fonts['font32'])

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            if state == 'category':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_category['bt_rect'].collidepoint(event.pos):
                        quiz_set = create_quiz_set(quiz_category)
                        return 'quiz', quiz_set

                    for ind, rect in enumerate(rect_category):
                        if rect.collidepoint(event.pos):
                            quiz_category[ind]['active'] = not quiz_category[ind]['active']

        screen.fill(qlib.BG_COLOR)

        qlib.draw_text(screen, "Выбор категории", (250, 50), False, fonts['font32'])
        rect_category = []
        for ind, qcat in enumerate(quiz_category):
            rect = qlib.draw_answer(screen, qcat['category'], (150, 200 + 50 * ind), qcat['active'], fonts['font32'])
            rect_category.append(rect)

        qlib.draw_button(screen, button_category)

        pygame.display.flip()
        clock.tick(FPS)
