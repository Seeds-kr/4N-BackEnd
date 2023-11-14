from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Post , Photo
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required #로그인시 필요
from accounts.models import User
import json



@method_decorator(csrf_exempt, name= 'dispatch') 
class PostListView(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            user_posts = Post.objects.filter(author_id=user_id)
            serialized_posts = []
            for post in user_posts:
                photo_list = Photo.objects.filter(post=post)
                post_info = {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "image_url": [photo.image.url for photo in photo_list],
                }
                serialized_posts.append(post_info)
            return JsonResponse({"user_posts": serialized_posts}, status=200)
        else:
            return JsonResponse({"message": "로그인이 필요합니다."}, status=401)


    def post(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            post = Post()
            post.title = request.POST['title']
            post.content = request.POST['content']
            post.locationid = request.POST['locationid']
            post.author = User.objects.get(id=user_id)
            post.save()

            for img in request.FILES.getlist('imgs'):
                photo = Photo()
                photo.image = img
                photo.save()
                post.photos.add(photo)  
            return JsonResponse({"message": "저장되었습니다."},status=200)
        else:
            return JsonResponse({"message" : "로그인이 필요합니다."},status = 400)




@method_decorator(csrf_exempt, name= 'dispatch')
class PostDetailView(View):   
    def post(self, request, post_id): #수정 뷰 
            post = get_object_or_404(Post, pk=post_id)
            author_id = request.session.get('user_id')
            print(post_id)
            if author_id != post.author.id:
                return JsonResponse({"message": "수정권한이 없습니다."}, status=400)
            
            post.title = request.POST['title']
            post.content = request.POST['content']
            post.author = User.objects.get(id=author_id)

            # 기존의 이미지를 모두 삭제
            post.photos.all().delete()

            for img in request.FILES.getlist('imgs'):
                    photo = Photo()
                    photo.image = img
                    photo.save()
                    post.photos.add(photo)  
            
            post.save()
            return JsonResponse({"message" : "수정되었습니다."},status=200)

    
    def delete(self , request , post_id):
        post = get_object_or_404(Post, id=post_id)
        user_id = request.session.get('user_id') 
        if user_id == post.author.id:
            post.photos.all().delete()
            post.delete()
            return JsonResponse({'message': '삭제되었습니다.'},status = 200)
        else:
            return JsonResponse({"message": "삭제 할 수 없습니다."}, status=403)
