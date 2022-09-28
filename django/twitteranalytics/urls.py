from django.urls import path, include
from .views import *

app_name='twitteranalytics'
urlpatterns=[
    path(r'', IndexView.as_view(template_name='src/index.html'), name='index'),
]