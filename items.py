# по-хорошему закинуть всё это в MongoDB в коллекцию items. Очевидно, что это легко сделать (тут просто словари лежат, которые отлично принимаются MongoDB).
# но время ожидания ответа возрастает, поэтому сделал так

Sword = \
{
    'name' : 'Sword',
    'type' : 'weapon',
    'attack' : 10,
    'cost_to_buy' : 10,
    'cost_to_sell' : 3,
}
BreastPlate = \
{
    'name' : 'BreastPlate',
    'type' : 'chest',
    'defense' : 10,
    'cost_to_buy' : 10,
    'cost_to_sell' : 3,
}
KeanuReevesShades = \
{
    'name' : 'KeanuReevesShades',
    'type' : 'head',
    'attack' : 100,
    'defense' : 100,
    'max_hp' : 100,
    'max_mana' : 100,
    'cost_to_buy' : 1337,
    'cost_to_sell' : 0,
}
AmuletSchoolOfWolf = \
{
    'name' : 'AmuletSchoolOfWolf',
    'type' : 'amulet',
    'max_hp' : 50,
    'max_mana' : -50,
    'cost_to_buy' : 100,
    'cost_to_sell' : 10,
}
MerchantAmulet = \
{
    'name': 'MerchantAmulet',
    'type' : 'amulet',
    'max_hp' : -99,
    'max_mana' : -99,
    'cost_to_buy' : 1,
    'cost_to_sell' : 100,
}

items_dict = \
{
    'MerchantAmulet' : MerchantAmulet,
    'AmuletSchoolOfWolf' : AmuletSchoolOfWolf,
    'KeanuReevesShades' : KeanuReevesShades,
    'BreastPlate' : BreastPlate,
    'Sword' : Sword,
}