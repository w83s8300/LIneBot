from django.db import models

# Create your models here.
class User_Info(models.Model):
    uid = models.CharField(max_length=50,null=False,default='')         #user_id
    uid_notify = models.CharField(max_length=100,null=False,default='')         #user_id
    name = models.CharField(max_length=255,blank=True,null=False)       #LINE名字
    pic_url = models.CharField(max_length=255,null=False)               #大頭貼網址
    mtext = models.CharField(max_length=255,blank=True,null=False)      #文字訊息紀錄
    mdt = models.DateTimeField(auto_now=True)                           #物件儲存的日期時間
    isDelete = models.IntegerField(default=0)                              #是否移除
    last_message= models.TextField(null=False,default='')
    def __str__(self):
        return self.uid

class User_text_Log(models.Model):
    Info_ID = models.IntegerField(default=0)    
    L_uid = models.CharField(max_length=50,null=False,default='')         #user_id
    L_uid_notify = models.CharField(max_length=100,null=False,default='')         #user_id
    L_name = models.CharField(max_length=255,blank=True,null=False)       #LINE名字
    L_mtext = models.CharField(max_length=255,blank=True,null=False)      #文字訊息紀錄
    L_Rmtext = models.CharField(max_length=255,blank=True,null=False)      #回的文字訊息紀錄
    L_mdt = models.DateTimeField(auto_now=True)                           #物件儲存的日期時間
    def __str__(self):
        return self.uid
    
class Test(models.Model):
    name = models.CharField(max_length=20)

