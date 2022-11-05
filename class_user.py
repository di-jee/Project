class User:

	def __init__(self, id_user, balance=0):
		self.__id_user = id_user
		self.__balance = balance # get from database

	def __del__(self):
		print('close database')

	@classmethod
	def __check_other(cls, other, balance=None):
		# проверяем что other это int
		if not isinstance(other, int):
			raise TypeError(f'Other not int: {other}')

		# проверка для вычитания
		# если other > balance, то на балансе недостаточно средств
		if balance != None and other > balance:
			if other > balance:
				raise ValueError(f'Other < balance: {other}')

		return other

	# сложение
	def __add__(self, other):
		money = self.__check_other(other)
		self.__balance += money

		# не предпологается сложение или вычитание объектов типа User
		# по-этому возвращаем этот же экземпляр
		return self

	def __radd__(self, other):
		return self + other

	def __iadd__(self, other):
		money = self.__check_other(other)
		self.__balance += money

		return self

	# вычитание
	def __sub__(self, other):
		money = self.__check_other(other, self.__balance)
		self.__balance -= money

		return self

	def __rsub__(self, other):
		return self - other

	def __isub__(self, other):
		money = self.__check_other(other, self.__balance)
		self.__balance -= money

		return self