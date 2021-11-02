from VKService import VKService
from Filter import Filter
from FileService import FileService
from GarbageService import GarbageService
import Constants
import time


if __name__ == '__main__':
    start_time = time.time()

    vk = VKService(Constants.fields, Constants.id_range_start, Constants.id_range_end, Constants.requests_number_by_thread)
    file_service = FileService(Constants.users_filename)
    filter = Filter(None, Constants.fields)
    for i in range(Constants.users_files_number): 
        users = vk.get_users_threading()

        filter._Filter__users = users
        users_filtered = filter.get_filtered_users()

        file_service._users_filename = Constants.users_filename + str(i)
        file_service.save_users(users_filtered, file_service._users_filename, Constants.fields)

        GarbageService.delete_variables(users, users_filtered)
   
    for i in range(Constants.users_files_number):
        file_service._users_filename = Constants.users_filename + str(i)
        users = file_service.read_users(file_service._users_filename)
        # Do something with users

    print(time.time() - start_time)
    print()