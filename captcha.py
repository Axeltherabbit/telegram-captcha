from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from database import *

from logger import *

def new_user(bot,update,bot_id):
    for user in update.message.new_chat_members:
        admin=[user.user.id for user in bot.get_chat_administrators(update.message.chat.id)]
        if user.id == bot_id: #if the bot has been added into a group
            bot.sendMessage(update.message.chat_id, "Hi, please give me admin permissions and I'll start work")
            log.debug(f"bot added in {update.message.chat_id}")
        elif r.get(f"aweek:{user.id}") is not None: #if the user is in whitelist
            log.debug(f"{user.id} {user.first_name} @{user.username} is in the whitelist")
        elif r.get(f"warn:{user.id}") is not None and int(r.get(f"warn:{user.id}")) >= 3: #if the user has got 3 warns
            bot.kickChatMember(chat_id=update.message.chat_id,user_id=user.id)
            m=bot.sendMessage(update.message.chat_id,f"A blacklisted user has been banned {user.first_name @{user.username}}")
            r.setex(f"clearspam:{m.chat_it}:{m.message_id}",360,'')
            log.debug(f"{user.id} {user.first_name} @{user.username} is in the blacklist")
        elif update.message.from_user.id not in admin:#finally the captcha if the user has not been added by an admin
            try:#it works just in supergroups
                bot.restrictChatMember(update.message.chat_id,user.id,can_send_messages=False)
            except Exception as e:
                log.warning(e)
            keyboard = [[InlineKeyboardButton("I'm not a robot 🤖", callback_data=user.id)]]
            captcha = InlineKeyboardMarkup(keyboard)
            msg=bot.sendMessage(update.message.chat_id,f'''Hello {user.first_name} @{user.username}!\n
If you're not a robot please press the button and I'll unmute you or I'll kick you in a minute''',
                                reply_markup = captcha)
            r.setex(f"aminute:{user.id}:{update.message.chat_id}:{msg.message_id}",60,'')
            log.debug(f"{user.id} {user.first_name} @{user.username} has got a captcha")
