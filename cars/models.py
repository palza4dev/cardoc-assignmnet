from django.db    import models

from core.models  import TimeStampModel
from users.models import User

class Trim(TimeStampModel):
    name = models.CharField(max_length=100)
    car  = models.ForeignKey('Car', on_delete=models.CASCADE)
    user = models.ManyToManyField(User, through='UserTrim')
                                                                                                                                                                                    
    class Meta:
        db_table = 'trims'

class UserTrim(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trim = models.ForeignKey(Trim, on_delete=models.CASCADE)

    class Meta:
        db_table = 'users_trims'

class Car(TimeStampModel):
    brand_name    = models.CharField(max_length=50)
    model_name    = models.CharField(max_length=50)
    submodel_name = models.CharField(max_length=50)
    grade_name    = models.CharField(max_length=50)

    class Meta:
        db_table = 'cars'

class FrontTire(TimeStampModel):
    name         = models.CharField(max_length=50)
    value        = models.CharField(max_length=50)
    unit         = models.CharField(max_length=50, blank=True)
    multi_values = models.CharField(max_length=100, blank=True)
    width        = models.CharField(max_length=50)
    profile      = models.CharField(max_length=50)
    diameter     = models.CharField(max_length=50)
    trim         = models.ForeignKey(Trim, on_delete=models.CASCADE)

    class Meta:
        db_table = 'front_tires'

class RearTire(TimeStampModel):
    name         = models.CharField(max_length=50)
    value        = models.CharField(max_length=50)
    unit         = models.CharField(max_length=50, blank=True)
    multi_values = models.CharField(max_length=100, blank=True)
    width        = models.CharField(max_length=50)
    profile      = models.CharField(max_length=50)
    diameter     = models.CharField(max_length=50)
    trim         = models.ForeignKey(Trim, on_delete=models.CASCADE)

    class Meta:
        db_table = 'rear_tires'