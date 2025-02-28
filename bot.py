import telebot
from translate import translate
from ai import ai_message

bot = telebot.TeleBot("7912914148:AAFwSMvaK5mIjCkjCLFs7L_FtBlJ0KTtlHI")

messages_list = {}

@bot.message_handler()
def messages_function(message):
    if message.text.endswith("_translate"):
        all_commands = message.text.split(" ")
        if len(all_commands) > 1:
            if all_commands[1].endswith("_translate"):
                bot.delete_message(message.chat.id, message.id)
                print("Translate")
                messages_list = ai_message(message, bot, messages_list)
        bot.send_message(message.chat.id, "[Text](https://t.me/YaroTest1_bot?start=hello_translate)", parse_mode="Markdown", disable_web_page_preview=True)
    else:
        ai_message(message, bot, {})
    


bot.infinity_polling(timeout=20)