from django.db import models


# Create your models here.
class Face(models.Model):
    name = models.CharField(max_length=30,blank=False, verbose_name='姓名')
    work_id = models.CharField(max_length=30,blank=False, verbose_name='工作编号',unique=True)
    face_encode_str = models.CharField(max_length=300,blank=False, verbose_name="人脸编码值")
    update_time = models.DateField(auto_now=True, verbose_name="更改时间")

    def __str__(self):
        return self.name