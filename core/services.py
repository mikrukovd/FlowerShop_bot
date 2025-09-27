from .models import (
    User,
    Order,
    Bouquet,
    Composition,
    Occasion,
    Color,
)


def get_user(id_tg, user_name,):
    user, created = User.objects.get_or_create(
        id_tg=id_tg,
        defaults={
            "name": user_name,
            'id_tg': id_tg
        }        
    )
    return user


def get_all_bouquets():
    return list(Bouquet.objects.all())


def get_all_occasions():
    return list(Occasion.objects.all())


def get_all_colors():
    return list(Color.objects.all())


def get_bouquet(id):
    return Bouquet.objects.get(id=id)


def get_bouquets(occasion, color=None, start_price=None, end_price=None):
    filters = {}

    if occasion:
        filters['occasion'] = occasion

    if color:
        filters['color'] = color

    if start_price is not None:
        filters['price__gte'] = start_price

    if end_price is not None:
        filters['price__lte'] = end_price

    return list(Bouquet.objects.filter(**filters))


def create_order(user, name, address, phone, bouquet, delivery_date):
    Order.objects.create(
        user=user,
        name=name,
        address=address,
        phone=phone,
        bouquet=bouquet,
        delivery_date=delivery_date,
    )


def get_bouquet_composition_names(bouquet):
    return [comp.name for comp in bouquet.composition.all()]
