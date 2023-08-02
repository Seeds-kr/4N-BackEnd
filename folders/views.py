from django.http import JsonResponse
from .models import Folder


def get_folders(request):   
    folders = Folder.objects.all()  # 모든 폴더 객체 가져옴
    folder_data = []
    for folder in folders:
        location_names = list(folder.locations.values_list('name', flat=True))  # 장소들의 이름을 리스트로 저장
        folder_data.append({
            'id': folder.id,
            'name': folder.name,
            'location': location_names,
        })
    return JsonResponse(folder_data, safe=False)
