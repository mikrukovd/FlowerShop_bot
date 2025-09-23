from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# main_manu
btn_birthday = InlineKeyboardButton("день рождения", callback_data="birthday")
btn_wedding = InlineKeyboardButton("свадьба", callback_data="wedding")
btn_school = InlineKeyboardButton("в школу", callback_data="school")
btn_no_reason = InlineKeyboardButton("без повода", callback_data="no_reason")
btn_reason = InlineKeyboardButton("другой повод", callback_data="reason")

main_menu_kb = InlineKeyboardMarkup(
    [btn_birthday],
    [btn_wedding],
    [btn_school],
    [btn_no_reason],
    [btn_reason],
)
