# ============================================
# ООП (Объектно-Ориентированное Программирование) в Python
# ============================================

# ООП — это подход, где программа строится из "объектов".
# Объект = данные (атрибуты) + действия (методы), объединённые вместе.

# ------------------------------------------------------------
# 1. КЛАСС (class) — это "чертёж" или "шаблон" для создания объектов.
#    Объект (экземпляр) — конкретный представитель класса.
# ------------------------------------------------------------

class Dog:
    # Атрибут класса — общий для всех объектов этого класса
    species = "Canis familiaris"

    # __init__ — конструктор. Вызывается автоматически при создании объекта.
    # self — ссылка на сам объект (обязательный первый параметр).
    def __init__(self, name, age):
        # Атрибуты экземпляра — принадлежат конкретному объекту
        self.name = name
        self.age = age

    # Метод — функция, которая принадлежит классу
    def bark(self):
        return f"{self.name} говорит: Гав-гав!"

    def get_info(self):
        return f"{self.name}, {self.age} лет, порода: {self.species}"


# Создаём объекты (экземпляры) класса Dog
dog1 = Dog("Бобик", 3)
dog2 = Dog("Шарик", 5)

print("=== 1. КЛАССЫ И ОБЪЕКТЫ ===")
print(dog1.get_info())
print(dog2.get_info())
print(dog1.bark())
print()

# ------------------------------------------------------------
# 2. НАСЛЕДОВАНИЕ (inheritance)
#    Новый класс может "унаследовать" всё от родительского класса
#    и добавить/изменить что-то своё.
# ------------------------------------------------------------

class Puppy(Dog):  # Puppy наследует всё от Dog
    def __init__(self, name, age, training_level):
        # super() вызывает конструктор родительского класса
        super().__init__(name, age)
        self.training_level = training_level

    # Переопределяем (override) метод родителя
    def bark(self):
        return f"{self.name} пищит: тяв-тяв!"

    # Добавляем новый метод
    def train(self):
        self.training_level += 1
        return f"{self.name} тренируется! Уровень: {self.training_level}"


puppy = Puppy("Малыш", 1, 0)
print("=== 2. НАСЛЕДОВАНИЕ ===")
print(puppy.get_info())   # метод унаследован от Dog
print(puppy.bark())       # переопределённый метод
print(puppy.train())
print()

# ------------------------------------------------------------
# 3. ИНКАПСУЛЯЦИЯ (encapsulation)
#    Скрытие внутренних данных. В Python нет строгих модификаторов,
#    но есть соглашения:
#      _атрибут  — "защищённый" (не трогать снаружи)
#      __атрибут — "приватный" (Python искажает имя)
# ------------------------------------------------------------

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # приватный атрибут

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return f"Пополнено на {amount}. Баланс: {self.__balance}"
        return "Сумма должна быть положительной"

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
            return f"Снято {amount}. Баланс: {self.__balance}"
        return "Недостаточно средств"

    # Геттер — безопасный способ получить значение
    def get_balance(self):
        return self.__balance


account = BankAccount("Иван", 1000)
print("=== 3. ИНКАПСУЛЯЦИЯ ===")
print(account.deposit(500))
print(account.withdraw(200))
print(f"Баланс через геттер: {account.get_balance()}")
# print(account.__balance)  # Ошибка! Приватный атрибут недоступен снаружи
print()

# ------------------------------------------------------------
# 4. ПОЛИМОРФИЗМ (polymorphism)
#    Разные классы могут иметь методы с одинаковым именем,
#    но работать по-разному.
# ------------------------------------------------------------

class Cat:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} говорит: Мяу!"


class Cow:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} говорит: Му-у!"


# Один и тот же вызов .speak() работает по-разному для разных объектов
animals = [Dog("Рекс", 4), Cat("Мурка"), Cow("Бурёнка"), Puppy("Кнопка", 1, 2)]

print("=== 4. ПОЛИМОРФИЗМ ===")
for animal in animals:
    print(animal.speak())
print()

# ------------------------------------------------------------
# 5. МАГИЧЕСКИЕ МЕТОДЫ (dunder methods)
#    Методы с двойным подчёркиванием __...__ позволяют
#    настроить поведение объектов (сложение, сравнение, str и т.д.)
# ------------------------------------------------------------

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):          # что выводить через print()
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):   # что делает оператор +
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):    # что делает оператор ==
        return self.x == other.x and self.y == other.y


v1 = Vector(2, 3)
v2 = Vector(4, 1)
print("=== 5. МАГИЧЕСКИЕ МЕТОДЫ ===")
print(v1)              # используется __str__
print(v1 + v2)         # используется __add__
print(v1 == Vector(2, 3))  # используется __eq__
print()

# ------------------------------------------------------------
# 6. СТАТИЧЕСКИЕ И КЛАССОВЫЕ МЕТОДЫ
# ------------------------------------------------------------

class MathUtils:
    pi = 3.14159

    # Статический метод — не зависит от объекта и класса
    @staticmethod
    def add(a, b):
        return a + b

    # Классовый метод — получает сам класс (cls), а не объект
    @classmethod
    def get_pi(cls):
        return cls.pi


print("=== 6. СТАТИЧЕСКИЕ / КЛАССОВЫЕ МЕТОДЫ ===")
print(f"Статический метод: {MathUtils.add(5, 7)}")
print(f"Классовый метод: {MathUtils.get_pi()}")