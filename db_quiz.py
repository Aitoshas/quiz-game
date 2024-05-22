import os
import sqlite3 as sq
from PIL import Image
import io
import pygame

def sql_exec(str_sql):
    with sq.connect('game_quiz.db') as con:
        con.execute(str_sql)
        con.commit()

def sql_get_user(user_name,user_email):
    with sq.connect('game_quiz.db') as con:
        cur = con.cursor()
        cur.execute("select id from user where name = ? and email = ?",
                    (user_name, user_email))
        rez = cur.fetchone()
        if rez is None:
            return -1
        else:
            return rez[0]

def sql_get_category(cat_name):
    with sq.connect('game_quiz.db') as con:
        cur = con.cursor()
        cur.execute(f"select id from category where name = '{cat_name}'")
        rez = cur.fetchone()
        if rez is None:
            return -1
        else:
            return rez[0]

def sql_get_theme(theme_name):
    with sq.connect('game_quiz.db') as con:
        cur = con.cursor()
        cur.execute(f"select id from theme where name = '{theme_name}'")
        rez = cur.fetchone()
        if rez is None:
            return -1
        else:
            return rez[0]

def sql_get_all_theme():
    with sq.connect('game_quiz.db') as con:
        cur = con.cursor()
        cur.execute(f"select id, name from theme")
        rez = cur.fetchall()
        return rez


def sql_get_quiz(theme_name):
    with sq.connect('game_quiz.db') as con:
        cur = con.cursor()
        cur.execute(f"select id, quest, ans1, ans2, ans3, theme_name, category_name, points from quiz_set where theme_name = '{theme_name}'")
        rez = cur.fetchall()
        return rez

#   Сохранение в БД username
def sql_save_user(user_name, user_email):
    with sq.connect('game_quiz.db') as con:
        cur = con.cursor()
        cur.execute('insert into user(name, email) values(?,?)', (user_name, user_email))
        con.commit()
        user_id = cur.lastrowid
    return user_id

#   Сохранение Image в DB для текущего user id
def sql_save_image(user_id, image1):
    pygame.image.save(image1, '~tmp.png')
    with io.open('~tmp.png', 'rb') as f:
        image_blob = f.read()

    try:
        os.remove('~tmp.png')
    except:
        None

    with sq.connect('game_quiz.db') as con:
        cur = con.cursor()
        cur.execute('update user set avatar = ? where id = ?', (image_blob, user_id))
        con.commit()

def sql_get_avatar(user_id):
    with sq.connect('game_quiz.db') as con:
        cur = con.cursor()
        cur.execute('SELECT avatar FROM user WHERE id=?', (user_id,))
        image_blob = cur.fetchone()[0]
    retrieved_image = None
    if image_blob:
        with io.open('~tmp.png', 'wb') as f:
            f.write(image_blob)
            f.close()
        retrieved_image = pygame.image.load('~tmp.png')
        try:
            os.remove('~tmp.png')
        except:
            None
    return retrieved_image


def sql_get_next_game_id():
    with sq.connect('game_quiz.db') as con:
        cur = con.cursor()
        cur.execute(f"select max(game_id)+1 from GAME_SETS")
        rez = cur.fetchone()
        if rez == (None,):
            return 1
        else:
            return rez[0]

def sql_save_game_ansver(data_id, user_id, game_id, quiz_id, ans_num, points):
    with sq.connect('game_quiz.db') as con:
        cur = con.cursor()
        cur.execute('''
        insert into GAME_SETS(data_id, user_id, game_id, quiz_id, ans_num, points) 
        values(?,?,?,?,?,?)
        '''
        , (data_id, user_id, game_id, quiz_id, ans_num, points))
        con.commit()
    return game_id

# Статистика игр
def sql_get_stats_user(user_id):
    with sq.connect('game_quiz.db') as con:
        cur = con.cursor()
        cur.execute(f"select user_id, data_id, game_id, cnt, sum_pt from all_games where user_id = ? order by game_id desc limit 5" ,(user_id,))
        rez = cur.fetchall()
        return rez

def sql_get_full_stats_user(user_id):
    with sq.connect('game_quiz.db') as con:
        cur = con.cursor()
        cur.execute(f"select user_id, cnt, sum_all from game_set_stats where user_id = ?" ,(user_id,))
        rez = cur.fetchall()
        return rez

def sql_get_full_stats_all_users():
    with sq.connect('game_quiz.db') as con:
        cur = con.cursor()
        cur.execute(f"select user_id, cnt, sum_all from game_set_stats")
        rez = cur.fetchall()
        return rez
