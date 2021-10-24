import vk_api
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np

load_dotenv()

#LOGIN = os.getenv('LOGIN')
#PASSWORD = os.getenv('PASSWORD')
LOGIN = ''
PASSWORD = ''
START_OF_RANGE = 1000000
END_OF_RANGE = 50000000
GROUP_SIZE = 1000
COMMON_FIELDS = [
    'id',
    'is_closed',
    'bdate',
    'sex',
    'last_seen',
    'can_write_private_message',
    'first_name',
    'last_name'
]
PUBLIC_FIELDS = [
    'country',
    'city',
    'home_town',
    'connections',
    'contacts',
    'timezone',
    'relation'
    'games'
]
CLOSED_USERS_FILENAME = 'closed_users.csv'
OPENED_USERS_FILENAME = 'opened_users.csv'
#COMMON_FIELDS = ['id', 'first_name', 'last_name', 'sex', 'bdate', 'last_seen_time', 'last_seen_platform']


def connect_vk():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    vk_session.auth()
    vk = vk_session.get_api()
    return vk


def save_users(users, fields, path_to_save):
    try:
        dataFrame = pd.read_csv(path_to_save)
        data = dataFrame.to_numpy()
        data = np.delete(data, 0, 1)
    except FileNotFoundError:
        dataFrame = pd.DataFrame(columns=fields)
        data = dataFrame.to_numpy()
    for user in users:
        if user['id'] not in data[:, 0]:
            for field in fields:
                if field not in user:
                    user[field] = 'none'
            newRow = [
                user['id'],
                user['first_name'],
                user['last_name'],
                user['sex'],
                user['bdate'],
                user['last_seen']['time'],
                user['last_seen']['platform'],
            ]
            data = np.vstack([data, newRow])
    dataFrame = pd.DataFrame(data, columns=fields)
    dataFrame.drop_duplicates(inplace=True)
    dataFrame.to_csv(path_to_save)
    return


def parse_users():
    vk = connect_vk()
    # To do random pick ids
    ids = list(range(27 * GROUP_SIZE, 28 * GROUP_SIZE))
    users = vk.users.get(user_ids=ids, fields=COMMON_FIELDS)
    closed_users = []
    opened_users = []
    for user in users:
        if 'deactivated' not in user:
            if user['is_closed'] == 1:
                closed_users.append(user)
            else:
                opened_users.append(user)
    save_users(closed_users, COMMON_FIELDS, CLOSED_USERS_FILENAME)
    save_users(opened_users, COMMON_FIELDS + PUBLIC_FIELDS, OPENED_USERS_FILENAME)
    return


parse_users()
