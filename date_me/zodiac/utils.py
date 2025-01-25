from datetime import datetime

def get_zodiac_id(birth_date,gender):

    birth_date=datetime.strptime(birth_date,"%Y-%m-%d").date()
    """
    Определяет знак зодиака по дате рождения.
    
    :param birth_date: дата рождения (объект datetime.date)
    :return: id знака зодиака
    """
    
    zodiac_signs = [
    ("Овен",1, (3, 21), (4, 19)),
    ("Телец",3, (4, 20), (5, 20)),
    ("Близнецы",5, (5, 21), (6, 20)),
    ("Рак",7, (6, 21), (7, 22)),
    ("Лев",9, (7, 23), (8, 22)),
    ("Дева",11, (8, 23), (9, 22)),
    ("Весы",13, (9, 23), (10, 22)),
    ("Скорпион",15, (10, 23), (11, 21)),
    ("Стрелец",17, (11, 22), (12, 21)),
    ("Козерог",19, (12, 22), (1, 19)),
    ("Водолей",21, (1, 20), (2, 18)),
    ("Рыбы",23, (2, 19), (3, 20)),]
    
    for sign, sign_id, start, end in zodiac_signs:
        start_month, start_day = start
        end_month, end_day = end
        
        # Проверяем, входит ли дата в текущий диапазон знака
        if (
            (birth_date.month == start_month and birth_date.day >= start_day) or
            (birth_date.month == end_month and birth_date.day <= end_day)
        ):
            return sign_id if gender=='male' else sign_id+1