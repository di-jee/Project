class User:

	def __init__(self, id_user, name, balance: int):
		self._id_user = id_user
		self._name = name
		if balance < 0:
			raise ValueError(f'Balance > 0')
		self._balance = balance # запрос к базе данных

	@classmethod
	def __get_money_add(cls, oth):
		if not isinstance(oth, (int, User)):
			raise ValueError('Other don`t int or Human')

		# если oth явл. экземпляром класса Human, то берем его баланс
		# этим мы можем реализовать перевод денег от одного человека к другому
		money = oth
		if isinstance(oth, User):
			# достаем деньги другого Human
			money = oth._balance
			# минусуем их у него, мы же переводим их
			oth._balance -= money
		# возвращаем кол-во денег юзера
		return money

	@classmethod
	def __get_money_sub(cls, oth, balance):
		# проверяем что пользователь ввел число
		if not isinstance(oth, int):
			raise ValueError('Other don`t int')

		# проверяем что бы число не привышало баланс
		if balance < oth:
			raise ValueError(f'you don`t have enough money: {balance}')

		return oth

	# сложение
	def __add__(self, other):
		money = self.__get_money_add(other)
		# возвращаем новый объект с новым балансом
		return User(self._id_user, self._name, self._balance + money)

	# если переменные были прописаны в другом порядке
	def __radd__(self, other):
		return self + other

	# метод для сокращения +=
	def __iadd__(self, other):
		money = self.__get_money_add(other)
		self._balance += money

		return self

	# вычитание
	def __sub__(self, other):
		money = self.__get_money_sub(other, self._balance)
		return User(self._id_user, self._name, self._balance - money)

	def __rsub__(self, other):
		return self - other

	def __isub__(self, other):
		money = self.__get_money_sub(other, self._balance)
		self._balance -= money

		return self