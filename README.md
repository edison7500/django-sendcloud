# django-sendcloud
send cloud django 插件


## GUID

**Install** 

```
python setup.py install
```

** 在 Django 的 settings.py 加入** 

```
EMAIL_BACKEND = 'sendcloud.SendCloudBackend'
MAIL_APP_USER = '***' #使用api_user和api_key进行验证    
MAIL_APP_KEY = '***'
```