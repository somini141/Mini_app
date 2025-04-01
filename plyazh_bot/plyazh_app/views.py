from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Country, TourRequest
import json


def index(request):
    countries = Country.objects.all()
    return render(request, 'index.html', {'countries': countries})


def submit_request(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            country = Country.objects.get(id=data['country_id'])

            TourRequest.objects.create(
                name=data['name'],
                surname=data['surname'],
                email=data['email'],
                phone=data['phone'],
                country=country
            )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})