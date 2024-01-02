from click import open_file
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from requests import get
from yaml import load as load_yaml, Loader
from djangoDiplom.celery import celery_app
from backend.models import *


@celery_app.task()
def password_reset_token_created_task(reset_password_token):
    """
       Отправляем письмо с токеном для сброса пароля
       # Когда токен создан, пользователю необходимо отправить электронное письмо.
       # :param sender: Просмотр класса, отправившего сигнал
       # :param instance: Просмотр экземпляра, отправившего сигнал
       # :param reset_password_token: Объект модели токена
       # :param kwargs:
       # :return:
   """
    # send an e-mail to the user

    msg = EmailMultiAlternatives(
        # title:
        f"Токен сброса пароля для {reset_password_token.user}",
        # message:
        reset_password_token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
    msg.send()


@celery_app.task()
def new_user_registered_task(user_id):
    """Отправляем письмо с подтверждением почты
    """
    # send an e-mail to the user
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)

    msg = EmailMultiAlternatives(
        # title:
        f"Токен сброса пароля для {token.user.email}",
        # message:
        token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [token.user.email]
    )
    msg.send()


@celery_app.task()
def new_order_task(user_id):
    """Отправляем письмо при изменении статуса заказа"""
    # send an e-mail to the user
    user = User.objects.get(id=user_id)

    msg = EmailMultiAlternatives(
        # title:
        f"Обновление статуса заказа",
        # message:
        'Заказ сформирован',
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user.email]
    )
    msg.send()


@celery_app.task()
def do_import_task(partner_id, url):
    """Импорт прайса от поставщика"""
    if url:
        validate_url = URLValidator()
        try:
            validate_url(url)
        except ValidationError as e:
            return {'Status': False, 'Error': str(e)}
        else:
            stream = get(url).content

            data = load_yaml(stream, Loader=Loader)
            print(data)
            file = open_file(data)
            print(file)
            shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=partner_id)

        for category in data['categories']:
            category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
            category_object.shops.add(shop.id)
            category_object.save()
