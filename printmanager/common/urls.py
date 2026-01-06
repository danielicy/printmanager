from django.urls import re_path
 
from common import views
 
urlpatterns = [
    re_path(r'^rest$', views.test, name='test'),
    #This URL gets password  and returns the password encrypted
    re_path(r'^pass/(?P<password>[^/]+)$', views.getpass, name='test'),
]