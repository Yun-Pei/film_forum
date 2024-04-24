from django.db import models

# Create your models here.
class Forums(models.Model):
    f_id = models.AutoField(primary_key=True)
    m_id = models.IntegerField()
    time = models.DateTimeField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    user_id = models.IntegerField(default=1)

    class Meta:
        managed = True #代表需要Django幫你在資料庫建立這個table
        db_table = 'Forums' #資料庫內table的名字，預設會是django_space

class ForumsMessage(models.Model):
    f_id = models.ForeignKey(Forums, on_delete=models.CASCADE)
    m_id = models.ForeignKey(Forums, related_name='messages', on_delete=models.CASCADE)  # 设置 m_id 为外键
    time = models.DateTimeField()
    message_content = models.TextField()

    class Meta:
        managed = True #代表需要Django幫你在資料庫建立這個table
        db_table = 'ForumsMessage' #資料庫內table的名字，預設會是django_space
        unique_together = ('f_id', 'm_id', 'time', 'message_content')