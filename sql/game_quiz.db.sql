-- Пользователь

CREATE TABLE IF NOT EXISTS "USER" (
	"ID"	INTEGER,
	"name"	TEXT,
	"email"	TEXT,
	"pass"	TEXT,
	PRIMARY KEY("ID" AUTOINCREMENT)
);

-- Тема (ИСТОРИЯ, Культура ...)
CREATE TABLE IF NOT EXISTS "THEME" (
	"ID"	INTEGER,
	"NAME"	TEXT,
	PRIMARY KEY("ID" AUTOINCREMENT)
);

--	Категория вопрса (Легкий, Среднийб Сложный)
CREATE TABLE IF NOT EXISTS "CATEGORY" (
	"ID"	INTEGER,
	"NAME"	TEXT,
	"POINTS"	INTEGER,	--	Очки за вопрос из категории (10, 20, 30)
	PRIMARY KEY("ID" AUTOINCREMENT)
);

--	Вопрос - ответ
CREATE TABLE IF NOT EXISTS "QUIZ" (
	"iD"	INTEGER,
	"QUEST"	TEXT,
	"ANS1"	TEXT,
	"ANS2"	TEXT,
	"ANS3"	TEXT,
	"THEME_ID"	INTEGER,	--ссылка на темы
	"CATEGORY_ID"	INTEGER,	--ссылка на категории
	PRIMARY KEY("iD" AUTOINCREMENT)
);


CREATE TABLE IF NOT EXISTS "GAME_SETS" (
	"ID"	INTEGER,		--	ID ответа пользователя
	"DATA_ID"	TEXT,		--	дата и (время?) игры
	"USER_ID"	INTEGER,	--	ссылка на ID пользователя
	"GAME_ID"	INTEGER,	--	ID одной игры (10 вопросов по теме)
	"QUIZ_ID"	INTEGER,	--	ID вопроса (ссылка на таблицу QUIZ)
	"ANS_NUM"	INTEGER,	--	Номер ответа (1,2,3)
	"POINTS"	INTEGER,	--	Число очеов за ответ (0 - неправильно,10,20,30 - из category.points )
	PRIMARY KEY("ID" AUTOINCREMENT)
);

--	Представления
--	Выборка вопросов по теме для одной игры 
CREATE VIEW quiz_set as 
select q.id, q.quest, q.ans1, q.ans2, q.ans3, t.name theme_name , cc.name as category_name, cc.points
from quiz q 
join theme t on (t.id = q.theme_id)
join category cc on (q.category_id = cc.id);

--	Общее количество игр и набранных очков игроком
CREATE VIEW game_count as
select count(*) games_count, sum(gg.points) all_points, uu.user 
from game_sets gg join USER uu on uu.id = gg.user_id
group by USER_ID;

--Результаты одной игры для игрока (USER_ID? GAME_ID)
CREATE VIEW game_count_one as
select count(*) games_count, sum(gg.points) all_points, uu.user 
from game_sets gg join USER uu on uu.id = gg.user_id
group by USER_ID, GAME_ID;
