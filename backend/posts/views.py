from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Post
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
            serialized_posts = [
                {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "image_url": post.image.url if post.image else None,
                }
                for post in user_posts
            ]
            return JsonResponse({"user_posts": serialized_posts}, status=200)
        else:
            return JsonResponse({"message": "로그인이 필요합니다."}, status=401)


    def post(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            author = request.session.get('user_id')
            title = request.POST['title']
            content = request.POST['content']
            img =   request.FILES.get('image')
            post = Post(
                author_id= author,
                title = title,
                content = content,
                image = img ,
            )
            post.save()
            return JsonResponse({"message": "저장되었습니다."}, status=200)
        else:
            return JsonResponse({"message": "로그인이 필요합니다."}, status=401)



@method_decorator(csrf_exempt, name= 'dispatch')
class PostDetailView(View):   
    def post(self, request, post_id): #수정 뷰 
            post = get_object_or_404(Post, pk=post_id)
            author_id = request.session.get('user_id')
            if author_id != post.author.id:
                return JsonResponse({"message": "수정권한이 없습니다."}, status=400)
            
            title = request.POST.get('title', post.title)
            content = request.POST.get('content', post.content)
            image = request.FILES.get('image', post.image)
            post.title = title
            post.content = content
            post.image = image
            post.save()

            return JsonResponse({"message": "글이 수정 되었습니다."}, status=200)
    
    def delete(self , request , post_id):
        post = get_object_or_404(Post, id=post_id)
        user_id = request.session.get('user_id') 
        if user_id == post.author.id:
            post.delete()
            return JsonResponse({'message': '삭제되었습니다.'},status = 200)
        else:
            return JsonResponse({"message": "삭제 할 수 없습니다."}, status=403)
