from dotenv import load_dotenv
import os
import vk_api
import numpy as np


class VKService:
    def __init__(self, fields, idStart, idEnd, requestsNumber):
        self.fields = fields
        self.id_range_start = idStart
        self.id_range_end = idEnd
        self.request_max_users = 1000
        self.requests_number = requestsNumber

        load_dotenv()
        self.__login = os.getenv('LOGIN')
        self.__password = os.getenv('PASSWORD')

    def __connect_vk(self):
        vk_session = vk_api.VkApi(self.__login, self.__password)
        vk_session.auth(token_only=True)
        vk = vk_session.get_api()
        return vk

    def __get_random_ids(self):
        ids = []
        for j in range(self.request_max_users):
            ids.append(np.random.randint(self.id_range_start, self.id_range_end))
        return ids

    def get_users(self):
        vk = self.__connect_vk()

        users = []
        for i in range(self.requests_number):
            ids = self.__get_random_ids()
            users.extend(vk.users.get(user_ids=ids, fields=self.fields))

        return users