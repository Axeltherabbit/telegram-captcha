from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from database import *

def new_user(bot,update,bot_id):
    for user in update.message.new_chat_members:
        admin=[user.user.id for user in bot.get_chat_administrators(update.message.chat.id)]
        if user.id == bot_id:
            bot.sendMessage(update.message.chat_id, "Hi, please give me admin permissions and I'll start work")
            print(f"bot added in {update.message.chat_id}")
        elif r.get(f"aweek:{user.id}") is not None:
            print(f"{user.id} {user.first_name} @{user.username} is in the whitelist")
        elif update.message.from_user.id not in admin:
            keyboard = [[InlineKeyboardButton("I'm not a robot 🤖", callback_data=user.id)]]
            captcha = InlineKeyboardMarkup(keyboard)
            msg=bot.sendMessage(update.message.chat_id,f'''Hello {user.first_name} @{user.username}!\n
If you're not a robot please press the button or I'll kick you in a minute''',
                        reply_markup = captcha)
            r.setex(f"aminute:{user.id}:{update.message.chat_id}:{msg.message_id}",60,'')
            print(f"{user.id} {user.first_name} @{user.username} has got a captcha")
