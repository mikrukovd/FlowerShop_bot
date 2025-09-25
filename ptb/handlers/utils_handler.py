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
