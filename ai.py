import g4f
import g4f.Provider
import os
from telebot import TeleBot
import time 

response = g4f.ChatCompletion.create(
    model=g4f.models.gemini_2_0_flash_thinking,
    provider=g4f.Provider.Gemini,
    messages=[
        {"role" : "system", "content" : "You are not an AI and not an assistant, you are dansk teacher for ukrainian students with danish level B1-B2!"},
        {"role" : "user", "content" : "Hej!"},
    ],
    # stream=True,
    # api_key="AIzaSyB_wYlmOsTD9b2U84tdRgH9AD1nToHu_vg",
    cookies={
        "__Secure-1PSID" : "g.a000uAjUAPGE2J6ekF4LhheHgMDw5GYKcCDVAwXpUuPwNxhTtnOSKNjcq94JDydHwEv_6944DwACgYKAQ4SARcSFQHGX2Mi8HhBsDLzBOqq2SpNhqNE5BoVAUF8yKrQhP7gITbDFCO7DgnbQa9n0076",
        "__Secure-1PSIDTS" : "sidts-CjEBEJ3XV8beZsXsM2Yzbm6eBmhVKWLg399RQZOnmXiPGrk2P9QdLokC7o2p7D3Wfp5WEAA",
        "__Secure-1PSIDCC" : "AKEyXzUCYndLrCFV_dXwNLz5eor8_eapJzlNVs69yAry8RqWe2kk896u7t7PmLburJMNl6R1z_WO"
    },
    # _sid="g.a000uAjUAPGE2J6ekF4LhheHgMDw5GYKcCDVAwXpUuPwNxhTtnOS95kMQAM2DzsE63sq3Nm3SwACgYKAXQSARcSFQHGX2MiH84kSHOAP7T6sqVswr13RxoVAUF8yKpCfVVMPq-B9BgjbLGRbPdc0076"
)

text = ""

counter = 0
for i in response.split("\n\n\n\n\n\n")[1]:
    text += i
    if counter > 3:
        os.system("clear")
        print(text)
        counter = 0
    counter += 1

os.system("clear")
print(text)

messages_list = {}

def ai_message(user_message, bot: TeleBot):

    try:
        messages_list[str(user_message.chat.id)].append({"role" : "user", "content" : user_message.text})
    except Exception as e:
        print(e)
        messages_list[str(user_message.chat.id)] = [{"role" : "user", "content" : user_message.text}]
    user_messages = messages_list[str(user_message.chat.id)]
    
    print(user_messages)
    
    if len(user_messages) >= 1:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gemini_2_0_flash_thinking,
            provider=g4f.Provider.Gemini,
            messages=[
                {"role" : "system", "content" : "You are not an AI and not an assistant, you are dansk teacher for ukrainian students with danish level B1-B2 (You can translate words sometimes to ukrainian if necessery, when you should explore something)!"},
            ] + user_messages,
            # stream=True
            cookies={
                "__Secure-1PSID" : "g.a000uAjUAPGE2J6ekF4LhheHgMDw5GYKcCDVAwXpUuPwNxhTtnOSKNjcq94JDydHwEv_6944DwACgYKAQ4SARcSFQHGX2Mi8HhBsDLzBOqq2SpNhqNE5BoVAUF8yKrQhP7gITbDFCO7DgnbQa9n0076",
                "__Secure-1PSIDTS" : "sidts-CjEBEJ3XVzFUPJvJ2tVPJI0vq0f93Pi0RzyEtQK4tB4A4vUntGyXNPswjiIUxm1GLqjQEAA",
                "__Secure-1PSIDCC" : "AKEyXzXCg77ACIuB3DGQPD9akIWRsu4iVY6rxQUvSidOPVgQjkCsR1ukaEdNxQ9W4JwfihaMmrIi"
            }
        )

        text = ""
        counter = 0
        message_for_translate = ""
        bot_message = bot.send_message(user_message.chat.id, "[...](https://t.me/YaroTest1_bot?start)", parse_mode="Markdown", disable_web_page_preview=True)
        for i in response.split("\n\n\n\n\n\n")[1]:
            if i != "*":
                if i.isalpha() == True and message_for_translate == "":
                    # text += "["
                    # text += i
                    message_for_translate += i
                elif i.isalpha() == False and message_for_translate != "":
                    text += f"[{message_for_translate}](https://t.me/YaroTest1_bot?start={message_for_translate}_translate)"
                    text += i
                    message_for_translate = ""
                elif i.isalpha() == True and message_for_translate != "":
                    # text += i
                    message_for_translate += i
            if counter > 100:
                try:
                    bot.edit_message_text(text, bot_message.chat.id, bot_message.id, parse_mode="Markdown", disable_web_page_preview=True)
                except:
                    time.sleep(1)
                    # bot.edit_message_text(text, bot_message.chat.id, bot_message.id, parse_mode="Markdown", disable_web_page_preview=True)
                counter = 0
            counter += 1
        try:
            messages_list[str(user_message.chat.id)].append({"role" : "assistant", "content" : text})
            bot.edit_message_text(text, bot_message.chat.id, bot_message.id, parse_mode="Markdown", disable_web_page_preview=True)
            print(text)
        except Exception as err:
            print(err)
        return messages_list