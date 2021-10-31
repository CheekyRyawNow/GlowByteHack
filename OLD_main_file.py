#Not in use right now

def tag_users(users):
    user_age = 0
    for user in users:
        user['tag'] = []
        if user['is_closed']:
            user['tag'].append('Security')
        else:
            if user['bdate'] != None:
                user_age = calculate_age(user['bdate'])
                if user['sex'] == 2 and user_age in range(17, 28):
                    user['tag'].append('Army')
                elif user['sex'] == 1 and user_age in range(23, 41):
                    user['tag'].append('Motherhood')
                if user_age < 40:
                    user['tag'].append('Games')
                if user_age > 60:
                    user['tag'].append('Old_people')
                if user_age > 35:
                    user['tag'].append('Credit')
                    if user['sex'] == 2:
                        user['tag'].append('Fishing')
                        user['tag'].append('Hunting')
            if user['last_seen'] != None:
                if 'platform' in user['last_seen']:
                    if user['last_seen']['platform'] != 7:
                        user['tag'].append('Mobile')
                    else:
                        user['tag'].append('Desktop')
            if user['relation'] == 1 or user['relation'] in range(5, 7):
                user['tag'].append('Love_search')
            elif user['relation'] != 0:
                user['tag'].append('Love_in')
            if user['books'] != None:
                user['tag'].append('Books')
    return users

# DD.MM.YYYY string
def calculate_age(bdate):
    bdate = bdate.split('.')
    today = datetime.date.today()
    return today.year - int(bdate[2]) - ((today.month, today.day) < (int(bdate[1]), int(bdate[0])))