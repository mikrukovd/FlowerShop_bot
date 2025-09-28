import random
from asgiref.sync import sync_to_async
from . import states_bot
from .utils_handler import (
    send_pdf, format_date_for_display,
    format_time_for_display, send_order_to_courier, send_consultation_to_florist
)
from ptb.keyboards.keyboard import (
    shade_menu_kb, price_kb, choose_flowers_kb, delivery_date_kb,
    confirm_order_kb, main_menu_kb, yes_no_kb, occasions,
    generate_remove_flower_kb, opd_kb, all_flowers_kb, generate_delivery_time_kb,
    back_to_main_menu_kb
)
from core.services import (
    get_all_colors, get_bouquets, get_bouquet,
    get_all_bouquets, get_bouquet_composition_names
)

async_get_all_colors = sync_to_async(get_all_colors)
async_get_bouquets = sync_to_async(get_bouquets)
async_get_bouquet = sync_to_async(get_bouquet)
async_get_all_bouquets = sync_to_async(get_all_bouquets)
async_get_bouquet_composition_names = sync_to_async(get_bouquet_composition_names)
async_generate_remove_flower_kb = sync_to_async(generate_remove_flower_kb)


async def handler_main_menu(update, context):
    '''Обработчик главного меню'''
    query = update.callback_query
    await query.answer()

    if query.data == "any_reason":
        await query.edit_message_text(
            text="Напишите, к какому событию готовимся?",
            reply_markup=None
        )
        return states_bot.OTHER_EVENT

    elif query.data.startswith("occasion_"):
        occasion_id = query.data.replace("occasion_", "")

        for occasion in occasions:
            if str(occasion.id) == occasion_id:
                context.user_data['event'] = occasion.name
                context.user_data['occasion_id'] = occasion_id
                break

    await query.edit_message_text(
        text="Отлично! Теперь подберем оттенок, который вам по душе:",
        reply_markup=shade_menu_kb
    )
    return states_bot.SHADE_MENU


async def handler_shade_menu(update, context):
    '''Обработчик меню оттенков'''
    query = update.callback_query
    await query.answer()

    if query.data.startswith("color_"):
        color_id = query.data.replace("color_", "")

        colors = await async_get_all_colors()

        for color in colors:
            if str(color.id) == color_id:
                context.user_data['color'] = color.name
                context.user_data['color_id'] = color_id
                break
        else:
            context.user_data['color'] = "Не указано"
            context.user_data['color_id'] = None

    await query.edit_message_text(
        text="На какую сумму рассчитываете?",
        reply_markup=price_kb
    )
    return states_bot.PRICE_MENU


async def handler_price_menu(update, context):
    '''Обработчик меню цен'''
    query = update.callback_query
    await query.answer()

    occasion_id = context.user_data.get('occasion_id')
    color_id = context.user_data.get('color_id')

    price_filters = {}

    if query.data == "price_500":
        price_filters = {'start_price': 0, 'end_price': 500}
    elif query.data == "price_1000":
        price_filters = {'start_price': 501, 'end_price': 1000}
    elif query.data == "price_2000":
        price_filters = {'start_price': 1001, 'end_price': 2000}
    elif query.data == "price_more":
        price_filters = {'start_price': 2001}
    elif query.data == "price_any":
        price_filters = {}

    bouquets = await async_get_bouquets(
        occasion=occasion_id,
        color=color_id,
        **price_filters
    )

    if bouquets:
        bouquet = random.choice(bouquets)
        context.user_data['selected_bouquet'] = bouquet.id

        composition_names = await async_get_bouquet_composition_names(bouquet)
        composition_text = ", ".join(composition_names)

        text = (f"🌸 *{bouquet.name}* 🌸\n\n"
                f"{bouquet.discription}\n\n"
                f"*Состав:* {composition_text}\n"
                f"*Стоимость:* {bouquet.price} руб.\n\n"
                "*Хотите что-то еще более уникальное?* Подберите другой букет из нашей коллекции или закажите консультацию флориста")
    else:
        text = ("😔 *К сожалению, по вашим параметрам ничего не найдено*\n\n"
                "Попробуйте изменить критерии поиска или посмотрите всю нашу коллекцию")
        context.user_data['selected_bouquet'] = None

    await query.edit_message_text(
        text=text,
        reply_markup=choose_flowers_kb,
        parse_mode='Markdown'
    )
    return states_bot.FLOWERS


async def handler_flowers(update, context):
    '''Обработчик выбора букета'''
    query = update.callback_query
    await query.answer()

    if query.data == "confirm_flowers":
        if not context.user_data.get('selected_bouquet'):
            await query.edit_message_text(
                text="❌ Не удалось найти подходящий букет. Попробуйте изменить параметры поиска.",
                reply_markup=main_menu_kb
            )
            return states_bot.MAIN_MENU

        text = "Хотите убрать какой-нибудь цветок из букета?"
        await query.edit_message_text(
            text=text,
            reply_markup=yes_no_kb
        )
        return states_bot.REMOVE_FLOWER

    elif query.data == "all_flowers":
        await query.edit_message_text(
            text="🌸 *Вся наша коллекция букетов:*",
            reply_markup=all_flowers_kb,
            parse_mode='Markdown'
        )
        return states_bot.ALL_FLOWERS

    elif query.data.startswith("bouquet_"):
        bouquet_id = query.data.replace("bouquet_", "")

        selected_bouquet = await async_get_bouquet(int(bouquet_id))
        context.user_data['selected_bouquet'] = selected_bouquet.id

        composition_names = await async_get_bouquet_composition_names(selected_bouquet)
        composition_text = ", ".join(composition_names)

        text = (f"🌸 *{selected_bouquet.name}* 🌸\n\n"
                f"{selected_bouquet.discription}\n\n"
                f"*Состав:* {composition_text}\n"
                f"*Стоимость:* {selected_bouquet.price} руб.\n\n"
                "*Хотите что-то еще более уникальное?* Подберите другой букет из нашей коллекции или закажите консультацию флориста")

        await query.edit_message_text(
            text=text,
            reply_markup=choose_flowers_kb,
            parse_mode='Markdown'
        )
        return states_bot.FLOWERS

    elif query.data == "need_consult":
        await query.delete_message()
        await send_pdf(query, opd_kb)
        return states_bot.OPD_CONSULT

    return states_bot.FLOWERS


async def handler_all_flowers(update, context):
    '''Обработчик всей коллекции букетов'''
    query = update.callback_query
    await query.answer()

    if query.data.startswith("bouquet_"):
        bouquet_id = query.data.replace("bouquet_", "")

        selected_bouquet = await async_get_bouquet(int(bouquet_id))
        context.user_data['selected_bouquet'] = selected_bouquet.id

        composition_names = await async_get_bouquet_composition_names(selected_bouquet)
        composition_text = ", ".join(composition_names)

        text = (f"🌸 *{selected_bouquet.name}* 🌸\n\n"
                f"{selected_bouquet.discription}\n\n"
                f"*Состав:* {composition_text}\n"
                f"*Стоимость:* {selected_bouquet.price} руб.\n\n"
                "*Хотите что-то еще более уникальное?* Подберите другой букет из нашей коллекции или закажите консультацию флориста")

        await query.edit_message_text(
            text=text,
            reply_markup=choose_flowers_kb,
            parse_mode='Markdown'
        )
        return states_bot.FLOWERS

    return states_bot.ALL_FLOWERS


async def handler_remove_flower(update, context):
    '''Обработчик удаления цветка'''
    query = update.callback_query
    await query.answer()

    if query.data == "yes":
        selected_bouquet_id = context.user_data.get('selected_bouquet')

        if not selected_bouquet_id:
            await query.edit_message_text(
                text="❌ Ошибка: букет не выбран",
                reply_markup=main_menu_kb
            )
            return states_bot.MAIN_MENU

        remove_flower_kb = await async_generate_remove_flower_kb(selected_bouquet_id)

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
        await query.message.reply_text("📝 Как к вам можно обращаться? Укажите ваше имя:")
        return states_bot.NAME

    elif query.data == "decline":
        text = '''✨ *Превратим эмоции в цветы!*

Каждый букет — это история. Для какого момента создадим вашу?
• Готовые поводы ниже
• Или свой особенный случай'''
        await query.delete_message()
        await query.message.reply_text(text=text, reply_markup=main_menu_kb)
        return states_bot.MAIN_MENU

    return states_bot.OPD


async def handler_name(update, context):
    '''Обработчик ввода имени'''
    context.user_data['name'] = update.message.text
    await update.message.reply_text("📞 Укажите ваш номер телефона для связи:")
    return states_bot.PHONE


async def handler_phone(update, context):
    '''Обработчик ввода телефона'''
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("🏠 На какой адрес доставить букет?")
    return states_bot.ADDRESS


async def handler_address(update, context):
    '''Обработчик ввода адреса'''
    context.user_data['address'] = update.message.text
    await update.message.reply_text(
        "📅 На какую дату планируете доставку?",
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
        text="⏰ В какое время вам будет удобно принять заказ?",
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
✅ *Проверьте ваш заказ:*

*Событие:* {context.user_data.get('event', 'Не указано')}
*Имя:* {context.user_data.get('name', 'Не указано')}
*Телефон:* {context.user_data.get('phone', 'Не указан')}
*Адрес:* {context.user_data.get('address', 'Не указан')}
*Дата:* {formatted_date}
*Время:* {formatted_time}
*Корректировки:* Убрать {context.user_data.get('removed_flower', 'без изменений')}
*Стоимость:* 1500 руб.

Всё верно?
"""
    await query.edit_message_text(
        text=order_summary,
        reply_markup=confirm_order_kb,
        parse_mode='Markdown'
    )
    return states_bot.CONFIRM_ORDER


async def handler_confirm_order(update, context):
    '''Обработчик подтверждения заказа'''
    query = update.callback_query
    await query.answer()

    if query.data == "confirm_order":
        await query.edit_message_text(
            text="🎉 *Заказ подтвержден!* Спасибо, что выбрали нас! Ожидайте доставку в указанное время.",
            reply_markup=back_to_main_menu_kb,
            parse_mode='Markdown'
        )
        # await send_order_to_courier(context, courier_chat_id=)  # TODO: Заменить на ID чата курьера
        # TODO: Внесение информации о заказе в базу данных
        return states_bot.ORDER_COMPLETED

    elif query.data == "cancel_order":
        await query.edit_message_text(
            text="❌ *Заказ отменен.* Если передумаете - будем рады помочь с выбором букета!",
            reply_markup=back_to_main_menu_kb,
            parse_mode='Markdown'
        )
        return states_bot.ORDER_COMPLETED

    return states_bot.CONFIRM_ORDER


async def handler_back_to_main(update, context):
    '''Обработчик возврата в главное меню'''
    query = update.callback_query
    await query.answer()
    text = '''✨ *Превратим эмоции в цветы!*

Каждый букет — это история. Для какого момента создадим вашу?
• Готовые поводы ниже
• Или свой особенный случай'''

    await query.edit_message_text(
        text=text,
        reply_markup=main_menu_kb
    )
    return states_bot.MAIN_MENU


async def handler_other_event(update, context):
    '''Обработчик другого события'''
    context.user_data['event'] = update.message.text
    context.user_data['occasion_id'] = None
    await update.message.reply_text(
        "Замечательно! Теперь подберем оттенок, который вам по душе:",
        reply_markup=shade_menu_kb
    )
    return states_bot.SHADE_MENU


async def handler_opd_consult(update, context):
    '''Обработчик согласия с ОПД для консультации'''
    query = update.callback_query
    await query.answer()

    if query.data == "accept":
        await query.delete_message()
        await query.message.reply_text("📝 Как к вам можно обращаться? Укажите ваше имя:")
        return states_bot.NAME_CONSULT

    elif query.data == "decline":
        text = '''✨ *Превратим эмоции в цветы!*

Каждый букет — это история. Для какого момента создадим вашу?
• Готовые поводы ниже
• Или свой особенный случай'''
        await query.delete_message()
        await query.message.reply_text(
            text=text,
            reply_markup=main_menu_kb
        )
        return states_bot.MAIN_MENU

    return states_bot.OPD_CONSULT


async def handler_name_consult(update, context):
    '''Обработчик ввода имени для консультации'''
    context.user_data['consult_name'] = update.message.text
    await update.message.reply_text("📞 Укажите номер телефона, и наш флорист перезвонит вам в течение 20 минут:")

    return states_bot.PHONE_CONSULT


async def handler_phone_consult(update, context):
    '''Обработчик ввода телефона для консультации'''
    context.user_data['consult_phone'] = update.message.text
    # await send_consultation_to_florist(context, florist_chat_id=)  # TODO: Заменить на ID чата флориста
    await update.message.reply_text(
        "✅ *Флорист скоро свяжется с вами!* А пока можете присмотреть что-нибудь из готовой коллекции:",
        reply_markup=all_flowers_kb,
        parse_mode='Markdown'
    )
    return states_bot.ALL_FLOWERS
