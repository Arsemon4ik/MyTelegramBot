import telebot
from config import keys, TOKEN
from extensions import CryptoConverter, ConvertionException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ['start','help'])
def help(message):
    text = '''Чтобы начать работу введите команду бота в следующем формате:\n<Имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n
Например вот так: евро гривна 1 (вам выведет текущий курс первой валюты во вторую)\n
Увидеть список всех валют: /values'''
    bot.reply_to(message,text)



@bot.message_handler(commands = ['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key))

    bot.reply_to(message,text)


@bot.message_handler(content_types = ['text'])
def convert(message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote,base,amount)

    except ConvertionException as e:
         bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)






bot.polling(none_stop = True)