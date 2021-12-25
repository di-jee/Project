from telebot import types
from products_database import product_database
from config import track_product_database
from utils import get_level_one_in_shelve

def main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    catalog = types.KeyboardButton('🗂 Каталог')
    tovar = types.KeyboardButton('📜 Наличие товара')
    balans = types.KeyboardButton('💰 Баланс')
    profile = types.KeyboardButton('👨‍💼 Профиль')
    help_store = types.KeyboardButton('🆘 Помощь')
    markup.row(catalog, tovar)
    markup.row(help_store, profile, balans)
    return markup

def catalog_level_one_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu = types.KeyboardButton('В главное меню')
    markup.row(menu)
    try:
        sql = product_database(track_product_database)
        data_level_one = sql.select_all('ab_level_one')
        sql.close()

        for data in data_level_one:
            markup.row(data[1])

        return markup
    except:
        return markup


def catalog_level_two_markup(message_text):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu = types.KeyboardButton('В главное меню')
    back = types.KeyboardButton('Назад')
    markup.row(back, menu)
    try:
        sql = product_database(track_product_database)
        data_level_two = sql.select_level_two_item(message_text)
        sql.close()
        for data in data_level_two:
            markup.row(data[2])

        return markup
    except:
        return markup

def catalog_level_three_markup(message_text, id_user):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu = types.KeyboardButton('В главное меню')
    back = types.KeyboardButton('Назад')
    markup.row(back, menu)


    item_level_one = get_level_one_in_shelve(str(id_user))
    try: 
        sql = product_database(track_product_database)
        data_three = sql.product_availability(item_level_one)
        data_level = []
        for item in data_three:
            if message_text == item[1]:
                items_level_four_name_product = sql.select_level_four(item[0])
                len_items_level_four_name_product = len(items_level_four_name_product)
                sql.level_three_change_quantity_products(len_items_level_four_name_product, item[0])
                if len_items_level_four_name_product <= 0:
                    pass
                else:
                    markup.row(
                        item[0] + '|' +item[1] + '|' + str(item[2]) + 'руб|' + str(len_items_level_four_name_product) + 'шт'
                    );

        sql.close()
        return markup
    except:
        return markup


if __name__ == "__main__":
    pass