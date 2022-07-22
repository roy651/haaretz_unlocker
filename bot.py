import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
import os

telegram_bot_token = os.environ['TGRM_TKN']

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher

# set up the introductory statement for the bot when the /start command is invoked
def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Paste a locked link and I'll unlock it...")

def _transform_link(orig_link):
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
    # get the word info
    unlock_link = _transform_link(update.message.text)
    update.message.reply_text(unlock_link)
    return
    # format the data into a string
    # message = f"Word: {word}\n\nOrigin: {origin}\n{meanings}"

# run the start function when the user invokes the /start command 
dispatcher.add_handler(CommandHandler("start", start))

# invoke the get_word_info function when the user sends a message 
# that is not a command.
dispatcher.add_handler(MessageHandler(Filters.text, get_link))

# updater.start_polling()
updater.start_webhook(listen="0.0.0.0",
                      port=int(os.environ.get('PORT', 5243)),
                      url_path=telegram_bot_token,
                      webhook_url= 'https://hrtzunlk.herokuapp.com/' + telegram_bot_token
                      )