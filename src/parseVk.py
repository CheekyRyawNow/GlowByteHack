from VKService import VKService
from Filter import Filter
from FileService import FileService

FIELDS = [
    'id',
    'first_name',
    'last_name',
    'bdate',
    'sex',
    'last_seen',
    'can_write_private_message',
    'country',
    'city',
    'relation'
]

if __name__ == '__main__':
    vk = VKService(FIELDS, 1000000, 50000000, 2)
    users = vk.get_users()

    filter = Filter(users, FIELDS)
    users_filtered = filter.get_filtered_users()

    file_service = FileService('../users.csv')
    file_service.save_users(users_filtered, file_service._users_filename, FIELDS)
    users = file_service.read_users(file_service._users_filename)