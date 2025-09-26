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
    app.add_handler(conversation_handler)
    app.run_polling()


if __name__ == "__main__":
    main()
