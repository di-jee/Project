import requests
import time

def payment_history_last(my_login, api_access_token, rows_num, next_TxnId, next_TxnDate):
    ses = requests.Session()
    ses.headers['authorization'] = 'Bearer ' + api_access_token  
    parameters = {'rows': rows_num, 'nextTxnId': next_TxnId, 'nextTxnDate': next_TxnDate}
    h = ses.get('https://edge.qiwi.com/payment-history/v2/persons/' + my_login + '/payments', params = parameters)
    return h.json()




mylogin = '79198346466'
api_access_token = '18931f998b38a956beb558218a7d04b3'

# последние 20 платежей
lastPayments = payment_history_last(mylogin, api_access_token, '5','','')
for last in lastPayments['data']:
    if last['comment'] != None:
        print('id - ' + str(last['txnId']))
        print('data - ' + last['date'])
        print('Number - ' + last['account'])
        print(last['sum'])
        print(last['provider'])
        print('Message - ' + last['comment'])
        print()




