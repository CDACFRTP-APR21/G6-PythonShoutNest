from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt
from .models import User

from app.models import User,Shouts,Friends,Reports
from app.serializers import UserSerializer,ShoutSerializer,FriendsSerializer,ReportsSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.core.files.storage import default_storage
import jwt, datetime


class RegisterView(APIView):
   
    @method_decorator(csrf_exempt)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request,format=None):
        print(request)
        userName = request.data['userName']
        print(userName)
        password = request.data['password']

        user = User.objects.filter(userName=userName,password=password).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

      

        payload = {
            'id': user.userId,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()
       
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'userId':user.userId,
            
            'userName':user.userName

        }
        return response



# Create your views here.
@csrf_exempt
def UserApi(request,id=0):
    if request.method=='GET':
        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)

    elif request.method=='POST':
        user_data=JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)
    
    elif request.method=='PUT':
        user_data = JSONParser().parse(request)
        user=User.objects.get(userId=user_data['userId'])
        user_serializer=UserSerializer(user,data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method=='DELETE':
        user=User.objects.get(userId=id)
        user.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)


@csrf_exempt
def SaveFile(request):
    file=request.FILES['uploadedFile']
    file_name = default_storage.save(file.name,file)
    

    return JsonResponse(file_name,safe=False)

@csrf_exempt
def ShoutsApi(request,id=0):
    if request.method=='GET':
        shouts = Shouts.objects.all()
        shouts_serializer = ShoutSerializer(shouts, many=True)
        return JsonResponse(shouts_serializer.data, safe=False)

    elif request.method=='POST':
        shouts_data=JSONParser().parse(request)
        shouts_serializer = ShoutSerializer(data=shouts_data)
        if shouts_serializer.is_valid():
            shouts_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)
    
    elif request.method=='PUT':
        shouts_data = JSONParser().parse(request)
        shouts=Shouts.objects.get(shoutId=shouts_data['shoutId'])
        shouts_serializer=ShoutSerializer(shouts,data=shouts_data)
        if shouts_serializer.is_valid():
            shouts_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method=='DELETE':
        shouts=Shouts.objects.get(shoutId=id)
        shouts.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)


@csrf_exempt
def FriendsApi(request,id=0):
    if request.method=='GET':
        friends = Friends.objects.all()
        friends_serializer = FriendsSerializer(friends, many=True)
        return JsonResponse(friends_serializer.data, safe=False)

    elif request.method=='POST':
        friends_data=JSONParser().parse(request)
        friends_serializer = FriendsSerializer(data=friends_data)
        if friends_serializer.is_valid():
            friends_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)
    
    elif request.method=='PUT':
        friends_data = JSONParser().parse(request)
        user=Friends.objects.all().filter(userId=friends_data['userId'],friendId=friends_data['friendId']).first()
        #print(user)
        #print(user[0].userId)
        user_serializer=FriendsSerializer(user,data=friends_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

        

    elif request.method=='DELETE':
        row1=Friends.objects.get(id=id)
        row1.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)





@csrf_exempt
def ReportsApi(request,id=0):
    if request.method=='GET':
        reports = Reports.objects.all()
        reports_serializer = ReportsSerializer(reports, many=True)
        return JsonResponse(reports_serializer.data, safe=False)

    elif request.method=='POST':
        reports_data=JSONParser().parse(request)
        reports_serializer = ReportsSerializer(data=reports_data)
        if reports_serializer.is_valid():
            reports_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)
    
    elif request.method=='PUT':
        reports_data = JSONParser().parse(request)
        reports=Reports.objects.get(shoutId=reports_data['reportId'])
        reports_serializer=ReportsSerializer(reports,data=reports_data)
        if reports_serializer.is_valid():
             reports_serializer.save()
             return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method=='DELETE':
        reports=Reports.objects.get(reportId=id)
        reports.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)



@csrf_exempt
def friendShoutsApi(request, UserId=0):
    if request.method == 'GET':
        if UserId != 0:
            friends=Friends.objects.filter(userId=UserId) | Friends.objects.filter(friendId=UserId)
            friends_serializers = FriendsSerializer(friends,many=True)
            friend_list=friends_serializers.data
            print('friendlist',friend_list)
            friends_set=set()
            for i in friend_list:
                if i['status']==3:
                    friends_set.add(i['friendId'])
            for i in friend_list:
                if i['status']==3:
                    friends_set.add(i['userId'])
            print('friendset',friends_set)

            shouts_list = list()

            for i in friends_set:
                shouts=Shouts.objects.filter(userId=i)
                shouts_serializer = ShoutSerializer(shouts,many=True)
                shouts_list.append(shouts_serializer.data)
            print('shoutlist',shouts_list)
            
            final_shouts_list=list()
            for i in shouts_list:
                for j in i:
                    final_shouts_list.append(j)
            print('final',final_shouts_list)

            """ user_list = list()

            for i in friends_set:
                fuser=User.objects.filter(userId=i)
                user_serializer = UserSerializer(fuser,many=True)
                user_list.append(user_serializer.data)
                print(' user',fuser)

            final_shouts_list.append(user_list)
            print('****appended list',final_shouts_list)
 """
            


        return JsonResponse(final_shouts_list,safe=False)
    return JsonResponse("Shouts not found..",safe=False)


@csrf_exempt
def DetailsOfFriendsApi(request, UserId=0):
    if request.method == 'GET':
        if UserId != 0:
            friends=Friends.objects.filter(userId=UserId) | Friends.objects.filter(friendId=UserId)
            friends_serializers = FriendsSerializer(friends,many=True)
            friend_list=friends_serializers.data
            print('friendlist',friend_list)
            friends_set=set()
            for i in friend_list:
                if i['status']==3:
                    friends_set.add(i['friendId'])
            for i in friend_list:
                if i['status']==3:
                    friends_set.add(i['userId'])
            print('friendset',friends_set)

            user_list = list()

            for i in friends_set:
                fuser=User.objects.filter(userId=i)
                user_serializer = UserSerializer(fuser,many=True)
                user_list.append(user_serializer.data)
                print(' user',fuser)

            
            


        return JsonResponse(user_list,safe=False)
    return JsonResponse(" not found..",safe=False)





