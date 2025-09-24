from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# main_menu
btn_birthday = InlineKeyboardButton("День рождения", callback_data="birthday")
btn_wedding = InlineKeyboardButton("Свадьба", callback_data="wedding")
btn_school = InlineKeyboardButton("В школу", callback_data="school")
btn_no_reason = InlineKeyboardButton("Без повода", callback_data="no_reason")

# price_menu
btn_price_500 = InlineKeyboardButton("~500", callback_data="price_500")
btn_price_1000 = InlineKeyboardButton("~1000", callback_data="price_1000")
btn_price_2000 = InlineKeyboardButton("~2000", callback_data="price_2000")
btn_price_any = InlineKeyboardButton("Другая сумма", callback_data="price_any")

# flowers_menu
btn_flowers_1 = InlineKeyboardButton("Букет 1", callback_data="flowers_1")
btn_flowers_2 = InlineKeyboardButton("Букет 2", callback_data="flowers_2")
btn_another_flowers = InlineKeyboardButton(
    "Выбрать другой букет",
    callback_data="another_flowers"
)

# choose_flowers
btn_confirm_flowers = InlineKeyboardButton(
    "Заказать",
    callback_data="confirm_flowers"
)
btn_another_flowers = InlineKeyboardButton(
    "Выбрать другой букет",
    callback_data="another_flowers"
)

# opd
btn_accept = InlineKeyboardButton("Согласен", callback_data="accept")
btn_decline = InlineKeyboardButton("Не согласен", callback_data="decline")

# confirm_order
btn_confirm_order = InlineKeyboardButton(
    "Подтвердить заказ",
    callback_data="confirm_odrder"
)
btn_cancel_order = InlineKeyboardButton(
    "Отменить заказ",
    callback_data="cancel_order"
)

# delivery_date
btn_date_1 = InlineKeyboardButton("Дата 1", callback_data="data_1")
btn_date_2 = InlineKeyboardButton("Дата 2", callback_data="data_2")


# keyboards
main_menu_kb = InlineKeyboardMarkup([
    [btn_birthday],
    [btn_wedding],
    [btn_school],
    [btn_no_reason],
])

price_kb = InlineKeyboardMarkup([
    [btn_price_500],
    [btn_price_1000],
    [btn_price_2000],
    [btn_price_any],
])

flowers_kb = InlineKeyboardMarkup([
    [btn_flowers_1],
    [btn_flowers_2],
    [btn_another_flowers],
])

choose_flowers_kb = InlineKeyboardMarkup([
    [btn_confirm_flowers],
    [btn_another_flowers],
])

opd_kb = InlineKeyboardButton([
    [btn_accept],
    [btn_decline],
])

confirm_order_kb = InlineKeyboardMarkup([
    [btn_confirm_order],
    [btn_cancel_order],
])

delivery_date_kb = InlineKeyboardMarkup([
    [btn_date_1],
    [btn_date_2],
])
