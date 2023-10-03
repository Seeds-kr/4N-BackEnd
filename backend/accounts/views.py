import json
import requests
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# from django.contrib.auth import get_user_model
from django.shortcuts import redirect  
from django.contrib.auth import authenticate, login

from .models import User

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response





# Create your views here.

@method_decorator(csrf_exempt, name= 'dispatch')
def register(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        username = params.get('username')
        useremail = params.get('useremail') 
        password = params.get('password')
        re_password = params.get('re_password')
        #유효성 처리 
        res_data={}

        if password!=re_password:
            return JsonResponse({"message":"비밀번호가 다릅니다."},status=400)
        
        try:
            user = User.objects.get(useremail=useremail)
            if user:
                res_data['status'] = '0' # 기존 가입된 회원 
                return JsonResponse({"message":"가입된 회원입니다."},status=200)
        except User.DoesNotExist:
            user = User(
                username = username,
                useremail = useremail,
                password = make_password(password),
            )
            user.save()
            #session 생성
            user = User.objects.get(useremail=useremail)
            request.session['user'] = user.id
            print(request.session['user'])
            res_data['data'] = '1'#회원가입완료 
            res_data['message'] = '회원가입 완료'
            return JsonResponse({"message" : res_data},status = 200)
        
@method_decorator(csrf_exempt, name= 'dispatch')
def login(request):        
    if request.method == "POST":
        params = json.loads(request.body)
        useremail = params.get('useremail')
        password = params.get('password')

        if not (useremail and password):
            return JsonResponse({"message": "유저이름과 비밀번호를 입력해주세요."}, status=200)
        else:
            try:
                # 기존 DB에 있는 유저 모델 가져옴
                user = User.objects.get(useremail=useremail)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id  # 변경: 'user_id'로 세션에 저장
                    print(user.id)
                    request.session.save()
                    return JsonResponse({"message": '로그인 했습니다. '}, status=200)
                else:
                    return JsonResponse({"message": '비밀번호가 틀립니다.'}, status=400)
            except User.DoesNotExist:
                return JsonResponse({"message": '존재하지 않는 유저입니다.'}, status=400)
 
def logout(request):
    if request.method == "GET":
        if request.session.get('user_id') == None:
            return JsonResponse({"message":"로그인이 안되었습니다."},status=400)
        
        del request.session['user_id']
        return JsonResponse({"message":"로그아웃이 되었습니다."},status=200)
    
def findpassword(request):
    if request.method == "POST":
        params = json.loads(request.body)
        username = params.get('username')
        password = User.objects.get(username=username).password
        return JsonResponse({"message" : "비밀번호를 찾았습니다.", "password": password},status=200)
    

def changepassword(request):
    if request.method == "POST":
        params = json.loads(request.body)
        username = params.get("username")
        password = params.get("password")
        user = User.objects.get(username = username)

        if check_password(password, user.password): #지금 내 패스워드가 맞는지 확인
            new_password = params.get('new_password')
            password_confirm = params.get('re_password')

            if check_password(new_password, user.password): #지금 내 패스워드와 변경할 패스워드가 같은지 확인
                return JsonResponse({"message": "현재 비밀번호와 동일합니다."},status=200)

            if new_password == password_confirm:
                user.password = make_password(new_password)
                user.save()
                return JsonResponse({"message": "비밀번호가 변경되었습니다."},status=200)
            else:
                return JsonResponse({"message": "변경하실 비밀번호가 일치하지 않습니다."},status=400)
        else:
            return JsonResponse({"message": "현재 비밀번호가 틀립니다."} ,status=400)


def findid(request):
    if request.method == "POST":
        params = json.loads(request.body)
        useremail = params.get('useremail') 
        username = User.objects.get(useremail=useremail).username
        return JsonResponse({"message" : "유저아이디를 찾았습니다.", "username": username},status=200)
    
@method_decorator(csrf_exempt, name= 'dispatch')
def delete(request):
    if request.method == "DELETE":
        user_id = request.session.get("user_id")

        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                user.delete()
                return JsonResponse({"message": "회원탈퇴 성공"}, status=200)
            
            except User.DoesNotExist:
                return JsonResponse({"message": "회원을 찾을 수 없습니다."}, status=404)
            
        return JsonResponse({"message": "로그인된 회원이 아닙니다."}, status=401)
    else:
        return JsonResponse({"message": "잘못된 요청 메서드입니다."}, status=400)


KAKAO_TOKEN_API = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_API = "https://kapi.kakao.com/v2/user/me"
KAKAO_CALLBACK_URI ="http://localhost:8000/kakao"

@method_decorator(csrf_exempt, name= 'dispatch')
class KakaoLoginView(APIView):
    def get(self, request):
        code = request.GET["code"]
        if not code:
            return JsonResponse({"message" : "허가받지 않은 코드입니다."},status = 401)
        
        # kakao에 acces token 발급 요청
        data = {
          "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
          "grant_type": "authorization_code",
          "client_id": settings.KAKAO_REST_API_KEY, # 카카오 디벨로퍼 페이지에서 받은 rest api key
          "redirect_uri": "http://localhost:8000/kakaologin/",
          "code": code,
        }
        try:
            token = requests.post(KAKAO_TOKEN_API, data=data).json() # 받은 코드로 카카오에 access token 요청하기
            access_token =  token.get('access_token') # 받은 access token
            request.session['kakao_access_token'] = access_token
            # kakao에 user info 요청
            headers = {"Authorization": f"Bearer ${access_token}"}
            user_infomation = requests.get(KAKAO_USER_API, headers=headers).json() # 받은 access token 으로 user 정보 요청
            data = {'access_token': access_token, 'code': code}
            kakao_account = user_infomation.get('kakao_account')
            email = kakao_account.get('email') 
            try:
                kakao_users = User.objects.filter(useremail=email)
                kakao_name= kakao_account['profile']['nickname']
                if kakao_users.exists():
                    #기존회원과 동일한 이메일일 경우 
                    user = kakao_users.first()
                    kakao_name = kakao_account['profile']['nickname']
                    request.session['kakao_user'] = user.id
                    return Response({"message":"가입된 회원입니다."},status=200)
                else:
                    #간편회원가입
                    user = User.objects.create(
                        username = kakao_name,
                        useremail = email 
                    )
                    user.save()
                    request.session['kakao_user'] = user.id
                    return Response({"message":"간편회원가입이 완료되었습니다."},status=200)
            
            except User.DoesNotExist:
                #일반회원가입
                return Response ({"message" : "일반 회원가입"})

        except Exception as e:
            print(e)
            return Response({"message": "카카오로그인 오류가 발생했습니다."} , status=400) 

KAKAO_LOGOUT_API = "https://kapi.kakao.com/v1/user/logout"

class KakaoLogoutView(APIView):
    def post(self, request):
        access_token = request.session.get('kakao_access_token')
        if not access_token:
            return Response({"message": "토큰이 제공되지 않았습니다."}, status=400)
        
        # 카카오 API를 호출하여 해당 액세스 토큰으로 로그아웃 처리를 수행
        logout_data = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            # 카카오 로그아웃 요청 보내기
            logout_response = requests.post(KAKAO_LOGOUT_API, headers=logout_data)
            
            # 로그아웃에 성공하면 세션에서 사용자 정보를 삭제합니다.
            if logout_response.status_code == 200:
                if 'user' in request.session:
                    del request.session['user']
                if 'kakao_user' in request.session:
                    del request.session['kakao_user']
                return Response({"message": "로그아웃되었습니다."}, status=200)
            else:
                return Response({"message": "카카오로그아웃 오류가 발생했습니다."}, status=400)
        except requests.exceptions.RequestException as e:
            print(e)
            return Response({"message": "카카오로그아웃 오류가 발생했습니다."}, status=400)
        

KAKAO_UNLINK_API = "https://kapi.kakao.com/v1/user/unlink"
        
class KakaoUnLinkView(APIView):
     def post(self, request):
        access_token = request.session.get('kakao_access_token')
        if access_token:
            user_kakao_id = request.session.get('kakao_user')
            url = "https://kapi.kakao.com/v1/user/unlink"
            headers = {"Authorization": f"Bearer ${access_token}"}
            data = {"target_id_type": "user_id", "target_id": user_kakao_id}
            response = requests.post(url, headers=headers, data=data)
            deleted_user_id = response.json().get("id")
            if response.status_code == 200 and deleted_user_id:
                request.session.clear()  # 세션 정보 삭제
                """
                db삭제 로직 구현
                """
                return Response({"message": "연결 끊기 성공"}, status=200)
            else:
                return Response({"message": "연결 끊기 실패"}, status=400)
        else:
            return Response({"message": "액세스 토큰이 없습니다."}, status=400)
            
        

class NaverLoginView(APIView):
    def get(self,request):
        code = request.GET["code"]
        if not code:
            return JsonResponse({"message" : "허가받지 않은 코드입니다."},status = 401)
        
        try:
            token_url = 'https://nid.naver.com/oauth2.0/token'
            data = {
                'grant_type': 'authorization_code',
                'client_id': settings.NAVER_CLIENT_ID,
                'client_secret': settings.NAVER_CLIENT_SECRET,
                'redirect_uri': settings.NAVER_REDIRECT_URI,
                'code': code,
            }
            response = requests.post(token_url, data=data)
            token_json = response.json()

            # 액세스 토큰으로 사용자 정보 요청
            access_token = token_json.get('access_token')
            request.session['Naver_access_token'] = access_token
            me_url = 'https://openapi.naver.com/v1/nid/me'
            headers = {'Authorization': f'Bearer {access_token}'}
            me_response = requests.get(me_url, headers=headers)
            me_info = me_response.json()
            Naveremail = me_info['response']['email']

            try:
                Naver_users = User.objects.filter(useremail=Naveremail)
                Naver_name= me_info['response']['name']
                if Naver_users.exists():
                    #기존회원과 동일한 이메일일 경우 
                    user = Naver_users.first()
                    Naver_name = me_info['response']['name']
                    request.session['Naver_user'] = user.id
                    return Response({"message":"가입된 회원입니다."},status=200)
                else:
                    #간편회원가입
                    user = User.objects.create(
                        username = Naver_name,
                        useremail = Naveremail 
                    )
                    user.save()
                    request.session['Naver_user'] = user.id
                    return Response({"message":"간편회원가입이 완료되었습니다."},status=200)
            
            except User.DoesNotExist:
                return Response ({"message" : "일반 회원가입"})

        except Exception as e:
            return Response({"message": "네이버 로그인 오류가 발생했습니다."}, status=400)
        

Naverlogout_API = 'https://nid.naver.com/oauth2.0/token'

class NaverLogoutView(APIView):
    def post(self, request):
        access_token = request.session.get('Naver_access_token')
        if not access_token:
            return Response({"message": "토큰이 제공되지 않았습니다."}, status=400)
        
        # 네이버 API를 호출하여 해당 액세스 토큰으로 로그아웃 처리를 수행
        data = {
        'grant_type': 'delete',
        'client_id': settings.NAVER_CLIENT_ID,
        'client_secret': settings.NAVER_CLIENT_SECRET,
        'access_token': access_token,
        }

        try:
            # 네이버 로그아웃 요청 보내기
            response = requests.post(Naverlogout_API, data=data)
            
            # 로그아웃에 성공하면 세션에서 사용자 정보를 삭제합니다.
            if response.status_code == 200:
                if 'user' in request.session:
                    del request.session['user']
                if 'Naver_user' in request.session:
                    del request.session['Naver_user']
                return Response({"message": "로그아웃되었습니다."}, status=200)
            else:
                return Response({"message": "네이버 로그아웃 오류가 발생했습니다."}, status=400)
            
        except requests.exceptions.RequestException as e:
            return Response({"message": "네이버 로그아웃 오류가 발생했습니다."}, status=400)
        

class NaverUnLinkView(APIView):
    def post(self,request):
        access_token = request.session.get('Naver_access_token')
        print(access_token)
        if access_token:
            user_naver_id = request.session.get('Naver_user')
            url = "https://nid.naver.com/oauth2.0/token"
            headers = {"Authorization": f"Bearer {access_token}"}
            data = {
                'grant_type': 'delete',
                'client_id': settings.NAVER_CLIENT_ID,
                'client_secret': settings.NAVER_CLIENT_SECRET,
                "access_token": access_token
            }
            response = requests.post(url, headers=headers, data=data)
            
            if response.status_code == 200 and user_naver_id:
                request.session.clear()  # 세션 정보 삭제
                return Response({"message": "네이버 연결 끊기 성공"}, status=200)
            else:
                return Response({"message": "네이버 연결 끊기 실패"}, status=400)
        else:
            return Response({"message": "액세스 토큰이 없습니다."}, status=400)
        