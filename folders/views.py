from django.http import JsonResponse
from .models import Folder, Location, FolderLocation


def get_folders(request):
    folder_data = []
    folders = Folder.objects.all()
    for folder in folders:
        location_list = folder.locations.all()  # 해당 folder에 속한 locations 가져옴
        location_names = [location.name for location in location_list]  # 윗줄에서 가져온 장소 목록 'location_list'에서 장소의 이름만을 추출하여 저장
        folder_data.append({    # 딕셔너리
            'id': folder.id,
            'name': folder.name,
            'location': location_names  # JSON 응답에 10줄에서 가져온 장소 이름들이 포함되도록...
        })
    return JsonResponse(folder_data, safe=False)
