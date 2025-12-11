from django.db import models


# Create your models here.
class CarInfomation(models.Model):
    id = models.AutoField('id', primary_key=True)
    brand = models.CharField('品牌', max_length=255, default='')
    carName = models.CharField('车名', max_length=255, default='')
    carImg = models.CharField('图片链接', max_length=255, default='')
    saleVolume = models.CharField('销量', max_length=255, default='')
    price = models.CharField('价格', max_length=255, default='')
    manufacturer = models.CharField('厂商', max_length=255, default='')
    rank = models.CharField('排名', max_length=255, default='')
    carModel = models.CharField('车型', max_length=255, default='')
    energyType = models.CharField('能源类型', max_length=255, default='')
    marketTime = models.CharField('上市时间', max_length=255, default='')
    insure = models.CharField('保修期时间', max_length=255, default='')
    creteTime = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'CarInfomation'


class User(models.Model):
    id = models.AutoField('id', primary_key=True)
    username = models.CharField('用户名', max_length=255, default='')
    password = models.CharField('密码', max_length=255, default='')  # 修复：将第二个username改为password
    creteTime = models.DateTimeField('创建时间', auto_now_add=True)  # 修复：改为DateTimeField

    class Meta:
        db_table = 'user'