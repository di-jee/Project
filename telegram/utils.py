from config import token, track_database_users, table_track_database_users, shelve_way
from config  import track_product_database
from users_database import sql_users
from products_database import product_database
import time
import shelve
from config import shelve_way


def products_availability():
    try:
        sql = product_database(track_product_database)
        data_level_one = sql.select_all('ab_level_one')
        string_product = ''
        for data in data_level_one:
            data_level_three = sql.product_availability(data[1])

            i = 0
            for data_three in data_level_three:
                if data_three[3] > 0:
                    i += 1

            if i == 0:
                    continue
            else:
                string_product += ' *** ' + str(data[1]) + ' *** ' + '\n'
                for data_three in data_level_three:
                    if data_three[3] > 0:
                        string_product += str(data_three[0]) + ' | ' + str(data_three[1]) + ' | ' + str(data_three[2]) + ' руб | ' + str(data_three[3]) + ' шт\n'

        sql.close()
        if string_product == '':
            return 'В данный момент товара нету'
        else:
            return string_product
    except:
        return 'Произошла ошибка, попробуйте еще раз'


def save_user(user_name, id_user):
    sql = sql_users(track_database_users, table_track_database_users)
    sql.save_user_db(user_name, id_user)
    sql.close()


def search_users(id_user):
    sql = sql_users(track_database_users, table_track_database_users)
    data = sql.search_user(id_user)
    sql.close()
    return data


def change_name(id_inc, user_name):
    sql = sql_users(track_database_users, table_track_database_users)
    sql.change_username(id_inc, user_name)
    sql.close()


def change_money(id_user, money):
    sql = sql_users(track_database_users, table_track_database_users)
    sql.change_money(id_user, money)
    sql.close()


def search_or_save_user(id_user, user_name = None):
    sql = sql_users(track_database_users, table_track_database_users)
    sql.change_total_purch(id_user)
    check_user = sql.search_user(id_user)
    if not check_user:
        if not user_name:
            sql.save_user_db(id_user, id_user)
        else:
            sql.save_user_db('@' + user_name, id_user)
    elif check_user[0][1] == check_user[0][2]:
        if not user_name:
            pass
        else:
            sql.change_username(check_user[0][0], '@' + user_name)
    elif check_user[0][1] != check_user[0][2]:
        if not user_name:
            sql.change_username(check_user[0][0], id_user)
        elif check_user[0][2] != user_name:
            sql.change_username(check_user[0][0], '@' + user_name)
    data_user = sql.search_user(id_user)
    sql.close()
    return data_user


def check_level_items(text_message, level, id_user=None):
    try:
        level = int(level)
        sql = product_database(track_product_database)
        if level == 1:
            data_level = sql.select_all('ab_level_one')
        elif level == 2:
            item_level_one = get_level_one_in_shelve(str(id_user))
            data_three = sql.product_availability(item_level_one)
            data_level = []
            for item in data_three:
                if text_message == item[1]:
                    data_level.append(item)
        sql.close()

   
        flag = False
        for data in data_level:
            if text_message == data[1]:
                flag = True
                break

        return flag
    except:
        return None


def check_level_four_items(text_message, id_user):
    try:
        sql = product_database(track_product_database)
        item_level_one = get_level_one_in_shelve(str(id_user)).split('|')
        data_three = sql.product_availability(item_level_one[0])
        sql.close()


        flag = False
        for item in data_three:
            str_item = item[0] + '|' +item[1] + '|' + str(item[2]) + 'руб|' + str(item[3]) + 'шт'
            if text_message == str_item:
                flag = True
                break

        return flag
    except:
        return None
    
    
def level_in_shelve(user_id, message_text):
    try:
        with shelve.open(shelve_way) as storage:
            storage[str(user_id)] = message_text
    except:
        return None

def get_level_one_in_shelve(user_id):
    try:
        with shelve.open(shelve_way) as storage:
            product_name = storage[str(user_id)]
        return product_name
    except:
        return None


def del_level_one_in_shelve(user_id):
    try:
        with shelve.open(shelve_way) as storage:
            del storage[str(user_id)]
    except:
        return None


def quantity_product_level_three(id_user):
    try:
        sql = product_database(track_product_database)
        choice_user = get_level_one_in_shelve(id_user).split('|')
        all_product_one_level = sql.product_availability(choice_user[0])
        sql.close()
        number = 0
        for product in all_product_one_level:
            if product[0] == choice_user[2]:
                number = product[3]
                break

        return number
    except:
        return None


def func_level_sale(id_user, quantity_product_choice_user):
    try:
        sql_products = product_database(track_product_database)
        sql_user = sql_users(track_database_users, table_track_database_users)
        time.sleep(0.2)
        choice_user = get_level_one_in_shelve(id_user)
        choice_user_for_purchased_product = choice_user
        choice_user = choice_user.split('|')

        product_level_three = sql_products.product_availability(choice_user[0])
        product_price = None
        time.sleep(0.1)
        for product in product_level_three:
            if product[0] == choice_user[2]:
                product_price = int(product[2])
                break

        final_amount = product_price * quantity_product_choice_user
        data_user = sql_user.search_user(id_user)
        time.sleep(0.2)
        quantity_money_user = int(data_user[0][3])
        if quantity_money_user >= final_amount:
            items_level_four_name_product = sql_products.select_level_four(choice_user[2])
            len_items_level_four_name_product = len(items_level_four_name_product) - 1
            product_for_user = []

            for i in range(len_items_level_four_name_product, len_items_level_four_name_product-quantity_product_choice_user, -1):
                
                item_for_user = sql_products.delete_product_level_four(
                    items_level_four_name_product[i][0]
                );

                change_shel = get_level_one_in_shelve(
                    id_user
                );
                change_shel += item_for_user[0][1] + ','
                level_in_shelve(id_user, change_shel)

                sql_products.insert_purchased_product(
                    id_user, 
                    item_for_user[0][1],
                    choice_user_for_purchased_product,
                    time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
                );


            write_off_money = quantity_money_user - final_amount
            sql_user.change_money_user(id_user, write_off_money)
            sql_products.close()
            sql_user.close()


            return 'money_true'
        elif quantity_money_user < final_amount:
            sql_products.close()
            sql_user.close()
            return 'not_money'
    except:
        return None


def insert_database_products_level_four(user_way: str):
    sql_products = product_database(track_product_database)

    user_way = user_way.split('|')
    name_category = user_way[0]
    name_subcategory = user_way[1]
    name_product = user_way[2]

    all_product = user_way[3].split(',')

    len_all_product = len(all_product) - 1
    i = 0
    while i < len_all_product:
        sql_products.insert_into_level_four(
            all_product[i],
            name_product,
            name_subcategory,
            name_category,
        );
        i += 1

    sql_products.close()



if __name__ == "__main__":
    pass





