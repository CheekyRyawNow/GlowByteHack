import time
import datetime

class Filter:
    def __init__(self, users, fields):
        self.__users = users
        self.__fields = fields

    def set_users(self, users):
        self.__users = users

    def get_filtered_users(self):
        self.__users = self.__filter_users()
        return self.__uniform_users()

    def __is_inactive(self, current_date_unix, last_seen_date_unix):
        return (current_date_unix - last_seen_date_unix) / 86400 > 90

    def __is_valid(self, user):
        current_date = int(time.time())
        return 'deactivated' not in user and user['is_closed'] == 0 and 'last_seen' in user \
               and not self.__is_inactive(current_date, user['last_seen']['time'])

    # bdate is date object
    def calculate_age(bdate):
        bdate = bdate.split('.')
        today = datetime.date.today()
        return today.year - int(bdate[2]) - ((today.month, today.day) < (int(bdate[1]), int(bdate[0])))

    def __filter_users(self):
        users_filtered = []
        for user in self.__users:
            if self.__is_valid(user):
                users_filtered.append(user)

        return users_filtered

    def __unify_bdate_field(self, user):
        if 'bdate' in user and len(user['bdate']) < 8:
            user['bdate'] = None

    def __unify_fields(self, user):
        for field in self.__fields:
            if field not in user or not user[field]:
                user[field] = None

    # All objects have the same fields.
    def __uniform_users(self):
        for user in self.__users:
            self.__unify_bdate_field(user)
            self.__unify_fields(user)
        return self.__users
