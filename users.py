# добавить классы
User = \
{
    'name' : None,
    'user_id' : None,
    'items' : [],
    'money' : 100,
    'attack' : 1,
    'defense' : 1,
    'max_hp' : 100,
    'max_mana' : 100,
    'cur_hp' : 100,
    'cur_mana' : 100,
    'head' : None,
    'chest' : None,
    'amulet' : None,
    'weapon' : None,
    'location' : None,
    'exp' : 0,
    'user_state' : 'chilling',
    'mob_id' : None,
}


def create_user(user_id, username):
    user = dict(User)
    user['user_id'] = user_id
    user['name'] = username
    return user

