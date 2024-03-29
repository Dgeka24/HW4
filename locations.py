# по-хорошему закинуть всё это в MongoDB в коллекцию locations. Очевидно, что это легко сделать (тут просто словари лежат, которые отлично принимаются MongoDB).
# но время ожидания ответа возрастает, поэтому сделал так
City = \
{
    'name' : 'City',
    'transitions' : ['Shop', 'Dungeon'],
    'enter_msg' : 'You are in city'
}
Shop = \
{
    'name' : 'Shop',
    'transitions' : ['City'],
    'enter_msg' : 'You are in shop. Buy items by [/buy <item_name>] and sell by [/sell <item_name>]'
}
Dungeon = \
{
    'name' : 'Dungeon',
    'transitions' : ['City'],
    'enter_msg' : 'You are in Dungeon. Type [/fight] to fight',
}
locations_dict = \
{
    'Shop' : Shop,
    'City' : City,
    'Dungeon' : Dungeon,
}