import psycopg2
from datetime import datetime
from flask_mail import Mail, Message

def check_user_email_in_db(email):
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432",
                            database="MyDB")
    cursor = conn.cursor()
    cursor.execute(f"""SELECT email FROM users WHERE email = '{email}' """)
    user_email = cursor.fetchone()
    cursor.close()
    conn.close()
    if user_email is not None:
        if user_email[0] == email:
            return 1
    else:
        return 0







import secrets


reset_tokens = {}

def generate_token(email):
    # Generate a secure random token
    token = secrets.token_urlsafe(32)
    # Store the token in the dictionary along with the associated email
    reset_tokens[token] = email
    return token


def get_email_by_token(token):
    # Retrieve the email associated with the token from the dictionary
    return reset_tokens.get(token)


# def send_reset_email(email, reset_link):
#     subject = 'Восстановление пароля'
#     recipients = [email]
#     body = f'Для восстановления пароля перейдите по ссылке: {reset_link}'
#
#     message = Message(subject=subject, recipients=recipients, body=body)
#
#     try:
#         mail.send(message)
#         print(f'Email sent successfully to {email}.')
#     except Exception as e:
#         print(f'Error sending email to {email}: {e}')





def execute_query(query, params=None):
    connection = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432",
                                  database="MyDB")
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    cursor.close()
    connection.close()


def get_students():
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432",
                            database="MyDB")
    cursor = conn.cursor()
    cursor.execute(f"""select * from """)
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    print(students)


def check_username(username):
    # Проверка длины пользователя и отсутствия в базе данных
    if not (2 <= len(username) <= 25) or check_username_in_db(username) != 0:
        return False

    # Проверка наличия служебных символов
    forb_symbols = {' ', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', ']', '{', '}',
                    '|', '\\', ';', ':', "'", '"', ',', '.', '<', '>', '/', '?'}
    if any(char in forb_symbols for char in username):
        return False

    # Проверка ASCII-символов с кодами 0-31
    if any(ord(char) < 32 for char in username):
        return False

    return True


def check_password(password):
    # Проверка длины пароля
    if not (8 <= len(password) <= 25):
        return False

    # Проверка наличия символов русского алфавита
    if any('а' <= char <= 'я' or 'А' <= char <= 'Я' for char in password):
        return False

    # Проверка ASCII-символов с кодами 0-31
    if any(0 <= ord(char) <= 31 for char in password):
        return False

    return True


def check_username_in_db(username):
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432",
                            database="MyDB")
    cursor = conn.cursor()
    cursor.execute(f"""SELECT username FROM users WHERE username = '{username}' """)
    user_name = cursor.fetchone()
    cursor.close()
    conn.close()
    if user_name is not None:
        if user_name[0] == username:
            return True
    else:
        return False


def check_user_info_before_db(username, password):
    error = []
    if not check_username(username):
        error.append('username')
    if not check_password(password):
        error.append('password')
    return error


def check_confirm_password(password, confirm_password):
    return password == confirm_password


def get_data_for_profile_redirect(username):
    student_info = get_student_info(username)

    # Передаем информацию в шаблон
    student_info_dict = {}
    for key, value in student_info.items():
        student_info_dict[key] = value
        print(student_info_dict)
    return student_info_dict


# def get_tests_form_bd()
def get_tests_from_db():
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432",
                            database="MyDB")
    cursor = conn.cursor()
    cursor.execute("SELECT question FROM questions")
    questions = cursor.fetchall()
    for i in questions:
        print(i[0])
    cursor.close()
    conn.close()
    return questions


# def get_student_info(username, studid):
#     # Здесь вам нужно выполнить SQL-запрос к базе данных
#     # для извлечения информации о студенте по логину и studid
#     # Замените этот код на ваш реальный запрос
#     conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432",
#                             database="MyDB")
#     cursor = conn.cursor()
#     cursor.execute("select firstname, lastname, course, groupnumber from students where username = 'Testuser'")
#
#     student_info = {
#         'username': username,
#         'studid': studid,
#         'other_field': 'значение',
#         # Дополнительные поля из базы данных
#     }
#     return student_info


def get_student_info(username):
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()

    try:
        # Получаем userid по username
        cursor.execute(f"SELECT userid FROM users WHERE username = '{username}'")
        userid = cursor.fetchone()

        # Если userid найден, получаем информацию о студенте
        if userid:
            userid = userid[0]

            cursor.execute(f"SELECT s.firstname, s.lastname, s.course, s.groupnumber, s.username "
                           f"FROM students s "
                           f"JOIN users_stud us ON s.studid = us.studid "
                           f"WHERE us.userid = {userid}")

            # Получение результата
            student_info = cursor.fetchone()

            # Проверяем, были ли получены данные
            if student_info:
                # Преобразуем результат запроса в словарь для удобства использования в шаблоне
                student_info_dict = {
                    'firstname': student_info[0],
                    'lastname': student_info[1],
                    'course': student_info[2],
                    'groupnumber': student_info[3],
                    'username': student_info[4],
                }

                return student_info_dict
            else:
                return {}
        else:

            return {}

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_professor_info(username):
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT username, firstname, lastname, department FROM professors WHERE username = %s",
            (username,)
        )
        professor_info = cursor.fetchone()

        if professor_info:
            professor_info_dict = {
                'username': professor_info[0],
                'firstname': professor_info[1],
                'lastname': professor_info[2],
                'department': professor_info[3]
            }
            return professor_info_dict
        else:
            return {}

    except Exception as e:
        print(f"Error fetching professor info: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_user_password_from_db(username):
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()
    cursor.execute(f"""SELECT "userpassword" FROM users WHERE username = '{username}'""")
    password = cursor.fetchone()
    cursor.close()
    conn.close()
    return password[0]


def get_themes_from_db():
    try:
        conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
        cursor = conn.cursor()

        # Выполните запрос для получения тем из таблицы questions
        cursor.execute("SELECT DISTINCT theme FROM questions")

        # Получите все уникальные темы
        themes = [row[0] for row in cursor.fetchall()]
        #print(themes)
        return themes

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None

    finally:
        if conn:
            cursor.close()
            conn.close()


def get_num_questions(selected_theme):
    # Подключаемся к базе данных
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()

    # Формируем и выполняем запрос
    query = f"SELECT COUNT(*) FROM questions WHERE theme = '{selected_theme}'"
    cursor.execute(query)
    num_questions = cursor.fetchone()[0]
    print(num_questions)
    print(selected_theme)

    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()

    return num_questions


# def get_questions_from_db(selected_theme):
#     conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
#     cursor = conn.cursor()
#     try:
#         cursor.execute(f"SELECT questid, question_text FROM questions WHERE theme = '{selected_theme}'")
#         questions = cursor.fetchall()
#
#         # Возвращаем список словарей, где каждый словарь содержит quest_id и question_text
#         return [{'quest_id': question[0], 'question_text': question[1]} for question in questions]
#     except Exception as e:
#         print(f"Ошибка при выполнении запроса: {e}")
#         return []
#     finally:
#         cursor.close()
#         conn.close()


def get_questions_from_db(selected_theme):
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT questid, question_text FROM questions WHERE theme = '{selected_theme}'")
        questions = cursor.fetchall()
        return questions
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


# def get_answer_from_db(quest_id):
#     conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
#     cursor = conn.cursor()
#
#     try:
#         cursor.execute(f"SELECT answer FROM questions WHERE questid = {quest_id}")
#         answer = cursor.fetchone()
#
#         if answer:
#             return answer[0]
#         else:
#             return None
#
#     except Exception as e:
#         print(f"Ошибка при выполнении запроса: {e}")
#         return None
#     finally:
#         cursor.close()
#         conn.close()

def get_answer_from_db(quest_id):
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT answer FROM questions WHERE questid = {quest_id}")
        answer = cursor.fetchone()

        if answer:
            return answer[0]
        else:
            return None

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_wrong_answer_from_db(quest_id):
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT wrong_answer FROM questions WHERE questid = {quest_id}")
        wrong_answer = cursor.fetchone()

        if wrong_answer:
            return wrong_answer[0]
        else:
            return None

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


import psycopg2


def calculate_average_scores():
    try:
        conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
        cursor = conn.cursor()

        # Получение списка тестов
        cursor.execute("SELECT DISTINCT testid FROM testresults")
        test_ids = cursor.fetchall()

        for test_id in test_ids:
            # Расчет средней оценки для каждого теста
            cursor.execute("SELECT AVG(mark) FROM testresults WHERE testid = %s", (test_id,))
            average_score = cursor.fetchone()[0]

            #print(f"Средняя оценка для теста {test_id}: {average_score}")

            # Обновление столбца averagemark в таблице testresults
            cursor.execute("UPDATE testresults SET averagemark = %s WHERE testid = %s", (average_score, test_id))
            conn.commit()


    except (Exception, psycopg2.Error) as error:

        print(f"Ошибка при расчете и обновлении средних оценок: {error}")

        conn.rollback()

    finally:
        # Закрытие соединения с базой данных
        if conn:
            cursor.close()
            conn.close()


def get_all_students():
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()

    try:
        print('privet')
        cursor.execute("SELECT studid, firstname, lastname, course, groupnumber FROM students")
        students = cursor.fetchall()

        student_list = []
        for student in students:
            student_info = {
                'student_id': student[0],
                'firstname': student[1],
                'lastname': student[2],
                'course': student[3],
                'groupnumber': student[4]
            }
            student_list.append(student_info)
        print(student_list)
        return student_list

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


import psycopg2


def add_student_to_db(firstname, lastname, course, groupnumber):
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO students (firstname, lastname, course, groupnumber)
            VALUES (%s, %s, %s, %s)
        """, (firstname, lastname, course, groupnumber))

        # Подтверждаем изменения в базе данных
        conn.commit()

        return True  # Возвращаем True в случае успешного добавления
    except Exception as e:
        print(f"Ошибка при добавлении студента в базу данных: {e}")
        return False  # Возвращаем False в случае ошибки
    finally:
        cursor.close()
        conn.close()


# Ваш класс file1


def delete_student_by_id(studid):
    conn = None
    try:
        conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
        cursor = conn.cursor()

        # SQL-запрос для удаления студента по ID
        delete_query = "DELETE FROM students WHERE studid = %s"

        # Выполняем запрос
        cursor.execute(delete_query, (studid,))

        # Подтверждаем изменения в базе данных
        conn.commit()

        return True  # Успешное удаление
    except Exception as e:
        # Обработка ошибок, например, логирование
        print(f"Ошибка при удалении студента: {str(e)}")
        return False  # Ошибка при удалении
    finally:
        if conn is not None:
            conn.close()


def add_question_to_db(question_text, answer, weight, theme, wrong_answer):
    try:
        # Установка соединения с базой данных
        conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO questions (question_text, answer, weight, theme, wrong_answer)
            VALUES (%s, %s, %s, %s, %s)
        """, (question_text, answer, weight, theme, wrong_answer))

        # Подтверждение изменений
        conn.commit()

        # Закрытие соединения
        conn.close()

        return True  # Возвращаем True в случае успешного добавления
    except Exception as e:
        print(f"Ошибка при добавлении вопроса в базу данных: {e}")
        return False  # Возвращаем False в случае ошибки


def get_question_weight_by_id(questid):
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()

    # SQL-запрос для извлечения поля weight из таблицы questions по questid
    cursor.execute(f"SELECT weight FROM questions WHERE questid = {questid}")
    # query = "SELECT weight FROM questions WHERE questid = {quest_id}"
    # cursor.execute(query, (questid,))

    # Получаем результат
    weight = cursor.fetchone()

    # Закрываем соединение
    cursor.close()
    conn.close()

    return weight[0] if weight else None


import sqlite3  # Предположим, что вы используете SQLite, но замените на свой тип базы данных

import psycopg2


def get_question_id_by_answer(answer):
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()

    try:
        # Используем параметризированный запрос для безопасности
        query = "SELECT questid, weight FROM questions WHERE answer = %s"
        cursor.execute(query, (answer,))

        question_info = cursor.fetchone()

        if question_info:
            # Если есть результат, возвращаем кортеж (questid, weight)
            return question_info
        else:
            # Если ответ не найден, возвращаем None
            return None
    finally:
        # Закрываем соединение
        conn.close()


def get_studid_by_username(username):
    try:
        # Используем менеджер контекста для автоматического закрытия соединения
        with psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432",
                              database="MyDB") as conn:
            with conn.cursor() as cursor:
                # Используем параметризированный запрос для безопасности
                query = "SELECT studid FROM students WHERE username = %s"
                cursor.execute(query, (username,))

                student_id = cursor.fetchone()

                return student_id[0] if student_id else None
    except Exception as e:
        # Обработка ошибок
        print(f"Ошибка: {e}")
        return None


def get_tetstid_by_theme(theme):
    try:
        # Используем менеджер контекста для автоматического закрытия соединения
        with psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432",
                              database="MyDB") as conn:
            with conn.cursor() as cursor:
                # Используем параметризированный запрос для безопасности
                query = "SELECT testid FROM tests WHERE theme = %s"
                cursor.execute(query, (theme,))

                test_id = cursor.fetchone()

                return test_id[0] if test_id else None
    except Exception as e:
        # Обработка ошибок
        print(f"Ошибка: {e}")
        return None


def average_score_by_theme(theme):
    try:
        conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
        cursor = conn.cursor()

        # Расчет средней оценки для теста с заданной темой
        cursor.execute("SELECT AVG(mark) FROM testresults WHERE testid IN (SELECT testid FROM tests WHERE theme = %s)",
                       (theme,))
        average_score = cursor.fetchone()[0]

        if average_score is not None:
            print(f"Средняя оценка для тестов по теме '{theme}': {average_score}")
        else:
            print(f"Нет данных о тестах по теме '{theme}' в таблице testresults.")

    except (Exception, psycopg2.Error) as error:
        print(f"Ошибка при расчете средней оценки: {error}")

    finally:
        # Закрытие соединения с базой данных
        if conn:
            cursor.close()
            conn.close()


def average_mark_by_theme(theme):
    try:
        conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
        cursor = conn.cursor()

        # Расчет средней оценки для теста с заданной темой
        cursor.execute("SELECT AVG(mark) FROM testresults WHERE testid IN (SELECT testid FROM tests WHERE theme = %s)",
                       (theme,))
        average_score = cursor.fetchone()[0]

        if average_score is not None:
            print(f"Средняя оценка для тестов по теме '{theme}': {average_score}")
            return average_score
        else:
            print(f"Нет данных о тестах по теме '{theme}' в таблице testresults.")
            return None

    except (Exception, psycopg2.Error) as error:
        print(f"Ошибка при расчете средней оценки: {error}")
        return None

    finally:
        # Закрытие соединения с базой данных
        if conn:
            cursor.close()
            conn.close()


def get_test_count_by_theme():
    try:
        conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
        cursor = conn.cursor()

        # Запрос для получения темы и количества тестов по каждой теме
        cursor.execute("SELECT tests.theme, COUNT(testresults.testid) FROM tests LEFT JOIN testresults ON tests.testid = testresults.testid GROUP BY tests.theme")
        test_count_by_theme = cursor.fetchall()

        return test_count_by_theme

    except (Exception, psycopg2.Error) as error:
        print(f"Ошибка при получении количества тестов по темам: {error}")
        return None

    finally:
        # Закрытие соединения с базой данных
        if conn:
            cursor.close()
            conn.close()

def get_students_count_by_theme():
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()

    # SQL-запрос для подсчёта уникальных студентов по темам
    query = """
        SELECT t.theme, COUNT(DISTINCT tr.studid) AS student_count
        FROM testresults tr
        JOIN tests t ON tr.testid = t.testid
        GROUP BY t.theme
        ORDER BY student_count DESC;
    """
    try:
        # Выполнение запроса
        cursor.execute(query)
        results = cursor.fetchall()
    finally:
        # Закрытие соединения
        conn.close()

    # Возвращает список кортежей [(theme, student_count), ...]
    print(results)
    return results





def insert_test_result(testid, studid, mark):
    # Подключение к базе данных
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()

    try:
        current_date = datetime.now().strftime('%Y-%m-%d')

        # SQL-запрос для вставки данных в таблицу test_result
        sql_query = "INSERT INTO testresults (testid, studid, date, mark) VALUES (%s, %s, %s, %s)"

        # Значения для вставки
        values = (testid, studid, current_date, mark)

        # Выполнение запроса
        cursor.execute(sql_query, values)

        # Подтверждение изменений
        conn.commit()

        print("Данные успешно добавлены в таблицу test_result.")

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        # Закрытие соединения
        cursor.close()
        conn.close()


# def get_test_results_by_studid(studid):
#     conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
#     cursor = conn.cursor()
#     try:
#         # Замените 'your_table' на реальное имя вашей таблицы
#         query = f"SELECT testid, studid, date, mark, averagemark FROM testresults WHERE studid = {studid}"
#         cursor.execute(query)
#
#         # Получаем все строки результата
#         test_results = cursor.fetchall()
#
#         # Если есть результаты, возвращаем их
#         if test_results:
#             return test_results
#         else:
#             # Если нет результатов, возвращаем None
#             return None
#     finally:
#         # Закрываем соединение
#         conn.close()

def get_test_results_by_studid(studid):
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()

    try:

        query = f"""
            SELECT 
                testresults.testid, 
                testresults.studid, 
                testresults.date, 
                testresults.mark, 
                testresults.averagemark, 
                tests.theme
            FROM 
                testresults 
            JOIN 
                tests ON testresults.testid = tests.testid
            WHERE 
                testresults.studid = {studid}
        """
        cursor.execute(query)

        # Получаем все строки результата
        test_results = cursor.fetchall()

        # Если есть результаты, возвращаем их
        if test_results:
            return test_results
        else:
            # Если нет результатов, возвращаем None
            return None
    finally:
        # Закрываем соединение
        conn.close()




import psycopg2


def search_results_in_db(theme, date):
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()

    try:
        # Формируем SQL-запрос с использованием JOIN и условиями WHERE для поиска по теме и дате
        query = """
            SELECT 
                testresults.testid, 
                testresults.studid, 
                testresults.date, 
                testresults.mark, 
                testresults.averagemark, 
                tests.theme
            FROM 
                testresults 
            JOIN 
                tests ON testresults.testid = tests.testid
        """

        conditions = []

        if theme:
            conditions.append(f"tests.theme ILIKE '%{theme}%'")

        if date:
            conditions.append(f"testresults.date = '{date}'")

        # Добавляем условия в WHERE, если они есть
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query)

        # Получаем все строки результата
        search_test_results = cursor.fetchall()

        # Если есть результаты, возвращаем их
        if search_test_results:
            return search_test_results
        else:
            # Если нет результатов, возвращаем None
            return None
    finally:
        # Закрываем соединение
        conn.close()


import json


def export_database_to_json(host, database, user, password, output_folder):
    # Подключение к базе данных
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()

    # Получение списка всех таблиц в базе данных
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cursor.fetchall()

    # Создание JSON-файла для каждой таблицы
    for table in tables:
        table_name = table[0]
        cursor.execute(f'SELECT * FROM {table_name}')
        data = cursor.fetchall()

        # Закрытие соединения с базой данных
        conn.close()

        # Преобразование данных в формат JSON и сохранение в файл
        json_data = json.dumps(data, ensure_ascii=False, indent=2)

        output_file = f'{output_folder}/{table_name}.json'
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json_file.write(json_data)


# if __name__ == "__main__":
#     # Замените параметры подключения и папку вывода на свои
#     host = 'your_host'
#     database = 'your_database'
#     user = 'your_user'
#     password = 'your_password'
#     output_folder = 'output_folder'
#
#     export_database_to_json(host, database, user, password, output_folder)

import psycopg2


def check_question_in_db(question):
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()

    # Используйте параметризованный запрос
    cursor.execute("SELECT question_text FROM questions WHERE question_text = %s", (question,))

    # Используйте fetchone() вместо fetchall(), так как вы ищете одну конкретную запись
    row = cursor.fetchone()

    if row is not None:
        return 1
    else:
        return 0


def check_student_in_db(first, second):
    conn = psycopg2.connect(user="postgres", password="rootparol", host="127.0.0.1", port="5432", database="MyDB")
    cursor = conn.cursor()
    # Используйте параметризованный запрос
    cursor.execute("SELECT studid FROM students WHERE firstname=%s and lastname=%s", (first, second))
    # Используйте fetchone() вместо fetchall(), так как вы ищете одну конкретную запись
    row = cursor.fetchall()
    print(row)
    if not row:
        return 0
    else:
        return 1



# Пример использования

