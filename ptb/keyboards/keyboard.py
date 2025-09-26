from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
from core.services import get_all_occasions

# TODO: нужно будет переписать по другому
occasions = get_all_occasions()
occasion_buttons = []

for occasion in occasions:
    occasion_buttons.append([InlineKeyboardButton(
        occasion.name,
        callback_data=f"occasion_{occasion.id}"
    )])
btn_no_reason = InlineKeyboardButton("Без повода", callback_data="no_reason")
btn_any_reason = InlineKeyboardButton("Другой повод", callback_data="any_reason")

# main_menu_with_db
main_menu_buttons = occasion_buttons + [
    [btn_no_reason],
    [btn_any_reason],
]


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
    "Посмотреть всю коллекцию",
    callback_data="all_flowers"
)
btn_need_consult = InlineKeyboardButton(
    "Заказать консультацию",
    callback_data="need_consult"
)

# remove_flower_menu
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
def generate_delivery_date_kb():
    '''Генерация клавиатуры выбора даты'''
    weekdays_ru = {
        'Monday': 'пн', 'Tuesday': 'вт', 'Wednesday': 'ср', 'Thursday': 'чт',
        'Friday': 'пт', 'Saturday': 'сб', 'Sunday': 'вс'
    }

    months_ru = {
        'Jan': 'янв', 'Feb': 'фев', 'Mar': 'мар', 'Apr': 'апр',
        'May': 'май', 'Jun': 'июн', 'Jul': 'июл', 'Aug': 'авг',
        'Sep': 'сен', 'Oct': 'окт', 'Nov': 'ноя', 'Dec': 'дек'
    }

    today = datetime.now()
    buttons = []

    for i in range(0, 7, 2):  # 2 кнопки в строке
        row = []

        # Первая кнопка
        date1 = today + timedelta(days=i)
        day_ru1 = weekdays_ru[date1.strftime("%A")]
        month_ru1 = months_ru[date1.strftime("%b")]

        if i == 0:
            date_str1 = f"Сегодня ({date1.day} {month_ru1})"
        elif i == 1:
            date_str1 = f"Завтра ({date1.day} {month_ru1})"
        else:
            date_str1 = f"{date1.day} {month_ru1} ({day_ru1})"

        # Формат для бд: YYYY-MM-DD
        callback_data1 = f"date_{date1.strftime('%Y-%m-%d')}"
        row.append(InlineKeyboardButton(
            date_str1, callback_data=callback_data1
            )
        )

        # Вторая кнопка
        if i + 1 < 7:
            date2 = today + timedelta(days=i+1)
            day_ru2 = weekdays_ru[date2.strftime("%A")]
            month_ru2 = months_ru[date2.strftime("%b")]

            if i + 1 == 1:
                date_str2 = f"Завтра ({date2.day} {month_ru2})"
            elif i + 1 == 2:
                date_str2 = f"Послезавтра ({date2.day} {month_ru2})"
            else:
                date_str2 = f"{date2.day} {month_ru2} ({day_ru2})"

            callback_data2 = f"date_{date2.strftime('%Y-%m-%d')}"
            row.append(InlineKeyboardButton(
                date_str2,
                callback_data=callback_data2
                )
            )

        buttons.append(row)

    return InlineKeyboardMarkup(buttons)


# delivery_time
def generate_delivery_time_kb(callback_date=None):
    '''Генерация клавиатуры выбора времени с учетом текущего времени'''
    time_slots = [
        "09:00", "10:00", "11:00", "12:00",
        "13:00", "14:00", "15:00", "16:00",
        "17:00", "18:00", "19:00", "20:00"
    ]

    # Если передана выбранная дата и это сегодняшний день
    if callback_date and callback_date.startswith('date_'):
        selected_date_str = callback_date[5:]
        today_str = datetime.now().strftime('%Y-%m-%d')

        if selected_date_str == today_str:
            current_time = datetime.now()
            current_hour = current_time.hour
            current_minute = current_time.minute

            # Фильтрует слоты: оставляет только те, которые еще не прошли
            filtered_slots = []
            for time_slot in time_slots:
                slot_hour = int(time_slot.split(':')[0])
                slot_minute = int(time_slot.split(':')[1])

                if slot_hour > current_hour:
                    filtered_slots.append(time_slot)
                elif slot_hour == current_hour and slot_minute > current_minute:
                    filtered_slots.append(time_slot)

            time_slots = filtered_slots

    buttons = []

    for i in range(0, len(time_slots), 2):  # 2 кнопки в строке
        row = []

        # Первая кнопка в строке
        time1 = time_slots[i]
        row.append(InlineKeyboardButton(
            time1,
            callback_data=f"time_{time1.replace(':', '')}"
        ))

        # Вторая кнопка в строке
        if i + 1 < len(time_slots):
            time2 = time_slots[i + 1]
            row.append(InlineKeyboardButton(
                time2,
                callback_data=f"time_{time2.replace(':', '')}"
            ))

        buttons.append(row)

    return InlineKeyboardMarkup(buttons)


# yes\no
btn_yes = InlineKeyboardButton("Да", callback_data="yes")
btn_no = InlineKeyboardButton("Нет", callback_data="no")


# all_flowers
btn_all_flowers = InlineKeyboardButton(
    "Все цветы",
    callback_data="all_flowers"
)

# keyboards

main_menu_kb = InlineKeyboardMarkup(main_menu_buttons)

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

delivery_date_kb = generate_delivery_date_kb()

yes_no_kb = InlineKeyboardMarkup([
    [btn_yes],
    [btn_no],
])

all_flowers_kb = InlineKeyboardMarkup([
    [btn_all_flowers],
])
