from django.db   import models

from core.models import TimeStampModel

class User(TimeStampModel):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'users'