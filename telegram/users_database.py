import sqlite3 as sql
from config import track_database_users, track_product_database
from products_database import product_database


class sql_lite3:
    ''' main class sqlite3 '''
    def __init__(self, track_database, name_table):
        ''' connection to database '''
        self.connection = sql.connect(track_database)
        self.cursor = self.connection.cursor()
        self.name_table = name_table

    def select_all(self):
        ''' method returns all string table '''
        with self.connection:
            return self.cursor.execute('SELECT * FROM ' + str(self.name_table)).fetchall()

    def len_rows(self):
        ''' method returns all numbers string '''
        arr = self.cursor.execute('SELECT * FROM ' + str(self.name_table)).fetchall()
        return len(arr)

    def close(self):
        ''' close database '''
        self.connection.close()

class sql_users(sql_lite3):
    ''' class heir for table users '''
    def save_user_db(self, user_name, id_user):
        ''' method that saves the user to a table'''
        with self.connection:
            # put all strings in an arr
            arr = self.cursor.execute('SELECT * FROM ' + str(self.name_table)).fetchall()

            id_u = len(arr) + 1
            id_user = str(id_user)
            user_name = user_name
            money_number = '0'
            purch_number = '0'
            params = (id_u, id_user, user_name, money_number, purch_number)
            # I create another user in the talitza
            self.cursor.execute('''INSERT INTO users (id, id_user, nick_name, money_user, total_purch) 
            VALUES (?,?,?,?,?)''', params)

    def search_user(self, id_user):
        ''' 
        user search method in talitsa
        if not found returns None,
        otherwise, it returns this user's string

        '''
        with self.connection:
            user_id = str(id_user)
            data = self.cursor.execute('''SELECT * FROM users WHERE id_user = ''' + user_id).fetchall()

            if not data:
                return None
            else:
                return data

    def change_username(self, id_inc, user_name):
        ''' method for changing nick_name under the given id '''
        with self.connection:
            id_user = id_inc
            nameuser = user_name
            parameters = (nameuser, id_user)
            self.cursor.execute('UPDATE users SET nick_name = ? WHERE id = ?', parameters)
    
    def change_money(self, id_user, money):
        ''' Method for changing money_user under given id_user '''
        with self.connection:
            user_id = str(id_user)
            new_money = money
            data_user = self.cursor.execute('''SELECT * FROM users WHERE id_user = ''' + user_id).fetchall()
            old_money = data_user[0][3]
            user_money = int(old_money) + int(new_money)
            str(user_money)
            parameters = (user_money, user_id)
            self.cursor.execute('UPDATE users SET money_user = ? WHERE id_user = ?', parameters)

    def change_money_user(self, id_user: str, money: int):
        ''' Change string money_user
            id_iser: id user
            money: money
        '''
        try:
            with self.connection:
                user_id = str(id_user)
                user_money = int(money)
                parameters = (
                    user_money,
                    user_id,
                );
                self.cursor.execute('UPDATE users SET money_user = ? WHERE id_user = ?', parameters)
            return True
        except:
            return False

    def change_total_purch(self, id_user: str):
        try:
            sql_product = product_database(track_product_database)
            len_total_purch_user = sql_product.select_purchased_product_user(id_user)
            sql_product.close()
            parameters = (
                len_total_purch_user,
                id_user,
            );
            with self.connection:
                self.cursor.execute(
                    'UPDATE users SET total_purch = ? WHERE id_user = ?',
                    parameters
                );
        except:
            return None


if __name__ == "__main__":
    pass