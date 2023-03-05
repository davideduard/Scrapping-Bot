import logging
import os
import time

import bs4
import requests
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.updater import Updater

PORT = int(os.environ.get('PORT', '8443'))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '5235704142:AAEXQPOhu1L2aeGL-1Ex8NqnfUT8mpyDUOw'

last_link = ["asd"]

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text("Vei primi acum toate anunturile postate pe site-ul facultatii direct pe telefon sub forma de notificare.")
    link = get_last(update, context)
    while True:
        if (last_link[0] != link):
            link = get_last(update,context)
        time.sleep(3600)

def help(update, context):
    meniu = ""
    meniu += "Lista comenzilor: \n"
    meniu += "/start -> porneste botul\n"
    meniu += "/get_last -> afiseaza ultimul anunt de pe site\n"
    update.message.reply_text(meniu)

def get_last(update, context):
    URL = 'https://www.cs.ubbcluj.ro/anunturi/anunturi-studenti/'
    response = requests.get(URL).text
    soup = bs4.BeautifulSoup(response, 'html.parser')
    links = soup.find('h2', class_="title").find('a')['href']
    titlu = soup.find('h2', class_="title").find('a')['title']

    string = ""
    string += titlu + "\n" + links

    last_link.clear()
    last_link.append(links)

    update.message.reply_text(string)
    return links

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    updater.dispatcher.add_handler(CommandHandler("get_last", get_last))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
