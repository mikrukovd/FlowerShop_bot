from . import states_bot
from ptb.keyboards.keyboard import *


async def edit_message(query, text, reply_markup):
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup
    )


async def handler_main_menu(update, context):
