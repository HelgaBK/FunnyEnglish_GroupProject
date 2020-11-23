import telebot
import config
import time
import random

bot = telebot.TeleBot( config.TOKEN )
global words
global w
global anything
global count_
words__ = ['flower', 'dog', 'cat', 'text', 'apple', 'lollipop', 'cake', 'desk', 'boy']
words = []
for y in words__:
    words.append( y )

w = 0
anything = []
count_ = [0]
word = []
words_taken = []
pass_ = [0]

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
    word.append( word_taken )
    anything.clear()
    f = ''
    for i in word[0]:
        anything.append( '*' )
        f += "➖"
    #bot.send_message( message.chat.id, word[0] )
    count_.clear()
    count_.append(len(word[0]))
    count_life = '⭐️' * int(count_[0])
    bot.send_message( message.chat.id,
                      'Залишилось ' + str(len_) + ' слів.\nВи почали гру \nспробуйте вгадати слово.' )
    bot.send_message( message.chat.id, 'Слово:' + f + '\n Кількість спроб:' + count_life )

@bot.message_handler(commands=['start'])

@bot.message_handler(content_types=['text'])
def lalala(message):
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
                bot.send_message(message.chat.id, m)
                count_life = '⭐️' * count_[0]
                bot.send_message( message.chat.id, 'Слово:' + m + '\n Кількість спроб:' + count_life)
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
                bot.send_message( message.chat.id, 'Помилка\n' +'\nСлово:' + m + '\n Кількість спроб:' + count_life)

# RUN



bot.polling( none_stop=True )

