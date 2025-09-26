from . import states_bot
from .utils_handler import (
    send_pdf, format_date_for_display,
    format_time_for_display, send_order_to_courier, send_consultation_to_florist
)
from ptb.keyboards.keyboard import (
    shade_menu_kb, price_kb, choose_flowers_kb, delivery_date_kb,
    confirm_order_kb, main_menu_kb, yes_no_kb, occasions,
    remove_flower_kb, opd_kb, all_flowers_kb, generate_delivery_time_kb
)


async def handler_main_menu(update, context):
    '''Обработчик главного меню'''
    query = update.callback_query
    await query.answer()

    if query.data == "any_reason":
        await query.edit_message_text(
            text="Выбор события:",
            reply_markup=None
        )
        return states_bot.OTHER_EVENT

    elif query.data.startswith("occasion_"):
        occasion_id = query.data.replace("occasion_", "")

        for occasion in occasions:
            if str(occasion.id) == occasion_id:
                context.user_data['event'] = occasion.name
                break

    elif query.data in ["no_reason"]:
        context.user_data['event'] = "Без повода"

    await query.edit_message_text(
        text="Выбор оттенка:",
        reply_markup=shade_menu_kb
    )
    return states_bot.SHADE_MENU


async def handler_shade_menu(update, context):
    '''Обработчик меню оттенков'''
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="Выбор бюджета:",
        reply_markup=price_kb
    )
    return states_bot.PRICE_MENU


async def handler_price_menu(update, context):
    '''Обработчик меню цен'''
    query = update.callback_query
    await query.answer()

    # Заглушка для демонстрации букета
    text = "Ваш букет:\nФото \nСостав: Розы, тюльпаны, лилии\nОписание: Красивый букет\nЦена: 1500 руб."
    await query.edit_message_text(
        text=text,
        reply_markup=choose_flowers_kb
    )
    return states_bot.FLOWERS


async def handler_flowers(update, context):
    '''Обработчик выбора букета'''
    query = update.callback_query
    await query.answer()

    if query.data == "confirm_flowers":
        text = "Хотите убрать какой-нибудь цветок из букета?"
        await query.edit_message_text(
            text=text,
            reply_markup=yes_no_kb
        )
        return states_bot.REMOVE_FLOWER

    elif query.data == "all_flowers":
        await query.edit_message_text(
            text="Букеты из всей коллекции",
            reply_markup=all_flowers_kb
        )
        return states_bot.ALL_FLOWERS

    elif query.data == "need_consult":
        await query.delete_message()
        await send_pdf(query, opd_kb)
        return states_bot.OPD_CONSULT

    return states_bot.FLOWERS


async def handler_all_flowers(update, context):
    '''Обработчик всей коллекции букетов'''
    query = update.callback_query
    await query.answer()

    if query.data == "all_flowers":
        text = "Ваш букет:\nФото \nСостав: Розы, тюльпаны, лилии\nОписание: Красивый букет\nЦена: 1500 руб."
        await query.edit_message_text(
            text=text,
            reply_markup=choose_flowers_kb
        )
        return states_bot.FLOWERS

    return states_bot.ALL_FLOWERS


async def handler_remove_flower(update, context):
    '''Обработчик удаления цветка'''
    query = update.callback_query
    await query.answer()

    if query.data == "yes":
        text = "Какой цветок вы хотите убрать из букета?"
        await query.edit_message_text(
            text=text,
            reply_markup=remove_flower_kb
        )
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
    delivery_time_kb = generate_delivery_time_kb(query.data)
    await query.edit_message_text(
        text="Выбор времени:",
        reply_markup=delivery_time_kb
    )
    return states_bot.TIME


async def handler_time(update, context):
    '''Обработчик выбора времени'''
    query = update.callback_query
    await query.answer()

    context.user_data['time'] = query.data

    raw_date = context.user_data.get('date', '')
    formatted_date = format_date_for_display(raw_date)

    raw_time = context.user_data.get('time', '')
    formatted_time = format_time_for_display(raw_time)

    # Формирование данных заказа
    order_summary = f"""
Ваш заказ:
Событие: {context.user_data.get('event', 'Не указано')}
Имя: {context.user_data.get('name', 'Не указано')}
Телефон: {context.user_data.get('phone', 'Не указан')}
Адрес: {context.user_data.get('address', 'Не указан')}
Дата: {formatted_date}
Время: {formatted_time}
Удаленные цветы: {context.user_data.get('removed_flower', 'не удалялись')}
Цена: 1500 руб.
"""
    await query.edit_message_text(
        text=order_summary,
        reply_markup=confirm_order_kb
    )
    return states_bot.CONFIRM_ORDER


async def handler_confirm_order(update, context):
    '''Обработчик подтверждения заказа'''
    query = update.callback_query
    await query.answer()

    if query.data == "confirm_order":
        await query.edit_message_text(
            text="Заказ подтвержден!",
            reply_markup=main_menu_kb
        )
        # await send_order_to_courier(context, courier_chat_id="")  # TODO: Заменить на ID чата курьера
        # TODO: Внесение информации о заказе в базу данных
        return states_bot.MAIN_MENU

    elif query.data == "cancel_order":
        await query.edit_message_text(
            text="Главное меню",
            reply_markup=main_menu_kb
        )
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


async def handler_opd_consult(update, context):
    '''Обработчик согласия с ОПД для консультации'''
    query = update.callback_query
    await query.answer()

    if query.data == "accept":
        await query.delete_message()
        await query.message.reply_text("Ввод имени")
        return states_bot.NAME_CONSULT

    elif query.data == "decline":
        await query.delete_message()
        await query.message.reply_text(
            "Главное меню",
            reply_markup=main_menu_kb
        )
        return states_bot.MAIN_MENU

    return states_bot.OPD_CONSULT


async def handler_name_consult(update, context):
    '''Обработчик ввода имени для консультации'''
    context.user_data['consult_name'] = update.message.text
    await update.message.reply_text("Ввод номера")

    return states_bot.PHONE_CONSULT


async def handler_phone_consult(update, context):
    '''Обработчик ввода телефона для консультации'''
    context.user_data['consult_phone'] = update.message.text
    # await send_consultation_to_florist(context, florist_chat_id="")  # TODO: Заменить на ID чата флориста
    await update.message.reply_text(
        "Все букеты",
        reply_markup=all_flowers_kb
    )
    return states_bot.ALL_FLOWERS
