import configuration
import requests
import data

def post_new_client_kit(kit_body, auth_token):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_KITS,
                         json=kit_body,
                         headers=auth_token)
response_kit = post_new_client_kit(data.kit_body, data.auth_token)

def get_kit_body(name):
    current_body = data.kit_body.copy()
    current_body["name"] = name
    return current_body
