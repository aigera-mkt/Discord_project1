import time
import pytest
import allure
from pages.base_page import DiscordPage
from tests.conftest import email, password


@pytest.mark.usefixtures("driver")
class TestDiscord:
    @allure.title("Тест проверяет отправку сообщения")
    def test_login_and_send(self, driver):
        discord_page = DiscordPage(driver)
        with allure.step("Авторизация пользователя"):
            discord_page.login(email, password)
        with allure.step("Нажатие на сервер Diplom"):
            discord_page.select_server()
        with allure.step("Нажатие на канал №3"):
            discord_page.select_channel()
            message_text = "У меня все получится, надо верить!"
        with allure.step("Отправка сообщения"):
            discord_page.send_message_ch3(message_text)
            time.sleep(3)
            last_message = discord_page.get_text_last_message()
            print("Последнее отправленное сообщение: ", last_message)
        with allure.step("Проверка совпадает ли текст с последним сообщением"):
            try:
                assert message_text == last_message, "Отправленное сообщение не найдено"
            except AssertionError as e:
                allure.attach(driver.get_screenshot_as_png(), name="screenshot",
                              attachment_type=allure.attachment_type.PNG)
                raise e

    @allure.title("Тест проверяет отправку и удаление реакции")
    def test_reaction(self, driver):
        discord_page = DiscordPage(driver)
        with allure.step("Ставим реакцию к сообщению"):
            discord_page.put_reaction_ch3()
            time.sleep(5)
        with allure.step("Проверка отображения реакции"):
            assert discord_page.is_emoji_present(), "Реакция к сообщению отсутствует"
        with allure.step("Удаление реакции"):
            discord_page.delete_reaction_ch3()
            time.sleep(3)
        with allure.step("Удаление сообщения"):
            discord_page.delete_message_ch3()

    @allure.title("Тест проверяет редактирование текста сообщения")
    def test_edit_message(self, driver):
        discord_page = DiscordPage(driver)
        with allure.step("Отправка сообщения"):
            discord_page.send_message_ch3("Прекрасная сегодня погода!")
            time.sleep(3)
        with allure.step("Редактирование сообщения"):
            discord_page.edit_message_ch3()
            time.sleep(3)
            edited_message = discord_page.get_text_last_message()
            time.sleep(5)
        with allure.step("Проверка отображения отредактированного сообщения"):
            assert edited_message == "Прекрасная сегодня погода! С первым снегом!"
        with allure.step("Удаление сообщения"):
            discord_page.delete_message_ch3()
