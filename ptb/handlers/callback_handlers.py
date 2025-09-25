from . import states_bot
from .utils_handler import (
    edit_message, send_pdf
)
from ptb.keyboards.keyboard import (
    shade_menu_kb, price_kb, choose_flowers_kb, delivery_date_kb,
    delivery_time_kb, confirm_order_kb, main_menu_kb, yes_no_kb,
    remove_flower_kb, opd_kb
)


async def handler_main_menu(update, context):
    '''Обработчик главного меню'''
    query = update.callback_query
    await query.answer()

    if query.data == "any_reason":
        await edit_message(query, "Выбор события:", None)
        return states_bot.OTHER_EVENT

    await edit_message(query, "Выбор оттенка:", shade_menu_kb)
    return states_bot.SHADE_MENU


async def handler_shade_menu(update, context):
    '''Обработчик меню оттенков'''
    query = update.callback_query
    await query.answer()

    await edit_message(query, "Выбор бюджета:", price_kb)
    return states_bot.PRICE_MENU


async def handler_price_menu(update, context):
    '''Обработчик меню цен'''
    query = update.callback_query
    await query.answer()

    # Заглушка для демонстрации букета
    text = "Ваш букет:\nФото \nСостав: Розы, тюльпаны, лилии\nОписание: Красивый букет\nЦена: 1500 руб."
    await edit_message(query, text, choose_flowers_kb)
    return states_bot.FLOWERS


async def handler_flowers(update, context):
    '''Обработчик выбора букета'''
    query = update.callback_query
    await query.answer()

    if query.data == "confirm_flowers":
        text = "Хотите убрать какой-нибудь цветок из букета?"
        await edit_message(query, text, yes_no_kb)
        return states_bot.REMOVE_FLOWER

    elif query.data == "another_flowers":
        await edit_message(query, "Выбор бюджета:", price_kb)
        return states_bot.PRICE_MENU

    elif query.data == "need_consult":
        # TODO: Тут переход к сценарию консультации
        await edit_message(query, "Консультация", main_menu_kb)
        return states_bot.MAIN_MENU

    return states_bot.FLOWERS


async def handler_remove_flower(update, context):
    '''Обработчик удаления цветка'''
    query = update.callback_query
    await query.answer()

    if query.data == "yes":
        text = "Какой цветок вы хотите убрать из букета?"
        await edit_message(query, text, remove_flower_kb)
        return states_bot.REMOVE_FLOWER

    elif query.data == "no":
        await query.delete_message()
        await send_pdf(query, opd_kb)
        return states_bot.OPD

    elif query.data.startswith("remove_"):
        removed_flower = query.data.replace("remove_", "")

        if removed_flower != "nothing":
            context.user_data['removed_flower'] = removed_flower

        await query.delete_message()
        await send_pdf(query, opd_kb)
        return states_bot.OPD

    return states_bot.REMOVE_FLOWER


async def handler_opd(update, context):
    '''Обработчик согласия с ОПД'''
    query = update.callback_query
    await query.answer()

    if query.data == "accept":
        await query.delete_message()
        await query.message.reply_text("Ввод имени")
        return states_bot.NAME

    elif query.data == "decline":
        await query.delete_message()
        await query.message.reply_text("Главное меню", reply_markup=main_menu_kb)
        return states_bot.MAIN_MENU

    return states_bot.OPD


async def handler_name(update, context):
    '''Обработчик ввода имени'''
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Ввод номера телефона")
    return states_bot.PHONE


async def handler_phone(update, context):
    '''Обработчик ввода телефона'''
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("Ввод адреса")
    return states_bot.ADDRESS


async def handler_address(update, context):
    '''Обработчик ввода адреса'''
    context.user_data['address'] = update.message.text
    await update.message.reply_text(
        "Выбор даты:",
        reply_markup=delivery_date_kb
    )
    return states_bot.DATE


async def handler_date(update, context):
    '''Обработчик выбора даты'''
    query = update.callback_query
    await query.answer()

    context.user_data['date'] = query.data
    await edit_message(query, "Выбор времени:", delivery_time_kb)
    return states_bot.TIME


async def handler_time(update, context):
    '''Обработчик выбора времени'''
    query = update.callback_query
    await query.answer()

    context.user_data['time'] = query.data

    # Формирование данных заказа
    order_summary = f"""
Ваш заказ:
Имя: {context.user_data.get('name', 'Не указано')}
Телефон: {context.user_data.get('phone', 'Не указан')}
Адрес: {context.user_data.get('address', 'Не указан')}
Дата: {context.user_data.get('date', 'Не указана')}
Время: {context.user_data.get('time', 'Не указано')}
Удаленные цветы: {context.user_data.get('removed_flower', 'не удалялись')}
Цена: 1500 руб.
"""
    await edit_message(query, order_summary, confirm_order_kb)
    return states_bot.CONFIRM_ORDER


async def handler_confirm_order(update, context):
    '''Обработчик подтверждения заказа'''
    query = update.callback_query
    await query.answer()

    if query.data == "confirm_order":
        await edit_message(query, "Заказ подтвержден!", None)

        # TODO: Тут отправка данных курьеру

        return states_bot.COMPLETE_ORDER

    elif query.data == "cancel_order":
        await edit_message(query, "Главное меню", main_menu_kb)
        return states_bot.MAIN_MENU

    return states_bot.CONFIRM_ORDER


async def handler_other_event(update, context):
    '''Обработчик другого события'''
    context.user_data['event'] = update.message.text
    await update.message.reply_text(
        "Выберите оттенок:",
        reply_markup=shade_menu_kb
    )
    return states_bot.SHADE_MENU
