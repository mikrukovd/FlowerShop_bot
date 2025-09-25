async def edit_message(query, text, reply_markup):
    '''Редактор сообшения'''
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup
    )
