from datetime import datetime


async def edit_message(query, text, reply_markup):
    '''Редактор сообшения'''
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup
    )


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
