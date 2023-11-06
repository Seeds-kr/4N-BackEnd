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
        user_id = request.session.get('user_id')
        print(user_id)
        if user_id:
            data = json.loads(request.body)
            title = data.get('title')
            user_id = data.get('user')
            places_data = data.get('places', [])

            if not title or not user_id :
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
        else:
              return JsonResponse({'message': 'xxxxxx'}, status=400)
    
@method_decorator(csrf_exempt, name='dispatch')
class FolderUpdateView(View):
    def post(self, request, folder_id):
        user_id = request.session.get('user_id')
         # 폴더 객체 가져오기. 없으면 404 에러 반환.
        folder = get_object_or_404(Folder, pk=folder_id)
        if user_id:
            data = json.loads(request.body)
            folder_id = data.get('folder_id')
            # 새로 추가할 장소 데이터 가져오기.
            new_places_data = data.get('places', [])

            # 새로운 장소들 추가하기.
            for place_data in new_places_data:
                place = Places.objects.create(
                    name=place_data.get('name', ''),
                    address=place_data.get('address', ''),
                    phone=place_data.get('phone', ''),
                    latitude=float(place_data['latitude']),
                    longtitude=float(place_data['longtitude'])
                )
                folder.locations.add(place)

            return JsonResponse({'message': '폴더가 성공적으로 업데이트되었습니다.'}, status=200)
        else:
             return JsonResponse({'message': '로그인이 필요합니다.'}, status=400)

    def put(self, request, folder_id):  # 폴더 title 수정
        user_id = request.session.get('user_id')
        folder = get_object_or_404(Folder, pk=folder_id)
        if user_id and folder.owner.id == user_id:  # 폴더 소유자 확인
            data = json.loads(request.body)
            new_title = data.get('title', folder.title)  # 새 제목이 입력되지 않으면 기존 제목 유지

            folder.title = new_title  # 제목 수정
            folder.save()

            return JsonResponse({'message': '폴더가 성공적으로 수정되었습니다.'}, status=200)

        else:
            return JsonResponse({'message': '로그인이 필요합니다.'}, status=400)

    def delete(self, request,folder_id):
        user_id = request.session.get('user_id') 
        folder = get_object_or_404(Folder, pk=folder_id)
        if user_id:
            data = json.loads(request.body)
            folder_id = data.get('folder_id')
            remove_place_ids = data.get('remove_place_ids', [])

            for place_id in remove_place_ids:
                try:
                    place_to_remove = Places.objects.get(id=place_id)
                    if place_to_remove not in folder.locations.all():
                        return JsonResponse({'message': '폴더에 저장된 장소가 없습니다.'}, status=400)
                    folder.locations.remove(place_to_remove)

                except Places.DoesNotExist:  
                    return JsonResponse({'message': '장소를 찾을 수 없습니다.'}, status=400)
                
            return JsonResponse({'message': '장소가 성공적으로 폴더에서 제거되었습니다.'}, status=200)
        else:
            return JsonResponse({'message': '로그인이 필요합니다.'}, status=400)


# class FolderListview(View):
#     def get(self,request):
#         folders = request.user.folder_set.all()
#         folder_list = [folder.title for folder in folders]
#         return JsonResponse( folder_list, safe=False,status=200)
        

        
