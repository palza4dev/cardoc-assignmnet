import json, re
from json.decoder import JSONDecodeError

from django.views import View
from django.http  import JsonResponse

from cars.models  import Trim, UserTrim, Car, FrontTire, RearTire
from users.models import User
from users.utils  import login_decorator

class TrimListView(View):
    def post(self, request):
        try:
            data_list = json.loads(request.body)
            
            if len(data_list) > 5:
                return JsonResponse({'message' : 'TOO_MANY_DATA'}, status=400)

            for data in data_list:
                user = User.objects.get(username = data['id'])
                trim = Trim.objects.get(id = data['trimId'] )
                
                if UserTrim.objects.filter(user = user, trim = trim).exists():
                    return JsonResponse({'message' : 'ALREADY_EXISTS_DATA'}, status=400)
                
                UserTrim.objects.create(user = user, trim = trim)
                
                # 타이어 정보(value)의 구조 : {width}/{profile}R{diameter}
                
                front_tire             = data['frontTire']
                front_tire_value       = front_tire['value']
                front_tire_value_split = re.split('/|R', front_tire_value)
                
                FrontTire.objects.create(
                    name         = front_tire['name'],
                    value        = front_tire['value'],
                    unit         = front_tire['unit'],
                    multi_values = front_tire['multiValues'],
                    width        = front_tire_value_split[0],
                    profile      = front_tire_value_split[1],
                    diameter     = front_tire_value_split[2],
                    trim         = trim
                )
            
                rear_tire             = data['rearTire']
                rear_tire_value       = rear_tire['value']
                rear_tire_value_split = re.split('/|R', rear_tire_value)
                
                RearTire.objects.create(
                    name         = rear_tire['name'],
                    value        = rear_tire['value'],
                    unit         = rear_tire['unit'],
                    multi_values = rear_tire['multiValues'],
                    width        = rear_tire_value_split[0],
                    profile      = rear_tire_value_split[1],
                    diameter     = rear_tire_value_split[2],
                    trim         = trim
                )
            return JsonResponse({'message': 'created'}, status=201)
    
        except Trim.DoesNotExist:
            return JsonResponse({'message' : 'TRIM_DOES_NOT_EXIST'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'USER_DOES_NOT_EXIST'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        
    @login_decorator
    def get(self, request):
        
        if not UserTrim.objects.filter(user=request.user).exists:
            return JsonResponse({'message': 'USER_TRIM_DOES_NOT_EXIST'}, status=404)

        user_trim_list = [usertrim.trim.id for usertrim in UserTrim.objects.filter(user=request.user)]

        trims = Trim.objects.select_related('car').filter(id__in = user_trim_list).prefetch_related('fronttire_set','reartire_set')

        data = [{
            'brandName'    : trim.car.brand_name,
            'submodelName' : trim.car.submodel_name, 
            'gradeName'    : trim.car.grade_name,
            'trimId'       : trim.id,
            'trimName'     : trim.name,
            'frontTire'    : [{
                'name'         : front_tire.name,
                'value'        : front_tire.value,
                'multi_values' : front_tire.multi_values,
                'width'        : front_tire.width,
                'profile'      : front_tire.profile,
                'diameter'     : front_tire.diameter,
                } for front_tire in trim.fronttire_set.all()],
            'rearTire'    : [{
                'name'         : rear_tire.name,
                'value'        : rear_tire.value,
                'multi_values' : rear_tire.multi_values,
                'width'        : rear_tire.width,
                'profile'      : rear_tire.profile,
                'diameter'     : rear_tire.diameter,
                } for rear_tire in trim.reartire_set.all()]
            } for trim in trims]
        return JsonResponse({'data':data}, status=200)
        
        
class TrimDetailView(View):
    def get(self, request, trim_id):
        try:
            trim = Trim.objects.select_related('car').prefetch_related('fronttire_set','reartire_set').get(id=trim_id)
            front_tire = trim.fronttire_set.get(trim=trim)
            rear_tire  = trim.reartire_set.get(trim=trim)
            
            data = {
                'brandName'    : trim.car.brand_name,
                'submodelName' : trim.car.submodel_name, 
                'gradeName'    : trim.car.grade_name,
                'trimId'       : trim.id,
                'trimName'     : trim.name,
                'frontTire'    : {
                    'name'         : front_tire.name,
                    'value'        : front_tire.value,
                    'multi_values' : front_tire.multi_values,
                    },
                'rearTire'    : {
                    'name'         : rear_tire.name,
                    'value'        : rear_tire.value,
                    'multi_values' : rear_tire.multi_values,
                    }
                }  
            return JsonResponse({'data':data}, status=200)
        
        except Trim.DoesNotExist:
            return JsonResponse({'message': 'TRIM_DOES_NOT_EXIST'}, status=400)          
