import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = "53a987ba81983d78efb3f3cc228d8b172146256cd8e65fb900064f6d216f5f6a999ec7d0d9e1cc11486ff"

def write_msg(user_id, message):
    global vk
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 12345})

vk = vk_api.VkApi(token = token)
longpoll = VkLongPoll(vk)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text

            if request == "/start":
                write_msg(event.user_id, "Добро пожаловать в сервис!")
            else:
                write_msg(event.user_id, "Я вас не понимаю(")
