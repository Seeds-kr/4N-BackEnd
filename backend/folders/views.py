from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Folder
from accounts.models import User
from place.models import Places
from django.views import View

import json


@method_decorator(csrf_exempt, name= 'dispatch') 
class FoldersView(View):
    def post(self , request): #폴더 생성 및 장소저장
        data = json.loads(request.body)
        
        title = data.get('title')
        user_id = request.session.get("user_id")
        places_data = data.get('places', [])

        if not title:
            return JsonResponse({'message' : "로그인 및 제목을 입력해주세요."},status=400)

        folder = Folder.objects.create(
            title=title,
            user_id="17"  # user_id로 나중에 대체.
        )

        for i, place_data in enumerate(places_data):
            latitude = place_data.get('latitude')
            longitude = place_data.get('longtitude')
            name = place_data.get('name', '') 
            address = place_data.get('address', '') 
            phone = place_data.get('phone', '')

            if latitude is None or longitude is None:
                return JsonResponse({'message': f'Missing "latitude" or "longitude" in place {i}'}, status=400)

            place = Places.objects.create(
                name=name,  # 제공되지 않을 경우 빈 칸으로 입력됨.
                address=address,  # 제공되지 않을 경우 빈 칸으로 입력됨.
                phone=phone,  # 제공되지 않을 경우 빈 칸으로 입력됨.
                latitude=float(latitude),
                longitude=float(longitude)
            )

            folder.locations.add(place)


        return JsonResponse({'message': '폴더에 장소를 성공적으로 저장하였습니다.'}, status=201)
        
        

        
