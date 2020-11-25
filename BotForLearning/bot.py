import telebot
import config
import time
import random

from  decorate_ import theme_
from  init_data_ import *

bot = telebot.TeleBot(config.TOKEN)

def start_(message):
    if len( words ) == 0:
        bot.send_message( message.chat.id,
                          'Ви спробували спробували угадати всі наявні слова. \nГра почнеться з початку.' )
        anything.clear()
        for y in words__:
            words.append( y )
    word.clear()
    len_ = len( words ) - 1

    index = random.randint( 0, len_ )

    word_taken = words[index]
    words.pop( index )

    word.append( word_taken[1] )
    anything.clear()
    f = ''
    for i in word[0]:
        anything.append( '*' )
        f += "➖"
    #bot.send_message( message.chat.id, word[0] )
    count_.clear()
    count_.append(len(set(word[0])) * 2 - len(set(word[0])) // 3)
    count_life = '⭐️' * int(count_[0])

    bot.send_message( message.chat.id,
                      theme_(str(word_taken[0])) + '\nТема слова: ' + str(word_taken[0]) +'\n\nЗалишилось слів: ' + str(len_) + ' \nВи почали гру, спробуйте вгадати слово.' )
    bot.send_message( message.chat.id, 'Слово:' + f + '\nКількість спроб, що залишилось:\n' + count_life )

@bot.message_handler(commands=['start'])

@bot.message_handler(content_types=['text'])
def init_funk(message):

    msg = message.text.lower()
    if msg == '/start':
        pass_.clear()
        pass_.append(0)
        start_(message)

    elif pass_[0] == 0:
        if msg == word[0]:
            bot.send_message( message.chat.id, 'Вітаємо! Ви вгадали слово '+ word[0] +'!\n🍀😉🍀😉🍀😉🍀😉🍀😉🍀😉🍀😉🍀 \nЯкщо хочете продовжити гру, то натисніть /start' )
            pass_.clear()
            pass_.append(1)
        elif msg in word[0]:
            k = 0
            for i in word[0]:
                if i == msg:
                    anything[k] = msg
                k += 1
            k = 0
            m = ''
            for i in anything:
                if i == '*':
                    m += "➖"
                else:
                    m += i

            if '*' not in anything:
                bot.send_message( message.chat.id,
                                  'Вітаємо! Ви вгадали слово '+ word[0] +'!\n🍀😉🍀😉🍀😉🍀😉🍀😉🍀😉🍀😉🍀 \nЯкщо хочете продовжити гру, то натисніть /start' )
                pass_.clear()
                pass_.append(1)
            else:
                #bot.send_message(message.chat.id, m)
                count_life = '⭐️' * count_[0]
                bot.send_message( message.chat.id, 'Слово: ' + m + '\n\nКількість спроб, що залишилось:\n' + count_life)
        else:
            if count_[0] == 0:
                bot.send_message( message.chat.id, 'Ви не вгадали слово: ' + word[0] +'.\nНатисніть /start, щоб почати гру з початку')
            else:
                count_[0] -= 1
                count_life = '⭐️' * count_[0]
                m = ''
                for i in anything:
                    if i == '*':
                        m += "➖"
                    else:
                        m += i
                bot.send_message( message.chat.id, '🔴Помилка🔴\n' +'\nСлово: ' + m + '\nКількість спроб, що залишилось:\n' + count_life)

# RUN



bot.polling( none_stop=True )

