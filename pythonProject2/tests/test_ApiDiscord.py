import pytest
from pages.base_page import DiscordAPI

@pytest.fixture(scope="module")
def discord_api(base_url, headers, channel_id):
    return DiscordAPI(base_url, headers, channel_id)

def test_send_and_delete_message_with_mention(discord_api):
    content = "Привет!"
    response = discord_api.send_message(content)
    print(response.text)
    assert response.status_code == 200

    message_id = response.json().get("id")

    delete_message_response = discord_api.delete_message(message_id)
    assert delete_message_response.status_code == 204

def test_send_and_delete_message_with_attachment(discord_api):
    content = "Сообщение с вложенным файлом PNG"
    file_path = "C:/Users/DRT/PycharmProjects/Diplom_discord/pythonProject2/tests/winter.png"

    response_with_attach = discord_api.send_message_with_attachment(content, file_path)
    assert response_with_attach.status_code == 200

    message_id = response_with_attach.json().get("id")

    response_reaction = discord_api.add_reaction(message_id, "%F0%9F%98%8A")
    assert response_reaction.status_code == 204

    response_delete_message = discord_api.delete_message(message_id)
    assert response_delete_message.status_code == 204

def test_send_and_delete_message_with_emoji(discord_api):
    content = "Все будет супер 🙌"
    response = discord_api.send_message(content)
    message_id = response.json().get("id")

    # Проверка на статус код 200
    assert response.status_code == 200, f"Ошибка при отправке сообщения: {response.text}"
    # Проверка, что сообщение действительно отправлено
    assert message_id is not None, "ID сообщения не получен."

    reaction_response = discord_api.add_reaction(message_id, "%F0%9F%98%8A")
    assert reaction_response.status_code == 204

    delete_reaction_response = discord_api.delete_reaction(message_id, "%F0%9F%98%8A")
    assert delete_reaction_response.status_code == 204

    delete_message_response = discord_api.delete_message(message_id)
    assert delete_message_response.status_code == 204

def test_get_messages(discord_api):
    response_get_messages = discord_api.get_message(limit=10,before_id=1300029060994564137)
    print (response_get_messages.text)
    #assert response_get_messages.status_code == 200








