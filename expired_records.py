import threading

def expiration_listener(pubsub, bot):
    for msg in pubsub.listen():
        msg = msg["data"].decode("utf-8") if type(msg["data"]) is bytes else ''
        if msg.startswith("aminute:"):
            data=msg.split(":")
            user_id=data[1]
            chat_id=data[2]
            message_id=data[3]
            bot.kickChatMember(chat_id=chat_id,user_id=user_id)
            bot.editMessageText(chat_id=chat_id,message_id=message_id,text="captcha failed, the user has been banned")
            print(f"{user_id} has been banned from {chat_id}")
