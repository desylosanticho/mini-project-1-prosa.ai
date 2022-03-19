from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# Create your models here.
def upload_location(instance, filename):
    file_path = 'profile_pic/{user_id}/{user_user}-{filename}'.format(
        user_id = str(instance.id), user_user = str(instance.user), filename = filename
    )
    return file_path

"""  
class account(models.Model):
  nama = models.CharField(max_length=50)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  def name(self):
      return self.first_name + ", " + self.last_name

  def __str__(self):
      return self.name    
class NameUser(models.Model):
    def name(self):
        user = User.objects.all()
        first_name = first_name
        
        return self.first_name + " - " + self.last_name
"""

class Profile(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    photo_pict= models.ImageField(upload_to=upload_location, null=True, blank=True)
    