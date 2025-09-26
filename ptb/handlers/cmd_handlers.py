from ptb.keyboards import keyboard
from . import states_bot


async def start(update, context):
    text = '''✨ *Превратим эмоции в цветы!*

Каждый букет — это история. Для какого момента создадим вашу?
• Готовые поводы ниже
• Или свой особенный случай'''

    await update.message.reply_text(
        text,
        reply_markup=keyboard.main_menu_kb,
        parse_mode='Markdown'
    )

    return states_bot.MAIN_MENU
