import logging
import os
import requests
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
)
from telegram.ext.filters import Filters
from telegram.update import Update

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

import settings

token = os.environ.get('BOT_TOKEN')
updater = Updater(token)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Merhaba! Wikipedia botuna hoşgeldiniz! Bir şey bulmak için /search  ve isteğinizi yazın. Örn: /search Mustafa Kemal Atatürk"
    )


def search(update: Update, context: CallbackContext):
    args = context.args

    logging.info("checking args length")

    if len(args) == 0:
        update.message.reply_text(
            "Lütfen bir şey yazın. Örn: /search Osmanlı Devleti"
        )
    else:
        search_text = " ".join(args)
        logging.info("sending request to Wikipedia API")
        response = requests.get(
            "https://tr.wikipedia.org/w/api.php",
            {
                "action": "opensearch",
                "search": search_text,
                "limit": 1,
                "namespace": 0,
                "format": "json",
            },
        )

        logging.info("result from Wikipedia API")
        result = response.json()
        link = result[3]

        if len(link):
            update.message.reply_text("Links found: " + link[0])
        else:
            update.message.reply_text("Nothing Found")


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("search", search))
dispatcher.add_handler(MessageHandler(Filters.all, start))

updater.start_polling()
updater.idle()
