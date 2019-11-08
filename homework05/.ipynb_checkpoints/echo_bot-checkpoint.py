import telebot


access_token = 'AAEbpZxyCvZAmrGpEMkuNvvAJvXVaznkeV0'
telebot.apihelper.proxy = {'https': 'https://23.237.22.172:3128'}
bot = telebot.TeleBot(access_token)

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling()
