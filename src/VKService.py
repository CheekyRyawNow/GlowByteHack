from dotenv import load_dotenv
import os
import vk_api
import numpy as np
from VKThread import VKThread


class VKService:
    def __init__(self, fields, idStart, idEnd, requestsNumber):
        self.fields = fields
        self.id_range_start = idStart
        self.id_range_end = idEnd
        self.request_max_users = 1000
        self.requests_number = requestsNumber
        self.thread_count = 4

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

    def __wait_threads(self, threads):
        for i in range(self.thread_count):
            threads[i].join()

    def __get_full_users_array(self, threads):
        users = []
        for i in range(self.thread_count):
            users.extend(threads[i].users)
        return users

    def __create_and_start_threads(self, threads):
        for i in range(self.thread_count):
            threads.append(VKThread(self.requests_number, self))
            threads[i].start()

    def get_users_threading(self):
        threads = []
        self.__create_and_start_threads(threads)
        self.__wait_threads(threads)
        return self.__get_full_users_array(threads)

    def get_users(self):
        vk = self.__connect_vk()
        users = []
        for i in range(self.requests_number):
            ids = self.__get_random_ids()
            users.extend(vk.users.get(user_ids=ids, fields=self.fields))
        return users
