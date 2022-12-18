# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import database
import locations
import asyncio
import aioschedule
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import pymongo
from pymongo import MongoClient

BOT_API = "5844677783:AAHFUFqvEBMGvWc6KYPwAIrU1nbaPhqQTfE"
bot = AsyncTeleBot(BOT_API)

@bot.message_handler(commands=['help', 'start'])
async def print_hi(message):
    await bot.reply_to(message, "Hi! Use /start_game <nickname> to start a game. To finish game use /finish_game")

@bot.message_handler(commands=['start_game'])
async def register(message):
    if database.check_user(message.chat.id):
        await bot.reply_to(message, "You already registered. Just play game!")
        return
    msg = message.text.split()
    if len(msg) == 1:
        await bot.reply_to(message, "Use /start_game <nickname> to register account. Enter your nickname")
    else:
        user_id = message.chat.id
        username = ' '.join(msg[1:])
        database.create_user(user_id, username)
        await bot.reply_to(message, "You have created account!")

@bot.message_handler(commands=['location'])
async def location(message):
    if not database.check_user(message.chat.id):
        await bot.reply_to(message, "Register using [/start_game <nickname>]")
        return
    location = database.get_location(message.chat.id)
    ans_string = location['name'] + '\n' + location['enter_msg']
    await bot.reply_to(message, ans_string)

@bot.message_handler(commands=['transitions'])
async def location(message):
    if not database.check_user(message.chat.id):
        await bot.reply_to(message, "Register using [/start_game <nickname>]")
        return
    transitions = database.possible_transitions(message.chat.id)
    ans_string = '\n'.join(transitions)
    await bot.reply_to(message, ans_string)

@bot.message_handler(commands=['goto'])
async def goto(message):
    if not database.check_user(message.chat.id):
        await bot.reply_to(message, "Register using [/start_game <nickname>]")
        return
    msg = message.text.split()
    if len(msg) == 1:
        await bot.reply_to(message, "[/goto <location>]")
        return
    else:
        location = ' '.join(msg[1:])
        response = database.goto(message.chat.id, location)
        if response == 1:
            await bot.reply_to(message, "You can't go to this location or location is unconceivable")
        else:
            new_location = database.get_location(message.chat.id)
            ans_string = "You entered " + new_location['name'] + "\n" + new_location['enter_msg']
            await bot.reply_to(message, ans_string)

@bot.message_handler(commands=['sell'])
async def sell(message):
    if not database.check_user(message.chat.id):
        await bot.reply_to(message, "Register using [/start_game <nickname>]")
        return
    user_id = message.chat.id
    if database.get_location(user_id)['name'] != 'Shop':
        await bot.reply_to(message, "You are not in shop!!!")
        return
    msg = message.text.split()
    if len(msg) == 1:
        await bot.reply_to(message, "Use /sell <item_name>")
    else:
        item_name = ' '.join(msg[1:])
        response = database.sell_item(user_id, item_name)
        if response == 1:
            await bot.reply_to(message, "You have not this item in your inventory")
        else:
            ans_string = "You sold item.\nYour balance now: " + str(database.get_money(user_id))
            ans_string += "\n" + "Your inventory is: " + '; '.join(database.get_items(user_id))
            await bot.reply_to(message, ans_string)

@bot.message_handler(commands=['buy'])
async def sell(message):
    if not database.check_user(message.chat.id):
        await bot.reply_to(message, "Register using [/start_game <nickname>]")
        return
    user_id = message.chat.id
    if database.get_location(user_id)['name'] != 'Shop':
        await bot.reply_to(message, "You are not in shop!!!")
        return
    msg = message.text.split()
    if len(msg) == 1:
        await bot.reply_to(message, "Use /buy <item_name>")
    else:
        item_name = ' '.join(msg[1:])
        response = database.buy_item(user_id, item_name)
        if response == 1:
            await bot.reply_to(message, "You have not enough money")
        else:
            ans_string = "You bought item.\nYour balance now: " + str(database.get_money(user_id))
            ans_string += "\n" + "Your inventory is: " + '; '.join(database.get_items(user_id))
            await bot.reply_to(message, ans_string)

@bot.message_handler(commands=['equip'])
async def sell(message):
    if not database.check_user(message.chat.id):
        await bot.reply_to(message, "Register using [/start_game <nickname>]")
        return
    user_id = message.chat.id
    msg = message.text.split()
    if len(msg) == 1:
        await bot.reply_to(message, "Use /equip <item_name>")
    else:
        item_name = ' '.join(msg[1:])
        if item_name not in database.get_items(user_id):
            await bot.reply_to(message, "You haven't this item")
            return
        database.equip_item(user_id, item_name)
        await bot.reply_to(message, "You equiped " + item_name)

@bot.message_handler(commands=['unequip'])
async def sell(message):
    if not database.check_user(message.chat.id):
        await bot.reply_to(message, "Register using [/start_game <nickname>]")
        return
    user_id = message.chat.id
    msg = message.text.split()
    if len(msg) == 1:
        await bot.reply_to(message, "Use /unequip <item_type>")
    else:
        item_type = ' '.join(msg[1:])
        if item_type not in ['head', 'chest', 'amulet', 'weapon']:
            await bot.reply_to(message, "Incorrect item_type")
            return
        database.unequip_item(user_id, item_type)
        await bot.reply_to(message, "You unequiped " + item_type)

@bot.message_handler(commands=['fashion'])
async def fashion(message):
    if not database.check_user(message.chat.id):
        await bot.reply_to(message, "Register using [/start_game <nickname>]")
        return
    user_id = message.chat.id
    ans_string = '\n'.join(database.get_equiped_items(user_id))
    await bot.reply_to(message, ans_string)

@bot.message_handler(commands=['stats'])
async def stats(message):
    if not database.check_user(message.chat.id):
        await bot.reply_to(message, "Register using [/start_game <nickname>]")
        return
    user_id = message.chat.id
    ans_string = ""
    for key, val in database.get_stats(user_id).items():
        ans_string += str(key) + " : " + str(val) + "\n"
    await bot.reply_to(message, ans_string)


@bot.message_handler(commands=['check_db'])
async def check(message):
    database.check_db()
    await bot.reply_to(message, "Hooray")

async def scheduler():
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(bot.infinity_polling(), scheduler())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())







"""
mongodb+srv://Test123:Test123@cluster0.bd7x4ih.mongodb.net/?retryWrites=true&w=majority
"""
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
