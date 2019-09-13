from django.db import models

# Create your models here.
gender = (
    ('male','男'),
    ('female','女'),
)
class JCLASS(models.Model):
    """ 教学班表"""
    weekday = (
        ('1', '星期一'),
        ('2', '星期二'),
        ('3', '星期三'),
        ('4', '星期四'),
        ('5', '星期五'),
        ('6', '星期六'),
        ('7', '星期日'),
    )
    jclassid = models.IntegerField(primary_key=True)
    startweek = models.IntegerField()
    endweek = models.IntegerField()
    week = models.CharField(max_length=10,choices=weekday,default='星期一')
    jieci = models.IntegerField()
    classroomid = models.IntegerField()

class CLASSROOM(models.Model):
    """教室表"""
    classroomid = models.IntegerField(primary_key=True)
    weizhi = models.CharField(max_length=20)

class LESSONS(models.Model):
    """ 课程表"""
    lessionid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10)
    lesson_time = models.IntegerField()

class TEACHER(models.Model):
    """教师表"""
    teacherid = models.IntegerField(primary_key=True)
    xiid = models.IntegerField()
    name = models.CharField(max_length=20)
    sex =models .CharField(max_length=32,choices=gender,default='男')
    age = models.IntegerField()
    password = models.CharField(max_length=256,default='123456')
    perid = models.CharField(max_length=32)
    zhicheng = models.CharField(max_length=32)

class PAIKE(models.Model):
    """排课表"""
    lessionid = models.IntegerField()
    teacherid = models.IntegerField()
    jclassid = models.IntegerField()

class XUANKE(models.Model):
    """选课表"""
    studentid = models.IntegerField()
    lessonid = models.IntegerField()
    latetime = models.IntegerField()
    kuangtime = models.IntegerField()
    jiatime = models.IntegerField()
    grade = models.FloatField()

class STUDENT(models.Model):
    """学生表"""
    studentid = models.IntegerField(primary_key=True)
    xiid = models.IntegerField()
    perid = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    sex = models .CharField(max_length=32,choices=gender,default='男')
    age = models.IntegerField()
    xclassid = models.IntegerField()
    password = models.CharField(max_length=128,default='123456')

class XCLASS(models.Model):
    """行政班表"""
    xclassid = models.IntegerField(primary_key=True)
    xiid = models.IntegerField()
    name = models.CharField(max_length=32)
    teacherid =  models.IntegerField()
    jieshao = models.CharField(max_length=128)

class QIANDAO(models.Model):
    """签到状态表"""
    studentid = models.IntegerField()
    jclassid = models.IntegerField()
    zhuangtai = models.CharField(max_length=10)

class XI(models.Model):
    """系别表"""
    xiid = models.IntegerField(primary_key=True)
    xizhurenid = models.IntegerField()
    name = models.CharField(max_length=32)
    jeishao = models.CharField(max_length=128)

class QINGJIA(models.Model):
    """请假表"""
    use = (
        ('是','是'),
        ('否','否'),
        )
    tai = (
        ('待审','待审'),
        ('同意','同意'),
        ('不同意','不同意'),
    )
    qingid = models.AutoField(primary_key=True)
    studentid = models.IntegerField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    zhuangtai = models.CharField(max_length=32,choices=tai,default='待审')
    cause = models.CharField(max_length=256)
    is_xiao = models.CharField(max_length=32,choices=use,default='否')

class XIAOJIA(models.Model):
    xiajiaid = models.IntegerField(primary_key=True)
    time = models.DateTimeField()









