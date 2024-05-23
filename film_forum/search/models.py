from django.db import models

# Create your models here.

# class TrieTree(models.Model):
#     tree_id = models.AutoField(primary_key=True)
#     movie_name = models.CharField(max_length=255)
#     data = models.TextField()
#     class Meta:
#         managed = True #代表需要Django幫你在資料庫建立這個table
#         db_table = 'TrieTree' #資料庫內table的名字，預設會是django_space  