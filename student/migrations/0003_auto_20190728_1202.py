# Generated by Django 2.2.2 on 2019-07-28 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_qingjia_studentid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qingjia',
            name='is_xiao',
            field=models.CharField(choices=[('是', '是'), ('否', '否')], default='否', max_length=32),
        ),
        migrations.AlterField(
            model_name='qingjia',
            name='zhuangtai',
            field=models.CharField(choices=[('待审', '待审'), ('同意', '同意'), ('不同意', '不同意')], default='待审', max_length=32),
        ),
    ]
