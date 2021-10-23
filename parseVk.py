import vk_api
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np

load_dotenv()

LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
START_OF_RANGE = 1000000
END_OF_RANGE = 50000000
GROUP_SIZE = 1000
FIELDS = [
    'first_name',
    'last_name',
    'deactivated',
    'is_closed',
    'bdate',
    'country',
    'home_town',
    'city',
    'last_seen',
    'connections',
    'contacts',
    'sex',
    'timezone',
    'games',
]
CLOSED_USERS_FILENAME = 'closed_users.csv'
OPENED_USERS_FILENAME = 'opened_users'
CLOSED_COLUMNS = ['id', 'first_name', 'last_name', 'sex', 'bdate', 'last_seen_time', 'last_seen_platform']


def connectVk():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    vk_session.auth()
    vk = vk_session.get_api()
    return vk


def saveClosedUsers(users):
    try:
        dataFrame = pd.read_csv(CLOSED_USERS_FILENAME)
        data = dataFrame.to_numpy()
        data = np.delete(data, 0, 1)
    except FileNotFoundError:
        dataFrame = pd.DataFrame(columns=CLOSED_COLUMNS)
        data = dataFrame.to_numpy()
    for user in users:
        if user['id'] not in data[:, 0]:
            if 'bdate' not in user:
                user['bdate'] = 'none'
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
    dataFrame = pd.DataFrame(data, columns=CLOSED_COLUMNS)
    dataFrame.drop_duplicates(inplace=True)
    dataFrame.to_csv(CLOSED_USERS_FILENAME)
    return


def saveOpenedUsers(users):
    # Нужно доделать
    # try:
    #     dataFrame = pd.read_csv(OPENED_USERS_FILENAME)
    #     data = dataFrame.to_numpy()
    #     data = np.delete(data, 0, 1)
    # except FileNotFoundError:
    #     dataFrame = pd.DataFrame(columns=FIELDS)
    #     data = dataFrame.to_numpy()
    # for user in users:
    #     if user['id'] not in data[:, 0]:
    #         if 'bdate' not in user:
    #             user['bdate'] = 'none'
    #         newRow = [
    #             user['id'],
    #             user['first_name'],
    #             user['last_name'],
    #             user['sex'],
    #             user['bdate'],
    #             user['last_seen']['time'],
    #             user['last_seen']['platform'],
    #         ]
    #         data = np.vstack([data, newRow])
    # dataFrame = pd.DataFrame(data, columns=FIELDS)
    # dataFrame.drop_duplicates(inplace=True)
    # dataFrame.to_csv(OPENED_USERS_FILENAME)
    return


def parseUsers():
    vk = connectVk()
    # for i in range(int(START_OF_RANGE / GROUP_SIZE), int(END_OF_RANGE / GROUP_SIZE)):
    ids = list(range(27 * GROUP_SIZE, 28 * GROUP_SIZE))
    users = vk.users.get(user_ids=ids, fields=FIELDS)
    closedUsers = []
    openedUsers = []
    for user in users:
        if 'deactivated' not in user:
            if user['is_closed'] == 1:
                closedUsers.append(user)
            else:
                openedUsers.append(user)
    saveClosedUsers(closedUsers)
    # saveOpenedUsers(openedUsers)
    return


parseUsers()
