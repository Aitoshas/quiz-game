import pygame
import quiz_lib as qlib
import db_quiz

FPS = 30

def check_user(login_data):
    # check_user({'username': input_login_text, 'email': input_email_text})
    username = login_data['username'].lower()
    email = login_data['email'].lower()

    cur_user = db_quiz.sql_get_user(username, email)

    if cur_user == -1:
        cur_user = db_quiz.sql_save_user(username, email)
        cur_user_avatar = None
    else:
        cur_user_avatar = None
        try:
            cur_user_avatar = db_quiz.sql_get_avatar(cur_user)
        except:
            cur_user_avatar = None

    return {'id': cur_user, 'username': username, 'email': email, 'avatar': cur_user_avatar}

def draw_start_page(screen, state):

    fonts = qlib.create_fonts()

    label_title = 'Вход/регистрация'
    label_title_pos = (500, 30)
    label_login = 'Ваше имя:'
    label_login_pos = (465, 75)
    label_email = 'Ваша э-почта:'
    label_email_pos = (435, 105)

    input_login_active = False
    input_email_active = False

    input_login_text = ''
    input_email_text = ''
    empty_input = False

    input_login = pygame.Rect(570, 75, 180, 24)
    input_email = pygame.Rect(570, 105, 180, 24)

    clock = pygame.time.Clock()
    button_start = qlib.create_button('Войти', 560, 150, 110, 40, qlib.TEXT_COLOR, font=fonts['font32'])
    #background_image = pygame.image.load('img/fon1.png')
    background_image = pygame.image.load('img/fon1.png')

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return 'quit'

            if state == 'start':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_start['bt_rect'].collidepoint(event.pos):
                        if (input_login_text != '') and (input_email_text != ''):
                            cur_user = check_user({'username': input_login_text, 'email': input_email_text})
                            return 'profile', cur_user
                        else:
                            empty_input = True

                    # Активация полей ввода по клику
                    if input_login.collidepoint(event.pos):
                        input_login_active = True
                    else:
                        input_login_active = False

                    if input_email.collidepoint(event.pos):
                        input_email_active = True
                    else:
                        input_email_active = False

                # Обработка нажатия кнопок клавиатуры
                elif event.type == pygame.KEYDOWN:

                    if input_login_active:
                        if event.key == pygame.K_BACKSPACE:
                            input_login_text = input_login_text[:-1]
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                            pass
                        else:
                            input_login_text += event.unicode
                        empty_input = False

                    if input_email_active:
                        if event.key == pygame.K_BACKSPACE:
                            input_email_text = input_email_text[:-1]
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                            pass
                        else:
                            input_email_text += event.unicode
                        empty_input = False

        #screen.fill(qlib.BG_COLOR)
        #screen.fill((255, 190, 0))
        screen.blit(background_image, (0, 0))


        qlib.draw_text(screen, label_title, label_title_pos, False, fonts['font32'])
        qlib.draw_text(screen, label_login, label_login_pos, False, fonts['font24'])
        qlib.draw_text(screen, label_email, label_email_pos, False, fonts['font24'])
        pygame.draw.rect(screen, qlib.GRAY200 if input_login_active else qlib.GRAY240, input_login, 130)
        pygame.draw.rect(screen, qlib.GRAY200 if input_email_active else qlib.GRAY240, input_email, 130)
        log_text = fonts['font24'].render(input_login_text, True, qlib.TEXT_COLOR)
        screen.blit(log_text, (input_login.x + 5, input_login.y))
        em_text = fonts['font24'].render(input_email_text, True, qlib.TEXT_COLOR)
        screen.blit(em_text, (input_email.x + 5, input_email.y))
        qlib.draw_button(screen, button_start)
        if empty_input:
            qlib.draw_text(screen, 'Укажите имя и э-почту', (560, 200), True, fonts['font24'])

        qlib.draw_text(screen, 'ВИКТОРИНА', (150, 300), False, fonts['font48'])

        pygame.display.flip()
        clock.tick(FPS)
