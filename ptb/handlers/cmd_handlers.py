from ptb.keyboards import keyboard
from . import states_bot


async def start(update, context):
    text = "Главное меню"

    await update.message.reply_text(
        text,
        reply_markup=keyboard.main_menu_kb
    )

    return states_bot.MAIN_MENU
