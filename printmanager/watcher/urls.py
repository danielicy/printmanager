from django.urls import re_path
from watcher import views
 

urlpatterns = [
    re_path(r'^$', views.test, name='test'),
    
]

 