from models.User import User, Prediction, Transaction
from datetime import datetime
from models import Model
from database.config import get_settings
from database.database import get_session, init_db, engine
from services import user
import random
import string

if __name__ == '__main__':
    init_db()

    test_user1 = User(user_id = 1, username = "Kevin", email = "kevin_osbrone@gmail.com", password = "12345", balance = 0, is_admin = False) 
    test_user2 = User(user_id = 2, username = "Dima", email = "dfom11@mail.ru", password = "dima11", balance = 200, is_admin = True) 
    test_user3 = User(user_id = 3, username = "Sonia", email = "apple_apple@inbox.ru", password = "12345", balance = 25, is_admin = False) 
    test_user4 = User(user_id = 4, username = "Egor", email = "tom_smith@gmail.com", password = "password", balance = 100, is_admin = False) 
    test_user5 = User(user_id = 5, username = "John", email = "john_cabbot@inbox.ru", password = "lollollol", balance = 15, is_admin = False) 

    lst = [test_user1,test_user2,test_user3,test_user4,test_user5]
    
    for el in lst:
        user.create_user(el, get_session())

    #баланс 1 пользователя. Посмотрим. Добавим 10. Посмотрим. Уберём 5. Посмотрим.

    print(user.get_balance(1,get_session()))
    user.modify_balance(id = 1, amount = 10, description_arg = "User deposited money", session = get_session())
    print(user.get_balance(1,get_session()))
    user.modify_balance(id = 1, amount = -5, description_arg = "User spend money", session = get_session())
    print(user.get_balance(1,get_session()))

    #исправления #2

    #История трансакций пользователя 1 and 2
    
    user.get_user_history(id = 1, session = get_session())

    user.get_user_history(id = 2, session = get_session()) #пусто (пока)

    #протестируем иничиализацию транзацкий. Пусть ид пользователя 2. Далле проверем, сохранилась ли запись.

    user.add_transaction(Transaction(user_id = 2, description = "adding transaction for testing", credits = 7, date_time = datetime.now()), session = get_session())

    user.get_user_history(id = 2, session = get_session()) #теперь запись об этой транзакции появилась у пользователя 2.

    #теперь история предсказаний

    user.get_predictions_history(id = 3, session = get_session()) #Empty - Пока Пусто

    #создадим модель

    test_model = Model.Model("1.2")

    test_data = "123"

    test_cost = 5

    #тестируем. Историю предсказаний. И создание предсказаний.

    if (test_model.validate(test_data)):
        user.add_transaction(Transaction(user_id = 3, description = "User payed for model use", credits = -test_cost, date_time = datetime.now()), session = get_session())
        user.add_prediction(Prediction(user_id = 3, input = test_data, output = test_model.predict(test_data), modelVersion = test_model.get_version(), cost = test_cost, date_time = datetime.now()), session = get_session())
    else:
        print("Data invalid")

    user.get_predictions_history(id = 3, session = get_session()) #Empty - Пока Пусто

