from django.http import JsonResponse
from .models import Location


def get_location_preview(request, location_id):     # 미리보기 모달, 해당 장소의 정보를 json 형태로 반환
    try:
        location = Location.objects.get(id=location_id)
        data = {
            'latitude': location.latitude,
            'longitude': location.longitude,
            'name': location.name,
        }
        return JsonResponse(data)
    except Location.DoesNotExist:
        return JsonResponse({'error': 'Location not found'}, status=404)
