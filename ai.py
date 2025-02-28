import g4f
import g4f.Provider
import os
from telebot import TeleBot

response = g4f.ChatCompletion.create(
    model=g4f.models.gemini_exp,
    provider=g4f.Provider.PollinationsAI,
    messages=[
        {"role" : "system", "content" : "You are not an AI and not an assistant, you are dansk teacher for ukrainian students with danish level B1-B2!"},
        {"role" : "user", "content" : "Hi! Who are you and what can you do?"},
    ],
    # stream=True
    # cookies={
    #     "__Secure-1PSID" : "g.a000uAjUAPGE2J6ekF4LhheHgMDw5GYKcCDVAwXpUuPwNxhTtnOSKNjcq94JDydHwEv_6944DwACgYKAQ4SARcSFQHGX2Mi8HhBsDLzBOqq2SpNhqNE5BoVAUF8yKrQhP7gITbDFCO7DgnbQa9n0076"
    # }
)

text = ""

counter = 0
for i in response:
    text += i
    if counter > 3:
        os.system("cls")
        print(text)
        counter = 0
    counter += 1

os.system("cls")
print(text)

def ai_message(user_message, bot: TeleBot, messages_list):
    try:
        messages_list[str(user_message.chat.id)].append({"role" : "user", "content" : user_message.text})
    except Exception as e:
        print(e)
        messages_list[str(user_message.chat.id)] = [{"role" : "user", "content" : user_message.text}]
    user_messages = messages_list[str(user_message.chat.id)]
    
    print(user_messages)
    
    if len(user_messages) >= 1:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gemini_exp,
            provider=g4f.Provider.PollinationsAI,
            messages=[
                {"role" : "system", "content" : "You are not an AI and not an assistant, you are dansk teacher for ukrainian students with danish level B1-B2!"},
            ] + user_messages,
            # stream=True
            # cookies={
            #     "__Secure-1PSID" : "g.a000uAjUAPGE2J6ekF4LhheHgMDw5GYKcCDVAwXpUuPwNxhTtnOSKNjcq94JDydHwEv_6944DwACgYKAQ4SARcSFQHGX2Mi8HhBsDLzBOqq2SpNhqNE5BoVAUF8yKrQhP7gITbDFCO7DgnbQa9n0076"
            # }
        )

        text = ""
        counter = 0
        bot_message = bot.send_message(user_message.chat.id, "...")
        for i in response:
            text += i
            if counter > 10:
                bot.edit_message_text(text, bot_message.chat.id, bot_message.id)
                counter = 0
            counter += 1
        try:
            messages_list[str(user_message.chat.id)].append({"role" : "assistant", "content" : text})
            bot.edit_message_text(text, bot_message.chat.id, bot_message.id)
        except Exception as err:
            print(err)
        return 