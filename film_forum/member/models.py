from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Movies(models.Model):
    id = models.AutoField(primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=255)  # Field name made lowercase.
    year = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    introduction = models.TextField()
    link = models.CharField(max_length=255)
    img = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    star = models.TextField()
    type = models.CharField(max_length=255)

    class Meta:
        managed = True #代表需要Django幫你在資料庫建立這個table
        db_table = 'Movies' #資料庫內table的名字，預設會是django_space