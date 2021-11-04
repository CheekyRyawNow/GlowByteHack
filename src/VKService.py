from dotenv import load_dotenv
import os
import vk_api
import numpy as np
from VKThread import VKThread
from Filter import Filter


class VKService:
    def __init__(self, fields, id_start, id_end, requests_number):
        self.fields = fields
        self.id_range_start = id_start
        self.id_range_end = id_end
        self.request_max_users = 1000
        self.requests_number = requests_number
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

    def get_users_additional(self, users):
        vk = self.__connect_vk()
        users_new = []
        for user in users:
            users_new.append(vk.users.get(user_ids=user['id'], fields=self.fields))
            # groups.get
        return users_new

    def update_users(self, users, fields_to_update):
        raise Exception('This block is not finished yet')

    def send_message(self, users):
        user_age = 0
        greeting_word = None
        main_part = None 
        conclusion = None
        # a set of messages for every tag (tag_message)
        # a set of messages for gretting_word, comclusion, main_part
        # NLP for names check and processing
        for user in users:
            if user['can_send_private_message'] == 1:
                if user['bdate'] != None:
                    print()
                    # user_age = Filter.calculate_age()
                    # <= 27:
                    #   greeting_word = Привет, %first_name%
                    #   conclusion = что-нибудь для зумеров
                    # 28-60:
                    #   greeting_word = %first_name%!
                    #   conclusion = что-нибудь молодежное крутецкое
                    # > 60
                    #   greeting_word = Здравствуйте, %frist_name%
                    #   conclusion = С наилучшими пожеланиями, %company_name%
                    # Not specified:
                    #   greeting_word = Здравствуйте!
                # for tag in user['tag']:
                #   main.part = main.part + tag_message[tag] -- not +, but join()
        return ''.join(greeting_word, main_part, conclusion)