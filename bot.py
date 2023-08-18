import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
import os
import re

# set up the introductory statement for the bot when the /start command is invoked
def start(update, context):
    print("### on start()")
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Paste a link and I'll unlock it...")

def _transform_link(orig_link):
    # first start with http cause sometimes the share button from android appends text at the beginning
    orig_link = "http" + orig_link.split("http")[1]

    # now handle the tokenization
    orig_link = orig_link.split("?")[0]
    orig_link = orig_link.split("/")
    result_link = []
    found_date_already = False
    for idx, tok in enumerate(orig_link):
        if re.search("^\d\d\d\d-\d\d-\d\d$", tok) != None:
            found_date_already = True
            result_link.append("tmr")
        if not found_date_already:              
            if idx <= 2:
                result_link.append(tok)
        else:
            if not tok.startswith("."):
                result_link.append(tok)
    result_link = ("/").join(result_link)
    return result_link

# obtain the information of the word provided and format before presenting.
def get_link(update, context):
    print("### on get_link()")
    # get the word info
    unlock_link = _transform_link(update.message.text)
    update.message.reply_text(unlock_link)
    return
    # format the data into a string
    # message = f"Word: {word}\n\nOrigin: {origin}\n{meanings}"


telegram_bot_token = os.environ['TGRM_TKN']
if telegram_bot_token != 'TEST':
    print("### Starting updater: " + telegram_bot_token)
    updater = Updater(token=telegram_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    # run the start function when the user invokes the /start command 
    dispatcher.add_handler(CommandHandler("start", start))

    # invoke the get_word_info function when the user sends a message 
    # that is not a command.
    dispatcher.add_handler(MessageHandler(Filters.text, get_link))

    # updater.start_polling()
    print("### Starting webhook")
    updater.start_webhook(listen="0.0.0.0",
                        port=int(os.environ.get('PORT', 5243)),
                        url_path=telegram_bot_token,
                        webhook_url= 'https://hrtzunlk-royabitbol.b4a.run/' + telegram_bot_token
                        # webhook_url= 'https://hrtzunlk.up.railway.app/' + telegram_bot_token
                        )
    print("### Started")
