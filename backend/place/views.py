from django.shortcuts import render
from .models import Location
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


import json

@csrf_exempt
def save_location(request):
    if request.method == 'POST':
        user_id = request.session.get("user_id")
        # if user_id:
        data = json.loads(request.body)

        name = data.get('name')
        address = data.get('address')
        phone = data.get('phone')

        latitude_str = data.get('latitude')
        longitude_str = data.get('longitude')

        if latitude_str is None or longitude_str is None:
            return JsonResponse({'message': '위치 정보가 제공되지 않았습니다.'}, status=400)

        try:
            latitude = float(latitude_str)
            longitude = float(longitude_str)
        except ValueError:
            return JsonResponse({'message': '잘못된 위치 정보입니다.'}, status=400)

        
        location = Location(name=name, address=address, phone=phone, latitude=latitude, longitude=longitude)
        location.save()
        print(location.id) #저장 눌렀을때 장소 id확인
        return JsonResponse({'message': '성공적으로 저장되었습니다.'})

    return JsonResponse({'message': '허용되지 않는 메소드입니다.'}, status=400)


def alllocation(request):
    if request.method == "GET":
        all_locations = Location.objects.all()
        data = serializers.serialize('json', all_locations)
        return JsonResponse({'message': '서버에 저장된 모든 기록 가져오기', 'locations': json.loads(data)}, safe=False)
