import os

import django
from environs import Env
from telegram.ext import ApplicationBuilder


env = Env()
env.read_env()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flowers_shop.settings")
django.setup()

from ptb.handlers.conversation_handlers import conversation_handler


def main():
    app = ApplicationBuilder().token(env.str("TG_BOT_TOKEN")).build()
    app.bot_data.update({
        'courier_chat_id': env.str("COURIER_CHAT_ID"),
        'florist_chat_id': env.str("FLORIST_CHAT_ID")
    })
    app.add_handler(conversation_handler)
    app.run_polling()


if __name__ == "__main__":
    main()
