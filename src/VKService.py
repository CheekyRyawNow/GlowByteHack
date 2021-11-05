from dotenv import load_dotenv
import os
import vk_api
import numpy as np
from VKThread import VKThread
import gc


class VKService:
    def __init__(self, fields, id_start, id_end, requests_number):
        self.fields = fields
        self.id_range_start = id_start
        self.id_range_end = id_end
        self.request_max_users = 10
        # self.requests_number = requests_number
        self.requests_number = 1
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
            # ids = self.__get_random_ids()
            ids = 155909408
            users.extend(vk.users.get(user_ids=ids, fields=self.fields))
        return users

    def get_users_additional(self, users):
        vk = self.__connect_vk()
        for user in users:
            user['counters'] = []
            # user['groups'] = []

            user_object_counters = vk.users.get(user_ids=user['id'], fields='counters')
            # user_object_groups = vk.groups.get(user_id=user['id'], extended=0, filter='publics')

            user['counters'] = user_object_counters[0]['counters']
            # user['groups'] = user_object_groups['items']

            del user_object_counters
            # del user_object_groups
            gc.collect()
        return users

    def update_users(self, users, fields_to_update):
        raise Exception('This block is not finished yet')

    def send_message(self, users):
        vk = self.__connect_vk()
        # a set of messages for every tag (tag_message)
        # a set of messages for gretting_word, comclusion, main_part
        # NLP for names check and processing
        for user in users:
            if user['can_write_private_message'] == 1:
                main_part = None
                greeting = {
                'not_specified': 'Здравствуйте!', 
                'young_people': f'Привет, {user["first_name"]}!',
                'economically_active': f'{user["first_name"]}, добрый день!',
                'nature_age': f'Добрый день, {user["first_name"]}',
                'old_people': f'Шалом, дед!'
                }
                if 'audios' in user['tag']:
                    main_part = 'Купи музыку, бажожьда.'
                elif 'fishing' in user['tag']:
                    main_part = 'Купи удочку, бажожьда.'
                conclusion = {
                'not_specified': 'Еще больше предложений каждую среду', 
                'young_people': 'Подписывайся на новости, чтобы ничего не пропустить',
                'economically_active': 'Группа telegram: @fakeskanretail',
                'nature_age': 'Выгодные предложения на нашем сайте: fakedomain.skam.ru',
                'old_people': 'Не забудьте выпить таблетки!'
                }
                message_to_send = ' '.join((greeting[user['age']], main_part, conclusion[user['age']]))
                vk.messages.send(user_id=user['id'], message=message_to_send)
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