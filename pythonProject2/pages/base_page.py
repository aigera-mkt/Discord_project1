import time
import requests
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DiscordAPI:
    def __init__(self, base_url, headers, channel_id):
        self.base_url = base_url
        self.headers = headers
        self.channel_id = channel_id

    def send_message(self, content):
        data = {"content": content}
        response = requests.post(
            f"{self.base_url}/channels/{self.channel_id}/messages",
            headers=self.headers,
            json=data
        )
        return response

    def send_message_with_attachment(self, content, file_path):
        data = {"content": content}
        with open(file_path, "rb") as file:
            files = {
                "files[0]": ("winter.png", file, "image/png")
            }
            response = requests.post(
                f"{self.base_url}/channels/{self.channel_id}/messages",
                headers=self.headers,
                data=data,
                files=files
            )
        return response

    def add_reaction(self, message_id, emoji):
        url = f"{self.base_url}/channels/{self.channel_id}/messages/{message_id}/reactions/{emoji}/@me"
        response = requests.put(url, headers=self.headers)
        return response

    def delete_reaction(self, message_id, emoji):
        url = f"{self.base_url}/channels/{self.channel_id}/messages/{message_id}/reactions/{emoji}/@me"
        response = requests.delete(url, headers=self.headers)
        return response

    def delete_message(self, message_id):
        url = f"{self.base_url}/channels/{self.channel_id}/messages/{message_id}"
        response = requests.delete(url, headers=self.headers)
        return response

    def get_message(self, limit=10, before_id=None):
        params = {"limit": limit, "before_id": before_id}
        url = f"{self.base_url}/channels/{self.channel_id}/messages"
        response = requests.delete(url, headers=self.headers, params=params)
        return response


class DiscordPage:
    def __init__(self, driver):
        self.driver = driver

    time.sleep(1)

    def login(self, email, password):
        email_input = self.driver.find_element(By.NAME, "email")
        password_input = self.driver.find_element(By.NAME, "password")
        email_input.send_keys(email)
        # time.sleep(2)
        password_input.send_keys(password)
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[div[text()='Вход']]"))
        )
        login_button.click()

        # Ожидание завершения загрузки после входа
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("channels")
        )

    def last_message_locator(self):
        return By.XPATH, "//li[starts-with(@id, 'chat-messages')][last()]"

    # def last_message_locator(self):
    #     return By.XPATH, "//div[starts-with(@id,'message-content') and contains(@class,'messageContent_f9f2ca')]//span"

    def last_message(self):
        # Используем * для распаковки кортежа из last_message_locator
        return self.driver.find_element(*self.last_message_locator())

    def hover(self, element):
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()
        action.context_click(element).perform()

    def select_server(self):
        # Ожидание появления и переход на сервер "Сервер Диплом"
        server_icon = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='childWrapper_f90abb childWrapperNoHoverBg_f90abb acronym_f90abb']"))
        )
        server_icon.click()

    def select_channel(self):
        # Переход на указанный канал "#3"
        channel = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@data-list-item-id='channels___1286673494603731044']"))
        )
        channel.click()
        # time.sleep(5)

    def send_message_ch3(self, message_text):
        message_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//div[@class ='markup_f8f345 editor_a552a6 slateTextArea_e52116 fontSize16Padding_bdf0de']"))
        )
        message_box.click()
        message_box.send_keys(message_text + Keys.ENTER)

    def delete_message_ch3(self):
        #Находим и нажимаем правой кнопкой мыши на последнее сообщение в чате
        last_message = self.last_message()
        self.hover(last_message)
        # Находим и нажимаем удалить
        delete_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='message-delete' and .='Удалить сообщение']"))
        )
        # self.driver.find_element(
        # By.XPATH, "//div[@id='message-delete' and .='Удалить сообщение']"))
        # action.move_to_element(delete_button).click().perform()
        # self.hover(delete_button)
        delete_button.click()
        # time.sleep(1)
        # Подтверждаем удаление
        confirm_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and .//div[text()='Удалить']]")))
        confirm_button.click()

    def put_reaction_ch3(self):
        last_message = self.last_message()
        self.hover(last_message)
        reaction = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='hoverBarButton_e986d9 button_f7e168' and @aria-label='Добавить реакцию']"))
        )
        # reaction = self.driver.find_element(*reaction_element)
        reaction.click()
        thumb_sub = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='emoji-picker-grid-0-1']/button"))
        )
        # thumb_sub = self.driver.find_element(By.XPATH, "//*[@id='emoji-picker-grid-0-1']/button")
        thumb_sub.click()
        # time.sleep(2)

    def delete_reaction_ch3(self):
        # thumb_sub_to_delete_last_message_locator = self.driver.find_element(By.XPATH,
        thumb_sub_to_delete_last_message = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[starts-with(@id, 'chat-messages')][last()]//img[@data-name='👍']"))
        )
        thumb_sub_to_delete_last_message.click()

    def edit_message_ch3(self):
        last_message = self.last_message()
        self.hover(last_message)
        edit_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='message-edit' and @role='menuitem']"))
        )
        edit_button.click()
        textbox_edit = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='textbox' and @contenteditable='true']"))
        )
        # textbox_edit.clear()
        # Выделим и удалим старый текст
        textbox_edit.send_keys(Keys.CONTROL + 'a')  # Выделяет весь текст
        textbox_edit.send_keys(Keys.BACKSPACE)  # Удаляет выделенный текст
        new_text = "Прекрасная сегодня погода! С первым снегом!"
        textbox_edit.send_keys(new_text)
        textbox_edit.send_keys(Keys.ENTER)

        # Находим поле ввода и отправляем сообщение с помощью клавиши Enter
        # edit_input = WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'slateTextArea')]"))
        # )
        # edit_input.send_keys(Keys.RETURN)

    def get_text_last_message(self):
        last_message_element = self.last_message()
        # Получаем текст последнего сообщения
        message_text = ''.join(
            span.text for span in last_message_element.find_elements(
                By.XPATH, ".//div[contains(@id,'message-content')]//span"
            )
        )
        return message_text.replace("(изменено)", "").strip()

    def is_emoji_present(self):
        try:
            # Проверяем, присутствует ли эмодзи в последнем сообщении
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//li[starts-with(@id, 'chat-messages')][last()]//img[@data-name='👍']"))
            )
            return True
        except TimeoutException:
            return False
