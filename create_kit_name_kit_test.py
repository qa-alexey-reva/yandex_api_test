import sender_stand_request
import configuration
import data
import requests


def get_new_user_token(body):
        return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                             json=body,
                             headers=data.headers)

response_token = get_new_user_token(data.user_body)
data.auth_token["Authorization"] = "Bearer" + response_token.json()["authToken"]

# Функция позитивной проверки
def positive_assert(name):
    kit_body = sender_stand_request.get_kit_body(name)
    kit_response = sender_stand_request.post_new_client_kit(kit_body, data.auth_token)
    assert kit_response.status_code == 201
    assert kit_response.json()["name"] == name

# Функция негативной проверки
def negative_assert_code_400(name):
    kit_body = sender_stand_request.get_kit_body(name)
    kit_response = sender_stand_request.post_new_client_kit(kit_body, data.auth_token)
    assert kit_response.status_code == 400

def negative_assert_no_name(kit_body):
    response = sender_stand_request.post_new_client_kit(kit_body, data.auth_token)
    assert response.status_code == 400

# Тест 1. Один символ параметра name
def test_create_kit_1_letter_in_name_get_success_response():
    positive_assert("а")

# Тест 2. Допустимое количество символов (511)
def test_create_kit_511_letters_in_name_get_success_response():
    positive_assert("Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
                    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
                    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
                    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcd" +
                    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
                    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
                    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")


# Тест 3. Количество символов меньше допустимого (0)
def test_create_kit_empty_name_get_error_response():
    kit_body = sender_stand_request.get_kit_body("")
    negative_assert_code_400(kit_body)

# Тест 4. Количество символов больше допустимого (512)
def test_create_kit_512_letters_in_name_get_error_response():
    negative_assert_code_400("Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
                    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
                    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
                    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcd" +
                    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
                    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
                    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")

# Тест 5. Разрешены английские буквы
def test_create_kit_english_letters_in_name_get_success_response():
    positive_assert("QWErty")

# Тест 6. Разрешены русские буквы
def test_create_kit_russian_letters_in_name_get_success_response():
    positive_assert("Мария")

# Тест 7. Разрешены спецсимволы
def test_create_kit_has_special_symbol_in_name_get_success_response():
    positive_assert('"№%@",')

# Тест 8. Разрешены пробелы
def test_create_kit_has_space_in_name_get_success_response():
    positive_assert(" Человек и КО ")

# Тест 9. Разрешены цифры
def test_create_kit_has_number_in_name_get_success_response():
    positive_assert("123")

# Тест 10. Параметр не передан в запросе
def test_create_kit_no_name_get_error_response():
    kit_body = data.kit_body.copy()
    kit_body.pop("name")
    negative_assert_no_name(kit_body)

# Тест 11. Передан другой тип параметра (число)
def test_create_kit_number_type_name_get_error_response():
    kit_body = sender_stand_request.get_kit_body(12)
    response = sender_stand_request.post_new_client_kit(kit_body, data.auth_token)
    assert response.status_code == 400