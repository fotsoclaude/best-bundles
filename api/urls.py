from django.urls import path

from .views import *

urlpatterns = [
    path('datas/', load_datas),
    path('choices/', get_choice)
]
