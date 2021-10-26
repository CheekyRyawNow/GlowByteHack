import vk_api
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import datetime

load_dotenv()

LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
ID_RANGE_START = 1000000
ID_RANGE_END = 50000000
QUERY_CONSTRAINT = 1000
REQUESTS_NUMBER = 5
COMMON_FIELDS = [
    'bdate',
    'sex',
    'last_seen',
    'can_write_private_message'
]
PUBLIC_FIELDS = [
    'country',
    'city',
    'relation',
    'games',
    'books'
]
TAG = ['tag']
PRIVATE_USERS_FILENAME = 'private_users.csv'
PUBLIC_USERS_FILENAME = 'public_users.csv'
TAGGED_PRIVATE_USERS_FILENAME = 'private_users_tagged.csv'
TAGGED_PUBLIC_USERS_FILENAME = 'public_users_tagged.csv'


def connect_vk():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    vk_session.auth()
    vk = vk_session.get_api()
    return vk


def parse_users(vk, requests_number):
    private_users = []
    public_users = []
    for i in range(requests_number):
        ids = []
        for i in range(QUERY_CONSTRAINT):
            ids.append(np.random.randint(ID_RANGE_START, ID_RANGE_END))
        users = vk.users.get(user_ids=ids, fields=(COMMON_FIELDS + PUBLIC_FIELDS))
        for user in users:
            if 'deactivated' not in user:
                if user['is_closed'] == 1:
                    private_users.append(user)
                else:
                    public_users.append(user)
    return private_users, public_users


def save_parsed_users(users, fields, path_to_save):
    data, dataFrame = read_csv(path_to_save, fields)
    for user in users:
        if user['id'] not in data[:, 0]:
            new_row = []
            if 'bdate' in user and len(user['bdate']) < 8:
                user['bdate'] = None
            for field in fields:
                if field not in user or not user[field]:
                    user[field] = None
                new_row.append(user[field])
            data = np.vstack([data, new_row])
    save_csv(path_to_save, fields, data) 
    return users

 
def read_csv(path_to_read, fields):
    try:
        dataFrame = pd.read_csv(path_to_read)
        data = dataFrame.to_numpy()
        data = np.delete(data, 0, 1)
    except FileNotFoundError:
        dataFrame = pd.DataFrame(columns=fields)
        data = dataFrame.to_numpy()
    # return data, dataFrame
    return data, dataFrame


def save_csv(path_to_save, fields, data):
    dataFrame = pd.DataFrame(data, columns=fields)
    dataFrame.to_csv(path_to_save)


def tag_users(users):
    user_age = 0
    for user in users:
        user['tag'] = []
        if user['is_closed']:
            user['tag'].append('Security')
        else:
            if user['bdate'] != None:
                user_age = calculate_age(user['bdate'])
            if user['sex'] == 2 and user_age in range(17, 28):
                user['tag'].append('Army')
            elif user['sex'] == 1 and user_age in range(23, 41):
                user['tag'].append('Motherhood')
            if user_age < 40:
                user['tag'].append('Games')
            if user['last_seen'] != None:
                if 'platform' in user['last_seen']:
                    if user['last_seen']['platform'] != 7:
                        user['tag'].append('Mobile')
                    else:
                        user['tag'].append('Desktop')
            if user_age > 60:
                user['tag'].append('Old_people')
            if user_age > 35:
                user['tag'].append('Credit')
                if user['sex'] == 2:
                    user['tag'].append('Fishing')
                    user['tag'].append('Hunting')
            if user['relation'] == 1 or user['relation'] in range(5, 7):
                user['tag'].append('Love_search')
            elif user['relation'] != 0:
                user['tag'].append('Love_in')
            if user['books'] != None:
                user['tag'].append('Books')
    return users


def save_tagged_users(users, fields, path_to_save):
    data, dataFrame = read_csv(path_to_save, fields)
    for user in users:
        if user['id'] not in data[:, 0]:
            new_row = []
            for field in fields:
                new_row.append(user[field])
            data = np.vstack([data, new_row])
    save_csv(path_to_save, fields, data)


# DD.MM.YYYY string
def calculate_age(bdate):
    bdate = bdate.split('.')
    today = datetime.date.today()
    return today.year - int(bdate[2]) - ((today.month, today.day) < (int(bdate[1]), int(bdate[0])))


if __name__ == '__main__':
    vk = connect_vk()
    private_users, public_users = parse_users(vk, REQUESTS_NUMBER)
    private_users = save_parsed_users(private_users, COMMON_FIELDS + TAG, PRIVATE_USERS_FILENAME)
    public_users = save_parsed_users(public_users, COMMON_FIELDS + PUBLIC_FIELDS + TAG, PUBLIC_USERS_FILENAME)

    private_users_tagged = tag_users(private_users)
    public_users_tagged = tag_users(public_users)
    save_tagged_users(private_users_tagged, COMMON_FIELDS + TAG,TAGGED_PRIVATE_USERS_FILENAME)
    save_tagged_users(public_users_tagged, COMMON_FIELDS + PUBLIC_FIELDS + TAG, TAGGED_PUBLIC_USERS_FILENAME)
