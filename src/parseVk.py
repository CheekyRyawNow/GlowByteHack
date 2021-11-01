from VKService import VKService
from Filter import Filter
from FileService import FileService
import Constants


if __name__ == '__main__':
    vk = VKService(Constants.fields, Constants.id_range_start, Constants.id_range_end, Constants.requests_number)
    for i in range(Constants.users_files_number): 
        users = vk.get_users()

        filter = Filter(users, Constants.fields)
        users_filtered = filter.get_filtered_users()

        file_service = FileService(Constants.users_filename + str(i))
        file_service.save_users(users_filtered, file_service._users_filename, Constants.fields)
    
    for i in range(Constants.users_files_number):
        file_service = FileService(Constants.users_filename + str(i))
        users = file_service.read_users(file_service._users_filename)
    print()