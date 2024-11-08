import pytest
from selenium import webdriver
import requests
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options

# Загружаем данные из .env
load_dotenv()
# Получаем значения из переменных окружения
api_key = os.getenv("DISCORD_API_KEY")
email = os.getenv("email")
password = os.getenv("password")

# Фикстуры для API:
@pytest.fixture(scope="session")
def base_url():
    return "https://discord.com/api/v10"

@pytest.fixture(scope="session")
def headers():
    return {
        "Authorization": api_key
    }

@pytest.fixture(scope="session")
def channel_id():
    return "1286673494603731044"


# Фикстуры для WEB UI
@pytest.fixture(scope="module")
def driver():
    # options = Options()
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    driver.get("https://discord.com/login")
    driver.implicitly_wait(5)
    driver.maximize_window()
    yield driver
    driver.quit()

    # # Авторизация через токен
    # script = f'''
    #        window.localStorage.setItem("token", "{api_key}");
    #        '''
    # # script = f'window.localStorage.setItem("token", "{api_key}");'
    # driver.execute_script(script)
    # driver.refresh()  # Обновляем страницу для применения токена
    # yield driver
    # driver.quit()

