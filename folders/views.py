from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Folder
from locations.models import Location
import json


@login_required     # 로그인 상태 확인
def get_folders(request):
    # 모든 폴더 객체 가져옴, 업데이트 날짜 순 조회
    folders = request.user.folder_set.all()

    # 각 폴더에 대한 정보 JSON 형태로 반환
    folder_list = []
    for folder in folders:
        folder_info = {
            'name': folder.name,
            'locations_count': folder.locations.count(),     # 저장된 장소의 수
            'updated': folder.updated.strftime('%Y-%m-%d %H:%M:%S'),    # 날짜와 시간을 문자열로 변환
        }
        folder_list.append(folder_info)

    return JsonResponse(folder_list, safe=False)


@csrf_exempt  # CSRF 보호 비활성화 (테스트 용도)
@login_required     # 로그인 상태 확인
def create_folder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '')
            if name:
                folder = Folder.create_folder(name, user=request.user)
                return JsonResponse({'message': '폴더가 생성되었습니다.', 'folder_id': folder.id})
            else:
                return JsonResponse({'message': '폴더 이름을 제공해야 합니다.'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'POST 요청을 사용하세요.'}, status=400)


@csrf_exempt  # 임시로 CSRF 보호 비활성화 (테스트 용도)
@login_required     # 로그인 상태 확인
def add_location_to_folder(request):    # 폴더에 장소 저장
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            folder_id = data.get('folder_id')
            location_name = data.get('location_name')

            if folder_id and location_name:
                folder = get_object_or_404(Folder, pk=folder_id)    # get_object_or_404를 통해 존재하지 않는 객체 처리
                location = get_object_or_404(Location, name=location_name)
                folder.locations.add(location)
                return JsonResponse({'message': '장소가 폴더에 추가되었습니다.'})
            else:
                return JsonResponse({'message': '폴더 ID와 장소 이름을 제공해야 합니다.'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'POST 요청을 사용하세요.'}, status=400)


@login_required     # 로그인 상태 확인
def folder_locations(request, folder_id):   # 특정 폴더 내 장소 목록 조회
    folder = get_object_or_404(Folder, id=folder_id)
    location_names = list(folder.locations.values_list('name', flat=True))
    response_data = {
        'folder_name': folder.name,
        'location_names': location_names,
    }
    return JsonResponse(response_data)