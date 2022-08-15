# import asyncio
import os
from dotenv import load_dotenv

from enum import Enum
import requests

load_dotenv()

auth_token = os.getenv('auth_token')


class Category(Enum):
    consultation_litigation = "Судебный спор"
    consultation_business = "Деловые отношения и бизнес"
    consultation_property = "Жилье и недвижимость"
    consultation_copyright = "Интеллектуальные права"
    consultation_inheritance = "Семейное и наследственное право"
    consultation_bankrupt = "Долги и банкротство"
    consultation_pension = "Социальная и пенсионная сфера"
    consultation_other = "Другое"


class Type(Enum):
    consultation_other = "Другое"
    consultation_type_personal = "Консультация в офисе"
    consultation_type_phone = "Консультация по телефону"
    consultation_type_letter = "Консультация в письме"


def create_payment_consultation_task(name, phone, category, type, price):
    title = "Новый запрос: Платная консультация"
    description = f"Имя: {name}" \
        f"<br/>Телефон: {phone}" \
        f"<br/>Категория: {Category[category].value}" \
        f"<br/>Тип: {Type[type].value}" \
        f"<br/><br/>Цена: {price}"

    send_request(title, description)


def create_pro_bono_task(name, phone):
    title = "Новый запрос: PRO BONO"
    description = f"Имя: {name}" \
        f"<br/>Телефон: {phone}"

    send_request(title, description)


def create_angels_task(name, phone):
    title = "Новый запрос: Ангелы Права"
    description = f"Имя: {name}" \
        f"<br/>Телефон: {phone}"

    send_request(title, description)


def create_faq_task(name, phone, job):
    title = "Новый запрос: Правовые знания"
    description = f"Имя: {name}" \
        f"<br/>Телефон: {phone}" \
        f"<br/>Категория: {job}"

    send_request(title, description)


def create_payment_media_task(name, phone):
    title = 'Новый запрос: Рассказать на ТВ (платная консультация)'
    description = f"Имя: {name}" \
        f"<br/>Телефон: {phone}"

    send_request(title, description)


def create_club_task(name, phone):
    title = 'Новый запрос: Правовой клуб'
    description = f"Имя: {name}" \
        f"<br/>Телефон: {phone}"

    send_request(title, description)


def create_cooperation_task(name, phone, cooperation):
    title = 'Новый запрос: Сотрудничество'
    description = f"Имя: {name}" \
        f"<br/>Телефон: {phone}" \
        f"<br/>Категория: {cooperation}"

    send_request(title, description)


def send_request(title, description):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {auth_token}',
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
    }
    json_data = {
        'name': title,
        'description': description,
    }
    response = requests.post(
        'https://egorredin.planfix.ru/rest/task/', headers=headers, json=json_data)
    print(auth_token)
    print(response)
    print(response.text)
