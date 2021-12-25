import telebot
from config import token
from markup import main_markup, catalog_level_one_markup, catalog_level_two_markup, catalog_level_three_markup
from utils import search_or_save_user, change_money, products_availability
from utils import check_level_items, check_level_four_items, quantity_product_level_three
from utils import level_in_shelve, get_level_one_in_shelve, del_level_one_in_shelve, func_level_sale
from utils import insert_database_products_level_four
from cripto_info import criptoInfo

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    markup = main_markup()
    try:
        search_or_save_user(message.from_user.id, message.from_user.username)
    except:
        search_or_save_user(message.from_user.id)   
    bot.send_message(message.chat.id, 'Hello my frend', reply_markup=markup)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def mail_fucn_store(message):
    chat_id = message.chat.id
    
    if message.text == '📜 Наличие товара':
        bot.send_message(
            chat_id, 
            products_availability());
    elif message.text == '👨‍💼 Профиль':
        try:
            data_user = search_or_save_user(message.from_user.id, message.from_user.username)
        except:
            data_user = search_or_save_user(message.from_user.id)

        string_id = 'Ваш id:\t' + str(data_user[0][1]) + '\n'
        string_name = 'Ваше имя:\t' + str(data_user[0][2]) + '\n'
        string_money = 'У вас на счету:\t' + str(data_user[0][3]) + ' руб' + '\n'
        string_total = 'Количество попупок:\t' + str(data_user[0][4]) + '\n'
        string_data = string_id + string_name + string_money + string_total
        bot.send_message(chat_id, string_data)
    elif message.text == '🗂 Каталог':
        markup_catalog = catalog_level_one_markup()
        bot.send_message(message.chat.id, message.text, reply_markup=markup_catalog)
        bot.register_next_step_handler(message, catalog_level_two)
    elif message.text == '💰 Баланс':
        markup_balance = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        balance = telebot.types.KeyboardButton('Пополнить')
        main_menu = telebot.types.KeyboardButton('В главное меню')
        markup_balance.row(balance, main_menu)
        user_data = search_or_save_user(message.from_user.id, message.from_user.username)
        text_message = 'Ваш баланс: ' + str(user_data[0][3]) + ' руб'
        bot.send_message(message.chat.id, text_message, reply_markup=markup_balance)
        bot.register_next_step_handler(message, choice_from_balance)
    elif message.text == '🆘 Помощь':
        text_message = 'Если возникли проблемы, напишите вот суюда -> @help_sos123'
        bot.send_message(message.chat.id, text_message)
    else:
        markup = main_markup()
        bot.send_message(chat_id, 'Воспользуетесь клавиатурой')
        bot.send_message(chat_id, 'Главное меню', reply_markup=markup)

# /C/
def catalog_level_two(message):
    if message.text == 'В главное меню':
        markup_main = main_markup()
        bot.send_message(message.chat.id, message.text, reply_markup=markup_main)
    else:
        check = check_level_items(message.text, 1)
        if check:
            level_in_shelve(message.from_user.id, message.text)
            markup_level_two = catalog_level_two_markup(message.text)
            bot.send_message(message.chat.id, message.text, reply_markup=markup_level_two)
            bot.register_next_step_handler(message, catalog_level_three)
        elif check == None:
            markup_main = main_markup()
            bot.send_message(message.chat.id, 'Произошла ошибка, попробуйте еще раз', reply_markup=markup_main)
        elif not check:
            markup_main = main_markup()
            bot.send_message(message.chat.id, 'Воспользуеутесь клавиатурой', reply_markup=markup_main)

def catalog_level_three(message):
    if message.text == 'В главное меню':
        del_level_one_in_shelve(message.from_user.id)
        markup_main = main_markup()
        bot.send_message(message.chat.id, message.text, reply_markup=markup_main)
    elif message.text == 'Назад':
        del_level_one_in_shelve(message.from_user.id)
        markup_catalog = catalog_level_one_markup()
        bot.send_message(message.chat.id, message.text, reply_markup=markup_catalog)
        bot.register_next_step_handler(message, catalog_level_two)
    else:
        id_user = message.from_user.id
        check = check_level_items(message.text, 2, id_user)
        if check:
            markup_three = catalog_level_three_markup(message.text, id_user)

            choice_user_level_two = get_level_one_in_shelve(id_user)
            choice_user_level_three = choice_user_level_two + '|' + message.text
            level_in_shelve(id_user, choice_user_level_three)

            bot.send_message(message.chat.id, message.text, reply_markup=markup_three)
            bot.register_next_step_handler(message, catalog_level_four)

        elif check == None:
            del_level_one_in_shelve(message.from_user.id)
            markup_main = main_markup()
            bot.send_message(message.chat.id, 'Произошла ошибка, попробуйте еще раз', reply_markup=markup_main)
        elif not check:
            bot.send_message(message.chat.id, 'Воспользуеутесь клавиатурой')
            bot.register_next_step_handler(message, catalog_level_three)

def catalog_level_four(message):
    id_user = message.from_user.id
    if message.text == 'В главное меню':
        del_level_one_in_shelve(message.from_user.id)
        markup_main = main_markup()
        bot.send_message(message.chat.id, message.text, reply_markup=markup_main)
    elif message.text == 'Назад':
        choice_one_level = get_level_one_in_shelve(message.from_user.id).split('|')
        markup_level_two = catalog_level_two_markup(choice_one_level[0])
        level_in_shelve(id_user, choice_one_level[0])
        bot.send_message(message.chat.id, message.text, reply_markup=markup_level_two)
        bot.register_next_step_handler(message, catalog_level_three)
    else:
        check = check_level_four_items(message.text, id_user)
        if check:
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            menu = telebot.types.KeyboardButton('В главное меню')
            markup.row(menu)
            сhoice_user = (message.text).split('|')
            choice_back_level = get_level_one_in_shelve(message.from_user.id)
            choice_back_level += '|' + сhoice_user[0] + '|'
            level_in_shelve(id_user, choice_back_level)

            bot.send_message(message.chat.id, 'Сколько штук вы хотите купить?', reply_markup=markup)
            bot.register_next_step_handler(message, level_of_sale)

        elif check == None:
            del_level_one_in_shelve(message.from_user.id)
            markup_main = main_markup()
            bot.send_message(message.chat.id, 'Произошла ошибка, попробуйте еще раз', reply_markup=markup_main)
        elif not check:
            bot.send_message(message.chat.id, 'Воспользуеутесь клавиатурой')
            bot.register_next_step_handler(message, catalog_level_four)
            

def level_of_sale(message):
    markup_main = main_markup()
    if message.text == 'В главное меню':
        del_level_one_in_shelve(message.from_user.id)
        bot.send_message(message.chat.id, message.text, reply_markup=markup_main)
    else:
        try:
            check_choice_user_for_number = int(message.text)
            choice_user_quantity_product = quantity_product_level_three(message.from_user.id)

            if check_choice_user_for_number <= choice_user_quantity_product and check_choice_user_for_number > 0:

                product_user = func_level_sale(message.from_user.id, check_choice_user_for_number)

                if product_user == 'money_true':
                    confirmation = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                    menu = telebot.types.KeyboardButton('В главное меню')
                    conf = telebot.types.KeyboardButton('Подтверждаю')
                    confirmation.row(conf)
                    confirmation.row(menu)
                    bot.send_message(message.chat.id, 'Подтвердите вашу покупку', reply_markup=confirmation)
                    bot.register_next_step_handler(message, confirmation_user)

                elif product_user == 'not_money':
                    bot.send_message(message.chat.id, 'У вас не хватает денег на счету', reply_markup=markup_main)
                    del_level_one_in_shelve(message.from_user.id)
                elif product_user == None:
                    insert_database_products_level_four(
                        get_level_one_in_shelve(message.from_user.id),
                    );
                    bot.send_message(message.chat.id, 'Произошла ошибка, попробуйте еще раз', reply_markup=markup_main)
                    del_level_one_in_shelve(message.from_user.id)
            else:
                del_level_one_in_shelve(message.from_user.id)
                bot.send_message(message.chat.id, 'У нас нету такого количества', reply_markup=markup_main)
        except ValueError:
            bot.send_message(message.chat.id, 'Некорректная запись. Введите заново или воспользуетесь клавиатурой')
            bot.register_next_step_handler(message, level_of_sale)

def confirmation_user(message):
    markup_main = main_markup()
    if message.text == 'В главное меню':
        insert_database_products_level_four(
            get_level_one_in_shelve(message.from_user.id),
        );
        del_level_one_in_shelve(message.from_user.id)
        bot.send_message(message.chat.id, message.text, reply_markup=markup_main)
    elif message.text == 'Подтверждаю':
        choice_one_level = get_level_one_in_shelve(message.from_user.id).split('|')
        products_user = choice_one_level[3].split(',')
        str_products = ''
        for product in products_user:
            str_products += product + '\n'
        bot.send_message(message.chat.id, str_products)
        bot.send_message(message.chat.id, 'Спасибо за покупку!', reply_markup=markup_main)

    else:
        bot.send_message(message.chat.id, 'Воспользуетесь клавиатурой')
        bot.register_next_step_handler(message, confirmation_user)
# /C/

# /B/
def choice_from_balance(message):
    if message.text == 'В главное меню':
        markup_main = main_markup()
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=markup_main)
    elif message.text == 'Пополнить':
        payment = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        qiwi_button = telebot.types.KeyboardButton('🥝 QIWI')
        replenishment = telebot.types.KeyboardButton('Пополнение')
        crip_info = telebot.types.KeyboardButton('CRIPTO INFO')
        menu = telebot.types.KeyboardButton('В главное меню')
        back = telebot.types.KeyboardButton('Назад')
        payment.row(qiwi_button)
        payment.row(replenishment)
        payment.row(menu, back, crip_info)
        bot.send_message(message.chat.id, 'Выберете способ оплаты', reply_markup=payment)
        bot.register_next_step_handler(message, choice_of_payment_method)
    else:
        markup_main = main_markup()
        bot.send_message(message.chat.id, 'Воспользуеутесь клавиатурой', reply_markup=markup_main)

def choice_of_payment_method(message):
    markup_main = main_markup()
    if message.text == 'В главное меню':
        text_message = 'Главное меню'
        bot.send_message(message.chat.id, text_message, reply_markup=markup_main)

    elif message.text == 'Назад':
        markup_balance = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        balance = telebot.types.KeyboardButton('Пополнить')
        main_menu = telebot.types.KeyboardButton('В главное меню')
        markup_balance.row(balance, main_menu)

        user_data = search_or_save_user(message.from_user.id, message.from_user.username)
        text_message = 'Ваш баланс: ' + str(user_data[0][3]) + ' руб'

        bot.send_message(message.chat.id, text_message, reply_markup=markup_balance)
        bot.register_next_step_handler(message, choice_from_balance)

    elif message.text == 'Пополнение':
        text_message = 'Введите сумму на которую вы хотите пополнить баланс'

        bot.send_message(message.chat.id, text_message)
        bot.register_next_step_handler(message, refill)

    elif message.text == '🥝 QIWI':
        text_message = 'Главное меню'
        bot.send_message(message.chat.id, text_message, reply_markup=markup_main)
    elif message.text == '** BTC **':
        text_message = 'Главное меню'
        bot.send_message(message.chat.id, text_message, reply_markup=markup_main)
    elif message.text == 'CRIPTO INFO':
        arrCriptoInfo = criptoInfo()
        text_message = ''

        for infoC in arrCriptoInfo:
            text_message += infoC[3] + ' - ' +  infoC[4] + ' $ ' + '\n'

        bot.send_message(message.chat.id, text_message, reply_markup=markup_main)
    else:
        text_message = 'Воспользуйтесь клавиатурой'

        bot.send_message(message.chat.id, text_message)
        bot.register_next_step_handler(message, choice_of_payment_method)

def refill(message):
    try:
        message_int = int(message.text)
        if message_int > 0:
            change_money(message.from_user.id, message_int)
            markup_main = main_markup()
            bot.send_message(message.chat.id, 'Спасибо за пополнение баланса', reply_markup=markup_main)
        else:
            bot.send_message(message.chat.id, 'Возможно вы ошиблись, попробуйте заново')
            bot.register_next_step_handler(message, refill)
    except ValueError:
        bot.send_message(message.chat.id, 'Введите число')
        bot.register_next_step_handler(message, refill)


def refillQIWI(message):
    text_message = 'Главное меню'
    markup_main = main_markup()
    bot.send_message(message.chat.id, text_message, reply_markup=markup_main)



def refillBTC(message):
    text_message = 'Главное меню'
    markup_main = main_markup()
    bot.send_message(message.chat.id, text_message, reply_markup=markup_main)
# /B/


if __name__ == '__main__':
    bot.polling() 
