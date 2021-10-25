import vk_api
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np

load_dotenv()

LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
ID_RANGE_START = 1000000
ID_RANGE_END = 50000000
QUERY_CONSTRAINT = 1000
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
    'relation',
    'games'
]
PRIVATE_USERS_FILENAME = 'private_users.csv'
PUBLIC_USERS_FILENAME = 'public_users.csv'


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
            new_row = []
            for field in fields:
                if field not in user or not user[field]:
                    user[field] = np.nan
                new_row.append(user[field])
            data = np.vstack([data, new_row])
    dataFrame = pd.DataFrame(data, columns=fields)
    dataFrame.to_csv(path_to_save)


def parse_users():
    vk = connect_vk()
    ids = []
    for i in range(QUERY_CONSTRAINT):
        ids.append(np.random.randint(ID_RANGE_START, ID_RANGE_END))
    users = vk.users.get(user_ids=ids, fields=(COMMON_FIELDS + PUBLIC_FIELDS))
    private_users = []
    public_users = []
    for user in users:
        if 'deactivated' not in user:
            if user['is_closed'] == 1:
                private_users.append(user)
            else:
                public_users.append(user)
    save_users(private_users, COMMON_FIELDS, PRIVATE_USERS_FILENAME)
    save_users(public_users, COMMON_FIELDS + PUBLIC_FIELDS, PUBLIC_USERS_FILENAME)


parse_users()
