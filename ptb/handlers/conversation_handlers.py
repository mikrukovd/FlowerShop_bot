from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)
from . import (
    callback_handlers,
    cmd_handlers,
    states_bot,
)

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("start", cmd_handlers.start)],
    states={
        states_bot.MAIN_MENU: [
            CallbackQueryHandler(callback_handlers.)
        ]
    }
)