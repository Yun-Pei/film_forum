from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.db import models
from django.contrib.auth.models import Group, Permission

class Rank(models.Model):
    rid = models.AutoField(primary_key=True)
    rtype_choice = [(1, 'score'), (2, 'hot')]
    rtype = models.IntegerField(choices=rtype_choice)
    class Meta:
        managed = True #代表需要Django幫你在資料庫建立這個table
        db_table = 'Rank' #資料庫內table的名字，預設會是django_space  

class Movies(models.Model):
    mid = models.AutoField(primary_key=True)     
    rid = models.ForeignKey(Rank, on_delete=models.CASCADE, default=None, null=True)   
    time = models.CharField(max_length=255)     
    year = models.CharField(max_length=255)    
    name = models.CharField(max_length=255)     
    rating = models.IntegerField(default=-1)     
    age = models.CharField(max_length=255, default="R-12")    
    director = models.CharField(max_length=255, default="Frank Darabont")    
    star = models.TextField(default="Tim Robbins, Morgan Freeman, Bob Gunton")   
    introduction = models.TextField(default="Over the course of several year")    
    img = models.CharField(max_length=255, default='https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_QL75_UX140_CR0,1,140,207_.jpg')     
    tag = models.CharField(max_length=255, default="Drama")
    
    class Meta:
        managed = True #代表需要Django幫你在資料庫建立這個table
        db_table = 'Movies' #資料庫內table的名字，預設會是django_space  

class User(AbstractUser):
    img = models.CharField(max_length=255, default=1, null=True) #照片link
    history_browse = models.ManyToManyField(Movies, through="Browse")
    class Meta:
        managed = True #代表需要Django幫你在資料庫建立這個table
        db_table = 'User' #資料庫內table的名字，預設會是django_space
        # Add related_name to groups field


class MPreference(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    preference = models.CharField(max_length=255)

    class Meta:
        managed = True #代表需要Django幫你在資料庫建立這個table
        db_table = 'MPreference' #資料庫內table的名字，預設會是django_space  
        unique_together = ('uid', 'preference')    


class Browse(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE) #留言人
    mid = models.ForeignKey(Movies, on_delete=models.CASCADE)
    browseTime = models.DateTimeField()
    class Meta:
        managed = True #代表需要Django幫你在資料庫建立這個table
        db_table = 'Browse' #資料庫內table的名字，預設會是django_space  
        unique_together = ('uid', 'browseTime', 'mid')


class LikeMovies(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    mid = models.ForeignKey(Movies, on_delete=models.CASCADE)

    class Meta:
        managed = True #代表需要Django幫你在資料庫建立這個table
        db_table = 'LikeMovies' #資料庫內table的名字，預設會是django_space  
        unique_together = ('uid', 'mid')  

class Chatroom(models.Model):
    aid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    be_uid = models.IntegerField(null=False, blank=False)

    class Meta:
        managed = True #代表需要Django幫你在資料庫建立這個table
        db_table = 'Chatroom' #資料庫內table的名字，預設會是django_space  

class Message(models.Model):
    aid = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    time = models.DateTimeField()
    conent = models.TextField()

    class Meta:
        managed = True #代表需要Django幫你在資料庫建立這個table
        db_table = 'Message' #資料庫內table的名字，預設會是django_space  
        unique_together = ('aid', 'time')  

class Article(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    mid = models.ForeignKey(Movies, on_delete=models.CASCADE)
    art_id = models.AutoField(primary_key=True)
    time = models.DateTimeField()
    title = models.CharField(max_length=255)
    conent = models.TextField()

    class Meta:
        managed = True #代表需要Django幫你在資料庫建立這個table
        db_table = 'Article' #資料庫內table的名字，預設會是django_space  
        unique_together = ('mid', 'art_id')


class ArticleComment(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE) #留言人
    mid = models.ForeignKey(Movies, on_delete=models.CASCADE)
    art_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    time = models.DateTimeField()
    conent = models.TextField()

    class Meta:
        managed = True #代表需要Django幫你在資料庫建立這個table
        db_table = 'ArticleComment' #資料庫內table的名字，預設會是django_space  
        unique_together = ('uid', 'time')


# class MovieComment(models.Model):
#     uid = models.ForeignKey(User, on_delete=models.CASCADE)
#     mid = models.OneToOneField(Movies, on_delete=models.CASCADE)
#     Comment_id = models.AutoField(primary_key=True)
#     content = models.CharField(max_length=255)
#     score = models.IntegerField()
#     time = models.DateTimeField(default=None, null=True)

#     class Meta:
#         managed = True #代表需要Django幫你在資料庫建立這個table
#         db_table = 'MovieComment' #資料庫內table的名字，預設會是django_space  
#         unique_together = ('mid', 'Comment_id')

class MovieComments(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    mid = models.ForeignKey(Movies, on_delete=models.CASCADE, default=300)
    Comment_id = models.AutoField(primary_key=True)
    content = models.TextField(default="test") 
    score = models.IntegerField()
    time = models.DateTimeField(default=None, null=True)

    class Meta:
        managed = True #代表需要Django幫你在資料庫建立這個table
        db_table = 'MovieComments' #資料庫內table的名字，預設會是django_space  
        unique_together = ('mid', 'Comment_id')



