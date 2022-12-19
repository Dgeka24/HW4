import items
import locations
import mobs
import users
import pymongo
import random
from pymongo import MongoClient
cluster = MongoClient('mongodb+srv://Test123:Test123@cluster0.bd7x4ih.mongodb.net/?retryWrites=true&w=majority')

def check_user(user_id):
    db = cluster['DB']
    collection = db['users']
    return len(list(collection.find({'user_id' : user_id}))) > 0

def create_user(user_id, username):
    db = cluster['DB']
    collection = db['users']
    user = dict(users.User)
    user['user_id'] = user_id
    user['name'] = username
    user['location'] = 'City'
    collection.insert_one(user)

def get_user(user_id):
    db = cluster['DB']
    collection = db['users']
    user = collection.find_one({'user_id': user_id})
    return user

def get_location(user_id):
    user = get_user(user_id)
    current_location = user['location']
    return locations.locations_dict[current_location]

def get_money(user_id):
    user = get_user(user_id)
    return user['money']

def get_items(user_id):
    user = get_user(user_id)
    return user['items']

def possible_transitions(user_id):
    current_location = get_location(user_id)
    cur_loc = locations.locations_dict[current_location['name']]
    return cur_loc['transitions']

def restore_hp(user_id, amount=10000000000):
    user = get_user(user_id)
    stats = get_stats(user_id)
    amount = min(amount, stats['max_hp'] - stats['cur_hp'])
    db = cluster['DB']
    collection = db['users']
    collection.delete_one(user)
    user['cur_hp'] += amount
    collection.insert_one(user)

def restore_mana(user_id, amount=10000000000):
    user = get_user(user_id)
    stats = get_stats(user_id)
    amount = min(amount, stats['max_mana'] - stats['cur_mana'])
    db = cluster['DB']
    collection = db['users']
    collection.delete_one(user)
    user['cur_mana'] += amount
    collection.insert_one(user)

def goto(user_id, location_name):
    user = get_user(user_id)
    current_location = get_location(user_id)
    if location_name in current_location['transitions']:
        db = cluster['DB']
        collection = db['users']
        collection.delete_one(user)
        user['location'] = location_name
        collection.insert_one(user)
        if location_name == 'City':
            restore_hp(user_id)
            restore_mana(user_id)
        return 0
    else:
        return 1

def sell_item(user_id, item_name):
    user = get_user(user_id)
    if item_name not in user['items']:
        return 1
    else:
        db = cluster['DB']
        collection = db['users']
        collection.delete_one(user)
        user['money'] += items.items_dict[item_name]['cost_to_sell']
        user['items'].remove(item_name)
        collection.insert_one(user)
        return 0

def buy_item(user_id, item_name):
    user = get_user(user_id)
    item = items.items_dict[item_name]
    price = item['cost_to_buy']
    if user['money'] < price:
        return 1
    else:
        db = cluster['DB']
        collection = db['users']
        collection.delete_one(user)
        user['money'] -= price
        user['items'].append(item_name)
        collection.insert_one(user)
        return 0

def equip_item(user_id, item_name):
    user = get_user(user_id)
    item = items.items_dict[item_name]
    db = cluster['DB']
    collection = db['users']
    collection.delete_one(user)
    user['items'].remove(item_name)
    if user[item['type']] is not None:
        user['items'].append(user[item['type']])
    user[item['type']] = item_name
    collection.insert_one(user)
    restore_mana(user_id, 0)
    restore_hp(user_id, 0)

def unequip_item(user_id, item_type):
    user = get_user(user_id)
    db = cluster['DB']
    collection = db['users']
    collection.delete_one(user)
    if user[item_type] is not None:
        user['items'].append(user[item_type])
    user[item_type] = None
    collection.insert_one(user)
    restore_mana(user_id, 0)
    restore_hp(user_id, 0)

def get_equiped_items(user_id):
    user = get_user(user_id)
    ans = []
    for item_type in ['weapon', 'head', 'chest', 'amulet']:
        ans.append(item_type + " : " + str(user[item_type]))
    return ans

def get_stats(user_id):
    user = get_user(user_id)
    ans = {}
    for stat_type in ['attack', 'defense', 'max_hp', 'max_mana', 'cur_hp', 'cur_mana']:
        ans[stat_type] = user[stat_type]
        for item_type in ['weapon', 'head', 'chest', 'amulet']:
            item_name = user[item_type]
            if item_name is not None:
                item = items.items_dict[item_name]
                ans[stat_type] += item.get(stat_type, 0)
    return ans

def create_mob(user_id):
    mob_type = random.choice(mobs.mob_list)
    mob = dict(mob_type)
    mob['user_id'] = user_id
    db = cluster['DB']
    collection = db['mobs']
    collection.insert_one(mob)
    user = get_user(user_id)
    collection_user = db['users']
    collection_user.delete_one(user)
    user['user_state'] = 'fighting'
    user['mob_id'] = collection.find_one(mob)['_id']
    collection_user.insert_one(user)
    return mob

def get_mob(user_id):
    user = get_user(user_id)
    db = cluster['DB']
    collection = db['mobs']
    mob = collection.find_one({'_id' : user['mob_id']})
    return mob

def stop_fight(user_id):
    db = cluster['DB']
    collection_users = db['users']
    collection_mobs = db['mobs']
    user = get_user(user_id)
    mob_id = user['mob_id']
    collection_mobs.delete_one({'_id' : mob_id})
    collection_users.delete_one(user)
    user['user_state'] = 'chilling'
    user['mob_id'] = None
    collection_users.insert_one(user)

def calc_harm(attack, defense):
    return max(0, attack - defense)

def attack(user_id):
    # 0 - attacked, 1 - killed mob, 2 - killed player
    db = cluster['DB']
    collection_users = db['users']
    collection_mobs = db['mobs']
    user = get_user(user_id)
    mob = collection_mobs.find_one({'_id' : user['mob_id']})
    stats = get_stats(user_id)
    collection_mobs.delete_one(mob)
    collection_users.delete_one(user)
    mob['cur_hp'] -= calc_harm(stats['attack'], mob['defense'])
    if mob['cur_hp'] <= 0:
        collection_users.insert_one(user)
        collection_mobs.insert_one(mob)
        return 1
    user['cur_hp'] -= calc_harm(mob['attack'], stats['defense'])
    if user['cur_hp'] <= 0:
        collection_users.insert_one(user)
        collection_mobs.insert_one(mob)
        return 2
    collection_users.insert_one(user)
    collection_mobs.insert_one(mob)
    return 0

def kill_mob(user_id):
    user = get_user(user_id)
    mob = get_mob(user_id)
    db = cluster['DB']
    collection_users = db['users']
    collection_users.delete_one(user)
    user['exp'] += mob['exp']
    collection_users.insert_one(user)
    stop_fight(user_id)

def kill_player(user_id):
    user = get_user(user_id)
    db = cluster['DB']
    collection_users = db['users']
    collection_users.delete_one(user)

def check_db():
    db = cluster['DB']
    collection = db['users']
    print(cluster.list_database_names())
    return True