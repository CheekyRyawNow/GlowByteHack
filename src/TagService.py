from Filter import Filter

class TagService:
    @staticmethod
    def get_tagged_users(users):
        user_age = 0
        for user in users:
            user['tag'] = []
            if user['bdate'] != None:
                user['tag']['age'] = None
                user_age = Filter.calculate_age(user['bdate'])
                user['tag']['age'] = 'not_specified'
                if 15 <= user_age <= 24:
                    user['tag']['age'] = 'young_people'
                elif 25 <= user_age <= 44:
                    user['tag']['age'] = 'economically_active'
                    if user['sex'] == 1:
                        user['tag'].append('motherhood')
                elif 45 <= user_age <= 60:
                    user['tag']['age'] = 'mature_age'
                elif user_age > 60:
                    user['tag']['age'] = 'old_people'
                if user['sex'] == 2 and 17 <= user_age <= 27:
                    user['tag'].append('army')
                if user_age > 35:
                    user['tag'].append('credit')
                    if user['sex'] == 2:
                        user['tag'].append('fishing')
                        user['tag'].append('hunting')
            if user['last_seen'] != None:
                if 'platform' in user['last_seen']:
                    if user['last_seen']['platform'] != 7:
                        user['tag'].append('mobile')
                    else:
                        user['tag'].append('desktop')
            if user['relation'] == 1 or user['relation'] in range(5, 7):
                user['tag'].append('love_search')
            elif user['relation'] != 0:
                user['tag'].append('love_in')
            if user['counters']['audios'] > 100:
                user['tag'].append('audios')
            if user['counters']['videos'] > 100:
                user['tag'].append('videos')
            if user['counters']['photos'] > 100:
                user['tag'].append('photos')
        return users