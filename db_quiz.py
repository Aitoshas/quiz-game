import sqlite3 as sq

def sql_exec(str_sql):
    with sq.connect('game_quiz.db') as con:
        con.execute(str_sql)
        con.commit()

def sql_get_user(user_name,user_email):
    with sq.connect('game_quiz.db') as con:
        cur = con.cursor()
        cur.execute("select id, avatar from user where name = ? and email = ?",
                    (user_name, user_email))
        rez = cur.fetchone()
        if rez is None:
            return -1
        else:
            return rez

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

def sql_get_quiz(theme_name):
    with sq.connect('game_quiz.db') as con:
        cur = con.cursor()
        cur.execute(f"select id, quest, ans1, ans2, ans3, theme_name, category_name, points from quiz_set where theme_name = '{theme_name}'")
        rez = cur.fetchall()
        return rez

