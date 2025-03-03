import telebot
from translate import translate
from ai import ai_message
from tests import translate_text

bot = telebot.TeleBot("7912914148:AAFwSMvaK5mIjCkjCLFs7L_FtBlJ0KTtlHI")

messages_list = {}

@bot.message_handler()
def messages_function(message):
    if message.text.endswith("_translate") and message.text.startswith("/start"):
        all_commands = message.text.split(" ")
        if len(all_commands) > 1:
            if all_commands[1].endswith("_translate"):
                bot.delete_message(message.chat.id, message.id)
                print("Translate")
                print(message.text)
                translate_text("danish", "ukrainian", all_commands[1].split("_translate")[0], bot, message.chat.id)
                # messages_list = ai_message(message, bot, messages_list)
    elif message.text.endswith("_hide") and message.text.startswith("/start"):
        all_commands = message.text.split(" ")
        if len(all_commands) > 1:
            if all_commands[1].endswith("_hide"):
                bot.delete_message(message.chat.id, message.id)
                bot.delete_message(message.chat.id, int(all_commands[1].split("_hide")[0]))
    else:
        ai_message(message, bot)
    


bot.infinity_polling(timeout=20)