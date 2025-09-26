from datetime import datetime


async def send_pdf(query, reply_markup):
    '''Отправляет пдф'''
    with open("opd/opd.pdf", "rb") as pdf_file:
        await query.message.reply_document(
            document=pdf_file,
            caption="Согласие с обработкой персональных данных",
            reply_markup=reply_markup
        )


def format_date_for_display(date_str):
    '''Форматирует дату для отображения'''
    if date_str.startswith('date_'):
        date_str = date_str[5:]
        delivery_date = datetime.strptime(date_str, '%Y-%m-%d')
        return delivery_date.strftime('%d.%m.%Y')

    return date_str


def format_time_for_display(time_str):
    '''Форматирует время для отображения'''
    if time_str.startswith('time_'):
        time_code = time_str[5:]
        if len(time_code) == 4:
            return f"{time_code[:2]}:{time_code[2:]}"
    return time_str


async def send_order_to_courier(context, courier_chat_id):
    '''Отправляет заказ курьеру'''

    raw_date = context.user_data.get('date', '')
    formatted_date = format_date_for_display(raw_date)
    raw_time = context.user_data.get('time', '')
    formatted_time = format_time_for_display(raw_time)

    order_info = f"""
Новый заказ!
Событие: {context.user_data.get('event', 'Не указано')}
Имя: {context.user_data.get('name', 'Не указано')}
Телефон: {context.user_data.get('phone', 'Не указан')}
Адрес: {context.user_data.get('address', 'Не указан')}
Дата: {formatted_date}
Время: {formatted_time}
Удаленные цветы: {context.user_data.get('removed_flower', 'не удалялись')}
Цена: 1500 руб.
"""
    await context.bot.send_message(
        chat_id=courier_chat_id,
        text=order_info
    )
