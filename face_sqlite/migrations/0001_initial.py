# Generated by Django 3.1.4 on 2020-12-24 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Face',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='姓名')),
                ('work_id', models.CharField(max_length=30, verbose_name='工作编号')),
                ('face_encode_str', models.CharField(max_length=300, verbose_name='人脸编码值')),
                ('update_time', models.DateField(auto_now=True, verbose_name='更改时间')),
            ],
        ),
    ]
