from stop_words import get_stop_words
import pandas as pd
import pymorphy2
import requests
import textwrap
import gensim
import config
import emoji

from pandas.io.json import json_normalize
from string import Template
from gensim import corpora
from pprint import pprint
from tqdm import tqdm

morph = pymorphy2.MorphAnalyzer()
stop_words = get_stop_words('ru')


def get_wall(
    owner_id: str='',
    domain: str='',
    offset: int=0,
    count: int=10,
    filter: str='owner',
    extended: int=0,
    fields: str='',
    v: str='5.103'
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.
    """
    code = ("return API.wall.get({" +
        f"'owner_id': '{owner_id}'," +
        f"'domain': '{domain}'," +
        f"'offset': {offset}," +
        f"'count': {count}," +
        f"'filter': '{filter}'," +
        f"'extended': {extended}," +
        f"'fields': '{fields}'," +
        f"'v': {v}," +
    "});")

    response = requests.post(
        url="https://api.vk.com/method/execute",
            data={
                "code": code,
                "access_token": config.VK_CONFIG["access_token"],
                "v": "5.103"
            }
    )

    return response.json()['response']['items']

extra_chars = ['-', ',', '.', '!', '(', ')', '[', ']', '\n']

def delete_links(text):
    if "http" in text:
        ind = text.index("http")
        bg = ind

        while ind < len(text) and text[ind] != " ":
            ind += 1

        text = text[:bg] + text[ind:]

        return text, True
    else:
        return text, False

def delete_emojis(text):
  return ''.join(c for c in text if not c in emoji.UNICODE_EMOJI)

def normilize_texts(domain):
    posts_list = get_wall(domain=domain)
    posts_texts = [post["text"].lower() for post in posts_list]

    for text_ind in range(len(posts_texts)):
        text = posts_texts[text_ind]

        status = True

        while status:
            text, status = delete_links(text)

        for char in extra_chars:
            text = text.replace(char, " ")


        posts_texts[text_ind] = text

    for text_ind in range(len(posts_texts)):
        text = posts_texts[text_ind]
        text = text.split()

        for ind in range(len(text)):
            if text[ind] in stop_words:
                text[ind] = ''
                continue

            text[ind] = morph.parse(text[ind])[0].normal_form

        posts_texts[text_ind] = " ".join(text)
        posts_texts[text_ind] = delete_emojis(posts_texts[text_ind])

    return posts_texts
    pass
