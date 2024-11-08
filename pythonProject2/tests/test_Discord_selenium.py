import time
import pytest
from pages.base_page import DiscordPage
from tests.conftest import email, password


@pytest.mark.usefixtures("driver")
class TestDiscord:
    def test_login_and_send(self, driver):
        discord_page = DiscordPage(driver)
        discord_page.login(email, password)
        discord_page.select_server()
        discord_page.select_channel()
        message_text = "У меня все получится, надо верить!"
        discord_page.send_message_ch3(message_text)
        time.sleep(3)
        last_message = discord_page.get_text_last_message()
        print("Последнее отправленное сообщение: ", last_message)
        assert message_text == last_message, "Отправленное сообщение не найдено"


    def test_reaction(self, driver):
        discord_page = DiscordPage(driver)
        discord_page.put_reaction_ch3()
        time.sleep(5)
        assert discord_page.is_emoji_present(), "Реакция к сообщению отсутствует"
        discord_page.delete_reaction_ch3()
        time.sleep(3)
        discord_page.delete_message_ch3()


    def test_edit_message(self, driver):
        discord_page = DiscordPage(driver)
        discord_page.send_message_ch3("Прекрасная сегодня погода!")
        time.sleep(3)
        discord_page.edit_message_ch3()
        time.sleep(3)
        edited_message = discord_page.get_text_last_message()
        time.sleep(5)
        assert edited_message == "Прекрасная сегодня погода! С первым снегом!"
        discord_page.delete_message_ch3()






