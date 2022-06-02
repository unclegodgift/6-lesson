from marshmallow import Schema, fields, validate, post_load, ValidationError
import json
import os


# # ---------------------------------
# проверка настроек
# Q:\Selection\Te.json
# settings = input("Путь к настройкам\n")
# print(os.path.exists(settings))
save = "Save.json"

# ---------------------------------
# конструктор
class User(object):
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

# __repr__, чтобы мы легко могли вывести экземпляр для проверки
    def __repr__(self):
        return f'I am {self.name}, my age is {self.age} and my gender is {self.gender}'

class UserSchema(Schema):
    name = fields.String(missing='Unknown', default='Unknown', valdiate=validate.Length(min=1)) # Дает дефолт значения
    age = fields.Integer(required=True, error_messages={'required': 'Please enter your age.'}, validate=validate.Range(min=0, max=None)) #  обязательно заполнить
    gender = fields.String(required=False, valdiate=validate.OneOf(['F', 'M', 'Other']))

# @post_load опциональная. Она нужна для загрузки схемы в качестве экземпляра какого-либо класса.
# Следовательно, в нашем случае она нужна для генерации экземпляров User.
# Метод make реализует экземпляр с помощью атрибутов.
    @post_load
    def make(self, data, **kwargs):
        return User(**data)

# ---------------------------------
#Открываем файл настройек, загружаем в конструктор, валидация
try:
    data = json.load(open("Te.json", "r"))
    users = UserSchema().load(data)
except ValidationError as e:
    print(f'\nError Msg: {e.messages}')
    print(f'Valid Data: {e.valid_data}')

#Открываем save файл
try:
    data = json.load(open(save, "r"))
    users = UserSchema().load(data)
    print("\n" + str(users) + " - ЭТО СТАРЫЕ ДАННЫЕ\n")
except ValidationError as e:
    print(f'Error Msg: {e.messages}')
    print(f'Valid Data: {e.valid_data}\n')

# ---------------------------------
# ---------------------------------
# ---------------------------------
# Даем значения
class JSONAble(object):
    def __init__(self):
        '''
        Constructor
        '''

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def getValue(self, v):
        if (hasattr(v, "asJSON")):
            return v.asJSON()
        elif type(v) is dict:
            return self.reprDict(v)
        elif type(v) is list:
            vlist = []
            for vitem in v:
                vlist.append(self.getValue(vitem))
            return vlist
        else:
            return v

    def reprDict(self, srcDict):
        '''
        get my dict elements
        '''
        d = dict()
        for a, v in srcDict.items():
            d[a] = self.getValue(v)
        return d

    def asJSON(self):
        '''
        recursively return my dict elements
        '''
        return self.reprDict(self.__dict__)

data = JSONAble()
try:
    data.name = input("Введите имя\n")
    data.age = int(input("Возраст\n"))
    data.gender = input("M F\n")
except ValueError:
    print("Oops!  That was no valid number.  Try again...")

user = data.asJSON() # преобразовали в JSON, а его в dict

# ---------------------------------
# смотрим их
try:
    users = UserSchema().load(user)
except ValidationError as e:
    print(f'Error Msg: {e.messages}')
    print(f'Valid Data: {e.valid_data}')
finally:
    print(users)

# ---------------------------------
# Суем в файл

with open(save, 'w') as outfile:
    json.dump(user, outfile)

# ---------------------------------
# Открываем
with open(save) as json_file:
    users = json.load(json_file)
    print(users)








