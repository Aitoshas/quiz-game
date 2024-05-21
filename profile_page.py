import pygame
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import quiz_lib as qlib
import db_quiz

FPS = 30

#users = []
init_profile = False
current_user = False

# Данные пользователя
#user_data = {
#    'id': 0,
#    'username': 'zerocoder',
#    'email': 'zero@code.ru',
#    'avatar': pygame.image.load("img/avatar.png")
#}

#users.append(user_data)


#def check_user(login_data):
#    username = login_data['username'].lower()
#    email = login_data['email'].lower()

#    cur_user = False
#    for user in users:
#        if user['username'] == username and user['email'] == email:
#            cur_user = user
#            break

#    if not cur_user:
#        cur_user = {'username': username, 'email': email, 'avatar': '', 'id': len(users)}
#        users.append(cur_user)

#    return cur_user


# Функция для загрузки файла
def load_file(cur_user):
    root = tk.Tk()
    root.withdraw()  # Скрыть главное окно tkinter
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )
    if file_path:
        try:
            image = pygame.image.load(file_path)
            scaled_image = pygame.transform.scale(image, (150, 150))
            cur_user['avatar'] = scaled_image
            raw_image = pygame.image.tostring(scaled_image, 'RGBA')
            #db_quiz.sql_exec(f"UPDATE user SET avatar = ? WHERE id = ? ({raw_image}, {cur_user['id']}")
            ##db_quiz.sql_exec(f'UPDATE user SET avatar = ? WHERE ID = ?, ({raw_image}, {user_id})')

        except pygame.error as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

def get_history(cur_user):
    user_history = []
    #
    stat_user = db_quiz.sql_get_stats_user(cur_user['id'])
    #user_id, data_id, game_id, cnt, sum_pt
    for r_one in stat_user:
        user_history.append({'date': r_one[1], 'score': r_one[4], 'game_id': r_one[2]})
    #
    '''
    user_history = [{'date': '2023-05-01', 'score': 100, 'game_id': 1},
                    {'date': '2023-05-02', 'score': 10, 'game_id': 12},
                    {'date': '2023-05-03', 'score': 80, 'game_id': 33}]
                    '''

    return user_history


def draw_profile_page(screen, state, current_user):

    fonts = qlib.create_fonts()
    clock = pygame.time.Clock()
    user_history = get_history(current_user)
    button_profile = qlib.create_button('Перейти к категориям', 130, 500, 270, 50, qlib.TEXT_COLOR, font=fonts['font32'])
    button_end = qlib.create_button('Покинуть игру', 410, 500, 200, 50, qlib.TEXT_COLOR, font=fonts['font32'])
    button_load_avatar = qlib.create_button('Загрузить аватар', 250, 170, 180, 40, qlib.TEXT_COLOR, font=fonts['font24'])

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return 'quit'

            if state == 'profile':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_profile['bt_rect'].collidepoint(event.pos):
                        return 'category'

                    if button_load_avatar['bt_rect'].collidepoint(event.pos):
                        load_file(current_user)
                        #
                        db_quiz.sql_save_image(current_user['id'], current_user['avatar'])

                    if button_end['bt_rect'].collidepoint(event.pos):
                        return 'quit'

        # Очистка экрана
        screen.fill(qlib.BG_COLOR)

        qlib.draw_text(screen, 'Личный кабинет', (150, 30), False, fonts['font32'])
        qlib.draw_text(screen, f'Имя игрока: {current_user["username"]}', (250, 100), False, fonts['font24'])
        qlib.draw_text(screen, f'Э-почта: {current_user["email"]}', (250, 130), False, fonts['font24'])
        user_avatar = current_user['avatar']
        if user_avatar != None:
            screen.blit(current_user['avatar'], (80, 80))
        qlib.draw_button(screen, button_load_avatar)

        qlib.draw_text(screen, f'Всего пройдено викторин: {len(user_history)}', (80, 250), False, fonts['font24'])
        qlib.draw_text(screen, f'Набрано очков: {sum([x["score"] for x in user_history])}', (350, 250), False, fonts['font24'])

        qlib.draw_text(screen,f'Результаты последних 5 игр',(80, 290), False, fonts['font24'])
        for ind, history in enumerate(user_history):
            if ind == 6:
               break
            qlib.draw_text(screen, f'Викторина {history["game_id"]} : дата: {history["date"]} : результат: {history["score"]}',
                           (80, 320 + ind * 30), False, fonts['font24'])

        qlib.draw_button(screen, button_profile)
        qlib.draw_button(screen, button_end)

        pygame.display.flip()
        clock.tick(FPS)
