from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters
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
            CallbackQueryHandler(callback_handlers.handler_main_menu)
        ],
        states_bot.OTHER_EVENT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, callback_handlers.handler_other_event)
        ],
        states_bot.SHADE_MENU: [
            CallbackQueryHandler(callback_handlers.handler_shade_menu)
        ],
        states_bot.PRICE_MENU: [
            CallbackQueryHandler(callback_handlers.handler_price_menu)
        ],
        states_bot.FLOWERS: [
            CallbackQueryHandler(callback_handlers.handler_flowers)
        ],
        states_bot.REMOVE_FLOWER: [
            CallbackQueryHandler(callback_handlers.handler_remove_flower)
        ],
        states_bot.OPD: [
            CallbackQueryHandler(callback_handlers.handler_opd)
        ],
        states_bot.NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, callback_handlers.handler_name)
        ],
        states_bot.PHONE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, callback_handlers.handler_phone)
        ],
        states_bot.ADDRESS: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, callback_handlers.handler_address)
        ],
        states_bot.DATE: [
            CallbackQueryHandler(callback_handlers.handler_date)
        ],
        states_bot.TIME: [
            CallbackQueryHandler(callback_handlers.handler_time)
        ],
        states_bot.CONFIRM_ORDER: [
            CallbackQueryHandler(callback_handlers.handler_confirm_order)
        ],
    },
    fallbacks=[CommandHandler("start", cmd_handlers.start)],
)