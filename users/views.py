import json, re, jwt, bcrypt
from json.decoder    import JSONDecodeError

from django.http     import JsonResponse
from django.views    import View

from users.models    import User
from cardoc.settings import SECRET_KEY

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            username = data['id']
            password = data['password']

            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'USERNAME_ALREADY_EXIST'}, status=400)
            
            if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$", password):
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=404)

            User.objects.create(
                username = username,
                password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)
            
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            username = data['id']
            password = data['password']

            if not User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'INVALID_USERNAME'}, status=401)
            
            user = User.objects.get(username=username)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)
            
            access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')
            return JsonResponse({'access_token':access_token}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)