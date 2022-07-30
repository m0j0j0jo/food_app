import csv
import json
import os
csvFilePath = "<path to the food file>\\food_ai_data - Sheet1.csv"

FOOD_NAME = 'food_name'
TIME = 'time'
SCORE = 'score'


def csv_to_json():
    users_json = {}

    with open(csvFilePath, encoding='utf-8') as csvf:
        csv_reader = csv.DictReader(csvf)

        for row in csv_reader:
            user_name = row.get('user name')
            user_data = {FOOD_NAME: row.get('food name'),
                         TIME: row.get('time').replace('\"', ''),
                         SCORE: int(row.get('score')) }
            if not users_json.get(user_name):
                users_json[user_name] = {'foods': [user_data]}
            else:
                users_json[user_name]['foods'].append(user_data)

    for user_name, user_data in users_json.items():
        with open(os.path.join(os.getcwd(), '..', 'resource', f'{user_name}.json'), 'w', encoding='utf-8') as jsonf:
            json_string = json.dumps(user_data, indent=4)
            jsonf.write(json_string)


if __name__ == '__main__':
    csv_to_json()

