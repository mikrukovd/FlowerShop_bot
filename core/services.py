from .models import (
    User,
    Order,
    Bouquet,
    Composition,
    Occasion,
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


def get_bouquet(id):
    return Bouquet.objects.get(id=id)


def get_bouquets(occasion, start_price=None, end_price=None):
    if not start_price:
        return list(
            Bouquet.objects.filter(
                occasion=occasion,
            )
        )
    
    if not end_price:
        return list(
            Bouquet.objects.filter(
                occasion=occasion, 
                price__gte=start_price,
            )
        )

    return list(
        Bouquet.objects.filter(
            occasion=occasion, 
            price__gte=start_price,
            price__lte=end_price,
        )
    )


def create_order(user, name, address, phone, bouquet, delivery_date):
    Order.objects.create(
        user=user,
        name=name,
        address=address,
        phone=phone,
        bouquet=bouquet,
        delivery_date=delivery_date,
    )
