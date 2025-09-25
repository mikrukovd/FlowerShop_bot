from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# main_menu
btn_birthday = InlineKeyboardButton("День рождения", callback_data="birthday")
btn_wedding = InlineKeyboardButton("Свадьба", callback_data="wedding")
btn_school = InlineKeyboardButton("В школу", callback_data="school")
btn_no_reason = InlineKeyboardButton("Без повода", callback_data="no_reason")
btn_any_reason = InlineKeyboardButton(
    "Другой повод",
    callback_data="any_reason"
)

# shade_menu
btn_shade = InlineKeyboardButton("Оттенок", callback_data="shade")

# price_menu
btn_price_500 = InlineKeyboardButton("~500", callback_data="price_500")
btn_price_1000 = InlineKeyboardButton("~1000", callback_data="price_1000")
btn_price_2000 = InlineKeyboardButton("~2000", callback_data="price_2000")
btn_price_more = InlineKeyboardButton("Больше", callback_data="price_more")
btn_price_any = InlineKeyboardButton("Не важно", callback_data="price_any")

# choose_flowers
btn_confirm_flowers = InlineKeyboardButton(
    "Заказать",
    callback_data="confirm_flowers"
)
btn_another_flowers = InlineKeyboardButton(
    "Выбрать другой букет",
    callback_data="another_flowers"
)
btn_need_consult = InlineKeyboardButton(
    "Заказать консультацию",
    callback_data="need_consult"
)

# remove_flower menu
btn_remove_flower = InlineKeyboardButton(
    "Убрать цветок",
    callback_data="remove_flower"
)
btn_remove_nothing = InlineKeyboardButton(
    "Не убирать ничего",
    callback_data="remove_nothing"
)

# opd
btn_accept = InlineKeyboardButton("Согласен", callback_data="accept")
btn_decline = InlineKeyboardButton("Не согласен", callback_data="decline")

# confirm_order
btn_confirm_order = InlineKeyboardButton(
    "Подтвердить заказ",
    callback_data="confirm_order"
)
btn_cancel_order = InlineKeyboardButton(
    "Отменить заказ",
    callback_data="cancel_order"
)

# delivery_date
btn_date_1 = InlineKeyboardButton("Дата 1", callback_data="date_1")

# delivery_time
btn_time_1 = InlineKeyboardButton("Время 1", callback_data="time_1")

# yes\no
btn_yes = InlineKeyboardButton("Да", callback_data="yes")
btn_no = InlineKeyboardButton("Нет", callback_data="no")


# keyboards

main_menu_kb = InlineKeyboardMarkup([
    [btn_birthday],
    [btn_wedding],
    [btn_school],
    [btn_no_reason],
    [btn_any_reason],
])

shade_menu_kb = InlineKeyboardMarkup([
    [btn_shade],
])

price_kb = InlineKeyboardMarkup([
    [btn_price_500],
    [btn_price_1000],
    [btn_price_2000],
    [btn_price_more],
    [btn_price_any],
])

choose_flowers_kb = InlineKeyboardMarkup([
    [btn_confirm_flowers],
    [btn_another_flowers],
    [btn_need_consult],
])

remove_flower_kb = InlineKeyboardMarkup([
    [btn_remove_flower],
    [btn_remove_nothing],
])

opd_kb = InlineKeyboardMarkup([
    [btn_accept],
    [btn_decline],
])

confirm_order_kb = InlineKeyboardMarkup([
    [btn_confirm_order],
    [btn_cancel_order],
])

delivery_date_kb = InlineKeyboardMarkup([
    [btn_date_1],
])

delivery_time_kb = InlineKeyboardMarkup([
    [btn_time_1],
])

yes_no_kb = InlineKeyboardMarkup([
    [btn_yes],
    [btn_no],
])
