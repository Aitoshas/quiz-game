import pygame
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import quiz_lib as qlib

FPS = 30

users = []
init_profile = False
current_user = False

# Данные пользователя
user_data = {
    'id': 0,
    'username': 'zerocoder',
    'email': 'zero@code.ru',
    'avatar': pygame.image.load("img/avatar.png")
}

users.append(user_data)


def check_user(login_data):
    username = login_data['username'].lower()
    email = login_data['email'].lower()

    cur_user = False
    for user in users:
        if user['username'] == username and user['email'] == email:
            cur_user = user
            break

    if not cur_user:
        cur_user = {'username': username, 'email': email, 'avatar': '', 'id': len(users)}
        users.append(cur_user)

    return cur_user


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
            cur_user['avatar'] = image
        except pygame.error as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")


def draw_profile_page(screen, state, login_data):

    global current_user

    fonts = qlib.create_fonts()
    clock = pygame.time.Clock()
    button_profile = qlib.create_button('Перейти к категориям', 230, 500, 370, 50, qlib.TEXT_COLOR, font=fonts['font32'])
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

        # Очистка экрана
        screen.fill(qlib.BG_COLOR)

        qlib.draw_text(screen, 'Личный кабинет', (150, 30), False, fonts['font32'])
        current_user = check_user(login_data)
        qlib.draw_text(screen, f'Имя игрока: {current_user['username']}', (250, 100), False, fonts['font24'])
        qlib.draw_text(screen, f'Э-почта: {current_user['email']}', (250, 130), False, fonts['font24'])
        user_avatar = current_user['avatar']
        if user_avatar != '':
            screen.blit(current_user['avatar'], (80, 80), (0, 0, 150, 150))

        qlib.draw_button(screen, button_load_avatar)
        qlib.draw_button(screen, button_profile)

        pygame.display.flip()
        clock.tick(FPS)
