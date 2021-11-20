from django.db import models
import uuid

# Create your models here.



class Place(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, null=False, verbose_name=u'location uuid',help_text="location uuid")
    name = models.CharField(max_length=20, verbose_name='location name')
    place_id = models.CharField(max_length=50, verbose_name='GoogleMap place ID')
    lat = models.DecimalField(max_digits=15, decimal_places=10, verbose_name='GoogleMap place lat')
    lng = models.DecimalField(max_digits=15, decimal_places=10, verbose_name='GoogleMap place lng')
    score = models.IntegerField(verbose_name='score',default=5)
    is_startPlace = models.BooleanField(default=False, verbose_name='start location')

    class Meta:
        db_table = 'Place_info'  # 指明数据库表名
        verbose_name = 'location'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

class Path(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False, verbose_name=u'location uuid',help_text="location uuid")
    startPlace = models.ForeignKey(Place,on_delete=models.CASCADE,related_name='startplace')
    endPlace = models.ForeignKey(Place,on_delete=models.CASCADE,related_name='endPlace')
    distance = models.CharField(max_length=20,verbose_name='distance')
    duration = models.CharField(max_length=20,verbose_name='duration',default=0)


