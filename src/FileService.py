import pandas as pd


class FileService:
    def __init__(self, users_filename):
        self.__users_filename = users_filename


    def set_users_filename(self, path):
        self.__users_filename = path


    def get_users_filename(self):
        return self.__users_filename


    def save_users(self, users, fields):
        df = pd.DataFrame(users, columns=fields)
        df.to_json(self.__users_filename)


    def read_users(self):
        users = []
        try:
            df = pd.read_json(self.__users_filename)
            users = df.to_dict('records')
        except:
            raise Exception('ERROR: users file not found')
        return users