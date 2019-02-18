from database import *
from logger import *

def buttons(bot, update):
    query = update.callback_query
    if query.data == str(query.from_user.id):
        if r.delete(f"aminute:{query.from_user.id}:{query.message.chat_id}:{query.message.message_id}") > 0:
            bot.deleteMessage(chat_id=query.message.chat_id,message_id=query.message.message_id)
            r.setex(f"aweek:{query.from_user.id}",604800,'')
            log.debug(f"{query.from_user.id} {query.from_user.first_name} @{query.from_user.username} has solved the captcha")
            try:
                bot.restrictChatMember(query.message.chat_id,query.from_user.id,can_send_messages=True,
                                                                                can_send_media_messages=True,
                                                                                can_send_other_messages=True,
                                                                                can_add_web_page_previews=True)
            except Exception as e:
                log.warning(e)
    else:
        pass
        #bot.answer_callback_query(query.id, text="It's not for you", show_alert=True)
