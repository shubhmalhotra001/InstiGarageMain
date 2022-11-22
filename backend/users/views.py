from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime, json
from django.http import HttpResponse

# endpoint to create a user
# /api/user/register
class RegisterView(APIView):
    def post(self, request):
        # serialize the user data that was in the request body 
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # add the user record into the database
        serializer.save()
        user = serializer.data

        payload = {
            'id': user['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        # Generate a jwt token for authentication 
        token = jwt.encode(payload, 'terces', algorithm='HS256').decode('utf-8')

        response = Response()

        # send the jwt token to the user (will be stored on the user's browser)
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'name': user['name'],
            'id':user['id'],
            'phone':user['phone'],
            'email':user['email'],
            'wallet':user['wallet'],
        }
        return response


# endpoint to login
# /api/user/login
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        # get user details
        user = User.objects.filter(email=email).first()
        response = Response()        

        # check if the user password combination is valid or not
        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=6000),
            'iat': datetime.datetime.utcnow()
        }

        # Generate a jwt token for future authentication
        token = jwt.encode(payload, 'terces', algorithm='HS256').decode('utf-8')

        response = Response()

        # send the jwt token to the user (will be stored on the user's browser)
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'name': user.name,
            'id':user.id,
            'phone':user.phone,
            'email':user.email,
            'wallet':user.wallet,
        }
        return response


# endpoint to get user details using jwt token
# /api/user/
class UserView(APIView):

    def get(self, request):

        # get jwt token from the authorization header field
        token = request.headers.get('Authorization')

        if not token:
            return HttpResponse(json.dumps({"error":"Unauthenticated!"}), content_type='application/json')

        # Authentication check using jwt
        try:
            token = token.split('=')[1]
            payload = jwt.decode(token, 'terces', algorithm=['HS256'])
        except Exception:
            return HttpResponse(json.dumps({"error":"Unauthenticated!"}), content_type='application/json')

        # return user details
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data) 
