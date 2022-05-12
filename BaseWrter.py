import json
import psycopg2
from config import host, password, db_name, user



with open("data/1.json", 'r', encoding='UTF-8') as file:
    info = json.load(file)

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    cursor = connection.cursor()
    for row in info:
        phone_numbers_text = "{"
        for phone in row["phones"]:
            phone_numbers_text += phone + "\n"
        phone_numbers_text += "}"
    #     cursor.execute(
    #     f'INSERT INTO organizations (org_name, adres, good_review, bad_review, phone_numbers) '
    #     f'VALUES ("{row["org_name"]}","{row["adress"]}",{row["good_review"]},{row["bad_review"]},'
    #     f'"{phone_numbers_text}");'
    # )
        params = (row["org_name"], row["adress"], row["good_review"], row["bad_review"])
        cursor.execute(
            'INSERT INTO organizations (org_name, adres, good_review, bad_review) '
            'VALUES (%s,%s,%s,%s);',
            vars=params)
        connection.commit()
        print('xxx')

except Exception as ex_:
    print(ex_)
finally:
    if connection:
        connection.close()
        cursor.close()
