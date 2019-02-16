from config import * #config vars

import time
from redis import StrictRedis
import threading

import telegram
from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler
from functools import partial

from captcha import *
from buttons_query import *
from expired_records import *

from logger import *

def error_callback(bot, update, error):
    log.warning("error: ", error)

def main():

    r = redis.Redis(host='localhost',port=6379)
    r.flushdb() #clean db before the start

    bot = telegram.Bot(token)
    comandi = Updater(token)


    bot_id=bot.get_me().id #used for skip the captcha for itself
    msg_handler = MessageHandler(Filters.status_update.new_chat_members, partial(new_user,bot_id=bot_id))
    comandi.dispatcher.add_handler(msg_handler)

    comandi.dispatcher.add_handler(CallbackQueryHandler(buttons))
    comandi.dispatcher.add_error_handler(error_callback)

    r = redis.StrictRedis()
    pubsub = r.pubsub()
    pubsub.psubscribe("__keyevent@0__:expired")
    thread = threading.Thread(target = expiration_listener, args = (pubsub, bot ))
    thread.start()

    comandi.start_polling(0.75, clean=True)
    comandi.idle()


if __name__=="__main__":
    main()
