from VKService import VKService
from Filter import Filter
from FileService import FileService
from GarbageService import GarbageService
from TagService import TagService
import Constants
import time
import gc


def parse_users():
    for i in range(Constants.users_files_number): 
        users = vk.get_users_threading()

        filter.set_users(users)
        users_filtered = filter.get_filtered_users()

        file_service.set_users_filename(Constants.users_filename + str(i))
        file_service.save_users(users_filtered, Constants.fields)

        del users
        del users_filtered
        gc.collect()


def tag_users():
    tag_service = TagService(None)
    for i in range(Constants.users_files_number):
        file_service.set_users_filename(Constants.users_filename + str(i))
        users = file_service.read_users()

        user_counters, user_groups = vk.get_users_additional(users)
        
        # tag_service.set_users(users)
        # users_tagged = tag_service.get_tagged_users()

        # file_service.set_users_filename(file_service.get_users_filename() + '_tagged')
        # file_service.save_users(users_tagged, Constants.fields + Constants.tag)


if __name__ == '__main__':
    start_time = time.time()

    vk = VKService(Constants.fields, Constants.id_range_start, Constants.id_range_end, Constants.requests_number_by_thread)
    file_service = FileService(Constants.users_filename)
    filter = Filter(None, Constants.fields)

    # parse_users()
    tag_users()
    
    print(time.time() - start_time)