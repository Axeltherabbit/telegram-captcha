from database import *
import threading

from logger import *

def exp_msg_thread(msg,bot):
    msg = msg["data"].decode("utf-8") if type(msg["data"]) is bytes else ''
    if msg.startswith("aminute:"):
        data=msg.split(":")
        user_id=data[1]
        chat_id=data[2]
        message_id=data[3]

        try:#it need admin permissions
            bot.kickChatMember(chat_id=chat_id,user_id=user_id)
        except Exception as e:
            log.warning(e)
        else:#if it has admin permissions
            if r.get(f"warn:{user_id}") is None :
                r.setex(f"warn:{user_id}",86400,1)
            else:
                r.setex(f"warn:{user_id}",86400,int(r.get(f"warn:{user_id}"))+1)
            num_warn=int(r.get(f"warn:{user_id}"))
            bot.editMessageText(chat_id=chat_id,message_id=message_id,text=f"captcha failed, the user has been kicked, warn: {num_warn}/3")
            log.debug(f"{user_id} has been banned from {chat_id} -> warn num {num_warn}")
            if num_warn < 3:
                try:#just for supergroups
                    bot.unbanChatMember(chat_id=chat_id,user_id=user_id)
                except Exception as e:
                    log.warning(e)
            else:
                bot.sendMessage(chat_id,"warn number 3, permanent ban")
                log.debug(f"permanent ban from {chat_id} for {user_id}")



def expiration_listener(pubsub, bot):
    for msg in pubsub.listen():
        thread = threading.Thread(target = exp_msg_thread, args = (msg, bot ))
        thread.start()
