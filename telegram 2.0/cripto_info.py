import requests
from bs4 import BeautifulSoup
import fake_useragent


def criptoInfo():
	criptoArray = []

	url = 'https://ru.investing.com/crypto/'
	user = fake_useragent.UserAgent().random
	header = {'user-agent': user}

	responce = requests.get(url, headers=header).text
	soup = BeautifulSoup(responce, 'lxml')
	t_body = soup.find('tbody')

	get_i = t_body.find_all('tr')
	for info in get_i:
		infoCripto = info.text.split('\n')
		criptoArray.append(infoCripto)

	return criptoArray



if __name__ == '__main__':
	pass
