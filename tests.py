import g4f
import g4f.Provider
import os

import telebot


def translate_text(from_lang, to_lang, message_to_translate, bot: telebot.TeleBot, chat_id):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gemini_2_0_flash,
        provider=g4f.Provider.Gemini,
        messages=[
            {"role" : "system", "content" : f"You are not an AI assistant, you are translator and all your answers it is ONLY translated text. You should tranlate text from {from_lang} to {to_lang}, you can also write sysnonymous and other variants of tranlation, every synonymoum shoud be ander first variant on new line and start with '* '!"},
            {"role" : "user", "content" : message_to_translate}
        ],
        stream=False,
        cookies={
            "__Secure-1PSID" : "g.a000uAjUAPGE2J6ekF4LhheHgMDw5GYKcCDVAwXpUuPwNxhTtnOSKNjcq94JDydHwEv_6944DwACgYKAQ4SARcSFQHGX2Mi8HhBsDLzBOqq2SpNhqNE5BoVAUF8yKrQhP7gITbDFCO7DgnbQa9n0076",
            "__Secure-1PSIDTS" : "sidts-CjEBEJ3XV8beZsXsM2Yzbm6eBmhVKWLg399RQZOnmXiPGrk2P9QdLokC7o2p7D3Wfp5WEAA",
            "__Secure-1PSIDCC" : "AKEyXzUCYndLrCFV_dXwNLz5eor8_eapJzlNVs69yAry8RqWe2kk896u7t7PmLburJMNl6R1z_WO"
        },
    )

    text = ""
    bot_message = bot.send_message(chat_id, "...", parse_mode="Markdown", disable_web_page_preview=True)
    counter = 0
    for i in response:
        text += i
        if counter > 50:
            bot.edit_message_text(text, chat_id, bot_message.id, chat_id, bot_message.id)
            counter = 0
        counter += 1
    bot.edit_message_text(f"{message_to_translate}\n{text}\n\n[Hide](https://t.me/YaroTest1_bot?start={bot_message.id}_hide)", chat_id, bot_message.id, parse_mode="Markdown", disable_web_page_preview=True)