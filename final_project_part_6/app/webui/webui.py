import requests
import streamlit as st
from auth.jwt_handler import verify_access_token
from datetime import datetime, timedelta
import extra_streamlit_components as stx
import streamlit.components.v1 as components
import pandas as pd

API_URL = "http://app:8080"

def get_cookie_manager():
    return stx.CookieManager()
cookie_manager = get_cookie_manager()

def set_token(token):
    st.session_state.token = token
    st.session_state.token_expiry = datetime.now() + timedelta(minutes=20)
    cookie_manager.set("token", token, expires_at=st.session_state.token_expiry)
def get_token():
    return st.session_state.token
def remove_token():
    st.session_state.token = None
    st.session_state.token_expiry = None

# Login page
def login_page():
    add_custom_css()
    st.markdown('<h1 class="main-title">Вход в личный кабинет</h1>', unsafe_allow_html=True)
    email = st.text_input("Email", key="login_email")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    login_button = st.button("Войти")
    back1_button = st.button("Вернуться в меню")

    if login_button:
        url = f'{API_URL}/user/login/'
        payload = {"email": email, "username": username, "password": password}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            res = response.json()
            token = res.get("access_token")
            user_id = res.get("user_id")
            set_token(token)
            st.session_state.admin = verify_access_token(token)["is_admin"]
            st.session_state.logged = True
            st.session_state.username = verify_access_token(token)["username"]
            st.session_state.user_id = verify_access_token(token)["user_id"]
            st.session_state.current_page = "dashboard"
            st.rerun()
        else:
            st.error("Error logging in")

    if back1_button:
        st.session_state.current_page = "menu"
        st.rerun()

#Register page
def register_page():
    add_custom_css()
    st.markdown('<h1 class="main-title">Регистация</h1>', unsafe_allow_html=True)
    username = st.text_input("Name", key="register_username")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")

    reg_button = st.button("Зарегестрироваться")
    back1_button = st.button("Вернуться в меню")

    if reg_button:
        url = f'{API_URL}/user/register/'
        payload = {"email": email, "username": username, "password": password}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            st.success("Регистация прошла успешно, поздравляем!")
            st.session_state.current_page = "login"
            st.rerun()
        else:
            st.error("К сожалению возникла ошибка при регистрацие :(")

    if back1_button:
        st.session_state.current_page = "menu"
        st.rerun()

#Dashboard
def dashboard_page():
    add_custom_css()

    if (st.session_state.username == ""):
        return

    st.markdown('<h1 class="main-title">Личный кабинет</h1>', unsafe_allow_html=True)

    st.markdown('<p class="welcome-text">Добро пожаловать. В личный кабинет, здесь у вас возможность пополнить ваш баланс. Или потратить его на создание предсказаний. Однако считаем необходимым указать на тот факт, что для большого количества данных лучше использовать другой наш сервис api. И наконец сдесь вы можете ознакомиться с историей ваших покупок и транзакций. На сайте присутствует модерация (админ) которые тоже могут видеть историю ваших покупок на случай возникновения непредвиденных сложностей. Также заметим, что результаты сделланных вами предсказаний сохраняються в нашей базе данных</p>', unsafe_allow_html=True)

    url = f'http://final_project_part_6-app-1:8080/user/balance/{st.session_state.user_id}?id={st.session_state.user_id}'
    response = requests.get(url)

    if response.status_code == 200:
        balance = response.json()
        st.write(f"Ваш баланс: {balance} кредитов")
    else:
        st.write("Ошибка при обработке баланса")

    st.subheader("Пополнение баланса")
    amount = st.number_input("Добавить х кредитов") #не ставим html в части с инпутами по соображением безопасности

    if st.button("Положить средства на счёт"):
        if (amount <= 0):
            st.error("Ошибка вы можете класть только положительное значение")
            return
        url = 'http://final_project_part_6-app-1:8080/user/balance/'
        payload = {
          "user_id": st.session_state.user_id,
          "amount": amount,
           "description_arg": "Пользователь пополнил баланс"
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            st.success("Баланс успешно пополнен")
            st.rerun()
        else:
            st.error("Ошибка, кредиты не начисленны, извините.")

    st.subheader("Предсказания")
    input_data = st.file_uploader("Прикрепите файл с данными пользователя", type=["csv"])
    model_ver = st.text_input("Версия модели")
    if (model_ver != "1" and model_ver != "2"):
        st.error(f"На данный момент существуют только версии: 1,2")

    if st.button("Провести предсказание"):
        url = 'http://final_project_part_6-app-1:8080/user/predict/'
        df = pd.read_csv(input_data)
        payload = {
            "user_id": st.session_state.user_id,
            "amount": "5",
            "description_arg": "предсказание",
            "data2": df.to_json(orient="split"),
            "version":model_ver
        }
        response = requests.post(url, json=payload)
        if  response.status_code == 200:
            result = response.json()
            st.success("Предсказание выполнено")
            st.write(f"Результат: {result}")
        else:
            st.error("Ошибка при выполнение предсказания :(")

    st.subheader("История предсказаний")
    if st.button("Посмотреть предсказания"):
        url = f'http://final_project_part_6-app-1:8080/user/predictions/{st.session_state.user_id}?id={st.session_state.user_id}'
        response = requests.get(url)
        if response.status_code == 200:
            history = response.json()
            st.write(history)
        else:
            st.error("Error fetching history")

    st.subheader("История транзакций")
    if st.button("Посмотреть транзакции"):
        url = f'http://final_project_part_6-app-1:8080/user/transactions/{st.session_state.user_id}?id={st.session_state.user_id}'
        response = requests.get(url)
        if response.status_code == 200:
            history = response.json()
            st.write(history)
        else:
            st.error("Error fetching history")
    
    if (st.session_state.admin == 1):
        st.subheader("Секретная страница админа")
        st.subheader("Смотреть истории транзакций других пользователей")
        user_id_search = st.text_input("Введите интересующий вас ИД")
        if (st.button("Смотреть")):
            url = f'http://final_project_part_6-app-1:8080/user/transactions/{user_id_search}?id={user_id_search}'
            response = requests.get(url)
            if response.status_code == 200:
                history = response.json()
                st.write(history)
            else:
                st.error("Ошибка")

        st.subheader("Изменить баланс пользователя")
        user_id_balance = st.text_input("Введите ИД пользователя")  
        user_add_amount = st.text_input("Введите количество кредитов")
        if (st.button("Пополнить баланс пользователя")):
            if (int(user_add_amount) <= 0):
                st.error("Пополнение должно быть > 0")
                return
            url = 'http://final_project_part_6-app-1:8080/user/balance/'
            payload = {
            "user_id": user_id_balance,
            "amount": user_add_amount,
            "description_arg": "Баланс пополнен"
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                st.success("Баланс успешно пополнен")
                st.rerun()
            else:
                st.error("Ошибка, мы не смогли пополнить ваш баланс")


def add_custom_css():
    st.markdown("""
        <style>
            /* Задник */
            .stApp {
                background: linear-gradient(135deg, #6DD5FA 0%, #2986cc 100%);
                font-family: 'Arial', sans-serif;
            }
            /* Стиль заголовка */
            .main-title {
                font-size: 3rem;
                text-align: center;
                font-weight: bold;
                color: white;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
                margin-bottom: 1rem;
            }
            /* Стиль основного текста */
            .welcome-text {
                font-size: 1.2rem;
                color: white;
                text-align: center;
                margin-bottom: 2rem;
                padding: 0 2rem;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
            }
            /* Кнопки (Логин регистация) */
            .stButton > button {
                border: none;
                color: white;
                background-color: #4CAF50;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 1.2rem;
                margin: 0.5rem;
                border-radius: 25px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                transition: background-color 0.3s ease, transform 0.3s ease;
            }
            /* (Эффект выделения кнопки, что бы когда наводим курсор кнопка рееалировал) */
            .stButton > button:hover {
                background-color: #45a049;
                transform: translateY(-3px);
            }
            /* Фотографии */
            .carousel-container {
                width: 100%;
                overflow: hidden;
                position: relative;
            }

            .carousel {
                display: flex;  /* Align images horizontally */
                flex-wrap: nowrap;  /* No wrapping, all images are in a row */
                justify-content: start; /* Align items at the start of the carousel */
            }

            .carousel img {
            width: 20%; /* Adjust this depending on your image width */
            transition: all 0.5s ease;
            opacity: 0.5; /* Default opacity for images away from center */
            transform: scale(0.8); /* Default smaller scale for images away from center */
            }

            .carousel img.center {
            opacity: 1;
            transform: scale(1);
            }
        </style>
    """, unsafe_allow_html=True)

def add_custom_css2():
    #2 задник
    pass

# Main page
def main_page():
    add_custom_css()

    st.markdown('<h1 class="main-title">Главное Меню</h1>', unsafe_allow_html=True)

    st.markdown('<p class="welcome-text">Добро пожаловать. Вы находитесь на веб приложение нашего сервиса по созданию реккомендаций для пользователей стим. Мы готовы предоствить вам в пользование созданные нами модели, но для начала просим вас зарегестрироваться, или же в случае если у вас уже сть аккаует войти. Удачи!.</p>', unsafe_allow_html=True)

    if not st.session_state.logged:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Вход"):
                st.session_state.current_page = "login"
                st.rerun()
        with col2:
            if st.button("Регистация"):
                st.session_state.current_page = "register"
                st.rerun()

    carousel_html = """
    <div class="carousel-container">
        <div class="carousel">
            <img src="https://imgur.com/uhDuFnn.png" alt="img1">
            <img src="https://imgur.com/hciCKd5.png" alt="img2">
            <img src="https://imgur.com/Y37ktNP.png" alt="img3">
            <img src="https://imgur.com/NY6VqDe.png" alt="img4">
            <img src="https://imgur.com/uhDuFnn.png" alt="img5">
        </div>
    </div>

    <script>
      const carousel = document.querySelector('.carousel');
      const images = document.querySelectorAll('.carousel img');
      const totalImages = images.length;
      let index = 0;
      const speed = 2000;

      function moveImages() {
        index = (index + 1) % totalImages;

        images.forEach((image, i) => {
          const position = (i - index + totalImages) % totalImages;  // Calculate relative position to center
          if (position === 0) {
            image.classList.add('center');
            image.style.opacity = '1'; 
            image.style.transform = 'scale(0.9)'; 
          } else {
            image.classList.remove('center');
            image.style.opacity = '0.5'; 
            image.style.transform = 'scale(0.8)';
          }
        });

        if (index === totalImages - 1) {
          setTimeout(() => {
            carousel.style.transition = 'none';
            carousel.style.transform = 'translateX(0)';
            setTimeout(() => {
              carousel.style.transition = 'transform 0.5s ease';
            });
          }, speed);
        }
      }

      moveImages();
      setInterval(moveImages, speed);
    </script>
    """

    # Render the carousel HTML
    components.html(carousel_html, height=350)


def initialize_session_state():
    if 'logged' not in st.session_state:
        st.session_state.logged = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "menu"
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'token' not in st.session_state:
        st.session_state.token = None
        st.session_state.token_expiry = None
    if 'admin' not in st.session_state:
        st.session_state.admin = 0

def main():
    initialize_session_state()

    token = get_token()

    if token:
        try:
            decoded_token = verify_access_token(token)
            if decoded_token:
                st.session_state.logged = True
                st.session_state.username = verify_access_token(token)["email"]
                st.session_state.user_id = verify_access_token(token)["user_id"]
                st.sidebar.write("ИНСТРУКЦИЯ")
                st.sidebar.write(f"Вы автаризовались как {st.session_state.username}!")

                st.sidebar.write("Работа с балансом")
                st.sidebar.write("Здесь вы можете Посмотреть ва баланс и положить на него деньги. Для этого в разделеле пополнение баланса укажите желаемое количество крелитов для пополенния и нажмите <положить средства на счёт>")

                st.sidebar.write("Работа с моделью")
                st.sidebar.write("Для того что бы создать воспользоваться моделью вам необходимо иметь на балансе минимум 5 кредитов. Именно столько состовляет цена одного использования.")
                st.sidebar.write("Наша модель запросит у вас информацию о вашем провиле стим. В случае если вы выберете версию модели 1 - она порекомендует вам 5 игр, которые могут вас заинтересовать. Вводите минимум 5 имеющихся игр для более точной оценки. В случае выбора модели с версией 2 она выдаст оценку кредитного рейтинга вашего профиля и выдаст вам предложения об рассрочках в разных ценовых сегментах.")
                st.sidebar.write("Данные об аккаунте в стиме должна быть в формате csv и содержать (Список всех имеюшихся у вас игр, список ИД этих игр в соответствующем порядке, общее кол во игр, уровень стима, бэйдж стима, текущий опыт, опыт до повыщеия, кол-во друзей")
                
                st.sidebar.write("Просморт результатов")
                st.sidebar.write("Нажав на соответствующую кнокпу вы увидите все ваши предсказания созданые за периуд пользования сайта.")

                st.sidebar.write("Просморт транзакций")
                st.sidebar.write("Нажав на соответствующую кнокпу вы увидите все ваши транзацкие произошедшие за периуд пользования сайта.")
            else:
                print("Bad token")
                raise ValueError("Invalid token")

        except Exception as e:
            print("Auth error")
            st.error(f"Ошибка при проверке токена: {e}")
            remove_token()
            st.session_state.logged = False
    else:
        st.session_state.logged = False

    if st.session_state.logged:
        pages = {
            "menu": main_page,
            "dashboard": dashboard_page,
        }
        logout_button = st.button("Выйти")
        if logout_button:
            remove_token()
            st.session_state.logged = False
            st.session_state.username = ""
            st.session_state.user_id = None
            st.session_state.current_page = "menu"
            st.rerun()
    else:
        pages = {"menu": main_page, "login": login_page, "register": register_page}

    if st.session_state.current_page in pages:
        pages[st.session_state.current_page]()


if __name__ == "__main__":
    main()
