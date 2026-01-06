"""
Definition of urls for printmanager.
"""

from django.urls import path,include
from django.urls import re_path
from django.contrib import admin


urlpatterns = [
    re_path(r'^com/', include(('common.urls','apps'), namespace = 'common')),
    re_path(r'^watcher/', include(('watcher.urls','apps'), namespace = 'watcher')),  
     re_path(r'^generator/', include(('generator.urls','apps'), namespace = 'generator')),   
  
]
 