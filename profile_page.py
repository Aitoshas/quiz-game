import pygame
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import quiz_lib as qlib
import db_quiz

FPS = 30

init_profile = False
current_user = False


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
            # rwa_image = pygame.image.tostring(scaled_image, 'RGBA')

        except pygame.error as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")


def get_history(cur_user):
    user_history = []
    #
    stat_user = db_quiz.sql_get_stats_user(cur_user['id'])
    # user_id, data_id, game_id, cnt, sum_pt
    for r_one in stat_user:
        user_history.append({'date': r_one[1], 'score': r_one[4], 'game_id': r_one[2]})
    #
    user_history.sort(key=lambda x: x['date'], reverse=True)

    return user_history

def get_stats(cur_user):
    user_stats = []
    user_stats = db_quiz.sql_get_full_stats_user(cur_user['id'])
    all_stats = 0
    all_sum = 0
    #user_id, cnt, sum_all
    for s_one in user_stats:
        all_stats = s_one[1]
        all_sum = s_one[2]
        break

    return {'all_count': all_stats, "all_sum": all_sum}

def draw_profile_page(screen, state, current_user):

    fonts = qlib.create_fonts()
    clock = pygame.time.Clock()
    user_history = get_history(current_user)
    #user_stats = get_stats(current_user)
    button_profile = qlib.create_button('Перейти к категориям', 100, 520, 290, 40, qlib.TEXT_COLOR, font=fonts['font32'])
    button_end = qlib.create_button('Покинуть игру', 420, 520, 200, 40, qlib.TEXT_COLOR, font=fonts['font32'])
    button_load_avatar = qlib.create_button('Загрузить аватар', 250, 170, 200, 40, qlib.TEXT_COLOR, font=fonts['font24'])
    background_image = pygame.image.load('img/fon1.png')

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
        # screen.fill(qlib.BG_COLOR)
        screen.blit(background_image, (0, 0))

        qlib.draw_text(screen, 'Личный кабинет', (350, 20), False, fonts['font32'])
        qlib.draw_text(screen, f'Имя игрока: {current_user["username"]}', (250, 90), False, fonts['font24'])
        qlib.draw_text(screen, f'Э-почта: {current_user["email"]}', (250, 120), False, fonts['font24'])
        user_avatar = current_user['avatar']
        if user_avatar is not None:
            screen.blit(current_user['avatar'], (80, 60))
        qlib.draw_button(screen, button_load_avatar)

        qlib.draw_text(screen, f'Всего пройдено викторин: {len(user_history)}', (80, 230), False, fonts['font24'])
        qlib.draw_text(screen, f'Набрано очков: {sum([x["score"] for x in user_history])}', (380, 230), False, fonts['font24'])
        #qlib.draw_text(screen, f'Всего пройдено викторин: {user_stats["all_count"]}', (80, 230), False, fonts['font24'])
        #qlib.draw_text(screen, f'Набрано очков: {user_stats["all_sum"]}', (380, 230), False, fonts['font24'])

        qlib.draw_text(screen, f'Результаты последних 5 игр', (80, 270), False, fonts['font24'])
        qlib.draw_grid(screen, (75, 295), 480, 210)
        qlib.draw_text(screen, f'№ викторины           дата                     результат',(80, 300), False, fonts['font24'])
        for ind, history in enumerate(user_history):
            if ind == 5:
                break
            qlib.draw_text(screen, f'{history["game_id"]:^20} {history["date"]:^20} {history["score"]:^28}',
                           (80, 330 + ind * 30), False, fonts['font24'])

        qlib.draw_button(screen, button_profile)
        qlib.draw_button(screen, button_end)

        pygame.display.flip()
        clock.tick(FPS)
