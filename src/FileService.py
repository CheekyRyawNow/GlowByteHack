import pandas as pd


class FileService:
    def __init__(self, users_filename):
        self.__users_filename = users_filename

    def save_users(self, users, path_to_save, fields):
        df = pd.DataFrame(users, columns=fields)
        df.to_json(path_to_save)

    def read_users(self, path_to_read):
        df = pd.read_json(path_to_read)
        users = df.to_dict('records')
        return users