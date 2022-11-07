class User:

	def __init__(self, id_user, balance=0):
		self.__id_user = id_user
		self.__balance = balance # get from database

	def __del__(self):
		pass

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

	@classmethod
	def __check_other_for_bool(cls, other):
		if not isinstance(other, (int, User)):
			raise TypeError('Other not int or User')

		return other if isinstance(other, int) else other.__balance

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

	# __eq__ ==
	# __ne__ !=
	# __lt__ <
	# __gt__ >
	# __le__ <=
	# __ge__ >=
	# методы работают в обратном порядке

	# переопределяем метод сравнения
	# можно написать только метод __eq__ все равно будет работать
	# ==
	def __eq__(self, other):
		oth = self.__check_other_for_bool(other)
		return self.__balance == oth

	def __ne__(self, other):
	 	oth = self.__check_other_for_bool(other)
	 	return self.__balance != oth

	# <
	def __lt__(self, other):
		oth = self.__check_other_for_bool(other)
		return self.__balance < oth

	# >
	def __gt__(self, other):
		oth = self.__check_other_for_bool(other)
		return self.__balance > oth

	# <=
	def __le__(self, other):
		oth = self.__check_other_for_bool(other)
		return self.__balance <= oth

	# >=
	def __ge__(self, other):
		oth = self.__check_other_for_bool(other)
		return self.__balance >= oth