# This is a main file of Telegram bot.

# Bot require personal token from @BotFather
# (Get your own in Telegram)
# Bot using API from free.currconv.com
# (get your own API and place in config.py)

# Made for second final practice exercise in chapter
# "OOP" for SkillFactory

# For education purpose only. Workability is not guarantee.

# Made by IvanDamNation (a.k.a. IDN)
# GNU General Public License v3, 2022


import telebot

from config import TOKEN, currency
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_message(message: telebot.types.Message):
    text = 'To convert send a message in this form: \n' \
           '<currency name> <which currency to convert> <amount>\n' \
           'Supported currencies: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Supported currencies: '
    for key in currency.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        inquiry = message.text.split()

        if len(inquiry) != 3:
            raise APIException(
                'Unacceptable number of parameters (need 3) ')

        quote, base, amount = inquiry
        total_base, amount = Converter.get_price(quote, base, amount)

        total_base *= amount

    except APIException as e:
        bot.reply_to(message, f'User error:\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Failed to process a command\n{e}')

    else:
        total_base = round(total_base, 2)
        text = f'Price {amount} of {quote} in {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
