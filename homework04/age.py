import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    friends = get_friends(user_id, 'bdate')
    year_in_seconds = 3.154e7
    friend_ages = []

    for friend in friends['response']['items']:
        try:
            bdate = friend['bdate']
            date_now = dt.datetime.now()
            bdate = dt.datetime.strptime(bdate, "%d.%m.%Y")
            age_in_seconds = (date_now - bdate).total_seconds()
            friend_ages.append(age_in_seconds//year_in_seconds)

        except:
            pass

    return median(friend_ages)
