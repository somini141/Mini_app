# from django.contrib.sites import requests
# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from .models import Country, TourRequest
# import json
# from django.views.decorators.csrf import csrf_exempt
#
# TELEGRAM_BOT_TOKEN = '7780414878:AAERZUOT4Qiqh-CodPVArmqpI2yBObMlgCw'
# TELEGRAM_CHAT_ID = '-4729247445'
#
from django.shortcuts import render


def index(request):
    countries = Country.objects.all()
    return render(request, 'index.html', {'countries': countries})
#
#
# def submit_request(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             country = Country.objects.get(id=data['country_id'])
#
#             TourRequest.objects.create(
#                 name=data['name'],
#                 surname=data['surname'],
#                 email=data['email'],
#                 phone=data['phone'],
#                 country=country
#             )
#
#             return JsonResponse({'status': 'success'})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)})
#
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'})
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Country, TourRequest
import json


@csrf_exempt
def submit_request(request):
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            country_id = request.POST.get('country')

            # Получаем объект страны
            country = Country.objects.get(id=country_id)

            # Сохраняем заявку в базу
            tour_request = TourRequest.objects.create(
                name=name,
                surname=surname,
                email=email,
                phone=phone,
                country=country
            )

            # Отправка в Telegram бот
            bot_token = '7780414878:AAERZUOT4Qiqh-CodPVArmqpI2yBObMlgCw'
            chat_id = '-4729247445'
            message = (
                "🌴 Новая заявка на тур!\n\n"
                f"👤 Имя: {name} {surname}\n"
                f"📧 Email: {email}\n"
                f"📞 Телефон: {phone}\n"
                f"🌍 Страна: {country.name}\n"
                f"🆔 Номер заявки: {tour_request.id}"
            )

            send_telegram_message(bot_token, chat_id, message)

            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def send_telegram_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': text
    }
    try:
        response = requests.post(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return None