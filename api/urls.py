from django.urls import path

from .views import *

urlpatterns = [
    path('datas/', load_datas),
    path('choices/', UserChoiseAPI.as_view())
]
