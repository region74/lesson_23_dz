import requests
import pprint
import json
import sqlite3


def get_info(text):
    DOMAIN = 'https://api.hh.ru/'
    url = f'{DOMAIN}vacancies'
    found_vac = text
    gorod = '1384'
    params = {
        'text': found_vac,
        # 'experience': 'noExperience',
        'area': gorod
    }

    conn = sqlite3.connect('C:/Users/Кирилл/Desktop/PYTHON/BD/api.db', check_same_thread=False)  # соединяем с бд
    cursor = conn.cursor()

    result = requests.get(url, params=params).json()
    pprint.pprint(result)
    final_result = []
    vacancy_list = []

    for item in result['items']:
        city = item['area']['name']
        employer = item['employer']['name']
        position = item['name']
        link = item['alternate_url']
        try:
            salary = item['salary']['from']
            if salary == None:
                salary = 'Не указана'
        except Exception:
            salary = 'Не указана'

        cursor.execute('insert or ignore into  city (name) values (?)', [city])
        cursor.execute('insert or ignore into link (name) values (?)', [link])
        cursor.execute('insert or ignore into firma (name) values (?)', [employer])
        cursor.execute('insert or ignore into zarplata (name) values(?)', [salary])
        conn.commit()
        city_id = cursor.execute(f'select id from city where city.name="{city}"').fetchone()[0]
        firma_id = cursor.execute(f'select id from firma where firma.name="{employer}"').fetchone()[0]
        link_id = cursor.execute(f'select id from link where link.name="{link}"').fetchone()[0]
        zp_id = cursor.execute(f'select id from zarplata where zarplata.name="{salary}"').fetchone()[0]
        cursor.execute('insert or ignore into vacancy (name,firma_id,city_id,zp_id,link_id) values(?,?,?,?,?)',
                       [position, firma_id, city_id, zp_id, link_id])
        vacancy_list.append(cursor.execute(f'select id from vacancy where vacancy.link_id ="{link_id}"').fetchone()[0])
        conn.commit()

    load_info(final_result, vacancy_list)
    conn.close()
    return final_result,


def load_info(final_result, vacancy_list):
    conn = sqlite3.connect('C:/Users/Кирилл/Desktop/PYTHON/BD/api.db', check_same_thread=False)  # соединяем с бд
    cursor = conn.cursor()
    for vac in vacancy_list:
        query = f'select v.name, c.name, f.name, z.name, l.name ' \
                'from vacancy v, city c, firma f, zarplata z, link l ' \
                f'where v.city_id=c.id and v.firma_id=f.id and v.link_id=l.id and v.zp_id=z.id and v.id="{vac}"'
        cursor.execute(query)
        result = cursor.fetchall()
        for res in result:
            line = ''
            for i in res:
                line += f'{i} '
            final_result.append(line)

    return final_result


text = 'java'

result = get_info(text)
pprint.pprint(result)
