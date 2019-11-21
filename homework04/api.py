import requests
import random
import time

import config


def get(url, params={}, timeout=5, max_retries=2, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    min_delay = 0.1
    max_delay = 3
    jitter = 0.1

    delay = min_delay

    for retries in range(max_retries):
        response = requests.get(url,
                                timeout=timeout
                    )

        if response.status_code == 200:
            return response

        time.sleep(delay)

        delay = min(delay * backoff_factor, max_delay)
        delay = delay + random.randint(0,5) * jitter

    return response.raise_for_status()

def get_friends(user_id, fields=''):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    query = (f"{config.VK_CONFIG['domain']}/" +
            "friends.get?" +
            f"access_token={config.VK_CONFIG['access_token']}&" +
            f"user_id={user_id}&" +
            f"fields={fields}&" +
            f"v={config.VK_CONFIG['version']}")
    response = requests.get(query)

    return response.json()
